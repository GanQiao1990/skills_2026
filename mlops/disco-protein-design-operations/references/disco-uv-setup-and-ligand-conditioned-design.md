# Archived skill: disco-uv-setup-and-ligand-conditioned-design

Original path: `mlops/disco-uv-setup-and-ligand-conditioned-design`

---

---
name: disco-uv-setup-and-ligand-conditioned-design
description: Set up DISCO with uv, run smoketest inference to trigger weight downloads via HF mirror, prepare ligand SDFs, run ligand-conditioned design, handle OOM by serializing seeds, and monitor progress with scripts/cron.
version: 1.0
---

## When to use
- You need to set up `/home/qiao/qiao_design/DISCO` following README (uv-managed `.venv`).
- You want to run a minimal inference once to trigger automatic HuggingFace weight downloads (optionally via `HF_ENDPOINT` mirror).
- You want ligand-conditioned design (multi-ligand pocket) using SDF inputs.
- You hit CUDA OOM when generating many designs and need a robust serial/batched strategy.
- You want automated progress monitoring every N minutes.

## Prerequisites
- CUDA available (e.g., A100 40GB), driver ok.
- `uv` installed.

## Environment setup (README-recommended)
```bash
cd /home/qiao/qiao_design/DISCO
export HF_ENDPOINT=https://hf-mirror.com
uv sync   # creates .venv
source .venv/bin/activate
```

## Minimal inference (smoketest) to trigger model downloads
Run a small unconditional job once to populate `~/.cache/huggingface`.
```bash
cd /home/qiao/qiao_design/DISCO
export HF_ENDPOINT=https://hf-mirror.com
source .venv/bin/activate
CUDA_HOME=/usr/local/cuda-12.1 \
python runner/inference.py \
  use_deepspeed_evo_attention=false \
  experiment=designable \
  effort=fast \
  input_json_path=input_jsons/unconditional_config.json \
  seeds='[0]' \
  dump_dir=./_hermes_smoketest_output
```
Notes:
- Avoid DeepSpeed EvoAttention compile issues by setting `use_deepspeed_evo_attention=false`.
- If HF rate limits appear, consider setting `HF_TOKEN`.

## Prepare ligands (SDF)
### Substrate from chiral SMILES (RDKit)
```bash
cd /home/qiao/qiao_design/DISCO
source .venv/bin/activate
python - <<'PY'
from rdkit import Chem
from rdkit.Chem import AllChem
from pathlib import Path
outdir = Path('studio-179/priority_1'); outdir.mkdir(parents=True, exist_ok=True)
smiles = "[C@H]1(O)[C@@]2(C)CC[C@@H]1C(C)(C2)C"  # (1R,2S,4R)-borneol skeleton
mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
AllChem.UFFOptimizeMolecule(mol, maxIters=200)
mol = Chem.RemoveHs(mol)
mol.SetProp('_Name','borneol_1R2S4R')
Chem.SDWriter(str(outdir/'borneol_1R2S4R.sdf')).write(mol)
print('wrote', outdir/'borneol_1R2S4R.sdf')
PY
```

### Cofactor from PubChem (recommended)
Example: NADP+ CID 5886 3D SDF.
```bash
cd /home/qiao/qiao_design/DISCO
python - <<'PY'
from pathlib import Path
import urllib.request
url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/5886/SDF?record_type=3d'
out=Path('studio-179/priority_1/NADP_plus.sdf')
data=urllib.request.urlopen(url, timeout=60).read()
out.write_bytes(data)
print('saved', out, 'bytes', len(data))
PY
```

## Create ligand-conditioned input JSON
DISCO expects an array of jobs. Protein length is expressed as a dash string, and ligands are `FILE_...` references.
Example for length 200 with two ligands:
```json
[
  {
    "sequences": [
      {"proteinChain": {"sequence": "----...----", "count": 1}},
      {"ligand": {"ligand": "FILE_studio-179/priority_1/borneol_1R2S4R.sdf", "count": 1}},
      {"ligand": {"ligand": "FILE_studio-179/priority_1/NADP_plus.sdf", "count": 1}}
    ],
    "name": "length_200_borneol_NADPplus"
  }
]
```
Tip: copy the exact dash-length from existing configs (e.g., warfarin) to avoid miscounting.

## Run design: start small, then scale
### Serial (one-by-one) to avoid CUDA OOM
OOM was observed when requesting large `count` (e.g., 100) on A100 40GB. A robust strategy is to run with `count=1` and increment seeds.

Run seed 0:
```bash
cd /home/qiao/qiao_design/DISCO
export HF_ENDPOINT=https://hf-mirror.com
source .venv/bin/activate
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
CUDA_HOME=/usr/local/cuda-12.1 \
python runner/inference.py \
  use_deepspeed_evo_attention=false \
  experiment=designable \
  effort=fast \
  input_json_path=input_jsons/borneol_nadpplus_1.json \
  seeds='[0]' \
  dump_dir=./_enzyme_design_borneol_NADPplus_serial
```
Repeat with `seeds='[1]'`, `seeds='[2]'`, etc. Each seed should produce `sample_<seed>.pdb`.

### If you must do batches
- Try reducing `count` (e.g., 25) and/or free GPU memory (`nvidia-smi` to identify other processes).
- Prefer multiple runs that aggregate outputs, rather than a single huge run.

## Verify execution status
```bash
cd /home/qiao/qiao_design/DISCO
nvidia-smi
ps -ef | egrep 'runner/inference.py' | grep -v egrep || true
ls -1 _enzyme_design_borneol_NADPplus_serial/pdbs | egrep 'sample_[0-9]+\.pdb$' | wc -l
```
Note: In serial mode GPU may be idle between runs; check output directory growth.

## Progress monitoring script
Create `scripts/serial_design_monitor.py` to count `sample_*.pdb` and print JSON on changes.
Key behaviors:
- Polls `outdir/pdbs/*.pdb`
- Extracts sample indices from filenames
- Prints only when count changes

## Optional: schedule updates every 10 minutes
Use a cronjob that counts samples and sends a concise message to the desired channel.

## Pitfalls / Lessons learned
- Large `count` can trigger CUDA OOM (e.g., attempted allocation ~47.76 GiB on 40GB A100).
- Other running Python processes can consume GPU memory; reduce concurrency.
- Make sure shell commands don’t contain hidden control characters; they can cause `cd: too many arguments`.
- The platform may show “machine not running” because the job finished and GPU is idle; always confirm via output files.
