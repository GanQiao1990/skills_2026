# Local PDF paper discussion and bilingual notes workflow

Use this pattern when the user provides a local paper PDF path and asks to discuss, summarize, or translate notes derived from it.

## When to use
- A user points to a local PDF and wants a collaborative discussion of the paper.
- The task is not just raw extraction; it needs structured reading notes.
- The user later asks for a Chinese version of previously written English notes.

## Recommended workflow
1. Verify the PDF exists and extract lightweight metadata first.
   - Prefer `pdfinfo <file>` for title, DOI/subject, page count, and preview status.
   - Confirm the file path before doing heavier extraction.
2. Extract text with a robust local parser.
   - `pypdf` is usually enough for article-level text extraction.
   - Use keyword/section searches to find Summary, Introduction, Discussion, Conclusion, and case-study terms.
3. Build an interpretation layer, not just a summary.
   - Capture: core claim, technical contributions, workflow/architecture, evidence, validations, limitations, and discussion questions.
   - For AI-for-science papers, explicitly separate what the paper claims from what the evidence actually supports.
4. Save the deliverable as markdown adjacent to the PDF.
   - Recommended naming: `<source-stem>_notes.md`.
   - Keep the note self-contained: source path, metadata, summary, critical reading, and suggested discussion angles.
5. If the user asks for a Chinese version of the notes:
   - Preserve the original section structure as much as possible for side-by-side comparison.
   - Adapt into concise, professional Chinese markdown rather than literal line-by-line translation.
   - Save as `<source-stem>_notes_zh.md` alongside the English file.
6. Verify by reading back the saved file after writing.

## Content checklist for paper discussion notes
- Basic metadata
- One-paragraph core summary
- Claimed technical contributions
- How the system/method works
- Main evidence presented
- Why the paper is interesting
- Limitations and critical points
- Good follow-up discussion questions
- Provisional judgment / take-home view

## Pitfalls
- Do not stop at extraction-only output when the user asked to discuss the paper.
- Do not overstate validation strength; distinguish in vitro or proof-of-concept evidence from clinical or broad scientific validation.
- Do not translate discussion notes too literally into Chinese if that hurts readability; preserve logic and structure, but optimize expression.
- When writing the Chinese version, prefer a polished standalone Chinese markdown artifact rather than inline chat-only translation.
