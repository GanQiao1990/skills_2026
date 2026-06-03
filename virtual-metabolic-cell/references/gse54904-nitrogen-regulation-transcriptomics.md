# GSE54904 transcriptomics integration for nitrogen-source / ntrC-nac analysis

Use this note when the user wants transcriptomics-guided interpretation of amino-acid synthesis under different nitrogen conditions in the `/home/qiao/qiao_design/e_coli_model` workspace, especially with `Ec_coli_modelling` as the reference background and scripts written under `narl_virtual_metabolic`.

## Dataset shape used in this session
- Input matrix: `GSE54904_rnaseq_processed.csv.gz`
- First column is gene locus (`bxxxx`)
- Sample columns follow these patterns:
  - `E_<source>_<rep>` → WT
  - `del_ntrC_<source>_<rep>`
  - `del_nac_<source>_<rep>`
- Observed source labels in the processed file: `nh4`, `gln`, `cyd`, `cts`
- Preserve the raw source labels in outputs unless the user explicitly defines their biological interpretation. Do not silently rename `cyd` or `cts`.

## Recommended integration workflow
1. Read the processed expression matrix and parse genotype / nitrogen-source / replicate from the sample names.
2. Load background annotation from `Ec_coli_modelling/input/gene_expression/GPL199.annot` for gene symbol and GO process.
3. Load metabolic context from `Ec_coli_modelling/input/models/ecoli/iML1515/iML1515.mat`.
4. Restrict interpretation to amino-acid / nitrogen-related subsystems when the user asks specifically about amino-acid synthesis. Useful subsystems in this workspace included:
   - Arginine and Proline Metabolism
   - Threonine and Lysine Metabolism
   - Glutamate Metabolism
   - Glycine and Serine Metabolism
   - Methionine Metabolism
   - Valine, Leucine, and Isoleucine Metabolism
   - Histidine Metabolism
   - Cysteine Metabolism
   - Tyrosine, Tryptophan, and Phenylalanine Metabolism
   - Nitrogen Metabolism
5. For gene-level summaries, compute WT-vs-knockout log2FC within each nitrogen source and report the strongest amino-acid-related hits.
6. For reaction-level interpretation, reuse the `Ec_coli_modelling` GPR logic:
   - `AND` → minimum gene expression
   - `OR` → maximum gene expression
   - if expression >= 1: multiplier = `1 + log(expr)`
   - if expression < 1: multiplier = `1 / (1 + abs(log(expr)))`
7. Report both gene-level effects and subsystem/reaction-capacity shifts; in this session the reaction layer made the `ntrC` vs `nac` distinction much clearer than gene lists alone.

## Durable pitfalls discovered

### 1) Pandas categorical groupby can silently create unobserved combinations
When `genotype` and `nitrogen_source` are categorical, `groupby(..., observed=False)` can produce unobserved category combinations during condition-mean aggregation. In this workflow that propagated into empty/NaN reaction activities and misleading all-zero subsystem deltas.

Use:
```python
mean_df = long_df.groupby(
    ['gene', 'genotype', 'nitrogen_source', 'condition'],
    as_index=False,
    observed=True,
)['expression'].mean()
```

Do not use the default if the downstream logic expects only observed experimental conditions.

### 2) Annotation/model merges can create duplicate gene labels before pivot
After merging platform annotation and model-context tables, a gene can appear multiple times because one gene maps to multiple subsystems. If you pivot directly on `gene_label` and `condition`, pandas raises `ValueError: Index contains duplicate entries, cannot reshape`.

Fix by either:
- `drop_duplicates('gene')` before building the label map, and/or
- aggregating again before pivot:
```python
sub = sub.groupby(['gene_label', 'condition'], as_index=False)['log2_expr'].mean()
```

### 3) Validate regulator self-consistency before interpreting pathway effects
For nitrogen-regulation datasets, first verify the regulator deletions from the expression matrix itself:
- `b3868 / glnG / ntrC` should collapse in `del_ntrC`
- `b1988 / nac` should collapse in `del_nac`
- `b1987 / cbl` is a useful companion marker under alternative nitrogen conditions

This prevents over-interpreting downstream pathway changes if labels are wrong.

## Interpretation pattern that was useful
- `del_ntrC` behaved like an upstream nitrogen-assimilation failure: strong suppression of `glnA` / GLNS and broad disruption of glutamate-centered assimilation, especially under non-`nh4` conditions.
- `del_nac` behaved more like branch redistribution than total collapse: glutamate / serine / aromatic-amino-acid branches could increase even while the regulatory program was altered.
- When summarizing for this user, emphasize the mechanistic distinction `ntrC = upstream assimilation switch` vs `nac = downstream branch allocation/regulon shaper` if the data support it.

## Output package that worked well
Produce one directory containing:
- sample metadata
- condition-mean expression table
- gene annotation + model context table
- gene-level knockout effects
- amino-acid-focused effect table
- reaction-activity table
- subsystem-delta table
- 2–3 compact figures
- one Markdown report summarizing regulator QC, strongest hits, and subsystem interpretation
