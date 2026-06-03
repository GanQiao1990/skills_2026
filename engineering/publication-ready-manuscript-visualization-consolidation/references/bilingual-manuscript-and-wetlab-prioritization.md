# Bilingual manuscript + wet-lab prioritization pattern

Use this reference when a repository-grounded publication package must be expanded from a single-language manuscript into bilingual deliverables and the user also wants a practical decision on which candidate should enter wet-lab first.

## Durable pattern

### 1. Keep one evidence boundary across languages
- Both language versions must say the same source-path truth.
- If the literal requested path token is malformed or unreadable, both versions must state that explicitly.
- The translated manuscript must not introduce stronger claims than the source manuscript.

### 2. Treat Markdown as authoritative in both languages
Recommended package shape:
- `report_name.md` — authoritative English source
- `report_name.docx` — derived English DOCX
- `report_name_zh.md` — authoritative Chinese source
- `report_name_zh.docx` — derived Chinese DOCX

### 3. Share one figure family
- Reuse the same package-local figure set in both languages.
- Keep figure filenames stable and package-local under `figures/`.
- Mirror outputs under `publication_assets/` only as a convenience, not as the manuscript-facing path.

### 4. Add a wet-lab recommendation only as prioritization under uncertainty
Safe framing:
- Primary choice = strongest aggregate support
- Backup = strongest peak mechanistic signal or complementary profile
- Optional third choice = orthogonal comparator from another batch or profile

Unsafe framing to avoid:
- "best enzyme"
- "most active enzyme"
- "validated winner"
- any wording implying biochemical superiority without wet-lab evidence

### 5. Evidence types that support first-pass wet-lab prioritization
Useful computational signals:
- highest mean relevance or aggregate rank
- highest total relevance across subsections
- balanced support across EC / catalytic activity / cofactor / function / GO-like subsections
- strongest maximum mechanistic signal for the backup candidate
- inclusion of one orthogonal comparator to reduce overfitting to a single ranking logic

### 6. Cost/time minimizing recommendation template
- Tier 1: one primary construct to minimize cloning/expression/screening burden
- Tier 2: one immediate backup candidate if two constructs are affordable
- Tier 3: one orthogonal comparator if the user wants cross-batch or cross-profile contrast

## Package-doc updates to remember
When adding bilingual deliverables, also update:
- `README_REPORT_WORKFLOW.md`
- `INDEX.md`
- `VALIDATION_NOTE.md`
- `EVIDENCE_MAP.md`

## Verification checklist
- both Markdown sources exist
- both DOCX outputs regenerate cleanly
- both language versions contain the same figure count
- both language versions retain the same path limitation statement
- the recommendation subsection includes candidate IDs and rationale
- the rationale is explicitly computational and uncertainty-aware
