---
name: integrate-openai-compatible-provider
description: "Add a custom OpenAI-compatible API provider (e.g. Xiaomi Mimo, Deepseek, vLLM, Ollama) to an existing Python codebase that uses the openai SDK. Covers the critical pitfall of missing dispatch points."
trigger:
  - "User asks to add a new LLM provider/model to an existing project"
  - "User provides a base_url + api_key for an OpenAI-compatible endpoint"
  - "Integrating Xiaomi Mimo, Deepseek, custom vLLM, or similar into AI-Scientist, Axolotl, etc."
---

# Integrate an OpenAI-Compatible API Provider

## When to use
The user gives you a base URL + API key for an LLM endpoint that speaks the OpenAI chat/completions protocol (e.g. Xiaomi Mimo, Deepseek, a self-hosted vLLM, LiteLLM proxy). You need to wire it into an existing Python project.

## Critical Pitfall: Missing Dispatch Points

**This is the #1 failure mode.** Most LLM codebases have MULTIPLE model-dispatch locations — not just one. If you miss even one, the code crashes at runtime with `ValueError: Model X not supported`.

**Best practice: Audit first, then fix.** Use `delegate_task` to run a parallel audit of all Python files before making any edits. This catches dispatch points that grep alone might miss (e.g. fallback branches in else clauses, batch functions in separate modules).

### Step 1: Find ALL dispatch points BEFORE editing anything

Search for these patterns in the codebase:

```bash
# Find model-name dispatch chains (if/elif on model string)
grep -rn '"gpt"' --include='*.py' .
grep -rn '"claude"' --include='*.py' .
grep -rn 'startswith("ollama' --include='*.py' .
grep -rn 'in model' --include='*.py' .
grep -rn 'ValueError.*not supported' --include='*.py' .
grep -rn 'def create_client' --include='*.py' .
grep -rn 'def get_ai_client' --include='*.py' .
```

### Step 2: Catalog every dispatch point

In AI-Scientist-v2, the dispatch points are in **3 files, 9 functions**:

| File | Function | Purpose |
|------|----------|---------|
| `ai_scientist/llm.py` | `get_batch_responses_from_llm()` | Ensemble/batch LLM calls |
| `ai_scientist/llm.py` | `make_llm_call()` | Single LLM call (used by writeup, review) |
| `ai_scientist/llm.py` | `get_response_from_llm()` | Main single-response LLM call |
| `ai_scientist/llm.py` | `create_client()` | Client factory |
| `ai_scientist/vlm.py` | `make_llm_call()` | VLM text-only calls |
| `ai_scientist/vlm.py` | `make_vlm_call()` | VLM vision+text calls |
| `ai_scientist/vlm.py` | `create_client()` | VLM client factory |
| `ai_scientist/vlm.py` | `get_batch_responses_from_vlm()` | VLM batch (has `seed=0` pitfall) |
| `ai_scientist/treesearch/backend/backend_openai.py` | `get_ai_client()` | Tree-search backend client |

**Total: 9 dispatch points across 3 files + 1 pricing config.**

| `ai_scientist/utils/token_tracker.py` | `MODEL_PRICES` dict | Token cost tracking (silently returns $0.00 if missing) |

**The `make_llm_call()` in llm.py was the hardest to spot** — it's called by writeup/review code, not by the main experiment loop. Missed it in the first pass → runtime crash.

### Step 3: Add the provider branch to EVERY dispatch point

Pattern for each:

```python
elif "mimo" in model:  # or your provider name
    # For create_client / get_ai_client:
    return openai.OpenAI(
        api_key=os.environ.get("MIMO_API_KEY", ""),
        base_url=os.environ.get("MIMO_BASE_URL", "https://your-endpoint.com/v1"),
        max_retries=max_retries,
    ), model

    # For call functions:
    return client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            *prompt,
        ],
        temperature=temperature,
        max_tokens=MAX_NUM_TOKENS,
        n=1,
        stop=None,
    )
```

### Step 4: Register the model name

Add to every `AVAILABLE_*` list:
- `AVAILABLE_LLMS` in llm.py
- `AVAILABLE_VLMS` in vlm.py (if vision-capable)

### Step 5: Add dotenv loading

Add to every file that reads env vars:

```python
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass
```

Files that need this in AI-Scientist-v2:
- `ai_scientist/llm.py`
- `ai_scientist/vlm.py`
- `ai_scientist/tools/semantic_scholar.py`
- `ai_scientist/treesearch/backend/backend_openai.py`
- `launch_scientist_bfts.py`

### Step 6: Create .env file

```env
# Provider API key
MIMO_API_KEY=your-key-here
MIMO_BASE_URL=https://your-endpoint.com/v1
```

### Step 6.5: Update token pricing

If the codebase has a token cost tracker (e.g. `token_tracker.py` with `MODEL_PRICES` dict), add the new model's pricing. Otherwise cost tracking silently returns $0.00 — not a crash, but misleading in reports.

### Step 7: Update defaults

- `bfts_config.yaml` — model fields
- CLI arg defaults in launcher scripts
- Web UI model dropdowns

## Xiaomi MiMo TTS compatibility notes

When the user is integrating Xiaomi MiMo beyond plain text chat, remember that the TTS path may still be exposed through the OpenAI-compatible chat endpoint rather than a separate `/audio/speech` route.

Observed working pattern for `mimo-v2.5-tts`:
- endpoint: `POST <base_url>/chat/completions`
- headers: keep normal OpenAI-style auth; adding `api-key: ...` alongside bearer auth is also accepted by MiMo examples and is a safe compatibility fallback
- request must include an `assistant` role message containing the text to be spoken
- request should include `modalities: ["text", "audio"]`
- request should include `audio: {"voice": "<supported voice>", "format": "mp3"}`
- successful responses return base64 audio in `choices[0].message.audio.data`

Important MiMo-specific pitfalls:
- Do not assume OpenAI's `/audio/speech` endpoint exists on a proxy just because the model list includes a TTS model. Probe or test first.
- MiMo rejects TTS calls that omit an `assistant` role with an error equivalent to `messages must contain an assistant role for TTS model`.
- MiMo rejects generic voice labels like `female`; use an exact supported voice name such as `mimo_default`, `冰糖`, `茉莉`, `苏打`, `白桦`, `Mia`, `Chloe`, `Milo`, or `Dean`.
- For long-form audiobook generation, split text into short chunks, decode each returned base64 MP3, then concatenate with ffmpeg.

See `references/mimo-tts-openai-compat.md` for the concrete request/response pattern and a project-layout suggestion for long-form TTS jobs.

## API Compatibility Pitfalls

### Xiaomi MiMo TTS can be chat-completions based, not audio-endpoint based
Some Xiaomi MiMo compatible proxies expose TTS through `POST /chat/completions` rather than `/audio/speech`. In a validated session, `/v1/audio/speech` and similar routes returned 404, while `model='mimo-v2.5-tts'` worked on `/chat/completions` with:
- an `assistant` message containing the narration text
- `modalities: ['text', 'audio']`
- provider-specific `audio.voice` values such as `冰糖`
- base64 audio returned at `choices[0].message.audio.data`

See `references/mimo-tts-compat.md` for the exact working request shape, accepted voice list, and long-form audiobook project layout.

### seed parameter
OpenAI supports `seed=0` for reproducibility. **Most proxy APIs (Mimo, Deepseek, vLLM) reject this parameter.** When adding a new provider to a batch/ensemble function, always create a separate branch WITHOUT `seed`:

```python
# WRONG: single else branch for all non-OpenAI models
else:
    response = client.chat.completions.create(..., seed=0)  # Mimo rejects this!

# RIGHT: separate mimo branch without seed
elif "mimo" in model:
    response = client.chat.completions.create(..., stop=None)  # no seed
else:
    response = client.chat.completions.create(..., seed=0)  # OpenAI only
```

This was caught in `vlm.py` `get_batch_responses_from_vlm()` — the `else` branch sent `seed=0` for all non-ollama models, crashing Mimo API calls.

### Other common API differences
- `max_tokens` vs `max_completion_tokens` (some APIs use different names)
- System message position (some need it as first message, not separate param)
- `n` parameter (some APIs don't support n > 1)
- `stop` parameter (some APIs don't support stop sequences)

## Support files

- `references/ai-scientist-v2-dispatch-map.md` — exact line numbers for every dispatch point in AI-Scientist-v2
- `templates/env.example` — .env template with all known provider keys
- `scripts/verify_dispatch.py` — run `python verify_dispatch.py <provider>` to check all dispatch points are covered

## Verification checklist

After editing, run:

```bash
# 1. Syntax check all modified files
python -c "
import ast
for f in ['file1.py', 'file2.py', ...]:
    with open(f) as fh: ast.parse(fh.read())
    print(f'OK {f}')
"

# 2. No stale model references
grep -rn 'old-model-name' --include='*.py' . | grep -v 'new-model-name'

# 3. All dispatch points covered
grep -n '"provider"' file1.py file2.py  # should show N matches = N dispatch points

# 4. Import test
python -c "
from module import AVAILABLE_LLMS
print([m for m in AVAILABLE_LLMS if 'provider' in m])
"

# 5. List all 'not supported' error paths — confirm each has your branch
grep -n 'not supported' --include='*.py' -r .
```

## AI-Scientist-v2 specific notes

- `make_llm_call()` in llm.py has a DIFFERENT signature than `get_response_from_llm()` — it takes `(client, model, temperature, system_message, prompt)` not `(prompt, client, model, system_message, ...)`
- `vlm.py` functions are nearly identical to `llm.py` but in a separate module for vision models
- The `elif "mimo" in model:` check uses `in` not `==` — this catches `mimo-v2-pro`, `mimo-v2.5-pro`, any future `mimo-*` variant
- Rate limiting for external APIs (like Semantic Scholar) should use a module-level `_rate_limit()` function with `time.monotonic()`, not `time.sleep()` inline
- For building a no-code Streamlit frontend around the CLI tool, see the `streamlit-cli-wrapper` skill
