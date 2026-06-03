# Staged multi-model binder pipeline: reusable outline + checkpoints

This reference is a reusable outline for turning a messy method dump into a clean method-positioning note when the work is a **staged multi-model binder design pipeline** (e.g., ProteinHunter  HalluDesign  Chai-1).

## A. Canonical narrative spine (why it is fast + why it is accurate)

1) **Speed comes from scheduling**
- Put cheap/high-throughput exploration first.
- Apply expensive refinement only to a compressed candidate set.
- Avoid all-candidates-on-the-most-expensive-model.

2) **Accuracy comes from orthogonality + multi-signal scoring**
- Avoid single-model self-consistency (design and judge by the same model).
- Require agreement across at least one independent model (orthogonal audit).
- Add non-DL checks (geometry/physics) and task-intent checks.

## B. Minimal stage diagram template (keep user numbering)

```text
Stage 0: Initialization
  
Stage 1: Generator (fast exploration)
  
Stage 2: Seed selection (Top-N by confidence)
  
Stage 3: Refinement (sequencestructure closure)
  
Stage 4: Orthogonal validation
  
Stage 5: Metric extraction (multi-signal)
  
Stage 6: Composite score + Top-K
```

## C. Metrics table template (4-signal example)

| Signal type | Metric | What it checks | Typical failure it blocks |
|---|---|---|---|
| Interface confidence | ipTM | assembly/interface plausibility | doesnt bind |
| Fold quality | pLDDT | binder fold stability proxy | binder collapses |
| Physics/geometry | clash penalty | steric feasibility | atoms interpenetrate |
| Task intent | pocket coverage | binds correct pocket/contact residues | binds wrong site |

## D. Comparison section: prefer one table over long prose

- Make 1 table with rows = methods (BindCraft / RFdiffusion / single-model / staged pipeline).
- Columns = generation mechanism, refinement, validation independence, physics checks, task-intent checks, scheduling/reproducibility.

## E. Quality/legibility checkpoints

- Preserve user-provided stage numbering, funnel counts, and bracketed internal tokens (e.g., `[1c][6g]`).
- Do not introduce new model names unless the repo/docs explicitly do.
- Verify output markdown is UTF-8 plain text (no hidden control characters).
