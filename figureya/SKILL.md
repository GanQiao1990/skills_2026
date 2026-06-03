---
name: figureya
description: "Run and reuse FigureYa biomedical RMarkdown modules from /home/qiao/dockerai/FigureYa. Use this when you need to search modules, inspect inputs, choose the correct Rmd entry point, and render reports reproducibly."
license: CC BY-NC-SA 4.0 (see FigureYa repository)
metadata:
  skill-author: GanQiao (local integration)
  figureya-root: /home/qiao/dockerai/FigureYa
---

# FigureYa Skill (local)

> *"Each FigureYa module is a self-contained RMarkdown workflow with install_dependencies.R and easy_input files. The agent's job: match the user's biomedical visualization need to the right module, verify the actual Rmd filename, and render reproducibly."*

## Quick Start for LLM Agents

**When a user asks for a biomedical visualization:**

1. **Match** → Search the [Task-to-Module mapping table](#task-to-module-mapping-table) for the analysis type
2. **Verify** → Check `filelist.txt` for the actual `Rmd` filename (folder name ≠ Rmd name)
3. **Inspect** → List the module folder to confirm `install_dependencies.R` and `easy_input_*` files
4. **Execute** → Run from inside the module directory: `Rscript install_dependencies.R`, then `R -e "rmarkdown::render('<ACTUAL_RMD>')"` 
5. **Validate** → Confirm `*.html`, `*.pdf`, and `output_*` files exist
6. **Report** → Tell user the exact output filenames generated

**Critical: Never guess the Rmd filename. Always check `filelist.txt` first.**

## Primary goal
- Help the agent choose the correct FigureYa module with minimal guessing.
- Help the agent run the module in the right directory with the right `Rmd` file.
- Help the agent inspect inputs and outputs based on the real module contents, not assumptions.
- Help the agent explain failures precisely when dependencies, file names, or input schemas do not match.

## Architecture: How an agent should use FigureYa

```
User request → "I need a PCA plot"
       │
       ▼
Agent searches filelist.txt + module names
       │
       ▼
Agent identifies candidates: FigureYa101PCA, FigureYa38PCA, etc.
       │
       ▼
Agent inspects target folder for actual Rmd + inputs
       │
  ┌────┴────┐
  │         │
Custom    Use example
data?     data as-is
  │         │
  ▼         ▼
Edit      Run directly
easy_input_*
  │         │
  └────┬────┘
       │
       ▼
cd /home/qiao/dockerai/FigureYa/<MODULE>
Rscript install_dependencies.R
R -e "rmarkdown::render('<ACTUAL_RMD>')"
       │
       ▼
Verify outputs: *.html, *.pdf, output_*
       │
  ┌────┴────┐
Success    Failure
  │           │
Report     Diagnose:
output     - Missing packages?
files      - Wrong Rmd name?
           - Input schema mismatch?
           - Missing external data?
```

## When to use this skill
- The user asks for a biomedical plot or analysis that may already exist in FigureYa.
- The user wants a FigureYa module rendered locally.
- The user wants to inspect a module's expected input files, output files, or report.
- The user wants to adapt inputs for a known FigureYa module.

## When not to use this skill
- The user wants a brand-new plotting pipeline unrelated to FigureYa.
- The user needs broad R debugging that is not tied to a FigureYa module.
- The request is better handled by a different local workflow or a custom analysis script.

## Repository map
- Repo root: `/home/qiao/dockerai/FigureYa`
- Modules list: `/home/qiao/dockerai/FigureYa/filelist.txt`
- Included modules: `/home/qiao/dockerai/FigureYa/all_included.txt`
- Gallery and generated content: `/home/qiao/dockerai/FigureYa/gallery`
- Common summary files: `/home/qiao/dockerai/FigureYa/summary.txt`
- Upstream repo overview: `/home/qiao/dockerai/FigureYa/README.md`

## Critical realities of this repository
- Do not assume the folder name and the main `Rmd` file name are identical.
- Do not assume every module has only one `Rmd` file.
- Do not assume every module uses the same input naming pattern.
- Do not assume every module writes the same output filenames.

Real examples from this repository:
- `FigureYa11bubble` uses `FigureYa11bubbles.Rmd`.
- `FigureYa20mortality` uses `FigureYa20mortalityV2.Rmd`.
- `FigureYa45V2` uses `FigureYa45iClusterV2.Rmd`.
- `FigureYa53PPImodule` uses `FigureYa53PPImodule.rmd` with lowercase extension.
- `FigureYa177RNAvelocity` contains a main `Rmd` plus multiple staged scripts under `scripts/`.

Because of this, always treat `filelist.txt` as the authoritative source for mapping a module folder to its actual `Rmd` entry point.

## Golden rules for agent use
1. Start from the user intent, not from random folder browsing.
2. Use `filelist.txt` to locate the actual `Rmd` before trying to render.
3. Inspect the target module folder before editing or running anything.
4. Prefer editing `easy_input_*` files over editing the `Rmd` unless the user explicitly asks for code changes.
5. Do not overwrite canonical example inputs blindly if the user is asking for a custom run; confirm or use a working copy strategy.
6. Verify outputs after rendering instead of assuming success from command completion.
7. If more than one module is plausible, present the top candidate and one backup, or ask a narrow clarification question.

## Recommended LLM interaction workflow
1. Identify the requested visualization, task, or statistical pattern.
2. Search for matching modules using `filelist.txt`, `all_included.txt`, folder names, and the repo `README.md` description.
3. Choose the best candidate module.
4. Read the module folder to confirm the actual `Rmd`, `install_dependencies.R`, available `easy_input_*` files, and any existing outputs or logs.
5. If the module is a simple single-report module, render the main `Rmd` from that module directory.
6. If the module looks like a staged workflow or contains multiple `Rmd` files, inspect before running and do not guess the correct entry point.
7. After rendering, confirm generated HTML, figures, and tables in the module directory.
8. Report back using concrete filenames.

## Task-to-Module mapping table

Use this table as the primary decision aid. Always verify the actual `Rmd` name in `filelist.txt` before running.

| Task / Analysis Type | Recommended Module(s) | Actual Rmd File | Typical Inputs |
|----------------------|----------------------|-----------------|----------------|
| **Dimensionality Reduction** |
| Basic PCA (batch-aware) | `FigureYa101PCA` | `FigureYa101PCA.Rmd` | `easy_input_expr.csv`, `easy_input_meta.csv`, `easy_input_batch.csv` |
| PCA (simple) | `FigureYa38PCA` | `FigureYa38PCA.Rmd` | Single expression matrix |
| 3D PCA | `FigureYa164PCA3D` | `FigureYa164PCA3D.Rmd` | Expression + metadata |
| t-SNE | `FigureYa27tSNE_update` | `FIgureYa27tSNE_update.Rmd` | Expression matrix |
| UMAP | `FigureYa93UMAP` | `FigureYa93UMAP.Rmd` | Expression + labels |
| **Classification / Prediction** |
| ROC curve (basic) | `FigureYa24ROC` | `FigureYa24ROC.Rmd` | `easy_input.txt` |
| Multi-panel ROC | `FigureYa102multipanelROC` | `FigureYa102multipanelROC.Rmd` | Multiple classifier outputs |
| Pairwise AUC | `FigureYa200pairwiseAUC` | `FigureYa200pairwiseAUC.Rmd` | Multi-class predictions |
| Calibration plot | `FigureYa138NiceCalibration` | `FigureYa138NiceCalibration.Rmd` | Predicted probabilities |
| **GWAS / Genomics** |
| Manhattan plot | `FigureYa43ManhattanV2` | `FigureYa43ManhattanV2.Rmd` | `easy_input.csv` (chr, pos, p-value) |
| Chromosome ideogram | `FigureYa10chromosomeV2_update` | `FigureYa10chromosomeV2_update.Rmd` | Genomic coordinates |
| Lollipop plot | `FigureYa19Lollipop` | `FigureYa19Lollipop.Rmd` | Protein domains + variants |
| **Survival Analysis** |
| Kaplan-Meier curves | `FigureYa1survivalCurve_update` | `FigureYa1survivalCurve_update.Rmd` | Survival time + status |
| Prognostic model | `FigureYa128Prognostic` | `FigureYa128Prognostic.Rmd` | Clinical + expression data |
| Subgroup survival | `FigureYa171subgroupSurv` | `FigureYa171subgroupSurv.Rmd` | Stratified cohorts |
| Time-dependent C-index | `FigureYa189timeCindex` | `FigureYa189timeCindex.Rmd` | Longitudinal risk scores |
| **Heatmaps** |
| Clustered heatmap | `FigureYa9heatmap` | `FigureYa9heatmap.Rmd` | Expression matrix |
| Cluster heatmap | `FigureYa91cluster_heatmap` | `FigureYa91cluster_heatmap.Rmd` | Pre-clustered data |
| Customizable heatmap | `FigureYa213customizeHeatmap` | `FigureYa213customizeHeatmap.Rmd` | Flexible annotation |
| Association heatmap | `FigureYa124AssociationHeatmap` | `FigureYa124AssociationHeatmap.Rmd` | Correlation matrix |
| **Machine Learning** |
| Logistic + RF + SVM | `FigureYa159LR_RF_V2` | `FigureYa159LR_RF_V2.Rmd` | Features + labels |
| Elastic Net | `FigureYa218Elasticnet` | `FigureYa218Elasticnet.Rmd` | High-dimensional features |
| 10-fold Random Forest | `FigureYa221tenFoldRF` | `FigureYa221tenFoldRF.Rmd` | Training + test sets |
| Comprehensive ML suite | `FigureYa293machineLearning` | `FigureYa293machineLearning.Rmd` | Multi-cohort validation |
| RF + XGBoost + Boruta | `FigureYa316RF_XGBoost_Boruta` | `FigureYa316RF_XGBoost_Boruta.Rmd` | Feature selection focus |
| **Enrichment / Pathway** |
| GSEA (Java-based) | `FigureYa13GSEA_Java_update` | `FigureYa13GSEA_Java_update.Rmd` | Gene sets + expression |
| GSEA (clusterProfiler) | `FigureYa60GSEA_clusterProfilerV2` | `FigureYa60GSEA_clusterProfilerV2.Rmd` | Gene list + background |
| ssGSEA | `FigureYa71ssGSEA_update` | `FigureYa71ssGSEA_update.Rmd` | Single-sample scoring |
| GSVA | `FigureYa61GSVA` | `FigureYa61GSVA.Rmd` | Gene set variation |
| GO clustering | `FigureYa80GOclustering` | `FigureYa80GOclustering.Rmd` | Enriched terms |
| **Differential Expression** |
| Volcano plot | `FigureYa59volcanoV2` | `FigureYa59volcanoV2.Rmd` | `easy_input_limma.csv` |
| Multi-class DESeq2 | `FigureYa118MulticlassDESeq2` | `FigureYa118MulticlassDESeq2.Rmd` | Count matrix |
| Multi-class limma | `FigureYa119Multiclasslimma` | `FigureYa119Multiclasslimma.Rmd` | Expression matrix |
| Multi-class edgeR | `FigureYa120MulticlassedgeR` | `FigureYa120MulticlassedgeR.Rmd` | Count matrix |
| **Single-Cell** |
| scRNA UMAP | `FigureYa93UMAP` | `FigureYa93UMAP.Rmd` | Seurat/Scanpy output |
| scRNA marker genes | `FigureYa224scMarker` | `FigureYa224scMarker.Rmd` | Cluster markers |
| scRNA DEG | `FigureYa235scDEG` | `FigureYa235scDEG.Rmd` | Single-cell DE results |
| scRNA violin plot | `FigureYa254scViolin` | `FigureYa254scViolin.Rmd` | Gene expression by cluster |
| scRNA CellChat | `FigureYa267scCellChat` | `FigureYa267scCellChat.Rmd` | Ligand-receptor analysis |

**Decision rule for generic requests:**
- If the user says "PCA" without details → ask whether they have batch effects, metadata, or 3D needs
- If the user says "survival" without details → ask whether it's basic KM, prognostic model, or subgroup comparison
- If the user says "heatmap" without details → ask whether it's simple clustering, custom annotation, or association matrix
- If the user says "machine learning" without details → ask whether they need feature selection, multi-algorithm comparison, or nested CV

## Preflight checklist before running
- Confirm the module directory exists.
- Confirm the actual main `Rmd` filename from `filelist.txt` or the folder contents.
- Confirm `install_dependencies.R` exists.
- Inspect whether inputs are named `easy_input.txt`, `easy_input.csv`, `easy_input_batch.csv`, `easy_input_expr.csv`, `easy_input_meta.csv`, or another pattern.
- Check whether an `example.png` exists and use it as a style and layout hint.
- Check whether `install.log` or previous output files already exist.
- If the module has multiple scripts or subdirectories, inspect them before execution.

## How to run a module
Fastest helper-script path:

```bash
/home/qiao/anaconda3/bin/python /home/qiao/.claude/skills/figureya/scripts/search_modules.py --query pca

/home/qiao/anaconda3/bin/python /home/qiao/.claude/skills/figureya/scripts/render_module.py \
  --module FigureYa101PCA \
  --format html \
  --output-dir /home/qiao/qiao_design/workbench/figureya_runs/FigureYa101PCA
```

If using a terminal manually:
```bash
cd /home/qiao/dockerai/FigureYa/FigureYa101PCA
Rscript install_dependencies.R
R -e "rmarkdown::render('FigureYa101PCA.Rmd')"
```

If using an agent terminal tool, prefer setting the working directory to the module folder instead of issuing `cd` inside the command.

Generic pattern:
```bash
Rscript install_dependencies.R
R -e "rmarkdown::render('<ACTUAL_RMD_FILE>')"
```

Replace `<ACTUAL_RMD_FILE>` with the real file name from `filelist.txt` or the folder, not with a guessed name based on the folder.

If the module has a folder and `Rmd` name mismatch, pass the explicit `--rmd` value:

```bash
/home/qiao/anaconda3/bin/python /home/qiao/.claude/skills/figureya/scripts/render_module.py \
  --module FigureYa11bubble \
  --rmd FigureYa11bubbles.Rmd \
  --format html \
  --output-dir /home/qiao/qiao_design/workbench/figureya_runs/FigureYa11bubble
```

## Input handling rules
- Prefer changing `easy_input_*` files instead of editing the `Rmd`.
- If there are multiple input files, identify their roles before editing. For example, one module may separate expression, metadata, and batch information.
- If the user has custom data, do not silently overwrite the repository's example inputs unless they explicitly want in-place edits.
- If the input schema is unclear, inspect the relevant `easy_input_*` files first and summarize the expected columns or structure for the user.

## Output validation rules
- Typical outputs include `*.html`, `*.pdf`, `*.jpg`, `example.png`, `output_*`, and table-like text or spreadsheet files.
- Some modules output domain-specific filenames such as `auc_output.xls`, `pvalue_output.xls`, or `output_feature_lasso.csv`.
- Do not claim success until you confirm the expected rendered HTML and at least one figure or result file exists.
- When reporting success, name the actual output files you found.

## Failure handling
- If package installation fails, report the missing package name and whether the failure appears to be CRAN, Bioconductor, network, or version related.
- If the `Rmd` name does not match the folder name, mention both explicitly and use the actual `Rmd` filename.
- If a module contains multiple `Rmd` files, do not guess the entry point; inspect first.
- If the request cannot be mapped to a module confidently, ask which module or output style the user wants.
- If the module appears to require large external files not present locally, say so explicitly rather than pretending the module is ready.

## Installation hints
If packages fail to install, ensure CRAN or Bioconductor mirrors are reachable. You can set the CRAN mirror in R:
```r
options(repos = c(CRAN='https://cran.r-project.org'))
```

## Real-world usage examples

### Example 1: User requests a PCA plot with batch correction

**User:** "I need a PCA plot with batch correction."

**Agent reasoning:**
1. Search task-to-module table → "Basic PCA (batch-aware)" → `FigureYa101PCA`
2. Check `filelist.txt` → Confirm `FigureYa101PCA/FigureYa101PCA.Rmd`
3. Inspect folder → Found `easy_input_expr.csv`, `easy_input_meta.csv`, `easy_input_batch.csv`
4. Verify this matches user need → Yes, batch-aware

**Agent action:**
```bash
cd /home/qiao/dockerai/FigureYa/FigureYa101PCA
Rscript install_dependencies.R
R -e "rmarkdown::render('FigureYa101PCA.Rmd')"
```

**Agent verification:**
- Check for `FigureYa101PCA.html` ✓
- Check for `PCA.2batches.withgrid.pdf` ✓
- Check for `PCA.2batches.withoutgrid.pdf` ✓

**Agent report:**
> I've rendered `FigureYa101PCA` which handles batch correction. Outputs:
> - HTML report: `FigureYa101PCA.html`
> - Figures: `PCA.2batches.withgrid.pdf`, `PCA.2batches.withoutgrid.pdf`, `PCA.replicates.withoutgrid.pdf`
> - Inputs used: `easy_input_expr.csv` (expression), `easy_input_meta.csv` (metadata), `easy_input_batch.csv` (batch labels)

### Example 2: User requests a ROC curve but folder name doesn't match Rmd name

**User:** "Generate a ROC curve."

**Agent reasoning:**
1. Search table → `FigureYa24ROC`
2. Check `filelist.txt` → `FigureYa24ROC/FigureYa24ROC.Rmd` ✓ (matches)
3. Inspect folder → `easy_input.txt` exists

**Agent action:**
```bash
cd /home/qiao/dockerai/FigureYa/FigureYa24ROC
Rscript install_dependencies.R
R -e "rmarkdown::render('FigureYa24ROC.Rmd')"
```

**Agent verification:**
- `FigureYa24ROC.html` ✓
- `ROC.pdf` ✓
- `auc_output.xls` ✓
- `pvalue_output.xls` ✓

**Agent report:**
> ROC analysis complete. Outputs in `/home/qiao/dockerai/FigureYa/FigureYa24ROC/`:
> - Report: `FigureYa24ROC.html`
> - Figure: `ROC.pdf`
> - Results: `auc_output.xls`, `pvalue_output.xls`

### Example 3: Handling folder/Rmd name mismatch

**User:** "Run the bubble plot module."

**Agent reasoning:**
1. Search → `FigureYa11bubble`
2. Check `filelist.txt` → **`FigureYa11bubble/FigureYa11bubbles.Rmd`** (note the 's')
3. This is a common mismatch pattern

**Agent action:**
```bash
cd /home/qiao/dockerai/FigureYa/FigureYa11bubble
Rscript install_dependencies.R
R -e "rmarkdown::render('FigureYa11bubbles.Rmd')"  # Use actual Rmd name
```

**Agent report:**
> Note: Module folder is `FigureYa11bubble` but the Rmd file is `FigureYa11bubbles.Rmd` (with 's'). Rendered successfully.

### Example 4: Multi-stage module with subdirectories

**User:** "I need RNA velocity analysis."

**Agent reasoning:**
1. Search → `FigureYa177RNAvelocity`
2. Check folder → Contains main `Rmd` + `scripts/` subdirectory with 7 staged scripts
3. This is NOT a simple single-render module

**Agent action:**
> I found `FigureYa177RNAvelocity` which contains a multi-stage workflow:
> - Main: `FigureYa177RNAvelocity.Rmd`
> - Staged scripts under `scripts/`: `s0_createEnv.Rmd`, `s1_prepare.Rmd`, ..., `s7_RNAVelocity.Rmd`
>
> This appears to be a pipeline with 7 sequential steps. Would you like me to:
> 1. Run the main `Rmd` (may orchestrate all steps)
> 2. Run the staged scripts in sequence
> 3. Just inspect the workflow structure first?

## Troubleshooting table

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| `Error: could not find function "xxx"` | Missing R package | Check `install_dependencies.R` ran successfully; try `install.packages("xxx")` manually |
| `cannot open file 'FigureYaXXX.Rmd'` | Wrong Rmd filename | Check `filelist.txt` for actual name; folder name ≠ Rmd name |
| `Error in eval: object 'input_data' not found` | Missing or misnamed input file | Inspect module folder for expected `easy_input_*` pattern; check schema |
| Package install hangs | Network/mirror issue | Set `options(repos = c(CRAN='https://cran.r-project.org'))` or try `.cn` mirror |
| `Error: Bioconductor version xxx` | Version conflict | May need `BiocManager::install(version = "x.y")` |
| OOM / memory error | Dataset too large for default settings | Check if module has memory-efficient alternatives or downsample data |
| `Pandoc error` | Missing pandoc or version mismatch | Install pandoc: `conda install pandoc` or use system package manager |
| Output PDF empty/corrupted | Graphics device issue | Check if cairo/X11 available; try rendering to HTML first |
| Module requires external file > 100MB | File not in repo (GitHub limit) | Check module README or contact FigureYa authors (baidu group 967269198) |
| Multiple Rmd files, unclear entry point | Staged workflow module | Inspect `filelist.txt` for main entry; check for `step1`, `main`, or numbered scripts |

## Module file structure patterns

| File Type | Role | Agent Action |
|-----------|------|-------------|
| `*.Rmd` | Analysis script | **Execute this** via `rmarkdown::render()` |
| `install_dependencies.R` | Package installer | **Run first** via `Rscript` |
| `easy_input_*.csv` | Primary data inputs | **Inspect schema**, edit if user has custom data |
| `easy_input.txt` | Simple parameter file | **Read** to understand expected format |
| `example.png` | Reference output style | **Show to user** if they ask what the output looks like |
| `*.html` | Rendered report | **Generated output**, verify exists after render |
| `*.pdf` | Vector figures | **Generated output**, primary deliverable |
| `output_*.txt`, `output_*.csv` | Result tables | **Generated output**, parse for summary stats |
| `install.log` | Installation log | **Read on failure** to diagnose package issues |
| `scripts/` subdirectory | Staged workflow | **Inspect before running**; likely multi-step pipeline |

## Helper utilities

### Quick module search

To help the agent quickly find modules without reading the full `filelist.txt`:

```bash
# Search for keyword in module names
grep -i "survival" /home/qiao/dockerai/FigureYa/filelist.txt

# Search for keyword in all Rmd files (slower but comprehensive)
grep -r "keyword" /home/qiao/dockerai/FigureYa/*/FigureYa*.Rmd | head -20

# List all modules with "heatmap" in the name
ls -d /home/qiao/dockerai/FigureYa/*heatmap* /home/qiao/dockerai/FigureYa/*Heatmap*
```

### Verify module readiness

Before rendering, the agent can run this checklist:

```bash
MODULE="FigureYa101PCA"
cd /home/qiao/dockerai/FigureYa/$MODULE

# Check for required files
[ -f install_dependencies.R ] && echo "✓ Installer found" || echo "✗ Missing installer"
ls *.Rmd 2>/dev/null && echo "✓ Rmd found" || echo "✗ No Rmd file"
ls easy_input* 2>/dev/null && echo "✓ Input files found" || echo "⚠ No easy_input files"

# Check for previous outputs (indicates example has been run)
[ -f *.html ] && echo "✓ Example HTML exists" || echo "⚠ No previous output"
```

### Extract module metadata

To understand a module without running it:

```bash
# Read the first comment block in the Rmd (often contains description)
head -50 FigureYa101PCA.Rmd | grep -A 20 "^#"

# Check what packages it will install
grep "install.packages\|BiocManager::install" install_dependencies.R

# Peek at input file structure
head -5 easy_input_*.csv
```

## Response style for the agent
- Be concrete.
- Mention the chosen module by full folder name.
- Mention the actual `Rmd` filename (especially if it differs from folder name).
- Mention the input files inspected and their schema if relevant.
- Mention the output files generated or found by their exact names.
- If a module has known quirks (name mismatch, multi-stage, large external files), mention them proactively.
- If uncertain, ask one focused clarification question instead of listing many possibilities.

## Best Practices for LLM Agents

### DO:
1. **Always start with the task-to-module mapping table** – it saves time and reduces errors
2. **Always verify the Rmd filename in `filelist.txt`** – folder names lie, `filelist.txt` doesn't
3. **Inspect before executing** – check for `install_dependencies.R`, `easy_input_*`, and any `scripts/` subdirectories
4. **Prefer editing `easy_input_*` over editing the Rmd** – cleaner separation of data and code
5. **Verify outputs before claiming success** – command completion ≠ successful rendering
6. **Report concrete filenames** – "Generated `PCA.2batches.withgrid.pdf`" not "Generated PCA plot"
7. **Ask focused clarifications** – "Do you have batch effects?" not "What kind of PCA do you want?"
8. **Read `install.log` on failure** – it contains the exact package error

### DON'T:
1. **Don't assume folder name = Rmd name** – check `filelist.txt` or you will fail
2. **Don't guess which module** – if unclear, present top 2 candidates and ask
3. **Don't blindly overwrite example inputs** – ask if user wants in-place edit or working copy
4. **Don't render multi-stage modules without inspection** – some have 7+ sequential scripts
5. **Don't claim success without file verification** – "should have generated" is not acceptable
6. **Don't run commands from wrong directory** – rendering must happen inside module folder
7. **Don't skip `install_dependencies.R`** – even if packages seem installed, run it

### When Uncertain:
- **Multiple plausible modules** → Present top candidate + one backup, explain difference
- **Complex module structure** → Inspect first, explain to user, ask for confirmation
- **Missing expected files** → Report what's missing explicitly, don't make assumptions
- **Render failure** → Read logs, diagnose root cause (package/input/file), report clearly

## Step-by-Step Instructions

### For a Simple Visualization Request

**Example: User says "I need a PCA plot"**

```
Step 1: Search the mapping table
  → Found: Basic PCA (batch-aware), PCA (simple), 3D PCA

Step 2: Clarify if needed
  → Ask: "Do you have batch effects or metadata to include?"
  → User: "Yes, I have batch information"
  → Decision: Use FigureYa101PCA

Step 3: Verify actual Rmd name
  → grep "FigureYa101PCA" /home/qiao/dockerai/FigureYa/filelist.txt
  → Result: FigureYa101PCA/FigureYa101PCA.Rmd ✓

Step 4: Inspect module folder
  → ls /home/qiao/dockerai/FigureYa/FigureYa101PCA/
  → Found: install_dependencies.R ✓
  → Found: FigureYa101PCA.Rmd ✓
  → Found: easy_input_expr.csv, easy_input_meta.csv, easy_input_batch.csv ✓

Step 5: Check if user has custom data
  → If yes: Guide them to edit easy_input_* files
  → If no: Use example data

Step 6: Execute rendering
  → cd /home/qiao/dockerai/FigureYa/FigureYa101PCA
  → Rscript install_dependencies.R
  → R -e "rmarkdown::render('FigureYa101PCA.Rmd')"

Step 7: Verify outputs
  → ls *.html *.pdf
  → Expected: FigureYa101PCA.html, PCA.2batches.withgrid.pdf, etc.
  → If missing: Read error logs, diagnose

Step 8: Report to user
  → "Rendered batch-aware PCA. Outputs:
     - Report: FigureYa101PCA.html
     - Figures: PCA.2batches.withgrid.pdf, PCA.2batches.withoutgrid.pdf
     - Used inputs: easy_input_expr.csv (5000 genes × 120 samples)"
```

### For a Complex Multi-Stage Module

**Example: User says "I need RNA velocity analysis"**

```
Step 1: Search → Find FigureYa177RNAvelocity

Step 2: Inspect folder structure
  → ls -la /home/qiao/dockerai/FigureYa/FigureYa177RNAvelocity/
  → Found: FigureYa177RNAvelocity.Rmd (main)
  → Found: scripts/ subdirectory with s0-s7 staged scripts

Step 3: Don't guess – ask user
  → "I found FigureYa177RNAvelocity with a 7-step pipeline:
      s0_createEnv.Rmd → s1_prepare.Rmd → ... → s7_RNAVelocity.Rmd
     
     Would you like me to:
     1. Run the main Rmd (may orchestrate all steps)
     2. Run staged scripts sequentially
     3. Show you the workflow first?"

Step 4: Based on user choice, execute appropriately

Step 5: Verify each stage's outputs if running sequentially
```

## Common Workflows

| User Intent | Agent Workflow |
|-------------|----------------|
| **"Generate a volcano plot"** | 1. Table → `FigureYa59volcanoV2`<br>2. Verify `FigureYa59volcanoV2.Rmd`<br>3. Check for `easy_input_limma.csv`<br>4. Render<br>5. Report `Volcano_classic.pdf`, `Volcano_advanced.pdf` |
| **"I need survival analysis"** | 1. Ask: "Basic KM curves, prognostic model, or subgroup comparison?"<br>2. Based on answer → `FigureYa1survivalCurve_update`, `FigureYa128Prognostic`, or `FigureYa171subgroupSurv`<br>3. Proceed with standard workflow |
| **"Create a heatmap"** | 1. Ask: "Simple clustering, custom annotation, or correlation matrix?"<br>2. Route to appropriate module<br>3. Standard workflow |
| **"Machine learning analysis"** | 1. Ask: "Feature selection focus, multi-algorithm comparison, or comprehensive suite?"<br>2. Route: `FigureYa316RF_XGBoost_Boruta`, `FigureYa159LR_RF_V2`, or `FigureYa293machineLearning`<br>3. Standard workflow |

## Notes
- License: CC BY-NC-SA 4.0 (FigureYa).
- Prefer reproducible local execution over ad hoc manual copying.
- Treat `filelist.txt` as the primary routing table for this repository.
- When in doubt, inspect before executing.
- Always report concrete outputs, never vague success messages.
