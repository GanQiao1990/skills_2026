# Notebook OpenAI-Compatible Gateways

Use this note when adapting a notebook-centric Python project to a custom OpenAI-compatible gateway instead of the default OpenAI endpoint.

## Durable pattern

1. Inspect the code's actual env handling first.
   - If the core code only auto-reads `OPENAI_API_KEY` (and perhaps one service-specific key), do not assume extra `.env` keys like `base_url` or `model` will be applied automatically.
   - Keep `.env` focused on keys the code truly reads, then let notebooks/UI read additional optional keys.

2. Shape `.env` with two layers.
   - Core runtime keys actually used by the code, e.g.:
     - `EDISON_API_KEY=...`
     - `OPENAI_API_KEY=...`
   - Notebook/UI-only convenience keys for the gateway, e.g.:
     - `ROBIN_OPENAI_BASE_URL=https://api-cn1.gptnb.ai/v1`
     - `ROBIN_LLM_MODEL=grok-4-fast-reasoning`

3. In notebooks or app code, build `llm_config` explicitly.
   - Read the convenience env vars.
   - Normalize the model for LiteLLM when using an OpenAI-compatible gateway.
   - Practical rule: if the configured model has no provider prefix, convert `model` to `openai/<model>` before passing it into LiteLLM-backed config.

Example config cell pattern:

```python
import os
from robin.configuration import RobinConfiguration

raw_llm_name = os.getenv("ROBIN_LLM_MODEL", "grok-4-fast-reasoning")
llm_name = raw_llm_name if "/" in raw_llm_name else f"openai/{raw_llm_name}"
base_url = os.getenv("ROBIN_OPENAI_BASE_URL", "https://api-cn1.gptnb.ai/v1")

config = RobinConfiguration(
    disease_name="dry age-related macular degeneration",
    llm_name=llm_name,
    llm_config={
        "model_list": [
            {
                "model_name": llm_name,
                "litellm_params": {
                    "model": llm_name,
                    "api_key": os.getenv("OPENAI_API_KEY", ""),
                    "base_url": base_url,
                    "timeout": 300,
                },
            }
        ]
    },
)
```

## Smoke-test sequence

Use this order to distinguish local config errors from upstream gateway errors:

1. Verify imports and config construction only.
2. Run one real minimal function call that reaches the LLM.
3. If it fails with `LLM Provider NOT provided`, fix the provider-qualified model name first.
4. If it then reaches the gateway and fails with an upstream 5xx, treat that as current gateway behavior, not a local integration failure.

## UI pattern for notebook-centric apps

A simple Gradio app is a good fit for a notebook-centric Python project when the user wants a more approachable interactive frontend without redesigning the backend.

Recommended controls:
- disease name
- run folder name
- num queries / assays / candidates
- model name
- OpenAI-compatible base URL

Recommended outputs:
- run status / step log
- output folder path
- experimental assay summary text
- therapeutic candidate summary text

Implementation notes:
- Reuse the same `RobinConfiguration` construction pattern as the notebook.
- Normalize the model name before building `llm_config`.
- Detect empty `experimental_assay()` returns and fail with a clear message instead of passing `None` downstream.
- Bind the UI to localhost by default, e.g. `127.0.0.1:7860`.

## What not to over-generalize

Do not encode a permanent claim that a specific gateway is broken if a real request reached it and returned a transient server-side 5xx. Save the configuration pattern, not the transient failure.