# Archived skill: metabolic-campaign-audit

Original path: `metabolic-engineering/metabolic-campaign-audit`

---

---
name: metabolic-campaign-audit
description: "Audit and synthesize the state of multiple parallel metabolic optimization campaigns, reconciling calibration factors, comparing results across configurations, and assessing convergence even from incomplete runs."
license: MIT
category: metabolic-engineering
tags: [metabolic-engineering, optimization, audit, bayesian-optimization, campaign-management, state-assessment]
---

# Metabolic Optimization Campaign Auditor

## When to Use This Skill

Use when you need to answer **"How are the optimization results?"** or **"What's the current state?"** in a computational biology project with:

- **Multiple parallel optimization campaigns** (e.g., base 50-round vs enhanced 1000-round)
- **Calibrated simulation outputs** (simulated units × factor → literature-grounded values)
- **Scattered result directories** (`results/` vs `scripts/results/`, nested runs)
- **Incomplete runs** (e.g., 174/1000 completed) requiring convergence assessment
- **Need for quick synthesis** across reports, JSON logs, CSV trajectories, and figures

**Typical trigger**: User asks "How's the virtual metabolism task going?" after weeks of background optimization.

**Do NOT use** for single-run projects, pure literature reviews, or when all results fit in one directory.

---

## What This Skill Does

Given a project root path, it will:

1. **Discover all optimization campaigns** by signature detection:
   - `autoresearch_loop.py` vs `autoresearch_loop_enhanced.py`
   - `results/autoresearch/` (base outputs)
   - `scripts/results/autoresearch_runs/` (enhanced batch outputs)
   - `daemon_autoresearch.py` background runner presence

2. **Extract campaign metadata** for each:
   - Total budget (from `N_INITIAL + N_ITER * BATCH_SIZE` in script or best.json)
   - Completed simulation count (from `autoresearch_log.jsonl`)
   - Calibration factor (`TITER_CALIBRATION_FACTOR` or `calibration_factor` in metadata)
   - Search space ranges (Kd_no3, Ki_no2, no3_bolus, t_switch, etc.)
   - Script variant (base vs enhanced — different T_FINAL, objectives)

3. **Identify optimal configuration** from each campaign:
   - Read `autoresearch_best.json`
   - Extract: `strain`, `arg_titer_g_L` (calibrated), `no3_bolus`, `t_switch`, NarL params, yields
   - Compute true titer: `titer_calibrated / calibration_factor`
   - Note biomass, NO2 peak, NarL~P level for mechanistic interpretation

4. **Compare campaigns side-by-side**:
   - Table: Campaign | Completed | Budget | Best Titer (true) | Best Titer (cal) | Strain | NO3 | t_sw
   - Relative improvement from baseline (typically 2.79 g/L arginine)
   - Shifts in optimal strain choice or parameter ranges between campaigns

5. **Assess convergence** if incomplete:
   - Count `traj_*.csv` files in `autoresearch_runs/`
   - Show recent best from log.jsonl
   - Estimate remaining time assuming ~5-10 sims/minute
   - Look for saturation in learning curves if figures exist

6. **Generate executive summary**:
   - Key discoveries (e.g., "optimal strain shifted from Full_Optimised to ArgEng+dSthA+PntAB")
   - Parameter trends (NO3 window right-shifted, Ki_no2 bounds, t_switch extension)
   - Recommendation: continue to X rounds or stop now
   - Wet-experiment validation priority list

---

## Output Structure

The skill produces a markdown report with these sections:

```markdown
📊 Campaign Audit — <Project Name>
├── Campaign 1: <name> (<completed>/<budget> = <pct>%)
│   └── Best: <strain> @ NO3=<no3>mM, t_sw=<t>h → <titer_cal> g/L (<titer_true> g/L true)
├── Campaign 2: ...
└── Cross-Campaign Insights
    ├── Strain ranking across campaigns
    ├── Parameter drift analysis
    └── Convergence assessment
```

**Key numeric fields**:
- `true_titer`: simulated mM value converted via titer = arg_mM × MW × VOL / V (or calibration division)
- `calibrated_titer`: value in best.json that may be scaled to match literature
- `relative_improvement`: (true_titer - baseline) / baseline × 100%

---

## Implementation Pattern

```python
def audit_campaigns(project_root: Path):
    campaigns = []

    # 1. Discovery
    for candidate in [project_root / "results/autoresearch",
                      project_root / "scripts/results/autoresearch_runs"]:
        if candidate.exists():
            campaigns.append(discover_campaign(candidate))

    # 2. Extract metadata per campaign
    for c in campaigns:
        c['budget'] = read_budget_from_script_or_json(c)
        c['completed'] = count_jsonl_lines(c['log_path'])
        c['cal_factor'] = read_calibration_factor(c)
        c['best'] = read_best_config(c['best_json'])

    # 3. Reconciled comparison table
    table = []
    for c in campaigns:
        table.append({
            'campaign': c['name'],
            'completed': c['completed'],
            'budget': c['budget'],
            'titer_cal': c['best']['arg_titer_g_L'],
            'titer_true': c['best']['arg_titer_g_L'] / c['cal_factor'],
            'strain': c['best']['strain'],
            'no3': c['best']['no3_bolus'],
            't_switch': c['best']['t_switch']
        })

    # 4. Convergence hint
    convergence_note = assess_convergence(campaigns)

    return format_report(table, convergence_note)
```

### File Patterns Recognized

| Pattern | Meaning |
|---------|---------|
| `autoresearch_loop.py` | Base 50-round campaign (N_INITIAL=100, N_ITER=180? Actually 50) |
| `autoresearch_loop_enhanced.py` | 1000-round campaign (N_INITIAL=100, N_ITER=180, T_FINAL=48h) |
| `results/autoresearch/autoresearch_best.json` | Base campaign summary |
| `scripts/results/autoresearch_runs/traj_*.csv` | Enhanced per-simulation trajectories |
| `scripts/results/autoresearch_runs/*.summary.json` | Enhanced per-simulation metrics |
| `narl_nadph_circuit_params_override.py` | Dynamic parameter injection during BO |

### Calibration Factor Recovery

The factor is found in:
1. `best.json → metadata.calibration_factor` (base)
2. `autoresearch_loop_enhanced.py → TITER_CALIBRATION_FACTOR = 22.67` comment
3. If absent, assume factor=1.0 (raw simulation units)

**Formula**: `true_g_per_L = calibrated_g_per_L / calibration_factor`

---

## Common Scenarios & Interpretations

### Scenario 1: Two campaigns, different optima
```
Base (50 rounds):   Full_Optimised @ 53 mM → 95 g/L (cal) = 4.19 g/L (true)
Enhanced (174/1000): ArgEng+dSthA+PntAB @ 87 mM → 114 g/L (cal) = 5.01 g/L (true)
```
**Interpretation**: Enhanced search space (40-180 mM NO3) discovered higher-dose regime benefits. Strain shift suggests ΔsthA+PntAB synergy outweighs astCADBE knockdown under high NO3.

**Action**: Continue enhanced run; baseline already superseded.

---

### Scenario 2: Calibrated value exceeds literature
```
Target: 108.3 g/L
Current best (calibrated): 114 g/L
```
**Interpretation**: Calibration factor may be too conservative, or simulation genuinely exceeds known strains. Check:
- Is factor derived from `108.3 / 4.78 = 22.67`? Then current 5.01 true → 113.5 cal is **above** literature.
- Could be real: strain engineering + dynamic control surpasses prior art.
- Or factor needs adjustment: re-fit using a known benchmark strain.

**Action**: Verify calibration by simulating the benchmark strain (e.g., ArgEng baseline) and comparing to literature.

---

### Scenario 3: Incomplete run already converged
```
Top-5 titers: 5.01, 4.80, 4.78, 4.71, 4.54  (gap < 0.5)
```
**Interpretation**: Marginal gains diminishing; early stopping justified.

**Action**: Generate final report; move to validation.

---

### Scenario 4: Large variance, poor convergence
```
Mean titer: 2.9 g/L, Std: 0.95 g/L (33% CV)
Best: 5.01, Median: 2.72 → heavily right-skewed
```
**Interpretation**: Many poor designs sampled; search space vast. Need more rounds.

**Action**: Continue to 500+ rounds; consider narrowing search space.

---

## Pitfalls & Gotchas

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Confusing campaign directories** | `results/` vs `scripts/results/` look similar | Always check parent path; they are separate campaigns |
| **Misreading calibration** | Reporting 95 g/L as real | Divide by `calibration_factor` before comparing to papers |
| **Ignoring simulation duration** | Base uses 36h, enhanced 48h | Direct titer comparison invalid unless normalized per hour |
| **Assuming design params saved** | Can't find NO3 dose for top design | Infer from filename `no<design_id>` or regenerate from BO log |
| **Daemon running unnoticed** | "Only 174 rounds" but daemon adds more | Check `ps aux | grep autoresearch` before concluding |

---

## Related Skills

- `metabolic-engineering-transcription-factor-optimization` — the **mechanistic insight** behind why optima shift (NirBD factor 1.0 beats 3.0)
- `scientific-brainstorming` — hypothesizing why a parameter drift occurred
- `statistical-analysis` — formal convergence metrics (EI acquisition variance, improvement rate)
- `wet-experiment-design` — translating top 3 simulated configurations into lab protocols

---

## Example Report Snippets

**Two-campaign comparison:**
```
📊 E. coli Arginine NarL Optimization — Campaign Audit

Campaign Base (results/autoresearch/)
  └─ 50/50 rounds ✓  Best: Full_Optimised @ 53 mM NO3, t=18.9h
     → 4.19 g/L true (95 g/L cal) | +50% vs baseline

Campaign Enhanced (scripts/results/autoresearch_runs/)
  └─ 174/1000 rounds (17%)  Best: ArgEng+dSthA+PntAB @ ~87 mM, t≈20h
     → 5.01 g/L true (114 g/L cal) | +80% vs baseline

🔬 Key Insight: Optimal strain shifted as NO3 window expanded.
   Full_Optimised excels at moderate NO3 (50-70 mM).
   ArgEng+dSthA+PntAB dominates at high NO3 (80-100 mM) where PntAB's
   NADPH rescue outweighs astCADBE repression.

⏭️  Recommendation: Continue Enhanced to 500 rounds.
   Current top-5 gap = 0.5 g/L; likely 0.2-0.3 g/L remaining gain.
   Expected final best: 5.3-5.6 g/L true (120-127 g/L cal).
```
