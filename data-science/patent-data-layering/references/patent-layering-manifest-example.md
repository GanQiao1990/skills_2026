# Example Manifest from 51M-row Chinese Patent Build (2026-05)

## Build Summary
- Source: 92 GB raw CSV (51,122,488 rows, 1985–2025)
- Intermediate: year-sharded TSVs under `中国专利数据库_llm_retrieval/by_year/`
- Output: 14 GB Parquet layer (`中国专利数据库_parquet/year=*/data.parquet`)
- Compression ratio: ~85% (92 GB → 14 GB)
- Per-year example (2020): 5.39M rows, ~546 MB Parquet file

## Key Schema Fields Used (LLM-optimized)
row_id, line_no, 申请号, 专利名称, 专利类型, 申请人, 申请人类型, 申请年份, 公开公告号, IPC主分类号, 发明人, 摘要精简, 主权项精简

## Performance Notes
- Polars `scan_csv` + `sink_parquet` with ZSTD was stable and memory-efficient
- Year partitioning essential; single-file Parquet would be too large for practical use
- SQLite lean metadata (18 GB) + FTS5 provides fast candidate recall before Parquet analytics

## Recommended Next Steps for LLM Use
1. SQLite FTS5 for keyword/applicant/patent-number lookup
2. Parquet for year/IPC range filters and aggregations
3. Feed filtered row_ids back to TSV or original CSV for full text when needed

This manifest was generated from a successful full run on the 92 GB dataset.
