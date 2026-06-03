# Virtual Cell Simulation Patterns

## AIVM Framework Implementation

AI Virtual Metabolism (AIVM) framework for intelligent metabolic pathway reconstruction.

### Core Architecture

1. **Modular Biological Constraint Layers**
   - Nitrogen-state / nitrate-gated control (NarL, NtrC)
   - Nitrogen assimilation boost
   - Redox balancing
   - Export enhancement
   - Enzyme complex / local pathway organization

2. **Transcriptomics Integration**
   - Gene expression data via GPR (Gene-Protein-Reaction) rules
   - Log-scale adjustments for reaction bounds
   - Handle both AND/OR relationships in GPR

3. **Dynamic Simulation**
   - Time-stepped state transitions
   - Phase-based condition changes (growth vs production)
   - Pool tracking (glucose, nitrate, nitrite)

## Critical Correction: Oxygen Conditions

### User Correction Pattern

**Initial assumption**: Low-oxygen fermentation during production phase
**Actual condition**: 全程高溶氧发酵 (high dissolved oxygen throughout)

**Implementation**:
```python
# WRONG - assumes low-oxygen production
StepCondition(5.0, -2.0, 0.0, 'production_low_o2')

# RIGHT - maintains high oxygen throughout
StepCondition(5.0, -18.0, 0.0, 'production_high_o2')
```

### Impact on Results

High oxygen conditions affect:
- NtrC-like gene regulation effectiveness (+113.9% vs +101.4% for arginine)
- Redox balance module performance (reduced effectiveness)
- Overall pathway flux predictions

**Rule**: Always confirm actual fermentation oxygen conditions with user before simulation.

## Transcriptomics Integration via GPR Rules

### Implementation Pattern

```python
def evaluate_gpr(gpr_rule: str, gene_expr: dict) -> float:
    """Evaluate GPR rule and return reaction expression value."""
    # Find genes in rule
    genes_in_rule = re.findall(r'[a-z]\d{4}', gpr_rule)
    
    # Get expression values
    expr_values = [gene_expr.get(gene, 1.0) for gene in genes_in_rule]
    
    # Simple GPR evaluation:
    # - If any gene is lowly expressed (<0.5), use minimum
    # - Otherwise use average
    if any(val < 0.5 for val in expr_values):
        return min(expr_values)
    else:
        return sum(expr_values) / len(expr_values)

def apply_transcriptomics_constraints(model, expression_df):
    """Adjust reaction bounds based on gene expression."""
    for rxn in model.reactions:
        reaction_expr = evaluate_gpr(rxn.gene_reaction_rule, gene_expr)
        
        if reaction_expr >= 1.0:
            # Highly expressed: increase bounds
            multiplier = 1 + np.log(reaction_expr)
        else:
            # Lowly expressed: decrease bounds
            divisor = 1 + abs(np.log(reaction_expr))
```

## Autoresearch Loop Integration

### Configuration Pattern

```python
# autoresearch.md
METRIC_COMMAND = "python aivm_va_cell.py"
METRIC_EXTRACTION = "Extract product_flux_auc from va_summary.csv"
METRIC_DIRECTION = "higher_is_better"
```

### Key Features

1. Git-based version control for each experiment
2. Automated testing and result logging
3. Focus on improving specific amino acid production
4. Revert unsuccessful experiments

## Reference Project Learning

### From METABOLIC
- KEGG modules for pathway analysis
- Biogeochemical cycling (N, C, S)
- Support for MAGs and isolate genomes

### From Ec_coli_modelling
- FBA + Petri Net modeling
- Transcriptomics integration via GPR rules
- Dynamic feeding regimes (constant, pulsed, linear)
- Gene expression data integration

## Simulation Results Summary

### High Oxygen Fermentation Results

| Amino Acid | Best Strategy | Improvement |
|------------|--------------|-------------|
| Arginine | NtrC-like gene regulation | +113.9% |
| Lysine | NtrC-like gene regulation | +101.0% |
| Glutamate | NtrC-like gene regulation | +53.5% |

**Key Finding**: NtrC-like gene regulation is most effective across all amino acids in high oxygen conditions.

## Common Pitfalls

### 1. Wrong Oxygen Assumption
- Don't assume low-oxygen without confirmation
- Ask: "全程都是高溶氧吗？后期也保持高氧？"

### 2. GPR Rule Parsing
- Handle both AND/OR relationships
- Default to 1.0 for missing genes
- Use min for bottleneck, average otherwise

### 3. Summarize Function Baseline
- Must include baseline scenario matching expected label
- Update label when changing conditions (Low O2 shift → High O2 constant)

## Code Structure

```
narl_virtual_metabolic/
├── aivm_va_cell.py          # Main simulation
├── autoresearch.py          # Iterative optimization
├── learning_module.py       # Reference project integration
├── transcriptomics/         # Gene expression data
└── outputs/                 # Simulation results
    ├── va_timecourse.csv
    ├── va_summary.csv
    └── va_manifest.json
```

## Usage

```bash
# Run simulation
python aivm_va_cell.py

# Run autoresearch loop
python autoresearch.py

# Quick test
python quick_run.py
```
