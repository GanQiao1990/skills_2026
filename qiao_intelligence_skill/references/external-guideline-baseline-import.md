# 外部 guideline repo 作为底层执行基线：导入与固化模式

适用场景：
- 用户明确说“把某个 GitHub repo 写入最底层逻辑”“执行过程要严格参考”；
- 该 repo 提供的是行为准则、coding guidelines、agent workflow，而不是单纯资料库。

## 处理顺序

1. 先检查仓库结构
- 顶层是否有 `skills/` 或标准 `SKILL.md`
- 不要先讲方案，先实际检查

2. 若存在可导入 skill
- 直接将 `SKILL.md` 导入本地技能目录
- 然后显式加载该 skill，不能只下载不启用

3. 在当前任务余下过程里，将其当作执行基线
- 例如 `multica-ai/andrej-karpathy-skills` -> `karpathy-guidelines`
- 应显式采用：
  - think before coding
  - simplicity first
  - surgical changes
  - goal-driven execution

4. 不要只写入 memory
- 这种用户要求属于“如何做这类任务”的工作流偏好，应进入 skill 层
- 若 memory 空间不足，也必须至少完成 skill 层固化

## 对 `multica-ai/andrej-karpathy-skills` 的稳定经验

已验证：
- 仓库顶层存在 `skills/karpathy-guidelines/SKILL.md`
- 可通过 GitHub contents API 拉取并写入本地 `~/.hermes/skills/karpathy-guidelines/SKILL.md`
- 这类 repo 更适合作为“执行约束基线”，而不是一次性资料

## 默认对外表述

“已将该外部 guideline repo 中的核心 skill 导入本地，并在后续执行中作为底层行为基线：先想清楚再动手、优先最小方案、外科手术式修改、用可验证成功标准驱动执行。”
