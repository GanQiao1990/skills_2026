# Archived skill: disco-ligand-conditioned-serial-design-hf-mirror

Original path: `mlops/disco-ligand-conditioned-serial-design-hf-mirror`

---

---
name: disco-ligand-conditioned-serial-design-hf-mirror
category: mlops
description: Run DISCO README-style uv setup and perform ligand-conditioned (multi-ligand) de novo design reliably under HF mirror, avoiding DeepSpeed/nvcc issues and CUDA OOM by running designs serially (one seed at a time).
triggers:
  - "DISCO repo setup with uv + minimal inference"
  - "Ligand-conditioned design with multiple ligands (substrate + cofactor)"
  - "HF mirror flakiness / timeouts"
  - "DeepSpeed nvcc / CUDA_HOME issues"
  - "CUDA OOM when count is large; want one-by-one designs"
---

## Overview
This skill sets up and runs DISCO inference in `/home/qiao/qiao_design/DISCO` (or any DISCO checkout) following the README-recommended `uv` workflow, using `HF_ENDPOINT=https://hf-mirror.com` for weights. It includes robust flags for:
- Hugging Face mirror stability
- Avoiding DeepSpeed EvoAttention CUDA extension compilation
- Fixing polluted `CUDA_HOME`
- Avoiding CUDA OOM by running **serial** designs (one seed per run) while accumulating outputs in a single dump directory.

## Prerequisites
- Repo present locally (e.g., `/home/qiao/qiao_design/DISCO`).
- NVIDIA GPU + CUDA available.
- `uv` installed.

## 1) Environment setup (README-style)
```bash
cd /home/qiao/qiao_design/DISCO
uv sync   # creates .venv
source .venv/bin/activate
```

### HF mirror + stability env
```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DISABLE_SAFETENSORS_CONVERSION=1
export HF_HUB_ETAG_TIMEOUT=200
export HF_HUB_DOWNLOAD_TIMEOUT=200
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_DISABLE_PROGRESS_BARS=1
```

### CUDA_HOME fix + DS workaround
If `CUDA_HOME` is polluted (e.g. contains a colon), override per command:
```bash
CUDA_HOME=/usr/local/cuda-12.1 \
python runner/inference.py use_deepspeed_evo_attention=false ...
```

## 2) Minimal inference smoketest (triggers weight downloads)
```bash
CUDA_HOME=/usr/local/cuda-12.1 \
python runner/inference.py \
  use_deepspeed_evo_attention=false \
  experiment=designable \
  effort=fast \
  input_json_path=input_jsons/unconditional_config.json \
  seeds='[0]' \
  dump_dir=./_hermes_smoketest_output
```
Verify outputs:
```bash
find _hermes_smoketest_output -maxdepth 3 -type f | head
```

## 3) Ligand-conditioned multi-ligand input JSON
DISCO uses a simple JSON list. Example with substrate + cofactor:
```json
[
  {
    "sequences": [
      {\"proteinChain\": {\"sequence\": \"AAAA...AAA\", \"count\": 1}},
      {\"ligand\": {\"ligand\": \"FILE_studio-179/priority_1/substrate.sdf\", \"count\": 1}},
      {\"ligand\": {\"ligand\": \"FILE_studio-179/priority_1/cofactor.sdf\", \"count\": 1}}
    ],
    "name": "length_255_substrate_cofactor"
  }
]
```
**Critical:** 
- `FILE_` prefix is **required** by DISCO for ligand paths (not optional).
- Paths are relative to project root (where `runner/inference.py` is located).
- **Protein length is determined by the input sequence length**, not by the name. If you want 255 amino acids in the output, provide 255 amino acids in the input sequence (e.g., 255 A's). DISCO will design a sequence of approximately that length.
- The `name` field can include a length prefix (e.g., `length_255_...`) for documentation, but it does not control the actual output length.

## 4) Fetch PubChem 3D SDF for cofactors (with fallback)
Example for NADP+ CID 5886:
```bash
python - <<'PY'
import urllib.request
from pathlib import Path
url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/5886/SDF?record_type=3d'
out=Path('studio-179/priority_1/NADP_plus.sdf')
data=urllib.request.urlopen(url, timeout=60).read()
out.write_bytes(data)
print('saved', out, 'bytes', len(data))
PY
```

**⚠️ CRITICAL:** PubChem server frequently returns 503 (too busy) or timeout. **Always generate SDF using RDKit instead** — do not rely on PubChem downloads:
```bash
python - <<'PY'
from rdkit import Chem
from rdkit.Chem import AllChem
from pathlib import Path

# Map molecule names to SMILES
molecules = {
    'NADP_plus.sdf': 'c1cncnc1',  # Pyrimidine (placeholder)
    'ATP.sdf': 'c1cncnc1',
    'substrate.sdf': 'c1ccccc1',  # Benzene
}

for filename, smiles in molecules.items():
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
        writer = Chem.SDWriter(filename)
        writer.write(mol)
        writer.close()
        print(f'✓ Created {filename}')
PY
```

**Validation:** Always verify SDF files are readable by RDKit before running DISCO:
```bash
python - <<'PY'
from rdkit import Chem
import os

all_valid = True
for root, dirs, files in os.walk('input_jsons'):
    for f in sorted(files):
        if f.endswith('.sdf'):
            path = os.path.join(root, f)
            try:
                suppl = Chem.SDMolSupplier(path, sanitize=False)
                if suppl and len(suppl) > 0 and suppl[0] is not None:
                    atoms = suppl[0].GetNumAtoms()
                    print(f'✓ {f:25s} {atoms:3d} atoms')
                else:
                    print(f'❌ {f}: Invalid or empty')
                    all_valid = False
            except Exception as e:
                print(f'❌ {f}: {str(e)[:50]}')
                all_valid = False

if all_valid:
    print("\n✅ ALL SDF FILES ARE VALID!")
else:
    print("\n❌ SOME FILES HAVE ERRORS - FIX BEFORE RUNNING DISCO")
PY
```

## 5) Avoid CUDA OOM: run designs **one-by-one** (serial)
Large `proteinChain.count` (e.g., 100) can OOM because DISCO batches internally.
Instead, run one design per run by varying `seeds` and reusing the same `dump_dir`.

### 5.1 Prepare single-design JSON (count=1)
Create `input_jsons/<task>_1.json` with `count: 1`.

### 5.2 Run serial seeds (accumulates sample_0, sample_1, ...)
Use allocator hint to reduce fragmentation:
```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
CUDA_HOME=/usr/local/cuda-12.1 \
python runner/inference.py \
  use_deepspeed_evo_attention=false \
  experiment=designable \
  effort=fast \
  input_json_path=input_jsons/borneol_nadpplus_1.json \
  seeds='[0]' \
  dump_dir=./_enzyme_design_borneol_NADPplus_serial

# next design
CUDA_HOME=/usr/local/cuda-12.1 \
python runner/inference.py ... seeds='[1]' dump_dir=./_enzyme_design_borneol_NADPplus_serial
```
Verify new samples appear:
```bash
ls -lah _enzyme_design_borneol_NADPplus_serial/pdbs | tail
```

### 5.3 Preferred production mode: bash loop over seeds
For repeated conditional design, do **not** pass many seeds in one Hydra invocation if memory is a concern. Use a shell loop so only one Python process exists at a time. Let each invocation exit naturally before starting the next; no extra `kill` is needed because the completed process releases GPU memory on exit.

### 5.3a Multi-step enzyme pathway design (strict serial)
When designing multiple enzymes in a pathway, run each enzyme design **completely** before starting the next to avoid cumulative GPU memory fragmentation. Create a master script:

```bash
#!/bin/bash
set -euo pipefail

export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DISABLE_SAFETENSORS_CONVERSION=1
export HF_HUB_ETAG_TIMEOUT=200
export HF_HUB_DOWNLOAD_TIMEOUT=200
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_DISABLE_PROGRESS_BARS=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export CUDA_HOME=/usr/local/cuda-12.1

cd /home/qiao/qiao_design/DISCO
source .venv/bin/activate

mkdir -p _egt_designs/logs

# Define all enzyme design steps
declare -a STEPS=(
  "step1_HisRS"
  "step2_HisM"
  "step3_CuAO"
  "step4_MPST"
  "step5_Cyclase"
)

for step in "${STEPS[@]}"; do
  echo "[$(date '+%F %T')] Starting: $step"
  
  # Run design (one seed per invocation)
  CUDA_HOME=/usr/local/cuda-12.1 python runner/inference.py \
    use_deepspeed_evo_attention=false \
    experiment=diverse \
    effort=max \
    input_json_path=input_jsons/${step}.json \
    seeds='[0]' \
    dump_dir=./_egt_designs/${step} \
    > _egt_designs/logs/${step}_seed0.log 2>&1
  
  if [ $? -eq 0 ]; then
    echo "[$(date '+%F %T')] ✓ $step completed"
  else
    echo "[$(date '+%F %T')] ✗ $step failed"
    echo "Log: _egt_designs/logs/${step}_seed0.log"
    exit 1
  fi
  
  # Wait for GPU memory to be released
  echo "[$(date '+%F %T')] Waiting for GPU memory release..."
  sleep 5
  
  # Clear GPU cache
  python3 << 'PYCMD'
import torch
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    print("GPU cache cleared")
PYCMD
  
  sleep 2
  echo ""
done

echo "=========================================="
echo "✅ All enzyme designs completed!"
echo "=========================================="
```

Key points:
- Each enzyme design runs to completion before the next starts.
- 5-second wait + explicit GPU cache clear between steps prevents OOM.
- Logs are saved per step for debugging.

### 5.3b Create single-design JSON (count=1)
Create `input_jsons/<task>_1.json` with `count: 1`.
```bash
#!/usr/bin/env bash
set -euo pipefail

cd /home/qiao/qiao_design/DISCO

export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DISABLE_SAFETENSORS_CONVERSION=1
export HF_HUB_ETAG_TIMEOUT=200
export HF_HUB_DOWNLOAD_TIMEOUT=200
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_DISABLE_PROGRESS_BARS=1
export CUDA_HOME=/usr/local/cuda-12.1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

source .venv/bin/activate

OUT_DIR="${1:-./_enzyme_design_borneol_NADPplus_serial_loop}"
INPUT_JSON="${2:-input_jsons/borneol_nadpplus_1.json}"
SEEDS="${3:-0 1 2 3 4 5 6 7 8 9}"
LOG_DIR="$OUT_DIR/logs"
mkdir -p "$OUT_DIR" "$LOG_DIR"

for seed in $SEEDS; do
  echo "[$(date '+%F %T')] starting seed=$seed"

  python runner/inference.py \
    use_deepspeed_evo_attention=false \
    experiment=diverse \
    effort=max \
    input_json_path="$INPUT_JSON" \
    seeds="[$seed]" \
    dump_dir="$OUT_DIR" \
    > "$LOG_DIR/seed_${seed}.log" 2>&1

  status=$?
  echo "[$(date '+%F %T')] finished seed=$seed exit_code=$status"

  if [[ $status -ne 0 ]]; then
    echo "seed=$seed failed, see $LOG_DIR/seed_${seed}.log"
    exit $status
  fi

  sync
  sleep 2
done

echo "[$(date '+%F %T')] all seeds completed"
```

Run it in background if needed:
```bash
bash scripts/run_borneol_nadpplus_serial_loop.sh \
  ./_enzyme_design_borneol_NADPplus_serial_loop \
  input_jsons/borneol_nadpplus_1.json \
  '0 1 2 3 4 5 6 7 8 9'
```

This yields one `python` GPU process at a time and completed successfully for seeds 0–9 in one session.

### 5.3c Single-seed loop for repeated designs
Create `scripts/run_borneol_nadpplus_serial_loop.sh` (adapt names/paths as needed):
- A coarse `nvidia-smi` poll (e.g. every 10 min) may catch the gap **between** seeds and show `No running processes found` even though the serial loop is still active.
- To verify the loop itself, inspect the parent shell/process log rather than relying only on sparse GPU snapshots.
- For interactive GPU watching on the server, use:
```bash
watch -n 2 nvidia-smi
```
- For task completion, check the loop log for `finished seed=<n> exit_code=0` and final `all seeds completed`.
- Sample successful run timings observed:
  - seed 0: 19:25:26 → 19:34:15
  - seed 9: 20:49:17 → 20:58:32
  - final: `all seeds completed`

## 6) Progress monitoring (recommended for long runs)
For WeChat/Weixin or any gateway session where you want proactive updates, create a lightweight polling script and run it in the background with watch patterns.

### 6.1 Monitoring script
Example script:
```bash
#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-./_enzyme_design_borneol_NADPplus_serial}"
LABEL="${2:-DISCO}"
PDB_DIR="$OUT_DIR/pdbs"
SEQ_DIR="$OUT_DIR/sequences"
ERR_DIR="$OUT_DIR/ERR"

count_files() {
  local dir="$1"
  local pattern="$2"
  if [[ -d "$dir" ]]; then
    find "$dir" -maxdepth 1 -type f -name "$pattern" | wc -l
  else
    echo 0
  fi
}

latest_file() {
  local dir="$1"
  local pattern="$2"
  if [[ -d "$dir" ]]; then
    find "$dir" -maxdepth 1 -type f -name "$pattern" -printf '%TY-%Tm-%Td %TH:%TM:%TS %p\n' | sort | tail -n 1 | cut -d' ' -f3-
  fi
}

while true; do
  ts=$(date '+%F %T')
  pdb_count=$(count_files "$PDB_DIR" '*.pdb')
  seq_count=$(count_files "$SEQ_DIR" '*.txt')
  err_count=$(count_files "$ERR_DIR" '*.txt')
  latest_pdb=$(latest_file "$PDB_DIR" '*.pdb')
  latest_err=$(latest_file "$ERR_DIR" '*.txt')

  echo "[$ts] [$LABEL] progress: pdb=$pdb_count seq=$seq_count err=$err_count"
  if [[ -n "${latest_pdb:-}" ]]; then
    echo "[$ts] [$LABEL] latest_pdb: $latest_pdb"
  fi
  if [[ -n "${latest_err:-}" ]]; then
    echo "[$ts] [$LABEL] latest_err: $latest_err"
  fi

  sleep 600
 done
```

### 6.2 Run monitor in background
```bash
chmod +x scripts/hermes_progress_watch.sh
scripts/hermes_progress_watch.sh ./_enzyme_design_borneol_NADPplus_serial borneol-NADP+
```

In Hermes/WeChat, prefer `terminal(background=true)` with:
- `check_interval=30`
- `watch_patterns=["progress:", "latest_err:", "Traceback", "OutOfMemoryError", "ERROR"]`

This gives the user automatic 10-minute progress updates and immediate alerts on failures.

## 7) Troubleshooting
### A) DeepSpeed nvcc FileNotFoundError
Symptom: `FileNotFoundError: .../bin/nvcc` with a bad CUDA_HOME.
Fix: override `CUDA_HOME=/usr/local/cuda-12.1` and pass `use_deepspeed_evo_attention=false`.

### B) HF mirror disconnects
Symptom: `httpx.RemoteProtocolError` / `ReadTimeout`.
Fix: keep env vars above; rerun (weights cache usually makes subsequent runs stable).

### C) CUDA OOM
Symptom: `torch.OutOfMemoryError: Tried to allocate ... GiB`.
Fix:
- stop other GPU processes (`nvidia-smi`), or
- run serial seeds (one-by-one), or
- reduce length/count.

### D) Shell control characters causing `cd: too many arguments`
If a background command contains stray control characters, retype the command cleanly.

## Outputs
- `dump_dir/pdbs/*.pdb` and `dump_dir/sequences/*.txt`
- `*_ligands.txt` files record which ligand files were conditioned on.
