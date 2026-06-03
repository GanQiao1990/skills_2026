# AI-Scientist-v2 Dispatch Point Map

Complete model-dispatch inventory as of 2026-05-26.
Every `elif` branch below must exist for a new provider to work.

## ai_scientist/llm.py

### `get_batch_responses_from_llm()` — batch/ensemble calls
- Line 109: `if model.startswith("ollama/")`
- Line 126: `elif "gpt" in model`
- Line 144: `elif model == "deepseek-coder-v2-0724"`
- Line 161: `elif model == "llama-3-1-405b-instruct"`
- Line 178: `elif 'gemini' in model`
- Line 195: `elif "mimo" in model`
- Line 212: `else` (fallback to single-response loop)

### `make_llm_call()` — single call helper (used by writeup/review)
- Line 242: `if model.startswith("ollama/")`
- Line 254: `elif "gpt" in model`
- Line 267: `elif "o1" in model or "o3" in model`
- Line 278: `elif "mimo" in model`
- Line 290: `else raise ValueError`

### `get_response_from_llm()` — main single-response
- Line 305: `if "claude" in model`
- Line 337: `elif model.startswith("ollama/")`
- Line 352: `elif "gpt" in model`
- Line 363: `elif "o1" in model or "o3" in model`
- Line 374: `elif model == "deepseek-coder-v2-0724"`
- Line 389: `elif model == "deepcoder-14b"`
- Line 433: `elif model in ["meta-llama/llama-3.1-405b-instruct", ...]`
- Line 448: `elif 'gemini' in model`
- Line 462: `elif "mimo" in model`
- Line 477: `else raise ValueError`

### `create_client()` — client factory
- Line 521: `if model.startswith("claude-")`
- Line 524: `elif model.startswith("bedrock") and "claude" in model`
- Line 528: `elif model.startswith("vertex_ai") and "claude" in model`
- Line 532: `elif model.startswith("ollama/")`
- Line 538: `elif "gpt" in model`
- Line 541: `elif "o1" in model or "o3" in model`
- Line 544: `elif model == "deepseek-coder-v2-0724"`
- Line 553: `elif model == "deepcoder-14b"`
- Line 565: `elif model == "llama3.1-405b"`
- Line 574: `elif 'gemini' in model`
- Line 583: `elif "mimo" in model`
- Line 592: `else raise ValueError`

## ai_scientist/vlm.py

### `make_llm_call()` — VLM text-only calls
- `ollama/`, `gpt`, `o1/o3`, `mimo`

### `make_vlm_call()` — VLM vision+text calls
- `ollama/`, `gpt`, `mimo`

### `create_client()` — VLM client factory
- explicit model list, `ollama/`, `mimo`

## ai_scientist/treesearch/backend/backend_openai.py

### `get_ai_client()` — tree-search client factory
- `ollama/`, `mimo`, default (OpenAI)

## Common mistakes

1. **Forgetting `make_llm_call()` in llm.py** — it's called by writeup/review code, NOT by the main experiment loop. Easy to miss because it's not in the `get_response_from_llm` path.
2. **Forgetting vlm.py entirely** — it's a separate module with its own dispatch chains.
3. **Not adding dotenv to backend_openai.py** — it uses `os.environ.get()` but without dotenv the .env file isn't loaded.
