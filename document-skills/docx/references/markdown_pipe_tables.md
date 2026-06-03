# Markdown pipe tables in DOCX conversion

Session note: When converting a Markdown manuscript to .docx, literal pipe-table blocks (`| a | b |`) should be parsed into real Word tables, not left as paragraphs. This avoids broken manuscript tables in the submission-ready DOCX.

## Practical rules
- Detect a table when a header row beginning with `|` is followed by a separator row containing dashes and optional colons.
- Convert the header + body into a `docx` table with grid styling.
- Normalize inline Markdown in table cells (`**bold**`, `*italic*`, code ticks) before writing cells.
- Keep table font slightly smaller than body text when the manuscript has wide tables.
- Verify the result by checking `len(doc.tables)` and ensuring no paragraph still begins with `|`.

## Common failure mode
- A Markdown-to-DOCX converter that only handles paragraphs/images/headings will render tables as literal text blocks. This is especially common in manuscript generators that treat Markdown as a lightweight markup layer rather than a structured document model.

## Verification recipe
- Open the generated DOCX and confirm the number of real tables is non-zero.
- Search the paragraph text for leading pipe characters; there should be none if tables were parsed correctly.
- Inspect the first row of each Word table to make sure the header survived as column text.