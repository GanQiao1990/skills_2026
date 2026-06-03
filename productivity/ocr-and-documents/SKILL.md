---
name: ocr-and-documents
description: "Extract text from PDFs/scans (pymupdf, marker-pdf)."
version: 2.3.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Research, Arxiv, Text-Extraction, OCR]
    related_skills: [powerpoint]
---

# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf (high-quality OCR)

```bash
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Vertical CJK scanned books (Chinese/Japanese, old prints, two-page spreads)

When the PDF is a scanned book with **vertical columns**, margin commentary, or a **two-page spread**:

1. First verify it is image-based by sampling with a lightweight extractor (`pdfplumber`/`pymupdf`). If sampled pages return empty text, switch to OCR immediately.
2. Render pages to images with `pdf2image` / `pdftoppm`.
3. For two-page spreads, OCR the **right half first, then the left half**.
4. Crop away outer borders, watermark zones, and some gutter area before OCR.
5. Use Tesseract with vertical language packs first:
   - Traditional: `chi_tra_vert`
   - Simplified: `chi_sim_vert`
   - Fallback: combine vertical + horizontal packs if output is too sparse, e.g. `chi_tra_vert+chi_tra`
6. Save output incrementally to Markdown and maintain a small state file so long OCR runs can resume after interruption.
7. Warn the user that old prints / annotations / bleed-through / center gutters will create OCR errors; this is expected, not a sign the pipeline failed.

Support script: `scripts/resumable_vertical_cjk_ocr.py` — resumable OCR to Markdown for scanned vertical CJK PDFs.

## Ancient / Vertical CJK Scans (critical OCR ordering pitfall)

For classical Chinese / Japanese / Korean scans, especially **two-page spreads with vertical columns, borders, marginal commentary, or center gutters**, plain OCR text output is often in the wrong reading order even when character recognition is acceptable.

When the user cares about readable output order, do **not** trust raw `image_to_string()` output alone. Add layout-order logic:

1. Render each PDF page to an image.
2. Detect or manually split the spread into logical reading regions (often left half / right half, but confirm the document's convention).
3. Crop away page borders, gutter, watermarks, and noisy margins before OCR.
4. Run OCR with vertical Chinese/Japanese models when appropriate (`chi_tra_vert`, `chi_sim_vert`, etc.).
5. Use bounding-box output (`pytesseract.image_to_data`) to recover token positions.
6. Reconstruct text in the document's intended reading order by grouping tokens into columns, then sorting columns and tokens explicitly.
7. Save to Markdown with the ordering assumption documented at the top.

Important: **ask or infer the reading order from the document tradition**. Do not assume all vertical CJK works are right-to-left. Some user workflows require **left-to-right across columns/pages, then top-to-bottom within each column**.

For long scanned books, prefer a resumable script that:
- appends page-by-page output to `.md`
- writes a simple state file with the next page number
- runs as a background job if extraction will take a long time

See `references/vertical-cjk-ocr-ordering.md` for a compact implementation note.

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
