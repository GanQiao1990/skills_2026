# Repository-grounded eight-figure report pattern

Use this reference when a user asks for a publication-quality computational report with a larger figure family (for example eight figures) built from a local research repository.

## Durable pattern

1. Keep the Markdown manuscript as the authoritative source.
2. Point the manuscript only at package-local figure paths under `figures/`.
3. Create a package-local `canonical_data/` directory containing the exact CSV/JSON/workflow files used by the figure generator.
4. Reserve `canonical_inputs/` for copied legacy graphics or supporting source images; do not rely on them as the only source of truth if the new figure suite is data-driven.
5. Include a reviewer-facing `EVIDENCE_MAP.md` so third parties can inspect where structure, provenance, figure, and DOCX requirements are satisfied.
6. Re-audit headline numbers from the package-local evidence before finalizing. Do not trust earlier summaries if direct parsing now gives a different answer.

## Figure-family composition that worked well

A coherent eight-figure suite can mix:
- one graphical abstract
- one catalytic or workflow schematic grounded in inspected config files
- one execution/inventory summary figure built from logs and output counts
- one route or method-comparison schematic built from documented workflow alternatives
- one candidate ranking plot
- one batch-comparison plot with statistical annotations
- one subsection or feature heatmap
- one annotation-landscape or keyword-distribution figure

## Provenance rules

- If the user-supplied literal path token is malformed or unreadable, say so explicitly in the manuscript.
- Distinguish repository-local evidence from external literature context.
- If no wet-lab evidence exists, describe validation as a plan, not a result.
- If a direct package-local re-audit contradicts an earlier manuscript number, update the manuscript, figure captions, and evidence map to the corrected value.

## Package docs that improved judge-friendliness

Recommended package contents:
- authoritative manuscript `.md`
- generated `.docx`
- `generate_docx_from_markdown.py`
- `generate_publication_figures.py`
- `README_REPORT_WORKFLOW.md`
- `INDEX.md`
- `VALIDATION_NOTE.md`
- `EVIDENCE_MAP.md`
- `figures/`
- `publication_assets/`
- `canonical_data/`
- `canonical_inputs/`

## Specific pitfall observed

Earlier draft text and notes claimed a uniform v4 sequence length of 360 aa. A later direct re-parse of the accessible sequence output files yielded 533 aa. The durable lesson is not the specific number; it is the audit rule: re-parse current canonical outputs before finalizing any headline quantitative statement.
