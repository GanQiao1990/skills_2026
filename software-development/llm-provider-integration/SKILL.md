---
name: llm-provider-integration
description: >
  Add a new LLM provider/model to an existing multi-file Python codebase that
  dispatches on model names via if/elif chains. Covers systematic audit,
  complete patching, and verification. Use when the user wants to integrate
  a new API provider (e.g. Xiaomi Mimo, DeepSeek, a new OpenAI-compatible
  endpoint) into a project that already supports multiple LLM backends.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  tags: [llm, integration, provider, dispatch, multi-model, openai-compatible]
---

# LLM Provider Integration

Use this skill when adding a new LLM provider to a Python project that already
supports multiple model backends via scattered if/elif dispatch chains.

## When to use

- User says "add model X" or "use provider Y" for an existing LLM-powered project
- Project has multiple files with model-name dispatch logic (if "gpt" in model, elif "claude", etc.)
- Provider is OpenAI-API-compatible (most common case) or Anthropic-API-compatible
- User provides API key, base URL, and model name

## Core problem

In multi-backend LLM projects, model dispatch logic is typically duplicated across:
1. `create_client()` — factory that returns the API client
2. `get_response_from_llm()` — single-response function
3. `get_batch_responses_from_llm()` — multi-response / ensemble function
4. `make_llm_call()` — lower-level call wrapper
5. VLM equivalents (`make_vlm_call`, `get_response_from_vlm`, etc.)
6. Backend modules (e.g. `treesearch/backend/backend_openai.py`)
7. AVAILABLE_MODELS lists
8. Config files (YAML/TOML) with default model names
9. CLI argument defaults
10. Token/cost tracking dictionaries

**Missing any one of these causes runtime crashes** that are hard to debug
because the error only appears when that specific code path is hit.

## Systematic audit procedure

### Step 1: Find ALL dispatch points

```bash
# Find all files with model-name matching
grep -rn '"gpt"\|'claude'\|"ollama"\|"gemini"\|"o1"\|"o3"\|"deepseek' \
  --include='*.py' project_root/

# Find AVAILABLE_MODELS / AVAILABLE_VLMS lists
grep -rn 'AVAILABLE_\|MODELS\s*=' --include='*.py' project_root/
```

For EACH file found, check:
- Does it have an if/elif chain matching on model name substrings?
- Is there already a branch for the new provider?
- Would the new model name fall through to `else: raise ValueError`?

### Step 2: Check each function type

| Function type | What to add | Common pitfall |
|--------------|-------------|----------------|
| `create_client()` | New elif returning OpenAI client with custom base_url/api_key | Forgetting to read from env vars |
| `get_response_from_llm()` | New elif with chat.completions.create call | Missing `stop=None` for some providers |
| `get_batch_responses_from_llm()` | New elif with `n=n_responses` | `seed=0` rejected by some providers |
| `make_llm_call()` | New elif — often missed! | Crashes at runtime when this path is hit |
| `make_vlm_call()` | New elif for vision calls | `seed=0` issue again |
| `get_response_from_vlm()` | Check AVAILABLE_VLMS list | Model not in list → ValueError |
| `get_batch_responses_from_vlm()` | New elif without `seed` | Same seed issue |
| Backend `get_ai_client()` | New elif in backend module | Separate from main llm.py |
| AVAILABLE_LLMS list | Add model string | Without this, config validation fails |
| AVAILABLE_VLMS list | Add model string | VLM calls fail silently |
| Token tracker pricing | Add pricing dict entry | Returns $0.00 (cosmetic but confuses users) |
| Config YAML defaults | Update model: fields | Old model used if config not updated |
| CLI arg defaults | Update default= values | Old model used if args not passed |
| Web frontend MODELS list | Add to dropdown | Users can't select new model |

### Step 3: Handle provider-specific quirks

| Quirk | Providers affected | Fix |
|-------|-------------------|-----|
| `seed` parameter rejected | Some OpenAI-compatible APIs | Remove `seed=0` from the new branch |
| `stop=None` required | Some providers | Add `stop=None` explicitly |
| Different model name format | Ollama (`ollama/model`), Bedrock (`bedrock/arn`) | Strip prefix before API call |
| No system message support | Some reasoning models (o1) | Move system msg to user msg |
| Max tokens required | Anthropic | Add `max_tokens` kwarg |
| API key from env | All | Use `os.environ.get("KEY", "")` with fallback |

### Step 4: Verify completeness

```bash
# 1. Syntax check all modified files
python -c "
import ast
for f in modified_files:
    with open(f) as fh: ast.parse(fh.read())
    print(f'OK {f}')
"

# 2. Import test
python -c "
from project.llm import AVAILABLE_LLMS, create_client
print([m for m in AVAILABLE_LLMS if 'new_provider' in m])
"

# 3. Stale reference check
grep -rn 'old-model-name' --include='*.py' --include='*.yaml' project/

# 4. Count dispatch branches
grep -c 'elif "new_provider" in model' file.py
# Should match the number of dispatch functions in that file
```

## .env pattern

Always create/update `.env` with:
```
PROVIDER_API_KEY=sk-xxx
PROVIDER_BASE_URL=https://api.provider.com/v1
```

Add `python-dotenv` to requirements.txt and load in each entry point:
```python
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass
```

**Why `override=True`**: Ensures .env values take precedence over any
environment variables already set in the shell.

**Why try/except**: Makes dotenv optional — works in production where
env vars are set by the container orchestrator.

## Pitfalls

1. **`make_llm_call()` is the most commonly missed function.** It's a lower-level
   wrapper used by other functions. If it raises ValueError for the new model,
   the error only appears when a specific code path (e.g. review, plotting) hits it.

2. **`seed=0` is not universal.** OpenAI accepts it, but many compatible APIs don't.
   Always create a separate elif branch for the new provider rather than falling
   through to the gpt branch.

3. **VLM has its own parallel dispatch.** `vlm.py` is a separate file from `llm.py`
   with its own `create_client()`, `make_llm_call()`, `make_vlm_call()`. All need
   patching independently.

4. **Token tracker pricing is cosmetic but important.** Users see $0.00 and think
   something is broken. Add a placeholder pricing entry.

5. **Config YAML and CLI defaults are separate from code.** Even if all Python
   dispatch is correct, the config file might still reference the old model.

6. **`AVAILABLE_VLMS` list is checked at call time**, not at import time. If the
   model is not in the list, VLM calls raise ValueError even if create_client works.

## Bulk model name changes

When updating model references (e.g. `mimo-v2-pro` → `mimo-v2.5-pro`) across
many files, use `sed -i` for speed rather than individual patch calls:

```bash
sed -i 's/mimo-v2-pro/mimo-v2.5-pro/g' \
  ai_scientist/llm.py \
  launch_scientist_bfts.py \
  bfts_config.yaml \
  web_app.py
```

Then verify zero stale references:
```bash
grep -rn 'old-model-name' --include='*.py' --include='*.yaml' . | grep -v 'new-model-name'
```

## Multi-round audit pattern

Integration across 3+ conversation rounds is common. Each round typically finds
different bugs because different code paths are exercised:

- **Round 1**: Core dispatch (create_client, get_response_from_llm)
- **Round 2**: Lower-level dispatch (make_llm_call) + VLM parallel dispatch
- **Round 3**: Config files (YAML defaults, vlm_feedback.model) + cosmetic (token pricing)

**Lesson**: Don't declare done after round 1. Run a systematic audit
(grep for all dispatch points) before claiming completion.

## Verification checklist

- [ ] All if/elif dispatch chains have new provider branch
- [ ] `create_client()` returns correct client with custom base_url/api_key
- [ ] `make_llm_call()` has new branch (most commonly missed!)
- [ ] `seed=0` removed or conditional for new provider
- [ ] AVAILABLE_LLMS list includes new model
- [ ] AVAILABLE_VLMS list includes new model (if VLM support needed)
- [ ] Token tracker has pricing entry
- [ ] Config YAML defaults updated
- [ ] CLI argument defaults updated
- [ ] .env file created with API key and base URL
- [ ] python-dotenv in requirements.txt
- [ ] dotenv loaded in all entry points
- [ ] Syntax check passes on all modified files
- [ ] Import test passes
- [ ] Zero stale old-model references

## Support files

- `references/ai-scientist-v2-case-study.md` — concrete example of adding
  Xiaomi Mimo to the AI-Scientist-v2 project, including all files modified
  and bugs caught during audit.
- `references/literature-to-proposal-workflow.md` — using AI-Scientist-v2's
  Semantic Scholar tool for systematic literature review and proposal integration.
  Covers query design, competitive analysis, and citation weaving.
