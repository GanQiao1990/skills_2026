---
name: disco-protein-design-operations
description: "Class-level operating guide for DISCO protein/enzyme design projects: uv setup, HF mirror weight handling, DeepSpeed/CUDA workarounds, ligand-conditioned inputs, multi-enzyme pathway configs, serial GPU-safe execution, monitoring, and troubleshooting. Use for any DISCO setup, inference, ligand-conditioned design, or pathway-scale enzyme design task."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mlops, protein-design, enzyme-design, DISCO, GPU, HuggingFace, workflow]
---

# DISCO Protein Design Operations

Use this umbrella skill for the full class of DISCO work: first-time repo setup, smoketest inference, ligand-conditioned generation, multi-ligand enzyme active-site design, pathway-scale multi-enzyme campaign setup, and GPU-safe long-running production runs.

## Core workflow

1. **Set up the repo with uv**
   ```bash
   cd /home/qiao/qiao_design/DISCO
   uv sync
   source .venv/bin/activate
   ```

2. **Stabilize Hugging Face downloads / mirrors**
   ```bash
   export HF_ENDPOINT=https://hf-mirror.com
   export HF_HUB_DISABLE_SAFETENSORS_CONVERSION=1
   export HF_HUB_ETAG_TIMEOUT=200
   export HF_HUB_DOWNLOAD_TIMEOUT=200
   export HF_HUB_DISABLE_TELEMETRY=1
   export HF_HUB_DISABLE_PROGRESS_BARS=1
   ```

3. **Avoid common CUDA / DeepSpeed failures**
   - Pin a real CUDA path per run, e.g. `CUDA_HOME=/usr/local/cuda-12.1`.
   - Pass `use_deepspeed_evo_attention=false` unless the CUDA extension environment is known-good.
   - For memory fragmentation, set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.

4. **Run a minimal smoketest before production**
   ```bash
   CUDA_HOME=/usr/local/cuda-12.1 python runner/inference.py \
     use_deepspeed_evo_attention=false \
     experiment=designable \
     effort=fast \
     input_json_path=input_jsons/unconditional_config.json \
     seeds='[0]' \
     dump_dir=./_hermes_smoketest_output
   ```
   Verify `pdbs/*.pdb` and `sequences/*.txt` exist before building a larger campaign.

## Ligand-conditioned design pattern

- Write DISCO input JSON as a list of jobs.
- Protein length is controlled by the input protein sequence length, not the job name.
- Include every explicit substrate, cofactor, metal proxy, or condition molecule as a ligand entry.
- Validate every SDF with RDKit before launching a GPU run.
- Be careful about path semantics: different DISCO configs observed both `FILE_<path>` and plain project-root-relative paths. When a run fails with `Bad input file`, inspect the exact resolved path in the traceback and adapt the JSON path convention for that checkout.

## Multi-enzyme pathway campaigns

For pathway-scale enzyme design:
1. Convert the biochemical reaction table into one JSON config per enzyme.
2. Build a cofactor / metal / aqueous-condition matrix per step.
3. Prioritize rate-limiting steps first.
4. Keep `count: 1` in JSON and run many seeds as separate Python invocations.
5. Save logs per enzyme and per seed.
6. Produce a small project index: reaction table, JSON inventory, SDF inventory, run script, and validation checklist.

## GPU-safe serial execution

Large `count` or many seeds in one Hydra invocation can OOM on a 40GB GPU. Prefer a shell loop:

```bash
for seed in 0 1 2 3 4 5 6 7 8 9; do
  CUDA_HOME=/usr/local/cuda-12.1 python runner/inference.py \
    use_deepspeed_evo_attention=false \
    experiment=diverse \
    effort=max \
    input_json_path=input_jsons/<task>_1.json \
    seeds="[$seed]" \
    dump_dir=./_<task>_serial \
    > ./_<task>_serial/logs/seed_${seed}.log 2>&1
  sync
  sleep 2
done
```

For multiple enzymes, finish all seeds for one enzyme before starting the next, and optionally clear CUDA cache between stages.

## Monitoring and diagnosis

Check all three before deciding a job is alive or dead:
```bash
nvidia-smi
ps -ef | grep -E 'runner/inference.py' | grep -v grep || true
find <dump_dir>/pdbs -maxdepth 1 -name '*.pdb' | wc -l
```
Sparse GPU polling can catch gaps between serial seeds; inspect the loop log for authoritative progress.

## Common pitfalls

- Polluted `CUDA_HOME` containing `:` causes `.../bin/nvcc` `FileNotFoundError`.
- HF mirror timeouts often improve with the HF hub timeout env vars and reruns after cache warm-up.
- Hidden control characters from chat copy/paste can make `cd` fail with `too many arguments`.
- PubChem 3D SDF downloads can 503; use RDKit/OpenBabel generation or cached SDFs and validate them before DISCO.
- Placeholder SDFs without real atom/bond records are rejected by RDKit/DISCO.

## Demoted reference notes

Detailed session-specific recipes were moved into support references under this skill:
- `references/ligand-conditioned-serial-design-hf-mirror.md`
- `references/uv-setup-and-ligand-conditioned-design.md`
- `references/uv-inference-smoketest-hf-mirror.md`
- `references/multi-enzyme-pathway-design.md`

Read those references when you need the exact historical command sequence, molecule examples, or project-specific troubleshooting details.
