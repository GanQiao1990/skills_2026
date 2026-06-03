---
name: streamlit-cli-wrapper
description: "Wrap CLI-based research/ML tools with a Streamlit web UI for non-coding users. Use when building no-code frontends for Python CLI pipelines (AI research tools, data analysis workflows, experiment runners). Covers Chinese-language UI, real-time log streaming, config management, API key management, and multi-provider LLM integration patterns."
tags: [streamlit, frontend, no-code, chinese-ui, cli-wrapper, experiment-runner]
triggers:
  - "Build a web UI for a CLI tool"
  - "Make this tool usable by non-programmers"
  - "Streamlit frontend for research pipeline"
  - "Chinese-language UI for AI tool"
  - "No-code interface for experiment runner"
---

# Streamlit CLI Wrapper

Wrap command-line research/ML tools with a Streamlit web UI so non-technical users can run them without coding.

## When to Use

- User has a Python CLI pipeline (experiment runner, data analysis, model training)
- Target audience lacks coding ability
- Need config management, API key storage, experiment history
- Chinese-language UI preferred (user works in Chinese)

## Architecture Pattern

```
web_app.py          — Streamlit frontend (single file, ~700 lines)
run_web.sh          — One-click launcher with dark theme
.env                — API keys (user edits via Settings page)
bfts_config.yaml    — Model/app config (user edits via Settings page)
```

## Page Structure (6 pages standard)

1. **首页概览 (Dashboard)** — metrics cards (ideas count, experiments count, API status), quick start guide, recent experiments list
2. **研究想法 (Ideas)** — 3 tabs: browse existing JSON ideas, manual create form, upload JSON file
3. **运行实验 (Run Experiment)** — select idea + model config from dropdowns, one-click run with real-time log streaming
4. **论文 & 审稿 (Papers & Reviews)** — view generated PDFs, read AI review JSON, download buttons
5. **实验历史 (History)** — chronological list with delete capability
6. **设置 (Settings)** — 3 tabs: API keys (with connection test buttons), model config editor, data upload

## Key Implementation Patterns

### Real-time log streaming
```python
def run_command_stream(cmd: list[str], cwd: Optional[str] = None):
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, cwd=cwd or str(PROJECT_ROOT),
        env={**os.environ, "AI_SCIENTIST_ROOT": str(PROJECT_ROOT)},
    )
    for line in iter(proc.stdout.readline, ""):
        yield line
    proc.wait()
    yield f"\n[EXIT CODE: {proc.returncode}]\n"
```

Display with:
```python
log_area = st.empty()
log_text = ""
for line in run_command_stream(cmd):
    log_text += line
    log_area.code(log_text[-5000:], language="text")  # show last 5000 chars
```

### .env management (without python-dotenv in Streamlit)
```python
def load_env() -> dict:
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                env[key.strip()] = value.strip()
    return env

def save_env(env: dict):
    # Preserve comments and ordering, update existing keys, append new
    lines = []
    remaining = dict(env)
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                key = stripped.split("=", 1)[0].strip()
                if key in remaining:
                    lines.append(f"{key}={remaining.pop(key)}")
                    continue
            lines.append(line)
    for key, value in remaining.items():
        lines.append(f"{key}={value}")
    ENV_PATH.write_text("\n".join(lines) + "\n")
```

### YAML config editor
```python
import yaml

def load_yaml_config(path: Path) -> dict:
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f) or {}
    return {}

def save_yaml_config(path: Path, config: dict):
    with open(path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
```

### Connection test buttons
```python
# Semantic Scholar test
r = requests.get(
    "https://api.semanticscholar.org/graph/v1/paper/search",
    headers={"X-API-KEY": key} if key else {},
    params={"query": "attention is all you need", "limit": 1},
    timeout=10,
)

# OpenAI-compatible API test (e.g., Mimo)
client = openai.OpenAI(api_key=key, base_url=url)
resp = client.chat.completions.create(
    model="mimo-v2.5-pro",
    messages=[{"role": "user", "content": "Say hello."}],
    max_tokens=50,
)
```

### Dark theme launcher (run_web.sh)
```bash
exec streamlit run web_app.py \
    --server.port "$PORT" \
    --server.address "$HOST" \
    --server.headless true \
    --browser.gatherUsageStats false \
    --theme.primaryColor "#6366f1" \
    --theme.backgroundColor "#0f172a" \
    --theme.secondaryBackgroundColor "#1e293b" \
    --theme.textColor "#f8fafc"
```

## Pitfalls

1. **Don't use st.code() for very long logs** — cap at last 5000 chars or Streamlit slows down
2. **PDF display via iframe with file:// protocol** — may not work in all browsers due to CORS; provide download button as fallback
3. **Import requests/openai inline** in connection test handlers, not at top level — avoids import errors when packages not installed
4. **Model selectors should default to index=0** (the primary model) for all dropdowns
5. **Preflight API probes can fail for the wrong reason** — some OpenAI-compatible gateways reject tiny `max_tokens` probes or newer reasoning-model parameter shapes even when the credentials are valid. For connection tests, prefer a tiny normal chat request like `Reply with ok.` plus `max_completion_tokens=8` (or another small but non-zero completion budget) so the UI doesn't falsely block job launch.
6. **Do not conflate access-key auth with admin-password auth** — if the console supports both distributed user keys and an internal admin password, track `auth_method` in session state and branch validation accordingly. A password-authenticated admin session must not be invalidated just because `auth_key_id` is absent.
7. **UI config controls must map to the backend's real config paths** — never expose friendly top-level fields that the engine does not read. Inspect the actual YAML/JSON schema first and write nested paths directly (for example `agent.num_workers`, `agent.stages.stage1_max_iters`, `agent.search.num_drafts`) instead of dummy placeholders like `max_iters` or `depth`.

## References

- `references/ai-scientist-console-hardening.md` — concrete notes from hardening a Streamlit wrapper around AI Scientist-v2: dual auth, preflight API probes, and nested BFTS config mapping.

## Requirements

```
streamlit
python-dotenv
pyyaml
```

## References

- `references/multi-provider-llm-dispatch.md` — audit checklist when adding new LLM providers to existing codebases
