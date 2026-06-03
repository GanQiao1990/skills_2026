# V7 pathway maintenance patterns

Context: local interactive pathway page with embedded CSS + JS arrays, used for amino-acid / nitrogen-assimilation explanation.

## Coordinate-edit convention

For `/home/qiao/qiao_design/公众号/fig4_metabolic_pathway_interactiveV7.html`:
- logical node positions are stored in `const NODES = [...]`
- render scale constant is `const S = 88`
- user movement requests such as “上调/下调/左调/右调 N 个体位” were correctly implemented as direct deltas on the node’s `x` / `y`
- therefore edits should modify the `NODES` entry, not rendered SVG transforms

Example from session:
- AmtB moved from `x:-6.45, y:18.0` to `x:-4.45, y:19.0`
- this resolved previous overlap risk and placed it between NtrBC and NH4 visually

## NtrC regulon cluster integration pattern

When the user asked to strengthen the relationship between NtrC and nitrogen assimilation, the useful pattern was:

1. Add a dedicated node representing the downstream transcriptional program, not just prose.
   - Example node:
     - `id: 'NtrClust'`
     - label: `NtrC regulon`
     - subtitle: `amtB-glnK · glnA · gltBD`

2. Connect it explicitly in the graph:
   - `NtrBC -> NtrClust`
   - `NtrClust -> AmtB`
   - `NtrClust -> Gln`

3. Update mechanism subsets so the new node appears in focused views:
   - `nitrogen`
   - `full`
   - `uptake`
   - `signal`

4. Update version-specific CSS selectors that determine which ver3 nodes remain fully visible / highlighted.
   - Without this, the node may exist in data but stay visually dim or excluded.

5. Add matching prose in the mechanism panel.
   - Best framing: NtrC-P is not only turning on one gene; it coordinates an assimilation program spanning input (`amtB-glnK`), fixation (`glnA`), and high-affinity sink expansion (`gltBD`).

## Why this matters biologically in presentation

A better explanation for nitrogen-assimilation figures is:
- AmtB = input valve
- GlnD/PII/NtrBC = nitrogen-state sensing and amplification
- NtrC regulon = transcriptional program layer
- GS-GOGAT/GDH = assimilation/output layer

This lets the diagram tell a four-layer story:
1. uptake
2. sensing
3. regulon-level transcriptional amplification
4. metabolic incorporation into Gln/Glu

That framing is more useful for project-writing and mechanism explanation than treating `glnA`, `gltBD`, and `amtB-glnK` as isolated labels.

## Layout + UX cleanup patterns learned from follow-up fixes

After repeated coordinate edits, three follow-up cleanup patterns proved durable:

1. Do not leave a cluster node extremely far from the module core just because the user asked for one directional move.
   - If the requested move produces an obviously detached layout, it is reasonable in a later cleanup pass to restore the node closer to the module and report the corrected coordinates.
   - For the V7 nitrogen module, moving `NtrClust` too far left made the cluster read like a detached annotation instead of an in-module transcription layer.

2. Reposition the badge when the node moves materially.
   - The badge `NtrC regulon cluster` can become biologically misleading if it stays near the old position while the node is moved far away.
   - Badge and node should read as the same explanatory object.

3. Keep default active module aligned with the current diagram emphasis.
   - In V7, once the nitrogen module became the main revised focus, it was more coherent to switch:
     - the active `.v5-module`
     - the active `.ml-btn`
     - `let mechanismMode = 'nitrogen'`
     - and the `switchVersion(v===5)` default to `mechanismMode = 'nitrogen'`
   - Otherwise the page opens on `arginine` while the newly revised biology and explanatory text are centered on nitrogen assimilation.

4. Remove stale commented-out graph edges after refactoring logic.
   - Example durable cleanup: after routing `NtrBC -> Gln` through `NtrClust`, remove the commented-out old edge rather than keeping a dead code note in the `EDGES` array.

5. Fill descriptive metadata consistently.
   - If a new node represents a cluster/regulon, populate its descriptive field (for example `enzyme:'NtrC regulon cluster'`) rather than leaving the string blank, so tooltip/info formatting stays consistent with surrounding nodes.

## Verification pattern

For single-file HTML apps with embedded JS:
- confirm modified node coordinates by parsing the HTML text directly
- confirm new IDs/edges with direct string checks
- extract `<script>...</script>` and run `node --check` on the assembled JS for syntax validation

This is a lightweight but sufficient verification loop for layout + interaction edits when no browser render check is requested.
