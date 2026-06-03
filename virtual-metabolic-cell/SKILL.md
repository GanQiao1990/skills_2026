---
name: virtual-metabolic-cell
description: 'Build AI Virtual Metabolism (AIVM) inspired virtual cell simulations for metabolic pathway reconstruction and optimization. Combines genome-scale metabolic models (GEMs) with modular biological constraints, transcriptomics integration, and autonomous research loops. USE FOR: metabolic engineering, amino acid production optimization, pathway design, flux balance analysis with dynamic constraints, multi-omics metabolic modeling. DO NOT USE FOR: simple FBA without modular constraints, non-metabolic simulations.'
license: MIT
compatibility: Requires COBRApy, pandas, numpy. Uses iML1515 or similar GEM models.
metadata:
  author: hermes-agent
  inspired-by: AIVM framework (AI Virtual Metabolism)
---

# Virtual Metabolic Cell (AIVM Framework)

Build AI Virtual Metabolism (AIVM) inspired virtual cell simulations for metabolic pathway reconstruction, combining genome-scale metabolic models with modular biological constraints, transcriptomics integration, and autonomous research capabilities.

## Support Files

- `references/iML1515_reactions.md` - Reaction ID reference for iML1515 GEM
- `references/high-o2-visualization-and-carbon-accounting.md` - Full-DO fermentation scenario design, DO/OD visualization logic, and carbon-allocation accounting guidance for this E. coli workflow
- `references/gse54904-nitrogen-regulation-transcriptomics.md` - Nitrogen-source + ntrC/nac transcriptomics integration pattern for the `e_coli_model` workspace, including GPR-based reaction-capacity interpretation and pandas pitfalls discovered during analysis
- `templates/transcriptomics_template.csv` - Template for gene expression data
- `scripts/validate_simulation.py` - Quick validation test script

## When to Use

- Metabolic engineering optimization (amino acids, biofuels, pharmaceuticals)
- Pathway design with biological constraint layers
- Flux balance analysis with dynamic environmental conditions
- Multi-omics data integration (transcriptomics + metabolism)
- Autonomous experimentation for metabolic optimization

## Core Architecture

### 1. Modular Biological Constraint Layers

Structure constraints as independent, composable modules:

```python
CONSTRAINT_MODULES = {
    'nitrogen_state': apply_nitrogen_constraints,      # Nitrate/nitrite gating
    'nitrogen_assimilation': apply_nitrogen_assimilation,  # NH4 uptake, GS/GOGAT
    'redox_balance': apply_redox_constraints,          # NADH/NADPH balancing
    'export_enhancement': apply_export_constraints,    # Product export capacity
    'enzyme_complex': apply_enzyme_complex,            # Pathway enzyme boosting
    'thermodynamic': apply_thermodynamic_filter,       # ΔG feasibility (optional)
}
```

Each module should:
- Accept a COBRA model and strength parameter
- Modify reaction bounds independently
- Be toggleable per scenario

### 2. Time-Stepped Dynamic Simulation

Use coarse time steps with environmental transitions. For this user's E. coli fermentation work, default to full-process high dissolved oxygen unless the user explicitly requests oxygen limitation or microaerobic/anaerobic phases.

```python
@dataclass
class StepCondition:
    time_h: float
    o2_lb: float          # Oxygen availability
    no3_lb: float         # Nitrate availability
    phase: str            # Phase label (growth/production)
```

High-DO default pattern:
```python
base_steps = [
    StepCondition(0.0, -18.0, 0.0, 'growth_high_o2'),
    StepCondition(5.0, -18.0, 0.0, 'production_high_o2'),
]
```

Do not reuse old `production_low_o2` labels, comments, or baseline names such as `Low O2 shift` in this project after the user clarified the real process. Keep tests, helper scripts, autoresearch baselines, manifests, and visualization labels aligned with the same high-oxygen assumption.

```python
@dataclass
class Scenario:
    scenario_id: str
    product: str
    label: str
    steps: List[StepCondition]
    total_h: float = 6.0
    dt_h: float = 2.0
    # Module strength parameters (1.0 = baseline)
    narl_strength: float = 1.0
    nitrogen_assimilation_boost: float = 1.0
    redox_boost: float = 1.0
    export_boost: float = 1.0
    enzyme_complex_boost: float = 1.0
```

### 3. Transcriptomics Integration via GPR Rules

Integrate gene expression data using Gene-Protein-Reaction rules:

```python
def evaluate_gpr(gpr_rule: str, gene_expr: dict) -> float:
    """Evaluate GPR rule and return reaction expression value."""
    # Find genes in rule (pattern: b0001, b0002, etc.)
    genes_in_rule = re.findall(r'[a-z]\d{4}', gpr_rule)
    
    # Get expression values
    expr_values = [gene_expr.get(gene, 1.0) for gene in genes_in_rule]
    
    # AND relationships: use minimum (bottleneck)
    # OR relationships: use maximum
    if any(val < 0.5 for val in expr_values):
        return min(expr_values)
    else:
        return sum(expr_values) / len(expr_values)

def apply_transcriptomics_constraints(model, expression_df):
    """Adjust reaction bounds based on gene expression."""
    gene_expr = dict(zip(expression_df['gene_id'], expression_df['expression_value']))
    
    for rxn in model.reactions:
        if rxn.id.startswith('EX_') or rxn.id.startswith('DM_'):
            continue
        
        reaction_expr = evaluate_gpr(rxn.gene_reaction_rule, gene_expr)
        
        if reaction_expr >= 1.0:
            multiplier = 1 + np.log(reaction_expr)
            rxn.bounds = (rxn.lower_bound * multiplier if rxn.lower_bound != 0 else 0,
                         rxn.upper_bound * multiplier)
        else:
            divisor = 1 + abs(np.log(reaction_expr))
            rxn.bounds = (rxn.lower_bound / divisor if rxn.lower_bound != 0 else 0,
                         rxn.upper_bound / divisor)
```

### 4. Product-Specific Pathway Modules

Define pathway reactions for each target product:

```python
PRODUCT_MODULES = {
    'arginine': {
        'objective': 'EX_arg__L_e',
        'pathway_rxns': ['ACGS', 'ACGK', 'OCBT', 'ARGSS', 'ARGSL'],
    },
    'lysine': {
        'objective': 'EX_lys__L_e',
        'pathway_rxns': ['ASPK', 'DHDPS'],
    },
    'glutamate': {
        'objective': 'EX_glu__L_e',
        'pathway_rxns': ['GLNS', 'GLUSy', 'GLUDy'],
    },
}
```

### 5. Comparative Scenario Framework

Run multiple scenarios to compare regulatory strategies:

```python
def scenario_family(product: str) -> List[Scenario]:
    """Generate scenario family for a product."""
    base_steps = [
        StepCondition(0.0, -18.0, 0.0, 'growth_high_o2'),
        StepCondition(5.0, -2.0, 0.0, 'production_low_o2'),
    ]
    
    return [
        Scenario(f'{product}_baseline', product, 'Low O2 shift', base_steps),
        Scenario(f'{product}_narl', product, 'NarL + NO3 gate', 
                 [StepCondition(0.0, -18.0, 0.0, 'growth_high_o2'),
                  StepCondition(4.0, -2.0, -2.0, 'production_narl_no3')],
                 narl_strength=3.0),
        Scenario(f'{product}_ntrc', product, 'NtrC regulation',
                 [StepCondition(0.0, -18.0, 0.0, 'growth_high_o2'),
                  StepCondition(4.0, -2.0, -1.0, 'production_ntrc')],
                 nitrogen_assimilation_boost=2.0),
        # Add more scenarios...
    ]
```

## Implementation Pattern

### Main Simulation Loop

```python
def simulate_scenario(model, scenario, expression_df=None):
    """Run a single scenario with time-stepped simulation."""
    biomass = 0.05
    glc_pool = 100.0
    rows = []
    
    for i in range(n_steps + 1):
        t = i * scenario.dt_h
        active_step = get_active_step(scenario.steps, t)
        
        model_copy = model.copy()
        apply_common_medium(model_copy)
        apply_product_objective(model_copy, scenario.product)
        
        # Apply environmental constraints
        set_bound(model_copy, 'EX_o2_e', lb=active_step.o2_lb)
        set_bound(model_copy, 'EX_glc__D_e', lb=calculate_glc_lb(glc_pool, biomass))
        
        # Apply modular biological constraints
        if scenario.narl_strength > 1.0:
            apply_narl_program(model_copy, scenario.narl_strength)
        if scenario.nitrogen_assimilation_boost > 1.0:
            apply_nitrogen_assimilation_module(model_copy, scenario.nitrogen_assimilation_boost)
        # ... other modules
        
        # Apply transcriptomics constraints
        if expression_df is not None:
            apply_transcriptomics_constraints(model_copy, expression_df)
        
        # Solve FBA
        sol = model_copy.optimize()
        
        # Record results and update pools
        rows.append(extract_results(sol, t, scenario))
        update_pools(sol, biomass, glc_pool)
    
    return pd.DataFrame(rows)
```

### Output Structure

```python
def summarize(df):
    """Generate summary statistics per scenario."""
    for (product, label), group in df.groupby(['product', 'label']):
        yield {
            'product': product,
            'label': label,
            'product_flux_auc': group['product_flux_auc_step'].sum(),
            'peak_nitrite_risk': group['nitrite_pool_proxy'].max(),
            'mean_redox_state': group['redox_state_proxy_flux'].mean(),
            'mean_nitrogen_assimilation': group['nitrogen_assimilation_proxy_flux'].mean(),
            'improvement_vs_baseline': calculate_improvement(group, baseline),
        }
```

For fermentation visualization and carbon-accounting workflows, also persist cumulative state variables instead of reconstructing everything from per-step flux AUCs alone. In particular, save scenario time-course columns such as:
- `o2_bound`
- `o2_uptake_flux`
- `co2_release_flux`
- `product_pool_mmol`
- `co2_pool_mmol`

These make downstream DO proxies, product concentration traces, and carbon partition plots much more reliable.

When presenting product concentration / yield / carbon allocation, prefer physically consistent pool-based calculations:
- product concentration from cumulative exported product pool, not a second cumsum over already integrated step AUCs
- carbon allocation from glucose carbon input versus product carbon + biomass carbon + CO2/other carbon sinks
- if a carbon-efficiency plot exceeds 100%, first check whether product accumulation was double-counted

## Learning from Reference Projects

Create a learning module to integrate best practices:

```python
class MetabolicLearningModule:
    """Learn from reference metabolic modeling projects."""
    
    def learn_from_metabolic(self):
        """METABOLIC: Microbial metabolic trait profiling."""
        return [
            "Use KEGG modules for pathway analysis",
            "Integrate biogeochemical cycling (N, C, S)",
            "Support both MAGs and isolate genomes",
        ]
    
    def learn_from_ecoli_modelling(self):
        """Ec_coli_modelling: FBA + Petri Net."""
        return [
            "Integrate transcriptomics via GPR rules",
            "Use log-scale adjustments for gene expression",
            "Model different feeding regimes (constant, pulsed, linear)",
            "Combine FBA with ODE-based Petri Net models",
        ]
```

## Autonomous Research Loop

Integrate autoresearch for iterative optimization:

```python
# autoresearch.md configuration
GOAL = "Improve amino acid production flux"
METRIC_COMMAND = "python aivm_va_cell.py"
METRIC_EXTRACTION = "Extract product_flux_auc from outputs/va_summary.csv"
METRIC_DIRECTION = "higher_is_better"

# Experiment ideas
EXPERIMENTS = [
    ("increase_narl_strength", "Increase NarL strength to 4.0"),
    ("increase_export_boost", "Increase export boost to 2.5"),
    ("combine_nitrogen_redox", "Combine nitrogen assimilation and redox boosts"),
    ("adjust_transcriptomics", "Modify transcriptomics data for key genes"),
]
```

## Pitfalls and Solutions

### 1. Output Buffering
**Problem**: Python output buffered in background processes
**Solution**: Use `flush=True` and `sys.stdout.flush()` after prints

### 2. GPR Rule Parsing
**Problem**: Complex GPR rules with nested AND/OR
**Solution**: Simplified heuristic - use min if any gene < 0.5, else average

### 3. Summarize Function Error
**Problem**: `summarize()` expects baseline scenario label
**Solution**: Ensure at least one scenario has label matching baseline (e.g., "Low O2 shift")

### 4. Long Simulation Times
**Problem**: 21 scenarios take several minutes
**Solution**: Run partial tests first, use background processes for full runs

### 5. Condition Drift Across Helper Files
**Problem**: Main simulation may be updated to full high-DO fermentation, but helper files (`test_simulation.py`, autoresearch baselines, plotting labels, reports) can still encode old low-oxygen assumptions.
**Solution**: After changing process assumptions, grep and update all helper scripts, baseline labels, and report text in the same pass. The baseline label used by summarization and autoresearch must match the real production condition.

### 6. Carbon Allocation Inflation in Visualizations
**Problem**: Visualizations can silently double-count product accumulation by cumulatively summing `product_flux_auc_step` after the simulation already emitted integrated step values, leading to impossible carbon efficiencies (>100%).
**Solution**: Track and save `product_pool_mmol` directly during simulation, and use that pool for concentration / yield / carbon partition plots. Include `co2_pool_mmol` or another explicit sink proxy when building carbon-allocation figures and reports.

## File Structure

```
project/
├── aivm_va_cell.py           # Main simulation script
├── autoresearch.py           # Autonomous research loop
├── autoresearch.md           # Autoresearch configuration
├── learning_module.py        # Learning from reference projects
├── test_simulation.py        # Quick validation test
├── transcriptomics/
│   └── example_expression.csv
└── outputs/
    ├── va_timecourse.csv     # Time series data
    ├── va_summary.csv        # Summary statistics
    └── va_manifest.json      # Experiment configuration
```

## Extensions

- **Thermodynamic filtering**: Install `equilibrator-api` for ΔG calculations
- **Petri Net dynamics**: Add ODE-based medium composition modeling
- **KEGG pathway analysis**: Integrate pathway context from KEGG
- **Gap-filling**: Implement reaction gap-filling for network connectivity
- **LLM-driven pathway proposal**: Use LLMs to suggest novel pathways

## References

- AIVM Framework: AI Virtual Metabolism for intelligent metabolic pathway reconstruction
- COBRApy: Constraint-based metabolic modeling
- iML1515: E. coli genome-scale metabolic model
- METABOLIC: Microbial metabolic trait profiling
- Ec_coli_modelling: FBA + Petri Net integration