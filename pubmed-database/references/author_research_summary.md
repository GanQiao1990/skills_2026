# Author Research Summary Pattern

Batch-fetching publications for one or more researchers and generating a structured summary report.

## When to Use
- User asks "summarize X's work" or "what has researcher Y published on topic Z"
- Comparing research output across multiple authors
- Building background literature profiles for grant proposals

## Key Steps

1. **Determine correct PubMed author name format**: LastName ForeName (e.g., "Liu Liming" not "Liming Liu")
2. **Check for name ambiguity**: Search without affiliation first, check count. If suspiciously high or includes unrelated fields, add affiliation filter.
3. **Construct query**: `"<LastName> <ForeName>"[Author]` optionally AND `"<Affiliation>"[Affiliation]` AND extra terms
4. **Fetch in batches**: esearch for PMIDs, then efetch in batches of 50 for abstracts
5. **Rate limit**: 0.35s between requests without API key, 0.1s with key

## Author Name Disambiguation Strategy

| Scenario | Risk | Mitigation |
|---|---|---|
| Common name (Liu, Wang, Zhang) | Multiple researchers share name | Add `[Affiliation]` filter |
| Single famous researcher (Lee Sang Yup) | Low ambiguity | Name-only query usually sufficient |
| Name matches unrelated field | Wrong person entirely | Verify first few results' journals/abstracts |

## Query Construction Examples

```
# Lee Sang Yup — KAIST, metabolic engineering
"Lee Sang Yup"[Author]

# Liu Liming — Jiangnan University, metabolic engineering
"Liu Liming"[Author] AND "Jiangnan University"[Affiliation]

# With topic filter
"Liu Liming"[Author] AND "Jiangnan University"[Affiliation] AND "amino acid"[Title/Abstract]
```

## Output Structure

The summary report should include:
1. Total paper count, year distribution
2. Top journals, top keywords (from MeSH/author keywords)
3. Paper list with: title, authors, journal, year, abstract excerpt, DOI, PMID link
4. Cross-author theme analysis (keyword overlap, complementary strengths)

## Standalone Script

A reusable script is available at the project level: `pubmed_author_summary.py`
It handles esearch/efetch, XML parsing, affiliation filtering, and markdown report generation.

Usage:
```bash
python pubmed_author_summary.py --authors "Lee Sang Yup" "Liu Liming" --max-results 50
python pubmed_author_summary.py --authors "Smith John" --query "metabolic engineering"
python pubmed_author_summary.py --json raw_data.json   # also export JSON
```

## XML Parsing Notes

- Abstract text is in `AbstractText` elements, may have `Label` attributes for structured abstracts
- Year can be in `PubDate/Year` or `PubDate/MedlineDate` (take first 4 chars)
- DOI is in `ArticleIdList/ArticleId[@IdType="doi"]`
- Keywords are in `KeywordList/Keyword` elements
- Author affiliations: `Author/AuthorList/Author/AffiliationInfo/Affiliation`
