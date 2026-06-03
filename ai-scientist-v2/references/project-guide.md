# AI-Scientist-v2 project guide

## File map

- `README.md`: upstream usage plus local AI Scientist Cloud authorization notes.
- `requirements.txt`: Python dependencies; notable runtime packages include `openai`, `anthropic`, `python-dotenv`, `streamlit`, `PyYAML`, `psutil`, `funcy`, `coolname`, `omegaconf`, `jsonschema`, `genson`, `shutup`, `humanize`, `dataclasses-json`, `python-igraph`, `PyMuPDF`, `pymupdf4llm`.
- `.env`: local secrets/config; do not display values.
- `bfts_config.yaml`: BFTS/tree-search runtime config.
- `launch_scientist_bfts.py`: main CLI pipeline for experiments, plotting, writeup, citations, and review.
- `web_app.py`: Streamlit AI Scientist Cloud console and background-job runner.
- `run_web.sh`: Streamlit launcher.
- `ideas/`: local idea JSON files used by launcher.
- `ai_scientist/ideas/`: example topic Markdown, generated ideas, and domain writing/review material.
- `experiments/`: generated runs, `_web_jobs` background job status/logs, `_api_access` registration/key pool.
- `ai_scientist/tools/semantic_scholar.py`: S2 paper search helper using `S2_API_KEY` and 1 req/sec rate limiter. For ad hoc paper queries, prefer the separate `s2-api` skill/script, which loads `S2_API_KEY` from `/home/qiao/dockerai/AI-Scientist-v2/.env` without printing it.
- `ai_scientist/openai_models.py`: product UI model catalog; default is `gpt-5-mini`.

## Environment

Minimum common variables:

```bash
export OPENAI_API_KEY="..."
export S2_API_KEY="..."                  # optional but recommended for Semantic Scholar throughput
export AI_SCIENTIST_MODEL="gpt-5-mini"   # ideation default if --model is omitted
export OPENAI_BASE_URL="..."             # optional OpenAI-compatible gateway
```

Claude via AWS Bedrock is supported by installing `anthropic[bedrock]` and setting `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION_NAME`.

The Streamlit console can also use:

```bash
export AI_SCIENTIST_APP_PASSWORD="..."
export AI_SCIENTIST_REQUIRE_ACCESS_KEY=true
export API_ACCESS_GROUP_LINK="https://..."
export API_SERVICE_CONTACT_NAME="..."
export API_SERVICE_CONTACT_EMAIL="..."
```

Never reveal `.env` contents. When editing `.env`, preserve `0600`-style private permissions if possible.

## Installation / readiness

From project root:

```bash
conda create -n ai_scientist python=3.11
conda activate ai_scientist
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
conda install anaconda::poppler
conda install conda-forge::chktex
pip install -r requirements.txt
```

For the web app only, `run_web.sh` auto-installs its minimal launcher dependencies.

Before launching a job, check:

- `OPENAI_API_KEY` is configured.
- `S2_API_KEY` is configured if ideation/citation novelty search matters.
- GPU/CUDA availability if experiments need it.
- `bfts_config.yaml` values are reasonable for cost/runtime.
- Idea JSON has the fields expected by `normalize_idea_for_bfts` (at minimum a name/title/hypothesis/experiment-like content).

## Ideation

Input: Markdown topic description. Example source: `ai_scientist/ideas/i_cant_believe_its_not_better.md`.

Command:

```bash
python ai_scientist/perform_ideation_temp_free.py \
  --workshop-file "ai_scientist/ideas/my_research_topic.md" \
  --model gpt-5-mini \
  --max-num-generations 20 \
  --num-reflections 5
```

If `AI_SCIENTIST_MODEL` is set, `--model` may be omitted. Output is the same stem as the input Markdown, e.g. `ai_scientist/ideas/my_research_topic.json`.

The script asks the LLM to use actions:

- `SearchSemanticScholar` with `{"query": "..."}`
- `FinalizeIdea` with `{"idea": {...}}`

The generated idea should include `Name`, `Title`, `Short Hypothesis`, `Related Work`, `Abstract`, `Experiments`, and `Risk Factors and Limitations`.

## BFTS experiment pipeline

Main launcher:

```bash
python launch_scientist_bfts.py \
  --load_ideas "ideas/my_research_topic.json" \
  --idea_idx 0 \
  --model gpt-5-mini \
  --writeup-retries 3 \
  --num_cite_rounds 12
```

Useful flags:

- `--model <model>`: applies one model across BFTS, plot aggregation, citation, writeup, and review.
- `--model_writeup`, `--model_citation`, `--model_review`, `--model_agg_plots`, `--model_writeup_small`: override specific stages.
- `--writeup-type normal|icbinb`: default `icbinb` (4 pages); `normal` uses 8 pages.
- `--skip_writeup`: skip citations/writeup; useful for debugging BFTS only.
- `--skip_review`: skip auto-review.
- `--load_code`: load same-stem `.py` next to the idea JSON.
- `--add_dataset_ref`: prepend `hf_dataset_reference.py` if present.
- `--attempt_id`: distinguish parallel attempts.

Output behavior:

1. Creates `experiments/<timestamp>_<idea Name>_attempt_<attempt_id>/`.
2. Writes `idea.md` and `idea.json`.
3. Copies edited BFTS config into run directory.
4. Runs `perform_experiments_bfts`.
5. Copies `logs/0-run/experiment_results` to run root, aggregates plots, saves token trackers.
6. If writeup enabled, gathers citations and generates PDF/LaTeX.
7. If review enabled and a PDF exists, writes `review_text.txt` and `review_img_cap_ref.json`.
8. Terminates only child processes spawned by the run.

## BFTS config knobs

Effective fields in `bfts_config.yaml`:

```yaml
agent:
  num_workers: 4
  steps: 5
  stages:
    stage1_max_iters: 20
    stage2_max_iters: 12
    stage3_max_iters: 12
    stage4_max_iters: 18
  multi_seed_eval:
    num_seeds: 3
  code:
    model: gpt-5-mini
    temp: 1.0
    max_tokens: 12000
  feedback:
    model: gpt-5-mini
    temp: 0.5
    max_tokens: 8192
  vlm_feedback:
    model: gpt-5-mini
    temp: 0.5
  search:
    max_debug_depth: 3
    debug_prob: 0.5
    num_drafts: 3
report:
  model: gpt-5-mini
  temp: 1.0
exec:
  timeout: 3600
```

Operational heuristics:

- `num_workers` controls parallel exploration paths and cost/concurrency.
- `steps` is fallback total exploration depth when stage-specific values are absent.
- `num_seeds` should usually match `num_workers` if workers < 3; otherwise use 3.
- `max_debug_depth` and `debug_prob` trade off recovery vs time/cost.
- `num_drafts` controls independent root nodes in Stage 1.

## Streamlit AI Scientist Cloud

Launch:

```bash
bash run_web.sh --port 8501 --host 127.0.0.1
```

Open `http://localhost:8501`.

`run_web.sh` defaults to localhost and warns that `0.0.0.0` should only be used behind HTTPS/auth.

Console sections:

- `总览`: readiness and operations queue.
- `想法库`: create/import/browse canonical idea JSON.
- `运行中心`: launch background experiments, edit effective BFTS params, view job status/log tails, rerun failed/lost jobs.
- `论文与审稿`: browse PDFs, reviews, token records, generated files.
- `API 注册与权限`: registration, group verification, permission tiers, verification-key assignment/revocation.
- `安全与设置`: API keys/base URL/model connection testing and service settings.

Background job files:

- Status JSON: `experiments/_web_jobs/<job_id>.json`
- Log: `experiments/_web_jobs/<job_id>.log`

For failures, inspect status JSON fields (`status`, `return_code`, `command`, `last_line`, `heartbeat_at`) and the log tail.

## Verification keys / API access

The console stores verification access under `experiments/_api_access/`:

- `verification_keys.json`: encrypted internal pool; do not distribute.
- `exports/verification_keys_<batch_id>.csv`: audit/distribution sheet with `key_id` and `verification_key`.
- `exports/verification_keys_<batch_id>.txt`: plaintext-only keys, one per line; safest to distribute when authorized.

Distribute only the plaintext `ASIC-TST-...` key, not `key_id`, `token_digest`, `encrypted_token`, the JSON pool, `API_ACCESS_KEY_FERNET`, or OpenAI keys.

## S2 paper queries

For user-facing paper queries/citation lookups, invoke the `s2-api` skill first. It uses `/root/.claude/skills/s2-api/scripts/s2_search.py` and loads `S2_API_KEY` from `/home/qiao/dockerai/AI-Scientist-v2/.env` without revealing the key.

Example:

```bash
python /root/.claude/skills/s2-api/scripts/s2_search.py search "agentic tree search automated scientific discovery" --limit 10
```

Only fall back to other paper-search skills after reporting why S2 was unavailable or insufficient.

## Troubleshooting

### Missing dependencies

The web app checks launcher runtime dependencies and may suggest:

```bash
pip install funcy coolname omegaconf jsonschema genson shutup humanize dataclasses-json python-igraph PyMuPDF pymupdf4llm
```

For full experiments, prefer `pip install -r requirements.txt` in the intended environment.

### Semantic Scholar

Errors originate in `ai_scientist/tools/semantic_scholar.py`:

- 401: bad/expired `S2_API_KEY`.
- 429: rate limit; slow down or use a valid key.
- TLS/network/timeout: check CA certificates, VPN/proxy, DNS, outbound access.

The helper rate-limits to roughly one request per second. It searches `https://api.semanticscholar.org/graph/v1/paper/search` and requests fields including title, authors, venue, year, abstract, and citation count.

### API model connection

The web app validates OpenAI-compatible text/reasoning models using a tiny chat completion. Non-experiment model prefixes (`gpt-image-`, `text-embedding-`, `tts-`, `whisper-`) are rejected for BFTS text experiments.

### CUDA OOM

Lower the workload/model size, reduce `agent.num_workers`, reduce stage max iterations, or adjust the idea prompt to prefer smaller models/experiments.

### Missing PDF/review

Check whether `--skip_writeup` or `--skip_review` was used, whether writeup succeeded after retries, and whether a PDF exists in the run directory. The launcher chooses final/highest reflection PDF for review when available.

### Lost web job

A job is marked `lost` when status says running but `child_pid` is no longer alive. Inspect `_web_jobs/<job_id>.log` and rerun only if the saved command is still appropriate.
