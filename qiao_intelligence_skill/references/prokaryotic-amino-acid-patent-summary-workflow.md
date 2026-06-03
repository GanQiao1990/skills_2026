# 原核氨基酸生产专利总结工作流（本地 5000 万专利库）

适用场景：
- 用户要求基于 `/home/qiao/qiao_design/e_coli_model/5000万专利申请全量数据1985-2025` 总结“原核生物生产氨基酸”的限制因素、瓶颈、条件优化或专家表格。
- 用户强调“真实专利内容”“不要幻想设计”“带 cite”“覆盖 20 种氨基酸”。

优先交付口径：
1. 先检查项目目录中是否已有可复用的权威总结稿；当前已有：
   - `prokaryotic_amino_acid_production_limiting_factors_recent10_patent_summary.md`
   - `amino_acid_biosynthesis_bottlenecks_and_condition_optimization_review.md`
   - `arginine_high_production_bottlenecks_and_optimization_workflow.md`
   - `liuliming_patents_amino_acid_narl_bottlenecks_summary.md`
2. 若用户要“20 种氨基酸 + 限制因素总表 + cite”，优先以 `prokaryotic_amino_acid_production_limiting_factors_recent10_patent_summary.md` 为当前项目中的首选权威成稿，再补充必要说明。
3. 明确区分两层证据：
   - 项目内已整理好的专利总结稿 / 专利号清单
   - 当前 SQLite / Parquet 检索层能否逐条回查验证
4. 如果尚未逐条回查所有专利号，不要声称“全部引文已从当前 SQLite 重新审计验证”；应明确表述为：基于项目内既有本地专利整理成果，且当前索引层与总结稿之间可能存在部分脱节，需要单独做 audit pass。
5. 当用户要求“每类限制因素至少 5 个证据”时，优先把限制因素归并为少数高频类别（如前体供给、反馈调控、redox、氮硫同化、耐受/外排、副产物、发酵窗口、工业底物适配），而不是给每个氨基酸硬拆完全独立的新类别。
6. 对 20 种标准氨基酸要逐一覆盖；若某一项在近年数据中缺乏有效“原核发酵生产该氨基酸本体”的证据，必须显式标记为“数据缺口”，不能用酶生产、衍生物或非原核用途冒充。

推荐输出结构：
- 数据来源与检索口径
- 20 种氨基酸覆盖表
- 限制性因素总表（每类 >= 5 条专利证据）
- 工程优先级/专家结论
- 数据边界与未完全审计项

关键坑点：
- 不要把食品添加、化妆品、医药组合物、材料用途中的氨基酸名字误当成“原核发酵生产专利”。
- 不要把 L-天冬酰胺酶生产误当成 L-天冬酰胺本体生产。
- 不要在没有逐条回查时夸大“最新专利都已重新核验”。

本次会话沉淀：
- 当前项目目录内已经存在一份覆盖 20 种氨基酸、并按 8 类限制因素归并且每类给出 >=5 条专利证据的近 10 年总结稿，可直接作为交付基础。
- 但总结稿中的专利号集合与当前 `patent_metadata.sqlite` 可直接逐条回查的索引层之间，可能存在部分不同步；后续若要做严格审计版，需要单独执行逐条 back-validation。