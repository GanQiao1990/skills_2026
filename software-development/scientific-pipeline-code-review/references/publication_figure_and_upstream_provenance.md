# Publication-figure and upstream-provenance notes for cardiovascular multi-omics projects

This note captures two recurring publication issues from the cardiovascular target-indication workflow:

1. Figure 1 volcano plots should use restrained, colorblind-safe encoding rather than multiple saturated colors for tiers and subgroups.
2. The manuscript should explicitly name the first data-treatment layer when the active report repository depends on an upstream sibling workspace for variant curation and BLISS-ready summary-statistic construction.

## Figure 1 design pattern
- Use at most two semantic colors for direction: muted blue for risk-decreasing and muted crimson for risk-increasing.
- Encode support strength with point size or alpha, not with extra hue categories.
- Put filter criteria in the caption or a bottom footnote, not inside the plotting field.
- If y-values are capped for display, state the cap directly in the axis label or caption.
- Label only a small set of canonical anchors; do not annotate every significant point.

## Upstream provenance pattern
- If variant preprocessing happens in a sibling workspace, mention it as the first data-treatment layer in Abstract, Results, and Methods.
- Report the actual number of retained disease terms, lead variants, and BLISS-formatted SNP records only after verifying the upstream output files.
- Do not present cross-model PWAS results as if they were generated from an untraceable black box.

## Numeric integrity checks
- If a figure or table shows repeated values, ask whether the repetition is a consequence of the design (for example, three seeds produce only 0, 1/3, 2/3, 1.0) or an artifact of formatting.
- Prefer direct values from result files over hand-copied mimic numbers.
- Every repeated or rounded value should be explainable from the underlying computation or seed count.
