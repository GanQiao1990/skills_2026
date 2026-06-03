"""
Protein Hallucination Review Template — Reference Implementation

This is the actual review template created for evaluating de novo protein design
papers using hallucination/diffusion algorithms. Copy and adapt for other domains.

Files in ai_scientist/review_templates/:
  __init__.py                          — exports review_form, scoring_rubric, thought_prompt
  protein_hallucination_review.py      — the 3 string components
  protein_hallucination_usage.py       — usage examples + example JSON output

Usage:
  from ai_scientist.review_templates import protein_hallucination_review_form
  from ai_scientist.perform_llm_review import perform_review
  
  review = perform_review(
      text=paper_text,
      model="mimo-v2.5-pro",
      client=client,
      num_reflections=2,
      num_reviews_ensemble=3,
      review_instruction_form=protein_hallucination_review_form,
  )
"""

# Key design decisions for this template:
# 
# 1. Extended NeurIPS form as base — familiar to reviewers, easy to parse
# 2. Domain-specific Strengths/Weaknesses sub-dimensions:
#    - Methodological Innovation (vs RFdiffusion/Chroma/DPLM-2)
#    - Experimental Validation (SPR/BLI, X-ray/cryo-EM, functional)
#    - Design Quality (scTM, novelty, diversity)
#    - Generality (task types, size limits, hyperparameter sensitivity)
# 3. Weighted scoring rubric (4 tiers):
#    - Tier 1: Methodological Rigor (30%)
#    - Tier 2: Computational Evaluation (30%)
#    - Tier 3: Experimental Validation (25%)
#    - Tier 4: Reproducibility & Impact (15%)
# 4. Structured thought-prompt (6-step evaluation framework)
# 5. Usage examples separated to avoid pymupdf import issues

# Adapting to another domain:
# 1. Copy protein_hallucination_review.py → your_domain_review.py
# 2. Replace domain-specific terms (hallucination → your method)
# 3. Replace sub-dimensions in Strengths/Weaknesses
# 4. Replace scoring rubric tiers and weights
# 5. Update thought-prompt steps
# 6. Update __init__.py exports
