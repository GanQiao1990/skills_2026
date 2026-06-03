# Quantified-evidence pattern for NarL/NO3/NADPH reviews in `basic_pathway_e_coli`

Use when the user escalates from a mechanism review to: "directly give me quantitative evidence", especially for NarL/NO3/NADPH/arginine claims in `/home/qiao/qiao_design/e_coli_model/basic_pathway_e_coli`.

## Durable lessons from this session

### 1. When the user asks for quantified support, do not stop at mechanism prose
The deliverable should become a quantified evidence chain with:
- absolute values
- deltas
- percent changes
- explicit support tier: strong / partial / not directly supported
- direct file anchors for every number

Required quantitative fields when available in this repo:
- arginine titer
- NarL AUC / peak
- peak NO2
- nitrate respiration
- terminal nitrate fraction
- NADPH_PntAB_stage2
- NADPH_PPP_stage2

### 2. If the user says “within/on top of our 108 g/L high-producing chassis”, anchor everything to the validated chassis lineage
Use:
- `Arg10_108gL_Validated`
- `Arg10_108gL_Validated_dSthA`
- `Arg10_108gL_Validated_dSthA_PntAB`
- `Arg10_108gL_Validated_NarLFull_Optimised`

Do NOT flatten the narrative back into generic WT or abstract labels unless explicitly needed for context.

### 3. Split claims into three tiers
#### Strong support
Typical examples in this repo:
- NarL/NO3-centered control is linked to late-stage redox/cofactor management
- PntAB-centered NADPH rescue improves nitrate-stage arginine performance
- dynamic NO3/O2/switch control changes NarL exposure and respiratory state

#### Partial support
Typical examples in this repo:
- stronger NarL exposure can intensify the control program
- NarL/NO3 improves nitrogen-assimilation state and may contribute nitrogen-source benefit into arginine production

#### Not directly supported as a strong claim
Typical example in this repo:
- extra nitrate-derived nitrogen atoms are already proven to be the dominant cause of arginine improvement

### 4. Current key quantitative comparisons worth reusing
#### A. 108 g/L chassis vs dSthA+PntAB at fixed 40 mM NO3
Sources:
- `results/strain_comparison.csv`
- `NarL_NADPH_Arginine_Production_Report.md:85-87`

Numbers from this session:
- `Arg10_108gL_Validated`: arginine `8.801 g/L`, peak NO2 `34.510 mM`, NADPH_PntAB `0.000`
- `Arg10_108gL_Validated_dSthA_PntAB`: arginine `13.332 g/L`, peak NO2 `12.284 mM`, NADPH_PntAB `0.294`
- deltas:
  - arginine `+4.531 g/L` (`+51.48%`)
  - peak NO2 `-22.226 mM` (`-64.41%`)

Interpretation: strongest evidence for cofactor/redox rescue on the validated chassis.

#### B. FullOpt_narl_40 vs FullOpt_narl_80
Source:
- `results/narl_phospho_control/narl_control_comparison_table.csv`

Numbers from this session:
- 40 mM: arginine `13.332 g/L`, NarL AUC `0.499`, peak NO2 `12.284 mM`
- 80 mM: arginine `10.815 g/L`, NarL AUC `1.303`, peak NO2 `25.735 mM`
- deltas:
  - NarL AUC `+161.34%`
  - peak NO2 `+109.50%`
  - arginine `-18.88%`

Interpretation: stronger NarL exposure is real, but carries nitrite cost and can reduce endpoint titer.

#### C. 20 mM vs 50 mM on `Arg10_108gL_Validated_NarLFull_Optimised`
Sources:
- `results/narl_phospho_local_search/top10_local_search.csv`
- `results/narl_phospho_local_search/best_local_search_case.json`

Numbers from this session:
- 20 mM / 0.03 O2 / 10 h: arginine `14.422 g/L`, NarL AUC `0.495`, NO2 `11.877 mM`, nitrate respiration `0.258`
- 50 mM / 0.03 O2 / 10 h: arginine `13.655 g/L`, NarL AUC `1.199`, NO2 `16.098 mM`, nitrate respiration `0.547`
- deltas:
  - arginine `-5.32%`
  - NarL AUC `+142.26%`
  - nitrate respiration `+112.12%`
  - peak NO2 `+35.54%`

Interpretation: dynamic tuning is quantitatively real, but NarL-focused optimum and titer optimum differ.

### 5. Mandatory caution on the nitrogen-atom-supply subclaim
If the simulator still retains Stage-II NH4 feed:
- `scripts/two_stage_simulation.py:70-75`
  - `nh4_0_mM = 40.0`
  - `feed_nh4_mmol_h = 10.0`

Then do NOT claim direct quantitative proof that nitrate-derived nitrogen atoms dominate arginine gains.

Allowed wording:
- improves nitrogen sufficiency / nitrogen-assimilation state
- may contribute added nitrogen-source benefit

Disallowed wording unless new direct evidence exists:
- nitrate-derived nitrogen atoms are already directly quantified as the dominant driver

## Recommended deliverables when user asks for quantified support
1. English markdown evidence chain
2. Chinese markdown evidence chain
3. Optional SVG summary if they also asked for visualization

## Session-specific file outputs created
- `NARL_NO3_NADPH_ARGININE_QUANT_EVIDENCE_CHAIN.md`
- `NARL_NO3_NADPH_ARGININE_QUANT_EVIDENCE_CHAIN_CN.md`
- `ARG10_108GL_VALIDATED_NARL_NO3_NADPH_ARGININE_QUANT_EVIDENCE_CHAIN.md`
- `ARG10_108GL_VALIDATED_NARL_NO3_NADPH_ARGININE_QUANT_EVIDENCE_CHAIN_CN.md`
