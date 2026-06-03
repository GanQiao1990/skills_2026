# Archived skill: skill-drug-local-esm-vina-fallbacks

Original path: `mlops/skill-drug-local-esm-vina-fallbacks`

---

---
name: skill-drug-local-esm-vina-fallbacks
description: Debug and harden the /home/qiao/qiao_design/skill_drug pipeline when embed tries to fetch ESM2 from hf-mirror despite local checkpoints existing, and when docking fails because smina is missing from PATH.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# skill_drug local ESM + docking fallback repair

Use this when working on the project at `/home/qiao/qiao_design/skill_drug` and either of these happens:
- `embed` logs: `We couldn't connect to 'https://hf-mirror.com' ... facebook/esm2_t33_650M_UR50D`
- the machine already has local ESM2 `.pt` checkpoints
- `dock` fails with `FileNotFoundError: 'smina'`
- generation succeeded but docking did not start because the default docking binary is wrong

## Root-cause pattern

There are two separate issues.

1. `scripts/embed_target.py` originally tries only Hugging Face `transformers` with model name `facebook/esm2_t33_650M_UR50D`.
   - This fails offline or when `hf-mirror.com` times out.
   - Local files such as `esm2_t33_650M_UR50D.pt` are **fair-esm checkpoints**, not Hugging Face cache format.
   - The base Python may have `esm` from EvolutionaryScale (`esm 3.x`), which does **not** expose the old `esm.pretrained.load_model_and_alphabet` loader needed for these `.pt` files.
   - A different interpreter may still have old fair-esm; on this machine `/home/qiao/anaconda3/envs/dynamicbind/bin/python` works.

2. `scripts/dock.py` originally defaults to executable name `smina`.
   - If no `smina` is on PATH, docking crashes before any ligand is docked.
   - A working AutoDock Vina binary may still exist elsewhere, e.g. `/home/qiao/anaconda3/envs/vina/bin/vina`.

## Known-good local resources on this machine

### fair-esm checkpoints
- `/home/qiao/md/DynamicBind/esm_models/checkpoints/esm2_t33_650M_UR50D.pt`
- `/home/qiao/allatom/DiffPepBuilder/experiments/checkpoints/esm2_t33_650M_UR50D.pt`

### interpreters with old fair-esm loader
- `/home/qiao/anaconda3/envs/dynamicbind/bin/python`
- `/home/qiao/anaconda3/envs/diffpepbuilder/bin/python`

### working docking binaries
- `/home/qiao/anaconda3/envs/vina/bin/vina`
- `/home/qiao/docking/vina/vina_1.2.5_linux_x86_64`

## Repair procedure

### A. Fix embed to use local fair-esm fallback

Patch `scripts/embed_target.py` so `try_esm2()` does this in order:
1. Try a local fair-esm fallback first.
2. If that fails, optionally try Hugging Face `transformers`.
3. If both fail, log skip and proceed without embedding.

Implementation pattern:
- Add imports: `subprocess`, `tempfile`, `os`
- Add a helper `try_esm2_local(seq, logger)`
- In that helper:
  - choose a Python from:
    - `FAIR_ESM_PYTHON`
    - `/home/qiao/anaconda3/envs/dynamicbind/bin/python`
    - `/home/qiao/anaconda3/envs/diffpepbuilder/bin/python`
  - choose a checkpoint from:
    - `ESM2_LOCAL_CKPT`
    - `/home/qiao/md/DynamicBind/esm_models/checkpoints/esm2_t33_650M_UR50D.pt`
    - `/home/qiao/allatom/DiffPepBuilder/experiments/checkpoints/esm2_t33_650M_UR50D.pt`
  - run a small subprocess using the chosen Python that calls `esm.pretrained.load_model_and_alphabet(ckpt_path)`
  - save `sequence_emb` and `mean_emb` to a temporary `.npz`
  - load that `.npz` back in the parent process and return it
- Mark the embedding model as something like:
  - `fair-esm-local:/home/qiao/md/DynamicBind/esm_models/checkpoints/esm2_t33_650M_UR50D.pt`

Important: do **not** rely on the base interpreter’s `esm` package for local `.pt` loading unless it actually exposes `esm.pretrained.load_model_and_alphabet`.

### B. Fix dock to auto-detect a real binary

Patch `scripts/dock.py`:
- add `detect_docking_bin(explicit: str | None = None) -> str`
- probe in this order:
  1. explicit `--smina`
  2. env `SMINA_BIN`
  3. `shutil.which("smina")`
  4. `shutil.which("vina")`
  5. `/home/qiao/anaconda3/envs/vina/bin/vina`
  6. `/home/qiao/docking/vina/vina_1.2.5_linux_x86_64`
- use the resolved binary in logging and in `run_smina(...)`

Even though the helper is still named `run_smina`, Vina 1.2.5 accepts the same CLI flags used here and works as a drop-in binary for this script.

## Verification commands

### Verify old fair-esm loader exists
```bash
/home/qiao/anaconda3/envs/dynamicbind/bin/python - <<'PY'
import torch, esm.pretrained as p
ckpt='/home/qiao/md/DynamicBind/esm_models/checkpoints/esm2_t33_650M_UR50D.pt'
model, alphabet = p.load_model_and_alphabet(ckpt)
print(type(model).__name__, type(alphabet).__name__)
labels, strs, toks = alphabet.get_batch_converter()([('x','MKT')])
with torch.no_grad():
    out = model(toks, repr_layers=[33], return_contacts=False)
print(tuple(out['representations'][33].shape))
PY
```
Expected: model loads and prints a representation shape.

### Verify embed stage
```bash
cd /home/qiao/qiao_design/skill_drug
/home/qiao/anaconda3/bin/python scripts/embed_target.py \
  --pdb /home/qiao/qiao_design/skill_drug/jobs/<job_id>/AF-B4ZY91-F1-model_v6.pdb \
  --out /home/qiao/qiao_design/skill_drug/jobs/<job_id>
```
Expected:
- `cache/target_embedding.npz` exists
- `cache/target_meta.json` contains:
  - `embedding_model`
  - `embedding_dim`
- latest `result.log` `embed` record ends successfully without needing hf-mirror

### Verify dock stage
```bash
cd /home/qiao/qiao_design/skill_drug
/home/qiao/anaconda3/bin/python scripts/dock.py \
  --out /home/qiao/qiao_design/skill_drug/jobs/<job_id> \
  --cutoff -5
```
Expected:
- log shows `bin` resolved to a real Vina/Smina path
- `cache/docking_scores.csv` gets populated
- `cache/poses/` contains pose files

## Files typically involved
- `/home/qiao/qiao_design/skill_drug/scripts/embed_target.py`
- `/home/qiao/qiao_design/skill_drug/scripts/dock.py`
- `/home/qiao/qiao_design/skill_drug/.env`
- `/home/qiao/qiao_design/skill_drug/jobs/<job_id>/result.log`
- `/home/qiao/qiao_design/skill_drug/jobs/<job_id>/cache/target_meta.json`
- `/home/qiao/qiao_design/skill_drug/jobs/<job_id>/cache/target_embedding.npz`
- `/home/qiao/qiao_design/skill_drug/jobs/<job_id>/cache/docking_scores.csv`

## Pitfalls
- Do not assume local ESM `.pt` files are compatible with Hugging Face `AutoModel`.
- Do not assume `import esm` means fair-esm is installed; `esm 3.x` is a different package family.
- Do not trust the executable name `smina`; verify a real binary path exists.
- `dock.py` can fail before writing meaningful rows if the binary is missing; check for `FileNotFoundError` and an almost-empty `docking_scores.csv`.

## Minimal-fix philosophy
- Keep the original transformers path intact for environments where Hugging Face cache is available.
- Add only a local fallback for embedding and binary autodetection for docking.
- Do not redesign the whole pipeline just to fix offline embedding and missing-path docking.
