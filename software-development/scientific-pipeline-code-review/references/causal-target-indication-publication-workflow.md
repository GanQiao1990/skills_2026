# Causal target-indication publication workflow

Use this reference when reviewing or upgrading a big-data-to-disease, PWAS, multi-omics, biomarker-to-target, or causal-analysis project toward publication quality.

## Core lesson

Do not let a manuscript imply definitive causality when the repository only contains protein-level/model-level PWAS summaries, SHAP rankings, enrichment outputs, or drug-perturbation overlaps. These are strong target-indication signals, not causal proof. Publication-quality supervision should explicitly separate:

1. Biomarker discovery: predictive or associative molecular features.
2. Genetically anchored target hypotheses: PWAS-supported proteins with replication and directional consistency.
3. Causal-inference candidates: targets ready for coloc/MR because variant-level inputs exist or are explicitly requested.
4. Causal targets: only after locus-level colocalization, harmonized cis-MR/two-sample MR, sensitivity checks, and endpoint-specific replication support the claim.

## Practical review sequence

1. Write or update a DEBUG.md scaffold with assumptions, evidence sources, and claim boundaries before executing changes.
2. Inspect the repository for the orchestration entry point, config, manuscript, results tables, figures, and health reports.
3. Audit whether current data support formal causality:
   - coloc requires gene/protein, trait, variant_id, chromosome, position, effect_allele, other_allele, eaf, beta, se, p, and n.
   - MR requires harmonized exposure/outcome variant effects, alleles, allele frequency, and exposure/outcome sample sizes.
   - If only protein/model-level fields exist, state that coloc/MR is blocked by missing SNP-level summary statistics.
4. Add a conservative target-indication module rather than forcing unsupported causal claims. Score candidates using PWAS strength, cross-model replication, direction consistency, ML predictive importance, marker stability, pharmacologic concordance, known biology, and heterogeneity flags.
5. Export publication-facing artifacts:
   - ranked target-indication table
   - evidence-grade matrix
   - causal-validation roadmap
   - priority loci for future coloc/MR
   - required input schemas for coloc and MR
6. Register any new scripts in the pipeline config and script inventory so the work is reproducible.
7. Re-run the specific new pipeline steps and verify exit status, generated artifacts, figure links, word count, references, and document export.
8. Revise the manuscript with conservative language: “target indication,” “genetically anchored target hypotheses,” and “causal-validation readiness,” not “proven causal targets.”

## Manuscript framing pattern

A publication-ready framing is:

“An integrated multi-omics framework identifies genetically anchored biomarkers and target hypotheses for cardiovascular disease and defines a prioritized roadmap for causal validation.”

Avoid unsupported claims such as:

- “We discovered causal therapeutic targets”
- “PWAS proves protein X causes disease”
- “SHAP feature importance validates the target”
- “Semaglutide overlap confirms target engagement”

Instead write:

- “supports target indication”
- “prioritizes proteins for colocalization, Mendelian randomization, and perturbation studies”
- “provides pharmacologic triangulation rather than direct validation”
- “the current data support target hypotheses, not definitive causality”

## Evidence grading template

Suggested grades:

- Grade A: coloc/MR-supported causal candidate with endpoint-specific replication and sensitivity analyses.
- Grade B+: high-priority causal-inference candidate with strong genetic support and low unresolved heterogeneity, ready for coloc/MR.
- Grade B: strong target hypothesis with heterogeneity caution or missing SNP-level causal evidence.
- Grade C+: genetically anchored hypothesis with PWAS support but limited orthogonal evidence.
- Grade D: exploratory signal.

## Key pitfall

High statistical significance is not a substitute for causal evidence. A candidate with very small FDR and high replication can still require caution if heterogeneity is high or if SNP-level exposure/outcome summary statistics are missing.
