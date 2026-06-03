# Multi-Provider LLM Dispatch Audit Checklist

When adding a new LLM provider (e.g., Xiaomi Mimo, DeepSeek, Gemini) to an existing multi-provider codebase, use this checklist to avoid silent runtime crashes.

## The Problem

Most multi-provider LLM codebases use `if/elif` chains dispatching on model name substrings:

```python
if "gpt" in model:
    ...
elif "claude" in model:
    ...
elif "ollama" in model:
    ...
else:
    raise ValueError(f"Model {model} not supported.")
```

Adding a new model requires adding branches to **every** dispatch function. Missing even one causes a runtime crash only hit when that code path executes.

## Audit Steps

### Step 1: Find ALL dispatch points
```bash
# Search for model dispatch patterns
grep -rn 'elif.*in model\|if.*in model\|model\.startswith\|model ==' --include='*.py' . | grep -v __pycache__
```

### Step 2: For each file, list all functions with dispatch
Read each file and document:
- Function name
- Full dispatch chain (which models are handled)
- Whether new provider has a branch
- What happens if missing (crash? silent wrong behavior?)

### Step 3: Check each dispatch function
Common functions that need dispatch (in a typical LLM codebase):
- `create_client()` — creates the API client
- `get_response_from_llm()` — single response
- `get_batch_responses_from_llm()` — multiple responses (ensembling)
- `make_llm_call()` — lower-level call helper
- `get_ai_client()` — treesearch backend client creation
- `make_vlm_call()` — vision model calls
- `get_response_from_vlm()` — VLM single response
- `get_batch_responses_from_vlm()` — VLM batch response

### Step 4: Check for API compatibility issues
Different providers have different API quirks:
- **seed parameter**: OpenAI supports it, many proxies don't — create separate branch without seed
- **system message position**: Some APIs need system as first message, others as separate parameter
- **max_tokens vs max_completion_tokens**: Some APIs use different parameter names
- **stop parameter**: Some APIs don't support stop sequences
- **n parameter**: Some APIs don't support n > 1 for multiple responses

### Step 5: Check AVAILABLE_MODELS lists
Many codebases have `AVAILABLE_LLMS` and `AVAILABLE_VLMS` lists that gate model validation:
```python
AVAILABLE_LLMS = ["gpt-4o", "claude-3-5-sonnet", ...]
# New model MUST be added here or get_response_from_llm() rejects it
```

### Step 6: Check config defaults
Update all config files and argument defaults:
- YAML config files (e.g., bfts_config.yaml)
- argparse defaults in launcher scripts
- Hardcoded fallback models in utility functions (log_summarization.py, journal.py)

### Step 7: Add dotenv loading
If the new provider uses environment variables for API keys, add `load_dotenv()` to:
- Main entry point (launch script)
- LLM module (llm.py)
- VLM module (vlm.py)
- Backend module (backend_openai.py)
- Any tool that makes API calls (semantic_scholar.py)

```python
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass
```

## Real-World Bug Example

In AI-Scientist-v2, adding `mimo-v2.5-pro` required branches in:
- `llm.py`: 4 functions (get_batch, make_llm_call, get_response, create_client)
- `vlm.py`: 4 functions (make_llm_call, make_vlm_call, create_client, get_batch)
- `backend_openai.py`: 1 function (get_ai_client)

**Bug caught**: `make_llm_call()` in llm.py was missing the mimo branch. This function is called by `get_response_from_llm()` for gpt/o1/o3 models, but mimo uses a different path. However, if any code path called `make_llm_call()` directly with a mimo model, it would crash with `ValueError`.

**API compat bug**: `vlm.py` `get_batch_responses_from_vlm()` sent `seed=0` for all non-ollama models. Mimo API rejects this parameter. Fixed by adding a separate mimo branch without seed.

## Quick Verification Command

```bash
# Count dispatch branches for new provider across all files
grep -rn 'elif "newprovider" in model' --include='*.py' .

# Verify all files parse correctly
python -c "
import ast
for f in ['file1.py', 'file2.py', ...]:
    with open(f) as fh: ast.parse(fh.read())
    print(f'OK {f}')
"
```
