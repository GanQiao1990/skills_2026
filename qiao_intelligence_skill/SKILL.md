---
name: qiao_intelligence_skill
description: 乔淦博士综合研究智能助手 - AI蛋白质设计、药物靶点发现、生物信息学与学术写作
version: 3.0.0
author: Claude (Anthropic)
updated: 2026-03-29
---

# 乔淦研究智能技能库 v3.0

## 🗂️ 目录结构总览

```
/home/qiao/ (总存储: ~4TB+)
├── 蛋白质研究 (3.0TB)
│   ├── allatom/          2.8TB  原子级模拟
│   ├── md/               893GB  分子动力学
│   ├── docking/          73GB   分子对接
│   ├── qiao_design/      核心设计项目
│   ├── RoseTTAFold/      248MB  结构预测
│   └── ptms/             107GB  翻译后修饰
├── 生物信息 (100GB+)
│   ├── biobank/          UK Biobank分析
│   ├── alphagenome_research/  基因组研究
│   └── mRNAid/           mRNA设计
├── AI/ML工具 (500GB+)
│   ├── dockerai/         35+项目集合
│   ├── anaconda3/        451GB  Python环境
│   ├── offline_models/   4.9GB  离线模型
│   └── huggingface/      47GB   HF缓存
├── 学术写作
│   ├── 2026_NSFC/        申报材料(v11最新)
│   ├── 2026_paper/       论文项目
│   └── doc_convert/      PDF转换工具
└── 配置
    ├── .claude/          35MB   技能库
    └── .hermes/          配置文件
```

## 🔬 核心研究领域

### 1. AI蛋白质从头设计
**方法**: Double Hallucination (ProteinHunter → HalluDesign → Chai-1)
**工具**: BoltzDesign1, LigandMPNN, Boltz-2, AutoDock Vina
**PLM-RAG**: ProTrek (512维) + Swiss-Prot (563K条)

### 2. NarL项目 (Nature Biotechnology)
**路径**: `/home/qiao/qiao_design/narl_project`
**应用**: 三元系统 (Effector + Linker + Target)
**目标**: NarL降解(ClpX) + 磷酸化(NarQ)

### 3. NSFC - NDUFB4靶点发现
**最新**: `/home/qiao/2026_NSFC/NSFC_Proposal_2026_v11.md`
**发现**: NDUFB4 (线粒体复合物I)
**验证**: SPR KD=1.56μM, Arg72Ala突变>64倍降低

### 4. 分子铆钉平台
**路径**: `/home/qiao/hermes-agent/me/qiao/qiao_design/NSFC_Proposal_Molecular_Rivet_Draft.md`
**目标**: 位点特异性磷酸化增强 (5-20倍)

### 5. PocketXMol - NK2R
**路径**: `/home/qiao/qiao_design/pocketxmol/`
**文档**: nk2r_keynote_8min_v5_defense_paper_final.md

### 6. 生物银行分析
**路径**: `/home/qiao/biobank/UKB_RAP/integrated_reportv2/`
**脚本**: cardiovascular_marker_ppi.py, cardiovascular_SGLT2_marker_identification.R

### 7. 分子对接
**路径**: `/home/qiao/docking/` (73GB, 104K文件)
**子项目**: 16个对接项目

### 8. 翻译后修饰
**路径**: `/home/qiao/ptms/` (107GB)
**工具**: PTMGPT2

## 🛠️ 技术栈

### 计算工具
- **结构预测**: Boltz-2, Chai-1, AlphaFold3, RoseTTAFold
- **序列设计**: ProteinMPNN, LigandMPNN, BoltzDesign1
- **骨架生成**: ProteinHunter, HalluDesign, RFdiffusion2
- **分子对接**: AutoDock Vina, Rosetta
- **PLM**: ProTrek (512维), PLM-interact-650M
- **MD模拟**: GROMACS, AMBER (md/ 893GB)

### 实验技术
- **亲和力**: Biacore T200 SPR, PuriMag™磁珠
- **成像**: Zeiss LSM 980 AiryScan 2
- **质谱**: TMT定量, 磷酸化位点
- **分子生物**: CRISPR-Cas9, HDR, ddPCR

### 数据分析
- **Python**: pandas, numpy, scikit-learn, PyTorch
- **R**: DESeq2, GEOquery, ggplot2, tidyverse
- **生信**: Bioconductor, STRING, UniProt

## 📋 工作流程

### 蛋白质设计标准流程
```bash
cd /home/qiao/qiao_design/narl_project/doulbe_hallu
# 1. ProteinHunter生成
bash runs/<run_id>/commands/run_proteinhunter_design.sh
# 2. 筛选候选 (summary_high_iptm.csv)
# 3. HalluDesign精修
bash runs/<run_id>/commands/run_halludesign_refine.sh
# 4. Chai-1预测
bash runs/<run_id>/commands/run_chai_predict.sh
```

### NSFC文档管理
```bash
# 最新版本
vim /home/qiao/2026_NSFC/NSFC_Proposal_2026_v11.md
# 归档旧版本
mkdir -p /home/qiao/2026_NSFC/archive
mv NSFC_Proposal_2026_v{1..10}.md archive/
```

### 生物银行分析
```bash
cd /home/qiao/biobank/UKB_RAP/integrated_reportv2
python cardiovascular_marker_ppi.py
Rscript cardiovascular_SGLT2_marker_identification.R
```

## 🔧 环境配置

### GitHub镜像 (中国)
```bash
git clone https://gh.llkk.cc/https://github.com/user/repo
```

### 搜索策略
- **学术检索**: 优先Bing (不用Google)
- **数据库**: UniProt, PDB, AlphaFold DB
- **文献**: PubMed, bioRxiv

## 🎯 项目优先级

### 高优先级 (活跃)
1. **NarL项目** - Nature Biotech目标
2. **NSFC申报** - v11最终版
3. **NDUFB4研究** - SPR验证完成
4. **生物银行分析** - integrated_reportv2

### 中优先级 (维护)
5. PocketXMol - NK2R拮抗剂
6. 分子铆钉平台
7. 翻译后修饰研究

### 低优先级 (归档候选)
- dockerai中不活跃项目 (35+项目过多)
- 旧版NSFC文档 (v1-v10)
- 临时模拟数据 (>90天)

## 📝 学术写作规范

### 中文学术风格
- 产品/管理导向公众号文章
- 学术段落增强注意力
- 推送: 周二/周四 10:00-11:30

### 实验数据报告
- 生物重复: n≥3
- 统计: t-test/ANOVA, p值标注
- 对照: 突变负对照 + WT
- 量化: 均值±SD, Cohen's d

### 图表要求
- 分辨率: ≥300 dpi
- 误差线: SD或SEM
- 显著性: *, **, ***
- 比例尺清晰

## 🚀 快速命令

### 查看项目状态
```bash
# NSFC最新版
head -50 /home/qiao/2026_NSFC/NSFC_Proposal_2026_v11.md

# NarL项目
ls -lh /home/qiao/qiao_design/narl_project/doulbe_hallu/academic_report/

# 生物银行
ls /home/qiao/biobank/UKB_RAP/integrated_reportv2/manuscript/

# 存储使用
du -sh /home/qiao/{allatom,md,docking,anaconda3}
```

### 批量转换PDF
```bash
cd /home/qiao/doc_convert
for pdf in *.pdf; do
    python convert_biosynthesis_to_markdown.py "$pdf"
done
```

## 🔍 关键文件索引

| 项目 | 路径 | 说明 |
|------|------|------|
| NSFC v11 | `/home/qiao/2026_NSFC/NSFC_Proposal_2026_v11.md` | 最新申报 |
| NarL Pipeline | `/home/qiao/qiao_design/narl_project/doulbe_hallu/docs/PIPELINE.md` | 设计流程 |
| 分子铆钉 | `/home/qiao/hermes-agent/me/qiao/qiao_design/NSFC_Proposal_Molecular_Rivet_Draft.md` | 平台草案 |
| Cas9 SOP | `/home/qiao/hermes-agent/me/qiao/qiao_design/cas9_narl/cas9_narl_SOP.md` | 实验流程 |
| 心血管报告 | `/home/qiao/biobank/UKB_RAP/integrated_reportv2/FINAL_REPORT.md` | 最终报告 |
| CVD手稿v5 | `/home/qiao/biobank/cardiovascular_analysis/CVD_PWAS_Manuscript_v5.md` | 论文手稿 |

## 💡 协作偏好

- **语言**: 中文交流
- **详细度**: 完整过程+每个细节；但当用户明确要求“20字总结”“within 25 words”“一句话总结”“two bullets”等超短输出时，优先严格服从字数/条目/句数约束，只返回压缩成品，不加铺垫说明
- **文档位置**: 优先写入项目工作路径；若用户用英文简写说 `within ./`，默认理解为“把成稿直接写到当前工作目录”，而不只是对话中返回文本
- **写入本地的默认整理方式**: 当用户直接粘贴较长中文学术/方法综述并要求“写入本地”时，默认保留其原有论证主线与分类框架，将内容整理为可复用的 markdown 成稿（标题、分级小节、比较表/清单），不要额外改写成完全不同的文风或过度压缩
- **指南建议/项目指南修订触发**: 当用户给出“指南建议”“拟申请指南题目”“研究内容”“考核指标”“关键词”等成套中文指南文本，并要求“增加乔相关内容”“以便拿到项目”“write it as markdown file in ./”时，默认先判断交付物究竟是“指南建议稿”还是“申报书正文”。若用户反复强调“这是指南”，必须严格按指南建议稿处理：保持题目凝练、研究内容聚焦任务边界、考核指标可考核可验收，不写成个人简历式介绍、承担单位说明或申报书式自我论证。仅在不改变原指南主轴的前提下增强中标竞争力；若需体现既有研究基础，优先通过研究指标、评价维度、机制指标、模型设置和考核指标来体现，不能通过“我们/乔/团队基础/交叉优势”等主体性措辞去写。另见 `references/national-guide-proposal-writing-zangyao-skin.md`。
- **国家级科技项目指南文风约束**: 当用户要求按“国家级科技项目指南提议书写标准”修订时，优先采用五模块结构：1）拟指南名称；2）国家重大战略需求与必要性；3）主要研究内容；4）主要考核指标；5）预期成果与应用前景。名称应控制在宏观、概括、非论文题目口径；需求部分须从国家需求、区域特色资源高值开发或产业链补短板切入；研究内容按“资源筛选/机理研究/关键技术/产品创制”组织为任务链；指标强调量化、可验收、可第三方核查；成果与应用前景说明成果形态和落地场景。避免“前沿性增强”“交叉优势”“更容易中标”等包装性话语。若用户要求“多个方向都要写”，默认每个方向都独立补齐这五个模块，并统一语体与粒度，不要出现某一条是正式指南口径、另一条仍是学术项目说明的风格漂移。
- **指南文本文风约束**: 当用户要求“academic paragraph”或在指南/申报场景中要求“更容易拿到项目”时，默认输出正式中文学术段落体，以连续论述强化研究逻辑、技术路线与转化价值，不要优先写成口号式条目、招商文案或过度工程化 checklist；但若用户进一步强调“这是指南”，则应优先服从指南文体，减少论证性和修饰性表达，保留必要的“考核指标/关键词”列表。若需要正式到部委口径，进一步改成名词短语密集、客观陈述句主导的“科研官话”，而非说明文或申报书自辩语气。若用户进一步要求“不要使用 bullet”，则正文必须全部改为段落承载，仅保留章节标题，不以项目符号列研究内容或指标点。
- **医学皮肤健康类指南增强触发**: 当主轴是皮肤光老化/功能性护肤品/藏药资源开发，而用户进一步要求加入“糖尿病皮肤病”“AI药物/藏药靶点研究”等内容时，默认将其作为围绕主线的交叉增强模块，而不是另起一题。推荐写法是：保持“藏药抗高原光老化”为主轴，把糖尿病相关皮肤损伤、高糖复合光损伤、AGE-RAGE、氧化应激、慢性炎症、屏障修复迟缓等写成补充评价场景或模型与指标体系扩展；把 AI 内容写成成分优选、候选靶点发现、网络机制解析与实验验证闭环。若用户要求“只从指标上体现工作基础”，则应把 diabetes skin 等既有积累压缩进指标体系，例如屏障/角化指标（FLG、FLG2、IVL、CLDN1、OCLN）、炎症黏附指标（IL-1β、CXCL10、ICAM1、VCAM1）、氧化应激与脂质过氧化/铁死亡指标（GPX4、SLC7A11、GCLC、HMOX1、NQO1）、微循环修复指标（NOS3、VEGFD）以及 AGE-RAGE、PI3K-Akt、MAPK、谷胱甘肽代谢、铁死亡、缺氧应答、细胞黏附等通路，不要把项目改写成糖尿病项目或在正文中显式讲“已有基础来自我们”。当用户进一步要求“增加 AI 的药物设计详细内容”，默认不要停留在笼统的“AI 靶点解析”，而应扩展为指南允许的任务链：活性成分识别、靶点预测、成分—靶点—通路网络构建、关键节点筛选、网络药理学、分子对接、分子动力学、药效团分析、构效关系建模、透皮吸收/安全性/配伍稳定性预测、候选物优选与实验回验，但仍保持为任务描述而非承担单位优势说明。若用户要求“凝练一些指标”，优先改成“建立1套综合评价体系/形成1套技术流程，代表性指标包括……”的写法，避免在考核指标中堆叠过长分子清单；分子指标再压缩时，优先写成“指标类别 + 少量代表性分子”，例如“皮肤屏障稳态、炎症黏附、氧化应激/脂质过氧化防御及微循环修复等指标，代表性分子包括 FLG、CLDN1、IL-1β、ICAM1、GPX4、HMOX1、NOS3 等”。若模型验证口径过细，优先把“1 种高糖或高糖合并光损伤模型验证”收束为“代谢异常相关复合损伤模型验证”，更符合指南口径。- **学生友好**: SOP包含同源臂、N20 gRNA、Cas9细节
- **任务执行**: 不在本地做结构分析(已在HPC完成)
- **机制优先**: 做代谢/生物系统优化时，若用户指定核心控制机制（如 NarL 磷酸化调控），必须围绕该机制组织建模、执行与汇报，不能默认退化为机制无关的通用产量最大化。
- **底盘优先于抽象标签**: 若项目已指定实验验证底盘（如 `Arg10_108gL_Validated`），后续工程化与过程优化应表述为该底盘的派生设计，而不是把 `ArgEng`、`Full`、`Full_Optimised` 等抽象标签当作独立起点。
- **跨模型学习方式**: 当用户要求“学习另一个 GEM/项目”来优化当前系统时，优先迁移建模纪律（底盘身份清晰、版本清晰、校准来源清晰），而不是迁移物种本身或把当前系统改写成外部模型。
- **项目参考**: NarL 动态代谢控制执行细节见 `references/narl-dynamic-metabolic-control-basic-pathway-ecoli.md`。
- **NarL proposal × 本地 PPT 对齐触发**: 当用户要求“based on 本地 .pptx 优化 proposal / scientific thought / summary”，尤其在 `/home/qiao/qiao_design/narl_project` 下处理 `proposal_nbt_binder_platform_*` 文件时，先提取 PPTX 文字内容，再按 PPT 主线重写 markdown，而不是只在现有 proposal 上局部润色。默认主线为“设计 → 筛选 → 调控 → 感知”；研究背景建议按“de novo 设计成为主流工具 → 现有方法要么慢要么易错 → 传统合成生物学调控方式不足 → 引出 protein-level regulatory elements”组织；研究逻辑中应将“精氨酸胁迫下的 S/T/Y 磷酸化调控”和“NarQ–NarL 动态生产调控”拆成两个独立部署层，并将 ppGpp 明确写成反馈/感知层。详见 `references/narl-proposal-ppt-alignment-2026-05.md`。
- **超大专利数据库 / LLM 检索触发**: 当任务涉及 `/home/qiao/qiao_design/e_coli_model/5000万专利申请全量数据1985-2025/中国专利数据库.csv` 这类超大专利表格库，并要求“压缩以便检索”“完成相关数据处理”“供 LLM 交互/编排层使用”时，优先采用分层检索栈：原始 CSV → 按年 TSV 压缩回查层 → SQLite Lean 元数据+FTS 稀疏召回层 → Parquet 列式分析层；不要一开始就把全库长文本塞进 SQLite，也不要未缩小主题就直接做全库 dense embeddings。详细做法见 `references/patent-corpus-retrieval-stack.md`。
- **专利 summary → audit 引用表触发**: 当用户先要一版“20种氨基酸 / 限制因素 / with cite / reality 专利内容”的总结，随后又要求 A 版、audit 版、可审计引用表或逐条回查时，默认采用“两阶段交付”：先给 summary 成稿，再从 summary 中抽取全部申请号，逐条回查 `中国专利数据库_llm_retrieval/by_year/patents_YYYY.tsv`，补成带 `标题 / 申请年份 / 关联氨基酸 / 关联限制因素 / 摘要证据句 / TSV位置(line_no,row_id) / 核验状态` 的审计表。用户要求“真实专利内容”时，必须优先保留专利原始事实句，不能只给专家化归纳。对数据缺口（如近10年内未检出可靠原核发酵生产证据的 L-天冬酰胺），必须显式标注为缺口，不可用酶生产或衍生用途替代。详见 `references/patent-audit-table-from-summary.md`。
- **专利组合评审触发**: 当用户要求在本地项目目录中“review 某位发明人/PI/机构 patents”时，优先视为对本地 CSV 专利组合的技术评审，而不是网络检索或逐条罗列。默认先定位发明人专属 CSV，再用 `申请号` 去重区分“原始记录数”与“独立申请数”，随后围绕“时间演化、技术主题、工程范式、产业化信号（g/L、得率、转化率、放大、底物兼容性）”形成技术组合判断。优先输出“技术谱系/平台能力”而非法律权利要求分析；若数据允许，可补充共发明人、校企合作方、代表性高被引专利。详见 `references/patent-portfolio-review-workflow.md`。
- **超大专利库 LLM 检索架构触发**: 当任务涉及 `/home/qiao/qiao_design/e_coli_model/5000万专利申请全量数据1985-2025/中国专利数据库.csv` 这类 10^7 级记录的大型专利 CSV，并且用户明确要“压缩后便于检索/用于 LLM 交互/对接 Moshi、LangGraph、AutoGen 等编排层”时，默认不要覆盖原始 CSV，也不要假装一次性完成全库 dense embedding。优先交付 Phase-1：先生成按申请年份切分的 LLM-friendly TSV 分片，保留 `row_id/line_no/申请号/专利名称/专利类型/申请人/申请人类型/申请年份/公开公告号/公开公告年份/IPC主分类号/发明人/摘要精简/主权项精简`；再在其上构建 lean SQLite+FTS5 元数据检索层，把 `title/applicant/ipc_main` 作为首轮 sparse candidate retrieval 字段；最后提供查询脚本与架构说明，明确推荐流程为“SQLite FTS 召回 → TSV/原始 CSV 回查 → 如有必要再做 dense rerank”。详见 `references/patent-corpus-llm-retrieval-stack.md`。
- **NarL 假设复核/证据图触发**: 当用户要求在 `/home/qiao/qiao_design/e_coli_model/basic_pathway_e_coli` 中“review ./ 找证据 + 判断假设是否成立 + 作出可视化”时，默认交付一个机制主线清晰的仓库内证据复核包：
  1. 明确区分“强支持 / 部分支持 / 反证或边界条件”；
  2. 不把“NO3 增加 NADPH”写成直接因果，优先表述为“NO3 通过硝酸盐呼吸维持 pmf，间接支撑 PntAB 介导的 NADPH 再生”；
  3. 不把“增强 NarL”写成单向更强更好，优先表述为“优化 NarL 暴露/控制窗口”；
  4. 若用户追问“直接给我量化证据”，必须把结论改写成数字化对照：直接列出 arginine titer、NarL AUC、peak NO2、nitrate respiration、NADPH(PntAB/PPP) 的绝对值、差值和百分比变化，不要只给机制性总结；详见 `references/narl-no3-nadph-quantified-evidence.md`；
  5. 若用户进一步限定“在我们 108g 高产菌基础上/within 108g high-producing chassis”，所有证据链、表格和结论都必须锚定 `Arg10_108gL_Validated` 及其派生体（如 `Arg10_108gL_Validated_dSthA_PntAB`、`Arg10_108gL_Validated_NarLFull_Optimised`），不能退回到机制无关的泛化表述；no-nitrate 场景只能作为边界条件或反证单列说明，不能冒充底盘主线。量化交付默认同时生成英文版与中文版 markdown 证据链；详见 `references/narl-no3-nadph-quantified-evidence.md`；
  6. 对“NO3/NarL 增加 arginine 氮原子供给”这一子命题，默认写成“部分支持”，除非仓库内已有去除外加 NH4 干扰后的直接氮流定量证据；若当前模型仍保留 Stage-II NH4 feed，只能表述为改善 nitrogen sufficiency / assimilation state，而不能声称已直接定量证明额外氮源供给主导增产；
  7. 若用户要求“帮我做一份不同参数的对照表”来说明假设与结果有效性，默认交付一个锚定 108 g/L 底盘谱系的参数对照包：主参数对照表 + 关键成对对照表 + 假设有效性判断表；核心结论必须写成“动态调控 NarL 可以促进 arginine 生产，但依赖参数窗口；单纯增强 NarL 不构成单调增产策略”。
  8. 若用户进一步要求“从 108g/L 高产菌出发的模拟调控数据”，除文字总结外，优先同时生成一个 machine-readable CSV 与一个 markdown 数据包说明，字段聚焦 NO3、O2、switch、NarL AUC/peak、NO2 peak、nitrate respiration、NADPH 与 arginine；详见 `references/narl-108gl-simulation-control-data.md`。
  9. 若用户进一步要求“完成 mimic + 给出增加/切入 NarL 的时机 + 讲完整逻辑过程”，必须额外区分两类最优：`arg_titer_g_L` 最优与 `narL_control_score` 最优；不得把 `best_local_search_case.json` 的 50 mM 条件误写成“产量最优”。回答切入时机时，要同时写 `t_switch_h`、`transition_window_h` 与 fully-engaged 时间点：例如 `t_switch=10 h` 应解释为约 `10.5 h` 进入 Stage II、`11.0 h` fully engaged。当前已测试窗口中，推荐口径是“10 h 启动切换、11 h 左右 NarL 完整接管、20–30 mM NO3 + 0.03 O2 为最优产量窗口”；详见 `references/narl-mimic-timing-and-score-vs-titer.md`。
  10. 输出应保存为项目路径下的权威 markdown 结论文件 + SVG 机制证据图，并在文中引用具体脚本/结果文件作为依据。相关执行模板与本次会话归纳见 `references/narl-no3-nadph-hypothesis-review.md`、`references/narl-no3-nadph-quantified-evidence.md`、`references/narl-108gl-simulation-control-data.md` 与 `references/narl-mimic-timing-and-score-vs-titer.md`。
- **NarL 启动子证据 → 氨基酸增产假设判读触发**: 当用户给出 `yeaR-yoaG`、`ogt`、`napF`、`dmsA` 等 NarL/FNR/NarP 启动子文献，并进一步追问“这些证据能否支持增强 NarL-P 促进氨基酸合成/增产”时，必须显式拆成三层判断：
  1. 启动子级直接证据：NarL-P 重排 nitrate-responsive respiration、NO/RNS 应答、DNA repair 与替代呼吸支路；
  2. 代谢层间接支持：这些证据只能间接支持后期生理状态、redox 与 stress buffering 改善，不等于直接激活氨基酸生物合成主通路；
  3. 若再结合本地 `basic_pathway_e_coli` 108 g/L 底盘定量结果，最强安全表述才升级为“NarL-P 作为后期动态控制器，可通过 respiratory hierarchy、redox/NADPH support 与 stress buffering 在优化窗口内间接促进 arginine 生产”。
  默认不要写成“增强 NarL-P 本身就直接促进氨基酸合成”或“越强越好”；优先输出强支持 / 部分支持 / 不支持强表述三档结论。详见 `references/narl-promoter-literature-evidence.md` 与 `references/narl-promoter-evidence-vs-amino-acid-hypothesis.md`。
- **外部规则库 / Karpathy 基线触发**: 当用户明确要求把某个外部 GitHub 技能库或 guideline repo “写入最底层逻辑”“严格参考执行”时，优先把它当作执行流程偏好而不是普通资料：先检查仓库结构，若存在可导入的 SKILL.md，则导入本地 skill 并显式加载；随后在该任务余下过程里把其中规则作为执行基线。对于 `multica-ai/andrej-karpathy-skills`，默认基线是：先想清楚再动手、优先最小方案、外科手术式修改、用可验证成功标准驱动执行。该偏好应进入相关工作流 skill，而不只放在记忆里。详见 `references/external-guideline-baseline-import.md`。
- **NarL/(p)ppGpp 写作触发**: 当任务涉及 `/home/qiao/qiao_design/mengjie_huan` 或 NarL + 氨基酸/精氨酸胁迫 + （p）ppGpp 机制解析时，优先保持“机制主线”而非泛化表述；若用户明确要求“四级标题”，默认交付精炼标题成品（可附总标题），不要自行扩展成多级大纲，除非用户再次明确要求“扩展/展开”。相关写法与覆盖要点见 `references/narl-ppgpp-heading-and-scope.md`。
- **NarL 特定启动子文献核查触发**: 当用户要求为 `yeaR-yoaG`、`ogt`、`napF`、`dmsA` 等 NarL/FNR/NarP 靶启动子的机制表述寻找“具体文章/数据支撑”时，默认先把任务拆成“直接支持 / 部分支持或系统层推断 / 不宜直接写”三层；优先回到原始启动子论文（位点映射、DNase I footprinting、突变、体外转录），不要只给综述性转述。默认收口规则：`yeaR-yoaG` 与 `ogt` 的“无需 FNR 的 NarL 独立激活”可强写；`napF` 更稳的经典结论是 `Fnr + NarP` 激活且 `NarL` 拮抗，不要轻易强写成“高 NarL-P 饱和 -44.5 并彻底关闭 10–25 倍”；`dmsA` 可强写为 NarL-P footprint 重叠 Fnr/RNAP 识别区并显著抑制厌氧激活，但不要直接夸写成“完全斩断 DMSO 呼吸”或“毫秒级”响应。会话级出处、PMID 与推荐表述见 `references/narl-promoter-specific-literature-evidence.md`。
- **NarL × 专利数据瓶颈提炼触发**: 当用户要求在 `/home/qiao/qiao_design/e_coli_model/5000万专利申请全量数据1985-2025/江南大学_刘立明_相关专利数据.csv` 内提炼“氨基酸高产瓶颈”并限定 `NarL` / `NarL 调控基因相关` / `为了后续 NarL 操纵` 时，默认执行一个“专利事实 → NarL 工程假设”双层交付：
  1. 先明确检索 `NarL|NarQ` 直接命中；若数据内无直接命中，必须在结论前部显式写出“不能把专利表述成已直接证明 NarL 因果作用”；
  2. 仍要继续抽取与 NarL 最相关的间接证据维度：硝酸盐/亚硝酸盐利用、氮源同化、氧化还原/辅因子（NADH/NADPH/PLP）、胁迫耐受、转录调控、两阶段发酵窗口；
  3. 输出中必须区分“强支持”与“间接支持/工程推断”，不能把机制推断伪装成直接证据；
  4. 若目标是氨基酸高产，优先将瓶颈归并为：产物毒性、工业碳源适配、硝酸盐/亚硝酸盐窗口、辅因子供给、前体碳流、胁迫稳态、动态生产窗口；
  5. 默认把 `CN202410537555.3`（高产赖氨酸且可利用硝酸盐/亚硝酸盐）视为当前数据集中与 NarL 工程最直接的专利锚点，并据此把“赖氨酸中的动态硝酸盐利用窗口”列为 NarL 操纵的最高优先验证方向；
  6. 对 NarL 操纵建议，默认强调“把 NarL 作为 growth-to-production transition 的动态控制节点，而非全程恒定强激活”；
  7. 默认交付一个项目路径下的中文 markdown 权威总结，并列出建议联测指标：nitrate/nitrite、NADH/NAD+、NADPH/NADP+、ATP、活菌率、终点死亡率、产物滴度与得率。详见 `references/liuliming-patent-narl-amino-bottlenecks.md`。
- **氨基酸生物合成瓶颈/条件优化调研触发**: 当用户在本地专利大库中询问“氨基酸生物合成过程中的制约因素/瓶颈/条件优化”，且措辞里出现“制约性引物”这类疑似笔误时，默认优先按“制约性因素/瓶颈”理解，而不是先跳到 PCR 引物设计，除非用户明确提到扩增、检测、克隆或引物序列。此类任务默认优先使用本地专利检索栈，从工业工程视角提炼六类高频限制因素：产物毒性/掉活、前体碳流不足、辅因子与还原力不足、关键酶与转运不足、静态表达不适配生长-生产切换、发酵工艺窗口未调顺；并把结论收敛为“底盘耐受性 + 通量重分配 + 辅因子平衡 + 动态调控 + 工艺窗口协同优化”的系统工程。优先交付一个项目路径下的中文 markdown，可进一步按天冬氨酸家族、芳香族家族、谷氨酸家族、支链氨基酸家族细化，或继续映射到 NarL / 氮代谢动态调控。若用户进一步要求“20种氨基酸全覆盖 + cite + 每类限制因素至少5条证据 + 强调真实专利而非幻想设计”，优先检查并复用项目内现成权威稿 `prokaryotic_amino_acid_production_limiting_factors_recent10_patent_summary.md`，同时明确区分“项目内既有专利整理成果”和“当前 SQLite/Parquet 索引层是否已经逐条回查审计”。若用户再把要求提升为“每种氨基酸尽量补到 10 个真实生产 example + 再总结策略与限制因素”，默认使用 2016-2025 Parquet 层做标题优先筛选：标题需同时指向目标氨基酸与 `生产/发酵/工程菌/菌株/方法/工艺` 等真实生产语境，文本需出现原核/工程菌/发酵相关词；然后按氨基酸分别做排除（如 `β-丙氨酸` 不算丙氨酸本体、`天冬酰胺酶` 不算天冬酰胺本体生产、`酪氨酸酶` 不算酪氨酸生产）。这类“10 examples 扩展版”适合作为近10年覆盖式综述，但必须在文中明确说明：为补足覆盖度，部分样本可能偏向发酵提取/纯化/发酵液资源化或与目标氨基酸直接相关的工业生产工艺，而不是全部都等价于从零构建高产底盘的代谢工程专利；若后续要用于正式汇报正文，应再压缩成“严格版主表”，每种氨基酸只保留 3–5 条最硬的原核高产/5L放大/明确工程策略专利。缺少原核发酵本体证据时必须标记为数据缺口，不能用酶生产、衍生物或用途专利替代；详细流程见 `references/prokaryotic-amino-acid-patent-summary-workflow.md`、`references/prokaryotic-amino-acid-10example-expansion.md` 与 `references/amino-acid-biosynthesis-bottlenecks-and-process-optimization-from-patents.md`。
- **精氨酸高产瓶颈/优化流程触发**: 当用户进一步把话题收束到“精氨酸高产的瓶颈与优化流程”时，默认不要只把它当成谷氨酸家族的一小段补充，而应单独按精氨酸工程问题处理。优先从本地专利中提炼五层核心瓶颈：谷氨酸/谷氨酰胺前体供给不足、`argB`/`argR` 等通路约束、氮同化与氮调控层（如 `AmtR/AmtB`、`GlnD/GlnK`）不顺、NADPH/ATP/redox 不平衡、外排与离子/pH/渗透压稳态压力；再按“通路解除约束 → 氮调控重构 → redox/能量补强 → 转运与耐受稳定 → 工艺窗口封顶”的顺序写成流程。若后续还要映射到 NarL，默认表述为“氮调控、低氧氮利用、redox 与分阶段供氧是关键层，因此 NarL 是值得验证的动态入口”，但不要伪装成专利已直接证明 NarL 因果作用。详见 `references/arginine-high-production-bottlenecks-and-optimization-workflow.md`。
- **NarL 项目 proposal / grant 写作触发**: 当任务是在 `/home/qiao/qiao_design/narl_project` 内撰写、重写或直接优化中文 proposal 文件，并且用户强调“with 科学思想”或要求系统回答 binder 设计问题时，默认采用平台式主线而不是并列小课题叙事。必须显式写出：现有方法“要么慢、要么易错”；双重幻想=“广域探索 + 局部精修”；Boltz-2/AF3/Chai-1 用于跨模型最小共识；ClpX binder–linker–GFP binder 或 target binder 的理论基础是临近效应；筛选评价原则是“靶点降解越多越好”；SPR 作为正交验证。若在“研究逻辑/部署层/应用方向”中同时出现“精氨酸胁迫下 S/T/Y 磷酸化调控”和“NarQ–NarL 动态生产调控”，默认将其写成两个独立部署部分，而把 ppGpp 模块稳定定位为反馈/感知层，而非与前两者混写成并列应用。若用户进一步要求“只保留两个核心问题”并强调“要利用我们设定的 de novo design 元件去执行”，默认收口为两问：其一，de novo 元件能否充当动态状态控制器，用于门控氮状态、redox/ATP 与生长-生产切换失配；其二，de novo 元件能否充当局部空间组织器，用于减少扩散损失与竞争支路截流。此时对刘立明与 Sang Yup Lee 的文献调研，不要写成普通综述，而应分别收束为“工业执行型策略”和“系统设计型策略”，再明确指出我们的 de novo 平台补的是蛋白级执行层空位。若用户要求“do paper query with PubMed API and do summary”或明确要求“like `/home/qiao/doc_convert/swmu_scraper`”，默认不要只做对话内概述，必须同时交付三层产物：1）运行本地 PubMed API 抓取并导出原始 CSV/XLSX；2）生成一个中文 markdown summary，明确写出检索范围、实际查询命令、原始输出路径、代表性 PMID 与这些文献对 proposal 的直接启发；3）将摘要结论进一步整合回 proposal 新版本，而不是把检索和 proposal 分离成两条互不相连的任务。此类 summary 不要写成平铺式作者介绍，而应始终围绕“两核心问题 + 主信号轴选择 + de novo 执行层补位”来组织。若用户追问“使用氨基盐是不是氮同化”，默认按条件判断：只有在氨基盐被摄取、其氮进入谷氨酸/谷氨酰胺等中心氮代谢并流入产物/生物量时，才可称为有机氮同化输入；若只是培养条件调节，则不能等同于氮同化增强。若用户进一步追问“具体进行哪种信号调节”“之前 NarQ–NarL 合适吗”“mimic 显示当前 NarQ–NarL 形式不可靠”，默认不要强行维护 NarQ–NarL 为第一主轴；应优先以精氨酸主验证体系和本地 mimic 为准，若 `nitrogen_assimilation` 模块优于 `narl_no3_gate` 且 nitrite-risk 更低，则把 proposal 主调控轴改写为 **NtrB–NtrC / 氮状态控制轴 + `amtB/glnA/gltBD/gdhA` 直接执行层**，并将 **`pntAB/sthA`（或 ArcB–ArcA 代表的 redox/ATP 支撑层）** 写为第二配套轴；NarQ–NarL 仅保留为低氧/硝酸盐边界条件下的辅助状态层或对照系统，而不是 proposal 的第一因果主线。若用户还提出“de novo 设计小分子结合蛋白拆分为两端、经小分子触发环化重排后连接调控 binder”，应把该机制写进第一核心问题作为动态执行架构，而不是扩展成第三问题；若用户进一步给出 circular permutation / loop permutation site / GS linker / 无配体高熵 OFF / 配体结合降熵 ON / TEM-1 插入位点 / 19F-NMR / HDX-MS 等细节，默认将其上升为 proposal 里的明确物理执行逻辑：通过剪断与重连打破天然稳定性，制造默认失稳、默认关闭的高熵态，再由目标配体作为“构象锁”恢复局部有序并驱动执行模块 ON，不要把这类机制继续写成笼统的“小分子触发构象变化”。针对 Asp 磷酸化监测，默认去掉“常规全局 phosphoproteomics”主路线，改用“功能 readout + 位点依赖 + 体外 phosphotransfer / targeted confirmation”的三层证据链。详细展开见 `references/narl-proposal-scientific-thought-v5.md`、`references/liu-lee-two-core-questions-amino-salt-n-assimilation.md` 与 `references/ntrlike-primary-axis-vs-narl-proposal-selection.md`。

## 📈 项目统计

- **总目录**: 50+
- **总存储**: ~4TB
- **Python代码**: 175K+ 行
- **R代码**: 15K+ 行
- **Markdown文档**: 9,956+ 个
- **活跃项目**: 10+

## ⚠️ 注意事项

1. **存储告警**: allatom(2.8TB) + md(893GB) 占用过大
2. **定期清理**: 每月清理临时模拟文件
3. **版本控制**: 保留最新版本，归档旧版
4. **项目聚焦**: dockerai项目过多，建议精简
5. **备份策略**: 重要数据定期备份到外部存储

---

**更新日志**:
- 2026-03-29 v3.0.0: 完整目录审查，添加存储管理和清理策略
- 2026-03-29 v2.0.0: 整合8大研究领域
- 2026-03-29 v1.0.0: 初始版本
