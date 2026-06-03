# Publication figure and upstream-data provenance fixes for causal target-indication projects

Use this reference when upgrading a big-data-to-disease / PWAS / multi-omics manuscript after supervisor review.

## 1. Do not let Figure 1 become visually noisy

For the main PWAS discovery volcano plot, avoid encoding too many concepts with color. A publication-clean default is:

- Below-filter/background points: light gray with low alpha.
- Risk-decreasing direction: one muted, colorblind-safe blue.
- Risk-increasing direction: one muted, colorblind-safe crimson/red.
- Cross-model support or evidence strength: marker size or alpha, not additional hue tiers.
- High-priority labels: only a short curated set of canonical or target-indication markers.
- Filter criteria: place in caption or a bottom figure note, not inside the densest plotting region.
- If p-values are clipped for display, disclose it in the y-axis label and caption, e.g. `-log10(P value), capped at 300 for display`.

Avoid multi-tier red/green palettes for volcano plots unless a journal explicitly requests them. They become visually cluttered and are harder to read in grayscale or for colorblind readers.

## 2. Include the first data-treatment layer when it exists outside the active report repo

If the integrated-report repo consumes results from an upstream workspace, explicitly document that provenance in the manuscript and methods. Do not start the workflow narrative at the first downstream figure if disease-variant curation or BLISS-ready summary-statistic construction happened elsewhere.

A good manuscript pattern is:

- Abstract: mention that the framework begins with cardiovascular GWAS Catalog/EFO variant curation and BLISS-ready summary-statistic construction.
- Introduction: state that the workflow begins with the first data-treatment/preprocessing layer, then proceeds to PWAS, enrichment, prediction, SHAP/stability, pharmacologic triangulation, and target indication.
- Results: add an early subsection such as `First data-treatment layer curates cardiovascular variants for BLISS PWAS`.
- Methods: add a dedicated preprocessing subsection describing trait/EFO resolution, GWAS Catalog lead-variant retrieval, rsID deduplication, Ensembl harmonization, Z-score construction, and per-chromosome BLISS sumstats output.
- Data/code availability: list both the integrated-report repo and upstream preprocessing/PWAS workspaces, if they are part of the reproducible analysis chain.

## 3. Evidence to extract before writing this section

Use actual local upstream outputs, not memory or vague claims. Typical evidence fields:

- Number of retained EFO terms.
- Number of unique GWAS Catalog lead variants.
- Number of per-chromosome BLISS summary-statistic files.
- Number of SNP records retained in BLISS format.
- Required BLISS columns, usually `CHR`, `SNP`, `A1`, `A2`, `Z`, and `N`.
- Path to cross-model PWAS outputs consumed by the downstream report.

Keep this as provenance and reproducibility evidence; do not inflate it into causal evidence. Variant preprocessing supports traceability, while colocalization/MR still require SNP-level exposure and outcome summary statistics.
