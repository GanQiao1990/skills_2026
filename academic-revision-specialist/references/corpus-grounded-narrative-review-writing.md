# Corpus-grounded narrative review writing

Use this reference when the user asks for a review article based primarily on a scraped CSV, metadata export, or title/abstract corpus instead of a manually screened full-text bibliography.

## Best-fit use case
- The source is a CSV/JSON with title, abstract, date, DOI, and link fields.
- The deliverable should read like an academic review or perspective.
- The user asks for journal-like prose (for example NBT / Nature Biotechnology style) and prefers paragraph-driven writing.

## Core framing rule
Do not present the result as a systematic review unless the workflow actually included database protocol, screening criteria, deduplication, full-text review, and formal study-selection reporting.

Preferred framing:
- "narrative review grounded in a curated corpus"
- "corpus-based review"
- "metadata-grounded landscape review"

Avoid:
- "systematic review"
- PRISMA language
- claims of bibliographic completeness

## Recommended opening moves
1. State the corpus basis directly in the abstract or scope section:
   - record count
   - date span or year distribution
   - source file type/path if relevant
2. Extract 3-5 dominant topic clusters from titles/abstracts when possible.
3. Use those clusters to organize the story around:
   - method evolution
   - bottlenecks
   - application classes
   - evidence standards
   - outlook

## Preferred section logic for NBT-style prose
1. Abstract — field transition + corpus basis + main thesis
2. Introduction — why the field changed, not just what changed
3. Conceptual origin / problem redefinition
4. Method genealogy by bottleneck solved
5. Application-layer comparison
6. Evidence calibration / limitations of current claims
7. Outlook toward platform/system competition
8. Conclusion

## Evidence-bounding rule
When the corpus comes from titles/abstracts only, the review can directly support:
- publication density trends
- visible topic concentration
- representative landmark-paper positioning
- broad method/application transitions

The review cannot directly support without further checking:
- exact performance comparisons across papers
- deep mechanistic comparisons absent from abstracts
- exhaustive priority claims
- journal-submission-ready reference completeness

## Source-path substitution rule
If the user gives a file path that is missing, but an identically named dataset is found in the active project tree and clearly matches the requested artifact, it is acceptable to use it.

But:
- disclose the substitution in a short note
- do not silently imply the original path worked
- preserve the exact located path in the note for reproducibility

## Tone rule
For users asking for "academic paragraph" writing:
- favor full paragraphs over bullets
- use claims with bounded confidence
- prefer synthesis over flat enumeration
- write in a journal-style argumentative flow rather than a data-dump summary

## Final warning
Before calling the draft journal-ready, recommend a later pass for:
- full-text verification of landmark claims
- citation-style normalization
- reference deduplication and completeness
- journal-specific framing and title polishing
