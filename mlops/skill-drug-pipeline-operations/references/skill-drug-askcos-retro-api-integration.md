# Archived skill: skill-drug-askcos-retro-api-integration

Original path: `mlops/skill-drug-askcos-retro-api-integration`

---

---
name: skill-drug-askcos-retro-api-integration
description: Replace the /home/qiao/qiao_design/skill_drug retrosynthesis stage with ASKCOS tree-search API calls, using the MIT ASKCOS deployment and preserving cache/routes.jsonl for downstream route scoring and emit.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# skill_drug ASKCOS retrosynthesis API integration

Use this when working on `/home/qiao/qiao_design/skill_drug` and the local retrosynthesis stage should use ASKCOS instead of AiZynthFinder or RXN.

## When to use
- `scripts/retro.py` currently depends on local `aizynthfinder`
- local AiZynthFinder assets are missing or cannot be downloaded
- the user wants ASKCOS / `askcos.mit.edu`
- downstream code still expects `cache/routes.jsonl`

## Goal
Swap only the retro stage backend while keeping the downstream contract unchanged:
- input: `cache/docking_scores.csv`
- output: `cache/routes.jsonl`
- consumers left unchanged: `route_economy.py`, `pipeline.py`, API readers

## Proven working approach

### 1. Replace local retrosynthesis with ASKCOS tree-search API
Patch `/home/qiao/qiao_design/skill_drug/scripts/retro.py` to:
- call ASKCOS instead of importing `aizynthfinder`
- read config from env / CLI:
  - `ASKCOS_BASE_URL`
  - `ASKCOS_RETRO_PLANNER`
  - `ASKCOS_REQUEST_TIMEOUT`
  - `ASKCOS_ACCESS_TOKEN`
- support planners:
  - `mcts`
  - `retro-star`

Known-good default base URL:
- `https://askcos.mit.edu`

### 2. Do NOT send flat payload fields
Initial naive payloads like:
- `smiles`
- `expansion_time`
- `max_depth`
- `max_branching`
- `return_first`

cause HTTP 422 with `extra_forbidden`.

Correct request shape comes from ASKCOS OpenAPI and must nest options under:
- `build_tree_options`
- `enumerate_paths_options`

Known-good MCTS payload pattern:
```json
{
  "smiles": "CCO",
  "build_tree_options": {
    "expansion_time": 30,
    "max_depth": 6,
    "max_branching": 25,
    "return_first": false
  },
  "enumerate_paths_options": {
    "path_format": "json",
    "json_format": "nodelink",
    "max_paths": 50
  }
}
```

For `retro_star`, omit `max_branching` unless explicitly supported by that schema.

### 3. Result parsing is NOT route-list shaped
Do not assume ASKCOS returns a convenient `routes` or `steps` list.

In practice, useful route data may come back under:
- `result.uds.pathways`
- `result.uds.uuid2smiles`

The `pathways` entries are edge lists, and reaction SMILES are recovered by mapping node UUIDs through `uuid2smiles`. A practical fallback is:
- iterate each pathway edge list
- for each edge, map `source` and `target` via `uuid2smiles`
- whichever mapped node contains `>>` is a reaction node
- collect unique reaction SMILES in pathway order
- emit them as `steps: [{"rxn_smiles": ...}]`

This is sufficient to preserve the existing downstream `routes.jsonl` format.

### 4. Async polling endpoint trap
If the synchronous response does not directly contain a usable route, extract the task ID.

Do NOT poll:
- `/api/celery/task/{task_id}`

That returned HTTP 404 on the MIT deployment.

Use:
- `GET /api/celery/task/get?task_id=<task_id>`

This endpoint is documented in `openapi.json` and is the correct polling route for the current deployment.

### 5. Preserve current output contract exactly — and order steps forward
Each solved record in `cache/routes.jsonl` should still look like the local format:
```json
{
  "smiles": "target_smiles",
  "dock_score": -8.1,
  "solved": true,
  "steps": [
    {"rxn_smiles": "A.B>>C"},
    {"rxn_smiles": "C.D>>TARGET"}
  ],
  "n_steps": 2
}
```

Important: ASKCOS pathway extraction can yield reaction steps in a non-forward order. Before writing `routes.jsonl`:
- reorder steps so the last reaction product equals the target `smiles`
- renumber `step_index` after reordering
- drop candidate routes that cannot be rearranged into a valid forward chain

Why this matters:
- `/home/qiao/qiao_design/skill_drug/scripts/validate_result.py` requires the last product to equal `mol_smiles`
- unordered ASKCOS steps can make a chemically reasonable route fail downstream validation even when the API call succeeded

This usually avoids changes to:
- `/home/qiao/qiao_design/skill_drug/api/main.py`

But in this project, live ASKCOS routes exposed two downstream needs:
- add small guards in `pipeline.py` when `routes.jsonl` is missing or empty
- add emit-time route validation filtering in `pipeline.py` using `validate_result.py` logic, so positively scored but chemically invalid ASKCOS routes do not enter `result.csv`

Optional project-specific relaxation:
- if the user explicitly wants a softer route-economy threshold, `/home/qiao/qiao_design/skill_drug/scripts/route_economy.py` can stop treating `balance_score == 0` as a hard-zero and instead keep it as a weighted penalty only
- this helps retain more candidate routes for ranking, but it does NOT make invalid routes submission-safe; emit-time validation is still required

### 6. Lower route-economy thresholds carefully
If the user asks to "lower the threshold" or keep more retrosynthesis candidates alive:
- relax `route_economy.py` first, not `validate_result.py`
- a minimal change is to stop treating `balance_score == 0` as an automatic hard-zero and keep it as a weighted penalty in `route_score`

Important:
- this can raise route scores for ASKCOS outputs that are still chemically invalid under the submission contract
- therefore `pipeline.py` emit must filter candidate routes through `validate_result.validate(...)` before writing `result.csv`
- if every surviving route is invalid, emit may end up with a header-only CSV; that is safer than emitting invalid chemistry, but it means the real next optimization target is `retro.py` candidate quality / breadth, not further score-threshold lowering

```bash
ASKCOS_BASE_URL=https://askcos.mit.edu
ASKCOS_RETRO_PLANNER=mcts
ASKCOS_REQUEST_TIMEOUT=120
ASKCOS_ACCESS_TOKEN=<bearer token>
```

Recommended starting defaults from live testing on the MIT deployment:
- planner: `mcts`
- retro time: `20` seconds
- request timeout: `120` seconds

Reason:
- `mcts` at 20 s returned usable routes reliably in live tests
- `mcts` at 60 s repeatedly hit HTTP 504 on the MIT gateway
- longer search time was worse operationally than the shorter setting for this deployment
- in a later real job (`jobs/22ea8917`), `mcts` with `retro_time=120` produced 16 straight `http_504` abandons, zero `retro solved` events, and an empty `cache/routes.jsonl`; for this deployment, increasing `retro_time` can make operational reliability worse rather than better

Project-specific hardening that proved worth keeping:
- add a helper like `choose_safe_retro_time()` in `scripts/retro.py`
- cap oversized requested retro times down to an effective 20 s even if older jobs/UI/API still pass `120`
- log a `retro/config_override` event showing requested vs effective time limit
- keep project defaults aligned at `20` across upstream entry points:
  - `api/main.py`
  - `scripts/pipeline.py`
  - `scripts/agent_orchestrator.py`
  - `config/skill_config.yaml`
  - `webapp/index.html`

### 6. Add transient HTTP retry and planner fallback around ASKCOS calls
When patching `/home/qiao/qiao_design/skill_drug/scripts/retro.py`, do not abandon immediately on transient gateway / upstream errors.

Proven minimal fix:
- split the one-shot logic into `_solve_askcos_once(...)`
- wrap it with `solve_askcos(..., retries=2, retry_sleep=2.0, fallback_planners=["retro-star"])`
- retry only transient HTTP codes:
  - `502`
  - `503`
  - `504`
- use small backoff, e.g. 2 s then 4 s
- if the primary planner is `mcts` and repeated transient failures persist, retry with `retro-star` before final abandon

Why this matters:
- the old behavior treated every 504 as permanent failure and logged `retro abandon`
- some failures are deployment / gateway flakiness, not chemistry failure
- on this deployment, shorter search windows plus planner fallback were more reliable than simply increasing `retro_time`

Suggested pattern:
```python
DEFAULT_RETRY_HTTP_CODES = {502, 503, 504}
DEFAULT_FALLBACK_PLANNERS = ("retro-star",)

planners = [planner, *DEFAULT_FALLBACK_PLANNERS]
for planner_name in deduped(planners):
    for attempt in range(1, retries + 2):
        try:
            return _solve_askcos_once(..., planner=planner_name)
        except error.HTTPError as exc:
            if exc.code not in DEFAULT_RETRY_HTTP_CODES:
                raise
            if attempt < retries + 1:
                time.sleep(retry_sleep * attempt)
                continue
            break
```

### 7. Diagnose `abandon` correctly from job artifacts
When a user asks why a job is "stuck" in retro, inspect both:
- `jobs/<job_id>/result.log`
- `jobs/<job_id>/cache/routes.jsonl`
- optionally `jobs/<job_id>/meta.json`

Useful interpretation pattern:
- many `dock hit` events + many `retro abandon` events + empty `routes.jsonl` = retro backend failure, not upstream generation/docking failure
- repeated `reason="http_504"` = ASKCOS gateway / backend timeout under current planner/time budget
- `meta.json` may still say `status: running` and `stage_status.retro: running` even when no routes are being produced; do not trust job status alone without checking the actual outputs

Fast checks:
- count retro events by reason
- confirm whether `routes.jsonl` exists and has nonzero lines
- if `routes.jsonl` is empty and there are zero `retro solved` events, then there were no successful retrosynthesis results for that job

## Verification workflow

### 1. Check current OpenAPI schema
```bash
python - <<'PY'
import json, urllib.request
with urllib.request.urlopen('https://askcos.mit.edu/openapi.json', timeout=60) as r:
    data = json.load(r)
print(data['paths']['/api/tree-search/mcts/call-sync-without-token'])
print(data['paths']['/api/celery/task/get'])
PY
```

### 2. Syntax-check retro.py
```bash
python -m py_compile /home/qiao/qiao_design/skill_drug/scripts/retro.py
```

### 3. Source env and test a small run
```bash
cd /home/qiao/qiao_design/skill_drug
set -a && source .env && set +a
python scripts/retro.py --out jobs/<job_id> --max 3 --time 20
```

### 4. Inspect outputs
- `jobs/<job_id>/result.log`
- `jobs/<job_id>/cache/routes.jsonl`

### 5. Verify downstream artifacts, not just API success
```bash
python scripts/route_economy.py --out jobs/<job_id>
python scripts/pipeline.py --pdb references/7XWO_prepared_nk2r_B.pdb --out jobs/<job_id> --stage emit
```

If emit fails, inspect whether the problem is:
- `routes.jsonl` missing / empty
- ASKCOS step order wrong
- ASKCOS route chemically invalid under `validate_result.py`
- all surviving routes filtered out as invalid, leaving no data rows

### 6. Add a focused regression test when changing emit behavior
For this repo, a useful test pattern is:
- create a temporary `cache/routes.jsonl` with one valid route and one invalid route
- create matching `route_scores.csv` and `docking_scores.csv`
- call `pipeline.emit(...)`
- assert the invalid route is filtered out of `result.csv`
- add a second case where only invalid routes survive and assert emit writes only the CSV header

This catches the exact failure mode where route-economy relaxation causes invalid ASKCOS routes to leak into final output.

Interpretation:
- `missing_askcos_token` → `.env` not loaded or token absent
- `http_422` → payload schema wrong, usually flat fields instead of nested options
- `http_404` after polling → wrong celery result endpoint or wrong planner slug
- `http_504` on long search windows → reduce `--time` / request timeout rather than increasing them
- `not_solved` → integration is working, but ASKCOS found no route for that molecule under current search budget
- `validate_result.py` failure after emit → route extraction/order is wrong or the returned route itself is chemically invalid for this pipeline

## Important lessons learned
- `call-sync-without-token` still has a strict request schema; read `openapi.json` before guessing fields.
- The planner slug is `retro-star`, not `retro_star`.
- A 200 response does not guarantee a directly serializable route list.
- `uds.pathways + uuid2smiles` is the robust fallback for reconstructing routes.
- Do not stop at reconstructing the first normalized pathway. Iterate the candidate UDS pathways, normalize/reorder each route, and prefer the first route that already passes `validate_result.py` semantics. This was the key improvement that turned a real job from `no valid rows` into a successful emit.
- On the MIT deployment, `mcts` with a 20 s search window was more reliable than 60 s; the longer run repeatedly hit HTTP 504.
- In a real rerun on `jobs/d968ae2f`, re-running `retro.py --max 5 --time 20` after adding submission-valid route selection produced 4 valid final rows and `pipeline.py --stage emit` returned `OK`.
- A header-only `result.csv` is safer than emitting invalid chemistry, but note that this repo's `validate_result.py` rejects `no data rows`. So an empty emit is only a temporary safety behavior; the real fix is better retrosynthesis candidate quality/breadth.
- Distinguish integration failure from route-quality failure:
  - 422 / 404 / missing token / 504 = integration or deployment behavior
  - `not_solved` = no route found for the molecule/search budget
  - `validate_result.py` failure = extracted route order/content is incompatible with the downstream submission contract
- For this project, preserving `routes.jsonl` shape is not enough; you must verify `route_economy.py` and `pipeline.py --stage emit` after any retro integration change.

## Files typically involved
- `/home/qiao/qiao_design/skill_drug/scripts/retro.py`
- `/home/qiao/qiao_design/skill_drug/.env`
- `/home/qiao/qiao_design/skill_drug/jobs/<job_id>/result.log`
- `/home/qiao/qiao_design/skill_drug/jobs/<job_id>/cache/routes.jsonl`
- `/home/qiao/qiao_design/skill_drug/jobs/<job_id>/meta.json`
- `/home/qiao/qiao_design/skill_drug/jobs/<job_id>/result.csv`
- `/home/qiao/qiao_design/skill_drug/jobs/<job_id>/result.zip`

## UI status reconciliation / stale meta repair
Sometimes the job UI can still show `运行` even when final artifacts already exist and validate. Before rerunning expensive stages, check:
```bash
cd /home/qiao/qiao_design/skill_drug
wc -l jobs/<job_id>/result.csv jobs/<job_id>/cache/routes.jsonl jobs/<job_id>/cache/route_scores.csv jobs/<job_id>/cache/docking_scores.csv
unzip -l jobs/<job_id>/result.zip
python scripts/validate_result.py jobs/<job_id>/result.csv
ps -eo pid,etime,cmd | grep -F '<job_id>' | grep -v grep || true
```
If `result.csv` validates, `result.zip` exists, and no live process owns the job, repair `meta.json` instead of rerunning:
- set `status: "done"`
- set `current_stage: null`, `waiting_for: null`
- set all stage statuses through `emit` to `done`
- set `routes_solved` from nonempty lines in `cache/routes.jsonl`
- set `result_rows` from data rows in `result.csv`
- recompute docking stats from `cache/docking_scores.csv`; current header may be `score_kcal_per_mol`, not `score`

This exact issue occurred on `jobs/22ea8917`: artifacts were valid (`validate_result.py` OK, 8 result rows, 37 routes) while `meta.json` still said `status=running`, `current_stage=retro`.

## Minimal-change philosophy
- Start with `retro.py` and `.env`, and preserve `routes.jsonl` shape.
- But do not assume downstream compatibility just because the file schema matches. In this repo, live ASKCOS routes exposed two necessary follow-up changes:
  - `pipeline.py` needed emit-time validation filtering and empty/filtered-route guards
  - `route_economy.py` sometimes needed softer score-zeroing when the user explicitly wanted more candidates kept alive
- So the practical minimal-change rule is: change the fewest files that restore end-to-end validity, then verify with `route_economy.py` + `pipeline.py --stage emit`, not just `retro.py` output.
