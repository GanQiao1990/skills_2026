# NarL mimic：切入时机与“控制评分最优”vs“产量最优”判读

适用场景：当用户在 `/home/qiao/qiao_design/e_coli_model/basic_pathway_e_coli` 中要求“完成 mimic”“给出增加/切入 NarL 的时机”“解释整个逻辑过程”时使用。

## 1. 先区分两个不同的最优

在 `results/narl_phospho_local_search/` 下，必须明确区分：

1. `arginine titer` 最优
2. `narL_control_score` 最优

不能把二者混写。

### 当前项目内已验证结论
- `20 mM NO3 + 0.03 O2 + 10 h switch`：当前扫描中 `arginine titer` 最高，约 `14.422 g/L`
- `30 mM NO3 + 0.03 O2 + 10 h switch`：次优，约 `14.263 g/L`
- `50 mM NO3 + 0.03 O2 + 10 h switch`：是 `best_local_search_case.json` 的“综合控制评分最优”，不是 arginine titer 最优

## 2. 为什么 50 mM 不能直接写成“最优产量”

`best_local_search_case.json` 来源于 `scripts/narl_phospho_local_search.py` 中的 `narL_control_score` 排序，而该 score 不是单纯产量目标。它综合考虑：

- arginine titer
- NarL AUC
- nitrate respiration / terminal nitrate fraction
- PntAB support
- nitrite penalty

因此：
- 若用户要“产量最高的 NarL 条件”，按 `arg_titer_g_L` 排
- 若用户要“NarL 控制程序最强/最明显的条件”，才可引用 `best_local_search_case.json`

## 3. NarL 切入时机的正确表述

`two_stage_simulation.py` 中要同时说明三个时间概念：

1. `t_switch_h`：策略层开始切换的时间
2. `transition_window_h`：平滑过渡窗口（当前默认 `1 h`）
3. `stage_alpha = 1.0`：NarL / Stage II fully engaged 的时间点

### 当前最稳口径
- 若 `t_switch = 10 h`，则约 `10.5 h` 进入 Stage II，`11.0 h` fully engaged
- 若 `t_switch = 12 h`，则约 `12.5 h` 进入 Stage II，`13.0 h` fully engaged

所以回答“什么时候开始增加 NarL”时，优先写：
- 推荐在 `10 h` 左右启动切换
- 真正完整接管在 `11 h` 左右出现

不要只写一个“10 h”而不解释 transition window。

## 4. 当前仓库内可直接引用的定量结论

- `t_switch = 10 h` 的最佳 arginine 高于 `t_switch = 12 h`
- 在当前扫描范围内，10 h 最佳值约比 12 h 高 `0.892 g/L`（约 `+6.6%`）
- 该结论应写成“在当前已测试窗口中，10 h 优于 12 h”，不要外推成“全局唯一最佳时间”

## 5. 推荐写法

### 最安全总表述
在当前 `Arg10_108gL_Validated_NarLFull_Optimised` mimic 中，NarL 更适合作为后期动态控制节点，在约 `10 h` 启动两阶段切换、`11 h` 左右 fully engaged，并在 `20–30 mM NO3 + 0.03 O2` 的中等暴露窗口内协调 nitrate respiration、redox/NADPH 支撑与 nitrogen-state control，从而促进 arginine 生产；该作用依赖窗口优化，不支持“持续增强 NarL 即单调增产”的表述。

### 必加边界条件
- 不要把 `50 mM` 写成“产量最优”，除非你明确说的是 `NarL control score` 最优
- 不要把 `NarL` 写成全程恒定增强器
- 不要把 `10 h` 写成不带过渡解释的刚性开关点
