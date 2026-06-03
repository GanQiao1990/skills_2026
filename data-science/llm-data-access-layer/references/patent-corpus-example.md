# 92 GB Chinese Patent Corpus – Concrete Implementation Notes

## Source
- Raw file: `中国专利数据库.csv` (92 GB, 51.1 M rows, 35 columns, UTF-8, 1985–2025)
- Columns include: 专利名称, 申请号, 申请日, IPC主分类号, 摘要文本, 主权项内容, 申请人, 发明人, etc.

## Compression achieved (2026-05)
- Parquet (ZSTD, year-partitioned): 14 GB total, 125 partitions (year=1985 … year=2025)
- SQLite lean + LIKE fallback: 18 GB (FTS5 virtual table was empty on this corpus)
- TSV year shards (for future RAG): still present under `中国专利数据库_llm_retrieval/by_year/`

## Working schema mapping (raw → LLM-friendly)
| Raw column          | LLM alias          | Notes |
|---------------------|--------------------|-------|
| app_no              | 申请号             | Primary key |
| title               | 专利名称           | - |
| application_year    | 申请年份           | Integer, good partition key |
| ipc_main            | IPC主分类号        | Use starts_with for C12/C07 etc. |
| applicant           | 申请人             | - |
| inventors           | 发明人             | - |
| abstract / 摘要文本 | 摘要精简           | Truncate to 600–800 chars |
| claims / 主权项     | 主权项精简         | Truncate to 400–600 chars |

## Critical lesson learned
FTS5 virtual table (`patents_fts`) contained only title/applicant/ipc_main and returned NULL for most rows.  
Solution: fall back to main `patents` table + `LIKE '%keyword%'` on title/applicant. This pattern should be documented as the default when FTS5 data quality is unknown.

## Recommended helper usage
```python
from patent_llm_helper import PatentLLMHelper
h = PatentLLMHelper()
hits = h.fts_search("NarL 硝酸盐", limit=20)
ctx  = h.prepare_for_llm(hits)
df   = h.parquet_filter(year=2020, ipc_prefix="C12", limit=100)
```

## Files produced in this session
- `patent_llm_helper.py` – reusable class (CLI + import)
- `patent_api.py` – FastAPI backend (port 8001)
- `patent_frontend.html` – minimal Tailwind frontend

## Future extension points
- Add dense vector index on (title + 摘要精简) using sentence-transformers or voyage.
- Mount the FastAPI router under a larger agent gateway.
