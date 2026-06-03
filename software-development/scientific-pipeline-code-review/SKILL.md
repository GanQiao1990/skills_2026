---
name: scientific-pipeline-code-review
description: >
  Systematic review and automated remediation of multi-script scientific analysis
  pipelines (Python + R + manuscript). Covers code bugs, scientific correctness,
  cross-file consistency, and pipeline reproducibility.
version: 1.0.0
metadata:
  hermes:
    tags: [code-review, scientific-computing, r-lang, python, pipeline, manuscript, bioinformatics]
    related_skills: [requesting-code-review, publication-ready-autoresearch-consolidation, systematic-debugging]
---

# Scientific Pipeline Code Review

End-to-end review of multi-script scientific analysis pipelines that combine Python, R, shell scripts, and academic manuscripts. Designed for bioinformatics, multi-omics, and computational biology projects where code correctness, scientific accuracy, and manuscript-data consistency all matter.

**Core principle:** In scientific pipelines, a "working" script can still produce wrong science. Review must span code quality, mathematical correctness, AND manuscript-data consistency.

## Publication-oriented causal target-indication reviews

When reviewing a big-data-to-disease, PWAS, multi-omics, or biomarker-to-target project for publication quality, distinguish three layers of evidence explicitly:

- target indication: genetically anchored, multi-model, or pharmacologic support for a candidate target
- causal-inference readiness: the project has the variant-level inputs needed for coloc/MR-style validation
- causal proof: only claim this after locus-level coloc/MR, harmonization, sensitivity checks, and endpoint-specific replication

Do not let a manuscript imply definitive causality when the available outputs are protein-level PWAS summaries, SHAP rankings, enrichment outputs, or drug-perturbation overlaps. These are strong target-indication signals, not causal proof.

For supervisor-style manuscript upgrades, use `references/publication-figure-and-upstream-provenance.md` to keep Figure 1 publication-clean and to document the upstream first data-treatment layer when preprocessing lives outside the active report repo.

For evidence grading, use `references/publication_evidence_grade_layer.md` and keep the manuscript language aligned with the grade.

## When to use

- Reviewing a scientific analysis repository before publication
- User says "review the project", "check the pipeline", "audit the code"
- Multi-script projects with Python + R + manuscript in the same repo
- Projects with pipeline orchestrators (run_pipeline.py, Snakemake, Nextflow)
- After major refactoring of analysis scripts
- When pipeline re-run produces different numbers than manuscript claims

**Skip for:** single-script tasks, pure data analysis, documentation-only review.

## Repository-Wide Review Trigger

When the user says **"review the project"**, **"audit the repo"**, or asks for a review of the current directory, treat it as a **repository-wide scientific project audit**, not just a code-style pass and not an instruction to start changing files.

In mixed scientific repos (simulation code + figures + manuscripts + generated results), the default review scope should include:

- project structure and real entrypoints (`README.md`, runners, main scripts)
- reproducibility and portability (declared deps vs actual imports, absolute paths, external sibling repos, data outside the repo)
- testing and verification gaps
- manuscript/report consistency (headline numbers, canonical figure family, duplicate drafts)
- release hygiene (debug logs, stale outputs, legacy artifacts left in the main tree)

Unless the user explicitly asks for fixes, deliver a structured audit first. Distinguish clearly between **scientifically strong but workspace-like** repos and **clean release-grade** repos.

## Workflow

### Phase 0: Survey the Project

1. **Map the structure**: List all scripts, data files, figures, results, manuscript
2. **Find the orchestrator**: Look for `run_pipeline.py`, `pipeline_config.yaml`, `Makefile`, `Snakefile`
3. **Identify data flow**: What are the inputs? What are the final outputs? What's the dependency chain?
4. **Check shared config**: Look for `lib/config.py`, `lib/palette.R`, `.env`, shared style modules

### Phase 1: Parallel Subagent Review

Use `delegate_task` with 2-3 parallel subagents, each covering different script groups:

```
Subagent 1: Python scripts (0-N) — code quality, bugs, scientific correctness
Subagent 2: R scripts — same focus
Subagent 3: Manuscript — number consistency, figure references, claims vs data
```

Each subagent should produce a structured table: | Severity | File | Line | Issue |

### Phase 2: Cross-File Consistency Check

This is the **highest-value** phase — issues that no single-file review catches:

**Repository-level consistency checks for publication-facing scientific repos:**
- Does the README quick-start actually match the packaged repository state?
- Are required dependencies declared (`requirements.txt`, `environment.yml`) for the scripts that are presented as runnable?
- Are there hard-coded absolute paths, workstation-specific interpreters, or sibling-repo dependencies that make the repo non-portable?
- Is there a clearly canonical manuscript, figure family, and result dataset, or are multiple drafts competing with conflicting headline numbers?
- Are generated results referenced in docs actually present in the repo snapshot, or are there stale references to missing artifacts?
- Does the repository contain tests or even smoke checks for the main entrypoints?

**Manuscript ↔ Data reconciliation:**
- Extract all numbers from manuscript (sample sizes, p-values, counts, percentages)
- Compare against actual data files and results JSONs
- Check abstract vs results vs discussion for internal consistency
- Verify figure references match actual figure files

**Cross-script data contract verification:**
- Does script B expect columns that script A produces?
- Are column names consistent across scripts?
- Do hardcoded constants match between scripts?
- In sourced R pipelines, check for hidden global-state contracts: helpers that read variables created by a different script (`<<-`, sourced side effects, objects assumed to exist in the caller environment) instead of taking explicit function arguments.
- Check for outer-scope variable leakage inside helpers (for example using loop variable `s` inside a function whose real argument is `carbon`). These pass syntax checks but break at runtime or silently write outputs to the wrong location.
- Verify that every runner-referenced input path actually exists in the packaged repo snapshot (ranking CSVs, reference tables, lookup TSVs, pretrained model files), not just in the author's working tree.

**Pipeline artifact verification:**
- Do expected output files exist?
- Are output file sizes reasonable (>0 bytes, not placeholders)?
- Treat suspiciously tiny exported figures as audit signals, not success. As a heuristic, clusters of debug PDFs around ~5 KB or PNGs under ~10 KB often indicate placeholder/minimal plots, failed render paths, or nearly empty panels.
- Check for black/empty placeholder figures (vision_analyze if available)

### Phase 3: Execute Fixes

Batch fixes by priority:
1. **P0 (Critical)**: Crash bugs, scientific errors, data corruption
2. **P1 (Important)**: Misleading labels, number inconsistencies, missing error handling
3. **P2 (Quality)**: Unused imports, memory leaks, style issues

**After each batch**: verify syntax (`python3 -c "import ast; ast.parse(open(f).read())"`, `Rscript -e "parse(f)"`)

### Phase 4: Re-run Pipeline

Run the full pipeline orchestrator to verify all fixes work together. Check the health report for any new failures.

---

## Common Pitfalls in Scientific Pipelines

### R-Specific Pitfalls

**1. Bioconductor namespace masking**
`clusterProfiler` exports `rename()` which masks `dplyr::rename()`. Always use explicit `dplyr::rename()` in scripts that load Bioconductor packages.

```r
# BAD: masked by clusterProfiler
df %>% rename(pvalue = `P-value`)

# GOOD: explicit namespace
df %>% dplyr::rename(pvalue = `P-value`)
```

**2. Manually constructed S4 enrichResult objects break cnetplot()**
`cnetplot()` from enrichplot requires specific internal slots that are hard to replicate manually. If you must construct enrichResult by hand, use igraph directly instead of cnetplot.

```r
# FRAGILE: manually constructed enrichResult
ego <- new("enrichResult", result = df, ...)
cnetplot(ego)  # often fails with "d should contain at least two columns"

# ROBUST: igraph-based CNET
g <- igraph::graph_from_data_frame(edges, vertices = nodes)
plot(g, layout = igraph::layout_with_fr(g))
```

**3. Shell escaping in R regex patterns**
When writing R scripts from Python (via patch/write_file), backslashes in R regex patterns get consumed. `\(` in R needs `\\(` in the source file, but Python string escaping can reduce this to `\(`.

```python
# BAD: Python consumes one escape level
patch(file, 'old', 'gsub("\\[|\\]"...)')  # writes \[ in file → R error

# GOOD: double-escape for Python→R
patch(file, 'old', 'gsub("\\\\[|\\\\]"...)')  # writes \\[ in file → R gets \[
```

**4. Pipe chain breaks**
When inserting code into an existing `%>%` pipe chain, the new code must be inside the chain, not between pipes.

```r
# BROKEN: code inserted between pipes
df %>%
  filter(x) %>%
  # compute helper value  ← BREAKS THE CHAIN
  helper <- compute()
mutate(y = helper)

# FIXED: helper computed before the chain
helper <- compute()
df %>%
  filter(x) %>%
  mutate(y = helper)
```

### Python-Specific Pitfalls

**5. Mislabeled mathematical transforms**
`logit(x/(1+x))` simplifies to `ln(x)`. If the axis label says "logit" but the transform is actually "signed log", reviewers will catch this.

```python
# This is NOT a logit, it's a signed log:
scaled = abs_beta / (1 + abs_beta)
result = np.log(scaled / (1 - scaled)) * np.sign(beta)
# = np.log(abs_beta) * np.sign(beta) = signed log

# Fix the label:
ax.set_xlabel("sign(β) × ln(|β|)")  # not "logit-transformed"
```

**6. matplotlib memory leak**
`plt.close(fig)` must be called after saving. Best practice: add it to the shared `save_fig()` function.

```python
def save_fig(fig, name):
    fig.savefig(f"figures/{name}.png", dpi=300)
    plt.close(fig)  # prevents memory leak in long pipelines
```

**7. API calls without retry logic**
Scientific APIs (Enrichr, KEGG, UniProt) can be rate-limited or temporarily unavailable. Always add exponential backoff.

```python
def retry_request(fn, max_attempts=3, base_delay=2.0):
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))
```

**8. Single-bolus process perturbation accidentally implemented as continuous feed**

This is a high-value failure mode in staged dFBA / bioreactor simulations. A code path may claim to add a one-time nitrate bolus, inducer pulse, or nutrient spike at the stage transition, but if the update term is written as `stage_alpha * bolus / ramp * dt` inside every post-switch step, the simulator will keep re-adding the bolus after the transition finishes.

```python
# BROKEN: once stage_alpha reaches 1.0, this keeps injecting forever
dS += stage_alpha * (bolus_total / ramp) * dt

# FIXED: add only the newly-entered fraction of the bolus
delta_alpha = max(0.0, stage_alpha - prev_stage_alpha)
dS += delta_alpha * bolus_total
prev_stage_alpha = stage_alpha
```

Symptoms:
- supposed "single bolus" conditions behave like chronic feed conditions
- nitrate / nitrite / inducer toxicity looks implausibly persistent
- optimization falsely prefers zero-bolus designs because all bolus designs are over-penalized

When reviewing a staged scientific simulator, explicitly trace whether event-style additions are implemented as **incremental delivery** or mistakenly as **persistent forcing**.

**9. Stage-specific objective coupling accidentally reused across phases**

In two-stage metabolic simulations, the growth phase should typically stay near biomass maximization, while the production phase relaxes growth and shifts toward product export. A common bug is to reuse the low production-stage growth-coupling parameter during Stage I, which suppresses biomass accumulation and caps later titer for the wrong reason.

```python
# BETTER: separate near-max-growth Stage I from low-growth Stage II
gc = ((1.0 - stage_alpha) * stage1_growth_coupling +
      stage_alpha * stage2_growth_coupling)
```

Review rule: if a simulator claims "Stage I = growth, Stage II = production", verify that the optimization objective and minimum-biomass constraints actually reflect that distinction.

**10. CLI path bypasses the config/env-override factory**

Scientific simulators often expose a helper like `make_stage_config()` or `load_config()` that applies environment-variable overrides for sweeps and automation loops. A subtle but important bug is when the library path uses that helper but the CLI constructs the config dataclass directly, silently ignoring env-driven overrides.

```python
# BROKEN: ignores env overrides
cfg = StageConfig(t_final_h=args.t_final, ...)

# FIXED: start from the override-aware factory, then apply CLI args
cfg = make_stage_config()
cfg.t_final_h = args.t_final
```

This mismatch causes reproducibility drift between:
- direct CLI runs
- autonomous optimization loops
- notebooks / scripts that rely on env-var control

**11. Script-relative output roots accidentally write into `scripts/figures` or `scripts/results`**

A common portability bug in multi-script scientific repos is anchoring output paths to `HERE = Path(__file__).resolve().parent` and then writing `HERE / "figures" / ...` or `HERE / "results" / ...`. For scripts stored under `repo/scripts/`, this silently creates shadow output trees under `repo/scripts/figures/` instead of the canonical repo-level artifact directories.

```python
# BROKEN: writes under repo/scripts/figures/
HERE = Path(__file__).resolve().parent
FIGURES_DIR = HERE / "figures" / "autoresearch"

# FIXED: anchor outputs at the repository root
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIGURES_DIR = ROOT / "figures" / "autoresearch"
RESULTS_DIR = ROOT / "results" / "autoresearch"
```

Review rule: if the repository convention is top-level `figures/`, `results/`, or `models/`, verify that maintained scripts write there consistently instead of creating nested duplicates under `scripts/`.

**12. Incompatible packaged dataset misdiagnosed as a missing-file error**

Scientific figure/report scripts often evolve against one JSONL/CSV schema, then later get pointed at a different results file that exists but lacks required columns. A naive implementation raises `FileNotFoundError` or fails deep inside plotting code, which misleads the user about the real issue.

```python
REQUIRED_COLUMNS = {"feeding_regime", "gene_expr_boost", "citrulline_pool"}

candidates = [
    ROOT / "results" / "autoresearch" / "autoresearch_log.jsonl",
    ROOT / "results" / "autoresearch" / "autoresearch_log_10000_patent_guided.jsonl",
]
log_path = next((p for p in candidates if p.exists()), None)
if log_path is None:
    raise FileNotFoundError("No compatible results log found")

df = pd.read_json(log_path, lines=True)
missing = sorted(REQUIRED_COLUMNS - set(df.columns))
if missing:
    raise ValueError(
        f"Input {log_path} is missing required columns: {missing}. "
        "Generate a compatible dataset or point the script at one explicitly."
    )
```

Review rule: separate three failure modes explicitly:
- file absent
- file present but wrong schema
- file present and schema-compatible but semantically stale

**13. Hard-coded Python interpreter paths and shell-joined subprocess calls in runners**

Repository runners frequently hard-code workstation-specific interpreters like `/home/user/anaconda3/bin/python` and then wrap command lists into `" ".join(cmd)` with `shell=True`. This makes the pipeline brittle across machines and re-introduces quoting bugs.

```python
# BROKEN
cmd = ["PYTHONNOUSERSITE=1", "/home/user/anaconda3/bin/python", "scripts/run.py"]
subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)

# FIXED
PYTHON = os.environ.get("AUTORESEARCH_PYTHON", sys.executable)
env = os.environ.copy()
env["PYTHONNOUSERSITE"] = "1"
cmd = [PYTHON, str(HERE / "run.py")]
subprocess.run(cmd, capture_output=True, text=True, env=env)
```

Review rule: when auditing scientific automation, explicitly search for:
- hard-coded interpreter paths
- `shell=True` used only to smuggle env vars
- command lists converted to joined strings instead of passed as argv


See `references/publication_evidence_grade_layer.md` for a compact evidence-grading pattern for causal target projects.

### Manuscript Pitfalls

**8. Number drift between abstract, results, and discussion**
After relaxing filtering thresholds (e.g., SigCount ≥ 1.5 instead of 2), the abstract may still show old numbers. Always reconcile:
- Abstract sample sizes vs actual data
- Results section counts vs pipeline output
- Discussion claims vs computed values
- Figure caption numbers vs actual data

**9. Missing or wrong directional consistency threshold**
If the pipeline uses 0.6 but the manuscript says 0.75, reviewers will question the rigor.

**10. Placeholder figures masquerading as real outputs**
A 4KB PNG is almost certainly a placeholder/error message, not a real figure. Check file sizes and use vision_analyze if available.

**11. README quick-start does not match actual runnable state**
A repo may claim `pip install -r requirements.txt && bash run_all.sh` is enough, while core scripts actually require undeclared packages (for example COBRApy), sibling repos, external datasets, or machine-specific interpreters. Treat this as a reproducibility bug, not just a documentation nit.

**12. Competing manuscript narratives**
Scientific repos that accumulate reports over time often contain multiple headline results (for example different best titers or simulation counts) across paper drafts, summaries, and visualization reports. Call this out explicitly as a publication-readiness risk and require one canonical manuscript, figure family, and result set.

**13. Live workspace mistaken for release package**
A repo can be scientifically valuable yet still be a live workspace rather than a clean distributable project. Say so directly when appropriate: this helps the user prioritize canonicalization, archiving, tests, and path cleanup instead of only polishing prose.

---

## Verification Checklist

After all fixes:

- [ ] All Python scripts pass `ast.parse()` syntax check
- [ ] All R scripts pass `Rscript -e "parse(f)"` syntax check
- [ ] Pipeline re-runs without new failures
- [ ] Manuscript numbers match actual data outputs
- [ ] No hardcoded user-specific paths remain (check `/home/username/...`)
- [ ] No bare `except Exception: pass` (at minimum, log the warning)
- [ ] All visualization scripts close figures (via shared `save_fig()`)
- [ ] Expected figure files exist and are >10KB (not placeholders)

---

## Output Format

For repository-wide review requests, prefer this structure:
- Overall verdict
- What looks strong
- Highest-priority findings table
- Issues by category (reproducibility, portability, testing, manuscript consistency, release hygiene)
- Priority action plan (P0/P1/P2)
- Bottom line

See also: `references/repo-audit-checklist.md`.

Produce a summary table:

| Round | Fixes | Coverage |
|-------|-------|----------|
| 1 | N | Python scripts 0-N, shared config |
| 2 | M | R scripts, CNS variants, manuscript |
| Total | N+M | Full pipeline |

For each fix: file, line, severity (🔴🟠🟡), one-line description.
