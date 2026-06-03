# Scientific Mechanism Dashboard Pattern

Use this pattern when the deliverable is a local HTML artifact (not a Streamlit app) but the user still wants the information architecture of a research frontend.

## When to use
- Mechanism figures for pathways, regulatory circuits, and systems-biology stories
- Single-file HTML artifacts that must open locally without a server
- Scientific visuals that need to be explainable, not just beautiful
- Chinese-language scientific communication where the user will present, screenshot, or embed the figure in a公众号/PPT

## Core idea
Borrow the `research frontend` structure from AI-Scientist-v2 even when the output is plain HTML:
1. A focused headline that names the mechanism, not a generic project title
2. A short explanatory panel that gives the causal story in 3-4 steps
3. A second "mechanism lab" panel with state summaries, route comparison, and engineering implications
4. Explicit state/mode toggles that re-focus the visual instead of showing everything equally
5. UI text that answers: what is active, why it matters, and what the engineering handle is

## Recommended panel structure
### Panel 1: Story panel
- Purpose: teach the mechanism in the correct order
- Good structure: input layer -> sensing layer -> amplification layer -> output layer
- Keep this stable across modes

### Panel 2: Mechanism lab
Include:
- `状态判读` — what biological state the current mode represents
- `主同化出口` or `主作用路径` — the dominant route/pathway under that state
- `工业启示` / `engineering insight` — why the mechanism matters for design
- `高氮/低氮状态` comparison when relevant
- `工程抓手` — OE, constitutive activation, feedback relief, transport unlocking, carbon skeleton coupling, etc.

## Interaction pattern
Use explicit buttons/tabs for scientific submodes, for example:
- 总览
- 摄入阀门
- 信号级联
- GS-GOGAT
- GDH 支路

Each mode should do two things simultaneously:
1. Update the explanation card text
2. Re-highlight only the corresponding nodes/edges/labels in the figure

Do not only change text without changing the network, and do not only highlight the network without updating the explanation.

## Visual rules
- De-emphasize irrelevant network regions instead of hiding everything abruptly
- Keep labels visible for the active mechanism subset
- Reserve pulses/glow for only 1-3 truly central nodes
- Use the right panel for dense explanation; keep the SVG itself visually clean
- In mechanism mode, disable unrelated controls if they create visual conflict

## E. coli ammonia assimilation example
Good mechanism decomposition:
- Input: AmtB-mediated ammonium uptake
- Sensing: GlnD reading Gln status
- Signal relay: PII/GlnB/GlnK state switching
- Amplification: NtrB/NtrC transcriptional activation
- Assimilation outputs:
  - GS-GOGAT = high-affinity, low-ammonium route
  - GDH = high-ammonium shortcut

## Pitfalls
- Do not present all highlighted nodes as equally important; users need hierarchy
- Do not treat GDH as the main low-ammonium route
- Do not explain regulation only in hover tooltips; the main story must be visible without hovering
- Do not reuse a global pathway title when the active view is a mechanism-specific v3/v4 topic mode
- Do not leave destructive/conflicting controls active in a focused mechanism mode

## Good default for this user
For scientific HTML artifacts, favor:
- Chinese UI
- research-dashboard information hierarchy
- compact explanatory cards
- engineering-language interpretation, not only biochemical annotation
- single-file HTML that works locally without extra runtime
