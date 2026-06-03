---
name: interactive-metabolic-pathway-diagrams
description: Maintain and extend interactive HTML/SVG/JS metabolic pathway diagrams, especially node-coordinate edits, regulatory overlays, and synchronized explanatory copy.
---

# Interactive Metabolic Pathway Diagrams

Use this skill when editing a local interactive metabolic or biochemical pathway page implemented as a single HTML file with embedded CSS + JS data structures (nodes, edges, badges, module views, explanatory panels).

This is a maintenance-and-extension skill for pathway figures that behave like small apps, not static illustrations.

## When to use

Trigger this skill when the user asks to:
- move one or more pathway nodes up/down/left/right by explicit layout units
- add a new regulatory node, gene cluster, operon/regulon, module, badge, or callout
- expand the diagram narrative so regulation is tied to metabolic consequences
- update a pathway figure where positions are encoded in JS objects instead of raw SVG coordinates
- keep interactive figure copy, highlighted subgraphs, and visible node sets in sync after structural edits

## Core workflow

1. Locate the target node or module in the `NODES` array first.
   - Adjust `x`/`y` there.
   - Treat user phrasing like “上调/下调/左调/右调 N 个体位” as direct coordinate deltas unless the file defines a different explicit snapping system.

2. Inspect the edge model before adding regulation.
   - New biological relationships usually need explicit entries in `EDGES`.
   - If the page has filtered or versioned views (for example `ver:3` nodes/edges), make sure new elements use the right version flag.

3. Check whether the figure uses focused mechanism views.
   - If the file contains structures like `MECH_MODES`, `SCENARIOS`, badges, or module toggles, structural edits are incomplete until these are updated too.
   - Adding a new regulatory concept often requires touching all of:
     - `NODES`
     - `EDGES`
     - `BADGES`
     - focused node/edge lists in `MECH_MODES`
     - explanatory text blocks or scenario copy
     - version-specific CSS selectors that whitelist highlighted nodes

4. Add explanatory copy that states the biological logic, not just the label.
   - For regulatory clusters, explain what is co-activated/co-repressed and how that changes flux or assimilation.
   - Prefer wording like “X is not just a single enzyme switch; it programmatically couples input, assimilation, and downstream sink expansion.”

5. Verify after editing.
   - Re-read the relevant lines to confirm coordinates and inserted IDs.
   - If the HTML contains embedded JS, run a syntax check on the script block (for example via `node --check` on extracted JS) before reporting success.

## Durable project pattern

For pathway pages similar to the user’s V7 nitrogen-assimilation figure:
- Node positions live in `NODES` as logical coordinates, then render through a scale constant such as `S`.
- Visual movement requests should be satisfied by editing those logical coordinates, not rendered pixel transforms.
- Regulatory additions are usually incomplete if they appear only as nodes; they should also be represented in edges and mechanism-panel copy.
- When adding a transcriptional program (operon/regulon/cluster), connect it explicitly between the upstream regulator and the downstream metabolic entry/output nodes.

## Pitfalls

- Do not move only the displayed SVG transform if the node source of truth is in `NODES`; the next render will overwrite it.
- Do not add a regulatory concept only to prose. If it matters biologically, encode it visually in nodes/edges too.
- Do not add nodes to a versioned pathway view without updating the CSS selectors or mechanism mode whitelists that control visibility/highlight.
- Do not stop after coordinate edits if the user also asked for stronger biological explanation; interactive figures often require both geometry and narrative updates.
- Beware overlap after coordinate edits. Always compare the edited node against nearby anchors (same row / same module) before finalizing.
- Do not let a newly added cluster/regulon drift visually away from the module it is supposed to explain. If a node is moved substantially, re-check whether the connected badge/label also needs repositioning.
- Keep default UI state aligned with the current conceptual focus. If the page has been revised to emphasize a different module, update both the active HTML classes and the JS default `mechanismMode` / version-switch defaults so the initial view is not misleading.
- Remove stale commented-out edges or half-deleted transition logic after refactors. For these single-file figure apps, dead commented graph entries become a source of biological inconsistency later.
- Keep informational fields structurally consistent. If peer nodes have an `enzyme` descriptor, avoid leaving the new node with an empty string unless blank is semantically intentional.

## Minimum completion checklist

A task is complete only if all relevant boxes are checked:
- [ ] requested node coordinates updated
- [ ] new biological entity or relation added to `NODES`/`EDGES` if requested
- [ ] version/module-specific visibility rules updated
- [ ] explanatory panel/copy updated to match the new biology
- [ ] JS syntax validated
- [ ] final report includes concrete new coordinates and what conceptual layer was added

## References

- See `references/v7-pathway-maintenance-patterns.md` for concrete patterns from the user’s interactive nitrogen-assimilation / amino-acid pathway figure, including NtrC regulon cluster integration and coordinate-edit conventions.
