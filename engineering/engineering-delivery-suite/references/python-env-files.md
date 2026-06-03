# Python `.env` files for notebook-driven projects

Condensed lessons from a Robin setup/debug session.

## 1. Verify what the code actually reads
Before editing `.env`, inspect the code for:
- `load_dotenv()`
- `os.getenv("...")`
- config objects that derive defaults from env vars

Do not assume extra keys in `.env` are used just because they look plausible.

## 2. Common failure mode: YAML-like content inside `.env`
A malformed `.env` may contain lines like:

```text
api_key: sk-...
base_url: https://example/v1
model: grok-4-fast-reasoning
```

`python-dotenv` expects `KEY=VALUE`, not YAML. Convert only the keys that the code actually consumes.

## 3. Preserve secrets, normalize shape
When rewriting `.env`:
- preserve existing secret values
- normalize formatting to `KEY=VALUE`
- add short comments about which keys are auto-read
- avoid inventing unused variables unless the code will be updated too

## 4. Robin-specific note
In this repo, `robin/configuration.py` auto-reads:
- `EDISON_API_KEY`
- `OPENAI_API_KEY`

It does **not** auto-read gateway/model overrides such as `base_url` or `model` from `.env`.

If the user wants a custom OpenAI-compatible endpoint or model, they must pass `llm_name` / `llm_config` explicitly in notebook or Python code.

## 5. Good rewrite pattern
```dotenv
# Project runtime environment
# Auto-read by the application:
EDISON_API_KEY=...
OPENAI_API_KEY=...

# Notes:
# - The application auto-loads this file via python-dotenv.
# - Only the keys above are auto-read by current code.
# - Custom gateway/model settings must be passed in notebook/code.
# Optional notebook override base_url: https://...
# Optional notebook override model: ...
```
