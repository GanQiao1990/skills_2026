# First-principles paper adaptation for 公众号 articles

Use this reference when a user wants a paper rewritten for public-facing Chinese distribution but asks for stronger logic than a normal summary.

## Trigger phrases
- 从第一性原理
- 为什么这么做
- 什么目的
- 为了完成这个目的他们做了什么
- 这一步证明了什么
- 为什么先筛这些，而不是直接优化

## Required structure
Turn the article into a causal chain, not a flat list of results.

Recommended order:
1. Root problem
   - What real-world or engineering contradiction defines the paper?
   - Example pattern: small size helps delivery, but short recognition length hurts specificity.
2. Why the starting system is insufficient
   - State the limitation in mechanistic terms, not just as "performance was low".
3. First-screen objective
   - Explain why the authors screened orthologs / constructs / conditions.
   - The question should read like a design hypothesis, not a catalog exercise.
4. Why this comparison set
   - Explain why related homologs, adjacent families, or ancestral relatives were included.
   - Good wording: included to reveal which structural or RNA/protein features may be necessary for the target function.
5. Why these assay conditions
   - Explain why a guide length, reporter, TAM/PAM filter, cell type, or mismatch panel was chosen.
   - If the paper later states the reason in Discussion, bring that explanation forward into the article.
6. What each stage proved
   - For every stage, use: objective -> action -> result -> implication.
   - Avoid skipping from experiment to conclusion without the intermediate implication.
7. Why the next engineering step followed
   - Make the transition explicit: because stage N exposed bottleneck X, stage N+1 targeted X.
8. Application closure
   - Explain why final base-editing / epigenome-editing / in vivo experiments are not decorative add-ons but the closure of the design logic.

## Writing rules
- Separate direct evidence from interpretation.
- If a number is a headline claim, connect it to what it proves.
- Preserve caveats: restrictive TAM/PAM, off-target method limitations, immunogenicity unknowns, restricted tissue validation, etc.
- For PR/expert tone, sound confident in the logic, not inflated in the claims.

## Good transformation pattern
Bad:
- They screened many proteins, found a better one, then optimized it and showed an application.

Good:
- They screened many proteins because the original system's short effective guide length made specificity fundamentally hard to improve by blind mutagenesis alone. Related type II-D Cas9s were included not as window dressing but because they are the closest homologs to IscB and could reveal what protein/RNA features matter for mammalian editing. Using long guides in the first screen functioned as a deliberate high-specificity filter. Once the screen pointed to a clade with REC-like features, REC-domain engineering became the next logical move.
