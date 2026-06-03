# NARL project briefing pattern: three-section deck with two background pages

Use this reference when a project-briefing PPT must satisfy all of the following at once:
- user provides a proposal/concept-summary source and a legacy-template lineage
- deck must stay inside exactly three macro sections: `研究背景 / 研究思路 / 研究方案`
- bullets must be short, around 20 Chinese characters
- keywords must be highlighted as bold + red runs
- user wants `研究背景` split into 2 pages
- user wants `研究方案` summarized again as `三个执行形式`
- user requires the English cover title to remain exactly as provided

## Recommended page order
1. Cover
2. 研究背景一：干实验与蛋白设计瓶颈
3. 研究背景二：代谢调控需要新工具
4. 研究思路：平台方法学驱动三层功能元件递进扩展
5. 研究思路：三层模块接入宿主后形成应用控制系统
6. 研究方案一：ClpX 原位 triage 建立验证入口
7. 研究方案二：NarL 成为平台与应用的关键枢纽
8. 研究方案三：PTE 实现微观写入与擦除
9. 研究方案四：TMR 改写系统级调控逻辑
10. 研究方案五：ppGpp 实现状态读取与闭环验证
11. 汇报总结：三个执行形式
12. 汇报总结：三段式主线

## Background split guidance
When the user says `研究背景要分割` or `研究背景要2页`, use this specific split:

### Background page 1
Title:
- 研究背景一：干实验与蛋白设计瓶颈

Suggested short bullets:
- 干实验设计命中率仍然偏低
- 传统验证流程长且成本偏高
- 建立设计压缩原位验证平台
- 加快候选进入细胞内验证

### Background page 2
Title:
- 研究背景二：代谢调控需要新工具

Suggested short bullets:
- 代谢调控需要更灵活新工具
- 基因操作难以快速可逆调控
- 蛋白写入比基因操作更自由
- 可逆且写入时间更快

Important: these two background pages should be consecutive immediately after the cover, not scattered later in the deck.

## Research-logic summary guidance
If the user says `研究思路应该围绕...进行总结`, treat the quoted source paragraph as the authoritative briefing spine and compress it into two slides:

### Research-logic slide 1
Theme:
- platform methodology -> three-layer expansion

Suggested short bullets:
- 原核调控仍缺关键平台方法
- 静态调控难支撑复杂合成任务
- 平台向三层功能元件递进扩展
- 部署写入擦除与状态读取模块
- 形成写入擦除到状态读取架构
- 打通设计筛选执行监测回路

### Research-logic slide 2
Theme:
- three layers + overall system goal

Suggested short bullets:
- S/T/Y模块负责微观写入擦除
- NarL模块负责宏观写入擦除
- ppGpp模块负责介观状态读取
- 接入宿主细胞形成控制闭环
- 构建新型合成生物学控制系统
- 提升工业宿主生存力生产力

## Three execution forms summary
When the user asks for `三个执行形式`, use a dedicated summary slide and keep the mapping explicit:
1. 执行形式一：PTE 实现微观写入擦除
2. 执行形式二：NarL 实现宏观写入擦除
3. 执行形式三：ppGpp 实现状态读取监测

If a JSON outline is requested first, represent these under `研究方案 -> three_execution_forms`, each with:
- `title`
- `summary` (2-3 short bullets)

## Styling constraints learned from session
- Keep the exact English cover title if the user says `我们的题目还是这个 ...`
- For keyword emphasis, use run-level formatting:
  - keyword = bold + red
  - remainder = slide primary text color
- If the user says each interface should use only two colors, use:
  - one primary text color for the slide
  - one red accent color for highlighted keywords
- If dark decorative fills conflict with that constraint, lighten the fills rather than introducing a third text color.

## Verification checklist
- cover title preserved exactly
- `研究背景` spans exactly 2 consecutive pages after cover
- total page order matches intended three-section storyline
- `three_execution_forms` exists in JSON if JSON was requested
- keyword runs are bold + red in at least one sampled bullet per slide family
- content slides use only primary text color + red accent
