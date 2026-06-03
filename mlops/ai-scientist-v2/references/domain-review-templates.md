# Domain-Specific Review Templates — Reference Implementation

## Protein Hallucination Review Template

Location in project: `ai_scientist/review_templates/protein_hallucination_review.py`

### Components

1. **`protein_hallucination_review_form`** — Main review form (5724 chars)
   - 9 evaluation dimensions with domain-specific prompts
   - Covers: Summary, Strengths/Weaknesses (with sub-dimensions), Questions, Limitations, Ethical Concerns, Soundness, Presentation, Contribution, Overall, Confidence, Decision

2. **`protein_hallucination_scoring_rubric`** — Weighted rubric (1371 chars)
   - Tier 1: Methodological Rigor (30%) — SE(3)-equivariance, noise schedules, architecture
   - Tier 2: Computational Evaluation (30%) — designability, novelty, diversity, AAR
   - Tier 3: Experimental Validation (25%) — SPR/BLI Kd, X-ray/cryo-EM, kcat/Km
   - Tier 4: Reproducibility & Impact (15%) — code, weights, data, protocols

3. **`protein_hallucination_thought_prompt`** — Structured thinking (1054 chars)
   - 6-step evaluation framework: Method Classification → Design Target → Key Innovation → Critical Weakness → vs RFdiffusion → Wet-lab Confidence

### Domain-Specific Review Dimensions

| Dimension | What to Evaluate |
|-----------|-----------------|
| Methodological Innovation | Novelty vs RFdiffusion/Chroma/DPLM-2; architecture justification |
| Experimental Validation | Computational benchmarks + wet-lab (SPR, X-ray, functional assays) |
| Design Quality | Self-consistency TM-score, scRMSD, novelty to PDB, diversity |
| Generality | Monomers/binders/enzymes; size limits; hyperparameter sensitivity |

### Key Metrics for Hallucination Papers

- **Designability**: self-consistency TM-score, scRMSD
- **Novelty**: max TM-score to PDB and training set
- **Diversity**: pairwise RMSD of generated samples
- **AAR**: amino acid recovery rate
- **Wet-lab**: Kd (SPR/BLI), Tm, structural validation (X-ray/cryo-EM)

### Adapting to Other Domains

To create a new domain review template:

1. Start from the NeurIPS form structure in `perform_llm_review.py` (the `neurips_form` variable)
2. Add domain-specific Strengths/Weaknesses sub-prompts
3. Add a domain-specific scoring rubric (weighted tiers)
4. Add a thought-prompt for structured evaluation
5. Create `__init__.py` that exports all components
6. Keep usage examples separate to avoid pymupdf import issues

### Pitfall: Module-Level Imports

`perform_llm_review.py` imports `pymupdf` at module level. Any file that imports from it (even indirectly) will fail if pymupdf is not installed. Solution: defer imports to function bodies in usage/example files.
