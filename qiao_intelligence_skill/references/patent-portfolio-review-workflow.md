# Patent portfolio review workflow for local Chinese CSV datasets

Use when the user asks to "review" or assess an inventor / PI / institution patent portfolio from a local CSV in the project workspace (for example `江南大学_刘立明_相关专利数据.csv`).

## Trigger pattern
- User asks for a review of a named inventor's patents without specifying web search.
- Workspace already contains a patent CSV exported from a local patent dataset.
- Best default is a repository-grounded review, not an internet summary.

## Preferred workflow
1. Locate the inventor-specific CSV first; prefer a direct inventor file over broad mixed patent tables.
2. Treat `申请号` as the primary deduplication key because the same invention often appears twice as `发明申请` and `发明授权`.
3. Report both:
   - raw record count
   - deduplicated unique application count
4. Summarize the portfolio on four axes:
   - time span / phase evolution
   - dominant product families or technology themes
   - engineering mode (process optimization, metabolic engineering, enzyme engineering, pathway design, etc.)
   - industrialization signal (g/L, yield, conversion, scale-up, feedstock flexibility, tolerance, downstream purification)
5. Pull line-grounded examples from the CSV for representative patents across early / middle / recent stages.
6. If useful, extract:
   - year histogram after deduplication
   - major co-inventors
   - co-applicants / company collaborations
   - most-cited patents
7. Final review should read as a technical portfolio assessment, not a flat patent list.

## Output shape
- Quick take
- Core stats
- Main technical trajectory
- Representative patents worth attention
- Strengths
- Boundary conditions / weaknesses
- Bottom-line judgment

## Durable heuristics
- In this dataset style, duplicated application + grant entries are normal; never treat raw row count as patent count.
- For this user, emphasize technology evolution and industrial biotechnology capability, not legal claim construction.
- Cite exact file path and line-grounded evidence when possible.
- Recent review value usually comes from comparing the early fermentation-optimization phase with the later platform-strain / enzyme-engineering / synthetic-biology phase.

## Example signals from the Liuliming session
- Dataset had 296 rows but only 191 unique application numbers after deduplication by `申请号`.
- Useful representative evidence included early pyruvate / α-ketoglutarate fermentation patents, mid-stage metabolic-engineering platform methods, and recent E. coli platform patents for lysine, succinate, diamines, and CO2-to-pyruvate.
- Co-applicant extraction helped reveal translation from university-only filings to university-enterprise collaborations.
