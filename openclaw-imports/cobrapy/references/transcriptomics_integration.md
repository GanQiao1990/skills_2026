# Transcriptomics Integration and Advanced Simulation Patterns

## GPR-Based Transcriptomics Constraint Application

### Pattern: Gene Expression to Reaction Bounds

```python
import re
import numpy as np
import pandas as pd

def apply_transcriptomics_constraints(model, expression_df):
    """Adjust reaction bounds based on gene expression using GPR rules."""
    if expression_df.empty:
        return
    
    # Create a gene expression dictionary for quick lookup
    gene_expr = dict(zip(expression_df['gene_id'], expression_df['expression_value']))
    
    def evaluate_gpr(gpr_rule: str) -> float:
        """Evaluate GPR rule and return reaction expression value."""
        if not gpr_rule or gpr_rule.strip() == "":
            return 1.0  # No GPR rule, assume normal expression
        
        # Find all gene IDs in the rule (b0001, b0002, etc.)
        gene_pattern = r'[a-z]\d{4}'
        genes_in_rule = list(set(re.findall(gene_pattern, gpr_rule)))
        
        if not genes_in_rule:
            return 1.0
        
        # Get expression values for genes in the rule
        expr_values = []
        for gene in genes_in_rule:
            if gene in gene_expr:
                expr_values.append(gene_expr[gene])
            else:
                expr_values.append(1.0)  # Assume normal if not found
        
        # GPR evaluation:
        # - AND relationships: use minimum (bottleneck)
        # - OR relationships: use maximum
        # Simplified: if any gene is lowly expressed (<0.5), use minimum
        if any(val < 0.5 for val in expr_values):
            return min(expr_values)
        else:
            return sum(expr_values) / len(expr_values)
    
    # Apply constraints to each reaction
    for rxn in model.reactions:
        # Skip exchange reactions
        if rxn.id.startswith('EX_') or rxn.id.startswith('DM_'):
            continue
        
        # Get reaction expression value from GPR rule
        reaction_expr = evaluate_gpr(rxn.gene_reaction_rule)
        
        # Adjust bounds based on expression level
        if reaction_expr >= 1.0:
            # Highly expressed: increase bounds
            multiplier = 1 + np.log(reaction_expr)
            new_lb = rxn.lower_bound * multiplier if rxn.lower_bound != 0 else 0
            new_ub = rxn.upper_bound * multiplier
        else:
            # Lowly expressed: decrease bounds
            divisor = 1 + abs(np.log(reaction_expr))
            new_lb = rxn.lower_bound / divisor if rxn.lower_bound != 0 else 0
            new_ub = rxn.upper_bound / divisor
        
        # Apply bounds (respecting reversibility)
        if rxn.lower_bound < 0:  # Reversible reaction
            rxn.bounds = (new_lb, new_ub)
        else:  # Irreversible reaction
            rxn.bounds = (0, new_ub)
```

### Key Insights

1. **GPR Rule Parsing**: Use regex `r'[a-z]\d{4}'` to extract E. coli gene IDs (b#### format)
2. **Expression Adjustment Formula**:
   - High expression (≥1): `bounds *= (1 + log(expression))`
   - Low expression (<1): `bounds /= (1 + abs(log(expression)))`
3. **Skip Exchange Reactions**: Don't apply transcriptomics to EX_ or DM_ reactions

## Time-Stepped Simulation Pattern

### Pattern: State Transitions with Dynamic Constraints

```python
from dataclasses import dataclass
from typing import List

@dataclass
class StepCondition:
    time_h: float
    o2_lb: float
    no3_lb: float
    phase: str

@dataclass
class Scenario:
    scenario_id: str
    product: str
    label: str
    steps: List[StepCondition]
    total_h: float = 6.0
    dt_h: float = 2.0
    # Additional boost parameters
    narl_strength: float = 1.0
    nitrogen_assimilation_boost: float = 1.0
    redox_boost: float = 1.0
    export_boost: float = 1.0
    enzyme_complex_boost: float = 1.0

def simulate_scenario(model, scenario, expression_df=None):
    """Run time-stepped simulation with state transitions."""
    biomass = 0.05
    glc_pool = 100.0
    rows = []
    n_steps = int(round(scenario.total_h / scenario.dt_h))
    
    for i in range(n_steps + 1):
        t = round(i * scenario.dt_h, 6)
        
        # Find active condition based on time
        active = scenario.steps[-1]
        for s in scenario.steps:
            if t >= s.time_h:
                active = s
        
        # Create model copy for this time step
        model_copy = model.copy()
        
        # Apply constraints based on active condition
        # ... (apply regulatory modules)
        
        # Run FBA
        try:
            sol = model_copy.optimize()
            if sol.status != 'optimal':
                raise RuntimeError(sol.status)
            # Extract fluxes...
        except Exception:
            # Handle failed optimization
            pass
        
        # Update pools based on uptake/secretion
        # ...
        
        rows.append({...})
    
    return pd.DataFrame(rows)
```

### Key Insights

1. **Copy Model per Step**: Use `model.copy()` to avoid state pollution
2. **Time-Based State Selection**: Find active condition by comparing `t >= s.time_h`
3. **Pool Tracking**: Maintain external metabolite pools between steps
4. **Biomass Growth**: Update biomass based on growth flux

## Handling Long-Running Simulations

### Pitfall: Python Output Buffering

**Problem**: Long-running simulations show no output until completion.

**Solution**: Use `flush=True` in print statements and `sys.stdout.flush()`:

```python
import sys

def main():
    print(f'Running {len(scenarios)} scenarios...', flush=True)
    sys.stdout.flush()
    
    for idx, sc in enumerate(scenarios, 1):
        print(f'[{idx}/{len(scenarios)}] {sc.scenario_id}', flush=True)
        sys.stdout.flush()
        # ... run simulation
```

### Pattern: Partial Testing Before Full Runs

```python
# Create quick_run.py for testing
test_scenario = Scenario(
    scenario_id='quick_test',
    product='arginine',
    label='Low O2 shift',  # Must match baseline label
    steps=[...],
    total_h=4.0,
    dt_h=2.0
)

# Run single scenario to verify functionality
df = simulate_scenario(model, test_scenario)
```

**Pitfall**: `summarize()` function expects baseline scenario with label "Low O2 shift". Single-scenario tests must use this label.

## Autoresearch Integration for Metabolic Engineering

### Pattern: Git-Based Experiment Tracking

```python
import subprocess
from pathlib import Path

def run_experiment(description):
    """Run an experiment with git tracking."""
    # Commit current state
    subprocess.run(["git", "add", "."], cwd=WORKDIR)
    subprocess.run(["git", "commit", "-m", f"experiment: {description}"], cwd=WORKDIR)
    
    # Run simulation
    metric, status = run_simulation()
    
    # Log results
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], 
        cwd=WORKDIR, 
        capture_output=True, 
        text=True
    ).stdout.strip()[:7]
    
    log_experiment(commit, metric, status, description)
    
    # Revert if no improvement
    if metric < best_metric:
        subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=WORKDIR)
```

### Metric Extraction for Amino Acid Production

```python
def extract_metric(summary_csv_path, product='arginine'):
    """Extract production flux AUC as optimization metric."""
    df = pd.read_csv(summary_csv_path)
    
    # Get baseline scenario
    product_rows = df[df['product'] == product]
    baseline_row = product_rows[product_rows['label'] == 'Low O2 shift']
    
    if baseline_row.empty:
        baseline_row = product_rows.iloc[[0]]
    
    return float(baseline_row['product_flux_auc'].iloc[0])
```

## Model Loading Pitfalls

### iML1515 Warnings (Safe to Ignore)

```
UserWarning: This model seems to have metCharge instead of metCharges field
Warning: No defined compartments in model iML1515
```

These warnings are harmless. COBRApy handles them automatically.

### MATLAB Model Loading

```python
from cobra.io import load_matlab_model

model = load_matlab_model('path/to/iML1515.mat')
# Works despite warnings about metCharge and compartments
```

## Performance Tips

1. **Copy Only When Needed**: `model.copy()` is expensive; minimize copies
2. **Batch Operations**: Collect changes before applying bounds
3. **Skip Unnecessary Reactions**: Don't process exchange reactions in constraint loops
4. **Use slim_optimize()**: When only objective value needed
