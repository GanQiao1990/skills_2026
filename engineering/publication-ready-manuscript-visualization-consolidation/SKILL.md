---
name: publication-ready-manuscript-visualization-consolidation
description: Turn a simulation-heavy research repository with multiple drafts, figures, and reports into a publication-ready package by selecting canonical artifacts, reconciling numbers, documenting the visualization pipeline, and keeping a live DEBUG log of assumptions and evidence.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [engineering, scientific-writing, scientific-visualization, reproducibility, publication]
---

# Publication-Ready Manuscript & Visualization Consolidation

Use this skill when a research repo has:
- multiple manuscript/report drafts
- multiple figure sets or iterations
- simulation logs or analysis outputs that need to be packaged for publication
- inconsistent benchmark values, filenames, or narrative versions

This skill is designed for the common situation where the work is already mostly done, but the repo needs to be turned into a coherent, reviewable, publication-ready package.

## What success looks like

- One canonical manuscript draft is clearly identified
- One canonical figure set is clearly identified
- Older drafts are labeled as supporting material, not competing sources of truth
- Benchmark numbers and claims match across README, manuscript, reports, and figures
- A reproducible pipeline exists from raw outputs to publication figures
- A DEBUG log records assumptions, evidence, and remaining risks

## Core workflow

### 1) Inspect first, do not guess

Before editing anything:
- enumerate the top-level docs, scripts, results, and figures
- identify which files are generated outputs vs source files
- locate the entry points that produce the current figures and manuscript text
- check for old versions that may conflict with newer ones

Evidence to collect:
- existing figure directories
- manuscript/report files
- result logs and best-configuration JSON
- README / run scripts / requirements
- any external paths the pipeline depends on

### 2) Create or update `DEBUG.md`

Maintain a live DEBUG log while investigating.

Include three sections:
- **Current assumptions** — what you think is true but have not yet verified
- **Evidence collected** — file paths, counts, outputs, syntax checks, command results
- **Open questions / remaining risks** — what still needs to be resolved

Keep it factual and compact. Update it when your understanding changes.

### 3) Choose a canonical narrative

Pick one manuscript/report as the source of truth and one figure family as the canonical set.

Rules:
- if two drafts disagree, do not merge them blindly
- if a newer draft supersedes an older one, label the older one as background or supporting material
- if numbers differ, identify the authoritative result log and use that consistently
- if multiple figure naming schemes exist, pick one and map the others to it explicitly

Create a short mapping table:
- canonical manuscript
- canonical figures
- supporting reports
- legacy drafts
- authoritative result logs

### 4) Reconcile numbers and claims

Cross-check every key benchmark across the repo:
- simulation count
- best objective / titer / yield / other headline metric
- experimental benchmark values
- dataset version / run identifier
- parameter ranges that appear in Methods and figures

If a value differs across files:
- trace it back to the log or script that produced it
- choose the version supported by the most direct evidence
- update the manuscript, README, and figure narratives to match

### 5) Make the visualization pipeline explicit

Add a dedicated process document that explains:
- source data
- transformation steps
- figure generation order
- QC checks
- export formats
- manuscript figure placement

The document should answer:
- where the numbers come from
- which code generates the figures
- how to rerun the pipeline
- how to keep the manuscript and figures synchronized

If helpful, include a Mermaid flowchart in Markdown to show the publication pipeline.

### 5.1 Volcano plot improvement pattern

When the user says a volcano plot is still not improved after an initial pass, do a second round focused on readability rather than aesthetics:
- keep the scientific encoding unchanged
- move the legend outside the data region
- reduce point size / alpha slightly
- label only top hits plus a small anchor set
- add collision avoidance if available (`adjustText`, `ggrepel`, or equivalent)
- prefer editing the source plotting script over patching the exported image
- regenerate the figure and verify visually with a screenshot / vision check

This pattern is especially useful when the first attempt is better but the user still perceives the figure as crowded or hard to read.
### 6) Verify code before finalizing docs

Run lightweight checks on the main scripts:
- syntax / import checks
- smoke tests for the main pipeline entry points
- existence checks for expected logs and outputs
- confirmation that the README instructions reflect the current workflow

If a runtime bug is found during inspection, fix the root cause rather than only patching the narrative.

### 7) Preserve the archive, reduce confusion

Do not delete older drafts unless explicitly asked.
Instead:
- move them into a supporting / legacy role in the docs
- explain which file should be read first
- make it obvious which outputs are authoritative

## Good deliverables

A publication-ready repo often benefits from these artifacts:
- `MANUSCRIPT_AND_VISUALIZATION_PROCESS.md`
- a canonical manuscript draft
- a supplementary visualization report
- a reproducibility / runbook section in README
- an updated DEBUG log
- a concise figure-to-section map
- for checklist-heavy judging, a package-local `EVIDENCE_MAP.md` crosswalking requirements to exact files and manuscript line locations (see `references/checklist-evidence-crosswalk.md`)
- when the user asks for a report "based on ./" or the current repo, a project-root markdown report grounded only in local artifacts plus a small `publication_assets/` figure bundle

### Repository-grounded academic report synthesis

Use this pattern when the user asks for a publication-quality report or manuscript "based on ./", "based on this folder", or otherwise expects the current repository to be the evidence base.

Workflow:
1. Treat the current working directory as the default evidence boundary unless the user names a different path.
2. Identify canonical sources before drafting: input configs, run scripts, output directories, result CSV/JSON tables, existing reports, and existing figure folders.
3. Reuse existing analysis figures when they already match the data and are publication-usable; do not regenerate plots unnecessarily.
4. Add synthesis visuals when they materially improve the package. Default to a compact set, but if the user explicitly requests a larger publication figure family (for example 6–8 figures), override the minimalist default and build a coherent figure suite from package-local canonical data plus clearly labeled workflow schematics.
5. For larger figure suites, create a package-local `canonical_data/` directory containing the exact CSV/JSON/workflow files used by the figure generator, and point the manuscript to figure files under `figures/` rather than to external or repo-fragile paths.
6. Write the main report in polished markdown in the project root or package root, with journal-style sectioning and figure callouts.
7. Explicitly distinguish executed workflow, documented design specifications, downstream screening, and true experimental validation. Do not let a computational repo narrative drift into unsupported wet-lab claims.
8. Create a short `MANUSCRIPT_AND_VISUALIZATION_PROCESS.md` or equivalent package docs mapping canonical files, figures, and reproducibility entry points so future sessions know what is authoritative.
9. Before finalizing, re-audit any headline numerical claims directly from the canonical outputs instead of trusting earlier notes or draft text. If a package-local re-parse contradicts an earlier manuscript number (for example observed sequence length), update the manuscript and figure captions to the re-audited value and document the provenance change.
10. If the repository mixes an experimentally validated benchmark or chassis, a mechanistic simulation layer, and a broader calibrated/autoresearch layer, do not force them into one apparent quantitative scale. Create a package-local submission bundle that explicitly separates these evidence tiers, states what each layer can and cannot support, and anchors the manuscript on the experimentally validated chassis or benchmark when the user says that is the real ground truth.
11. Audit the generating code for artificial ceilings, clipping, or other hard-coded output bounds before treating a reported maximum as an unconstrained optimum. If a script uses constructs like `min(max_titer, simulated_value)`, downgrade the manuscript claim from "best achievable" to a calibrated ceiling / prioritization output, and record the exact code path in the package docs or `EVIDENCE_MAP.md`.
12. When the repository already encodes a named validated chassis in code or configuration, elevate that exact chassis name into the manuscript and figure narrative and demote legacy abstract labels to compatibility-only status. Reviewers should see the same anchor strain in code, manuscript, captions, and package docs.
13. For checklist-driven or judge-facing deliverables, include a reviewer-facing `EVIDENCE_MAP.md` that points to the exact package files and manuscript locations satisfying structure, figure, conversion, and provenance requirements.
14. If the user asks for bilingual publication deliverables, create parallel authoritative Markdown sources (for example English and Chinese), keep the same evidence boundary and limitations statement in both languages, and generate separate DOCX files from each Markdown source.
12. For checklist-driven bilingual manuscript packages, make the package self-verifying inside the manuscripts themselves: include an explicit Keywords/关键词 block in both language versions, and ensure the body text explicitly calls out Figure 1..N / 图 1..N in order rather than relying only on captions or image placement.
13. When the Markdown-to-DOCX step is part of the judged deliverable, make the converter style both English and Chinese caption patterns (`Figure n.`, `Table n.`, `图 n.`, `表 n.`) and common front-matter metadata lines (`Author:` / `Correspondence:` / `Document type:` and `作者：` / `通讯信息：` / `文档类型：`). After any final manuscript edits, regenerate the DOCX instead of assuming the previous render is still valid.
14. If the user asks which candidate should go to wet-lab first, add an explicit prioritization subsection that recommends a Tier 1 primary construct, Tier 2 backup, and optionally a Tier 3 orthogonal comparator. Phrase this as a cost/time-minimizing experimental recommendation under uncertainty, grounded in accessible computational evidence such as aggregate rank, maximum mechanistic signal, and balanced subsection support — never as proof of experimentally validated superiority.
15. For final verification of judged manuscript packages, do not stop at file existence. Re-open the DOCX (for example with `python-docx` and/or ZIP media inspection), verify embedded image count, verify caption paragraphs survived conversion, and confirm the final enzyme recommendation and figure order remain aligned across both language versions.
16. If the user explicitly asks to **redo the visualizations with Python**, do not treat the existing figures as sufficient just because they already pass a checklist. Regenerate the figure family from the package-local canonical data with a Python script and prefer decision-oriented layouts over dense analysis-output defaults: (a) convert cluttered ranked bar charts into cleaner multi-panel ranking views when several metrics matter, (b) replace overly busy violin+annotation combinations with simpler boxplot/jitter or similarly interpretable summaries, (c) add subtle cell separators and move legends outside the data region for dense heatmaps, and (d) preserve the manuscript conclusions unless the underlying audited data change. After the redesign, regenerate the DOCX again so the delivered Word files actually embed the new figures.
17. When auditing repository-generated figures, verify that any effect-size transform used for display preserves left/right biological direction. A common publication blocker is `sign(beta) * ln(|beta|)`, which flips sign whenever `|beta| < 1` and silently places many positive effects on the negative side of a volcano-style plot. Prefer raw `beta` or a monotone direction-preserving compression such as `sign(beta) * log1p(|beta|)`, and update the axis label to match the real transform.
18. If the manuscript contains quantitative cross-omics correlation claims, pathway scores, or “integrated score” statements that do not have an exported table/script/result artifact in the repository, do not leave them as hard quantitative findings. Downgrade them to a qualitative synthesis, explicitly align the prose to the package evidence boundary, and avoid invented precision in captions.
19. Distinguish carefully between `unique genes/proteins` and `directional mappings` in therapeutic overlap analyses. If a package reports 29 unique overlaps but 30 directional mappings because one target appears in two directional contexts, the manuscript, README, captions, and summary JSON must all state which denominator is being used.
20. For simple Markdown→DOCX conversion pipelines, verify that markdown image syntax is actually parsed and embedded in the Word output. If the local converter is custom/lightweight, patch it to handle image nodes, point its defaults to the canonical manuscript, regenerate the DOCX, and then verify embedded image count from the DOCX archive instead of assuming the export was faithful.
21. For publication-facing pathway/network figures, do not rescue weak or failing KEGG / clusterProfiler branches by widening thresholds (for example `pvalueCutoff` 0.50→0.95, `p.adjust < 0.30`, or `qvalueCutoff = 0.8`). Keep confirmatory figures at adjusted P/FDR < 0.05. If live KEGG access is unstable, prefer cached enrichment tables plus a single stable igraph CNET and record the fallback in a diagnostics JSON so the manuscript can describe the evidence boundary honestly.
22. When a mechanism map or feature-bridge figure is vulnerable to the critique that it is hand-curated, rebuild it from packaged result tables instead of narrative constants. Typical inputs are model summary CSVs, SHAP audit JSON/CSVs, marker-prioritization tables, annotated PWAS hits, and therapeutic-overlap summaries. The caption should call such a panel a data-driven synthesis grounded in packaged results, not an unconstrained conceptual schematic.
23. If a volcano plot still reads as crowded after a first pass and collision-avoidance libraries are unavailable, do a source-level readability pass anyway: reduce the label set to anchor genes plus a few top hits, use boxed labels and leader lines, apply simple deterministic offset/collision heuristics, and move the legend fully outside the plotting region. Do not leave readability as-is just because `adjustText`/`ggrepel` is missing.
24. When a repository mixes an experimentally validated benchmark with one or more computational layers that operate on different numerical scales, do not force them into one headline-performance story. Promote the experimentally validated strain or benchmark to the manuscript anchor, then explicitly separate the computational layers by role: for example, a mechanistic simulation layer for pathway interpretation and a calibrated high-throughput search layer for prioritization. If a virtual layer is ceiling-limited, hand-tuned, or otherwise calibration-dependent, present it as hypothesis generation / ranking support rather than as an experimentally equivalent forecast.
25. If the repo contains multiple conflicting numbers because different pipelines use different scaling assumptions, create a package-local `canonical_data/package_metrics.json` or equivalent summary table that records the audited headline values for each evidence layer (experimental anchor, mechanistic baseline, mechanistic optimized result, calibrated virtual best, simulation count). Use that file as the manuscript-facing source of truth for the final package.
26. For supervisor-style publication rescue of a simulation-heavy repo, produce a handoff-ready `publication_package/` (or similarly named package-local directory) containing the canonical manuscript, figure legends, evidence map, process note, package README, and package-local copies of the exact figures/data used by the final narrative. This prevents the final paper from depending on root-level legacy drafts that still contain stale numbers.
27. When the user wants a true submission bundle rather than another draft, create package-level submission-control files (`SUBMISSION_MANIFEST.md`, `FINAL_SUBMISSION_CHECKLIST.md`, `JOURNAL_PACKAGE_MAP.md`, plus title page / cover letter / figure legends as needed) and explicitly demote confusing root-level manuscript-like files to archive/supporting status. State the single canonical manuscript starting point inside the package docs, not only in chat. See `references/final-submission-bundle-and-archive-demotion.md`.

What to verify:
- every headline number in the report appears in inspected local files
- figure files referenced in the manuscript exist at the stated paths
- for expanded figure families (6–8 figures or more), a package-local `canonical_data/` directory exists and the figure generator reads from it
- if the manuscript claims a sequence length, runtime summary, or output count, those values were re-audited from the current package-local evidence rather than inherited from a stale draft
- if bilingual deliverables exist, both language versions preserve the same evidence boundary and do not become stronger claims in translation
- if a wet-lab recommendation exists, it is explicitly framed as prioritization under uncertainty and cites the ranking logic used
- the report states limitations when structure-wide QC or experiments are not yet present
- the output package is easy to hand off: canonical markdown source(s), one figure directory, one conversion script, and reviewer-facing reproducibility docs

## Multi-language scientific pipeline review patterns

When reviewing a pipeline with both Python and R scripts (common in bioinformatics), check these additional patterns:

### Scientific label correctness
- Transform mislabeling is common: e.g., `logit(|β|/(1+|β|))` simplifies to `ln(|β|)` — verify mathematical claims in axis labels and variable names
- When renaming a transform, update ALL references: variable names, axis labels, plot titles, filenames, and manuscript descriptions

### Cross-language consistency checks
- If Python and R scripts both produce the same analysis (e.g., CNET plots from different sources), verify they use consistent thresholds and data
- Shared config modules (e.g., `lib/config.py` + `lib/palette.R`) should define the same color palette and paths
- Check that R scripts have fallback definitions for shared variables: `if (!exists("PALETTE")) PALETTE <- c(...)`

### Common bug patterns in scientific Python/R scripts
| Pattern | Where | Fix |
|---------|-------|-----|
| Bare `except Exception: pass` | Data loading | Replace with `except Exception as e: print(f"Warning: {e}")` |
| Hardcoded `/home/user/...` paths | `main()` functions | Use `Path(config.PROJECT_ROOT).parent / "relative"` or env vars |
| No retry on API calls | Enrichr, KEGG, etc. | Add `_retry_request()` with exponential backoff |
| `np.random.seed()` (legacy) | Visualization jitter | Use `np.random.default_rng(seed)` |
| `np.resize()` silent truncation | SHAP importance alignment | Raise `ValueError` on length mismatch |
| Missing `plt.close(fig)` | All visualization scripts | Add to shared `save_fig()` function |
| Unused imports | All scripts | Clean `urllib.parse`, `path_effects`, etc. |
| `foldChange` name mismatch after `setReadable()` | clusterProfiler CNET | Rebuild named vector with SYMBOL keys after `setReadable()` |
| Hardcoded `GeneRatio = "Count/396"` | Manual enrichResult objects | Compute from data: `paste0(Count, "/", nrow(df))` |
| Fake `BgRatio = "100/10000"` | Manual enrichResult objects | Compute from actual gene universe size |
| Double `save_fig()` on same figure | CNS-style variant scripts | Second call operates on closed figure; remove or create new fig |
| `volcano_df` undefined crash | R conditional blocks | Wrap downstream code in same `if` block or add guard |

### Manuscript internal consistency checklist
After any number change, search the ENTIRE manuscript for ALL instances of the old value:
```bash
grep -n "396\|400\|0\.75\|17/30" manuscript/*.md
```
Check these specific cross-references:
- Abstract protein counts ↔ §2.1 ↔ §2.2 ↔ Discussion
- Directional consistency threshold ↔ Methods section
- Semaglutide quadrant counts (text vs figure caption vs JSON)
- SHAP values in §2.3 (single run) vs §2.4 (stability mean) — explain the difference
- Table/figure references (e.g., "Table 1" exists but no table provided)
- Reference formatting (e.g., "et al." not "al.")

### Pipeline re-execution verification
After applying fixes, always re-run the full pipeline to verify:
1. All steps complete without errors
2. Generated figures update correctly
3. No cascading failures from changed variable names or thresholds
4. Check `results/run_health_report_*.json` for step-by-step status
5. Spot-check key output files (e.g., `semaglutide_concordance_summary.json`) match expected values

## Common pitfalls

- Mixing numbers from different runs in the same manuscript
- Treating multiple draft reports as equally authoritative
- Leaving stale filenames in figure captions
- Describing a figure set that no longer matches the code
- Claiming reproducibility without identifying the exact input log or script
- Making edits to prose without checking whether the underlying script changed
- Fixing numbers in the abstract but missing them in §2.2 or the Discussion
- Renaming a variable in Python but not in the corresponding R script
- Running `config.save_fig(fig, "name")` twice on the same figure after adding `plt.close(fig)`
- Accepting `p < 0.50` as a GSEA threshold without documenting the rationale

## Verification checklist

Before saying the project is publication-ready, verify:
- [ ] canonical manuscript chosen
- [ ] canonical figure set chosen
- [ ] benchmark numbers consistent across docs
- [ ] README matches actual entry points
- [ ] DEBUG log updated with evidence
- [ ] pipeline document exists and is readable
- [ ] code syntax / smoke checks passed
- [ ] legacy drafts are clearly labeled

## Class-level umbrella scope

This skill is the umbrella for publication-ready computational biology / scientific project consolidation. It absorbs narrower workflows that previously existed as separate skills: autoresearch manuscript consolidation, simulation-artifact smoothing, computational-project canonicalization, manuscript+figure revision, and multi-omics repo audit. Use the labeled subsections below instead of searching for one-session skills.

### Subsection: autoresearch and simulation-heavy project consolidation
Use when the repo has Bayesian optimization/autoresearch outputs, multiple manuscript drafts, multiple figure generations, and possible discontinuities in simulated trajectories. First establish canonical artifacts, then debug trajectory artifacts before rewriting prose. If the model should be continuous, inspect hard stage switches, clipping, and transition weights; prefer a finite transition window and expose it in output tables. Keep `DEBUG.md` as the evidence chain.

### Subsection: manuscript + figure script co-revision
Use when prose and figure-generating scripts must change together. Trace the manuscript-facing figure filename to the script that writes it, reduce label clutter at the source, use scientifically honest transforms, and verify the edited script parses/runs. For volcano plots, limit labels to top hits plus anchors, move legends outside data regions, and use collision avoidance where possible.

### Subsection: multi-omics repository audit
Use when README, manuscript, figures, and generated omics artifacts disagree. Treat result JSON/CSV tables and health reports as the source of truth, fix logic before prose when mismatches originate in code, and avoid framing exploratory overlaps as validation. Common audit issues include stale counts, transform mislabeling, missing sign in Stouffer z calculations, R variables referenced outside their creating block, and inconsistent thresholds across Python/R scripts.

### Subsection: computational project canonicalization
Use when a rough research repo needs one canonical story, one figure family, and one verified code path. Create a figure-to-section map, label older drafts as legacy/supporting, and cross-check every headline number against logs/results before claiming publication readiness.

### Demoted support references
Archived narrow skills were demoted into this umbrella's `references/` directory:
- `references/publication-ready-autoresearch-workflow.md`
- `references/publication-ready-autoresearch-consolidation.md`
- `references/publication-ready-computational-project-consolidation.md`
- `references/publication-ready-scientific-manuscript-figure-revision.md`
- `references/publication-quality-omics-audit.md`
- `references/repository-grounded-eight-figure-report-pattern.md` — package pattern for larger publication figure suites, `canonical_data/`, evidence maps, and final number re-audits
- `references/bilingual-manuscript-and-wetlab-prioritization.md` — how to extend a repository-grounded package into English/Chinese manuscripts plus an uncertainty-aware wet-lab candidate recommendation
- `references/final-submission-bundle-and-archive-demotion.md` — how to lock one canonical manuscript, add submission-control files, and demote competing root-level drafts to archival status

## When to use this skill

Use this skill whenever you are asked to:
- turn a research repo into a submission package
- reconcile competing manuscript drafts
- align figures with a paper narrative
- prepare a computational biology project for publication
- document the path from raw simulation output to final figures and manuscript
- review and fix a multi-script scientific pipeline (Python + R) for correctness
- verify manuscript numbers match actual pipeline outputs
- fix scientific mislabeling in transforms, axis labels, or variable names
- re-run a pipeline after fixes to verify no cascading failures
