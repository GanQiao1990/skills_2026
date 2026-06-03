# Virtual-cell mimic for multi-amino-acid production proposals

Session-derived pattern for extending a NarL/NO3 virtual metabolic project into a broader proposal-level amino-acid production platform.

## Durable lesson

When the user asks for “每一步都做状态 mimic” and says the project should cover amino-acid production beyond NarL, do not leave the proposal framed as NarL-only. Convert NarL into one representative state-gating instance inside a reusable virtual-cell mimic framework.

## Required state variables

Use the same state machine for every target amino acid:

| State layer | Computational / experimental readout | Purpose |
|---|---|---|
| Oxygen state | DO / respiration window | Separate growth, shift, and production phases |
| Nitrate input | NO3 uptake / pulse / linear feed | Test whether low-oxygen respiratory support is active |
| Nitrite risk | NO2 peak / clearance | Detect toxicity and downstream assimilation limits |
| Redox redistribution | NADH/NAD+, NADPH/NADP+, ATP proxies | Determine whether the production window is metabolically sustainable |
| Product output | Product flux, AUC-like output, export ratio | Decide whether the state truly improves production |

## Multi-product mapping

Keep the same state machine and swap only execution-layer modules:

| Product | Execution layer | Why it is included |
|---|---|---|
| Arginine | `argB/argG/argH`, `argO`, `NirBD-GlnA-GltBD/GdhA`, `pntAB/sthA` | Best main validation product for NarL/redox/nitrogen coupling |
| Lysine | `lysC/lysA/lysE`, nitrogen-assimilation and export modules, `pntAB/sthA` | Best migration/industrial validation product |
| Glutamate/glutamine | `gltBD/gdhA/glnA/amtB` | Tests whether nitrogen input and redox state redirect precursor pools |
| Threonine / other N-rich amino acids | Product-specific pathway enzymes, exporters, and competing branch suppression | Tests transferability of the mimic framework |

## Proposal patching pattern

When editing an existing proposal file:

1. Update the abstract first so the project is not read as NarL-only.
2. Add a dedicated subsection such as “虚拟细胞状态 mimic 与多氨基酸扩展”.
3. Keep NarQ-NarL as a representative low-O2 / nitrate gate, not the only production-enhancement axis.
4. Preserve direct evidence vs inference: NarL is a strong mechanistic hypothesis and state-gating example, while lysine/glutamate/threonine extensions are migration tests unless local data already proves them.
5. Update expected results, innovation, and project-boundary sections so the platform reads consistently as a reusable multi-amino-acid production mimic.
6. If the user says “完成这个 mimic 过程”, implement it, not just describe it: create a runnable script, generate timecourse/summary/manifest outputs, produce figures, and write a concise report in the target project directory.

## Implementation pattern

A first-pass multi-amino-acid virtual-cell mimic can be implemented as a deterministic state-machine script with:

- Product configurations for base flux, nitrogen need, redox need, export need, byproduct pressure, nitrite sensitivity, and module gains.
- Scenario configurations for high-O2 baseline, low-O2 shift, pathway enhancement, NarL+NO3 gate, nitrogen assimilation, redox balancing, export enhancement, enzyme complex, and minimal combo.
- Per-time-step updates for oxygen state, nitrate pool, nitrate respiration, nitrite generation/clearance, nitrogen state, redox state, export state, pathway state, burden penalty, byproduct flux, product flux, product pool, intracellular product, and export ratio.
- Outputs: `*_timecourse.csv`, `*_summary.csv`, `*_manifest.json`, publication-style trajectory/heatmap/tradeoff figures, and a markdown report.

## Example wording

“本项目并不是只为 NarL 建模，而是先建立一套可复用的氨基酸 production mimic，再将 NarL 作为其中一个最清晰、最适合验证的状态门控实例。”

## Pitfalls

- Do not frame NarL as the sole enhancement mechanism if the user asks to cover all amino-acid production mimics.
- Do not claim transferability is proven; label lysine and other amino-acid cases as migration validation unless direct results exist.
- Do not collapse all products into arginine-specific readouts; use “目标氨基酸” and product-specific execution nodes.
