---
name: upstream-llm-service-triage
description: Diagnose CLI and automation workflows that depend on upstream LLM providers, distinguishing local code/path issues from authentication, rate-limit, timeout, and service-unavailable failures.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  tags: [debugging, llm, cli, retries, authentication, service-unavailable, triage]
---

# Upstream LLM Service Triage

Use this skill when a local CLI, automation script, or evaluation pipeline reaches an upstream model call and then fails with errors such as AuthenticationError, ServiceUnavailableError, RateLimitError, timeout, or provider-specific 5xx failures.

This skill is for class-level troubleshooting of workflows that combine local code with remote model APIs. The core goal is to separate local defects from upstream service or credential issues quickly, then harden the codepath so the failure is reported cleanly.

## When to use

- A command now progresses past local setup and fails only at model invocation
- The failure text mentions an API key, auth, rate limit, timeout, or provider outage
- A retry loop exists but does not classify upstream errors correctly
- You need to decide whether to patch local code, retry, or ask the user to configure credentials

## Workflow

1. Re-run the exact command and capture the first failing stage.
2. Identify whether the failure happens before or after the first remote model call.
3. Classify the exception by both name and module, not just message text.
4. Treat auth errors and provider outages as upstream failures unless there is evidence of a local request-construction bug.
5. If the code already retries transient LLM failures, verify the retry filter includes authentication and provider-specific subclasses where appropriate.
6. Improve the CLI error message so the user sees the step name, model name, and upstream exception class.
7. Add a focused regression test for the newly observed exception shape.

## Pitfalls

- Do not assume a missing API key is a local code-path defect. It is usually an upstream credential problem surfaced by the model client.
- Do not treat all `Exception` subclasses from a model client as retryable. Authentication failures may be non-retryable even if they come from the same module family.
- Do not stop after the first clearer error if the code still omits a relevant exception class from its upstream-error filter.
- Do not rewrite the command or change local paths until you have evidence the failure occurs before remote invocation.

## Recommended implementation pattern

- Maintain a small allowlist of upstream model error class names.
- Also inspect the exception module prefix, such as `litellm` or `openai`, to catch provider-wrapped subclasses.
- Wrap final failures in a concise CLI exception of the form:
  `Failed to <step> with model '<model>': <ExceptionClass>: <message>`
- Keep retry delays exponential and configurable.

## Verification

After patching:

- Re-run the exact command that failed.
- Confirm the failure is either resolved or now reported as a clear upstream credential/service issue.
- Run the focused unit test that exercises the new exception class.
- If the code path is part of a CLI, verify the final error is readable without a stack trace dump.

## Support files

- `references/session-triage-note.md` — concrete command/output pattern from a real session, including `.env` export, base-url retargeting, and the auth→service-unavailable transition.

## Related skills

- `systematic-debugging`
- `llm-upstream-retry-patterns`
- `test-driven-development`
