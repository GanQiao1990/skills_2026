# E. coli ammonia assimilation mechanism dashboard pattern

Use this when adapting the AI-Scientist-v2 research-frontend information architecture to a single-file local HTML figure for E. coli nitrogen/ammonia assimilation.

## What worked in this session

### 1. Add two control layers, not one
Use both:
- mechanism submodes: 总览 / 摄入阀门 / 信号级联 / GS-GOGAT / GDH 支路
- biological scenarios: 低氮场景 / 高氮场景 / 工程设计场景

The figure becomes much easier to explain when users can switch both the pathway slice and the biological operating context.

### 2. Every toggle must update BOTH copy and network focus
Do not only change text, and do not only re-highlight the graph.
Each mode/scene change should simultaneously:
- update the explanation cards
- update active/dim node highlighting
- update active/dim edge highlighting
- update label emphasis

### 3. Keep a stable story panel + a dynamic mechanism lab
Recommended structure:
- stable story panel: input -> sensing -> amplification -> output
- dynamic mechanism lab: 状态判读 / 主同化出口 / 工业启示 / 高氮对照 / 工程抓手

The stable panel teaches the causal order; the dynamic panel answers "what matters in this state?"

### 4. Scenario layer should be allowed to constrain the mechanism layer
If a scenario makes the current mechanism mode misleading, coerce the mode.
Good defaults from this session:
- high-N scenario should prefer `gdh` or `full`
- engineering scenario should prefer `signal`, `uptake`, `gogat`, or `full`
- low-N scenario should not leave the dashboard stuck on `gdh`

This prevents logically inconsistent states such as a high-N scene still presenting GS-GOGAT as the dominant route.

### 5. E. coli ammonia assimilation story to keep visible without hover
Use the explicit chain:
- Input: AmtB-mediated NH4+ uptake
- Sensing: GlnD reads Gln status
- Signal relay: PII / GlnB / GlnK switching
- Amplification: NtrB/NtrC transcriptional activation
- Outputs:
  - GS-GOGAT = low-ammonium, high-affinity route
  - GDH = high-ammonium shortcut

Important pitfall: do NOT present GDH as the main low-ammonium route.

### 6. Engineering interpretation that helped
Useful design framing for Chinese scientific communication:
- 摄入阀门
- 状态感知
- 转录放大
- 氮汇出口

For engineering-mode copy, explicitly describe the system as a coupled design package rather than isolated enzyme edits.

### 7. Local HTML validation pattern
After editing a single-file HTML mechanism figure:
1. assert new UI strings and IDs exist in the HTML
2. extract the `<script>` block
3. run `node --check` on the extracted JS

This is a cheap, reliable syntax check for dashboard-style local artifacts.

## Recommended copy pattern for this user
Prefer concise Chinese dashboard language:
- 低氮下系统优先打开 AmtB 与 Ntr 调控程序，并把氮流压向 GS-GOGAT 高亲和同化回路。
- 高氮时 GDH 近路更重要，PII 去修饰与 AmtB 封闭倾向上升，昂贵的高亲和程序相对回落。
- 工程设计要按“摄入阀门 -> 氮状态感知 -> 全局转录 -> 氮汇出口”四层联动。
