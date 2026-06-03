# OCR/PDF-derived academic markdown cleanup

Use this when the user asks to revise a large Markdown file that was extracted from a PDF, scan, or OCR workflow rather than to rewrite the academic content from scratch.

## Typical noise to remove first
- PDF filename / timestamp banners
- CMYK print marks (`C`, `M`, `Y`, `K`, `CMY`)
- publisher contact / pricing / website blocks carried over from cover pages
- repeated cover / title / back-cover matter
- form-feed page markers and running headers / footers
- stray page numbers or roman numerals embedded between paragraphs

## Recommended workflow
1. Preserve the original file.
   - Save the cleaned result as a new Markdown file unless the user explicitly wants overwrite.
2. Clean extraction noise before doing language polish.
   - Remove obvious publication / printing artifacts first; otherwise later paragraph cleanup will propagate junk into the body.
3. Rebuild document structure.
   - Normalize chapter / section / subsection headings into consistent Markdown levels.
   - Add front-matter headings when needed (e.g. 内容简介, 前言, 目录).
4. Merge broken paragraph wraps carefully.
   - Join lines that were split by layout extraction, but do not blindly merge tables, formulas, references, figure captions, sequence blocks, or enumerations.
5. Scope pattern replacements narrowly.
   - Front-matter formatting passes (for example converting name lists to bullets) must be restricted to the intended section only.
   - Global regex replacements can silently corrupt later body text.
6. Verify with a search-after-edit pass.
   - Re-check for residual markers such as PDF filenames, CMYK tokens, publisher websites, running headers, duplicated wording, and malformed headings.

## Common pitfall
- An over-broad cleanup regex can introduce new errors far from the target area (for example duplicating a term like `团队团队` or turning ordinary prose into list items). After any structural regex pass, run a targeted residual-pattern review and spot-check downstream sections.

## Output target
- Prefer a readable, structurally clean Markdown artifact.
- If OCR loss remains in tables / formulas / figure-heavy zones, say so explicitly rather than pretending the text is fully restored.
