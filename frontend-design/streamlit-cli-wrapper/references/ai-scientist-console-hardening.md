# AI Scientist Streamlit console hardening

Use this when wrapping AI-Scientist-v2 or similar research CLIs with a Streamlit control plane.

## Durable lessons

### 1. Separate auth modes explicitly
If the app supports both:
- distributed access keys for end users, and
- an internal admin password,

then `st.session_state` must track `auth_method` and validate each mode separately.

Bad pattern:
- globally requiring `auth_key_id` whenever access-key mode exists
- this accidentally ejects password-authenticated admins

Good pattern:
- `auth_method == "access_key"` -> require `auth_key_id`
- `auth_method == "password"` -> do not require `auth_key_id`
- if both auth methods are configured, present both login paths in the UI

### 2. API preflight probes should match gateway quirks
A gateway can reject a tiny or malformed probe even when credentials are valid.

Observed good probe shape:
- messages: `[{"role": "user", "content": "Reply with ok."}]`
- `max_completion_tokens=8`

Observed bad probe shape for one OpenAI-compatible gateway:
- `max_tokens=2`
- this returned a 400-style "output limit reached" error and incorrectly made the frontend think auth/config was broken

Lesson:
- if a preflight check fails, verify with a second minimal request before treating it as invalid credentials
- prefer a tiny but realistic completion request over hyper-minimal probes

### 3. Frontend config widgets must write the real backend schema
Before exposing tuning controls, inspect the true config consumed by the engine.

In AI-Scientist-v2, the backend actually reads nested fields such as:
- `agent.num_workers`
- `agent.steps`
- `agent.stages.stage1_max_iters`
- `agent.stages.stage2_max_iters`
- `agent.stages.stage3_max_iters`
- `agent.stages.stage4_max_iters`
- `agent.search.num_drafts`
- `agent.search.max_debug_depth`
- `agent.search.debug_prob`
- `agent.multi_seed_eval.num_seeds`

Do not expose fake top-level fields like:
- `max_iters`
- `num_branches`
- `depth`

unless the runtime really consumes them.

### 4. Old helper/example files may drift behind the runtime API
In this repo, `create_client()` now returns a tuple:
- `(client, client_model)`

Any example/helper file that still does:
- `client = create_client(model)`

will silently drift out of date. When hardening a productized console around an actively changing backend, search examples/templates for old call signatures and patch them too.

## Minimal verification checklist

1. `python -m py_compile web_app.py`
2. Verify the preflight API helper returns success with the current gateway
3. Start Streamlit on a test port
4. Confirm the port is listening
5. Confirm `curl http://127.0.0.1:<port>/` returns `200 OK`
6. If the wrapper launches backend jobs, run one tiny self-test job and confirm status/log files are written
