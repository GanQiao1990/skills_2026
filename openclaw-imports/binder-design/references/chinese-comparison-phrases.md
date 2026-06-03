# Chinese comparison phrases for binder-design methods

Use these when the user wants one-line Chinese wording for proposals, notes, or manuscript-style comparisons.

## Style rules
- If the user asks for “20字总结”, output exactly one line and no explanation.
- Prefer tradeoff language over absolute dismissal.
- Focus on where the method spends computation and where the main uncertainty remains.
- Keep terms reusable in scientific Chinese: 结构先验、拓扑搜索、几何代理、结构精修、单模型偏差、实验转化。

## Compact formulations

### BindCraft problems
- 依赖结构先验算力昂贵成功率波动泛化性不足
- 单模型回传成本高复杂靶标泛化与转化不足

### RFdiffusion problems
- 骨架易偏功能位点序列适配差实验成功率不稳
- 骨架生成虽快但序列闭环弱实验转化不稳定

### ProteinHunter fast theory
- 几何代理前置结构精修后置快速筛出可行拓扑
- 先廉价搜拓扑再昂贵精修提升早筛效率

## Preferred framing in longer Chinese prose
- ProteinHunter is mainly for 前端快速拓扑搜索与 seed 生成.
- HalluDesign / HunterDesign is mainly for 后端局部精修与 sequence–structure closure.
- Chai-1 is mainly for 正交验证，降低单模型自证假阳性.

## Pitfall
Avoid answering terse Chinese requests with English labels, long setup text, or method-history exposition. The user may only want a submission-ready one-line judgment.
