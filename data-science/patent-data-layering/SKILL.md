---
name: patent-data-layering
category: data-science
description: Systematic compression and multi-layer indexing of massive patent CSV databases (50M+ rows) into Parquet + SQLite/FTS5 structures optimized for LLM retrieval and analytics.
tags: [patent, large-scale-data, parquet, sqlite, llm-retrieval, compression]
version: 1.0
---

# Patent Data Layering for LLM Interaction

## Purpose
Systematic compression and multi-layer indexing of massive patent CSV databases (50M+ rows, 90+ GB) into efficient retrieval and analytical structures suitable for LLM-augmented workflows.

## Core Architecture
Dual-branch design matching the standard 9GB→high-performance parsing→(vector + structured) pattern:

1. **Columnar Analytical Layer (Parquet)**
   - Year-partitioned (`year=YYYY/data.parquet`)
   - ZSTD compression + statistics
   - Reduced schema focused on LLM-relevant fields (row_id, 申请号, 专利名称, 申请人, IPC主分类号, 摘要精简, 主权项精简, etc.)
   - Ideal for: batch filtering, year/IPC/applicant aggregations, DuckDB external scans, pre-LLM candidate selection

2. **Sparse Retrieval Layer (SQLite + FTS5)**
   - Lean metadata table (~18 GB for 51M rows)
   - patents_fts virtual table for full-text search on titles, applicants, abstracts
   - Fast candidate recall by patent number, applicant, or keyword before deeper analysis

3. **Source Shards (TSV by year)**
   - Intermediate year-sharded TSVs as bridge from raw CSV
   - Preserved for full-text or vector embedding pipelines

## When to Use
- User provides or references a large Chinese patent CSV (e.g. "中国专利数据库.csv")
- Task involves LLM interaction, semantic search, or statistical analysis over patent corpora
- Need both fast retrieval and analytical querying on the same dataset

## Recommended Workflow
1. Raw CSV → year-sharded TSV (if not already done)
2. TSV → Parquet (ZSTD) via Polars `sink_parquet`
3. Build/maintain SQLite lean metadata + FTS5
4. For LLM queries: SQLite FTS5 for candidate recall → Parquet for filtering/aggregation → optional full text or vector lookup

## Pitfalls & Constraints
- Raw CSV is UTF-8 but contains many nulls and mixed types — always use `ignore_errors=True` and explicit schema overrides
- Parquet year partitioning is mandatory for manageable file sizes on 50M+ row datasets
- Do not attempt to load entire CSV into pandas/memory
- DuckDB is preferred for SQL analytics on Parquet once installed; fall back to Polars otherwise

## Support Files
- `references/patent-layering-manifest-example.md` — example manifest structure from successful 51M-row build
- `references/column-schema-recommendations.md` — minimal vs full schema trade-offs for LLM use cases
- `references/patent-recall-fallbacks.md` — evidence-enrichment pattern for turning curated patent-number lists into auditable tables using year-sharded TSV recall

## Related Skills
- `exploratory-data-analysis`
- `scientific-data-pipeline` (when created)

## Notes for Future Sessions
This skill captures the durable pattern for patent-scale data, not any single execution. Update with new compression ratios, schema changes, or retrieval benchmarks as they are validated.
