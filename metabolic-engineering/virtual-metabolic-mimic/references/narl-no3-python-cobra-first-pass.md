# NarL/NO3 first-pass Python/cobra fallback for Ec_coli_modelling

Use this when the user wants a runnable first-pass NarL/NO3 virtual experiment now, the project already has an `Ec_coli_modelling`-style dynamic workflow scaffold, but the full R/dFBA path is not yet executing end-to-end.

## When this pattern fits
- The repo already contains scenario-generation / compiled-model scripts for NarL/NO3.
- The metabolic backbone exists as a `.mat` GEM (for example `iML1515.mat`).
- You need actual results, figures, and a report in the current session.
- It is acceptable to produce a clearly labeled first-pass approximation rather than a full PN/GSPN-coupled run.

## Core move
Build a local Python/cobra runner in the target deliverable directory while preserving the source repo's intended architecture.

1. Keep the source R workflow as the canonical extension path.
2. Load the same GEM backbone from the repo's `.mat` file.
3. Express NarL states by reaction-bound changes rather than inventing a new regulatory model.
4. Generate time-course CSV outputs and figures locally.
5. Write the report as a first-pass computational study with explicit limitations.

## Practical mapping used successfully
For an E. coli NarL / nitrate hypothesis, the following reaction families were sufficient for a first executable pass:
- Exchange / environment: `EX_glc__D_e`, `EX_o2_e`, `EX_no3_e`, `EX_no2_e`, `EX_nh4_e`
- Product export: `EX_arg__L_e`, `EX_lys__L_e`
- Nitrate / nitrite handling: `NO3R1pp`, `NO3R2pp`, `NTRIR2x`, `NTRIR3pp`, `NTRIR4pp`, `NO3t7pp`, `NO2t2rpp`
- Amino-acid pathway / competition: `ARGSS`, `ARGSL`, `OCBT`, `ACGS`, `ACGK`, `AST`
- Fermentation competition: `PFL`, `FRD2`, `FRD3`
- Cofactor proxies: `NADTRHD`, `THD2pp`, `GLUSy`, `GLUDy`

## Minimal scenario set
A compact first-pass grid that gave interpretable results:
- High-O2 arginine baseline
- High-O2 to low-O2 arginine without nitrate
- High-O2 to low-O2 arginine with nitrate but NarL-off
- High-O2 to low-O2 arginine with nitrate and NarL-on
- High-O2 to low-O2 arginine with stronger nitrate input plus enhanced nitrite clearance
- One lysine-transfer scenario under NarL-on + nitrate

## Recommended approximations
- Use growth-to-production switching at a defined timepoint.
- Represent NarL-off by strongly limiting nitrate/nitrite reduction capacity.
- Represent NarL-on by increasing nitrate/nitrite reduction bounds, constraining competing fermentation / arginine-catabolism reactions, and widening transhydrogenase-related bounds.
- Track proxy metrics instead of overclaiming intracellular state estimation.

Good proxy outputs:
- product export flux
- biomass proxy
- nitrate uptake / reduction flux
- nitrite accumulation proxy
- nitrogen assimilation proxy (for example `GLUSy - GLUDy`)
- cofactor-balance proxy (for example `NADTRHD + THD2pp`)
- fermentation proxy (`PFL + FRD2 + FRD3`)

## Deliverables pattern
Write all of the following into the task directory:
- `*_virtual_experiment.py`
- `make_*_figures.py`
- `results/*.csv`
- `figures/*.png`
- an academic-style Markdown report

## Reporting guardrails
State clearly that:
- this is a first-pass approximation built on the project GEM backbone
- NarL is represented by constraint changes, not a full signaling model
- nitrate/nitrite are not yet fully integrated into the PN/GSPN layer if that layer still lacks explicit places/transitions
- the result supports scenario prioritization, not definitive process parameters

## Why this is worth saving
This pattern preserves continuity with the existing repo, produces figures and a report in one session, and avoids the common failure mode where the agent stops after discovering the canonical workflow is not yet runnable.