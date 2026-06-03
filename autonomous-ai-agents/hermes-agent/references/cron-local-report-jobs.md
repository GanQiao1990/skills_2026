# Cron pattern: local literature/report jobs that write files in a project

Use this pattern when the user asks for a recurring check like “monitor daily updates”, “track papers”, or “write a paper list into ./some_dir”.

## Durable rules

- Keep the editable project script inside the project repo/workdir.
- Copy the runnable cron copy into `~/.hermes/scripts/`.
- Create the cron job with:
  - `no_agent=true`
  - `script='<relative filename under ~/.hermes/scripts>'`
  - `workdir='/absolute/project/path'`
- Let the script write artifacts relative to `workdir` (for example `./de_novo.design/...`).
- Maintain a local state file in the project so repeat runs can report only newly seen items.
- For file-generation jobs, `deliver` will usually resolve to `local`; the durable result is the written file, not a chat message.
- Have the script print a short status summary to stdout so manual runs and scheduler logs are inspectable.

## Good file layout

Inside the project/workdir, prefer:

- `<target_dir>/<project>_daily_updater.py` — editable project script
- `<target_dir>/.<project>_state.json` — seen IDs / run history
- `<target_dir>/<project>_paper_list.md` or `<target_dir>/<project>_digest.md` — rolling index
- `<target_dir>/daily_reports/YYYY-MM-DD_<project>.md` — per-run report

## Literature-monitoring example

Common flow:

1. Pick a stable source with structured IDs (for example PubMed E-utilities or a journal RSS feed).
2. Query the newest items.
3. Normalize stable IDs (PMID, DOI, article URL, etc.).
4. Compare against the local state file.
5. Write a daily markdown report plus a rolling index.
6. Print a concise run summary.
7. Copy the script into `~/.hermes/scripts/` and create the cron job.

## Pitfall

If you pass an absolute path like `/path/to/script.py` to the cron `script` field, Hermes rejects it. The `script` field must be relative to `~/.hermes/scripts/`.

## Example job shape

- Script in repo: `/project/de_novo.design/de_novo_protein_design_daily_updater.py`
- Runnable copy: `~/.hermes/scripts/de_novo_protein_design_daily_updater.py`
- Cron config:
  - `script='de_novo_protein_design_daily_updater.py'`
  - `no_agent=true`
  - `workdir='/project'`
  - schedule like `0 9 * * *`

This keeps the job reproducible while still writing outputs into the project tree.
