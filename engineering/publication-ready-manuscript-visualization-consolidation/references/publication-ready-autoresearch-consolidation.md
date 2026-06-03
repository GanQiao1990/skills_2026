# Archived skill: publication-ready-autoresearch-consolidation

Original path: `writing/publication-ready-autoresearch-consolidation`

---

---
name: publication-ready-autoresearch-consolidation
description: >
  Consolidate a computational biology autoresearch repository into a publication-ready package.
  Use when the task involves manuscript cleanup, figure canonicalization, smoothing/validating
  simulation artifacts, or reconciling multiple reports into one submission-grade narrative.
---

# Publication-Ready Autoresearch Consolidation

## What this skill does

Use this skill when a project has multiple manuscript drafts, multiple figure families,
optimization/simulation outputs, and a risk that discrete solver artifacts are being mistaken
for biological discontinuities. The goal is to produce one canonical story that is:

- internally consistent,
- reproducible,
- publication-oriented,
- and explicit about what is model output versus biological interpretation.

## Core workflow

### 1) Establish evidence and assumptions first
- Write current assumptions and evidence to `DEBUG.md` before making substantive changes.
- Record:
  - canonical manuscript candidates,
  - canonical figure families,
  - known runtime bugs,
  - suspect discontinuities,
  - smoke-test results.
- Treat `DEBUG.md` as the live evidence chain for the investigation.

### 2) Identify the canonical artifacts
Prefer one manuscript draft and one figure family.

Typical pattern:
- main manuscript: `PAPER_SUBMISSION_DRAFT.md` or `AUTORESEARCH_PAPER.md`
- supplement/report: `AUTORESEARCH_COMPLETE_PAPER_REPORT.md` or `GRADIENT_AUTORESEARCH_PAPER_REPORT.md`
- canonical figures: prefer the most publication-oriented set, often an `enhanced` directory

Do not mix legacy and enhanced figures in one paper unless the text explicitly says the
figures come from different export passes.

### 3) Distinguish continuity from visualization artifacts
If a curve shows abrupt jumps:
- first suspect discrete switching logic, binning artifacts, or plotting artifacts,
- not biology.

For partial dependence / marginal sensitivity panels:
- they are **aggregated marginal summaries**, not time trajectories,
- sharp bends may be real threshold-like nonlinearities,
- jagged bin-to-bin jumps usually indicate sparse support or coarse binning.

Preferred fixes:
- increase bin density,
- interpolate onto a denser axis,
- apply light smoothing only for readability,
- keep raw binned points visible,
- update the caption so readers know what they are seeing.

### 4) Validate the simulator before rewriting the manuscript
Before final manuscript edits, run smoke tests on the core simulator and confirm:
- the code executes cleanly,
- the transition behavior is continuous where intended,
- summary outputs are plausible,
- no scope/name errors remain,
- the output file contains the expected columns and row count.

If needed, revise the simulator so hard switches become smooth transition windows.

### 5) Rewrite the manuscript around the corrected interpretation
When the model is continuous but discrete internally:
- say “finite transition window” or “smooth ramp” instead of “instantaneous jump”,
- separate marginal sensitivity from dynamics,
- avoid overclaiming physical continuity if the solver is still time-discrete,
- frame virtual-vs-experimental gaps as model limitations, not biological paradoxes.

### 6) Make the figure map explicit
Create a figure-to-section table with exact paths.
Recommended format:
- order
- figure name
- exact path
- role in manuscript

Also include a short note:
- which figure family is canonical,
- which family is legacy/reference-only,
- which benchmark numbers must remain identical across manuscript and supplement.

### 7) Keep the publication workflow simple
A good publication workflow usually includes:
1. source logs,
2. validated simulation/analysis code,
3. canonical figures,
4. manuscript draft,
5. supplement/report,
6. QC checklist.

## Practical checks

### For Figure 4 / partial dependence panels
Ask:
- Is this a marginal summary or a trajectory?
- Are there enough bins/samples in each region?
- Does the curve look jagged because of sparse support?
- Do we need a caption sentence clarifying threshold-like behavior?

### For simulation discontinuities
Ask:
- Is there a hard stage switch?
- Is there a discontinuous parameter update at switch time?
- Is the plot connecting discontinuous states without explaining them?
- Does a transition window fix the artifact?

### For manuscript consistency
Check:
- same benchmark values everywhere,
- same figure numbering everywhere,
- same terminology for the same mechanism,
- no conflicting claims between abstract, results, and supplement.

## Common pitfalls
- Treating a binned partial dependence plot like a process curve.
- Leaving multiple competing manuscript drafts unresolved.
- Mixing legacy and enhanced figures without explanation.
- Changing the simulator but not the caption text.
- Claiming biological continuity when the model still uses a hard switch.
- Forgetting to update `DEBUG.md` after each substantive finding.

## Output standard
When finishing the task, the repository should contain:
- one obvious manuscript draft,
- one canonical figure set,
- a figure-to-section map with exact paths,
- updated captions/sections that explain marginal sensitivity correctly,
- and a DEBUG log documenting the reasoning trail.
