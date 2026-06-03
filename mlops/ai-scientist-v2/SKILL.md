---
name: ai-scientist-v2
description: "Class-level operating guide for AI-Scientist-v2 — the autonomous research pipeline from Sakana AI. Covers project structure, OpenAI/OpenAI-compatible model wiring, Semantic Scholar integration, .env management, bfts_config.yaml tuning, launch parameters, and the Streamlit AI Scientist Cloud console (including access-key registration). Use for any task involving AI-Scientist-v2 setup, configuration, provider integration, experiment execution, or UI building."
tags: [ai-scientist, autonomous-research, llm-integration, streamlit, sakana]
version: 1
---

# AI-Scientist-v2 — Operating Guide

## Project Overview

AI-Scientist-v2 is Sakana AI's autonomous research pipeline. It generates research ideas, runs experiments (with code generation + debugging), writes papers, and performs AI-powered peer review — all without human intervention.

**Repo path:** `/home/qiao/dockerai/AI-Scientist-v2`

## Project Structure

```
AI-Scientist-v2/
├── launch_scientist_bfts.py   # Main entry point
├── bfts_config.yaml           # Runtime config (models, agents, timeouts)
├── .env                       # API keys (S2_API_KEY, MIMO_API_KEY, etc.)
├── web_app.py                 # Streamlit no-code frontend
├── run_web.sh                 # One-click launcher for web UI
├── requirements.txt           # Python dependencies
├── ai_scientist/
│   ├── llm.py                 # Core LLM abstraction (create_client, get_response_from_llm)
│   ├── vlm.py                 # Vision-language model abstraction
│   ├── perform_writeup.py     # Paper writing
│   ├── perform_ideation_temp_free.py  # Idea generation (uses Semantic Scholar)
│   ├── perform_llm_review.py  # AI peer review
│   ├── perform_vlm_review.py  # Visual review
│   ├── perform_plotting.py    # Plot aggregation
│   ├── ideas/                 # Pre-generated ideas (JSON + .py)
│   ├── fewshot_examples/      # Few-shot examples for prompts
│   ├── tools/
│   │   ├── base_tool.py       # Tool base class
│   │   └── semantic_scholar.py # S2 API wrapper with rate limiting
│   ├── treesearch/
│   │   ├── backend/
│   │   │   ├── backend_openai.py     # OpenAI-compatible backend
│   │   │   ├── backend_anthropic.py  # Anthropic backend (Bedrock)
│   │   │   └── utils.py             # FunctionSpec, backoff_create
│   │   ├── parallel_agent.py  # Multi-worker agent manager
│   │   ├── agent_manager.py   # Agent orchestration
│   │   └── ...
│   └── utils/
│       └── token_tracker.py   # Token usage tracking
├── data/                      # Datasets (symlinked or copied to workspaces)
└── experiments/               # Output directory for runs
```

## Adding a New OpenAI-Compatible LLM Provider

This is a 4-file pattern. Every new OpenAI-compatible provider (Xiaomi Mimo, DeepSeek, custom, etc.) touches the same files:

### Step 0: Audit ALL dispatch points BEFORE editing

**This is the #1 failure mode** — missing a dispatch point causes runtime crash.

```bash
grep -rn '"gpt"\|"claude"\|startswith("ollama\|in model\|not supported' --include='*.py' ai_scientist/
```

There are **9 dispatch functions across 3 files** (see `integrate-openai-compatible-provider` skill for the full map). The hardest to spot is `make_llm_call()` in llm.py — it's called by writeup/review code, not the main experiment loop.

### Step 1: `ai_scientist/llm.py` (4 dispatch points)
1. Add model name to `AVAILABLE_LLMS` list
2. Add branch in `get_batch_responses_from_llm()` — ensemble/batch calls
3. Add branch in `make_llm_call()` — **CRITICAL: often missed!** Used by writeup, review, plotting
4. Add branch in `get_response_from_llm()` — main single-response call
5. Add branch in `create_client()` — client factory with custom base_url

### Step 2: `ai_scientist/vlm.py` (4 dispatch points)
1. Add model name to `AVAILABLE_VLMS` list
2. Add branch in `make_llm_call()` — VLM text-only calls
3. Add branch in `make_vlm_call()` — VLM vision+text calls
4. Add branch in `get_batch_responses_from_vlm()` — **must NOT include `seed=0`** (see pitfalls)
5. Add branch in `create_client()` — VLM client factory

### Step 3: `ai_scientist/treesearch/backend/backend_openai.py` (1 dispatch point)
- Add `import os` if missing
- Add branch in `get_ai_client()` — same OpenAI pattern with custom base_url

### Step 4: `ai_scientist/utils/token_tracker.py`
- Add model pricing to `MODEL_PRICES` dict (otherwise cost tracking shows $0.00)

### Step 5: `bfts_config.yaml`
- Update ALL model fields: `agent.code.model`, `agent.feedback.model`, `agent.vlm_feedback.model`, `report.model`

### Step 6: `ai_scientist/openai_models.py`
- Update `DEFAULT_OPENAI_MODEL` if you want the launcher/UI/ideation default to change globally
- Add the new model to `OPENAI_MODEL_CATALOG` if the Streamlit console should offer it in dropdowns
- Keep `is_openai_experiment_model()` / `is_openai_vision_model()` in sync when adding new model families or non-text SKUs

### Step 7: `launch_scientist_bfts.py`
- Update all `--model_*` argument defaults (5 args) if you are hard-pinning a new default; otherwise they inherit `DEFAULT_OPENAI_MODEL`

### Pitfalls
- **Missing `import os`** in backend_openai.py — Pyright flags `os.environ` as undefined.
- **`make_llm_call()` in llm.py is the #1 missed dispatch point** — called by writeup/review/plotting, not the main experiment loop. If missing, experiments run fine but paper writing crashes.
- **`seed=0` in vlm.py `get_batch_responses_from_vlm()`** — the else branch sends `seed=0` for all non-ollama models. Most proxy APIs (Mimo, Deepseek, vLLM) reject this. Always add a separate provider branch WITHOUT seed.
- **`vlm_feedback.model`** — this DOES work with OpenAI-compatible providers (Mimo etc.). The previous note "VLM models cannot be Mimo" was wrong. Any OpenAI-compatible chat/completions endpoint works.
- **`token_tracker.py` MODEL_PRICES** — if the new model isn't listed, cost tracking silently returns $0.00. Not a crash, but misleading.
- **backend_anthropic.py is Bedrock-only** — uses `anthropic.AnthropicBedrock()`. Don't put OpenAI-compatible providers there.

## .env Loading Pattern

python-dotenv is in requirements.txt (installed as a dependency). Each file that needs env vars should add at the top:

```python
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass
```

The `try/except` keeps the code resilient if someone runs without installing deps.
Place it at the top of:
- `launch_scientist_bfts.py`
- `ai_scientist/llm.py`
- `ai_scientist/tools/semantic_scholar.py`

## Semantic Scholar Integration

### API Usage from Scripts

The S2 wrapper is at `ai_scientist/tools/semantic_scholar.py`. The main function:

```python
from ai_scientist.tools.semantic_scholar import search_for_papers

# Signature: search_for_papers(query, result_limit=10) -> Optional[List[Dict]]
# Returns a LIST of paper dicts (NOT a dict with 'data' key)
results = search_for_papers("RFdiffusion protein design", result_limit=15)

for paper in results:
    print(paper['title'], paper['year'], paper['citationCount'])
```

**Important**: `result_limit` (not `limit`), and returns `List[Dict]` directly. Each dict has: `paperId`, `title`, `year`, `venue`, `citationCount`, `openAccessPdf`, `url`.

For paper abstracts, use the S2 REST API directly (the wrapper doesn't expose `get_paper_details`):

```python
import requests, os

def get_paper_abstract(paper_id):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    params = {'fields': 'title,abstract,year,venue,citationCount,authors'}
    headers = {'X-API-KEY': os.environ.get('S2_API_KEY', '')}
    resp = requests.get(url, params=params, headers=headers)
    return resp.json() if resp.status_code == 200 else None
```

### Multi-Query Literature Search Pattern

For comprehensive literature reviews, search with multiple keyword angles and deduplicate by `paperId`:

```python
queries = [
    ("hallucination protein design", "核心: hallucination方法"),
    ("RFdiffusion protein backbone diffusion", "核心: RFdiffusion"),
    ("SE(3) equivariant diffusion protein", "核心: SE(3)扩散"),
    ("enzyme design generative model", "应用: 酶设计"),
]
all_papers = {}
for query, category in queries:
    results = search_for_papers(query, result_limit=15)
    for p in results:
        pid = p['paperId']
        if pid not in all_papers:
            all_papers[pid] = {**p, 'category': category}
    time.sleep(1.1)  # Respect 1 req/s rate limit
```

### Rate Limiting

**API key rate limit: 1 request/second** (cumulative across all endpoints).

The pattern uses a module-level rate limiter:

```python
_s2_last_request_time = 0.0

def _s2_rate_limit():
    global _s2_last_request_time
    now = time.monotonic()
    elapsed = now - _s2_last_request_time
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)
    _s2_last_request_time = time.monotonic()
```

Call `_s2_rate_limit()` before every `requests.get()` to S2 API. The header is `X-API-KEY` (not `Authorization`).

## Launch Parameters

`launch_scientist_bfts.py` key flags:

| Flag | Default | Purpose |
|------|---------|---------|
| `--load_ideas` | `ideas/...json` | Path to ideas JSON |
| `--idea_idx` | 0 | Index if JSON is array |
| `--writeup-type` | `icbinb` | `normal` (8p) or `icbinb` (4p) |
| `--model_writeup` | `mimo-v2.5-pro` | Paper writing model |
| `--model_review` | `mimo-v2.5-pro` | Review model |
| `--model_agg_plots` | `mimo-v2.5-pro` | Plot aggregation model |
| `--skip_writeup` | False | Skip paper generation |
| `--skip_review` | False | Skip AI review |
| `--writeup-retries` | 3 | Max writeup attempts |
| `--num_cite_rounds` | 20 | Citation search rounds |

## Streamlit AI Scientist Cloud Console

The local product surface is `web_app.py`, launched by `bash run_web.sh`. It is no longer just a thin no-code frontend: it includes idea management, experiment job orchestration, settings/key testing, and an API access registration + verification-key distribution workflow.

Key implementation facts:
- `run_web.sh` binds `127.0.0.1:8501` by default and warns to use `0.0.0.0` only behind HTTPS/auth.
- The launcher auto-installs Streamlit/runtime packages if missing.
- `web_app.py` persists job metadata under `experiments/_web_jobs/`.
- API-access state lives under `experiments/_api_access/`, especially `registrations.json`, `verification_keys.json`, and `exports/`.
- Verification keys are encrypted-at-rest with Fernet in the JSON pool, while CSV/TXT exports are the distribution artifacts.
- The UI uses `ai_scientist/openai_models.py` as the source of truth for selectable OpenAI-family models.

Operational implications:
- If you add/change default models, check both `bfts_config.yaml` and `ai_scientist/openai_models.py`.
- If you document user access or internal testing, mention the verification-key workflow, not just API keys.
- If exposing the app publicly, set `AI_SCIENTIST_APP_PASSWORD` and put it behind HTTPS/reverse proxy.

See `references/streamlit-frontend-pattern.md` for the broader frontend pattern.


## Bulk Model Migration (e.g. mimo-v2-pro → mimo-v2.5-pro)

When the provider renames or upgrades a model, do a project-wide find-replace:

```bash
cd /home/qiao/dockerai/AI-Scientist-v2

# 1. Bulk replace in all relevant files
sed -i 's/mimo-v2-pro/mimo-v2.5-pro/g' \
  ai_scientist/llm.py \
  launch_scientist_bfts.py \
  bfts_config.yaml \
  web_app.py

# 2. Verify zero stale references remain
grep -rn 'mimo-v2-pro' --include='*.py' --include='*.yaml' . \
  | grep -v 'mimo-v2.5-pro' || echo "(all clean)"

# 3. Syntax check all modified files
python -c "
import ast
for f in ['ai_scientist/llm.py','launch_scientist_bfts.py','web_app.py']:
    with open(f) as fh: ast.parse(fh.read())
    print(f'OK {f}')
"
```

Files that contain explicit model name strings (not just `"mimo" in model` guards):
- `ai_scientist/llm.py` — `AVAILABLE_LLMS` list
- `launch_scientist_bfts.py` — 5x `default="mimo-..."` argparse args
- `bfts_config.yaml` — 3x `model: mimo-...` lines
- `web_app.py` — MODELS list + default fallbacks in selectbox widgets

The generic `elif "mimo" in model:` branches do NOT need updating — they catch any mimo-* model.

## bfts_config.yaml Key Settings

```yaml
agent:
  type: parallel
  num_workers: 4          # Parallel experiment workers
  steps: 5                # Improvement iterations
  code.model: mimo-v2.5-pro   # Code generation model
  feedback.model: mimo-v2.5-pro  # Error evaluation model
  vlm_feedback.model: mimo-v2.5-pro  # Visual feedback (works via OpenAI-compatible API)
  exec.timeout: 3600      # Code execution timeout (seconds)
report:
  model: mimo-v2.5-pro    # Final report generation
```

## Creating Domain-Specific Review Templates

`perform_review()` in `ai_scientist/perform_llm_review.py` accepts a `review_instruction_form` parameter — pass a custom string to override the default NeurIPS form. This lets you write specialized review prompts for specific domains (protein design, drug discovery, materials science, etc.).

### Pattern

1. Create a module under `ai_scientist/review_templates/`
2. Export a `*_review_form` string following the NeurIPS form structure (Summary → Strengths/Weaknesses → Questions → Limitations → Ethical Concerns → Ratings → Overall → Confidence → Decision)
3. Add domain-specific sections (e.g., computational benchmarks, wet-lab validation criteria, method classification)
4. Optionally add a scoring rubric and thought-prompt companion strings

### Template Structure

```python
# 3 exported strings:
protein_hallucination_review_form      # Main form (pass to review_instruction_form)
protein_hallucination_scoring_rubric   # Weighted scoring rubric (append to form if needed)
protein_hallucination_thought_prompt   # Structured thinking framework
```

### Integration

```python
from ai_scientist.review_templates import protein_hallucination_review_form
from ai_scientist.perform_llm_review import perform_review

review = perform_review(
    text=paper_text,
    model="mimo-v2.5-pro",
    client=client,
    num_reflections=2,
    num_reviews_ensemble=3,
    review_instruction_form=protein_hallucination_review_form,
)
```

### Usage File Pitfall

**Do NOT import `perform_review` or `load_paper` at module level in usage/example files.** These pull in `pymupdf` (via `perform_llm_review.py`), which fails if not installed. Use deferred imports inside functions, or keep usage files as plain data (example JSON outputs) without importing the review machinery.

See `references/domain-review-templates.md` for the full protein hallucination template as a reference implementation.

## `create_client()` Return Type

**`create_client()` returns a tuple `(client, model_name)`, NOT a bare client object.** Always unpack:
```python
client, model_name = create_client('gpt-5-mini')  # correct
client = create_client('gpt-5-mini')               # WRONG — tuple, not OpenAI client
```
Passing the raw tuple to `get_response_from_llm()` causes `'tuple' object has no attribute 'chat'`. Every caller in the codebase should unpack.

Repo-specific pitfall discovered during inspection:
- `ai_scientist/review_templates/protein_hallucination_usage.py` still shows `client = create_client(model)` in its helper example. Treat that example as stale unless patched in the repo; the runtime contract remains tuple-unpack.

## Ideation Script (`perform_ideation_temp_free.py`) with OpenAI-family Defaults

The ideation script now defaults to `AI_SCIENTIST_MODEL` from `.env`, falling back to `gpt-5-mini` when unset:

```python
default_model = os.getenv("AI_SCIENTIST_MODEL", "gpt-5-mini")
```

It validates that choice against `AVAILABLE_LLMS` before parsing args, and still requires unpacking:

```python
client, client_model = create_client(args.model)
```

The script uses an ACTION/ARGUMENTS protocol plus `json.loads()` for tool invocations and `FinalizeIdea`, so malformed JSON remains a common failure mode for weaker proxy providers.

**Symptoms**: `JSONDecodeError: Expecting value: line X column Y` during `FinalizeIdea` action, even though the LLM content looks correct in the output. The LLM often writes the full idea as detailed prose in its `THOUGHT` section, then fails on the JSON action format.

**Workaround options**:
1. Increase `--num-reflections` to give the LLM more chances to self-correct
2. **Manual extraction (most reliable)**: The LLM's verbose output usually contains the complete idea as prose. Extract it manually and create the JSON file yourself. The JSON schema is simple (see below).
3. Use a stronger JSON-following model for ideation and another model downstream
4. Run ideation with `--max-num-generations` set high (e.g. 10-20) — even if 50%+ fail to parse, you'll get enough valid ideas

**Ideas JSON schema** — each entry is a JSON object with these fields:

```json
{
  "Name": "snake_case_id",
  "Title": "Full paper title",
  "Short Hypothesis": "1-2 sentence hypothesis",
  "Related Work": "Citations and differentiation paragraph",
  "Abstract": "Full abstract paragraph",
  "Experiments": "Numbered experiment plan as a single string",
  "Risk Factors and Limitations": "Numbered risks as a single string"
}
```

**Critical**: `Experiments` and `Risk Factors and Limitations` are **strings** (not arrays). The pipeline parses them as text blocks. Write them as numbered prose (e.g., "1. First experiment...\n2. Second experiment...").

The file is a JSON array: `[ {...}, {...}, {...} ]`. Place it in `ai_scientist/ideas/` with the same base name as your topic markdown file.

## Current Repo Defaults Observed

As inspected in this checkout:
- `bfts_config.yaml` currently defaults `report.model`, `agent.code.model`, `agent.feedback.model`, and `agent.vlm_feedback.model` to `gpt-5-mini`.
- `ai_scientist/openai_models.py` sets `DEFAULT_OPENAI_MODEL = "gpt-5-mini"` and includes `gpt-5.4-*` models in the catalog.
- `launch_scientist_bfts.py` imports `DEFAULT_OPENAI_MODEL`, so launcher defaults follow that central constant.
- `perform_ideation_temp_free.py` also falls back to `gpt-5-mini` if `AI_SCIENTIST_MODEL` is not set.

If the user switches providers or wants `gpt-5.4`/other models as the default, update all four layers deliberately: `.env` (optional runtime override), `bfts_config.yaml`, `openai_models.py`, and any documentation/UI copy that names the default model.

2. **`seed=0` API rejection** — OpenAI supports `seed=0` for reproducibility. Most proxy APIs reject it. The `else` fallback branch in `vlm.py` `get_batch_responses_from_vlm()` sends `seed=0` — if your provider doesn't support it, add a separate branch without seed.
3. **Ideas JSON format** — must include `Name`, `Title`, `Short Hypothesis`, `Related Work`, `Abstract`, `Experiments` (string), `Risk Factors and Limitations` (string). See "Ideation Script" section above for full schema and Mimo JSON parsing pitfalls.
4. **Experiments directory** — auto-created with timestamp prefix: `experiments/YYYY-MM-DD_HH-MM-SS_<name>_attempt_<id>/`
5. **process cleanup** — launch script kills all child processes on exit (psutil + signal). If running manually, watch for orphaned processes.
6. **Token tracker** — `token_tracker.json` and `token_tracker_interactions.json` saved in idea_dir after experiments and writeup.
7. **Bulk model migration** — when upgrading model name (e.g. mimo-v2-pro → mimo-v2.5-pro), `sed -i` across llm.py, vlm.py, launch_scientist_bfts.py, bfts_config.yaml, web_app.py. The generic `elif "mimo" in model:` branches don't need updating.
