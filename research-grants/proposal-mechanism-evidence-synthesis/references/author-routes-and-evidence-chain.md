# Author routes and evidence-chain mapping for biotech proposals

## What this reference is for
Use this reference when a proposal task is not just "summarize papers" but "convert author/field literature plus local evidence into a sharper project storyline".

## Pattern: author-centered literature synthesis
When the user asks for background on named authors, do not stop at listing representative papers. Extract:
1. recurrent bottlenecks they solve
2. preferred intervention level
3. what they optimize repeatedly
4. what gap remains that the current project can occupy

### Example route extraction
#### Liming Liu-type route
Typical recurring themes:
- industrially grounded amino-acid or platform-chemical production
- carbon-nitrogen coordination
- Gln/Glu pool maintenance and ammonium assimilation bottlenecks
- cofactor/redox and productivity balance
- tolerance, efflux, and late-stage fermentation stress

Proposal value:
- strong support for choosing product-state and nitrogen-state mismatches as the main problem
- supports writing dynamic control around nitrogen/redox/productivity rather than only static pathway amplification

#### Sang Yup Lee-type route
Typical recurring themes:
- systems metabolic engineering
- chassis selection and reuse
- pathway modularization
- branch-pathway deletion, transport engineering, cofactor balancing, process integration
- platform expansion from amino-acid chassis to derivative chemicals

Proposal value:
- supports whole-system framing and prioritization of the most direct product-relevant axis
- supports describing secondary axes as modules rather than inflating them into the main thesis

## Pattern: choosing a main signal axis
Use the combined ranking:
1. direct mechanistic relevance to the product bottleneck
2. local evidence advantage
3. feasibility of measurement/validation
4. safety/risk cost of the route
5. literature support density

If a legacy axis scores worse than a more direct axis, demote it.

### Example from a proposal session
If local mimic results suggest a nitrogen-state module outperforms a nitrate-gated regulator for arginine-relevant outputs, write:
- nitrogen-state sensing/control as the main axis
- nitrate/oxygen-linked signaling as auxiliary context, comparison, or later-stage refinement

Do not preserve the older main axis just because it is already present in drafts.

## Pattern: labile phospho-state evidence chains
For unstable phospho-chemistries such as phospho-Asp-like states:
- do not promise routine global phosphoproteomics
- instead write a 3-layer chain:
  1. functional output/readout
  2. dependency mutants / dead-state controls
  3. targeted biochemical confirmation for top candidates

This lets the proposal stay ambitious but technically credible.

## Pattern: wording for amino salts / exogenous nitrogenous supplements
Use careful language:
- "organic nitrogen input" or "nitrogen-containing supplement" by default
- only say "nitrogen assimilation enhancement" when there is evidence the nitrogen enters central nitrogen metabolism and contributes to product/biomass formation

## Fast checklist before finalizing proposal text
- Did the designed protein/binder/switch remain the execution layer in the final wording?
- Are there only 2 core questions unless biology truly forces more?
- Did the main control axis survive a literature + local-evidence re-ranking?
- Are measurement claims technically realistic?
- Did the final prose remove planning/meta language?
