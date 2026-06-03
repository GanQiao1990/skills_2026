# Curated Topic Review Workflow for AI-Scientist-v2

Use this workflow when the user asks for both:
1. a domain-specific paper review template, and
2. an academic-paragraph literature review on that same topic,
often with an approximate paper-count target such as “~120 papers”.

This pattern is especially useful for protein-design topics where the repo already contains a partial review, a domain template, or a raw Semantic Scholar export.

## When to use

Trigger this workflow when all or most of the following are true:
- The task is inside `/home/qiao/dockerai/AI-Scientist-v2`
- The user wants a review template plus a literature review, not just one or the other
- The user specifies a rough corpus size (e.g. ~50, ~100, ~120 papers)
- The topic is method-centric (e.g. hallucination protein design, RFdiffusion-family methods, binder design workflows)
- The repo already has topic materials such as `ai_scientist/ideas/*review*.md`, `ai_scientist/review_templates/*.py`, or `/tmp/*papers*.json`

## Recommended output package

For this class of request, produce three coordinated artifacts, not just one:

1. `ai_scientist/review_templates/<topic>_review_template[_zh].md`
   - Human-facing paper-review template
   - Prefer paragraph-oriented prompts over bullet-only checklists

2. `ai_scientist/ideas/<topic>_academic_review[_cn].md`
   - Narrative review written in academic paragraphs
   - Organized by methods, evaluation logic, applications, and future directions

3. `ai_scientist/ideas/<topic>_literature_pool_<N>.md` plus optional `.json`
   - Curated paper pool supporting the review
   - Include year, citation count, category, title, venue
   - Use approximate N in filename when the user asked for a target-sized corpus

## Step sequence

### 1. Reuse in-repo topic assets first

Before assembling a new review, inspect whether the repo already contains:
- an existing topic review under `ai_scientist/ideas/`
- an existing review template under `ai_scientist/review_templates/`
- a raw paper export in `/tmp/` or project-local JSON/MD files

If they exist, extend or curate them instead of starting from zero.

### 2. Distinguish “approximate paper target” from “exact systematic review count”

If the user says “120 paper 左右” or similar, interpret this as a curated corpus target, not a PRISMA-grade final inclusion count.

Recommended wording in the deliverable:
- “curated literature pool”
- “approximately / around N papers”
- “topic-relevant filtered corpus”

Do NOT imply that the result is a formal systematic-review inclusion set unless you actually performed:
- multi-database search,
- explicit inclusion/exclusion criteria,
- DOI verification,
- and PRISMA-style accounting.

### 3. Build a high-relevance curated pool

When the repo already has a larger raw pool, do a second-pass curation:
- deduplicate by normalized title
- remove obvious off-topic records
- explicitly force-retain landmark papers the topic clearly requires
- prefer relevance over hitting an exact numeric target

If the result lands slightly below the requested number (e.g. 117 instead of ~120), that is acceptable if relevance improved.

### 4. Force-retain landmark papers

For topic reviews, maintain an explicit list of must-keep landmark papers. For hallucination/de novo protein design, examples include:
- `De novo protein design by deep network hallucination`
- `De novo design of protein structure and function with RFdiffusion`
- `Illuminating protein space with a programmable generative model`
- `Hallucinating symmetric protein assemblies`
- `Graph Denoising Diffusion for Inverse Protein Folding`
- `DPLM-2: A Multimodal Diffusion Protein Language Model`
- `Multistate and functional protein design using RoseTTAFold sequence space diffusion`
- `One-shot design of functional protein binders with BindCraft`

Add a “Landmark papers explicitly retained” section in the curated-pool markdown when useful.

### 5. Review writing style for this user

For this user, the best review artifact is:
- Chinese, concise-but-scholarly markdown
- academic paragraphs rather than note fragments
- structured by methodological evolution, not paper-by-paper listing
- explicit about what is core method, what is application, and what is evaluation

A good section logic is:
1. early hallucination / oracle-guided optimization
2. diffusion / flow-matching convergence
3. major method families (RFdiffusion, Chroma, DPLM, inverse folding coupling)
4. applications (binder, enzyme, multistate/dynamic, symmetric assemblies)
5. evaluation and experimental validation limits
6. future directions

### 6. Review template writing style for this user

The user asked for “template for review a paper” in this topic. Prefer a markdown template that:
- is written for direct human use
- prompts paragraph-style responses
- explicitly checks method novelty, baseline fairness, oracle exploitation risk, evaluation metrics, experimental validation strength, and reproducibility

For this user, a Chinese version is often more reusable than only exporting a Python prompt string.

### 7. Important caveat to state in final handoff

If the corpus is curated from Semantic Scholar-style exports plus repo-local filtering, explicitly tell the user:
- this is a high-relevance curated literature pool,
- suitable for review drafting / proposal background / domain mapping,
- but not automatically equivalent to a publication-grade systematic review dataset.

If they need a systematic review, next steps should include:
- inclusion/exclusion criteria,
- DOI verification,
- cross-database expansion,
- PRISMA flow,
- and table-based evidence extraction.

## Naming patterns that worked well

Use readable file names such as:
- `de_novo_protein_hallucination_review_template_zh.md`
- `de_novo_protein_design_hallucination_academic_review_cn.md`
- `de_novo_protein_design_hallucination_literature_pool_120.md`
- `de_novo_protein_design_hallucination_literature_pool_120.json`

The exact paper count in the filename can stay tied to the user request even if the final curated count is slightly below it, as long as the document body states the actual total.

## Pitfalls

- Do not present a rough target like “~120 papers” as an exact systematic-review inclusion count.
- Do not write only a short prose review when the user also requested a reusable review template.
- Do not overfit to raw citation counts; landmark-method coverage matters more.
- Do not preserve obviously off-topic records merely to hit a numeric target.
- Do not let the review collapse into a flat paper list; keep method evolution and evaluation logic visible.
