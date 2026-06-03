# Static index.html maintenance for article/portal directories

Use this when a user says a new web page was added and asks to adjust an existing `index.html`.

## Goal
Update the existing portal/index page with the new entry instead of rebuilding the site.

## Procedure
1. Read the target `index.html` and locate the source of truth for entries:
   - JS array/object literals
   - hard-coded card lists
   - server-generated fragments checked into the file
2. Enumerate top-level `*.html` files in the same directory.
3. Compare filesystem files with files already referenced by the index.
4. Treat backup/scratch files as excluded by default:
   - `*_bak.html`
   - `*bak*.html`
   - similarly obvious temporary variants
5. Patch only the missing real page entries.
6. Preserve local naming conventions already used by the file:
   - title format
   - category labels
   - icon style
   - tags
7. Verify after editing:
   - the new file appears in `index.html`
   - no non-backup top-level HTML files remain unindexed

## Practical note
If the directory contains versioned files like `V5`, `V6`, `V7`, prefer adding the newest real version and leaving backup files unlisted unless the user requests otherwise.
