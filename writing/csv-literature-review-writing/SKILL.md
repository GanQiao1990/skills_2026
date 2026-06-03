---
name: csv-literature-review-writing
description: "Write publication-quality literature reviews from CSV/structured literature pools. Covers: comprehensive citation coverage (ALL papers cited, not a subset), expert thinking roadmap organization, category-based reference tables, claim-evidence matching, and Chinese academic markdown conventions."
triggers:
  - "literature review from CSV or structured data"
  - "综述 from literature database"
  - "academic review with reference pool"
  - "de novo protein design hallucination review"
---

# CSV-Driven Literature Review Writing

Write publication-quality narrative reviews grounded in a structured literature pool (CSV with title, abstract, DOI, year, etc.).

## Critical Rule: COMPREHENSIVE COVERAGE

**When given a CSV of N papers, ALL N papers must appear in the final review.** Never cherry-pick a subset. The user will notice and flag it immediately.

Steps:
1. Parse the CSV and assign each paper a unique number [1]–[N]
2. Categorize every paper (non-exclusive categories allowed)
3. Every paper must be cited at least once in the body text
4. The reference table at the end must list ALL papers, grouped by category

## Workflow

### Step 1: Data Audit
- Count total papers, papers with/without abstracts, DOI availability
- Year distribution (histogram)
- Topic clustering by title+abstract keywords (non-exclusive)
- Identify high-impact journals (Nature/Science/Cell series)
- Report these stats in the opening section
- **Run a dual coverage audit before and after writing**:
  - bibliography coverage: does the reference table list all N papers?
  - body coverage: does the narrative body cite all N papers at least once?
- Do not treat a complete reference table as proof of full literature use. A draft can list all 300 papers yet still only integrate a subset into the body argument.
- Final verification target: `unique ref numbers in body == CSV row count` and `unique ref numbers in reference table == CSV row count`.
- See `references/body-vs-reference-coverage.md` for the common failure mode and a compact audit recipe.

### Step 2: Category Assignment
- Assign each paper a PRIMARY category (first match from priority list)
- Papers can belong to multiple categories (non-exclusive)
- Use a priority ordering so the reference table groups meaningfully
- Build a citation map: category → list of [ref_numbers]

### Step 3: Expert Thinking Roadmap
Organize the body around 5 progressive questions, NOT chronological model listing:
1. Problem restatement: what is the actual goal?
2. Method lineage: which method solves which bottleneck?
3. Application divergence: different tasks need different evidence
4. Evidence calibration: what can proxy metrics support?
5. Future judgment: what determines real value?

### Step 4: Body Writing
- Each section MUST cite ALL papers in its category using [N] notation
- Use cite_list() and cite_range() functions for clean inline citations
- Include detailed work tables for major application sections (binder, enzyme, etc.)
- Tables should show: work name, target, key metric, reference number

### Step 5: Claim-Evidence Matching Framework
Include a table mapping design tasks to minimum/strong evidence requirements:
| Task | Minimum evidence | Strong evidence |
|---|---|---|
| Fold generation | self-consistency + novelty | high-res structure |
| Binder design | transparent funnel + binding | structure + specificity + cell function |
| Enzyme design | catalytic assay + kinetics | substrate specificity + mutation + mechanism |
| Dynamic design | switching readout | kinetics + structural dynamics |

### Step 5.5: Journal-Specific Reframing for Computational / Bioinformatics Review Venues
- When targeting venues like Briefings in Bioinformatics, do NOT leave the review as a protein-design narrative only.
- Reframe the manuscript around method comparability:
  - input representation (sequence / backbone / motif / interface / text)
  - generation mechanism (hallucination / inversion / diffusion / flow / language model)
  - sequence realization layer (inverse folding / redesign / discrete generation)
  - triage and robustness checks (cross-model agreement, diversity, developability)
  - benchmark / proxy metric / evidence ladder
- Emphasize what each metric can and cannot support; BIB-style readers care about evaluation discipline, not just success stories.
- Make the paper answer a methods question such as: which methods are comparable, under what protocol assumptions, and with what evidence depth?
- Add at least one comparison table and one benchmark/evidence table before calling the draft journal-ready.
- See `references/briefings-in-bioinformatics-review-framing.md` for a compact checklist.

### Step 6: Reference Table
- Group by category with section headers
- Each row: [N] | Title | Year | DOI link
- Escape pipe characters in titles
- Papers without DOI: use Semantic Scholar weblinker

## Chinese Academic Markdown Conventions

- Title: `# 中文标题：英文副标题`
- Opening blockquote: literature basis + key stats
- Keywords section after abstract
- Mermaid flowchart as graphical abstract
- Mixed Chinese body + English technical terms (no translation of established terms)
- Section numbering: `## 1.`, `## 2.`, etc.
- Tables with `|:---|` left-aligned, `|:---:|` center-aligned for numbers
- Conclusion section summarizes the three evidence chains

## Case Study
See `references/protein-design-case-study.md` for a worked example: 300-paper de novo protein design review with 19 categories, full citation coverage, and the pitfall of initial 50/300 subset citation.
See `references/body-vs-reference-coverage.md` for the specific audit pattern where the bibliography is complete but the narrative body still omits part of the corpus.
See `references/briefings-in-bioinformatics-review-framing.md` for how to reframe a protein-design review toward method comparison, benchmark discipline, and evidence mapping for BIB-style venues.

## Pitfalls

1. **Subset citation**: Never cite only 50/300 papers. The user WILL notice.
2. **Reference-table illusion**: Listing all papers in the bibliography is not enough. The body may still omit some references; audit body coverage separately.
3. **Flat reference list**: Group by category, not just numbered 1-N.
4. **Missing abstracts**: Papers without abstracts still get cited — use title keywords.
5. **Exclusive categories**: Papers can and should appear in multiple categories.
6. **Chronological body**: Don't organize body by year; use the 5-question roadmap.
7. **Weak evidence claims**: pLDDT ≠ function. Always use claim-evidence matching.
8. **execute_code import**: Use `from hermes_tools import terminal, read_file, write_file` — bare `terminal()` without import fails.
9. **Expert-roadmap expectation**: For this user, a publishable Chinese review should read like an expert argument, not a model catalog. Reframe around problem definition, method evolution, application layers, evidence calibration, and future judgment.

## Template: cite_list helper

```python
def cite_list(nums):
    """Format ref numbers as inline citation"""
    return "[" + "][".join(str(n) for n in sorted(nums)) + "]"

def cite_range(nums, max_show=8):
    """Format with first N shown + total count"""
    s = sorted(nums)
    if len(s) <= max_show:
        return cite_list(s)
    return cite_list(s[:max_show]) + f" 等共 {len(s)} 篇"
```
