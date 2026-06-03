---
name: metabolic-model-project-integration
description: Integrate, rescue, and operationalize metabolic-model repositories into executable projects. Use for COBRA/ecGEM/FBA repos that mix validated models with partially broken wrappers, dynamic layers, or orchestration scripts.
---

# Metabolic Model Project Integration

Use this skill when a user asks to integrate, clean up, or make executable a metabolic-modeling repository involving GEM/ecGEM assets, feeding-regime files, FBA pipelines, or mixed Python/R wrappers.

## When to use
- A repo contains valid COBRA-readable model assets (`.mat`, SBML, XML) plus legacy or copied wrapper scripts.
- The user wants an "executable project", not just scattered scripts.
- There is a mismatch between documented orchestration and what actually runs.
- A dynamic layer (R/Petri-net/ODE/shell pipeline) exists, but its runtime integrity is unclear.

## Core rule
Prefer verified assets over decorative wrappers.

If the model files and regime tables are real but the orchestration layer is inconsistent, build the executable project around the verified assets first. Do not present copied wrappers as runnable just because they exist in the tree.

## Workflow
1. Write assumptions and evidence to `DEBUG.md` before modifying the repo.
2. Verify the model asset directly:
   - load the `.mat` / SBML / XML model
   - run a real optimize call
   - confirm objective and target exchange reactions exist
3. Audit entrypoints before trusting them:
   - `source()` / imports must match real filenames exactly
   - required sidecar files must exist
   - variables must be defined before use
   - output paths in code must match the current repository tree
4. Separate repository layers into:
   - validated assets (models, regime tables, panels)
   - unverified wrappers (R launchers, shell pipelines, placeholder converters)
5. If the wrapper layer is broken, create a tested direct execution path first:
   - package/module layout
   - CLI entrypoint
   - explicit config
   - real output files
   - tests/smoke tests
6. Preserve the legacy dynamic layer as reference only until independently repaired.
7. Document the current truth clearly in `README.md`:
   - what is executable now
   - what remains reference-only / not yet verified

## Fermentation simulation reporting rule
When oxygen is experimentally important, record both:
- imposed oxygen bound / setpoint
- realized oxygen flux from the solution

These are not interchangeable. The first is the experimental assumption; the second is the model response.

## Output contract for an "executable project"
A successful delivery should include all of the following:
- one real entrypoint the user can run now
- dependency declaration
- tests or smoke tests with real output
- a README that distinguishes verified workflow from aspirational workflow
- concrete output files from a live run

## Common pitfalls
- Treating copied `run_*.R` or `run_*.sh` files as working without checking path integrity.
- Hiding broken dynamic layers behind optimistic README claims.
- Reporting only oxygen setpoint or only oxygen flux, which loses important experimental context.
- Declaring integration complete when only files were rearranged, not executed.

## References
- See `references/repo-integration-and-oxygen-reporting.md` for a compact playbook and pitfalls from an E. coli amino-acid production integration session.
