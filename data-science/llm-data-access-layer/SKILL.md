---
name: llm-data-access-layer
description: |
  Build production-grade, LLM-ready access layers for massive structured corpora 
  (patents, literature, clinical data, etc.). Converts raw multi-GB/GB-scale 
  tabular or semi-structured data into a hybrid retrieval + analytical stack 
  (Parquet columnar + SQLite FTS5 + optional vector) with first-class support 
  for LLM context preparation, FastAPI backends, and minimal frontends.
---

# LLM Data Access Layer

## When to use this skill
- User has a large CSV/TSV/JSONL corpus (>10 GB) that needs to be made queryable and LLM-friendly.
- Requirements include fast keyword retrieval + columnar analytics + direct generation of LLM context strings.
- Need a reusable helper class + optional FastAPI backend + simple HTML/JS frontend.

## Core Pattern (class-level)
1. **Ingestion & Compression**
   - Convert raw CSV → year-partitioned Parquet (ZSTD) for analytics.
   - Create lean SQLite + FTS5 (or LIKE fallback) for millisecond keyword search.
2. **Helper Class Design**
   - `LLMDataHelper` with methods: `fts_search()`, `parquet_filter()`, `prepare_for_llm()`.
   - Always return LLM-optimized context strings (title + key fields + truncated abstract/claims).
3. **Stacking Layers**
   - CLI helper (importable) → FastAPI backend → minimal frontend.
   - Keep schema mapping explicit (raw column names → LLM-friendly aliases).

## Critical Implementation Rules
- Never rely on FTS5 virtual table data if it is empty or incomplete; fall back to main table + LIKE or parameterized queries.
- Always expose a `prepare_for_llm()` or `search_and_prepare()` method that returns a single string ready to paste into an LLM prompt.
- Partition Parquet by a high-cardinality time or category field (year, IPC, etc.).
- Keep the helper class under 200 lines; move heavy lifting to Polars lazy evaluation.

## Pitfalls to avoid
- Assuming FTS5 virtual table will have all columns populated — verify with PRAGMA table_info.
- Returning raw DataFrame rows to LLM without truncation and formatting.
- Hard-coding port 8000 when multiple services may be running.

## References
- `references/patent-corpus-example.md` — concrete 92 GB Chinese patent database case (Parquet 14 GB + SQLite 18 GB).
- `references/schema-mapping-pattern.md` — how to map 35-column patent schema to LLM-friendly fields.

## Next evolution
- Add vector (dense) retrieval on top of the existing Parquet + FTS5 base.
- Provide a reusable FastAPI router that can be mounted into larger agents.
