---
name: proposal-mechanism-evidence-synthesis
description: Build proposal-ready scientific background and core-question framing from literature, local evidence, and mechanism constraints. Use for biotech/biomedical project proposals that need clear core questions, evidence chains, and executable technology positioning rather than generic review text.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
metadata:
  skill-author: Hermes Agent
  tags: [proposal, grants, literature, evidence-synthesis, biotechnology, biomedical, mechanism]
  category: research-grants
---

# Proposal Mechanism-Evidence Synthesis

## When to use
Use this skill when the user wants to:
- turn literature into proposal background, not just a paper list
- reduce a project to 1-3 core scientific questions
- decide whether a proposed regulatory axis is strong enough to be a main storyline
- integrate local simulation/mimic data with literature to refine aims
- write Chinese proposal text that reads as a standalone submission-ready document
- choose between several signaling/control routes while preserving mechanism fidelity

## Core principle
The proposal should be organized around the smallest number of mechanistically defensible questions. Literature is used to justify why those questions matter; local data is used to justify why this project chooses one execution path over another.

## Required workflow
1. Define the true execution layer.
   - Ask: what exactly is the engineered object that acts in the cell?
   - If the project's novelty is a designed protein/proximity/binder/switch element, make that the execution layer rather than letting the text drift into generic systems-metabolic-engineering language.

2. Compress to the minimum viable set of core questions.
   - Prefer 2 questions unless the biology genuinely requires more.
   - Each question must be phrased as a mechanism gap plus an execution path.
   - Good pattern: "How can we use X designed element to control Y mismatch/process?"

3. Separate evidence layers.
   - Direct evidence: literature or local data directly supporting the mechanism.
   - Indirect evidence: adjacent studies supporting plausibility.
   - Engineering inference: what the proposal will test, not what has already been proven.
   - Never blur these layers.

4. Use literature to extract research routes, not flat paper summaries.
   - For each author or field, summarize recurring strategy patterns:
     - what bottleneck they repeatedly solve
     - what level they intervene at (pathway, cofactor, transport, stress, dynamic control, spatial organization)
     - what this implies for the current proposal

5. Use local evidence to choose the main axis.
   - If local mimic/simulation/omics data disagree with the original narrative, re-rank the axes.
   - The proposal's primary signal axis should be the one with the strongest combined support from mechanism + local evidence + feasibility.
   - Demote weaker axes to auxiliary layers or controls instead of forcing them into the main storyline.

6. Write proposal text in submission-ready prose.
   - Avoid meta-commentary such as "this should say" or "we can mention".
   - Write as direct final copy.
   - In Chinese, prefer compact, authoritative paragraphs with explicit mechanism terms.

## Signal-axis selection rules
- Do not keep a signaling route as the primary storyline just because it was chosen earlier.
- Prefer axes that directly couple to the product-relevant bottleneck.
- If one route acts indirectly through respiratory/stress buffering while another directly controls nitrogen/redox/precursor state, the direct route usually deserves priority.
- Auxiliary axes can remain as boundary-condition modules, comparison systems, or later-stage refinements.

## Evidence-chain design rules
### For unstable or hard-to-capture regulatory chemistries
If the key state is chemically unstable or globally hard to detect, do not promise unrealistic omics.
Use a layered chain instead:
1. functional readouts
2. dependency-mutant validation
3. targeted reconstitution / targeted analytical confirmation for top candidates

This is especially important when the state of interest is short-lived and classical global phosphoproteomics is not credible.

## Wording rules for nitrogen-source claims
Do not automatically equate amino salts or exogenous amino compounds with "enhanced nitrogen assimilation".
Use that phrase only when there is evidence that the nitrogen enters central nitrogen metabolism and contributes to product or biomass formation. Otherwise describe them as medium inputs, nitrogen-containing supplements, or conditional organic nitrogen sources.

## Output package
For a strong proposal turn, produce all of the following when useful:
1. a short literature-backed background note
2. 2 core scientific questions in final prose
3. a recommended main control axis and relegated alternatives
4. a concise evidence-chain statement for risky measurements
5. one integrated proposal-ready paragraph or section

## Common pitfalls
- letting designed elements disappear from the narrative after the introduction
- presenting a general review of metabolic engineering instead of a project-specific mechanism case
- keeping too many "core questions"
- overstating weak signal axes because they are conceptually attractive
- calling a supplement "nitrogen assimilation" without flux-level justification
- promising global phosphoproteomics for labile phospho-states
- writing planning notes instead of submission-ready prose

## Support files
- `references/author-routes-and-evidence-chain.md`: author-centered literature-to-proposal mapping patterns, including signal-axis selection and evidence-chain examples from a biotech proposal session.

## Success criteria
A good deliverable produced with this skill should let the user answer all of these clearly:
- What are the only 2 core questions?
- What is the true execution layer?
- Why is the chosen main regulatory axis better than the alternatives?
- Which claims are already supported, and which remain to be tested?
- Can the text be pasted into a proposal without rewriting the tone?
