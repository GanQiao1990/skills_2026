# Proposal-safe validation ladder for phospho-His / phospho-Asp in two-component systems

Use this reference when revising proposals that rely on HK/RR phosphorylation logic but where direct phospho-state detection is chemically fragile.

## Core rule
Do not write the proposal as if direct phospho-His or phospho-Asp measurement is routine at scale. Present a three-layer validation ladder:
1. direct chemical evidence
2. site-dependence evidence
3. downstream functional evidence

Preferred Chinese framing:
- 直接化学证据 + 位点依赖证据 + 下游输出证据
- 不把“直接看到磷酸化条带”设为唯一成功标准

## Why this matters
- Histidine phosphorylation is acid-labile and can collapse during ordinary sample preparation.
- Aspartyl phosphate is also labile and often poorly preserved in standard workflows.
- Reviewers will attack overconfident mechanism claims if the proposal does not acknowledge this.

## Recommended ladder

### 1) HK phospho-His layer
Best proposal-safe baseline:
- Purify kinase domains of HKs such as NarQ / NtrB / ArcB / CpxA.
- Perform in vitro autophosphorylation with [γ-32P]ATP or ATPγS.
- Sample rapidly under non-acid, low-temperature conditions.
- Use His->Ala and kinase-dead controls.

Optional confirmation:
- pHis antibodies
- pHis enrichment/immunoprecipitation
- orthogonal mass spectrometry when feasible

Safe wording:
- “优先采用低温、快速、非酸条件下的体外自磷酸化与位点突变对照确认 HK 激酶活性变化。”

Avoid:
- “直接检测 HK 磷酸化即可系统证明机制成立。”

### 2) RR phospho-Asp layer
Best proposal-safe baseline:
- Rapid neutral or weak-base quench.
- Phos-tag / mobility-shift style readout if compatible with the system.
- For key samples only, use DBHA hydroxylamine-chemical-probe enrichment plus mass spectrometry to capture modified Asp sites.
- Validate with Asp->Asn / Asp->Ala mutants and upstream HK loss-of-function controls.

Safe wording:
- “对关键候选采用快速淬灭结合位点突变和化学探针富集，确认 RR 磷酸化依赖性。”

Avoid:
- “常规 Western 即可稳定检测 RR-Asp 磷酸化。”

### 3) System-output layer
Always retain this layer even if direct phospho-detection is planned.

Recommended outputs:
- oxygen-independent reporters when hypoxia/low oxygen matters
- regulon qPCR
- EMSA / DNA-binding changes when relevant
- NO3-, NO2-, NH4+ dynamics
- ATP / NADH/NAD / NADPH/NADP windows
- product titer, intracellular/extracellular ratio, growth burden

This layer is the operational Go/No-Go gate for screening.

## Screening-vs-confirmation split
Use this distinction explicitly in proposals:
- Large-scale candidate compression: reporter / regulon / phenotype first
- Mechanism confirmation on top candidates: direct phospho-His / phospho-Asp assays

This prevents the proposal from sounding operationally naive.

## Suggested table columns for the proposal
- object
- primary direct assay
- secondary validation
- key controls
- fallback operational readout

Typical rows:
- HK-His~P
- RR-Asp~P
- reconstructed phosphotransfer chain

## Good wording snippets
- “考虑到 phospho-His 和 phospho-Asp 的化学不稳定性，本项目采用分层证据链，而非单一检测作为机制判据。”
- “直接检测主要用于 Top 候选的机制确认，不作为所有构建体的普遍筛选入口。”
- “若直接磷酸化读出受限，则以位点依赖性、reporter、regulon 输出及代谢表型构成闭环验证。”

## Reviewer-risk triggers
If the draft contains any of these, rewrite immediately:
- “精准检测 histidine/aspartate 磷酸化状态并据此完成大规模筛选”
- “直接证明 NarQ-NarL 因果机制” without fallback layers
- “常规条件下稳定测定 phospho-His/phospho-Asp” without handling caveats

## Session-specific evidence anchors used in this project family
Useful anchors already seen in local project materials:
- nitrate/nitrite utilization as an industrially relevant leverage point in local patent summaries
- Nar regulon output reporters as practical system-output proxies
- Liu Liming-related high-yield amino-acid literature emphasizing ATP/NADPH, transport, and fed-batch coordination
- Sang Yup Lee route emphasizing systems metabolic engineering rather than single-node overexpression
