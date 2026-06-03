# Interactive HTML micro-edits

Use this reference when the task is not "design a new page" but "adjust one element inside an existing interactive HTML artifact" such as a local SVG/JS pathway map.

Checklist:
- Find the canonical layout source before editing: inline node arrays, data objects, frame definitions, CSS transforms, or runtime-generated positions.
- Search for saved-layout logic (`localStorage`, persisted JSON, restore/reset layout functions). A source edit may not be what the browser renders if saved positions overwrite defaults.
- Apply the smallest viable change. For coordinate requests, edit only the target node unless the surrounding geometry forces additional moves.
- Re-check adjacent nodes, labels, and edges after movement; report collisions or overlaps explicitly.
- In the reply, include the exact file path plus the before/after coordinates or delta.

Session-specific note from pathway-map editing:
- In `fig4_metabolic_pathway_interactiveV7.html`, node defaults are defined inline as `{id, x, y, ...}` and then copied into `DEFAULT_NODE_LAYOUT`; runtime can override them via `applyStoredNodeLayout()` from `localStorage`.
- Moving `AmtB` from `y:20.0` to `y:18.0` satisfies a literal "move up by 2 units" request but causes overlap with `PII` at the same coordinates. When a requested move causes overlap, call it out and offer a nearby non-overlapping coordinate.
