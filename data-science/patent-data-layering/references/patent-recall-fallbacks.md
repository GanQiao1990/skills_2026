# Patent recall fallbacks for evidence-heavy review tasks

Use this when a project already has layered patent data and you need to turn a curated candidate list into auditable evidence rows.

## Durable pattern from the amino-acid patent review workflow

Problem shape:
- Start from an existing candidate/example list (for example, a markdown table of patent application numbers)
- Need to enrich each row with real title/abstract/claim facts
- Need high recall on recent years without loading huge annual files into memory
- Need output suitable for expert tables, audit appendices, or project-review deliverables

## Recommended retrieval order

1. Use the curated candidate list as the source of truth for patent numbers.
2. Group application numbers by year from the `CNYYYY...` prefix.
3. Query the year shard directly under `中国专利数据库_llm_retrieval/by_year/patents_YYYY.tsv`.
4. For bulk enrichment, search the year TSV in small app-number batches rather than scanning the whole corpus into Python objects.
5. Parse the matched TSV line back into fields (`app_no`, `title`, `applicant`, `abstract`, `claim`).

## Why this fallback matters

In this repository shape, exact recall for application-number enrichment was more reliable from the year-sharded TSV retrieval layer than from direct `patent_metadata.sqlite` lookups during the same session.

Use this pattern especially when:
- the task is evidence-enrichment, not broad discovery
- the app numbers are already known
- you need recent-patent facts quickly
- SQLite exact-match lookup is slow, incomplete for your candidate list, or awkward to batch

## Batch pattern

- Group by year first.
- Search each `patents_YYYY.tsv` with a regex alternation of a small batch of app numbers.
- Keep batches modest (around 8-10 app numbers) to avoid giant regex payloads and to keep the match output manageable.
- Deduplicate application and grant rows after parsing.

## Output-shaping lesson

For domain summaries (for example, biosynthesis/patent review tables), store at least:
- patent number
- year
- title
- explicit engineering factor or process-control factor
- one short factual abstract/claim sentence
- inferred strategy
- inferred bottleneck/limiting factor

If the patent does not disclose a concrete gene edit, keep the row factual and label it as process-control / separation / fermentation-window logic rather than inventing a missing genetic design.

## Good fit

- patent audit tables
- expert summary tables
- recent-year evidence backfill
- converting a curated markdown list into a cited evidence appendix
