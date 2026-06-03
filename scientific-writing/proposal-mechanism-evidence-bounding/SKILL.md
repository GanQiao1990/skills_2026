---
name: proposal-mechanism-evidence-bounding
description: Write scientific and biomedical proposal text with strict evidence boundaries, especially for mechanism-heavy sections and design-method descriptions. Use when a user objects that a mechanism is insufficiently supported, a workflow slogan is too vague, or terminology such as nitrogen utilization vs nitrogen assimilation is being conflated.
license: Proprietary. LICENSE.txt has complete terms
---

# Proposal mechanism evidence bounding

Use this skill when drafting or revising grant/proposal text in which:
- a mechanistic module is attractive but not yet directly validated
- the user says a claim "needs proof", is "too broad", or sounds too certain
- a method description uses slogan-like labels instead of executable stages
- metabolism terminology needs tighter scientific boundaries

## Core principle

In proposal writing, separate three layers explicitly:
1. literature-supported facts
2. engineering rationale / transferable precedent
3. project hypothesis to be tested

Do not let layer 2 or 3 masquerade as layer 1.

## Required workflow

### 1) Audit each mechanistic claim
For each proposed control element or module, classify it as:
- directly supported in the same context
- supported in adjacent contexts only
- currently a candidate engineering strategy

If support is adjacent rather than direct, write it as a testable strategy, not an established mechanism.

### 2) Downgrade overstrong mechanism language
Preferred replacements:
- "drives control" -> "serves as a candidate control strategy"
- "will enable" -> "is expected to be evaluated for its ability to"
- "established execution mechanism" -> "testable execution configuration"
- "proved" -> "supported by prior studies in related systems"

### 3) Replace pipeline slogans with staged operations
If text says something like:
- broad generation / local refinement / cross-model audit

rewrite it into concrete stages such as:
- constrained initial candidate generation
- seed compression / first-pass filtering
- structure-sequence iterative refinement
- independent orthogonal model review
- multi-metric ranking for wet-lab entry

Whenever possible, name the metric families, not just the models. For example:
- interface confidence
- fold confidence / stability proxy
- clash or geometry penalties
- target-site / pocket coverage

### 4) Stage proximity-validation methods as a screening-to-mechanism chain
When writing or reviewing a binder/proximity validation plan, do not present all readouts as flat parallel tasks. Organize them into a minimum convincing sequence:

1. high-throughput functional screening first
   - e.g. flow-cytometry GFP loss or equivalent population-scale reporter
   - use this layer to rank candidates and compress the wet-lab entry set
2. visual readout second
   - fluorescence images are supportive only
   - use them to illustrate representative hits and controls, not as the primary quantitative proof
3. protein-level confirmation third
   - use Western blot or equivalent protein quantification on top hits to show the reporter/target protein truly decreases
   - if a recruited effector such as ClpX could vary in expression, check effector abundance only as a control for false ranking, not as the main readout
4. mechanism and benchmark controls throughout
   - include a nonbinding/scrambled control
   - include loss-of-target-binding-arm and loss-of-effector-recruitment-arm controls to prove proximity dependence
   - include a traditional degron or known positive route as a benchmark/assay anchor
5. burden/specificity check last
   - a minimal growth or non-target control is usually enough for an early package
   - do not force omics-scale burden analysis unless the claim requires it

Preferred phrasing pattern:
- "primary functional triage by flow cytometry"
- "fluorescence imaging as representative visual support"
- "protein-level confirmation by Western blot on prioritized hits"
- "mechanism-split controls establishing target-binding and effector-recruitment dependence"
- "traditional degron positive control as assay benchmark"

This pattern is especially useful when the user asks "how should we organize the wet experiments" for a partially completed design story and wants the smallest package that still feels complete.

### 5) Keep proposal language submission-ready
The output should read as a standalone proposal section, not as internal commentary about what the section is doing.
Avoid meta phrases such as:
- "换句话说"
- "真正意义在于"
- "这里我们"
when they make the text sound like explanation notes rather than formal submission prose.

### 5) Tighten metabolism terminology
Do not casually equate nitrogen-source use with nitrogen assimilation.
Prefer explicit distinctions:
- nitrogen uptake: external nitrogen acquisition/transport
- nitrogen utilization: broader productive use of supplied nitrogen
- nitrogen assimilation: incorporation into central metabolites such as glutamate/glutamine nodes
- downstream nitrogen allocation / redistribution: partitioning into product synthesis and related states

If the biology is mixed or not yet pinned to a specific node, use "nitrogen utilization" or "nitrogen uptake and assimilation efficiency" rather than asserting "nitrogen assimilation" alone.

## Circular permutation / topological rearrangement rule
When circular permutation or topology-rearrangement logic appears in a proposal:
- treat prior sensor/switch literature as enabling precedent, not direct proof in the new host/module
- state that effects on stability, binding, folding, and energy landscape are site-dependent and hard to predict a priori
- frame the module as a candidate dynamic-control strategy that requires comparative validation
- avoid writing circular permutation as if it is already the final confirmed mechanism

Preferred phrasing pattern:
- "based on circular-permutation-enabled topological rearrangement"
- "a candidate dynamic control strategy"
- "to be comparatively evaluated for responsiveness, stability, and downstream phenotypic transmission"

## Pitfalls
- Do not upgrade a literature precedent into a project-specific proof.
- Do not keep catchy method slogans when the user asked for clearer questions or workflow.
- Do not collapse uptake, assimilation, and allocation into one nitrogen term.
- Do not write speculative dynamic switches as guaranteed executable modules.

## Proposal structure optimization

When a proposal has gone through many iterations (v1→v10+) and accumulates
redundant content, apply these structural optimizations:

### Split wall-of-text 摘要
The abstract should be 2 paragraphs:
1. **Core content**: What the project does, how, and why
2. **Literature validation**: Key 2024-2026 findings that confirm feasibility

### Elevate competitive landscape to formal section
Don't bury competitive analysis inside the background. Promote it to a
top-level section (## 二·五 or equivalent) with:
- Most direct competitor → cite + differentiate (molecular vs systems level)
- Supporting breakthroughs → latest findings validating the approach
- Technology window → why NOW is the right time
- Gap confirmation → what remains unaddressed

### Use the "三个不是+一个而是" differentiation pattern
```
不是做A（已有文献做了）
不是做B（已有文献做了）
不是做C（已有文献做了）
而是做D——这条方法链本身才是核心产出
```

### Weave citations throughout, not just in references
- Background: field-level validation
- Research approach: timing justification
- Innovation points: differentiation from existing work
- Expected results: comparison benchmarks

### Add DOIs to key references
```
Author et al. (Year) Title. *Journal* Volume: Pages. DOI: xxx. N cites.
```

## Engineering-target table / CSV rule

When the user asks to add a mechanism-heavy idea into an engineering-target table, summary table, or CSV:
- do not upgrade a regulatory or post-translational hypothesis into a high-confidence engineering target just because the mechanism is attractive
- if the claim is not directly supported in the exact production context, write it as a `candidate strategy` / `testable hypothesis`
- if the effect is not captured by FBA or the current model, state `not directly modeled` rather than implying model support
- for upstream regulators such as `glnD`, `PII`, or `NtrB–NtrC`, distinguish the regulator from the downstream nitrogen-assimilation readouts; do not describe an upstream regulator like `glnD` as a downstream assimilation gene
- if the user mixes nearby systems or names (for example `Nar` vs `Ntr`), normalize the mechanism to the correct axis before writing it into the deliverable

Preferred phrasing pattern for such rows:
- `candidate upstream nitrogen-starvation mimic`
- `condition-dependent, not guaranteed`
- `stronger as a testable candidate than an established target`

For nitrogen-state regulatory candidates, preferred validation chain:
- `PII-UMP / PII ratio`
- `GS adenylylation state`
- `Ntr reporter output` such as `PamtB`, `PglnK`, `PglnA`
- `Gln/Glu pool`
- final `titer / yield / productivity`

This is especially important for ideas like binder-mediated biasing of `GlnD` UTase/UR balance: the mechanism may be biologically plausible and proposal-worthy, yet still belong in the table as a low-confidence candidate rather than a confirmed production target.

## Proposal phrasing cleanup for nitrogen-state modules

When revising proposal text after user feedback about legibility or scientific framing, tighten these recurring phrases:

- Replace vague `状态判读` with more operational wording such as `状态读出`, `可量化读出`, or `状态 readout`, unless the task is specifically about building a sensor for process monitoring.
- Do not describe a whole pathway vaguely as `主同化出口` unless you immediately anchor it to the concrete module. Prefer `GlnA-GltBD 主同化出口`, `GS-GOGAT 主同化出口`, or another explicit node/module.
- Avoid stacking multiple fuzzy `窗口` phrases in one paragraph (`生产窗口`, `状态窗口`, `响应窗口`, etc.) when they create visual clutter or ambiguous scope. If the meaning is temporal, prefer explicit stage wording such as `生产阶段`, `生产期中后段`, or `生长—生产切换阶段`. Reserve `窗口` for cases where an actual optimization interval or response range is being discussed.
- For upstream regulatory hypotheses, state that the earliest expected gain is in `state readouts` or `assimilation-output stability`, and only then discuss possible titer improvement. Do not jump directly from upstream control logic to `显著增产` without the intermediate readout chain.

Preferred rewrite pattern:
- `改善状态判读` -> `改善状态读出并提高可量化 readout 的一致性`
- `维持主同化出口` -> `维持 GlnA-GltBD 主同化出口的稳定输出`
- `在两个窗口中起作用` -> `在生产阶段中后段更容易维持连续氮同化状态`

## Minimal deliverable checklist
Before finalizing a proposal section, verify that:
- every mechanism-heavy sentence has an evidence level you can defend
- each method paragraph is operational rather than slogan-like
- hypothesis language is visibly distinct from established literature fact
- terminology around metabolism and regulation is biologically precise
- regulatory candidate rows in tables/CSVs are clearly separated from directly supported production targets

## Research assistance workflow

When assisting with proposal writing and literature research, follow this priority order:

1. **Project documentation first** — Check existing project files, notes, and documentation
2. **External search second** — Attempt literature searches if project docs are insufficient  
3. **Comprehensive synthesis** — Combine available information from all sources

See `references/research-assistance-fallback-strategy.md` for detailed workflow when external searches fail.

## Support files
- `references/circular-permutation-and-nitrogen-terminology.md` — concise reference for evidence-bounded circular-permutation wording and nitrogen-terminology choices in proposal writing
- `references/research-assistance-fallback-strategy.md` — workflow pattern for scientific research assistance when external literature searches fail
- `references/RESEARCH_ASSISTANCE_WORKFLOW.md` — additional workflow notes for research assistance