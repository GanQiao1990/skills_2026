# 108 g/L high-producing chassis simulation-control data package pattern

Use when the user asks for “从 108 g/L 高产菌出发的模拟调控数据”, “108g/l 高产菌模拟调控数据”, or wants a reusable dataset rather than only prose interpretation in `/home/qiao/qiao_design/e_coli_model/basic_pathway_e_coli`.

## Durable lesson
For NarL/NO3/NADPH/arginine tasks on the validated high-producing lineage, a useful deliverable is not only an evidence report or comparison table, but also a clean simulation-control data package extracted specifically from the 108 g/L chassis lineage.

## Scope restriction
Restrict the package to:
- `Arg10_108gL_Validated`
- `Arg10_108gL_Validated_dSthA`
- `Arg10_108gL_Validated_dSthA_PntAB`
- `Arg10_108gL_Validated_dSthA_PntAB_NirBD`
- `Arg10_108gL_Validated_NarLFull`
- `Arg10_108gL_Validated_NarLFull_Optimised`

Do not drift back to WT-centric framing unless the user explicitly asks for WT context.

## Preferred outputs
Write both:
1. a machine-readable CSV
2. a markdown summary explaining fields and highlighting key rows

Suggested filenames in the project root:
- `ARG10_108GL_VALIDATED_SIMULATION_CONTROL_DATA.csv`
- `ARG10_108GL_VALIDATED_SIMULATION_CONTROL_DATA_SUMMARY.md`

## Source files to merge
Primary sources:
- `results/strain_comparison.csv`
- `results/narl_phospho_control/narl_control_comparison_table.csv`
- `results/narl_phospho_local_search/top10_local_search.csv`
- `results/narl_phospho_local_search/best_local_search_case.json`

Optional narrative companions:
- `NARL_DYNAMIC_CONTROL_PARAMETER_COMPARISON_TABLE.md`
- `ARG10_108GL_VALIDATED_NARL_NO3_NADPH_ARGININE_EVIDENCE_REPORT.md`

## Fields worth preserving
For each retained record, prefer these columns:
- provenance: `source_group`, `design_level`, `source_anchor`
- strain/process parameters: `strain`, `no3_bolus_mM`, `o2_stage2_frac`, `t_switch_h`, `Kd_no3`, `Ki_no2`
- NarL/readout terms: `narl_p_stage2_peak`, `narl_p_stage2_auc`
- burden/respiration terms: `no2_peak_mM`, `nitrate_resp_stage2`, `terminal_nitrate_fraction_stage2`, `nitrate_to_o2_terminal_ratio_stage2`
- cofactor terms: `nadph_PntAB_stage2`, `nadph_PPP_stage2`
- production terms: `arg_titer_g_L`, `productivity_g_L_h`, `yield_mol_mol_glc`
- interpretation: `note`

## Recommended summary rows
When making a human-readable markdown summary, include at least:
- 108 g/L chassis nitrate baseline at 40 mM
- `Arg10_108gL_Validated_dSthA_PntAB` at 40 mM as redox-rescue reference
- `Arg10_108gL_Validated_NarLFull_Optimised` at 20 mM / 0.03 O2 / 10 h
- the same strain at 30 mM / 0.03 O2 / 10 h
- the same strain at 40 mM as standard reference
- the same strain at 50 mM / 0.03 O2 / 10 h as stronger-drive point
- the same strain at 80 mM / 0.02 O2 as overdriven boundary

## Interpretation guardrails
- Use the dataset to support “optimize NarL exposure window”, not “stronger NarL is always better”.
- Use 20–30 mM NO3, 0.03 O2, 10 h switch as the current productive window on the optimized NarL design.
- Use 50–80 mM rows to show that stronger NarL exposure raises burden and does not guarantee the highest arginine titer.
- Use the chassis vs `dSthA_PntAB` comparison to show that NarL-compatible redox/NADPH rescue is the strongest gain axis.

## Session outputs created
- `ARG10_108GL_VALIDATED_SIMULATION_CONTROL_DATA.csv`
- `ARG10_108GL_VALIDATED_SIMULATION_CONTROL_DATA_SUMMARY.md`
