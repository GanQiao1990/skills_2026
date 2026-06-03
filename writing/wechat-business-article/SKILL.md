---
name: wechat-business-article
description: Generate professional, WeChat-compatible HTML articles for business introductions and technical tools.
---

# WeChat Business Introduction HTML Article

A skill for generating professional, WeChat-compatible HTML articles for business introductions, technical tools, or project launches. WeChat's internal browser has specific styling restrictions, requiring a specialized approach for layouts.

## Trigger Conditions
- User asks for a "公众号" (Public Account) article.
- User requests HTML format for a business introduction.
- User wants a paper, preprint, technical article, or research result rewritten as a 公众号 article for a broader audience.
- Target is the `/home/qiao/qiao_design/公众号` directory.

## Research-paper adaptation rule
When the source material is a scientific paper or PDF, do not jump straight into promotional copy. First extract the paper's evidence chain in a compact internal brief: problem -> starting limitation -> engineering or experimental strategy -> key validation results -> in vivo or real-world significance -> remaining caveats. Keep direct evidence separate from interpretation.

### Source-acquisition fallback for scientific papers
If the user gives a paper URL and the direct PDF is blocked, times out, or returns an anti-bot/interstitial response, do not stop at the dead link. Resolve the paper identity first (title, authors, year, DOI, PMCID/PMID if available), then fetch from a more stable full-text source.

Preferred fallback order:
1. DOI landing page or publisher page to confirm the canonical paper identity.
2. Europe PMC / PubMed Central mirrors for open papers, especially `?pdf=render` PDF links and `fullTextXML` when available.
3. Other official or archival full-text mirrors only after the paper identity is verified.

Workflow rule:
- Save the downloaded PDF if available, but also save a machine-readable text source when possible (for example Europe PMC `fullTextXML`).
- Treat the XML/full-text source as the main evidence extraction substrate when the PDF text layer is noisy.
- In the internal evidence brief, explicitly record when the original user-supplied URL was inaccessible and which verified fallback source was used instead.
- For headline numerical claims in the public article, prefer values you can trace directly to the abstract, tables, or full-text XML.

See `references/scientific-paper-source-fallbacks.md` for a compact fallback playbook.

### Local-file override and replacement rule
If the user provides a local PDF path, or says they replaced the file and want the article rewritten from that local file, treat the local PDF as the canonical source immediately.

Workflow rule:
- Do not continue using the previously resolved URL, DOI, title, or evidence brief just because they were identified earlier in the session.
- Re-extract the paper identity from the local file itself: metadata, page-1 title/authors, abstract, and body evidence.
- If the local file conflicts with the earlier source, explicitly discard the earlier paper identity and regenerate the evidence brief from scratch.
- Do not infer the paper identity from the filename alone. Reused filenames like `esm_protein.pdf` can point to a different paper after replacement.
- If the user gives a malformed or repeated path string but it clearly points to one existing local PDF, normalize it and proceed without forcing a clarification round.

For this failure mode, add a short note in the internal evidence brief that the article was rewritten from the user-supplied local PDF and that prior draft content based on another source was invalidated.

Correction protocol after a user says the paper/source was wrong:
- Treat the prior evidence brief, title, and article draft as contaminated.
- Re-read the local PDF from scratch before reusing any prior claims.
- If the user pasted a malformed or repeated absolute path string, normalize it to the one existing local PDF and proceed.
- In the rewritten article, avoid carrying over old-paper framing just because the filename stayed the same.

If the user proposes a Chinese title or framing angle (for example asking "这个主题可以吗？"), handle it in two steps:
1. Briefly judge whether the title/theme is evidence-aligned.
2. If it is broadly good, keep the user’s framing, fix obvious typos silently when safe (for example "白质" -> "蛋白质"), and rewrite the article around that angle instead of reverting to a generic summary.
3. If the framing hinges on a technical metric term, verify the semantics before endorsing the title. Do not let a benchmark metric get promoted into a stronger scientific claim than the paper supports.

Metric-to-claim rule for scientific 公众号 writing:
- Distinguish benchmark metrics from physical or experimental validation.
- Examples of benchmark / model-evaluation metrics: DockQ, LDDT, ipTM, pass rate, perplexity, AUC.
- Examples of stronger physical / experimental evidence: cryo-EM or X-ray structures, binding assays such as BLI/SPR, competition assays, cell-based functional assays, animal validation.
- Do not write or imply that a metric like DockQ "is a physical model" or that a benchmark pass rate alone constitutes physical validation.
- When the user wants a title around "可验证" / "物理现实" / "实验验证", anchor the wording to the actual evidence chain in the paper: structure validation, affinity measurements, epitope validation, selectivity, functional readout.
- If the paper’s real contribution is concentrated in a specific subsystem (for example ESMFold2 rather than the whole umbrella narrative), prefer titles that foreground that subsystem instead of a vague model-family label.

See `references/local-pdf-replacement-and-correction.md` for the concrete correction pattern and `references/metrics-vs-experimental-validation.md` for a compact framing guide.

### First-principles evidence-chain mode
If the user asks for a deeper or more rigorous explanation, especially phrases like "从第一性原理", "为什么这么做", "什么目的", "为了完成这个目的他们做了什么", or asks why a screen included a specific set of proteins/constructs/conditions, upgrade the article from a result-summary into a causal narrative.

In this mode, the article should explicitly answer, in order:
1. What is the root problem or engineering contradiction?
2. Why is the starting system insufficient?
3. What exact hypothesis motivated the first screen or comparison set?
4. Why were specific comparison classes included (for example, related homologs added not as controls-for-show but to reveal structural/functional features)?
5. Why were specific assay conditions chosen (for example, a longer guide used intentionally as a high-specificity filter rather than a convenience default)?
6. What did each experimental stage prove, and what next design decision did that proof justify?
7. How do the final application experiments close the proof chain rather than merely decorate the paper with an extra use case?

For scientific PR writing, prefer a readable expert narrative, but make each major design choice answer the sequence: objective -> action -> evidence -> implication -> next step. This is especially important for screening-heavy and engineering-heavy papers.

When a user asks whether a proposed Chinese title/theme is appropriate, evaluate it against the paper's strongest evidence chain instead of treating the title as a cosmetic choice. If the title overstates or blurs the evidence, pivot to the nearest evidence-aligned framing. A common pattern is to shift from a broad claim (for example, a vague 'world model' framing) to the actual evidence-bearing subsystem or method (for example, a specific structure model such as ESMFold2) when that subsystem is what the paper truly validates.

For papers that mix benchmark metrics with experimental validation, explicitly separate the two in the article:
- Metrics such as DockQ, LDDT, AUROC, or pass rate are evaluation measures, not physical models and not experiments.
- Structural or biochemical evidence such as cryo-EM, X-ray structures, BLI/SPR affinities, competition assays, cellular readouts, or in vivo data are the stronger 'reality-check' layer.
- If the user asks a question like 'X = 物理模型吗？', answer it directly and then re-anchor the article around the real validation chain.

When the user asks to 'write in the core algorithm' or connect the paper to their own downstream work, do not stop at a result-summary. Add an algorithm-to-practice section that extracts:
- the factorization or objective the paper uses,
- the role of each major module,
- the search/optimization loop,
- and 3-5 concrete design takeaways for the user's likely workflow.
This is especially valuable in protein design, model-based optimization, and screening pipelines.

See `references/first-principles-paper-adaptation.md` for a reusable breakdown pattern.
See `references/metrics-vs-validation-and-algorithm-transfer.md` for a compact playbook on separating benchmark metrics from physical validation and translating methods into design guidance.

Default output format rule:
- If the user explicitly asks for HTML, produce WeChat-compatible HTML.
- If the user asks for a "公众号" article but does not explicitly ask for HTML, default to polished Markdown saved in the target directory. This is usually easier for review and later editing.
- For science or biotech topics, prefer a PR/expert-narrative tone: strong framing and readability, but no hype that outruns the paper's actual evidence.

## Step-by-Step Workflow

1.  **Context Reconnaissance**:
    - If the topic is a tool/project (e.g., "hyperframes"), check for local binaries (`which <tool>`) or project READMEs.
    - Run `<tool> --help` and `<tool> docs` to understand the value proposition, key features, and "Quick Start" steps.

2.  **HTML Architecture**:
    - **Container**: Use a `max-width: 600px` div with `margin: 0 auto`.
    - **Styling**: All CSS **must** be inlined. Avoid `<style>` blocks or external CSS.
    - **Layout**: Use `<table>` for side-by-side content or multi-column grids to ensure compatibility across WeChat versions.
    - **Typography**: Use `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`.

3.  **Content Structure**:
    - **Hero Section**: Catchy title, gradient background (`linear-gradient`), and high-level stats/badges.
    - **Value Proposition**: Answer "Why do I need this?" with 2-3 specific business benefits.
    - **Feature Grid**: 2x2 or 3x1 grid showing capabilities with icons/emojis.
    - **Instructional Section**: "3-Step Start" using terminal-style code blocks (background `#282c34`).
    - **Use Cases**: Real-world scenarios (e.g., "Automated Marketing", "Data Visualization").
    - **CTA (Call to Action)**: A prominent button or link at the bottom.

4.  **WeChat Specific Pitfalls**:
    - No JavaScript allowed.
    - No external fonts.
    - `float` is unreliable; use `display: inline-block` or `table`.
    - Images should have `max-width: 100%`.
    - For scientific papers, do not overstate claims. Preserve caveats such as TAM restrictions, off-target assessment limits, delivery scope, or unresolved immunogenicity when the source paper includes them.
    - If you produce both an internal evidence brief and a public-facing article, save them as separate files so the user can reuse the evidence chain for later academic or investor materials.
- If the source paper was recovered via a verified mirror because the original URL failed, note the fallback pattern in `references/scientific-paper-source-fallbacks.md`.

## Verification
- Open the `.html` file in a browser to check layout when HTML was requested.
- For markdown-first workflows, verify the saved article reads cleanly in raw Markdown and that headings/blockquote/code/table formatting are not overused.
- Ensure all command-line examples match the actual tool documentation.
- For paper-based articles, verify that headline numerical claims in the article are directly supported by the source text.
