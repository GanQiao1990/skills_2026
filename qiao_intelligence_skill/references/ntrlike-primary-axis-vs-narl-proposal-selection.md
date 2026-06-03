# 氨基酸高产 proposal 中主调控轴的选择：NtrB–NtrC 优先，NarQ–NarL 降级为辅助层

适用场景：
- 用户在 `/home/qiao/qiao_design/narl_project` 中继续优化 proposal，并追问“具体进行哪种信号调节”“之前选 NarQ–NarL 合适吗”“mimic 结果显示当前 NarQ–NarL 形式不可靠，怎么改主线”。
- 任务要求只保留两个核心科学问题，并强调要用已设定的 de novo design 元件去执行。

## 一、默认决策规则

当主验证产品是精氨酸，且本地 mimic 没有强力支持 NarQ–NarL 作为最优单模块入口时：

1. **不要再把 NarQ–NarL 写成第一主调控轴。**
2. **优先把 NtrB–NtrC / 氮状态控制轴提升为第一主线。**
3. **把 `amtB/glnA/gltBD/gdhA` 写成直接执行层。**
4. **把 `pntAB/sthA`（或 ArcB–ArcA 代表的 redox/ATP 支撑层）写成第二配套轴。**
5. **NarQ–NarL 只保留为低氧/硝酸盐边界条件下的辅助状态层或对照系统。**

## 二、为什么这样选

### 1. 文献逻辑更支持氮状态 / redox 主线
Liming Liu 与 Sang Yup Lee 的代表性研究共同更直接支持：
- 碳氮协调
- Gln/Glu 与氮同化状态
- NADPH/ATP 再平衡
- 外排/耐受
- 生产阶段时空解耦

而不是首先支持 nitrate-responsive TCS 作为高产氨基酸的最稳入口。

### 2. 本地 mimic 对精氨酸主体系的支持更偏向氮同化模块
当 `mimic_results/multi_amino_acid_mimic_summary.csv` 显示：
- arginine 的 `nitrogen_assimilation` `product_flux_auc` 高于 `narl_no3_gate`
- `final_product_pool_proxy` 也更高
- `peak_nitrite_risk_proxy` 更低甚至为 0

则默认结论应写为：
- **NarQ–NarL 不是当前精氨酸主验证体系里最稳的第一入口**
- **NtrB–NtrC / nitrogen-state control 更适合作为 proposal 的主调控轴**

本次会话里的稳定示例：
- arginine `nitrogen_assimilation` `product_flux_auc` 28.58
- arginine `NarL + NO3 gate` `product_flux_auc` 27.35
- 前者约高 `4.48%`
- `final_product_pool_proxy` 前者约高 `4.57%`
- NarL 路线还有额外 nitrite-risk proxy

## 三、proposal 里的推荐写法

### 最稳主线句
“本项目的动态控制主问题，不再优先设定为 NarQ–NarL 轴重编程，而是聚焦于氮状态—redox/ATP 失配的蛋白层级门控；其中以 NtrB–NtrC 作为状态感知层，以 `amtB/glnA/gltBD/gdhA` 作为直接执行层，并以 `pntAB/sthA` 等 redox 支撑模块作为并联配套层。”

### NarQ–NarL 的降级写法
“NarQ–NarL 在本项目中保留为低氧/硝酸盐边界条件下的候选辅助状态层与对照系统，用于评估 nitrate-responsive control 是否在特定窗口内带来额外收益，但不再承担 proposal 的第一因果主线。”

## 四、只保留两个核心问题时的收口方式

### 第一问
如何利用 de novo 设计的动态临近元件，对氮状态—redox/ATP 失配实施蛋白层级门控？

### 第二问
如何利用 de novo 设计的空间组织元件，提高关键反应节点的局部反应效率并减少扩散损失？

## 五、与动态执行元件的连接方式

当用户明确提出：
- de novo 设计小分子结合蛋白
- 拆分为两端
- 小分子触发环化重排/构象重组
- 再连接调控分子 binder

则默认把它写成第一问的执行机制，而不是单列成第三个问题。

推荐表述：
“动态临近元件采用小分子触发式执行架构：将 de novo 设计的小分子结合蛋白拆分为两端，在目标小分子存在时发生环化重排或构象重组，再将该结构变化耦联至调控分子 binder，从而形成仅在特定代谢状态和时间窗口下闭合的蛋白级执行器。”

## 六、Asp 磷酸化监测的正式边界

若用户追问 RR Asp 磷酸化怎么监测，而当前认知是 phosphoproteomics 不可行：

### 不要写成主路线
- 不要把“常规全局磷酸组学检测 phospho-Asp”写成 proposal 主承诺。

### 默认三层证据链
1. **功能输出 readout**：`PamtB/PglnK/PglnA`、转录输出、Gln/Glu、氮流、redox、产物表型
2. **位点依赖验证**：Asp→Asn/Ala、His 失活、scrambled binder、linker-only、无诱导对照
3. **Top 候选靶向确认**：体外 phosphotransfer 重构、快速中性/弱碱条件下的 targeted shift / chemistry / 小规模 targeted MS

### 推荐句
“本项目不依赖常规全局磷酸组学监测 phospho-Asp，而以 reporter 时序、位点突变依赖、体外磷酸转移重构及下游功能 readout 构成主证据链；Asp 磷酸化的直接化学证据仅用于关键候选的靶向确认。”

## 七、最终决策模板

当用户问“之前 NarQ–NarL 合适吗？”时，默认输出：
- 不是完全不合适；
- 但在当前精氨酸主验证和已有 mimic 支持下，**不适合作为第一主调控轴**；
- 更稳的主线是 **NtrB–NtrC + `amtB/glnA/gltBD/gdhA`**，并联 **`pntAB/sthA`**；
- NarQ–NarL 降级为辅助状态层或对照系统。