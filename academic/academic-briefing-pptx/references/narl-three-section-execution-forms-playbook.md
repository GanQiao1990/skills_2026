# NARL three-section + execution-forms playbook

Use this pattern when a user wants a template-derived Chinese academic briefing deck that must:
- stay inside exactly three macro sections: `研究背景 / 研究思路 / 研究方案`
- be JSON-first before PPT rewriting
- compress each bullet to about one short Chinese clause (~20 chars)
- preserve a user-specified English cover title literally
- use keyword-led bullets with bold + red keyword emphasis
- summarize `研究方案` under `三个执行形式`

## Recommended outline pattern

### 1. 研究背景
Do NOT blend everything into a single generic problem statement when the source actually contains two different background logics.

If the source mixes:
- current dry-lab / protein-design bottlenecks
- downstream metabolic-control need for new tools

split them into parallel background blocks.

Good split:
- 干实验问题
  - 干实验设计命中率仍然偏低
  - 传统验证流程长且成本偏高
- 代谢调控新工具
  - 蛋白写入比基因操作更自由
  - 可逆且写入时间更快

The explicit contrast that mattered in this session:
- protein-level write-in tools were preferred over gene-level manipulation because they offer:
  - freer control
  - reversibility
  - faster intervention timing

### 2. 研究思路
Center this section on the full platform-first paragraph, not a generic project plan summary.

Required logic:
1. build the platform foundation first:
   - de novo protein design using protein foundation models + hallucination algorithms
   - intracellular in situ screening / triage
2. then expand into three application layers:
   - S/T/Y module = micro write/erase
   - NarL module = macro write/erase
   - ppGpp module = system/mesoscopic state readout
3. then state the closed-loop system goal:
   - 计算设计 -> 原位筛选 -> 多层级干预执行 -> 系统级实时监测
4. end on the synthetic-biology control-system framing and industrial-host benefit

Useful compressed bullets from this session:
- 原核调控仍缺关键平台方法
- 开发 de novo 设计与原位筛选平台
- 形成写入擦除到状态读取架构
- 打通设计筛选执行监测回路
- S/T/Y 模块负责微观写入擦除
- NarL 模块负责宏观写入擦除
- ppGpp 模块负责介观状态读取
- 构建新型合成生物学控制系统
- 提升工业宿主生存力生产力

### 3. 研究方案
If the user asks for `三个执行形式`, do not leave the execution summary implicit.
Encode it explicitly as three named execution forms under `研究方案`.

Recommended mapping:
- 执行形式一：PTE 微观写入擦除
  - 围绕 S/T/Y 节点实施微观干预
  - 用于逆境胁迫相关修饰调控
  - 提升细胞稳健性与响应速度
- 执行形式二：NarL 宏观写入擦除
  - 围绕 NarL 轴实施系统级调控
  - 用于转录代谢过程动态改写
  - 支撑生长生产协调控制需求
- 执行形式三：ppGpp 状态读取监测
  - 围绕 ppGpp 建立实时读出模块
  - 用于评估不同干预后的状态
  - 形成执行监测配对闭环系统

## PPT implementation notes
- The working base in this session was a template-derived `.pptx` rather than direct `.ppt` conversion.
- The deck ended up using multiple slides under each macro section while keeping the visible section labels restricted to the three user-specified labels.
- A useful end-state was:
  - cover
  - 研究背景
  - 研究思路 (2 slides)
  - 研究方案 (multiple slides)
  - 汇报总结 · 三个执行形式
  - 汇报总结 · 三段式主线

## Formatting notes that mattered
- Preserve the exact English title if the user insists.
- Keep bullets short enough to be scannable on slide.
- Use run-level emphasis:
  - keyword = bold + red
  - remainder = primary body color
- When the user later asks for only two font colors per slide, collapse the scheme to:
  - primary body color
  - red accent color

## Pitfalls discovered
- Do not summarize `研究思路` too abstractly; anchor it in the actual platform paragraph.
- Do not leave `三个执行形式` as an implied takeaway; make them explicit in both JSON and PPT.
- Do not silently replace the user-specified English title with a Chinese translation.
- Do not keep background as one mixed problem list when the user wants a split between dry-lab bottlenecks and metabolic-tool demand.
