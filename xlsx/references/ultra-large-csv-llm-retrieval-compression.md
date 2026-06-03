# Ultra-large CSV -> LLM retrieval compression

Use this pattern when a spreadsheet-shaped dataset is too large to load comfortably into an LLM context or into ordinary interactive analysis (for example tens of GB, tens of millions of rows, or very long text columns).

## Goal

Do not overwrite the source file. Create a lossy, retrieval-oriented derivative that is much easier to search, shard, and feed into downstream LLM workflows.

## Recommended workflow

1. Preserve the original file unchanged.
2. Inspect schema first: row count, column count, text-heavy fields, obvious identifiers.
3. Keep only retrieval-critical columns, typically:
   - stable row id / source line id
   - primary identifier (e.g. application number)
   - title
   - type/category
   - applicant / inventor
   - year
   - one classification field (e.g. IPC main class)
   - shortened abstract / claim text
4. Truncate long text fields aggressively for first-pass retrieval.
   - Abstract: around 150-300 chars
   - Claims: around 80-150 chars
5. Shard by a natural partition key so each file is LLM-loadable.
   - For patent data, year is a strong default.
6. Emit plain-text TSV/CSV shards instead of XLSX for easier grep/search/LLM ingestion.
7. Write a manifest.json containing:
   - source path
   - source columns
   - retained columns
   - shard paths
   - row counts per shard
   - text truncation policy
8. Keep a README with usage instructions for future agents/users.

## Practical defaults for patent corpora

Retain columns like:
- row_id
- line_no
- 申请号
- 专利名称
- 专利类型
- 申请人
- 申请人类型
- 申请年份
- 公开公告号
- 公开公告年份
- IPC主分类号
- 发明人
- 摘要精简
- 主权项精简

## Why this works

This keeps enough information for first-pass topic retrieval, applicant/inventor filtering, IPC filtering, and year-scoped search, while avoiding the cost of loading full addresses, ownership metadata, and multi-kilobyte legal text into every query.

## Important caveat

A raw newline count can overestimate row count for CSV files with embedded newlines in quoted text. Use a CSV parser for the real record count.

## When the user says "excel表达"

If the source is already CSV, interpret this as tabular/spreadsheet representation unless they explicitly ask for .xlsx output. The safer default is retrieval-friendly derived text artifacts, not conversion back to Excel.
