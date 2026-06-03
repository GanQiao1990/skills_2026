# Semantic Scholar local export pipeline

Use this pattern when the user wants a repo-local paper export driven by `S2_API_KEY` rather than an abstract literature summary.

## When to use
- User asks to query Semantic Scholar papers by keyword and save a CSV/XLSX/JSON into a project directory
- User specifies exact output columns such as `title`, `abstract`, `paper time`, `doi`, or a paper URL/web link
- A small local script is safer than modifying an existing scraper with a different data source

## Minimal durable pattern
1. Read `S2_API_KEY` from `--api-key`, environment, or project `.env`.
2. Use `GET /graph/v1/paper/search`.
3. Request only needed fields, typically:
   - `title`
   - `abstract`
   - `publicationDate`
   - `year`
   - `url`
   - `externalIds`
4. For up to 300 papers, page with `offset=0,100,200` and `limit=100`.
5. Deduplicate by `paperId` when present; otherwise fall back to `(title, publicationDate, year)`.
6. Flatten to the exact requested CSV schema.

## Field mapping used in practice
When the user asks for a CSV with `title keyword abstract paper time doi weblinker`, map as follows:

- `title` -> `title`
- `keyword` -> the exact query string used for retrieval (Semantic Scholar search does not return a simple native keyword field here)
- `abstract` -> `abstract`
- `paper_time` -> `publicationDate`, falling back to `year`
- `doi` -> `externalIds.DOI`
- `weblinker` -> `url`

## Output contract
- Save the CSV in the user-requested project directory, not only under a generic output folder, if they explicitly asked for that path.
- Verify row count and header after writing.
- If the user asked for 300 papers, report the actual saved row count rather than assuming the query returned that many.

## Scope rule
If the repository already has a PubMed or other-source scraper, prefer adding a separate Semantic Scholar pipeline script instead of rewriting the existing workflow unless the user explicitly asks for integration.
