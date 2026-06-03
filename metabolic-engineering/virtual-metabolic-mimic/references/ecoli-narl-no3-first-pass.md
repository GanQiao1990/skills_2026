# E. coli dFBA repo: first-pass NarL/NO3 integration pattern

Use this note when a user asks to both write a NarL dynamic-control strategy and begin modifying an existing local E. coli dynamic-metabolism repository.

## Situation pattern
A local repository already has:
- an E. coli dFBA / Petri-net hybrid workflow
- carbon-regime CSV generators
- an execution wrapper that rewrites a small parameter file before each run
- compiled FBA model generation from a `.mat` GEM

The user wants a first NarL / nitrate-driven hypothesis runner without destabilizing the baseline project.

## Recommended adaptation strategy

### 1. Do minimal shared-interface edits first
The smallest durable shared changes are:
- extend `init.gen(iG, iL)` to `init.gen(iG, iL, iN = 0)` so nitrate can be represented in the interface even before the PN layer is fully expanded
- extend the experiment runner to accept:
  - `regime_subdir`
  - `init_values`
  - `result_tag`

This lets a new hypothesis runner coexist with the original carbon-only workflow.

### 2. Add a new NarL/NO3 regime generator rather than overloading the existing one
Create a separate script (for example `code/scripts/generating_narl_no3_regimes.R`) that outputs matrices like:
- `time_h, glc, lcts, no3`

Recommended first-pass regimes:
- `nar_blank`
- `nar_low_o2_no_no3`
- `nar_low_o2_no3_constant`
- `nar_low_o2_no3_linear`
- `nar_low_o2_no3_pulse_60`
- `nar_low_o2_no3_pulse_150`

### 3. Encode NarL hypotheses as separate compiled-model variants
Do not manually tweak one compiled model repeatedly. Generate separate `.txt` compiled models for:
- `narL_off`
- `narL_on_no3`
- `narL_on_no3_nitrite_clearance`

Use reaction-bound edits to approximate the mechanistic state differences.

Useful iML1515 reactions seen in local BiGG metadata for this task class:
- nitrate / nitrite layer:
  - `EX_no3_e`
  - `EX_no2_e`
  - `NO3R1pp`, `NO3R2pp`
  - `NO3R1bpp`, `NO3R2bpp`
  - `NO3t7pp`
  - `NO2t2rpp`
  - `NTRIR2x`, `NTRIR3pp`, `NTRIR4pp`
- arginine layer:
  - `ACGS`, `ACGK`, `AGPR`, `OCBT`, `ARGSS`, `ARGSL`
  - `AST` (arginine catabolic branch worth suppressing in NarL-on product mode)
- redox / competing respiration / fermentation proxies:
  - `PFL`
  - `FRD2`, `FRD3`
  - `FDH4pp`, `FDH5pp`
  - `NADTRHD`
  - `GLUDy`, `GLUSy`

### 4. Add a dedicated hypothesis runner
Create a separate runner (for example `run_narl_no3_dynamic.R`) that iterates over:
- model variant × regime

and writes a manifest such as:
- `results/narl_no3_run_manifest.csv`

This keeps the hypothesis work reproducible and auditable.

## Important limitation language
If the PN / GSPN graph still only has carbon places and transitions, do not present the system as a fully coupled nitrate-aware Petri net yet.

Use language like:
- first-pass approximation
- FBA-constraint layer extended
- PN / GSPN nitrate places and transitions still pending

## Environment/setup lesson to encode in setup skills, not as a negative claim
If execution fails because `.mat` reading requires `R.matlab`, the durable lesson is:
- install `R.matlab` before running compiled-model preparation scripts that read GEM `.mat` files

This is a setup requirement, not a claim that the repo or tool is broken.
