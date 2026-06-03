# Annotated Review Corpus Workflow for AI-Scientist-v2

Use this workflow when the user does NOT just want a narrative review, but explicitly wants:
- a larger curated corpus target (for example ~200 papers),
- per-paper algorithm labeling, and
- publication-oriented support artifacts such as CSV/JSON tables that can be turned into manuscript tables or supplementary materials.

This commonly appears in requests like:
- "200 paper 左右"
- "标记每篇文章的算法使用以及特点"
- "add more detail 以便我发表文章"

## Output package

For this class of request, produce a coordinated set of files:

1. Narrative review markdown
   - `ai_scientist/ideas/<topic>_academic_review_publishable[_cn].md`
   - academic-paragraph style
   - method evolution + applications + evaluation + gaps

2. Human-facing review template markdown
   - `ai_scientist/review_templates/<topic>_review_template_publishable[_zh].md`
   - paragraph-oriented prompts for novelty, baseline fairness, validation strength, reproducibility, and publication readiness

3. Annotated literature pool in THREE formats
   - `..._literature_pool_200_annotated.md`
   - `..._literature_pool_200_annotated.json`
   - `..._literature_pool_200_annotated.csv`

4. Method taxonomy summary
   - `..._method_taxonomy_200.md`
   - summarize algorithm families, counts, representative papers, common tasks, and recurring strengths/limits

5. Optional writing guide
   - `..._writing_guide_for_publication[_cn].md`
   - tells future agents or the user how to turn the corpus into a publishable review

## Per-paper annotation schema

When the user asks to mark each paper's algorithm and特点, prefer a stable structured schema instead of ad hoc notes.

Minimum columns:
- `title`
- `year`
- `venue`
- `citationCount`
- `category`
- `algorithm_family`
- `algorithm_used`
- `task_focus`
- `feature_notes`
- `validation_level`
- `relevance_note`

Recommended meanings:
- `algorithm_family`: class-level grouping such as RFdiffusion, Chroma, oracle-guided hallucination, flow matching, discrete diffusion, inverse folding, protein language model, reward-guided generation
- `algorithm_used`: best-effort exact named method or pipeline from title/category
- `task_focus`: binder, enzyme, multistate/dynamic, symmetric assembly, benchmark, sequence design, general de novo design
- `feature_notes`: one concise semicolon-separated summary of what is distinctive
- `validation_level`: one of `Benchmark / no new wet-lab`, `Primarily computational`, `Mostly computational / preprint-stage`, `Mixed computational + some experimental validation`
- `relevance_note`: `landmark/core` vs `supporting/application/benchmark`

## Important framing

A 200-paper annotated pool is usually a WRITING-GRADE curated corpus, not a PRISMA-grade systematic review inclusion set.

State this explicitly if the pool was built from:
- repo-local raw exports,
- title/category heuristics,
- citation prioritization,
- and manual/heuristic filtering.

Use wording like:
- "annotated curated corpus"
- "publication-oriented writing pool"
- "high-relevance filtered literature set"

Do NOT imply formal systematic-review inclusion unless you also performed:
- explicit inclusion/exclusion criteria,
- DOI/metadata verification,
- multi-database reconciliation,
- and PRISMA-style accounting.

## Practical ranking rule

When scaling from ~120 to ~200 papers, use a broader relevance filter instead of forcing an exact count from a narrow landmark list.

Good ordering principles:
1. force-retain landmark/core papers
2. retain major method families even when citations are low (recent preprints matter)
3. preserve application branches (binder, enzyme, multistate, symmetric assembly)
4. keep benchmark/designability papers that help interpret success claims
5. only then use citation count as a secondary ranking signal

## Pitfalls

- Do not collapse all papers into `Related generative protein design` if the title clearly identifies RFdiffusion, Chroma, DPLM, AlphaFold-guided hallucination, flow matching, or inverse folding.
- Do not present heuristic `feature_notes` as if they were full-text verified claims.
- Do not over-prune recent low-citation papers when the user wants a publishable review draft; recent preprints often matter for framing future directions.
- Do not stop at a narrative review when the user explicitly asked for per-paper algorithm labeling.
- Do not rely on markdown alone; write CSV too, because that is the easiest format for downstream manuscript tables.

## Best handoff language

When returning the deliverable, explicitly tell the user:
- where the narrative review is,
- where the annotated CSV is,
- that the CSV is the best starting point for supplementary tables,
- and that a final submission-grade version should still get DOI/metadata/full-text cleanup.
