---
name: skill-drug-pipeline-operations
description: "Class-level guide for operating and hardening /home/qiao/qiao_design/skill_drug: local/offline model fallbacks, docking binary detection, ASKCOS retrosynthesis integration, PocketXMol generate-stage watchdog debugging, stale UI/meta repair, and end-to-end pipeline verification."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mlops, drug-discovery, docking, retrosynthesis, ASKCOS, PocketXMol, pipeline-debugging]
---

# skill_drug Pipeline Operations

Use this umbrella skill for recurring work on `/home/qiao/qiao_design/skill_drug` when the task involves making the pipeline run end-to-end, debugging stalled stages, integrating external retrosynthesis, or repairing local/offline fallbacks.

## Pipeline contract mindset

Always preserve the downstream file contracts unless a broader refactor is explicitly requested:
- embedding stage writes `cache/target_embedding.npz` and `cache/target_meta.json`
- generation writes candidate files such as `cache/candidates_raw.smi`
- docking writes `cache/docking_scores.csv` and pose files
- retrosynthesis writes `cache/routes.jsonl`
- route scoring writes `cache/route_scores.csv`
- emit writes `result.csv` / `result.zip`

A stage-level API success is not enough; verify the downstream artifact and the next consumer.

## Local/offline embedding and docking fallbacks

When Hugging Face or `hf-mirror.com` is unavailable:
- Do not assume local ESM `.pt` checkpoints are Hugging Face format.
- Use a fair-esm-capable interpreter if available, e.g. `/home/qiao/anaconda3/envs/dynamicbind/bin/python`.
- Load local fair-esm checkpoints via `esm.pretrained.load_model_and_alphabet(...)` in a subprocess if the main interpreter has incompatible `esm` 3.x.

When docking fails before any molecules dock:
- Do not trust executable name `smina`.
- Auto-detect explicit CLI arg, `SMINA_BIN`, `smina`, `vina`, and known local Vina binaries.
- Log the resolved binary path.

## ASKCOS retrosynthesis integration

For ASKCOS-backed retrosynthesis:
- Preserve `cache/routes.jsonl` shape for `route_economy.py` and emit.
- Read ASKCOS OpenAPI before guessing payload shape.
- Nest options under `build_tree_options` and `enumerate_paths_options`.
- Poll async tasks at `/api/celery/task/get?task_id=<id>`, not stale endpoint variants.
- Reconstruct routes from `result.uds.pathways` + `uuid2smiles` when no convenient `routes` list exists.
- Reorder steps so the last product equals the target SMILES before writing output.
- Validate route quality through downstream emit / `validate_result.py`, not just HTTP 200.

Operational default learned on the MIT deployment:
- prefer `mcts` with a short effective search time around 20 s
- retry transient `502/503/504`
- fallback to `retro-star` after repeated transient failures
- cap oversized user/API timeouts down if the deployment reliably 504s at long search windows

## PocketXMol generate-stage watchdog debugging

When the UI says a job is stuck in `generate`, check authoritative state:
1. `jobs/<job_id>/meta.json`
2. `jobs/<job_id>/result.log`
3. `jobs/<job_id>/cache/pxm_progress.json`
4. live processes for `sample_use.py` / PocketXMol
5. `cache/pxm_rounds/round_*_try_*/stderr.log`

Classify the failure:
- stale frontend/progress snapshot after failure
- post-processing stall
- watchdog kill (`stall_no_progress`, `stall_post_frozen`, `stall_no_start`, `hard_timeout`)
- over-parallelized single-GPU self-contention causing `returncode=-9`

Hardening pattern:
- log explicit terminal `generate error` events with the last failure reason
- clamp `POCKETXMOL_PARALLEL_ROUNDS` to the actual device pool size
- widen watchdog thresholds only after confirming slow post-processing rather than launcher/OOM failure

## Stale meta/UI repair

Before rerunning expensive stages, verify artifacts:
```bash
cd /home/qiao/qiao_design/skill_drug
wc -l jobs/<job_id>/result.csv jobs/<job_id>/cache/routes.jsonl jobs/<job_id>/cache/route_scores.csv jobs/<job_id>/cache/docking_scores.csv
unzip -l jobs/<job_id>/result.zip
python scripts/validate_result.py jobs/<job_id>/result.csv
ps -eo pid,etime,cmd | grep -F '<job_id>' | grep -v grep || true
```
If `result.csv` validates, `result.zip` exists, and no live process owns the job, repair `meta.json` rather than rerunning.

## Verification checklist

After any fix, run the smallest useful chain:
- syntax check edited scripts
- run the fixed stage on a small job or small `--max`
- inspect the stage output file
- run the immediate downstream stage
- verify final `pipeline.py --stage emit` / `validate_result.py` when retrosynthesis or scoring changed

## Demoted reference notes

Detailed session-specific recipes were moved into support references:
- `references/local-esm-vina-fallbacks.md`
- `references/askcos-retro-api-integration.md`
- `references/pocketxmol-generate-watchdog-debugging.md`
