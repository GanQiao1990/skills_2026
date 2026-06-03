# NBT 平台故事打磨清单

适用触发：
- 用户说“不是把 story 写顺，而是往 NBT 级别打磨”
- 用户给出审稿人口吻的 critique，希望据此重写 proposal / manuscript story
- 任务目标是把多个模块收束成一个 platform manuscript 或平台型申请书主线

## 一、先做的不是润色，而是诊断
先用一句话判断当前 story 最大问题，常见三类：
1. 平台主线不够锋利
2. 生物学应用有点分散
3. 关键技术优势还需要被定量证明

推荐句式：
`这个 story 有 NBT 潜力，但现在最大问题是：[主线不够锋利/应用分散/技术优势未定量证明]。`

## 二、先提炼唯一主线
优先写成：
`我们建立了一个[双重幻想/多模型/平台方法]驱动的 binder 工程平台，并通过[ClpX/功能筛选/验证引擎]把计算设计转化为可验证的细胞内调控模块，最终用于[应激抵抗/生产优化/旗舰应用]。`

所有后续应用都必须能挂回这条主线。

## 三、强制三段式结构
NBT 平台故事优先使用：

### Part 1: Platform design
解决设计慢、易错、候选难压缩的问题。

### Part 2: Platform screening
解决验证贵、低通量、设计端和实验端不匹配的问题。

### Part 3: Platform demonstration
用 1–2 个强应用展示平台价值；其余模块一律降级为 supporting layer / feedback layer。

禁止默认写成五个并列 aim。

## 四、旗舰应用选择原则
优先选择最能同时满足以下条件的系统：
1. 属于天然信号通路，而不是纯人工 readout
2. 能直接连接 growth–production trade-off 或真实工程表型
3. 能证明 binder 不只是能 bind，而是能 control
4. 具有时间动态或阶段切换意义

若 NarQ–NarL 这类系统存在，应优先提升为旗舰应用。

## 五、反馈模块降级原则
以下模块若不能承担主因果链，应明确写成 feedback/readout/supporting layer，而不是并列主应用：
- sensor
- reporter
- omics discovery
- validation-only assay

标准句式：
`X 不是单独成为一个小项目，而是作为整个平台的 feedback readout。`

## 六、每个部分必须显式包含三类内容
对于 design / screening / application / feedback 四层，都应写：
1. 这一部分已经强的地方
2. 这一部分还弱在哪里
3. 必须补的关键证据

这样能把“强 proposal”与“NBT-ready package”的差距写清楚。

## 七、必补证据包

### 设计层
- 与 RFdiffusion / BindCraft / 单幻想方法比较计算时间
- 候选多样性：topology diversity、interface diversity
- 跨模型一致性：AF3/Boltz-2/Chai-1 预测复现率
- wet-lab hit rate
- ablation：只有第一重、去掉第二重、去掉 cross-model audit、完整系统

### 筛选层
- throughput
- 相对 SPR-only 或 purified screening 的成本优势
- enrichment fold
- 降解读出与 SPR/动力学/细胞功能的相关性
- linker 长度和构型机制对照
- 阴性对照矩阵：无 binder、错配 binder、无 recruitment、不可降解 target

### 应用层：stress phospho
- 明确 binder 如何影响 phosphorylation（recruitment / accessibility / conformation）
- 1–2 个强节点深挖，不要只做全局组学
- phosphosite mutant
- 直接磷酸化测量
- 表型改善：growth / survival / productivity
- stress readout 改善（可用 ppGpp）

### 应用层：NarQ–NarL
- NarL activity reporter
- NarL 活性与 growth/productivity 的量化关系
- static vs dynamic control
- dose / ligand tunability
- 排除慢生长伪解释
- time-course，明确最佳调控窗口

### 反馈层：ppGpp sensor
- dynamic range
- specificity（排除 GTP/GDP/pppGpp）
- response speed
- 与 LC-MS 或已知 perturbation 的相关性
- 调控前后 stress dynamics 变化

## 八、最终判断模板

### NBT 级别判断
推荐用法：
`现在的 idea 有 NBT 潜力，但当前 story 还处在强 proposal / 高潜力平台雏形阶段。`

随后明确：
- 如果只有概念和少量验证，更适合哪些次一级期刊
- 如果补齐 benchmark、多靶点验证、真实生理调控、生产提升和实时传感闭环，才具备冲 NBT 的条件

## 九、最强收束句模板
优先输出一个可直接复用的最后一句：

`我们开发了一个[双重幻想与跨模型复核驱动]的 binder 工程平台，通过[ClpX 临近降解]实现低成本功能筛选，并将设计得到的 binder 转化为可动态调控[细胞应激和生产状态]的细胞内工程模块。`

## 十、使用提醒
- 不要平均分配篇幅给所有模块
- 不要把 sensor 当成第三主应用
- 不要只做“概念很顺”的 narrative；必须主动写清“哪里还不够 NBT”
- 对此类任务，最重要的不是多写，而是先 sharpen hierarchy
