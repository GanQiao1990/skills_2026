# Cron literature watchers

Reusable pattern for recurring literature-monitoring jobs that write local artifacts into a project directory.

## When to use
- User wants a daily or recurring paper watcher
- Output should be written locally, not just sent as a chat message
- User wants variants like: paper list, digest, with abstracts, filtered subset, new subdirectory

## Durable workflow
1. Identify a structured source first
   - PubMed E-utilities for biomedical literature
   - RSS feeds for publisher/journal update streams
2. Write assumptions and evidence into `DEBUG.md` before execution if the environment requires that convention.
3. Keep the project-editable script in the repo/workdir.
4. For Hermes cron `no_agent=true`, copy the runnable script into `~/.hermes/scripts/` and reference only the relative filename in the cron job.
5. Use `workdir` to point at the project root so the script writes local files in the right place.
6. Write three durable artifacts under the requested output directory:
   - state file for deduplication
   - rolling index file
   - date-stamped daily report(s)
7. Run the script once immediately and verify the generated files before creating or replacing the cron job.
8. If the user asked for a replacement of an existing watcher:
   - list jobs first to get the exact old `job_id`
   - create and verify the replacement watcher first
   - remove the old cron job only after the new one is confirmed working
   - do not assume removing the cron job implies deleting old local files unless the user explicitly asks for cleanup

## Output contract patterns
- Digest: concise note per item
- Paper list: title/link/DOI oriented list
- With abstracts: include abstract or source-specific fallback summary text

## Source-specific abstract fallback rules
### PubMed
Preferred stack:
1. `esearch` for PMIDs
2. `esummary` for metadata and IDs
3. `efetch` with `retmode=xml&rettype=abstract` for actual abstract text

Implementation note:
- XML `<AbstractText>` can appear multiple times with `Label` attributes; concatenate them in order.
- Some records have no abstract; use `No abstract found.` rather than failing the whole run.

### Nature / publisher RSS + article pages
Preferred stack:
1. Journal RSS for current item discovery
2. Article page extraction for public teaser/editorial-summary text
3. RSS encoded content as fallback if no clean teaser/summary block is present

Implementation note:
- For Nature Biotechnology highlight/news-style pages, a standard abstract block may be absent even when useful summary text exists.
- A practical fallback is `div.article__teaser` or similar summary containers before falling back to RSS text.

## Naming guidance
- New output contract/path => new cron job name unless the user explicitly asks to replace the old one
- Good names are class-level and descriptive, e.g.:
  - `nature-biotechnology-abstract-daily`
  - `de-novo-protein-design-abstract-daily`

## Verification checklist
- Script runs successfully from the project workdir
- State file exists and updates
- Index file exists and appends correctly
- Daily report exists in the expected directory
- Cron job points at the correct relative script path under `~/.hermes/scripts/`
- Old cron removed only if replacement requested and verified
