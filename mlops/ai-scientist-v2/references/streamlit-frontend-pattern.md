# Streamlit No-Code Frontend for CLI Research Tools

## When to Use

When wrapping a command-line scientific pipeline (AI-Scientist, custom ML pipelines, bioinformatics workflows) for non-coding users.

## Architecture Pattern

Single `web_app.py` file with Streamlit. No framework, no REST API, no database.

### Page Structure (6 pages)
1. **Dashboard** — metrics (counts of items), quick start guide, recent activity
2. **Data/Config Manager** — CRUD for input files (ideas, configs, datasets) with forms + file uploaders
3. **Run Page** — select inputs, configure parameters via dropdowns/sliders, submit with live log streaming
4. **Results Viewer** — display outputs (PDFs, JSONs, reviews) with download buttons
5. **History** — list past runs with delete capability
6. **Settings** — API keys (password inputs), model config, connection test buttons

### Live Log Streaming Pattern

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

# In page:
log_area = st.empty()
log_text = ""
for line in run_command_stream(cmd):
    log_text += line
    log_area.code(log_text[-5000:], language="text")  # tail last 5000 chars
```

### .env Management Pattern (no dotenv dependency in frontend)

```python
def load_env() -> dict:
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip()
    return env

def save_env(env: dict):
    # Preserve comments/order, update matching keys, append new ones
```

### API Connection Testing

Always provide test buttons in Settings. For OpenAI-compatible APIs:

```python
client = openai.OpenAI(api_key=key, base_url=url)
resp = client.chat.completions.create(
    model="model-name",
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
    max_tokens=50,
)
```

For REST APIs (like Semantic Scholar):

```python
r = requests.get(url, headers={"X-API-KEY": key}, params={...}, timeout=10)
```

### Launch Script (run_web.sh)

```bash
#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
pip install -q streamlit python-dotenv pyyaml 2>/dev/null
exec streamlit run web_app.py \
    --server.port 8501 --server.address 0.0.0.0 \
    --server.headless true --browser.gatherUsageStats false
```

## UI Tips for Chinese Users

- Use Chinese labels for navigation: 首页概览, 研究想法, 运行实验, 论文 & 审稿, 设置
- Use emoji prefixes for nav items: 🏠 💡 🚀 📄 ⚙️
- Form submit buttons: 💾 保存, 🚀 开始运行, 📤 上传
- Status indicators: ✅ 已配置, ❌ 未配置, 📄 已生成论文
- `st.balloons()` on success — small delight for non-technical users

## Theme (Dark Mode)

```
--theme.primaryColor "#6366f1"
--theme.backgroundColor "#0f172a"
--theme.secondaryBackgroundColor "#1e293b"
--theme.textColor "#f8fafc"
```

## Dependencies

```
streamlit
python-dotenv
pyyaml
```
