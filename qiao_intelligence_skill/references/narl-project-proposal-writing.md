# narl_project proposal写作与review工作流

适用场景：`/home/qiao/qiao_design/narl_project` 中围绕 binder 设计、ClpX/ClpXP 筛选、S/T/Y 磷酸化、NarQ–NarL 动态调控、ppGpp 传感的中文 proposal / 研究方案 / 立项依据写作与修订任务。

## 本次会话沉淀出的稳定规则

1. 当用户要求“根据以上内容完成proposal书写”且任务位于 `narl_project` 时，不能只依据当前对话要点直接写；必须先 review 项目目录中的相关材料，再组织成稿。
2. 优先吸收项目内已有主线文件，而不是脱离仓库另起炉灶。高优先级参考通常包括：
   - `core.md`
   - `five_point_method_positioning_note.md`
   - `programmable_element_design_by_de_novo_protein_designing.md`
   - `manuscript/manuscript_v18_narl_dynamic_regulation_2026-04-09.md`
   - `concepts/narl-phosphorylation.md`
   - `entities/narl-system.md`
   - 现有 proposal 草稿/ reviewed 版本
3. proposal 叙事默认要收束为同一条平台主线，而不是几个平行小课题堆叠：
   - binder设计问题
   - binder筛选问题（ClpX + target binder）
   - 精氨酸胁迫下 S/T/Y 磷酸化识别与抗胁迫调控
   - NarQ–NarL 动态调控生长—生产切换
   - ppGpp binder + cpGFP 胁迫感知
4. 对尚未形成完整实验闭环的模块，必须写成“研究方案 / 拟开展工作 / 预期结果”，不要伪装成既有实证结果。
5. 交付优先写成项目路径下的权威 markdown 文件，而不是只在对话里给摘要。

## 推荐章节骨架

1. 项目名称
2. 摘要
3. 核心科学问题
4. 总体假说
5. 总体目标
6. 研究内容与研究方案（对应五条主线）
7. 总体技术路线
8. 创新点
9. 可行性分析
10. 预期结果 / 科学意义 / 应用前景
11. 结论

## 当用户要求“with 科学思想”或要求先梳理方法学问题再写 proposal

此时不要把 proposal 写成五个并列任务说明，而要显式先回答“为什么现有路线不够、为什么这套方法必须存在”。默认按以下逻辑组织：

1. 先把现有 binder 路线放在同一问题框架下比较：
   - BindCraft / RFdiffusion / 单幻想 ProteinHunter-HalluDesign
   - 它们的问题不是不会生成候选，而是更像 `proposal engine`，不够像 `decision engine`
   - 关键矛盾写成：单模型自证偏差、候选压缩能力不足、复杂功能约束支持不足、设计快验证慢

2. 再回答为什么要设计双幻想（Double Hallucination）：
   - 不是“多跑几个模型”
   - 而是把候选生成、候选压缩、正交审计拆成不同职责
   - ProteinHunter = 广域探索；HalluDesign = 结构-序列闭环精修；Chai-1 = 正交独立审计
   - 优点要写成：提高 wet-lab-entry 质量、降低单模型偏差、把便宜计算前置/昂贵验证后置、适合复杂 ternary/degradation/signaling/dynamic-control 任务

3. 写 ClpX 筛选时必须体现“效率-经济”思想：
   - 先指出传统 SPR/BLI/pull-down 的纯化负担、成本和通量问题
   - 再说明为什么用 ClpX 酶系统做首轮功能筛选
   - 默认写法：以 ClpX binder-linker-GFP binder / target binder 为核心，理论基础是临近效应（proximity effect）
   - 评价标准默认写成：`靶点降解越多越好`
   - SPR 的定位是高优先级命中的正交验证与动力学归因，不是所有候选的一开始前置门槛

4. 写 S/T/Y 与 NarQ–NarL 时，默认保持“先识别节点，再部署调控”的科学顺序：
   - 先用 S/T/Y 磷酸化组学测序识别精氨酸胁迫相关关键变化
   - 再部署 binder-linker / 小分子调控 binder-靶点蛋白 binder
   - NarL 部分必须强调：不是单纯增强 NarL，而是解析 NarL 与生长-生产关系，并通过 NarQ 动态调控 NarL 促进生产

5. 写 ppGpp 传感器时，默认把它放在“感知层”而不是孤立工具层：
   - `ppGpp binder + cpGFP`
   - 用于大肠杆菌胁迫变化的实时监测
   - 更高一层意义是为未来“胁迫感知-调控执行”闭环提供输入端口

## 本类任务的关键写法

### 1. Binder设计问题怎么写
要把重点放在：
- 候选压缩效率低
- 单模型生成—评分—筛选自证偏差强
- wet-lab-entry 优先级不可靠

默认解决路径：
- ProteinHunter 前端广域探索
- HalluDesign 序列—结构闭环精修
- Chai-1 正交审计

### 2. Binder筛选问题怎么写
不要泛写“后续验证”。要明确指出：
- 传统 SPR / BLI / pull-down 通量低、纯化负担重
- 使用 `ClpX + target binder` 建立细胞内功能筛选体系
- 形成“功能初筛 → 复筛 → 正交验证”的候选压缩流程

### 3. S/T/Y 磷酸化与精氨酸胁迫怎么写
默认组织顺序：
- 先用 S/T/Y 磷酸化组学/测序识别精氨酸胁迫下关键位点变化
- 再筛选与耐受、资源重分配、生产负担相关的节点
- 再部署两类调控架构：
  - 靶向调控蛋白 binder-linker
  - 小分子调控 binder-靶点蛋白 binder
- 输出目标写成：增强抗胁迫能力，而不仅是“改变磷酸化”

### 4. NarL 与生长生产关系怎么写
必须强调：
- NarL 不是单纯越强越好
- 重点是解析 NarL 活化状态与生长、生产、资源分配之间的关系
- 最终目的是用 NarQ 动态调控 NarL，完成生长优先到生产优先的平滑切换

### 5. ppGpp 传感器怎么写
默认表述为：
- 构建 `ppGpp binder + cpGFP` 融合型荧光传感器
- 用于大肠杆菌胁迫变化的实时监测
- 更高一层意义是为后续“胁迫感知—调控执行”闭环提供输入端口

## 交付提醒

- 当用户说“review the things in /home/qiao/qiao_design/narl_project”时，最终回复里应明确说明已经review过项目内材料，并点名若干关键来源。
- 若已经生成过初版 proposal，再次修订时要明确说明 v2 相比初版的改进点：更贴合项目材料、更像正式 proposal、对未闭环部分保持方案体写法。
