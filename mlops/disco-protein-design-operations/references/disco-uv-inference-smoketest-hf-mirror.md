# Archived skill: disco-uv-inference-smoketest-hf-mirror

Original path: `mlops/disco-uv-inference-smoketest-hf-mirror`

---

---
name: disco-uv-inference-smoketest-hf-mirror
description: Setup DISCO repo with uv, work around deepspeed/nvcc CUDA_HOME issues, and run a minimal inference to trigger HF weight downloads via hf-mirror.
triggers:
  - "DISCO repo setup"
  - "uv sync + run inference"
  - "deepspeed nvcc FileNotFoundError"
  - "HF mirror timeouts / safetensors conversion thread"
---

## Goal
In `/home/qiao/qiao_design/DISCO`, create `.venv` via `uv sync`, then run a minimal inference to trigger automatic weight downloads. Use `HF_ENDPOINT=https://hf-mirror.com` and apply mitigations for (1) DeepSpeed nvcc/CUDA_HOME issues and (2) hf-mirror timeouts.

## Steps

1) **cd into repo**
```bash
cd /home/qiao/qiao_design/DISCO
```

2) **Set HF mirror env**
```bash
export HF_ENDPOINT=https://hf-mirror.com
# Reduce flaky background calls on mirrors (safetensors conversion / metadata)
export HF_HUB_DISABLE_SAFETENSORS_CONVERSION=1
export HF_HUB_ETAG_TIMEOUT=200
export HF_HUB_DOWNLOAD_TIMEOUT=200
```

3) **Create/Sync venv with uv**
```bash
uv sync
```

4) **Activate venv**
```bash
source .venv/bin/activate
```

5) **Run minimal inference (triggers weight download)**
Work around DeepSpeed `nvcc` import issues by disabling DS evo attention and pinning `CUDA_HOME`.

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

## Verification
- Outputs should appear under `dump_dir`:
  - `./_hermes_smoketest_output/pdbs/*.pdb`
  - `./_hermes_smoketest_output/sequences/*.txt`

## Common pitfalls

### Hidden control characters in multi-line commands (chat copy/paste)
Symptoms:
- `bash: cd: too many arguments`

Cause:
- Some chat clients can inject ESC/control codes when copying multi-line commands (especially when they include ANSI escapes).

Fix:
- Prefer a single chained command line using `&&`.
- If you must use multi-line, retype the `cd ...` line manually.

### DeepSpeed / nvcc error
Symptoms:
- `FileNotFoundError: .../bin/nvcc`
- Often with an invalid path like: `/usr/local/cuda:/usr/local/cuda/bin/nvcc`

Cause:
- `CUDA_HOME` is polluted (contains `:`), so DeepSpeed constructs an invalid nvcc path.

Fix:
- Pin a valid CUDA install per-run, e.g. `CUDA_HOME=/usr/local/cuda-12.1`.
- Keep `use_deepspeed_evo_attention=false` to reduce nvcc dependency.

### HF mirror disconnect/timeout
Symptoms:
- `httpx.RemoteProtocolError: Server disconnected without sending a response`
- `httpx.ReadTimeout`

Cause:
- hf-mirror can be intermittently flaky during hub metadata calls or safetensors conversion checks.

Mitigations:
```bash
export HF_HUB_DISABLE_SAFETENSORS_CONVERSION=1
export HF_HUB_ETAG_TIMEOUT=200
export HF_HUB_DOWNLOAD_TIMEOUT=200
```

### CUDA OOM when increasing `count`
Symptoms:
- `torch.OutOfMemoryError: CUDA out of memory. Tried to allocate ...`

Cause:
- Setting `proteinChain.count` high can increase batch memory.
- Other GPU processes can reduce available memory.

Fix options:
- Run designs serially by keeping `count=1` and varying `seeds`.
- Or run in smaller chunks (e.g. `count=25` repeated 4 times).
- Optionally reduce fragmentation:
```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

## Notes (weights)
Primary required weights typically include:
- DISCO checkpoint: `DISCO-Design/DISCO` (e.g., `DISCO.pt` in HF cache)
- DPLM-650M: `airkingbd/dplm_650m` (either `pytorch_model.bin` or `model.safetensors` plus tokenizer files)
