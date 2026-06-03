# Centralized launch-config pattern for adjacent orchestration repos

Use this when improving one agent/orchestrator project by borrowing the config discipline of another local repo.

## When to apply
- The target repo has launch-critical defaults hardcoded inside a large launcher script.
- The source repo already has a stable config pattern (for example YAML config + dotenv + model/default catalogs).
- The user asks to "use repo A config within repo B" or to align projects.

## Preferred migration shape
1. Add a repo-level YAML config file for stable defaults.
2. Load `.env` early with `python-dotenv` using `load_dotenv(override=True)` inside a guarded `try/except ImportError` block.
3. Add a `--config PATH` CLI override.
4. Support an env override for the config path (for example `AUTOSCIENTISTS_CONFIG=/abs/path/config.yaml`).
5. Keep runtime-sensitive env vars higher priority than YAML defaults.
6. Move launch-critical constants into config-backed helpers instead of inline literals.
7. Make defaults task-aware where appropriate (for example different workshop naming/display text by task type).
8. Validate real request payload keys against the API reference while editing launch code.

## Good precedence order
- explicit CLI flag
- explicit environment variable
- repo YAML config
- hardcoded fallback

## Durable lessons from the AutoScientists improvement
- Centralizing API base URL, naming templates, agent roster sizing, and kickoff text made the launcher easier to adapt without rewriting the script.
- A config-backed agent-roster builder is safer than repeating fixed inline server/GPU tuples.
- When touching launch/bootstrap code, inspect POST payload field names carefully; a single wrong key can silently break initialization. Concrete example seen in practice: `submolt` should have been `workshop` for post creation.
- If repo docs still describe an older weaker model/workflow than the active runbook, patch the docs in the same pass so the repository does not contain conflicting operating instructions.

## Verification sequence
- `python -m py_compile <launcher>.py`
- `<launcher>.py --help`
- parse the new YAML config with Python
- search for stale keys / outdated guidance after edits
- only claim end-to-end success after credentials or required local services are actually present
