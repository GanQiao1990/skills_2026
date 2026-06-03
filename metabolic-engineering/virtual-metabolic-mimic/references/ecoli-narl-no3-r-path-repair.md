# Ec_coli_modelling NarL/NO3 R-path repair notes

Use this note when the first-pass Python path already works and you want to bring the original `Ec_coli_modelling` R/dFBA path forward for the NarL/NO3 experiment.

## What was fixed successfully

1. R package chain for the NarL R path:
   - `R.matlab`
   - `epimod` (from GitHub)
   - transitive dependency needed by `epimod`: `fdatest`
   - later blocker in model preparation: `strex`

2. Code-level pitfall in `code/scripts/generating_carbon regimes.R`:
   - the file expected a global `carbon_reg` vector
   - `run_narl_no3_dynamic.R` sources NarL regime generation indirectly, so add a default `carbon_reg` definition at the top of `generating_carbon regimes.R` when it does not already exist

3. Code-level pitfall in `run_narl_no3_dynamic.R`:
   - explicitly load `epimod` with `library(epimod)` before calling `Exe.exp()` / `model.generation()` / `model.analysis()`

## Install sequence that worked

```r
remotes::install_cran('R.matlab', repos='https://cloud.r-project.org', dependencies=TRUE, upgrade='never')
remotes::install_cran('fdatest', repos='https://cloud.r-project.org', dependencies=TRUE, upgrade='never')
remotes::install_cran('strex', repos='https://cloud.r-project.org', dependencies=TRUE, upgrade='never')
remotes::install_github('qBioTurin/epimod', upgrade='never')
```

## Verification sequence

From `Ec_coli_modelling/`:

```bash
Rscript code/scripts/prepare_narl_compiled_models.R
Rscript run_narl_no3_dynamic.R
```

Expected status after repair:
- `prepare_narl_compiled_models.R` should write:
  - `input/compiled_models/iML1515_narL_off.txt`
  - `input/compiled_models/iML1515_narL_on_no3.txt`
  - `input/compiled_models/iML1515_narL_on_no3_nitrite_clearance.txt`

## Remaining runtime requirement

After the R package fixes, the next blocker is usually not R code but epimod container availability.

`epimod::model.generation()` reads container names from the installed package and uses Docker. In this session the package expected images including:
- `qbioturin/epimod-generation:latest`
- `qbioturin/epimod-analysis:latest`

If `run_narl_no3_dynamic.R` reaches Docker and then fails, treat it as an epimod container-availability problem rather than an R-script logic problem.

## How to phrase the limitation

Use this wording pattern in deliverables:
- R dependency chain repaired
- NarL compiled-model generation verified
- full end-to-end R/dFBA run still depends on local availability of epimod Docker images

This avoids overstating that the modeling logic is broken when the real blocker is container access.