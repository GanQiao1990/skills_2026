# Autoresearch Application: Metabolic Engineering

## Example: Amino Acid Production Optimization

### Goal Configuration

```markdown
Goal: Improve amino acid production flux in virtual E. coli cells
Metric: Extract `product_flux_auc` for arginine from `outputs/va_summary.csv`
Direction: Higher is better (maximize production)
In-scope: aivm_va_cell.py, transcriptomics/example_expression.csv
Out-of-scope: outputs/, README.md, ARCHITECTURE.md
Constraints: Each run < 2 minutes, must not break existing functionality
Budget: Unlimited
```

### Experiment Ideas for Metabolic Engineering

1. **Regulatory Module Strength**
   - Increase NarL strength (3.0 → 4.0)
   - Increase export boost (1.8 → 2.5)
   - Increase enzyme complex boost (1.6 → 2.0)

2. **Combined Interventions**
   - Combine nitrogen assimilation + redox boosts
   - Increase all regulatory boosts by 20%

3. **Process Parameters**
   - Decrease biomass constraint (0.05 → 0.03)
   - Optimize O2 transition timing (5.0h → 4.0h)

4. **Transcriptomics Adjustments**
   - Modify expression values for key genes
   - Test sensitivity to gene expression changes

### Metric Extraction Pattern

```python
import pandas as pd

def extract_production_metric(csv_path, product='arginine'):
    """Extract production flux AUC as optimization metric."""
    df = pd.read_csv(csv_path)
    
    # Get product rows
    product_rows = df[df['product'] == product]
    
    # Get baseline scenario
    baseline_row = product_rows[product_rows['label'] == 'Low O2 shift']
    
    if baseline_row.empty:
        # Fallback to first row
        baseline_row = product_rows.iloc[[0]]
    
    return float(baseline_row['product_flux_auc'].iloc[0])
```

### Git Workflow for Simulation Experiments

```python
import subprocess
from pathlib import Path

WORKDIR = Path('/path/to/project')

def commit_experiment(description):
    """Commit current simulation state."""
    subprocess.run(["git", "add", "."], cwd=WORKDIR, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"experiment: {description}"], 
        cwd=WORKDIR, 
        capture_output=True
    )

def revert_experiment():
    """Revert to previous commit if experiment failed."""
    subprocess.run(
        ["git", "reset", "--hard", "HEAD~1"], 
        cwd=WORKDIR, 
        capture_output=True
    )

def get_current_commit():
    """Get short commit hash."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], 
        cwd=WORKDIR, 
        capture_output=True, 
        text=True
    )
    return result.stdout.strip()[:7] if result.returncode == 0 else "unknown"
```

### Results Logging for Metabolic Simulations

```python
def log_simulation_result(experiment_num, commit, metric, status, description):
    """Log experiment results to TSV file."""
    results_path = WORKDIR / 'results.tsv'
    
    with open(results_path, "a") as f:
        f.write(f"{experiment_num}\t{commit}\t{metric}\t{status}\t{description}\n")
```

### Example Results Table

```
experiment	commit	metric	status	description
0	a1b2c3d	14.92	baseline	unmodified code
1	b2c3d4e	16.92	keep	increase NarL strength to 4.0
2	c3d4e5f	15.92	discard	increase export boost to 2.5
3	d4e5f6g	28.46	keep	combine NtrC + enzyme complex
4	e5f6g7h	30.06	keep	NtrC-like gene regulation
```

## Key Insights for Metabolic Engineering Autoresearch

1. **Baseline Must Exist**: Ensure baseline scenario ("Low O2 shift") is always included
2. **Partial Testing**: Run quick tests with 2-3 scenarios before full 21-scenario runs
3. **Output Buffering**: Use `flush=True` and `sys.stdout.flush()` for long simulations
4. **Git History**: Each experiment committed enables clean revert of failed attempts
5. **Metric Consistency**: Always extract metric from same location/format

## Time Considerations

- Single scenario: ~10 seconds
- Full 21-scenario run: ~10 minutes
- Budget per experiment: 2 minutes recommended for quick iteration
