# NarL/NO3/NADPH hypothesis review pattern for `basic_pathway_e_coli`

Use when the user asks to review the current repo for support/refutation of a NarL-centered mechanism hypothesis and wants both a judgment and a visualization.

## Durable lesson from this session
In this project class, the correct deliverable is not a generic biology summary. The user wants a repo-grounded evidence review that keeps the named mechanism central and explicitly separates:
- strong support
- partial support
- counter-evidence / boundary conditions

## Wording constraints that mattered

### Prefer this framing
- NO3 does not "directly increase NADPH"
- Better: under low O2, NO3 supports nitrate respiration / pmf, which indirectly sustains PntAB-mediated NADPH regeneration
- NarL should be framed as a dynamic control node coupling nitrate response, nitrogen-state signaling, and arginine retention
- "Enhancing NarL" should usually be rewritten as optimizing the NarL exposure/control window

### Avoid this framing
- "NO3 directly补NADPH"
- "NarL越强越好"
- Mechanism-free output maximization language when the user explicitly asked for NarL-centered evidence

## Repo evidence anchors used in this session

### Mechanism document
- `NarL_NADPH_Arginine_Production_Report.md`
  - lines 15-17: arginine synthesis is NADPH intensive
  - lines 31-33: nitrate effect on NADPH is indirect via pmf -> PntAB
  - lines 39-41 and 47-49: NarL links nitrate respiration, nitrogen sufficiency, and AST repression

### Executable model code
- `scripts/narl_nadph_circuit.py`
  - `compute_narl_p_biphasic()` for NO3 activation + NO2 inhibition + aerobic damping
  - `apply_nadph_engineering()` for ΔsthA / pntAB / NirBD axis
  - `apply_ast_repression()` for dynamic AST repression by NarL~P
- `scripts/two_stage_simulation.py`
  - Stage II low-O2 + nitrate bolus execution
  - stepwise NarL recomputation and nitrite balance

### Quantitative result files
- `results/strain_comparison.csv`
- `results/narl_phospho_control/narl_control_comparison_table.csv`
- `results/narl_phospho_local_search/best_local_search_case.json`
- `results/narl_phospho_local_search/top10_local_search.csv`
- `NarL_PHOSPHO_LOCAL_SEARCH_REPORT.md`

## Output pattern that worked
1. Write a project-root markdown review with:
   - one-sentence verdict
   - corrected wording for the hypothesis
   - evidence table
   - supporting evidence section
   - counter-evidence / boundary conditions section
   - recommended final manuscript/report wording
2. Create an SVG mechanism-evidence summary figure in `figures/`
3. In the final reply, report both file paths and give a short verdict

## Important analytical guardrail
Do not overclaim from control-oriented optimization outputs.
This repo currently supports a distinction between:
- NarL-focused control optimum
- pure end-point titer optimum
These are not always the same. The review should say so explicitly.

## Session-specific file outputs
- `NARL_NO3_NADPH_ARGININE_HYPOTHESIS_REVIEW.md`
- `figures/narl_no3_nadph_arginine_evidence.svg`
