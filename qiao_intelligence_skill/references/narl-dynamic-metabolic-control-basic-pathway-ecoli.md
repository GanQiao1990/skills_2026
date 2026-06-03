# NarL-driven metabolic-control workflow for `basic_pathway_e_coli`

Use when the task is not generic arginine maximization but NarL-centered metabolic regulation in `/home/qiao/qiao_design/e_coli_model/basic_pathway_e_coli`.

## Key lesson
For this project, the user wants **NarL phosphorylation and its downstream metabolic perturbation** to remain the organizing mechanism. Do **not** collapse the task into static FBA yield maximization unless the user explicitly asks for a mechanism-agnostic optimum.

## Executable control path in this repo
- `scripts/narl_nadph_circuit.py`
  - `compute_narl_p_biphasic(...)`: NarL~P depends on nitrate activation, nitrite inhibition, and aerobic damping.
  - `apply_ast_repression(...)`: maps NarL~P to AST/astCADBE repression.
  - `apply_nadph_engineering(...)`: links NarL-state to nitrate/nitrite/NADPH axes via PntAB, SthA, NirBD.
- `scripts/two_stage_simulation.py`
  - Implements Stage I aerobic growth → Stage II microaerobic + nitrate bolus dFBA.
  - Recomputes NarL~P each step and propagates it into metabolic perturbation.
- `scripts/narl_nadph_circuit_params_override.py`
  - One-shot JSON override loader for NarL circuit parameters.

## Practical workflow
1. Treat the project as a **dynamic control** problem, not a single LP.
2. Before optimization, explicitly separate two identities:
   - `Arg10_108gL_Validated` = canonical experimentally validated ~108 g/L chassis
   - `Full_Optimised` = current NarL process-optimisation target / derived design
   Do not treat them as synonyms.
3. Define candidate control inputs:
   - `no3_bolus_mM`
   - `o2_stage2_frac`
   - `t_switch_h`
   - NarL parameters such as `Kd_no3`, `Ki_no2`, `n_hill`, `aerobic_damping`
4. Execute with `two_stage_simulation.run_two_stage(...)`, or with a dedicated runner script if you need a batch of NarL control scenarios.
5. Report both product and controller state:
   - arginine titer/productivity
   - NarL~P stage-II mean / peak / AUC
   - nitrite peak
   - PntAB and PPP NADPH contributions
   - AST flux suppression
6. Explicitly distinguish:
   - chassis baseline under NarL control
   - derived-design / process-optimised performance under NarL control
   - absolute production optimum
   These may differ.

## SC97-GEM-derived modeling lesson
When the user asks to learn from another GEM such as `SC97-GEM`, transfer the **modeling discipline**, not the organism identity:
- keep chassis identity explicit
- keep model/procedure versions explicit
- keep biomass/calibration provenance explicit
- express downstream engineering as derivatives of the chassis rather than replacing the chassis with abstract labels

In `basic_pathway_e_coli`, this means the most durable framing is:
- chassis anchor: `Arg10_108gL_Validated`
- NarL process target: `Full_Optimised`
- control layer: `compute_narl_p_biphasic`, AST repression, PntAB/SthA redox engineering, NirBD detox

If updating code or reports, prefer wording like “validated-chassis derivative” over presenting `ArgEng`, `Full`, or `Full_Optimised` as if they were independent biological starting points.

## Session-specific evidence from this run
Runners added:
- `scripts/narl_phospho_argmax_execute.py`
- `scripts/narl_phospho_local_search.py`

Outputs:
- `results/narl_phospho_control/narl_control_scenarios.csv`
- `results/narl_phospho_control/best_narl_controlled_case.json`
- `results/narl_phospho_control/narl_control_comparison_table.csv`
- `results/narl_phospho_local_search/local_search_results.csv`
- `results/narl_phospho_local_search/best_local_search_case.json`
- `results/narl_phospho_local_search/top10_local_search.csv`
- `NarL_PHOSPHO_ARGMAX_EXECUTION_REPORT.md`
- `NarL_PHOSPHO_LOCAL_SEARCH_REPORT.md`

## Observed optima from this session
### NarL-controlled scenario optimum (coarse scenario execution)
- strain: `Full_Optimised`
- `no3_bolus_mM = 40`
- `o2_stage2_frac = 0.03`
- `t_switch_h = 12`
- `Kd_no3 = 1.0`
- `Ki_no2 = 30.0`
- arginine titer ≈ `13.3324 g/L`

### Refined NarL-focused local-search optimum
- strain: `Full_Optimised`
- `no3_bolus_mM = 50`
- `o2_stage2_frac = 0.03`
- `t_switch_h = 10`
- `Kd_no3 = 1.0`
- `Ki_no2 = 30.0`
- arginine titer ≈ `13.6553 g/L`
- NarL AUC ≈ `1.1993`
- nitrite peak ≈ `16.10 mM`

### Important tradeoff
A lower-nitrate point (e.g. `20 mM`) can produce higher terminal arginine in some searches, but with materially lower NarL exposure. If the user frames the task as a **NarL control-theory** problem, choose the NarL-weighted optimum and explain the tradeoff explicitly.

## Pitfalls
- Do not interpret a higher absolute titer in a no-nitrate / NarL-off case as defeating the user's request when the task explicitly centers NarL control theory.
- Do not report only product titer; for this class of task, omit NarL~P, nitrite, and NADPH-state metrics only if the user explicitly says they are unnecessary.
