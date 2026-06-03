# Final submission bundle and archive demotion pattern

Use this pattern when a repository already contains a workable publication package but still has legacy root-level drafts that can confuse future sessions or lead the user to upload the wrong file.

## Trigger conditions
- The user wants a "投稿版本" / final submission version rather than another exploratory draft.
- A package-local canonical manuscript already exists or is being created.
- Root-level reports still look manuscript-like and compete with the package-local canonical draft.
- The project mixes experimental anchors, mechanistic simulations, and calibrated search/autoresearch layers.

## What to do
1. Create or confirm a package-local directory such as `publication_package/`.
2. Lock a **single canonical manuscript starting point** inside that package.
3. Create submission assets, at minimum:
   - `TITLE_PAGE_DRAFT.md`
   - `FIGURE_LEGENDS.md`
   - `COVER_LETTER_DRAFT.md`
   - `README_SUBMISSION_PACKAGE.md`
4. Create package-navigation and reviewer-facing control files:
   - `SUBMISSION_MANIFEST.md`
   - `FINAL_SUBMISSION_CHECKLIST.md`
   - `JOURNAL_PACKAGE_MAP.md`
   - `EVIDENCE_MAP.md`
5. Explicitly label root-level legacy manuscript-like files as archive/supporting material. If needed, rewrite a confusing legacy report into an **archive note** that points readers to the canonical package instead of competing with it.
6. In the package docs, state which files are canonical and which must **not** be uploaded as the main manuscript.
7. If the package is being tightened toward a default venue voice without an explicitly confirmed journal, record that assumption in the package docs and DEBUG log (for example: "Metabolic Engineering-style submission bundle").

## Why this matters
Without archive demotion, future sessions will often re-open an older root-level report and accidentally resurrect stale numbers or upload the wrong manuscript. A final-submission bundle should behave like a handoff package, not like a pile of plausible drafts.

## Minimum canonical bundle shape
- `MANUSCRIPT_FINAL_<venue-or-style>.md` or equivalent single canonical manuscript
- `TITLE_PAGE_DRAFT.md`
- `FIGURE_LEGENDS.md`
- `COVER_LETTER_DRAFT.md`
- `README_SUBMISSION_PACKAGE.md`
- `SUBMISSION_MANIFEST.md`
- `FINAL_SUBMISSION_CHECKLIST.md`
- `JOURNAL_PACKAGE_MAP.md`
- `EVIDENCE_MAP.md`
- `canonical_data/`
- `figures/`

## Pitfalls
- Leaving both a package-local manuscript and a root-level manuscript-like report unlabeled; future users will treat them as equal.
- Saying a file is "legacy" only in chat rather than inside the file or package docs.
- Treating a calibrated/autoresearch report as the main manuscript when the audited paper has already moved to a stricter evidence-boundary package.
- Forgetting to say which file is the **single canonical starting point**.

## Verification
- Search the package and confirm there is exactly one clearly named canonical manuscript entry point.
- Re-open README/INDEX and make sure they point first to that manuscript.
- Re-open any demoted root-level report and confirm it now identifies itself as archival/supporting rather than canonical.
- Ensure the final-submission checklist explicitly warns against uploading legacy drafts as the manuscript file.
