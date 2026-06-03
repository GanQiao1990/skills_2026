---
name: de-novo-metabolic-control-proposals
description: Write and refine research proposals for microbial amino-acid production where de novo designed protein modules are the execution layer. Use for arginine/lysine/glutamate/threonine proposal framing, signal-axis selection, execution-layer ranking, and evidence-chain design.
allowed-tools: Read Write Edit Bash
license: MIT
metadata:
  skill-author: Hermes Agent
  tags: [grant-writing, proposal, metabolic-engineering, synthetic-biology, de-novo-protein, amino-acid-production, dynamic-control]
  category: research
---

# De Novo Metabolic Control Proposals

## When to use

Use this skill when the task is to write, tighten, or review a proposal for microbial amino-acid production in which de novo designed protein modules are supposed to do real regulatory work rather than serve as decorative binders or generic background technology.

Typical triggers:
- The user wants “only two core questions” rather than a broad list of aims.
- The proposal is drifting back into generic systems metabolic engineering and needs to recover a protein-execution-layer identity.
- The user asks whether a regulator such as NtrC or NarL is the better main axis.
- The task involves de novo split receptors, circular permutation, ligand-triggered rearrangement, entropy-gated switching, or programmable proximity control.
- The proposal needs a more realistic phospho-Asp monitoring strategy.

## Core positioning rule

Do not frame the project as “another systems metabolic engineering optimization study.”
Frame it as: existing metabolic engineering already identifies important bottlenecks, but still lacks a portable protein-level execution layer that can perform reversible, local, state-dependent control.

The de novo module must be written as the execution layer, not merely the sensing layer.

## Default project compression rule

Unless the user explicitly asks for more, compress the proposal to two core scientific questions:

1. How to use de novo dynamic proximity elements to gate nitrogen-state / redox-ATP mismatch at the protein level.
2. How to use de novo spatial organization elements to improve local reaction efficiency and reduce diffusion loss at key pathway nodes.

Do not let the draft expand back into several parallel mini-projects.

## Preferred architecture for this class of proposal

Use a three-layer architecture.

### 1) State-sensing layer

For arginine- or nitrogen-centric production problems, prefer:
- NtrB–NtrC as the first sensing axis.

Use NarQ/NarX–NarL only as:
- a low-oxygen / nitrate boundary-state auxiliary layer,
- a comparison system,
- or a phase-switching helper.

Reason: NtrC is closer to nitrogen limitation, nitrogen assimilation, and transport/assimilation programs; NarL is more indirect and centered on respiratory/nitrate-state rewiring.

### 2) Direct execution layer

Default execution-layer ranking for nitrogen-centric amino-acid production:
- `amtB`
- `glnA`
- `gltBD`
- `gdhA`

Parallel support layer:
- `pntAB`
- `sthA`

These are usually better execution nodes than global response regulators when the goal is a short causal chain and a clean grant narrative.

### 3) Product-proximal execution layer

For arginine-focused proof-of-concept, strongly consider:
- `ArgG` or `ArgG-ArgH` as the minimum product-proximal execution module.

Use these when the proposal needs a sharper “execution-layer closure” story with direct readouts.

Second-stage spatial-organization modules can include:
- `ArgB-ArgC-ArgD`
- `NirBD-GlnA-GltBD/GdhA`
- synthesis-export coupling modules such as `ArgH + ArgO/LysE`-type exporters.

## Entropy-gated de novo execution logic

When the user proposes split receptors or circular permutation, do not paraphrase this as vague “allosteric change.”
Write the mechanism explicitly.

Recommended language pattern:
- choose a permissive loop-region permutation site,
- cut the natural receptor there to generate new N/C termini,
- reconnect the old termini with a GS linker,
- create a circularly permuted receptor that is intentionally destabilized in the ligand-free state,
- place the rearranged module into a structure-sensitive site of a reporter or execution protein,
- use ligand binding to reduce conformational entropy, restore local order, and switch the coupled execution module from OFF to ON.

Important framing rule:
The key value is not the reporter enzyme itself. The key value is the transferable physical principle: a default high-entropy OFF state that is driven into an ordered executable state by ligand binding.

## Evidence-chain rule for phospho-Asp systems

Do not promise routine global phosphoproteomics as the main validation route for phospho-Asp.

Use a three-level evidence chain:

1. Functional readouts
- promoter reporters (`PamtB`, `PglnK`, `PglnA`, or equivalents)
- Gln/Glu pools
- nitrogen-state and redox readouts
- growth/productivity phenotypes

2. Causal / site-dependent controls
- RR Asp→Asn/Ala
- HK His-dead controls
- scrambled binder / anchor-dead / geometry-break controls

3. Top-candidate mechanism support only
- in vitro phosphotransfer reconstruction
- fast targeted chemistry under compatible conditions
- targeted MS if needed

## Wording rule for amino salts and nitrogen assimilation

Do not write “amino salts increase nitrogen assimilation” as an absolute statement.
Use conditional wording:
- if the nitrogen from the amino salt is taken up and enters central nitrogen metabolism (for example the Gln/Glu pool) and then enters biomass or product, it counts as organic nitrogen input / nitrogen-assimilation support;
- if it only changes culture conditions, osmotic environment, or buffering, it should not be equated with enhanced nitrogen assimilation.

## Signal-axis selection heuristics

### Prefer NtrB–NtrC when
- the main product is arginine or glutamate,
- the question is nitrogen-state mismatch,
- the proposal needs a shorter causal chain,
- the user wants a stronger direct link to ammonium assimilation and Gln/Glu supply.

### Keep NarQ/NarL as auxiliary when
- the interest is low-oxygen / nitrate boundary control,
- the project wants a secondary switching layer,
- respiratory-state reallocation matters more than direct nitrogen assimilation,
- the product context is not dominated by arginine-like nitrogen constraints.

### Prefer product-proximal enzyme gating when
- the proposal needs a stronger proof-of-concept execution layer,
- the draft is too dependent on global regulons,
- the user needs a short and experimentally legible causal chain.

## Writing rules for this proposal class

- Write in formal Chinese suitable for direct insertion into a submission draft.
- Avoid meta-commentary such as “this section will say” or “the above suggests.”
- Keep the mechanism central and explicit.
- Distinguish sensing layer, execution layer, and support layer.
- Do not present NarL as if it were a direct amino-acid-production regulator if the evidence only supports a respiratory-state role.
- If the user insists on only two core questions, preserve that compression throughout background, aims, and technical route sections.

## Common pitfalls

### Pitfall 1: letting de novo design become decorative
Wrong: de novo binder is presented as a recognition module, while all real control still comes from ordinary transcription-factor rewiring.
Right: de novo geometry / entropy / proximity change determines whether execution happens.

### Pitfall 2: confusing sensing with execution
Regulators like NtrC or NarL may be excellent sensing or routing layers, but the best execution layer is often closer to the metabolic bottleneck itself.

### Pitfall 3: overcommitting to NarL
NarL can be mechanistically interesting but usually carries a longer and more conditional evidence chain for amino-acid production, especially in arginine-centered projects.

### Pitfall 4: overpromising phosphoproteomics
For phospho-Asp systems, reviewers can attack feasibility immediately if the validation section depends on standard global phosphoproteomics.

## Critical Pitfall: Oxygen Condition Assumptions

### Pitfall 5: Assuming low-oxygen fermentation when user uses high dissolved oxygen

**Wrong**: Automatically switching to low-oxygen conditions (o2_lb = -2.0) during production phase.
**Right**: Always confirm actual fermentation conditions with the user before simulation.

Many amino acid production processes use **全程高溶氧发酵** (high dissolved oxygen throughout), not low-oxygen fermentation. The oxygen condition significantly affects:
- NtrC vs NarL regulatory effectiveness
- Redox balance module performance
- Overall pathway flux predictions

**Rule**: When the user mentions "溶氧发酵" or industrial fermentation conditions, ask specifically about oxygen levels throughout the entire process, including the production phase.

### Virtual Cell Simulation Reference

For AIVM (AI Virtual Metabolism) framework implementation with:
- Modular biological constraint layers (nitrogen, redox, export, enzyme complex)
- Transcriptomics integration via GPR rules
- Time-stepped state transitions
- Multi-amino acid comparison (arginine, lysine, glutamate)

See `references/virtual-cell-simulation-patterns.md` for:
- High oxygen fermentation simulation setup
- Transcriptomics constraint implementation
- Autoresearch loop integration
- Reference project learning (METABOLIC, Ec_coli_modelling)

## Session-specific references

See `references/version8-proposal-patterns.md` for:
- PubMed-backed Liu/Lee strategy mapping,
- local mimic-derived NtrC vs NarL product ranking,
- execution-layer prioritization patterns,
- and wording templates for version8-style proposal tightening.

See `references/virtual-cell-simulation-patterns.md` for:
- AIVM framework implementation
- High oxygen fermentation correction
- Transcriptomics integration via GPR rules
- Autoresearch loop for iterative optimization
