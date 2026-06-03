# Archived skill: publication-ready-autoresearch-workflow

Original path: `engineering/publication-ready-autoresearch-workflow`

---

---
name: publication-ready-autoresearch-workflow
description: Reusable workflow for turning simulation-heavy research repos into a publication-ready package by consolidating manuscript drafts, aligning figure narratives, and smoothing discontinuous process trajectories when the underlying model should be continuous.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [engineering, scientific-writing, scientific-visualization, debugging, publication, workflow]
---

# Publication-Ready Autoresearch Workflow

Use this skill when a repository has multiple manuscript drafts, multiple figure pipelines, and simulation outputs that must be turned into a single publication-ready story. It is especially useful when the user asks for a manuscript + visualization process, asks to consolidate drafts, or notices abrupt jumps / discontinuities in trajectories that should be continuous.

## When to use

- Multiple markdown drafts disagree on canonical numbers, figures, or storyline
- Visualization scripts exist in more than one generation and need unification
- Simulation trajectories show abrupt jumps that look like solver or stage-switch artifacts
- The user wants the project to be publication-ready, not just technically runnable
- You need a defensible manuscript narrative that matches the actual code and outputs

## Core principle

Do not treat a discontinuity as a biological fact until you have ruled out:
1. stage-switch logic,
2. clipping / thresholding,
3. plotting artifacts,
4. discrete-time update artifacts.

If the underlying process is meant to be continuous, the model and figures should present a continuous transition window, not a hard jump.

## Workflow

### 1) Inventory the canonical artifacts
Read the repository structure and identify:
- one canonical manuscript draft,
- one canonical figure set,
- one canonical results/log directory,
- one canonical entry point for the pipeline.

Create or update a short process note in markdown so the decision is explicit.

### 2) Cross-check manuscript, figures, and logs
Compare the numbers and labels across:
- README,
- manuscript drafts,
- figure captions,
- results JSON/CSV/logs,
- supplementary reports.

If multiple drafts conflict, choose one canonical narrative and mark the others as supporting or legacy.

### 3) Diagnose discontinuities before editing prose
For abrupt jumps in a supposedly continuous bioprocess:
- inspect the simulator for hard stage transitions,
- inspect for clipped state updates or lower-bound/upper-bound clipping,
- inspect whether the plot is hiding the underlying sample density,
- run a short smoke test around the transition region,
- print a compact trajectory table with time, stage, key state variables, and any transition weights.

Form a single hypothesis, test it minimally, and only then patch.

### 4) Prefer smooth transition windows in continuous systems
If the process is physically continuous but the code uses discrete stages, introduce a finite transition window and blend:
- oxygen bounds,
- growth coupling,
- feed rates,
- regulator activity,
- any other stage-dependent controls.

Expose a transition weight column in the trajectory output so the manuscript can describe the continuous ramp explicitly.

### 5) Verify after each change
Run three checks:
- syntax check / import check,
- short smoke test around the transition,
- read the resulting table and confirm the jump is gone or justified.

Do not rewrite the manuscript until the trajectory behavior is verified.

### 6) Write the manuscript narrative last
For the final paper:
- state the biological mechanism first,
- then state what the model actually does,
- then state the figure interpretation,
- avoid claiming a hard physical jump if the process is being modeled as a smooth ramp.

Prefer a manuscript structure of:
- title / abstract,
- introduction,
- methods,
- results,
- discussion,
- supplement for algorithmic detail.

### 7) Maintain a DEBUG log
Keep a small DEBUG.md updated with:
- current assumptions,
- evidence collected,
- root-cause hypothesis,
- what was verified,
- what remains unresolved.

This is especially useful when multiple fixes are attempted and the approach changes based on smoke-test findings.

## Practical checks

### For manuscript consistency
- Same benchmark numbers everywhere
- Same figure filenames everywhere
- Same terminology for strains, regulators, and process variables
- One canonical virtual optimum / best result

### For visualization quality
- Publication-grade font sizes
- Consistent panel labels
- Consistent color logic
- PDF + PNG export
- No clipped titles or legends
- Trajectories should be smooth if the system is continuous

### For code verification
- `python -m py_compile ...` or equivalent import check
- short simulation smoke test at the transition boundary
- print and inspect the output table
- compare the before/after trajectory around the suspected jump

## Common pitfalls

- Declaring a model result to be biological when it is actually a stage-switch artifact
- Fixing prose before the trajectory bug is verified
- Mixing figures from multiple generations of the pipeline
- Keeping old drafts that contradict the canonical manuscript
- Leaving transition-state logic implicit instead of recording it in the output

## Output style

When using this workflow, be direct and evidence-based:
- say what is canonical,
- say what was verified,
- say what changed,
- say what remains uncertain.

Avoid overclaiming. If the model uses a smooth interpolation, describe it as a smooth interpolation; if it uses discrete stages, say so explicitly.
