# Autoresearch Examples: Metabolic Engineering

## Example 1: Optimizing Amino Acid Production in E. coli

### Scenario
Optimize arginine production flux in a genome-scale metabolic model (iML1515) by adjusting regulatory module parameters.

### Setup

| Parameter | Value |
|-----------|-------|
| Goal | Maximize arginine production flux |
| Metric command | `python aivm_va_cell.py` |
| Metric extraction | Extract `product_flux_auc` for arginine from `outputs/va_summary.csv` |
| Direction | Higher is better |
| In-scope files | `aivm_va_cell.py`, `transcriptomics/example_expression.csv` |
| Out-of-scope files | `outputs/`, `README.md` |
| Constraints | Each run < 2 min, no new deps, must maintain iML1515 compatibility |
| Max experiments | 10 |

### Experiment Ideas (Priority Order)

1. **Parameter tweaks**:
   - Increase NarL strength (nitrogen regulation)
   - Adjust export boost (transport capacity)
   - Modify enzyme complex boost (pathway enzyme expression)

2. **Transcriptomics adjustments**:
   - Upregulate key pathway genes (e.g., argG, argH)
   - Downregulate competing pathways

3. **Environmental conditions**:
   - Optimize O2 transition timing
   - Adjust biomass constraint

4. **Combinations**:
   - Combine nitrogen assimilation + redox boosts
   - Stack multiple regulatory modules

### Sample Script Pattern

```python
def apply_experiment_idea(experiment_num):
    """Apply experiment idea to improve production."""
    ideas = [
        ("increase_narl_strength", "Increase NarL strength to 4.0"),
        ("increase_export_boost", "Increase export boost to 2.5"),
        ("adjust_transcriptomics", "Upregulate argG gene"),
        ("combine_nitrogen_redox", "Combine nitrogen + redox boosts"),
    ]
    
    idea_id, description = ideas[experiment_num - 1]
    
    # Read script
    with open("aivm_va_cell.py", "r") as f:
        content = f.read()
    
    # Apply modification
    if idea_id == "increase_narl_strength":
        content = content.replace("narl_strength=3.0", "narl_strength=4.0")
    
    # Write back
    with open("aivm_va_cell.py", "w") as f:
        f.write(content)
    
    return idea_id, description
```

---

## Example 2: Model Parameter Optimization

### Scenario
Optimize FBA model parameters to match experimental growth rates.

### Setup

| Parameter | Value |
|-----------|-------|
| Goal | Minimize error between predicted and measured growth rates |
| Metric command | `python evaluate_model.py` |
| Metric extraction | Extract RMSE from output |
| Direction | Lower is better |
| In-scope files | `model_params.yaml` |
| Constraints | Must maintain thermodynamic feasibility |

### Experiment Ideas

1. **Vmax adjustments**: Scale reaction capacity bounds
2. **Km modifications**: Adjust Michaelis-Menten parameters
3. **Media composition**: Modify nutrient uptake rates
4. **Objective weights**: Adjust biomass vs. product trade-off

---

## Example 3: Pathway Design Optimization

### Scenario
Find optimal enzyme expression levels for a heterologous pathway.

### Setup

| Parameter | Value |
|-----------|-------|
| Goal | Maximize target compound yield |
| Metric command | `python pathway_sim.py` |
| Metric extraction | Extract yield from `results/yield.csv` |
| Direction | Higher is better |
| In-scope files | `pathway_config.json`, `enzyme_expression.csv` |
| Constraints | Must maintain cell viability (growth > 0.1) |

### Experiment Ideas

1. **Expression balancing**: Equalize pathway flux
2. **Rate-limiting step relief**: Increase bottleneck enzyme
3. **Competing pathway knockout**: Disable side reactions
4. **Cofactor balancing**: Adjust NADPH/NADH regeneration

---

## Common Patterns in Metabolic Engineering Autoresearch

### 1. Parameter Sweep Pattern

```python
# Generate parameter combinations
for param_name, param_range in parameters.items():
    for value in param_range:
        apply_parameter(param_name, value)
        metric = run_simulation()
        log_experiment(param_name, value, metric)
```

### 2. Gradient-Based Search

```python
# Estimate gradient and move in improving direction
current_value = get_parameter(param_name)
step_size = 0.1

# Test +step
set_parameter(param_name, current_value + step_size)
metric_plus = run_simulation()

# Test -step
set_parameter(param_name, current_value - step_size)
metric_minus = run_simulation()

# Move in better direction
if metric_plus > metric_minus:
    set_parameter(param_name, current_value + step_size)
else:
    set_parameter(param_name, current_value - step_size)
```

### 3. Combinatorial Search

```python
# Try combinations of successful individual changes
successful_experiments = get_kept_experiments()

for combo in itertools.combinations(successful_experiments, 2):
    apply_changes(combo)
    combined_metric = run_simulation()
    log_experiment(f"combo_{combo}", combined_metric)
```

---

## Metrics for Metabolic Engineering

### Production Metrics
- **Yield**: Product per substrate consumed (mol/mol)
- **Titer**: Final product concentration (g/L)
- **Productivity**: Product per time per volume (g/L/h)

### Model Accuracy Metrics
- **RMSE**: Root mean square error vs. experimental data
- **R²**: Coefficient of determination
- **Accuracy**: Fraction of predictions within tolerance

### Biological Constraints
- **Growth rate**: Must maintain viability
- **Flux consistency**: Thermodynamically feasible
- **Mass balance**: Elemental balance maintained

---

## Troubleshooting

### Infeasible Solutions
- Check if constraints are too tight
- Verify media composition supports growth
- Ensure mass balance is maintained

### Slow Simulations
- Use `model.slim_optimize()` for objective only
- Cache model copies instead of reloading
- Parallelize independent experiments

### Unstable Results
- Check solver tolerance settings
- Use loopless FBA to eliminate cycles
- Validate flux samples for numerical stability
