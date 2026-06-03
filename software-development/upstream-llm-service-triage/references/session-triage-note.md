# Session triage note: upstream LLM service failures in self-evolution

Observed pattern from a real run of `python -m evolution.skills.evolve_skill --skill github-code-review --iterations 10 --eval-source synthetic`:

1. With `.env` loaded incorrectly, the run failed at the first remote model call with `AuthenticationError` complaining that `OPENAI_API_KEY` was missing.
2. After exporting the env vars properly and confirming `OPENAI_API_KEY` and `OPENAI_BASE_URL` were present, the same command progressed into synthetic dataset generation and then failed with `ServiceUnavailableError` from `litellm.ServiceUnavailableError` / `OpenAIException`.
3. The local code path and retry wrapper were therefore healthy; the remaining blocker was upstream provider availability or endpoint behavior.
4. A useful shell pattern for project `.env` files is:

```bash
set -a
source /path/to/.env
set +a
```

This ensures variables from the file are exported to child processes such as `python`.

5. In this workflow, changing `OPENAI_BASE_URL` in `.env` is a valid way to retarget an OpenAI-compatible endpoint without changing the code.
6. If the new endpoint still returns `ServiceUnavailableError`, the next durable improvement is usually fallback logic: alternate model/base URL, or skip synthetic dataset generation and use an existing dataset source instead.
