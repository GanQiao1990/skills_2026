---
name: interactive-scientific-diagrams
description: Optimize interactive scientific HTML/SVG diagrams for presentations, reports, and article embeds. Use for pathway maps, regulatory networks, mechanism schematics, and other browser-based explanatory figures that need clearer focus, hierarchy, and storytelling.
---

# Interactive Scientific Diagrams

Use this skill when a user asks to improve an existing interactive scientific figure, especially HTML/SVG artifacts with multiple modes, overlays, labels, and controls.

## Goal

Turn a dense exploratory figure into a presentation-ready explanatory artifact:
- clearer narrative focus
- lower visual noise
- stronger emphasis on the active mechanism
- controls that match the current mode
- framing that lands the user on the important region immediately

## Default workflow

1. Identify the active storytelling mode.
   - Determine whether the user wants the whole figure improved or one subview/topic improved.
   - If one topic is named, optimize that mode first instead of globally restyling everything.

2. Preserve data semantics.
   - Do not change scientific meaning, node identities, edge meaning, or counts unless the user asked.
   - Prefer layout, copy, emphasis, and interaction changes over data rewrites.

3. Build a mode-specific focus layer.
   - Add a dedicated title/subtitle for the focused mode.
   - Add a small explanatory panel that tells the reader how to read the mechanism in order.
   - Reduce prominence of off-topic families, badges, or labels.

4. Strengthen visual hierarchy for the active pathway.
   - Increase stroke width / contrast / glow only for the active nodes and edges.
   - Dim non-core regions rather than hiding everything unless the hidden state is already established in the artifact.
   - Use animation sparingly for the true control points or outputs.

5. Align controls with the mode.
   - Disable or relabel controls that would create contradictory overlays in the focused view.
   - Example: if a topic mode is already a curated overlay, disable unrelated clutter toggles instead of stacking them.

6. Reframe the viewport.
   - In topic mode, reset zoom/pan to the relevant local region instead of the whole-canvas default.
   - Switching modes should also switch framing.

7. Synchronize explanatory copy.
   - Update header text, bottom info bar, legends, or callouts so the current mode explains itself.
   - The visible copy should answer: what am I looking at, why this subset, and how should I read it?

8. Verify interaction coherence.
   - Ensure mode switching restores the right title, control state, overlays, and viewport.
   - Check that buttons, labels, and focus panels do not drift out of sync.

## Proven patterns

### 1. Topic-mode storytelling
When one mechanism matters more than the full map, create a dedicated mode with:
- mode-specific heading
- one-sentence pathway summary
- numbered reading order (input -> sensing -> amplification -> output)
- only the most relevant nodes visually promoted

### 2. Focus panel pattern
A compact floating panel works well when the figure is dense. Include:
- a small badge naming the mode
- a strong title written as a causal story
- 3-5 short steps explaining the read order
- one practical interpretation line for engineering or experimental implications

### 3. Control pruning
In focused scientific views, fewer controls are better.
Disable or mute controls that introduce unrelated dimensions when a curated mode is active.

### 4. Auto-framing by mode
Use separate reset/initial camera states per mode.
A global fit is often wrong for subpathway explanation.

## Pitfalls

- Do not only dim the rest of the figure and call it done; add explanatory copy so the user can present from the artifact.
- Do not let button labels stay generic across very different modes.
- Do not keep all toggles equally available if some become misleading in a curated mode.
- Do not reuse the same viewport for whole-network and subnetwork views.
- Do not over-animate all highlighted elements; pulse only the true bottlenecks, regulators, or outputs.

## For this user

When optimizing scientific visuals for this user:
- prioritize mechanism clarity over decorative polish
- make the figure usable for direct explanation in Chinese
- favor explicit causal reading order over generic 'interactive dashboard' styling
- surface industrial or engineering interpretation when the underlying figure is about metabolic control or pathway engineering

## Support files

- `references/metabolic-pathway-focus-mode.md` — concrete notes from a metabolic-pathway HTML optimization session, including the focused-mode structure and control/viewport patterns that worked.

## Done criteria

A good optimization should make it obvious:
1. what subset the viewer should attend to
2. in what order to read it
3. which nodes/edges are the true control points
4. which controls are still relevant in this mode
5. why the focused view matters scientifically or engineering-wise
