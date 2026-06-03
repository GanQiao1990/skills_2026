---
name: llm-upstream-retry-patterns
description: Add resilient retry/backoff handling around upstream LLM service calls while preserving clear terminal-facing failures and focused regression tests.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [llm, retry, backoff, resilience, cli, dspy, litellm, error-handling]
---

# LLM Upstream Retry Patterns

Use this skill when a local workflow is correct but blocked by transient upstream LLM provider failures such as `ServiceUnavailableError`, timeout, rate limit, or API connection errors.

This is for improving resilience in CLIs, scripts, evaluation pipelines, and optimization loops that call hosted LLMs.

Do not encode environment-specific setup failures here (missing binaries, missing wrappers, missing credentials). Those belong in setup/troubleshooting skills.

## When to use

Trigger this skill when all of the following are true:
1. The failing path is an upstream LLM call, not a local path/import/config bug.
2. The task would reasonably succeed if retried later.
3. The user needs the workflow to degrade gracefully instead of failing immediately on the first transient provider error.

Common examples:
- Synthetic dataset generation via a judge model
- LLM-backed optimization/teleprompt loops
- Holdout evaluation or rubric scoring
- Multi-stage CLI pipelines that make several independent LLM calls

## Core pattern

1. Identify the exact LLM-backed step names.
   - Give each step a human-readable label like `build synthetic evaluation dataset`, `run optimization`, or `evaluate holdout set`.
   - Preserve that label in all final error messages.

2. Detect upstream-provider errors by class/module, not message substring alone.
   - Match known exception names such as `APIConnectionError`, `APITimeoutError`, `InternalServerError`, `OpenAIError`, `RateLimitError`, `ServiceUnavailableError`.
   - Also allow module-based detection for wrappers such as `litellm.*` or `openai.*`.

3. Wrap the operation in a reusable retry helper.
   - Inputs should include: `step`, `model`, `operation`, `max_attempts`, and `initial_delay_seconds`.
   - Retry only transient upstream LLM errors.
   - Re-raise non-LLM exceptions immediately.

4. Use bounded exponential backoff.
   - Default to small, explicit values suitable for CLI use.
   - Good baseline: `max_attempts=3`, `initial_delay_seconds=1.0`.
   - Double the delay after each failed attempt.

5. Keep terminal-facing errors concise on final failure.
   - After the last attempt, raise a short CLI error that keeps the original step name, model, exception class, and exception message.
   - Example shape: `Failed to <step> with model '<model>': <ExceptionType>: <message>`

6. Print retry notices before sleeping.
   - Emit a concise warning showing attempt number, model, exception type, and next delay.
   - This helps the user distinguish a transient provider issue from a local hang.

7. Expose retry tuning at the CLI boundary.
   - Add options such as `--llm-max-attempts` and `--llm-initial-retry-delay`.
   - Pass these values through to every LLM-backed stage that should share the same retry policy.

8. Add focused regression tests.
   - Test transient failure then success.
   - Test retry exhaustion produces the intended final CLI error.
   - Monkeypatch sleep in tests so the suite remains fast and deterministic.

## Pitfalls

- Do not swallow the final error after retries.
- Do not retry arbitrary local exceptions; that hides real bugs.
- Do not hardcode retry behavior only around the first failing stage if later stages use the same upstream model path.
- Do not rely only on raw message text like `503` for detection.
- Do not turn a clear one-line CLI failure into a long traceback unless debugging was explicitly requested.
- Do not record shell-wrapper failures (`command not found`, missing `within`, absent `.env` loader) as durable retry guidance.

## Verification checklist

- A transient provider failure triggers retry warnings and then succeeds, or fails cleanly after the last attempt.
- The final CLI error still names the exact step and model.
- Non-LLM exceptions still fail immediately.
- Tests cover success-after-retry and failure-after-exhaustion.
- CLI help exposes the retry controls if the workflow is user-invoked.

## Minimal implementation shape

```python

def run_with_llm_retries(step, model, operation, max_attempts=3, initial_delay_seconds=1.0):
    attempts = max(1, max_attempts)
    delay = max(0.0, initial_delay_seconds)
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except Exception as e:
            if not is_llm_service_error(e):
                raise
            if attempt >= attempts:
                raise_cli_error(step, model, e)
            print_retry_warning(step, model, attempt, attempts, e, delay)
            if delay > 0:
                time.sleep(delay)
                delay *= 2
```

## Reference

For a concrete session-derived example covering a DSPy-based evolution CLI, see `references/evolution-cli-llm-retries.md`.
