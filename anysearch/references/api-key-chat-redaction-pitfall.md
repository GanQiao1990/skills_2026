# AnySearch API key configuration pitfall in Hermes CLI sessions

Problem pattern:
- The user pastes an `ANYSEARCH_API_KEY` directly into chat and asks the agent to save it.
- The saved `.env` entry may contain a masked/redacted value rather than the full secret.
- A subsequent real search returns `invalid_api_key` even though the user appeared to provide a key.

Durable handling rule:
1. Save the key only when the user explicitly asks.
2. Persist it to the skill-local file: `<skill_dir>/.env` with the exact line `ANYSEARCH_API_KEY=<key>`.
3. Immediately verify with a real AnySearch CLI `search` call.
4. If verification returns `invalid_api_key`, do not assume the provider is down. First consider that the chat-delivered key may have been redacted or truncated before it reached the agent.
5. In that case, tell the user to write the key locally themselves (or provide it through a trusted non-redacted path) and then re-run the verification command.

Why this matters:
- The skill-local `.env` path is correct for AnySearch.
- The failure mode is often the chat transport or redaction layer, not the AnySearch runtime itself.

Recommended user-facing fallback:
```bash
printf 'ANYSEARCH_API_KEY=<full_key>\n' > <skill_dir>/.env
python <skill_dir>/scripts/anysearch_cli.py search "test query" --max_results 2
```
