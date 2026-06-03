# Archived skill: publication-ready-scientific-manuscript-figure-revision

Original path: `scientific-writing/publication-ready-scientific-manuscript-figure-revision`

---

---
name: publication-ready-scientific-manuscript-figure-revision
description: Revise computational biology or data-science manuscripts together with their generating figure scripts. Use when the task is not just prose editing but also requires aligning methods, results, figures, and code-generated visualizations for submission-ready consistency.
version: 1.0.0
author: hermes-agent
license: MIT
metadata:
  hermes:
    tags: [scientific-writing, engineering, figures, reproducibility]
---

# Publication-Ready Scientific Manuscript + Figure Revision

Use this skill when a manuscript, methods section, and figure script need to be revised together for publication quality. The goal is to keep the narrative, numbers, and visuals consistent with the actual pipeline output.

## When to use
- The user asks to revise a scientific manuscript and mentions figures or visualizations.
- The manuscript needs a missing preprocessing / methods stage added.
- The figure is readable but needs clearer labeling, fewer overlaps, or a more publication-style layout.
- The user wants the revision to be grounded in code and output files, not only prose.

## Core workflow
1. **Start with evidence**
   - Read the manuscript, the figure-generating script, and any result tables that the figure or text depends on.
   - Record assumptions and evidence in `DEBUG.md` before editing if the project uses one.

2. **Find the first missing conceptual step**
   - For Methods, check whether preprocessing, harmonization, and the primary analysis stage are both described.
   - If the manuscript only describes the downstream association step, add the upstream input-generation stage explicitly.

3. **Revise prose with minimal content drift**
   - Keep the scientific claim unchanged.
   - Improve clarity, make workflow order explicit, and tighten wording.
   - Preserve numbers exactly unless the source data prove they are stale.

4. **Improve visuals for readability, not decoration**
   - Reduce label count before changing colors or fonts.
   - Prioritize label overlap reduction, smaller point sizes, and cleaner titles/subtitles/captions.
   - Keep the plot scientifically honest; do not add decorative elements that obscure the data.

5. **Prefer script-level fixes over image-only fixes**
   - Edit the generating script first.
   - Avoid editing exported figures unless the script cannot be regenerated.
   - If a plotting script has duplicated output blocks, remove the duplicate and keep one canonical rendering path.

6. **Verify before finishing**
   - Run a parser or syntax check on the edited script.
   - Re-read the edited manuscript section to confirm the new step appears in the right place.
   - If possible, confirm the figure script writes the intended output file once.

## Practical revision rules
- Add missing methods stages in the order they happened: preprocessing → harmonization → analysis → meta-analysis → downstream prioritization.
- If the missing stage is the upstream BLISS/TWAS/PWAS input-generation step, verify the concrete counts from preprocessing docs or logs (for example: annotated variant records, retained harmonized SNPs, number of per-chromosome files) and propagate those numbers consistently into the abstract, methods, and the first results paragraph.
- When multiple manuscript drafts coexist in the same repo, identify the actively edited draft and also check whether a top-level or manuscript-facing canonical copy should be kept in sync.
- Before editing a figure, trace the manuscript-facing figure filename to the script that actually writes it. Do not assume the most recent or similarly named volcano-plot block is the canonical manuscript figure when multiple scripts generate related plots.
- For volcano plots, limit labels to top-ranked hits and known anchors.
- When the manuscript interpretation hinges on biological direction classes, prefer de-emphasized background points plus direction-based highlighting for key candidates over a dense continuous coloring by support count.
- If the effect-size axis is dominated by a few extreme values, use a monotonic signed compression transform (for example `sign(beta) * log10(1 + |beta|)`) to preserve direction while improving readability; then update the manuscript text or caption so the transformed axis is explicitly described.
- Prefer a cleaner axis transformation if it matches the analysis and helps interpretability.
- Use short, specific captions that explain the visual encoding and why labels were selected.
- In multi-script projects, verify whether the manuscript figure comes from the main analysis script or from a secondary candidate-only plotting script before editing; secondary EnhancedVolcano-style outputs are often not the canonical manuscript figure.
- Do not over-edit into a generic writing style; keep the project’s technical voice.

## Common pitfalls
- The manuscript mentions BLISS or PWAS, but not the initial BLISS-ready input generation.
- The plot is technically correct but cluttered because too many labels are drawn.
- The figure script contains two similar output blocks, causing confusion about the canonical plot.
- The new figure style is described as "beautiful" when the real goal is clarity and interpretability.
- The narrative and figure labels use slightly different statistical terms for the same quantity.

## Verification checklist
- [ ] The manuscript names the full workflow, including the first preprocessing stage.
- [ ] The figure script produces a single canonical output path.
- [ ] Label count is intentionally constrained.
- [ ] The plot title, axis labels, and caption match the manuscript terminology.
- [ ] The script parses or runs without syntax errors.
- [ ] `DEBUG.md` records assumptions and evidence if the project uses it.

## Output standard
When reporting back, summarize:
- what was added to the manuscript,
- what was changed in the plot logic,
- how the plot became clearer,
- and what verification was performed.
