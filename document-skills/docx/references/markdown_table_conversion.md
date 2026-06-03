# Markdown table conversion in DOCX workflows

Use this reference when converting manuscript Markdown that contains pipe tables into Word documents.

## Key lesson

A Markdown-to-DOCX script that only treats paragraphs, headings, and images will silently fail on pipe tables. The result is a DOCX that contains the literal table source as paragraphs, which looks broken in Word even though the conversion script "succeeds."

## What to do

1. Detect Markdown pipe tables explicitly.
2. Parse the header row, separator row, and body rows.
3. Create a real `python-docx` table rather than adding the table text as a paragraph.
4. Apply conservative formatting:
   - `Table Grid` style
   - compact font size for wide scientific tables
   - centered header row
   - no paragraph indentation inside cells
5. Rebuild the DOCX and verify it.

## Verification checks

After conversion, confirm all of the following:

- `len(doc.tables) > 0` when the manuscript contains pipe tables
- no paragraphs begin with `|`
- each important results table has the expected row and column count
- the DOCX file size is non-trivial and changes after regeneration

## Common pitfall

If you see output like this in Word, the converter did not actually create a table:

```text
| Dataset | model | auc |
|:--|:--|--:|
| Olink | XGB | 0.807 |
```

That means the Markdown table parser is missing or the script is not routing table blocks into `doc.add_table(...)`.
