# Submission artifact contracts

Use this pattern when the user asks to "完善" / repair / finalize an existing job or output directory for a competition, benchmark, or deliverable-driven pipeline.

## Goal
Bring the directory to a verifiably submit-ready state instead of only inspecting it.

## Minimal workflow
1. Inspect the existing artifact set first: expected CSV/log/ZIP names, cache files, and any validator script already in the repo.
2. Read the current final artifacts before regenerating them. Confirm header/field contract, row count, and whether route or product fields match the submission spec.
3. Trace the emit path in code (`pipeline.py`, validator, packaging code) before editing outputs manually.
4. Prefer rerunning the smallest terminal stages that rebuild the final contract from cached intermediates (for example `retro` -> `route_economy` -> `emit`) instead of rerunning the whole pipeline.
5. Re-run the repository's validator after regeneration.
6. Verify the archive itself: required filenames present at ZIP root, no missing required files, and the packaged CSV matches the on-disk CSV.

## Good practice
- Treat the validator as necessary but not sufficient: also inspect the ZIP member list and the actual CSV rows.
- If the job already contains useful cache outputs, preserve them and only refresh the downstream stages needed to make the submission consistent.
- When the final CSV contract depends on route validity, verify that the last reaction product canonically matches the `mol_smiles` field.
- If a report file exists, treat it as secondary; submission readiness is determined by the declared contract files.

## Common pitfall
Do not stop after saying the directory "looks fine". For submission tasks, regenerate or revalidate the final artifacts and confirm the exact packaged contents.