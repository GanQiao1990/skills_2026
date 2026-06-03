---
name: s2-api
description: Query papers with the Semantic Scholar Graph API using the S2_API_KEY stored in /home/qiao/dockerai/AI-Scientist-v2/.env. Use for paper queries, literature searches, citation lookups, DOI/arXiv/Semantic Scholar paper-id metadata retrieval, novelty checks, related-work gathering, and citation/background searches when the user asks to use S2, Semantic Scholar, or the s2-api skill.
---

# S2 API

Use Semantic Scholar/S2 first for paper queries. Load `S2_API_KEY` from `/home/qiao/dockerai/AI-Scientist-v2/.env`; never display the key.

## Quick start

Run the bundled script from anywhere:

```bash
python /root/.claude/skills/s2-api/scripts/s2_search.py search "protein hallucination de novo design" --limit 10
```

Fetch one paper by DOI/arXiv/S2 id:

```bash
python /root/.claude/skills/s2-api/scripts/s2_search.py paper "DOI:10.48550/arXiv.2504.08066"
python /root/.claude/skills/s2-api/scripts/s2_search.py paper "ARXIV:2504.08066"
python /root/.claude/skills/s2-api/scripts/s2_search.py paper "<SemanticScholarPaperId>"
```

The script prints JSON with paper metadata. Summarize results for the user; do not dump large JSON unless requested.

## Workflow

1. Translate the user’s paper query into 1-3 precise S2 search queries.
2. Use `scripts/s2_search.py search` for broad paper search or `paper` for DOI/arXiv/id lookup.
3. Rank papers by relevance first, then citation count/venue/year as secondary signals.
4. Report title, year, authors, venue, URL/DOI/arXiv id when available, citation count, and a concise relevance note.
5. If S2 fails, report the specific failure: missing `S2_API_KEY`, 401 invalid key, 429 rate limit, TLS/network timeout, or no results. Fall back to other paper-search skills only after noting S2 was unavailable or insufficient.

## Output style

For normal searches, use a compact table:

| Paper | Year | Venue | Why relevant |
|---|---:|---|---|

Then add 2-5 bullets synthesizing what the papers say.

For exact lookup, provide verified metadata and BibTeX-like citation fields if possible.

## Safety

- Do not print `.env` contents or `S2_API_KEY`.
- Do not commit `.env` or copied keys into skill files, logs, or outputs.
- Respect rate limits; avoid large loops. The script spaces requests and uses small limits by default.
