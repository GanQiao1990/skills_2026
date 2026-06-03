---
name: patent-data-llm-layer
category: data-science
tags: [patent, llm, retrieval, parquet, sqlite, fastapi, large-corpus]
description: Build LLM-ready retrieval and interaction layers on top of massive structured patent/scientific databases (50M+ records). Covers CSV→Parquet compression, SQLite+FTS5 sparse retrieval, FastAPI backend, minimal frontend, and context preparation for LLMs.
---

# Patent Data LLM Layer

## When to use
- You have a very large CSV/JSON scientific or patent corpus (tens of millions of rows).
- You need both **fast keyword retrieval** and **analytical filtering** before feeding data to an LLM.
- You want a reusable pattern that produces a clean API + simple frontend for human-in-the-loop exploration.

## Core Architecture (proven in 51M patent corpus)

1. **Ingestion & Compression**
   - Original: 92 GB CSV
   - Year-partitioned TSV shards (for incremental processing)
   - Parquet layer (ZSTD, ~14 GB) — columnar, excellent for filtering/aggregation
   - SQLite lean DB with FTS5 (or fallback LIKE on main table when FTS virtual table is incomplete)

2. **Dual Retrieval Strategy**
   - Sparse retrieval: SQLite `patents_fts` or main table `LIKE` for fast candidate recall
   - Analytical layer: Polars `scan_parquet` with year / IPC / applicant filters
   - LLM context preparation: deterministic formatting of title + abstract + main claim + metadata

3. **Backend + Frontend**
   - FastAPI exposing `/search`, `/filter`, `/prepare_llm`
   - Minimal Tailwind HTML frontend that calls the API and renders LLM-ready context with one-click copy

## Recommended Schema (LLM-friendly columns)
- 申请号, 专利名称, 申请年份, IPC主分类号, 申请人, 发明人, 摘要精简, 主权项精简

## Pitfalls & Lessons
- FTS5 virtual tables can be empty or incomplete after bulk import — always implement a graceful fallback to main-table LIKE search.
- Port conflicts are common when multiple uvicorn processes run; default to 8001 or make port configurable.
- Frontend must point to the actual running backend port (hardcode or env var).
- For 50M+ rows, always use lazy Polars scans and LIMIT early.
- Natural-language patent questions often underperform as direct retrieval queries. Add a query-reformulation step for evaluation and production, and keep the evaluation set in retrieval-friendly keyword form alongside any natural-language UI prompts.
- For question answering over patents, document-level hits are often too coarse. Split title / abstract / main-claim into chunk-level evidence units, score chunks separately, then let patent ranking inherit evidence scores.
- A practical “multimodal-document-graph style” adaptation for patents is lightweight graph linking rather than a full knowledge graph: connect adjacent chunks within a field and connect title chunks to abstract/claim entry chunks, then add a small graph bonus when neighboring chunks also match the query.
- Grounded patent summaries improve when the prompt requires a fixed citation schema using only retrieved evidence handles (for example `[证据: 专利号 | chunk_id | 字段]`) and explicitly forbids unstated background expansion.
- Retrieval upgrades should ship with a side-by-side evaluator (`old_top_ids`, `new_top_ids`, overlap, new-only IDs, top evidence chunks) so ranking changes are inspectable instead of purely anecdotal.

## Files in this skill
- `references/patent-llm-layer-architecture.md` — detailed notes from the 51M Chinese patent corpus implementation
- `references/patent-evidence-graph-retrieval.md` — chunk-level evidence retrieval, lightweight graph linking, grounded citation prompts, and evaluation patterns for patent QA/reporting
- `templates/patent_llm_helper.py` — core helper class (FTS5 + Parquet + context prep)
- `templates/patent_api.py` — FastAPI backend
- `templates/patent_frontend.html` — minimal interactive frontend

## Usage example
```python
from patent_llm_helper import PatentLLMHelper
helper = PatentLLMHelper()
hits = helper.fts_search("NarL 硝酸盐", limit=20)
context = helper.prepare_for_llm(hits)
df = helper.parquet_filter(year=2020, ipc_prefix="C12N")
```

This pattern generalizes to any large structured scientific dataset (papers, clinical trials, compound databases).