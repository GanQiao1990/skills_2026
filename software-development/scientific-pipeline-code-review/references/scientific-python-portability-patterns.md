# Scientific Python portability patterns

Concise patterns reinforced by the `basic_pathway_e_coli` remediation session.

## 1. Anchor outputs at repository root, not script directory

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIGURES_DIR = ROOT / "figures" / "autoresearch"
RESULTS_DIR = ROOT / "results" / "autoresearch"
MODELS_DIR = ROOT / "models"
```

Use this when scripts live under `repo/scripts/` but the canonical artifacts belong under top-level `figures/`, `results/`, or `models/`.

## 2. Replace hard-coded interpreters with override-aware selection

```python
import os, sys
PYTHON = os.environ.get("AUTORESEARCH_PYTHON", sys.executable)
```

Good for batch runners, daemon launchers, and subprocess-based simulation loops.

## 3. Pass env vars via `env`, not via `shell=True`

```python
import os, subprocess

env = os.environ.copy()
env["PYTHONNOUSERSITE"] = "1"
cmd = [PYTHON, str(HERE / "two_stage_simulation.py")]
subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(HERE))
```

Avoid:

```python
cmd = ["PYTHONNOUSERSITE=1", "/home/user/anaconda3/bin/python", "script.py"]
subprocess.run(" ".join(cmd), shell=True)
```

## 4. Preserve legacy aliases without letting them crash samplers

When `STRAIN_PANEL` or another registry contains legacy names needed for historical compatibility, give those entries explicit zero weights instead of omitting them from the weight table.

```python
STRAIN_LIST = list(STRAIN_PANEL.keys())
STRAIN_WEIGHTS = {
    "WT": 0.0,
    "Canonical": 0.5,
    "Canonical_Optimised": 0.5,
    "LegacyAlias": 0.0,
}
```

This prevents `KeyError` during weighted sampling while keeping old names representable in history and reports.

## 5. Distinguish missing file vs wrong schema

```python
REQUIRED_COLUMNS = {"feeding_regime", "gene_expr_boost", "citrulline_pool"}

for path in candidates:
    if path.exists():
        df = pd.read_json(path, lines=True)
        missing = sorted(REQUIRED_COLUMNS - set(df.columns))
        if missing:
            raise ValueError(f"{path} exists but is missing columns: {missing}")
        return df
raise FileNotFoundError("No compatible dataset found")
```

This prevents misleading debugging when a results artifact exists but belongs to a different pipeline branch.
