# PubMed E-utilities: Direct API Approach

When `scripts/pubmed_api.py` dependencies (science_skills_common) are unavailable, use NCBI E-utilities directly via `requests`.

## Core Endpoints

```
esearch.fcgi  → search and get PMIDs
efetch.fcgi   → fetch full records by PMIDs
```

Base URL: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils`

## Author Search Pattern

PubMed uses **Last First** author format, not "First Last".

```python
# Correct
query = '"Liu Liming"[Author]'
# Wrong — returns different person
query = '"Liming Liu"[Author]'
```

### Affiliation Disambiguation

Common names need affiliation filter to avoid wrong authors:

```python
query = '"Liu Liming"[Author] AND "Jiangnan University"[Affiliation]'
```

## Fetch All Papers (not just top N)

```python
# 1. esearch to get total count and PMIDs
pmids, total = esearch(term, retmax=total_count_from_first_search)

# 2. efetch in batches of 50 (NCBI limit per request)
for i in range(0, len(pmids), 50):
    batch = pmids[i:i+50]
    fetch_abstracts(batch)
    time.sleep(0.35)  # rate limit: 3 req/s without API key
```

## Rate Limits

- Without API key: 3 requests/second
- With `NCBI_API_KEY`: 10 requests/second
- Recommended delay: 0.35s between requests

## XML Parsing Notes

- `efetch` with `rettype=abstract` returns `PubmedArticle` XML
- Abstract sections may have `Label` attributes (e.g., "BACKGROUND", "RESULTS")
- Year can be in `<Year>` or `<MedlineDate>` (take first 4 chars)
- DOI is in `<ArticleId IdType="doi">`

## CSV Export Pattern

Columns: author, pmid, title, authors (semicolon-separated), journal, year, abstract, doi, keywords, link

Use `utf-8-sig` encoding for Excel compatibility with Chinese text.
Use `csv.QUOTE_ALL` quoting.
