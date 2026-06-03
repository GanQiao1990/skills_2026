# Checklist evidence crosswalk pattern

Use this pattern when a publication-ready package will be judged by inspecting files rather than by reading your chat summary.

## Goal

Add a reviewer-facing evidence map inside the package so a third party can quickly verify where each major requirement is satisfied.

## Recommended artifact

Create `EVIDENCE_MAP.md` in the package root.

## What to include

1. **Primary package files**
   - authoritative manuscript
   - derived DOCX/PDF
   - figure-generation script
   - conversion script
   - README / INDEX / validation note
   - figure directory and any package-local canonical inputs

2. **Manuscript line map**
   Point to exact line numbers for:
   - title
   - author/correspondence note
   - abstract
   - introduction
   - methods/workflow
   - validation plan
   - results/synthesis
   - discussion
   - conclusion
   - reproducibility note
   - provenance/citation note
   - references
   - figure captions and table captions

3. **Source-basis disclosure**
   Explicitly point reviewers to the lines where malformed or unreadable user-supplied paths are disclosed and where the actual inspected path is stated.

4. **Figure evidence**
   Record:
   - manuscript image links
   - package-relative figure paths
   - figure resolutions in pixels
   - whether the figure is programmatically reproducible
   - any package-local source graphics used to rebuild composite figures

5. **Conversion evidence**
   Point to the conversion script sections that show:
   - dependency declarations
   - input/output arguments
   - external-tool checks
   - conversion invocation
   - post-processing/layout logic

6. **DOCX verification evidence**
   Record direct inspection results such as:
   - paragraph count
   - table count
   - embedded image count
   - presence of title/major headings/captions

7. **Package cleanliness evidence**
   State that placeholders, `__pycache__`, and `.pyc` artifacts were checked and removed.

## Why this matters

For checklist-heavy tasks, judges often look for file-internal evidence instead of trusting a final chat response. An `EVIDENCE_MAP.md` reduces ambiguity and shortens review time.

## Related verification pattern

When auditing citations, expand numeric ranges like `[1-6]` before comparing cited numbers to the reference list. A naive regex that captures only the first number in a range will undercount citations and can create a false mismatch.
