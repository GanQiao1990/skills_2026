# Resumable vertical CJK OCR to Markdown

Use this pattern for scanned Chinese/Japanese book PDFs that are image-only, vertically typeset, and may contain two-page spreads or marginal notes.

Key points from this session:
- `pdfplumber` sampling returned empty text on sampled pages, confirming the PDF was image-based.
- Tesseract had useful vertical packs available (`chi_tra_vert`, `chi_sim_vert`).
- A rendered sample page showed a two-page spread with right-to-left page order, vertical columns, outer borders, marginal commentary, and a center gutter.
- Best practical baseline in this environment: render one page at a time with `pdf2image`, split into right/left halves, crop borders, OCR with `chi_tra_vert`, and append results incrementally to Markdown.
- For long runs, maintain a companion state file that stores the next page number, so interruption only loses the current page.

Recommended output shape:
- Header with source path + OCR caveat
- `## 第 N 页`
- `### 右半页`
- `### 左半页`

Typical OCR caveat to include:
- Old printed books with annotations, bleed-through, uneven paper tone, and gutter distortion will contain OCR errors in characters and order.

Suggested fallback logic:
- Primary: `chi_tra_vert` or `chi_sim_vert`
- If output is suspiciously short, retry same crop with `chi_tra_vert+chi_tra` or `chi_sim_vert+chi_sim`
