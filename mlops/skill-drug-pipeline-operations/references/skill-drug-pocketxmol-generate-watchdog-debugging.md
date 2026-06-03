# Archived skill: skill-drug-pocketxmol-generate-watchdog-debugging

Original path: `mlops/skill-drug-pocketxmol-generate-watchdog-debugging`

---

---
name: skill-drug-pocketxmol-generate-watchdog-debugging
description: Investigate and harden skill_drug PocketXMol generate-stage jobs that appear stuck, but are actually stalled, watchdog-killed, or leaving stale progress snapshots.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# skill_drug PocketXMol generate/watchdog debugging

## When to use

Use this when working in `/home/qiao/qiao_design/skill_drug` and a job appears stuck during the `generate` stage, especially when:
- the UI or user says a job has been "stuck" for a long time
- `meta.json` shows `current_stage: generate` or `error_stage: generate`
- `result.log` stops after `pxm_heartbeat` or `pxm_round_start`
- `cache/pxm_progress.json` shows an old snapshot that makes the frontend look live even though the run is over
- PocketXMol `stderr.log` shows long `Post process generated mols` stretches, repeated reconstruction warnings, or output that continues past the last `result.log` heartbeat
- the user wants to know whether the job is truly running, falsely appears stuck, or was killed by the watchdog

## Class of problem

This is a class of `skill_drug` failures where PocketXMol generation is not cleanly observable from the UI because the frontend reads stale progress state, while the actual subprocess has already stalled, been watchdog-killed, or exited without a clear final `generate error` summary.

## Root-cause pattern

There are usually two layers:

1. **Real generation trouble**
   - PocketXMol sampling may finish a batch, then hang or crawl during post-processing / reconstruction.
   - The watchdog can kill a round with reasons like:
     - `stall_no_progress`
     - `stall_post_frozen`
     - `stall_no_start`
     - `hard_timeout`
   - This often happens after some molecules were already written, so the run looks partially alive.

2. **Observability gap**
   - `cache/pxm_progress.json` can remain at the last heartbeat from a failed attempt.
   - `result.log` may stop before a clear terminal `generate error` event is written.
   - The UI may therefore look stuck even though no PocketXMol process is still running.

## Investigation workflow

### 1. Check authoritative job state first

Inspect:
- `jobs/<job_id>/meta.json`
- `jobs/<job_id>/result.log`
- `jobs/<job_id>/cache/pxm_progress.json`

What to look for:
- `status: error`
- `error_stage: generate`
- last `result.log` event such as `pxm_watchdog_kill`, `pxm_round_fail`, or missing completion
- whether `pxm_progress.json` is obviously older than now and frozen at an early attempt snapshot

### 2. Check whether anything is actually still running

Use process inspection, e.g. look for:
- `sample_use.py`
- `sample.py`
- project-specific Python processes

If no PocketXMol subprocess exists, the job is **not** truly still running even if the UI looks active.

### 3. Read the PocketXMol stderr, not just result.log

Inspect:
- `jobs/<job_id>/cache/pxm_rounds/round_*_try_*/stderr.log`
- `.../log.txt`
- `.../gen_info.csv`

Important pattern:
- `result.log` may stop at an early heartbeat
- but `stderr.log` can show later `Success:` lines or `Post process generated mols` movement
- this means the generate subprocess continued longer than the high-level heartbeat stream suggests

### 4. Distinguish stale UI from real live work

A job is usually only *apparently* stuck when all of these are true:
- `meta.json` already says `error`
- no live PocketXMol process exists
- `pxm_progress.json` still contains an old heartbeat
- `stderr.log` has no fresh writes anymore

### 5. Identify which watchdog path fired

Search `result.log` for:
- `pxm_watchdog_kill`
- `pxm_round_fail`
- `pxm_round_giveup`

Map common meanings:
- `stall_no_progress` = both file progress and stderr signal stopped for too long
- `stall_post_frozen` = post-process bar stayed at the same `(pct, cur)` too long
- `stall_no_start` = no molecules and no stderr signal after startup grace
- `hard_timeout` = absolute round timeout hit

## Code locations that matter

- `scripts/generate.py`
  - `_run_pxm_with_watchdog(...)`
  - `try_pocketxmol(...)`
  - watchdog env vars:
    - `POCKETXMOL_STALL_SEC`
    - `POCKETXMOL_POST_STALL_SEC`
    - `POCKETXMOL_POLL_SEC`
    - `POCKETXMOL_ROUND_TIMEOUT_SEC`
    - `POCKETXMOL_STARTUP_GRACE_SEC`
- `api/main.py`
  - `_run_one_stage(...)`
  - `_run_pipeline(...)`
  - `meta.json` status transitions for `generate`

## Proven hardening improvement

If `try_pocketxmol(...)` returns `False` after all rounds/attempts fail, make sure `generate.py` logs an explicit terminal event before exiting, e.g.:
- `stage=generate`
- `event=error`
- `reason=no generation backend succeeded`
- `pxm_last_failure_reason=<last watchdog or empty-results reason>`

This prevents ambiguous jobs where:
- `meta.json` says `generate=error`
- but `result.log` never tells the user *why*

Also track a `last_failure_reason` across attempts so the final log preserves the real failure mode.

## Additional failure mode: over-parallelized single-GPU runs

A separate class of generate failures is **self-contention**, not a true stall.

Pattern:
- `.env` sets `POCKETXMOL_PARALLEL_ROUNDS` to a large value
- `POCKETXMOL_DEVICE` still points to only one GPU, e.g. `cuda:0`
- `result.log` shows many concurrent `pxm_round_start` events
- each round dies with `pxm_round_fail`, `reason=nonzero_rc`, `returncode=-9`
- `stderr.log` may show normal startup and partial `Sampling steps` progress, then stop abruptly with no Python traceback
- GPU snapshots in heartbeats may look misleadingly idle because many short-lived competing processes are starting and dying on the same device

Interpretation:
- PocketXMol parallelism is only safe when you have an explicit multi-device pool.
- Multiple `sample_use.py` processes all targeting `cuda:0` can kill each other or be OOM-killed without a clean exception.

Hardening fix:
- Parse `POCKETXMOL_DEVICE` as a device list (comma/space separated).
- Clamp effective parallel rounds to `min(requested_parallel, rounds, len(device_pool))`.
- If only one device is configured, force serial execution even if `POCKETXMOL_PARALLEL_ROUNDS` is larger.
- Log a `pxm_parallel_adjusted` event so the reason is visible in `result.log`.

## Configuration guidance

If post-processing is genuinely slow rather than dead, widen the watchdog thresholds before rerunning:

Suggested conservative values:
```bash
POCKETXMOL_STALL_SEC=1200
POCKETXMOL_POST_STALL_SEC=600
```

Why:
- default post-process timing can vary widely across targets
- reconstruction / AR cleanup may take much longer than nominal per-item rates
- too-small thresholds can kill a slow but still progressing round

## Verification checklist after patching

After code/config changes, verify all of the following on the next reproduce:
- `result.log` records any final generate failure explicitly
- if a round is killed, the reason appears in `result.log`
- `meta.json` status agrees with the real subprocess state
- stale `pxm_progress.json` no longer misleads debugging because `result.log` now has a clear terminal explanation
- if the run truly completes, you get:
  - `generate end`
  - `cache/candidates_raw.smi`
  - optionally `cache/pxm_cfd.csv`

## Pitfalls

- Do **not** trust the frontend alone to determine liveness.
- Do **not** assume the last heartbeat in `result.log` is the last real subprocess activity.
- Do **not** treat `pxm_progress.json` as authoritative after a failure.
- A missing live process plus an old progress snapshot usually means stale state, not active compute.
- Repeated `Reconstruction error encountered` warnings do not by themselves prove a hang; inspect whether the post-process bar or `[Pool]` summary still advances.

## Minimal-fix philosophy

- First improve observability and determine whether the run truly died or only looked stuck.
- Prefer logging the last real failure reason over redesigning the whole generate stage.
- Tune watchdog thresholds only after confirming the problem is slow/frozen post-processing rather than an unrelated launcher failure.
