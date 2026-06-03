# Archived skill: metabolic-engineering-transcription-factor-optimization

Original path: `metabolic-engineering/metabolic-engineering-transcription-factor-optimization`

---

---
name: metabolic-engineering-transcription-factor-optimization
description: "Systematic optimization of transcription-factor-regulated metabolic production pathways using dynamic simulation. Pattern: literature assumptions about TF overexpression may be suboptimal — always scan TF activity levels (genetic and dynamic) before finalizing strain design."
license: MIT
category: metabolic-engineering
tags: [optimization, transcription-factor, simulation, metabolic-engineering, narL, dfba]
---

# Transcription Factor Dynamic Control Optimization

## When to Use This Skill

Use this workflow when optimizing a metabolic production pathway that is controlled by a transcription factor (TF), especially when:

1. The TF regulates **both the target pathway and off-target/competing pathways** (e.g., NarL activates nitrate respiration but also influences other nitrogen metabolism genes)
2. The TF **induction strategy is borrowed from literature** (e.g., "overexpress NirBD 3x" from a paper in a different organism)
3. You are implementing **dynamic control** (TF activity changes over time or in response to an inducer like NO3-)
4. You are using **dFBA/kinetic simulation** to evaluate strain designs before wet-lab construction
5. You observe a **non-monotonic response** — titer increases with inducer up to a point, then declines

**Do NOT use** for static gene knockouts without regulatory dynamics, or for pure TF screening at the genomic level (use `hypothesis-generation` instead).

---

## Core Principle: The TF Sweet Spot

Stronger activation is NOT always better.

For TFs with pleiotropic effects (regulating both beneficial and deleterious genes), maximum production often occurs at an **intermediate activity level**, not maximum. The optimum balances:

- **Positive**: Target pathway activation, redox balancing, stress response
- **Negative**: Off-target repression, resource competition (ATP/NAD(P)H), toxicity from induced byproducts

The default literature value (e.g., "overexpress 3x") may place you on the **declining limb** of the dose–response curve.

---

## The Optimization Workflow

### Step 1: Baseline Dose–Response Mapping

Run your baseline strain across a grid of **inducer concentration**. Record: Inducer → Titer + TF activity metric.

Identify the peak and the declining phase. Note the TF activity at that peak.

### Step 2: Hypothesis — "Default factor overshoots?"

If your design includes a **fixed TF overexpression factor** (e.g., `nirbd_factor=3`), ask:

> Is factor 3 exceeding the optimal activity window identified in Step 1?

### Step 3: Factor Scan Experiment

Systematically scan the **overexpression factor** across a range that brackets native expression:

```
Scan levels: [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0]
  - 0.0 = knockout
  - 1.0 = native expression
  - 3.0 = typical literature default
  - 5.0 = extreme overexpression
```

Run at:
- the **optimal inducer dose** (from Step 1)
- a **supra-optimal/high dose** where negative effects may magnify

Output should include: factor, titer, TF activity, peak byproduct (e.g., NO2-), key cofactor balance.

### Step 4: Locate the Optimum

Typical finding: plateau or maximum at **factor 0.5–1.5**, below factor-3 defaults.

If factor 1.0 (native) beats factor 3.0 by >10%, you have a **high-confidence design correction**.

### Step 5: Redefine the Strain

Create a new strain variant with `factor = optimal_value` (often 1.0). Keep all other genomic modifications unchanged.

Rerun full comparison and dose–response to confirm improvement.

### Step 6: Mechanistic Interpretation

Explain *why* the lower factor is better:

- **Co-factor competition**: Overexpressed enzyme consumes NADH/ATP needed elsewhere
- **Linear induction vs. saturated pathway**: pathway flux already maxed; extra enzyme does nothing
- **Toxicity escalation**: Product/intermediate accumulates beyond tolerable threshold

---

## Required Simulation Infrastructure

Your simulator must support:

1. **Per-step TF activity readout** (e.g., a number in [0, 1])
2. **Flux-proportional TF control**: Ability to set a **minimum flux** for TF-induced reactions, not just upper bounds:
   ```python
   if factor > 1.0:
       _force_minimum_flux(reaction, min_flux=base_flux * (factor - 1.0))
   ```
3. **Dynamic coupling**: TF activity updates each dFBA step (not static at t=0)
4. **Niched experiment runner**: Code to run the same protocol across a factor grid automatically

---

## Red Flags — When Optimization is Not Yet Complete

- Titre keeps increasing with factor → you haven't reached the downside; test higher factors
- Titre maximum at **factor = 0** (knockout) → TF is net negative; consider decoupling it
- TF activity > 0.85 across entire inducer range → kinetics need recalibration
- Peak titer at **zero inducer** → inducible system leaky or TF's positive effects overwhelmed
- No difference between 0.5x and 1.0x → native expression already exceeds saturation

---

## Case Study: NarL + NirBD Arginine Project

**Project**: `basic_pathway_e_coli/` — E. coli arginine production with NarL two-stage control.

### Discovery

- Literature precedent (Chen et al. 2022): overexpress NirBD 3x to detoxify nitrite
- Simulation at 60 mM NO3-: factor 3 gave 2.21 g/L; native (factor 1.0) gave **2.79 g/L (+26%)**
- Counterintuitive: NirBD consumes NADH under microaerobic conditions, competing with NarGHI nitrate respiration and PntAB NADPH production

### Actions Taken

1. Ran `scripts/nirbd_factor_scan.py` across 8 factors at two NO3- doses
2. Found optimal plateau at **factor 0.5–1.0** (native expression)
3. Added `Full_Optimised` strain to `STRAIN_PANEL` with `nirbd_factor=1.0`
4. Predicted 2.456 g/L at 40 mM NO3- (recovering +PntAB advantage while keeping NO2- low)

### Insight

For TFs that induce both a beneficial pathway **and** a cofactor-consuming enzyme, the net benefit can reverse at high induction. Always **validate literature factors with a downward scan** as well as upward.

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Only scanning upward (1x, 3x, 5x) | Misses optimum at 0.5–1.0 | Include 0.0, 0.5, 1.0 always |
| Assuming native is always best | Might miss 1.5–2.0 benefit | Still scan 1.5, 2.0, 3.0 |
| Not pairing with high-dose test | Can't see context-dependence | Test both optimal and supra-optimal inducer |
| Forgetting cofactor bookkeeping | Misdiagnosing cause of decline | Track NADH/NADPH/ATP balance |
| Static TF model (set only at t=0) | Misses dynamic biphasic effects | Update TF activity every dFBA step |

---

## Related Skills

- `hypothesis-generation`: Mechanistic explanations for *why* a TF optimum shifted
- `protein-design-workflow`: Engineering the TF protein itself (not just its expression level)
- `scientific-brainstorming`: Creative interpretation of non-monotonic results
- `statistical-analysis`: Confidence intervals on sensitivity scans; Morris/Sobol methods
