# Repo integration and oxygen reporting notes

## Durable pattern
When a metabolic-engineering repository mixes:
- validated GEM/ecGEM assets (`.mat`, SBML, XML)
- feeding-regime CSVs or experimental panels
- copied R/shell integration scripts

start by proving the model assets work directly.

Minimum verification:
1. load the model with COBRA
2. optimize once successfully
3. verify the requested product exchange reactions exist
4. verify the medium/oxygen assumptions explicitly

Only after that should you trust wrapper scripts.

## Entry-point audit checklist
For any inherited R or shell orchestration layer, check:
- exact filename matches in `source()` / imports
- no missing helper files
- no variables referenced before definition
- current output paths match the repo tree
- external reference files actually exist

If any of those fail, the wrapper layer is not yet an executable deliverable.

## Rescue strategy
If wrappers are broken but assets are good:
- build a direct Python/COBRA CLI first
- add tests around regime loading, CLI parsing, and simulation output shape
- produce real CSV/JSON outputs
- keep the old dynamic layer in the tree as reference only
- document the distinction in the README

## Oxygen reporting rule
In oxygen-sensitive fermentation simulations, keep two fields:
- oxygen_uptake: the imposed constraint / design setpoint
- oxygen_flux: the optimized solution value

This avoids confusing the design assumption with the realized model behavior.

## Why this is reusable
This pattern applies broadly to repositories that were assembled from several metabolic-modeling subprojects: the trustworthy core is often the model asset and curated scenario tables, while the fragile part is the copied orchestration layer.
