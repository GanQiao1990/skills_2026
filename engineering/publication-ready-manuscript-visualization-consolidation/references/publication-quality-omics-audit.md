# Archived skill: publication-quality-omics-audit

Original path: `engineering/publication-quality-omics-audit`

---

---
name: publication-quality-omics-audit
description: Audit and repair multi-omics analysis repos so code, manuscript, README, and figures stay numerically and logically aligned with generated artifacts.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [engineering, documentation, scientific-writing]
---

# Publication-Quality Omics Repo Audit

Use this skill when a user asks to make a multi-omics / bioinformatics project publication-ready, or when the repo contains a manuscript, README, figures, and analysis scripts that must agree with each other.

## When to use

Use this skill when the task involves one or more of:
- aligning manuscript claims with generated data files and result tables
- fixing stale counts / percentages / sample sizes in README or paper drafts
- repairing analysis logic that causes report numbers and artifacts to diverge
- improving figures so the visual title, annotation, and data summary match the current results
- preparing a repo for journal submission or a polished project report

## Parallel code review + batch fix execution

When the repo has 10+ scripts and the user wants a full review-and-fix cycle:

### A) Parallel review with delegate_task
Split scripts into 3 groups by language/type and dispatch parallel subagents:
```python
delegate_task(
    role="orchestrator",
    tasks=[
        {"goal": "Review Python scripts [1-5] for bugs, style, scientific correctness", "toolsets": ["file", "terminal"]},
        {"goal": "Review Python scripts [6-11] for bugs, style, scientific correctness", "toolsets": ["file", "terminal"]},
        {"goal": "Review R scripts for bugs, style, scientific correctness", "toolsets": ["file", "terminal"]},
    ]
)
```
Each subagent returns a structured summary with severity-ranked issues.

### B) Prioritized batch fix execution
Organize all findings into a todo list with priority tiers:
- **P0 (Critical)**: Crash bugs, scientific mislabeling, data corruption
- **P1 (Important)**: Missing retry logic, bare exception swallowing, hardcoded paths, manuscript number mismatches
- **P2 (Quality)**: Unused imports, memory leaks, missing close() calls

Execute fixes in order, verifying syntax after each batch:
```python
terminal("python3 -c \"import ast; ast.parse(open('file.py').read()); print('OK')\"")
terminal("Rscript -e \"parse('file.R')\"")
```

### C) Cross-cutting fix patterns
When a fix applies to many files (e.g., adding `plt.close(fig)` to all visualization scripts):
- Modify the shared config/utility module (e.g., `lib/config.py`) instead of patching each file individually
- This automatically applies to all scripts that import the shared module

## Core workflow

### 1) Establish the canonical artifacts
Identify the files that are the source of truth for claims:
- `data/` tables for derived candidate lists and ranks
- `results/` summary JSON/CSV files for final counts and concordance
- `figures/` for exported plots
- pipeline logs / health reports for run status

Treat these as the authoritative reference before editing prose.

### 2) Record assumptions and evidence in DEBUG.md
Before making changes, add a short audit note to `DEBUG.md` with:
- the request
- key assumptions
- the artifact(s) used as evidence
- any known mismatches discovered during the audit

This keeps the reasoning chain visible for later reviewers.

### 3) Search for stale claims
Search the repo for numbers and phrases that should match the current artifacts:
- candidate counts
- overlap counts
- concordance percentages
- sample sizes
- figure labels/titles
- “high-confidence”, “top genes”, “validated”, or other result-specific claims

Update the active manuscript/README first; keep archival versions untouched unless explicitly requested.

### 4) Fix logic before polishing prose
If a mismatch originates in code, repair the source script rather than only editing text.
Common fixes include:
- deduplicating overlaps before computing concordance
- using missing-safe means instead of naive averages
- excluding unclassified rows before summary statistics
- computing percentages from the same denominator used in the manuscript
- making figure annotations reflect the exact statistic reported in the text

### 5) Keep the story aligned with the evidence
When the evidence is exploratory rather than definitive:
- describe the result as exploratory / partial / directionally asymmetric
- avoid wording that implies statistical validation if the overlap test is not significant
- keep language consistent across abstract, results, discussion, and conclusion

### 6) Update visualizations at the source
Improve figures in the plotting script rather than editing exported images directly.
Prioritize:
- clearer plot titles
- on-figure summaries of the key statistic
- readable label placement
- consistent color semantics
- annotations that use the same denominator and counts as the manuscript

### 7) Verify the full chain
After editing, verify that the repo is internally consistent:
- search for stale counts and outdated percentages
- run syntax checks on edited Python/R files where possible
- confirm the manuscript/README now reference the same canonical values as the result tables
- confirm the figure scripts emit labels and summaries matching the written claims

## Practical heuristics

### If the manuscript says X but the artifact says Y
- change the manuscript to Y if the artifact is the final source of truth
- if Y is unexpected, inspect the code path that generated the artifact
- avoid “fixing” the artifact by editing exported files unless that artifact is actually wrong

### If there are multiple manuscript versions
- update only the active version the user is working from
- leave archived versions alone unless the user explicitly requests a full historical cleanup

### If a percentage changed after deduplication
- check the denominator carefully
- state whether the rate is based on raw rows, unique genes, or deduplicated overlaps
- ensure the same denominator is used in code, tables, figure annotations, and prose

## Verification checklist

- [ ] DEBUG.md records assumptions and evidence
- [ ] Manuscript matches current artifact counts
- [ ] README matches current artifact counts
- [ ] Figures and captions match current artifact counts
- [ ] Source scripts compute the same statistics described in prose
- [ ] Search results show no stale claims in the active docs
- [ ] Edited scripts pass syntax checks (`ast.parse` for Python, `parse()` for R)
- [ ] Full pipeline re-run completes without errors
- [ ] Health report JSON shows `overall_status: success`

## Common pitfalls

- old counts surviving in archived manuscript versions
- percentages that change after deduplication but are not updated everywhere
- exploratory overlaps being framed as validation
- plotting scripts whose visual title or annotation still reflects an old statistic
- changing only prose when the real issue is code logic
- **Scientific transform mislabeling**: `logit(x/(1+x)) = ln(x)`, so `logit(|β|/(1+|β|)) * sign(β)` is actually a signed log, not a logit. Always verify the mathematical identity of transforms before labeling axes.
- **Stouffer z-sign bias**: `z_from_p(p, 1)` always produces positive z; pass `sign(beta)` when direction is known
- **R undefined variable crash**: code outside an `if` block referencing a variable created inside it (e.g., `volcano_df`)
- **GSEA threshold confusion**: integer-valued `sigcount` with threshold 1.5 is effectively `≥2`, not "relaxed to 1.5"

## Pipeline re-run verification

After executing fixes, re-run the full pipeline to verify end-to-end correctness:
```bash
cd $PROJECT_ROOT && GLOBAL_RANDOM_SEED=42 RUN_PWAS_STRATEGY=1 python3 scripts/run_pipeline.py 2>&1
```
Monitor progress by checking `results/` and `figures/` timestamps:
```bash
ls -lt results/ | head -5; ls -lt figures/ | head -5
```
For long-running steps (e.g., XGBoost stability with 3 seeds), check process status:
```bash
ps aux | grep -E "run_pipeline|python3.*scripts" | grep -v grep
```

## Output style

When using this workflow, report:
- what the canonical artifacts are
- which claims were updated
- which logic changes were made in source scripts
- what verification passed
- any remaining historical files that still contain older numbers

