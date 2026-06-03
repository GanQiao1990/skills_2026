# Commercializing lightweight research web apps

Use this when a research/prototype app (often FastAPI + single static frontend + CLI scripts) needs to become distributable or commercially usable without a full rewrite.

## Preserve the core architecture first
- Keep the working entrypoints unless the user explicitly asks for a rewrite: existing CLI, FastAPI backend, and static frontend can remain.
- Add product-grade seams around the prototype: config, auth, persistence, storage isolation, docs, and smoke tests.
- Avoid introducing a large frontend build chain or heavy framework if the current app is intentionally lightweight.

## Minimum commercial-ready structure
Recommended additions:
- `backend/config.py`: environment loading, path config, model/API config, resource limits.
- `backend/db.py`: database schema + DAO layer; SQLite is acceptable for self-hosted/demo, with a migration path to Postgres.
- `backend/security.py`: password hashing and session/token helpers.
- `backend/auth.py`: current-user dependency and public user serializer.
- `backend/models.py`: Pydantic request/response shapes.
- `backend/storage.py`: atomic file writes and per-user storage paths.
- `backend/prompts.py` or equivalent: prompt profiles/templates separated from API handlers.
- `docs/COMMERCIALIZATION.md`: product positioning, deployment, data model, stability, roadmap.
- `scripts/smoke_test.py`: auth + health + save/list minimal verification.

## Multi-user and data isolation pattern
- Add `users`, `sessions`, `saved_results`, `prompt_profiles`, and `audit_events` tables.
- Store session token hashes, not plaintext tokens.
- Hash passwords with a slow KDF (PBKDF2/bcrypt/argon2). If avoiding new dependencies, PBKDF2-HMAC-SHA256 from stdlib is acceptable.
- Save generated files under `data/results/<user_id>/...` and gate downloads through DB owner checks; do not rely on filename/path secrecy.
- Keep `.env` secrets and runtime `data/` gitignored.

## Stability basics for small self-hosted deployments
- SQLite: enable WAL and `busy_timeout`; use atomic writes for JSON/file outputs.
- Add global exception handling that hides tracebacks from users but records audit/debug detail.
- Add resource caps such as `MAX_SEARCH_RESULTS`, `MAX_SUMMARY_PAPERS`, request timeouts, and API retry/backoff.
- Verify with compile/import checks and a local smoke test that exercises auth, DB, prompt profile listing, save, and list.

## Prompt-interactive AI feature pattern
- Do not leave product prompts hard-coded inside API handlers.
- Provide built-in profiles for common user habits (academic review, student quick reading, business brief, evidence table).
- Let users save custom prompt profiles with system prompt, section structure, default style, and depth.
- At generation time combine: paper corpus + selected profile + audience + language + depth + citation rule + custom user instruction.
- Include anti-hallucination constraints tied to supplied papers/abstracts.

## Verification checklist
1. Compile/import check: `python -m compileall backend ...` and import the FastAPI app.
2. DB schema check: connect and confirm expected tables exist.
3. Run service on a free port if default is occupied.
4. Smoke test: health, register/login, `/auth/me`, prompt profiles, save result, list saved results.
5. Clean transient runtime data created by tests if it should not be distributed.
