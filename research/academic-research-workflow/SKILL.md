---
name: academic-research-workflow
description: General academic workflow router for literature search, paper drafting, citation handling, peer review, rebuttals, thesis writing, and talk/poster preparation. Use this skill first when a user asks for scholarly or research help and then hand off to the most relevant specialist skills.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
metadata:
  skill-author: Hermes Agent
  tags: [academic, research, literature-review, paper-writing, citations, peer-review, thesis, slides, poster]
  category: research
  related_skills: [literature-review, scientific-writing, citation-management, venue-templates, arxiv, peer-review, scientific-slides, latex-posters]
---

# Academic Research Workflow

## Overview

Use this skill as the first-stop router for academic and scholarly requests. It turns vague requests like “帮我做文献综述”, “润色论文”, “写 rebuttal”, “准备组会汇报”, or “整理参考文献” into a concrete workflow and routes execution to the best existing specialist skills.

This skill is intentionally broad. It is not a replacement for domain-specific scientific skills; instead, it provides the decision logic, minimum quality bar, and recommended sequence for common academic tasks.

## When to Use This Skill

Use this skill when the user asks for any of the following:
- literature search, state-of-the-art scan, or reading list generation
- systematic/scoping/narrative review planning
- paper outlining, drafting, revising, shortening, or polishing
- abstract/title generation or cover letter writing
- peer review, reviewer response, rebuttal, or revision planning
- thesis/dissertation chapter writing and structure planning
- slide deck, poster, or lab meeting presentation preparation
- citation cleanup, bibliography normalization, DOI checking
- venue selection or formatting for journal/conference submission
- transforming notes, PDFs, or experiment logs into academic prose

## Core Rule

Always do three things before producing a final academic deliverable:
1. Clarify the deliverable type internally from context: review, manuscript, rebuttal, thesis text, slides, poster, notes, or reading list.
2. Identify the target audience or venue if it is available; if not, default to a discipline-appropriate scholarly style.
3. Separate evidence gathering from writing. First collect facts/sources/constraints, then draft.

## Routing Guide

### 1. Literature discovery and synthesis
Primary skills:
- literature-review
- arxiv
- openalex-database / pubmed-database / related database skills when relevant

Use for:
- “给我找这个方向的论文”
- “做一个综述框架”
- “总结近三年的进展”

Minimum workflow:
1. Define topic, scope, and time window.
2. Identify 3-6 search terms plus synonyms.
3. Search at least two sources for a quick review; three or more for a rigorous review.
4. Cluster papers by theme, method, dataset, or finding.
5. Output a structured synthesis, not a flat paper list.

For ongoing project background notes:
1. Save the result as a standalone markdown note in the active project directory when the user asks for a "summary", "background", or "调研总结" rather than only replying inline.
2. Keep the writing mechanism-centered: explain trigger → signal generation → downstream regulatory consequences → phenotype/application, instead of drifting into generic importance claims.
3. Distinguish clearly between established literature-backed mechanisms and project-specific hypotheses. If a direct link (for example between a regulator and ppGpp) is not well established, say it is a plausible coupling or a hypothesis to test, not a proven direct pathway.
4. When the topic is a stress signaling molecule, emphasize dynamics (induction timing, peak, duration, recovery) rather than only reporting endpoint abundance, because the trajectory is often more informative for mechanism and engineering design.
5. For Chinese-language users, default to concise, authoritative Chinese prose suitable for later insertion into a proposal or manuscript unless they ask for another style.
6. When the user asks for several scholarly deliverables at once (for example: a compressed grant paragraph, one or more focused literature scans, and manuscript insertion), produce a synchronized package: (a) a reusable short paragraph, (b) focused markdown notes for each subquestion, and (c) direct integration of the compressed version into the active manuscript/background file.
7. If direct literature for a narrow subcase is sparse (for example a specific amino-acid stressor), synthesize from the broader mechanism literature plus the closest direct studies, and explicitly label the remaining gap as indirect or still-to-be-validated evidence instead of overstating certainty.
8. If the user references a local scraper, notebook, or utility path as the desired style for a literature workflow (for example, 'PubMed API like /path/to/tool'), inspect that implementation first and align with its operational shape — query composition, export format, batching, and outputs — rather than defaulting to an ad hoc one-off search. When the pattern is reusable, create or update a project-local helper script so future literature pulls follow the same structure.
9. When the user is shaping a proposal rather than asking for a broad review, compress the literature synthesis into a small number of explicit scientific questions first. If the user says there are only two core questions, preserve that constraint and state the two questions plainly before expanding background.
10. When the user names exemplar labs or investigators (for example, Liming Liu and Sang Yup Lee), do not stop at paper listing. Extract each group's recurring strategy pattern, explain what problem layer each strategy addresses, and tie those strategies back to the user's project question.
11. If the user already has a specific engineered mechanism or de novo design setting, keep that mechanism as the execution layer in the writeup. Use the literature to sharpen problem definition, prioritization, and evidence boundaries; do not let the literature survey replace the user's chosen execution logic with a generic field summary.
12. Treat boundary-definition questions (for example, whether an amino salt should count as nitrogen assimilation) as explicit subquestions. Answer them with operational criteria based on metabolic role and evidence of net flux into core metabolism, rather than a blanket yes/no label.
13. When reviewing the evolution of multiple proposal drafts, summarize the progression along four axes: core problem definition, chosen control axis or mechanism, execution-layer design, and evidence base. This produces a more useful evolution narrative than a flat version-by-version diff.
14. When the user says the story should focus on one core module, limiting segment, or short contiguous reaction block rather than assembling every enzyme, keep the proposal framed around a dominant bottleneck module. Support the choice with flux-control concentration, substrate-channeling, and burden/stoichiometry arguments; do not drift back into whole-pathway assembly language.
15. When the user removes an execution layer or mechanism from scope, do not keep narrating the removal in the final draft with phrases like “we no longer retain X” unless they explicitly ask for contrastive rationale. Rewrite directly around the retained application forms so the text reads as a clean positive proposal, not a record of deleted options.
16. When the user asks to optimize an existing review draft into something closer to a publishable review article, do not limit yourself to sentence-level polishing. Rebuild the document around an explicit expert roadmap such as: problem redefinition -> method genealogy -> application stratification -> evaluation/evidence framework -> field-level judgment -> future roadmap.
17. When the user provides a local literature corpus file (for example a CSV with titles, abstracts, DOIs, and links), inspect its schema first and use it as structural evidence. Pull rough distributional signals from the corpus—such as method-family prevalence, application hotspots, and benchmark/review density—to support the rewritten narrative, while clearly distinguishing corpus-level synthesis from per-paper full-text verification.
18. For major review rewrites based on an existing markdown draft plus a local corpus, default to saving a new optimized markdown in the current working directory or requested output directory rather than overwriting the original source draft, unless the user explicitly asks for in-place replacement. This preserves provenance while giving the user a submission-grade candidate artifact.

### 2. Manuscript drafting and polishing
Primary skills:
- scientific-writing
- venue-templates
- research-paper-writing (especially for ML/AI papers)

Use for:
- abstract/introduction/methods/results/discussion drafting
- shortening to word limits
- converting bullets into academic prose
- tone normalization for journals/conferences

Minimum workflow:
1. Determine section and target venue if known.
2. Build section outline with claims, evidence, and citations.
3. Draft in full paragraphs.
4. Run one pass for logic and one pass for style.
5. Check that claims are supported and limitations are stated.

### 3. Citation and reference management
Primary skills:
- citation-management
- literature-review

Use for:
- DOI completion
- bibliography normalization
- switching citation styles
- finding missing metadata

Minimum workflow:
1. Parse the current reference list.
2. Detect duplicates, incomplete entries, and style inconsistencies.
3. Fill missing DOI/journal/year/page data when possible.
4. Reformat the entire list in one consistent style.

### 4. Peer review, rebuttal, and revision
Primary skills:
- peer-review
- scientific-writing
- venue-templates

Use for:
- reviewer response letters
- decision letter analysis
- revision plans
- internal mock review before submission

Minimum workflow:
1. Extract every reviewer concern as a discrete item.
2. Classify into evidence, writing clarity, methodology, statistics, novelty, or formatting.
3. Draft point-by-point responses with one action per point.
4. Ensure tone is respectful, specific, and non-defensive.

### 5. Thesis, dissertation, and long-form academic writing
Primary skills:
- scientific-writing
- citation-management
- venue-templates
- powerpoint or scientific-slides for defense materials

Use for:
- thesis chapter structure
- related-work chapters
- chapter-to-paper conversion
- defense prep

Minimum workflow:
1. Create chapter hierarchy first.
2. Define the contribution of each chapter in one sentence.
3. Standardize terminology, notation, and citation style across chapters.
4. Keep a running list of unresolved citation and figure tasks.

### 6. Talks, posters, and academic presentations
Primary skills:
- scientific-slides
- latex-posters or pptx-posters
- powerpoint

Use for:
- lab meeting slides
- conference talks
- poster outlines
- defense presentations

Minimum workflow:
1. Identify audience: advisor group, specialist conference, or broad interdisciplinary audience.
2. Reduce the story to problem → approach → evidence → takeaway.
3. Put one claim per slide or panel.
4. Prefer figures over dense text.

## Default Deliverable Templates

### Quick literature scan
Return:
- topic scope
- 5-15 key papers
- 3-5 thematic clusters
- current consensus
- open problems
- suggested next search terms

### Paper section drafting
Return:
- brief section objective
- concise outline
- polished prose draft
- list of citation placeholders or evidence gaps

### Rebuttal / reviewer response
Return:
- summary of review outcome
- prioritized action plan
- point-by-point response draft
- items needing new experiments or analyses

### Presentation prep
Return:
- storyline
- slide-by-slide outline
- suggested figures/tables
- likely audience questions

## Quality Bar

Before finalizing any academic output, verify:
- factual claims are traceable to provided material or retrieved sources
- terminology is consistent within the document
- the tone matches academic norms for the target venue
- citations are present where strong claims are made
- the output is structured for reader utility, not just completeness

## Common Pitfalls

Avoid these failure modes:
- listing papers without synthesis
- writing fluent but unsupported claims
- mixing venue styles in the same document
- overclaiming novelty or significance
- using generic summaries when the user asked for actionable academic output
- leaving TODO citations or placeholder references in a supposedly final draft

## Recommended Specialist Skill Map

If the task is mostly about:
- finding papers → literature-review, arxiv
- writing sections → scientific-writing
- ML/AI conference paper production → research-paper-writing
- citations and bibliography → citation-management
- review or rebuttal → peer-review
- venue adaptation → venue-templates
- talk/poster creation → scientific-slides, latex-posters, powerpoint

## Example Interpretations

User: “帮我写 related work”
- Gather topic, venue, and paper list.
- Route to literature-review for synthesis.
- Route to scientific-writing for paragraph drafting.

User: “把这篇文章润色成 Nature 风格”
- Keep claims/evidence unchanged.
- Route to venue-templates plus scientific-writing.

User: “审一下我的投稿”
- Route to peer-review.
- Return major concerns, minor concerns, and fix plan.

User: “给我做组会汇报”
- Route to scientific-slides.
- Produce talk arc, slide outline, and likely questions.

## Output Style

Unless the user requests otherwise, produce academic work in a practical format:
- concise framing sentence
- structured sections with informative headings
- clean prose rather than bloated filler
- explicit gaps or assumptions labeled clearly

## Summary

This skill expands academic coverage by adding one broad, reliable entry point for scholarly work. It reduces routing ambiguity, raises quality standards, and ensures that literature search, writing, citations, review, and presentation tasks follow a coherent academic workflow.