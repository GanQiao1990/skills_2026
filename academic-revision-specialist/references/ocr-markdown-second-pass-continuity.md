# OCR markdown second-pass continuity review

Use this after an initial OCR/PDF cleanup pass when the user says some sentences are still wrong, paragraph connections are awkward, or the document is readable but not yet trustworthy.

## Goal
Shift from broad structural cleanup to seam-by-seam continuity repair without re-corrupting the file.

## When to trigger
- The user says "still wrong", "请仔细核验", "段落之间连接不顺", or similar.
- The first-pass file is mostly clean, but residual issues remain at paragraph boundaries.
- Global regex cleanup already happened once; another broad pass would risk introducing new damage.

## Recommended workflow
1. Back up the current revised file before in-place editing.
2. Inspect seam types that commonly break after OCR cleanup:
   - heading -> first body paragraph
   - figure/table caption -> following body paragraph
   - footnote/legend -> resumed body paragraph
   - short orphan line -> continuation line
   - glossary/abbreviation line -> accidental merge with prose
3. Prefer bounded exact replacements over new global regex passes.
4. Keep table-heavy, sequence-heavy, and identifier-heavy regions out of prose-merging logic.
5. After patching, run a residual-pattern check for:
   - caption + body glued together
   - title + body glued together
   - explanation note + main text glued together
   - repeated fragments introduced by earlier formatting passes
6. Report the remaining boundary clearly:
   - prose continuity improved
   - table reconstruction still pending where layout loss is severe

## Common pitfalls
- Converting damaged tables into fake prose creates new errors that are harder to spot later.
- Front-matter formatting rules can silently damage body paragraphs if not section-scoped.
- A second global cleanup pass often fixes one seam while breaking three others.

## Practical rule
Once the file is 70-80% structurally clean, stop doing broad cleanup and switch to local continuity surgery.