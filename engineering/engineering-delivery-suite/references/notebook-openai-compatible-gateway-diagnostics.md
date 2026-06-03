# Notebook OpenAI-Compatible Gateway Diagnostics

Use this pattern when a notebook-centric Python app (or a thin local UI over it) calls an OpenAI-compatible gateway through LiteLLM and fails during the first real LLM step.

## Durable workflow

1. Validate the gateway itself before changing application code.
   - Call `GET /models` with the current bearer token.
   - Confirm the gateway returns a valid model list.

2. Run a minimal `POST /chat/completions` smoke test against a few candidate models.
   - Test the intended model.
   - Test the provider-qualified form if LiteLLM is involved (for example `openai/<model>`).
   - Test a simple known-good baseline model from the returned model list (for example `gpt-4o-mini`).

3. Interpret outcomes carefully.
   - If LiteLLM says `LLM Provider NOT provided`, the application must normalize bare model names to a provider-qualified form such as `openai/<model>`.
   - If the gateway returns 5xx for one model but 200 for another, the integration path is working; the failing model is currently not usable through that gateway.
   - If a model returns a provider-specific business error (for example pricing / ratio not configured), keep that as evidence about the current model choice, not as a rule that the gateway is generally broken.

4. Choose a stable default.
   - Set the notebook/UI default to a model that passed the direct smoke test.
   - Keep the original target model configurable, but do not leave it as the default if it is currently returning upstream 5xx errors.

5. Rerun the app after the LLM fix.
   - If the next failure moves downstream (for example Edison returns 403 / org permission errors), record that the LLM gateway issue is resolved and the remaining blocker is a different service.

## Robin-specific application

For this repo, the notebook/UI layer should read:
- `ROBIN_OPENAI_BASE_URL`
- `ROBIN_LLM_MODEL`

Then build `llm_config` explicitly and normalize the model for LiteLLM:
- bare `gpt-4o-mini` -> `openai/gpt-4o-mini`
- bare `grok-4-fast-reasoning` -> `openai/grok-4-fast-reasoning`

When the gateway's `/models` endpoint advertises a model but direct `chat/completions` returns upstream 5xx for that model, trust the smoke test over the catalog and switch the default to a known-good model until the gateway recovers.
