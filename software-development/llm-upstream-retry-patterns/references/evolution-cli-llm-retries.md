# Evolution CLI LLM retry example

Session-derived pattern from a Hermes Agent self-evolution repo update.

## Problem shape

A CLI workflow for skill evolution had already fixed local path/error-routing issues, but remained blocked by upstream model-service availability during synthetic dataset generation.

Observed durable lesson:
- Once the failure mode is clearly an upstream LLM provider outage/unavailability, the local code should add bounded retries/backoff rather than only failing fast.

Non-durable details not to generalize:
- A shell wrapper like `within` being unavailable in one environment.
- Approval-gated attempts to source `.env`.

## Concrete implementation choices that worked

Applied in `evolution/skills/evolve_skill.py`:
- Added `_run_with_llm_retries(step, model, operation, max_attempts=3, initial_delay_seconds=1.0)`
- Wrapped these stages:
  - synthetic dataset generation
  - optimization
  - holdout evaluation
- Preserved concise Click-style terminal errors on final failure
- Added CLI tuning flags:
  - `--llm-max-attempts`
  - `--llm-initial-retry-delay`

## Test strategy that worked

Added focused tests for:
1. transient `ServiceUnavailableError` twice, then success on the third attempt
2. repeated `ServiceUnavailableError` until retry exhaustion, asserting the final CLI error still includes:
   - step name
   - model
   - original provider message

Testing technique:
- monkeypatch `time.sleep` to record delays without slowing the suite
- assert backoff progression directly (for example `[0.25, 0.5]`)

## Why this is reusable

The same pattern fits any multi-stage LLM-backed CLI where:
- stage names should remain visible to the user
- transient upstream failures are common
- local code correctness has already been established
- deterministic regression tests are needed
