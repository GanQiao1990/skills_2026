---
name: synthetic-biology-bayesian-optimization
description: Autonomous closed-loop Bayesian optimization for metabolic engineering designs. Searches over process parameters + strain designs using Gaussian Process surrogate models and Expected Improvement acquisition.
version: 1.0
created: 2026-04-22
author: Hermes Agent (Nous Research)
use_case: Maximize metabolite production (e.g., arginine) via dynamic regulatory circuits (NarL, etc.)
reusable: true
---

# Synthetic Biology Bayesian Optimization Loop

**Purpose**: Autonomous closed-loop optimization of metabolic engineering designs using Gaussian Process surrogate modeling and acquisition functions. Maximize production titers (or any objective) by searching over:

- Continuous process parameters (NarL circuit kinetics, feed rates, switching times)
- Categorical strain designs (gene knockouts/overexpressions)
- Multi-objective weighted combinations (titer, yield, productivity)

---

## Umbrella scope for metabolic autoresearch optimization

This skill is the class-level umbrella for autonomous metabolic-engineering optimization campaigns. It covers closed-loop Bayesian optimization, simulator wrappers, parameter overrides, calibration, campaign monitoring, and post-run interpretation. Narrow siblings about virtual metabolic optimization, transcription-factor scans, and campaign audits have been absorbed as labeled subsections and detailed references.

### Subsection: calibrated virtual metabolic optimization
When simplified FBA/dFBA outputs are far below fermentation-scale titers, use an explicit calibration factor rather than overcomplicating the fast simulator. Keep raw and calibrated values separate in logs/reports. For existing completed runs, prefer fast log-analysis and visualization pipelines over rerunning BO.

### Subsection: transcription-factor dynamic control
For TF-controlled production pathways, stronger induction is not always better. Always scan expression/activity factors below and above literature defaults, especially when the TF regulates both target and competing pathways. Look for intermediate sweet spots and interpret declines through cofactor competition, toxicity, or saturated flux.

### Subsection: campaign audit and convergence assessment
When multiple campaign directories exist, discover all runs, read budgets/completed counts, recover calibration factors, compare best configurations side-by-side, and assess whether incomplete runs have converged. Do not compare calibrated numbers without noting the factor and simulation horizon.

### Demoted support references
- `references/virtual-metabolic-optimization.md`
- `references/metabolic-campaign-audit.md`
- `references/metabolic-engineering-transcription-factor-optimization.md`

## When to Use

Use this skill when:
- You have a **working metabolic simulator** (FBA/dFBA/ODE) that can be invoked from CLI
- Objective is a **continuous real-valued function** of design parameters
- Parameter space is **moderate-dimensional** (5-20 dims) and **expensive to evaluate** (> 1 min per run)
- You need to **surpass manual tweaking** and find global optima efficiently

**Do NOT use** for:
- Linear systems (use linear programming directly)
- Very high-dim spaces (>50 genes) without dimension reduction
- Stochastic simulators requiring >100 replicates per condition

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Autonomous Research Loop (autoresearch_loop.py)       │
├─────────────────────────────────────────────────────────┤
│  1. Design space definition (SPACE dict + STRAIN_LIST) │
│  2. Initial sampling (Latin Hypercube, N=20)            │
│  3. Simulation executor (run_simulation)                │
│  4. GP surrogate fitting (scikit-learn)                 │
│  5. Acquisition (Expected Improvement + Thompson)       │
│  6. Batch proposal (diversity constraint on strain)     │
│  7. Convergence check → final report                    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  Parameter Override Mechanism (two-way)                 │
├─────────────────────────────────────────────────────────┤
│  Option A: JSON override file                           │
│    → write narl_nadph_circuit_params_override.json      │
│    → module imports PARAM_OVERRIDE at runtime           │
│                                                          │
│  Option B: Environment variables                        │
│    → NARL_O2_STAGE2_FRAC, NARL_GROWTH_COUPLING, etc.   │
│    → simulator reads via os.environ()                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  Target Simulator (two_stage_simulation.py)             │
├─────────────────────────────────────────────────────────┤
│  - Accepts CLI args (--strain, --no3, --t-switch)      │
│  - Reads overrides at import time                       │
│  - Prints key=value summary to stdout                   │
│  - Saves trajectory CSV for later analysis              │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Pattern

### 1. Define Search Space

```python
SPACE = {
    "Kd_no3":          (0.3, 3.0),      # continuous: [min, max]
    "Ki_no2":          (10.0, 60.0),
    "n_hill":          (1.5, 3.5),
    "aerobic_damping": (0.25, 0.6),
    "t_switch":        (6, 18),
    "no3_bolus":       (30.0, 150.0),
    "o2_stage2_frac":  (0.01, 0.10),
    "growth_coupling": (0.05, 0.20),
}
# Categorical variable handled separately via STRAIN_WEIGHTS
```

### 2. Parameter Override Module

Create `narl_nadph_circuit_params_override.py` in the simulator directory:

```python
try:
    from narl_nadph_circuit_params_override import PARAM_OVERRIDE
except ImportError:
    PARAM_OVERRIDE = {}

# In the simulation function:
narl_kwargs = dict(
    Kd_no3=PARAM_OVERRIDE.get("Kd_no3", 1.0),
    Ki_no2=PARAM_OVERRIDE.get("Ki_no2", 30.0),
    n_hill=PARAM_OVERRIDE.get("n_hill", 2.0),
    aerobic_damping=PARAM_OVERRIDE.get("aerobic_damping", 0.4),
)
narl_p = compute_narl_p_biphasic(no3_c, no2_c, aerobic=aerobic, **narl_kwargs)
```

### 3. Simulation Wrapper

```python
def run_simulation(design: Design) -> Result:
    """Execute one simulation and parse output."""
    write_param_override(design)  # writes JSON file

    cmd = [
        "PYTHONNOUSERSITE=1", "/path/to/python",
        "two_stage_simulation.py",
        "--strain", design.strain,
        "--no3", f"{design.no3_bolus:.2f}",
        "--t-switch", f"{design.t_switch:.2f}",
        "--out", str(out_csv),
    ]
    result = subprocess.run(" ".join(cmd), ...)

    # Parse key=value output
    summary = {}
    for line in result.stdout.splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            try:
                summary[k.strip()] = float(v.strip())
            except ValueError:
                pass
    return Result(**summary)
```

### 4. Gaussian Process Surrogate

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
from sklearn.preprocessing import StandardScaler

def build_X(designs: List[Design], strain_names: List[str]) -> np.ndarray:
    """8 continuous + one-hot strain encoding."""
    X = []
    for d in designs:
        row = [d.Kd_no3, d.Ki_no2, ..., d.growth_coupling]
        row.extend([1.0 if d.strain == s else 0.0 for s in strain_names])
        X.append(row)
    return np.array(X)

def fit_gp(X, y):
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    kernel = ConstantKernel(1.0) * Matern(length_scale=1.0, nu=2.5) + WhiteKernel()
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=5)
    gp.fit(Xs, y)
    return gp, scaler
```

### 5. Acquisition Function (Expected Improvement)

```python
from scipy.stats import norm

def expected_improvement(gp, scaler, X, y_best, xi=0.01):
    Xs = scaler.transform(X)
    mu, sigma = gp.predict(Xs, return_std=True)
    sigma = np.maximum(sigma, 1e-9)
    imp = mu - y_best - xi
    Z = imp / sigma
    ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
    return ei
```

### 6. Batch Proposal with Diversity

```python
def propose_batch(gp, scaler, X_history, y_history, n=5):
    candidates = [sample_random() for _ in range(200)]
    X_cand = build_X(candidates, strain_names)

    ei = expected_improvement(gp, scaler, X_cand, y_best)
    ts = np.random.normal(*gp.predict(Xs_cand, return_std=True))  # Thompson
    score = 0.7 * ei + 0.3 * ts

    # Strain diversity: max 2 per strain per batch
    selected = []
    strain_counts = {}
    for idx in np.argsort(-score):
        cand = candidates[idx]
        if strain_counts.get(cand.strain, 0) < 2:
            selected.append(cand)
            strain_counts[cand.strain] = strain_counts.get(cand.strain, 0) + 1
        if len(selected) >= n:
            break
    return selected
```

---

## Directory Layout

```
basic_pathway_e_coli/
├── scripts/
│   ├── narl_nadph_circuit.py                  (existing simulator core)
│   ├── two_stage_simulation.py                (existing FBA driver, MODIFIED)
│   ├── narl_nadph_circuit_params_override.py  (NEW: dynamic param loader)
│   ├── autoresearch_loop.py                   (NEW: BO main loop)
│   └── run_batches.py                         (NEW: batch manager)
├── results/autoresearch/
│   ├── autoresearch_log.jsonl                 (full history)
│   ├── autoresearch_best.json                 (optimal config)
│   ├── OPTIMIZATION_REPORT.md                 (human summary)
│   └── figures/
│       ├── convergence.png
│       └── parallel_coords.png
└── run_persistent_autoresearch.sh             (launcher)
```

---

## Key Decisions & Rationale

| Decision | Rationale | Alternative Considered |
|----------|-----------|----------------------|
| **Gaussian Process surrogate** | Smooth, differentiable, built-in uncertainty quantification | Random Forest (less smooth), Neural Net (needs more data) |
| **Expected Improvement acquisition** | Balances exploitation (high μ) and exploration (high σ) | Pure EI (too greedy), UCB (requires β tuning) |
| **Latin Hypercube initial sampling** | Better space coverage than pure random | Sobol sequences (similar, but LHS simpler) |
| **One-hot strain encoding** | Treats strain as categorical, not ordinal | Embedding (overkill for 7 choices) |
| **Weighted multi-objective** | Titer primary, yield/productivity as tie-breakers | Pareto frontier (harder to pick single "best") |
| **JSON override file** | No need to edit simulator source; easy to inspect | Direct patching (fragile), CLI args (too many) |
| **Batch size = 5, total = 50** | ~30-60 min runtime; enough for GP to converge | Larger batches (faster but less adaptive) |
| **Environment variables for process params** | Simple, no code changes needed | Config file (needs more plumbing) |

---

## Common Pitfalls & Fixes

### Pitfall 1: Simulator output format mismatch
**Symptom**: `json.loads()` fails, `"Expecting value: line 1 column 3"`
**Cause**: Simulator prints human-readable table (`key = value`), not JSON
**Fix**: Parse line-by-line: `for line in stdout: if '=' in line: key, val = line.split('=', 1)`

### Pitfall 2: Parameter override not taking effect
**Symptom**: Simulations all use default Kd_no3=1.0 despite override file present
**Cause**: `two_stage_simulation.py` doesn't import `PARAM_OVERRIDE`
**Fix**: Add `try: from ...override import PARAM_OVERRIDE` at module level; use `PARAM_OVERRIDE.get(key, default)` in `compute_narl_p_biphasic` call

### Pitfall 3: Process dies after shell exits
**Symptom**: Background job killed when terminal disconnects
**Cause**: Process receives SIGHUP
**Fix**: Use `nohup` + `&`, `screen -dmS`, or double-fork daemon pattern

### Pitfall 4: Strain diversity depletion
**Symptom**: BO proposes same strain (e.g., Full_Optimised) 5/5 in a batch
**Cause**: Acquisition score dominated by one strain's region
**Fix**: Diversity constraint in `propose_batch`: `if strain_counts[strain] < 2: accept`

### Pitfall 5: GP numerical instability
**Symptom**: `LinAlgError: Cholesky decomposition failed`
**Cause**: X matrix poorly scaled or duplicate rows
**Fix**: Always `StandardScaler` transform X; add jitter to kernel (`WhiteKernel(noise_level=0.05)`)

### Pitfall 6: No convergence after 50 runs
**Symptom**: Best objective keeps improving, no plateau
**Cause**: Search space too large or simulator too noisy
**Fix**: Increase budget to 100; add priors (e.g., Kd_no3 likely ~1.0 from literature); narrow bounds based on pilot runs

---

## Adapting to Other Systems

To apply this framework to a different metabolic engineering project:

1. **Replace the simulator**: Modify `run_simulation()` to call your model (COBRApy, kinetic ODE, etc.)
2. **Define your design space**: Update `SPACE` dict with your continuous parameters (promoter strengths, induction levels, temperatures)
3. **Enumerate your strain panel**: Replace `STRAIN_PANEL` / `STRAIN_WEIGHTS` with your genetic designs
4. **Choose objective**: Modify `objective_score()` weights or replace with custom function
5. **Ensure output parsing**: Make sure `run_simulation()` can extract metrics from your simulator's stdout

**Example adaptation**: Optimize lysine production in *C. glutamicum*
- Simulator: `cgl_lysine_fba.py`
- Parameters: `Kd_lysG`, `feedback_resistance`, `glc_feed_rate`, `switch_time`
- Strains: `WT`, `Δldh`, `Δpyc`, `lysC*`, `pntAB↑`
- Objective: weighted(titer, yield, productivity)

---

## Directory Layout

```
basic_pathway_e_coli/
├── scripts/
│   ├── narl_nadph_circuit.py                  (existing simulator core)
│   ├── two_stage_simulation.py                (existing FBA driver, MODIFIED)
│   ├── narl_nadph_circuit_params_override.py  (NEW: dynamic param loader)
│   ├── autoresearch_loop.py                   (NEW: BO main loop)
│   └── run_batches.py                         (NEW: batch manager)
├── results/autoresearch/
│   ├── autoresearch_log.jsonl                 (full history)
│   ├── autoresearch_best.json                 (optimal config)
│   ├── OPTIMIZATION_REPORT.md                 (human summary)
│   └── figures/
│       ├── convergence.png
│       └── parallel_coords.png
└── run_persistent_autoresearch.sh             (launcher)
```

---

## Performance Expectations

| System | Avg eval time | Budget | Total wall time | Expected improvement |
|--------|---------------|--------|-----------------|---------------------|
| Small GEM (iML1515) | 10-30 s | 50 | 15-30 min | 20-40% over manual |
| Kinetic ODE (≤20 states) | 1-5 min | 30 | 1-3 h | 30-60% |
| Full-cell model | 10-30 min | 20 | 3-10 h | 50-100% |

**Note**: First 20 LHS samples are embarrassingly parallelizable across CPU cores or cluster nodes.

---

## Validation & Quality Control

Before trusting the optimal configuration:

1. **Replicate run**: Execute `two_stage_simulation.py` manually with the best parameters; verify titer matches log
2. **Sensitivity check**: Vary each parameter ±10% around optimum; identify brittle dimensions
3. **Strain robustness**: Test top-3 strains at nearby NO₃⁻ doses (±10 mM) to confirm window
4. **Trajectory inspection**: Plot `results/autoresearch_runs/traj_*.csv` for biological plausibility (no negative concentrations, monotonic biomass)

---

## Extensions (Future Work)

- **Multi-fidelity optimization**: Mix cheap FBA (n=100) with expensive dFBA (n=20) via COBOSS
- **Transfer learning**: Warm-start GP from previous organism optimization (e.g., from *E. coli* to *C. glutamicum*)
- **Constraint handling**: Add infeasibility penalty for models failing to find FBA solution
- **Interactive mode**: Real-time dashboard (Plotly Dash) showing live Pareto frontier
- **Experiment suggestion**: Rank top-N unmet conditions by Expected Improvement for lab validation

---

## References

- **Bayesian Optimization**: Snoek et al. (2012) "Practical Bayesian Optimization of Machine Learning Algorithms"
- **Surrogate modeling for metabolic engineering**: Wang et al. (2021) "Bayesian optimization of fermentation conditions"
- **NarL circuit**: Chen et al. (2022) *Metabolic Engineering*; Monk et al. (2017) *Nature Biotechnology* (iML1515)

---

**Skill version**: 1.0  
**Last updated**: 2026-04-22  
**Use case**: E. coli arginine pathway maximization via NarL dynamic regulation  
**Reusable**: Yes — drop-in replacement for any FBA/dFBA wrapper
