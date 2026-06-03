# AIVM timeout diagnosis and visualization pattern

Use this note when a Python/cobra virtual-cell workflow seems to produce no output, especially in multi-scenario amino-acid production mimic tasks.

## Problem pattern
A script appears silent or incomplete even though it is still progressing. Common cause: total runtime exceeds the foreground timeout, so the terminal truncates execution before final summary/CSV writes are observed.

## Durable workflow
1. Reproduce with direct progress visibility.
   - Add explicit prints before the long loop:
     - `Loaded model from ...`
     - `Running N scenarios...`
     - `[i/N] scenario_id | label`
2. Profile a few representative scenarios first.
   - Measure seconds per scenario.
   - Estimate total runtime as `avg_seconds_per_scenario * scenario_count`.
3. Distinguish timeout from crash.
   - If partial progress lines appear and no traceback is emitted, treat timeout as the primary hypothesis.
   - Do not call it a stack/hang without evidence.
4. Rerun with enough timeout to finish.
5. Verify outputs explicitly.
   - Check for CSV/JSON result tables.
   - Separately check whether figure files exist; do not assume visualization was generated.
6. If visualization is missing, generate it from the result tables.

## Applied pattern in this session
Target script:
- `/home/qiao/qiao_design/e_coli_model/narl_virtual_metabolic/aivm_virtual_amino_acid_cell.py`

Observed behavior:
- ~18 s per scenario
- 21 scenarios total
- estimated total runtime ~379 s (~6.3 min)
- earlier 300 s foreground runs timed out after partial progress, so the script looked silent/incomplete but was not deadlocked

## Figure set generated from result tables
From:
- `outputs/virtual_amino_acid_summary.csv`
- `outputs/virtual_amino_acid_timecourse.csv`

Create:
1. `virtual_amino_acid_improvement_barplot.(png|pdf)`
   - improvement vs low O2 baseline by product and strategy
2. `virtual_amino_acid_mechanism_heatmap.(png|pdf)`
   - normalized proxy comparison across product AUC, nitrogen assimilation, redox, pathway proxy
3. `virtual_amino_acid_timecourse_panels.(png|pdf)`
   - product flux and biomass proxy over time for key strategy labels
4. `virtual_amino_acid_dashboard.(png|pdf)`
   - one-page combined overview for proposal/internal slide use

## Interpretation guardrail
These figures visualize first-pass proxy outputs, not a full mechanistic NarL/NtrC phosphorylation → transcription → metabolism model.
State explicitly:
- NarL is approximated through nitrate/nitrite respiration constraints
- NtrC-like control is approximated through nitrogen-assimilation capacity changes
- enzyme-complex proximity is approximated through pathway-capacity boosts

## Why this matters
For this user class, the correct answer is not only "the script ran" but also:
- whether missing output was caused by timeout vs crash
- whether visualization has actually been completed
- where the concrete output files live
