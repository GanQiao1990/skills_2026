# Version8 proposal patterns for de novo metabolic-control projects

## Scope

This reference condenses a session pattern where a microbial amino-acid production proposal had to be tightened into two core scientific questions and re-grounded with PubMed-backed background plus local mimic evidence.

## PubMed-backed author-pattern summary

### Liming Liu pattern
Most useful framing is not “amino-acid expert” in general, but an industrial high-production route centered on:
- identifying the earliest mismatch layer in production strains,
- carbon/nitrogen coordination,
- Gln/Glu pool support,
- NADPH/redox reinforcement,
- spatiotemporal productivity,
- protein-status engineering,
- and eventually de novo proteins as executable intracellular modules.

Representative PMIDs used in session:
- 40676011
- 37939975
- 36328295
- 34870736
- 34936092
- 39082808
- 34140131
- 29424131

### Sang Yup Lee pattern
Most useful framing is not one product pathway, but a systems-metabolic-engineering platform route centered on:
- integrated host/pathway/module/fermentation design,
- platform-chassis reuse,
- Corynebacterium glutamicum product migration,
- growth-production balance,
- fermentation competitiveness,
- and cell-factory level reasoning.

Representative PMIDs used in session:
- 22596205
- 30737009
- 37778304
- 36635195
- 36341775
- 37451533
- 36357213
- 40966432

## Local mimic-derived ranking pattern

Source file used:
- `./mimic_results/multi_amino_acid_mimic_summary.csv`

Relevant product comparisons from session:

### Arginine
- nitrogen_assimilation AUC: 28.578350365356687
- narl_no3_gate AUC: 27.35337767015869
- nitrogen advantage: +4.48%
- final pool advantage: +4.57%
- nitrite risk: nitrogen 0.0 vs narl 0.0752999665950547

Conclusion: for arginine-centered proposals, nitrogen-state / NtrC framing is stronger than NarL-first framing.

### Glutamate
- nitrogen_assimilation AUC: 35.886960185336626
- narl_no3_gate AUC: 33.419008406869345
- nitrogen advantage: +7.38%
- final pool advantage: +7.44%

Conclusion: glutamate also supports nitrogen-state-first framing.

### Lysine / Threonine
- NarL can be slightly better in local mimic output.
- Do not generalize “NtrC is always better.”
- Product-aware wording is mandatory.

## Execution-layer ranking pattern

When the user asks for a more suitable execution layer than NtrC/NarL themselves, use this ranking for arginine/nitrogen-state projects:

1. `ArgG` or `ArgG-ArgH` as minimum product-proximal execution closure
2. `amtB/glnA/gltBD/gdhA` as primary nitrogen-assimilation execution layer
3. `pntAB/sthA` as redox-support execution layer
4. `ArgB-ArgC-ArgD` as second-stage spatial organization layer
5. `ArgH + ArgO/LysE`-type synthesis/export coupling when product backpressure matters

Important lesson:
- NtrC and NarL are often better described as sensing/routing layers than as the best direct execution layer.

## Entropy-gated writing pattern

The successful wording pattern in this session for de novo execution modules was:
- choose a loop-region permutation site,
- cut the receptor there,
- reconnect old termini with a GS linker,
- create a circularly permuted receptor,
- create a ligand-free high-entropy OFF state,
- couple ligand-induced entropy reduction to restoration of an executable ON state,
- and then couple that state change to binder recruitment/proximity/occlusion/release.

Key phrase to preserve in future writing:
- “default unstable, default OFF protein physical state pulled back into an executable ordered state by ligand binding.”

## Phospho-Asp validation pattern

Do not anchor validation on routine global phosphoproteomics.
Use:
1. functional reporters and metabolic readouts,
2. site-dependent breaks and dead controls,
3. in vitro phosphotransfer / targeted chemistry / targeted MS only for top candidates.

## Wording pattern for amino salts

Safe proposal wording:
- amino salts count as nitrogen-assimilation support only when their nitrogen is taken up and demonstrably enters central nitrogen metabolism and then product/biomass.
- otherwise they should be described as culture-condition modifiers, not automatically as strengthened nitrogen assimilation.
