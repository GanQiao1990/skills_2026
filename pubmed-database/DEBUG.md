# DEBUG

Assumptions:
- User now specifically wants a PubMed-based paper query plus a usable literature summary, mainly to strengthen proposal background around Liming Liu and Sang Yup Lee.
- The most useful deliverable is a project-local markdown note that summarizes representative papers, recurring strategy patterns, and how these support the two-core-question proposal framing.
- Because the bundled PubMed CLI currently fails from a missing `science_skills_common` dependency, I should diagnose once, then use direct NCBI E-utilities (PubMed API) as the fallback PubMed route rather than block the task.

Evidence:
- The PubMed skill instructions and references were loaded this turn.
- Direct `uv run scripts/pubmed_api.py ...` failed with `Distribution not found at: file:///root/.hermes/skills/science_skills_common`.
- Existing proposal v8/v8.1/v8.2 already argues for two core problems and a shift away from NarQ–NarL as the primary control axis.

Verification target:
- Query PubMed for representative Liming Liu and Sang Yup Lee papers relevant to amino-acid / systems metabolic engineering.
- Summarize their research content and strategy patterns in a proposal-usable markdown note.
- Keep the final synthesis aligned with the project's two-core-question framing.
