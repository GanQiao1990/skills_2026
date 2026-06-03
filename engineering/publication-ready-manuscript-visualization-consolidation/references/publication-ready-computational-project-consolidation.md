# Archived skill: publication-ready-computational-project-consolidation

Original path: `scientific-writing/publication-ready-computational-project-consolidation`

---

---
name: publication-ready-computational-project-consolidation
description: >
  Use when a computational biology / synthetic biology / autoresearch repository
  needs to be brought from rough drafts to a submission-ready package. This skill
  applies when the task involves reconciling multiple manuscript drafts, figure
  sets, simulation outputs, and code paths into one canonical publication story.
---

# Publication-Ready Computational Project Consolidation

## When to use
Use this skill when the user wants to turn a research codebase into a paper-ready project, especially if the repository contains:
- multiple manuscript/report drafts with conflicting numbers or claims
- several figure families for the same analysis
- simulation discontinuities or other model artifacts that must be explained or fixed
- a need to maintain an auditable debug log during revision

## Core objective
Produce one canonical narrative, one canonical figure set, and one verified simulation/storyline that are mutually consistent.

## Workflow

### 1) Audit the repository before editing
- Read the main manuscript draft(s), README, methods docs, and figure/report summaries.
- Identify the code paths that generate the main claims and figures.
- Record assumptions and evidence in `DEBUG.md` before making substantive changes.

### 2) Find the canonical story
- Choose a single manuscript draft to become the source of truth.
- Choose a single figure family for the main paper and designate any others as supplementary or archive-only.
- Normalize benchmark values, sample sizes, and names across manuscript, README, and figure captions.

### 3) Check for model artifacts before writing the paper around them
- Treat abrupt jumps, hard switches, and discontinuous curves as implementation/modeling artifacts unless the biology explicitly requires a discontinuity.
- Inspect the simulation code for:
  - threshold logic
  - hard state switches
  - piecewise definitions without transition windows
  - plotting artifacts caused by interpolation or binning
- Prefer continuous or ramped transitions when the biological system should evolve smoothly.
- For partial dependence / marginal sensitivity plots, remember they are aggregated summaries rather than time trajectories. Jagged or step-like appearance can come from sparse bin support or coarse binning, so consider denser binning, interpolation, or light smoothing while still showing the raw binned support points.
- In the manuscript, explicitly distinguish:
  - true dynamic state transitions in simulation
  - threshold-like nonlinear response surfaces
  - visualization artifacts introduced by binning or sparse sampling

### 4) Validate the code path with smoke tests
- Run a small, fast simulation or generation test after each change.
- Confirm that the revised code still produces output and that the artifact is gone.
- If a bug appears, debug the smallest failing scope first, then re-run the smoke test.

### 5) Rewrite the manuscript to match the verified behavior
- Keep the scientific content aligned with the validated code, not with older draft text.
- Make the continuity assumption explicit if the model now uses a transition window.
- Remove wording that overclaims a physical discontinuity if the simulator only shows a discrete solver step.
- Keep abstract, results, and discussion consistent about the same benchmark values.

### 6) Consolidate visualization workflow
- Create or update a process document that maps figures to manuscript sections.
- Ensure each figure has:
  - a clear role in the argument
  - consistent labels and units
  - one canonical file name used in the paper
- Run visual QC for readability, benchmark consistency, and absence of artificial jumps.

### 7) Keep a publication trail
- Maintain `DEBUG.md` with:
  - current assumptions
  - evidence collected
  - bugs found and fixed
  - remaining gaps for publication readiness
- Use this trail as the basis for the final readiness report.

## Recommended checks
- One canonical manuscript draft exists.
- One canonical figure family exists.
- All reported numbers match across manuscript, README, captions, and logs.
- The simulator output is consistent with the biology being claimed.
- The paper distinguishes model output from experimental reality.
- The debug log explains what was changed and why.

## Common pitfalls
- Multiple “main” manuscripts with incompatible figures or titer values.
- Describing a modeled hard switch as if it were a biological discontinuity.
- Fixing prose before fixing a broken or discontinuous simulation.
- Letting figure filenames drift from manuscript figure references.
- Mixing legacy and enhanced figure sets without a clear hierarchy.

## Output expectation
When using this skill, return a clear publication-readiness assessment plus the concrete edits made to code, docs, manuscript, and figures.
