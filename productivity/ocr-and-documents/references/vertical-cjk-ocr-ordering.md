# Vertical CJK OCR ordering

Use this note when OCRing scanned classical Chinese / Japanese books with vertical columns.

Core lesson:
- Recognition quality and reading order are separate problems.
- `pytesseract.image_to_string()` may return tokens in an order that is unusable for reading, even when many characters are recognized correctly.
- For user-facing output, reconstruct order from bounding boxes.

Recommended pattern:
1. Render PDF page to image.
2. Split the spread into reading regions if needed.
3. Crop borders, gutter, stamps, and marginal noise.
4. OCR with `pytesseract.image_to_data(..., output_type=Output.DICT)`.
5. Build token records with x/y/w/h and confidence.
6. Group tokens into columns by x-center clustering.
7. Sort columns according to the document's reading convention.
8. Sort tokens top-to-bottom within each column.
9. Join tokens column-by-column into Markdown.

Practical heuristics:
- Estimate column clustering tolerance from median bounding-box width.
- Keep ordering logic explicit in the output header, e.g.:
  - spread order: left half then right half
  - per-half order: left-to-right by column
  - within-column order: top-to-bottom
- Use a resumable state file for long books.
- Save page-level headings in Markdown so later correction is easier.

Pitfall:
- Do not assume all vertical CJK texts are right-to-left across columns. Confirm with the user or infer from the specific edition/workflow.
