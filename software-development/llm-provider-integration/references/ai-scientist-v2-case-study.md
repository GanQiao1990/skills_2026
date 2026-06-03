# AI-Scientist-v2: Adding Xiaomi Mimo as LLM Provider

## Project structure

```
AI-Scientist-v2/
├── ai_scientist/
│   ├── llm.py                          # Main LLM dispatch (4 functions)
│   ├── vlm.py                          # Vision LLM dispatch (4 functions)
│   ├── tools/semantic_scholar.py       # S2 API with rate limiting
│   ├── utils/token_tracker.py          # Cost tracking with MODEL_PRICES
│   └── treesearch/backend/
│       ├── __init__.py                 # Routes claude vs openai
│       ├── backend_openai.py           # OpenAI-compatible backend
│       └── backend_anthropic.py        # Anthropic backend
├── launch_scientist_bfts.py            # CLI entry point
├── bfts_config.yaml                    # Default model config
├── web_app.py                          # Streamlit frontend
├── run_web.sh                          # Launcher script
├── requirements.txt
└── .env                                # API keys
```

## Files that needed mimo branches

### ai_scientist/llm.py (4 dispatch points)
1. `get_batch_responses_from_llm()` — elif "mimo" in model
2. `make_llm_call()` — **MISSED IN FIRST PASS** — caused runtime crash
3. `get_response_from_llm()` — elif "mimo" in model
4. `create_client()` — returns OpenAI client with MIMO_BASE_URL

### ai_scientist/vlm.py (4 dispatch points)
1. `make_llm_call()` — elif "mimo" in model
2. `make_vlm_call()` — elif "mimo" in model
3. `create_client()` — elif "mimo" in model
4. `get_batch_responses_from_vlm()` — **seed=0 issue** — mimo rejects it

### ai_scientist/treesearch/backend/backend_openai.py (1 dispatch point)
1. `get_ai_client()` — elif "mimo" in model

### ai_scientist/utils/token_tracker.py
- MODEL_PRICES dict — added mimo-v2.5-pro placeholder pricing

## Bugs caught during audit

1. **make_llm_call() missing mimo branch** — Would crash when review/plotting
   code paths called this function. Only discovered after 3 rounds. This is the
   single most commonly missed function in LLM provider integration.

2. **seed=0 in get_batch_responses_from_vlm()** — mimo API rejects the seed
   parameter. Had to create separate elif branch without seed. The gpt branch
   uses seed=0 for reproducibility; not all OpenAI-compatible APIs accept it.

3. **vlm_feedback.model still gpt-4o** — bfts_config.yaml had `vlm_feedback.model`
   not updated (line 69). Would crash without OpenAI key. Lesson: grep ALL model
   references in YAML configs, not just the obvious ones.

4. **Token tracker returning $0.00** — Cosmetic but confusing. Added placeholder
   pricing entry for mimo-v2.5-pro.

5. **Bulk sed for model name change** — After initial round of individual patch
   calls, used `sed -i 's/mimo-v2-pro/mimo-v2.5-pro/g' file1 file2 file3` for
   the rename from v2 to v2.5. Much faster than 17 individual patches.

## Semantic Scholar integration

- API key via env var `S2_API_KEY`, sent as `X-API-KEY` header
- Rate limit: 1 req/sec enforced via module-level `_s2_rate_limit()` function
- Uses `time.monotonic()` for precise timing
- Applied before every HTTP request (both class method and standalone function)
- Old `time.sleep(1.0)` replaced with rate limiter for consistency

## .env contents

```
S2_API_KEY=s2k-xxx
MIMO_API_KEY=tp-xxx
MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
```

## Web frontend (Streamlit)

6 pages: 首页概览, 研究想法, 运行实验, 论文&审稿, 实验历史, 设置
- Chinese language UI for non-coding users
- Settings page has API connection test buttons
- Model dropdown defaults to mimo-v2.5-pro
- Launches via `bash run_web.sh` or `streamlit run web_app.py`

## Using AI-Scientist-v2 for literature research

The Semantic Scholar tool can be used standalone for systematic literature review:

```python
import sys
sys.path.insert(0, "/path/to/AI-Scientist-v2")
from dotenv import load_dotenv
load_dotenv("/path/to/.env", override=True)
from ai_scientist.tools.semantic_scholar import SemanticScholarSearchTool

tool = SemanticScholarSearchTool()
papers = tool.search_for_papers("your query here")
# Returns: title, authors, venue, year, abstract, citationCount
# Rate limited to 1 req/sec automatically
```

For proposal research: create 8-14 targeted queries covering all key topics,
run sequentially with 1.1s delay, compile into structured report with
competitive analysis and gap identification.
