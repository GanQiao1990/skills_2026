# Production optimization notes

Condensed notes from an iML1515 arginine-maximization session in `/home/qiao/qiao_design/e_coli_model/basic_pathway_e_coli`.

## Durable lessons

### 1) Medium editing pitfall
A custom `set_environment()` that replaced `model.medium` with only a short list of exchanges caused false infeasibility. The fix was to start from `model.medium.copy()` and update only intended exchanges (`EX_glc__D_e`, `EX_nh4_e`, `EX_o2_e`, `EX_no3_e`, etc.), preserving trace ions/cofactors unless deliberately changed.

### 2) Exchange-reaction interpretation
For COBRA exchange reactions:
- uptake = negative flux
- secretion = positive flux

In this session, arginine production was defined as positive flux through `EX_arg__L_e` in `mmol gDW^-1 h^-1`.

### 3) Balance-check scope
Internal arginine-pathway reactions were element/charge balanced, while `EX_arg__L_e` was not. That is expected for exchange reactions; do not flag this as a pathway-stoichiometry defect.

### 4) FVA around a production optimum
Built-in `flux_variability_analysis()` became brittle after changing the optimization target and pinning production. A robust fallback is:
1. Optimize the production target.
2. Constrain the target exchange to ~99% of the optimum.
3. Under a context manager, set each reaction as the temporary objective and optimize `max` / `min` manually.
4. Only accept rows where status is `optimal`.

### 5) Solver-status discipline
Infeasible solves may still expose stale `objective_value` or `fluxes`. Never report those values as real results. Gate all interpretation on accepted statuses such as `optimal`.

### 6) Compare structural vs scenario changes separately
If optimizing strain design, log:
- reaction knockouts / bound edits
- objective changes
- environment / medium changes
- biomass lower-bound constraints

This avoids over-attributing gains from a medium change to structural edits.

## Example production-analysis artifact set
Useful reproducibility outputs for metabolic-engineering sessions:
- baseline solve JSON
- optimized solve JSON
- baseline vs optimized CSV
- scenario comparison CSV
- key-flux tables
- change log CSV
- validation JSON (status, expected optimum, tolerance)
- named refactored model file distinct from the source model

## Example arginine-pathway reactions checked in the session
- `ACGS`
- `ACGK`
- `AGPR`
- `ACOTA`
- `ACODA`
- `OCBT`
- `CBPS`
- `ARGSS`
- `ARGSL`
- target exchange `EX_arg__L_e`

## Example competing branches edited in the session
- `ARGDC`
- `ARGDCpp`
- `ORNDC`
- `SPMS`
- `AST`
- partially restricted: `GLU5K`, `G5SD`

Use this file as a pattern reference, not as a universal biological claim.