# Big-data-to-disease causal target indication pattern

Use this reference when a biomedical big-data project tries to move from GWAS/PWAS/omics/ML signals to disease-causal targets or therapeutic target claims.

## Core lesson

Do not let biomarker evidence silently become causal language. A publication-ready review must separate:

1. Predictive biomarker support — ML/SHAP/stability evidence.
2. Genetic target hypothesis — PWAS/pQTL/GWAS association, replication, direction consistency.
3. Target indication — multi-evidence prioritization for downstream validation.
4. Causal target candidate — requires locus-level colocalization and/or valid cis-MR, endpoint replication, and unresolved-heterogeneity checks.
5. Confirmed target — requires strong causal inference plus experimental or perturbational validation.

## Recommended repository upgrade

Add two explicit, reproducible layers instead of only adding prose caveats.

### 1. Causal target indication layer

Create a script that integrates existing project outputs, commonly:

- candidate table: PWAS/GWAS/pQTL signals
- annotated target table: gene symbols, IDs, directions
- ML explainability table: SHAP or feature importance
- stability table: multi-seed/bootstrap recurrence
- drug perturbation or external validation overlap table

Recommended outputs:

- `results/causal_target_indication_table.csv`
- `results/causal_target_indication_report.md`
- `results/publication_evidence_grade_matrix.csv`
- `results/causal_validation_roadmap.md`
- `results/causal_target_indication_summary.json`

Suggested scoring fields:

- genome-wide or FDR-significant genetic support
- number of models/cohorts/ancestries replicated
- direction consistency
- heterogeneity, e.g. I2, retained as caution not hidden
- predictive support, e.g. top-20 SHAP
- multi-seed/bootstrapped stability
- pharmacologic or perturbational direction concordance
- known disease biology/drug-target prior

Suggested claim levels:

- `Grade B+`: high-priority causal-inference candidate; ready for coloc/MR, not causal proof
- `Grade B`: strong target hypothesis with heterogeneity caution
- `Grade C+`: genetically anchored hypothesis needing orthogonal evidence
- `Grade C`: predictive biomarker candidate only
- `Grade D`: exploratory signal

### 2. Causal inference readiness audit

Add a separate script that checks whether formal coloc/MR can actually be run from packaged files. This prevents the agent from fabricating unavailable causal results.

Recommended outputs:

- `results/priority_loci_for_coloc_mr.csv`
- `results/coloc_required_input_schema.csv`
- `results/mr_required_input_schema.csv`
- `results/causal_inference_readiness_summary.json`
- `results/causal_inference_readiness_report.md`

Minimum fields for colocalization schema:

- `gene_or_protein`
- `trait`
- `variant_id`
- `chromosome`
- `position`
- `effect_allele`
- `other_allele`
- `eaf`
- `beta`
- `se`
- `p`
- `n`

Minimum fields for MR schema:

- `gene_or_protein`
- `exposure_trait`
- `outcome_trait`
- `variant_id`
- `effect_allele`
- `other_allele`
- `exposure_beta`
- `exposure_se`
- `exposure_p`
- `outcome_beta`
- `outcome_se`
- `outcome_p`
- `eaf`
- `n_exposure`
- `n_outcome`

If packaged data only contain protein-level rows such as `protein, beta, se, p, chromosome, start, end, model`, then coloc/MR is blocked. Report this explicitly and export the required schema rather than running pseudo-causal analysis.

## Manuscript language rules

Use until coloc/MR/experimental validation exists:

- "target indication"
- "causal validation priority"
- "genetically anchored target hypothesis"
- "high-priority causal-inference candidate"
- "predictive biomarker"

Avoid before causal evidence exists:

- "causal target"
- "disease driver"
- "therapeutic target" as a definitive claim
- "validated mechanism" unless experimental validation exists

## Supervisor-style next-step decision rule

A target can move from target indication to causal target candidate only after:

1. Convincing shared-signal colocalization, e.g. PP.H4 or equivalent.
2. Directionally consistent cis-MR where valid instruments exist.
3. Endpoint-specific replication, preferably separating HF, MI/CAD, stroke, etc.
4. Allele harmonization, LD, and heterogeneity issues are resolved.
5. Biomarker targets such as NT-proBNP are not confused with intervention targets unless perturbation rationale is explicit.

## Verification checklist

- New scripts are registered in `pipeline_config.yaml` or the project orchestrator.
- Expected artifacts are listed in the pipeline config.
- A targeted pipeline run succeeds.
- Manifest or health report updates.
- Manuscript caveats are grounded in generated outputs.
- README or supervisor report points readers to the evidence matrix and readiness audit.
