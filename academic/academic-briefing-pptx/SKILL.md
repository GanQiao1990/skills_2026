---
name: academic-briefing-pptx
description: Create academic and executive scientific briefing slide outlines or finished PPTX decks from summaries, proposals, progress reports, or user-provided templates. Use when the deliverable is a leadership-facing or expert-facing presentation in Chinese or bilingual form, especially for PI / academician / reviewer briefings, direct “输出PPT” requests, template-derived deck generation, JSON-first briefing workflows, or template-constrained PPTX rewriting.
---

# Academic briefing PPTX

Use this as the umbrella skill for high-level academic/scientific briefing decks.

This class covers both:
- slide-by-slide outline generation
- direct `.pptx` production
- template-based rewriting when the user provides a PPTX template
- JSON-first intermediate briefing structures before final PPTX editing

It is for briefing decks aimed at academic leaders,院士, PIs, strategic reviewers, department heads, and expert panels. It is not the default skill for full teaching decks, manuscript figure packs, or broad classroom presentations.

## Decide the deliverable first
Before writing content, determine which of these the user actually wants:

1. **Outline mode**
   - User wants slide titles + bullets only.
   - Return direct slide-by-slide content.

2. **Finished PPTX mode**
   - User says `直接输出 PPT` or asks for a real file.
   - Default to creating or editing a `.pptx`, not merely proposing an outline.

3. **Template-derived mode**
   - User provides a PPT/PPTX template and asks to follow it.
   - Keep the template's visual system whenever feasible.
   - Duplicate layouts before abandoning the template.

4. **JSON-first mode**
   - User asks to first write the deck as JSON, then map it into slides.
   - Treat the JSON as the authoritative narrative spine for the PPT rewrite.

## Core briefing narrative
For this project class, the safest default storyline is:
1. research background / why the problem matters
2. overall research idea / project logic
3. completed methodological foundation first
4. experimental or validation evidence
5. transition from platform to application layers
6. innovation points
7. next-step work and expected outputs

Do **not** open with speculative applications before establishing the completed methodological base.

## Scientific-credibility rule
Always preserve the distinction between:
- `已完成 / 已建立 / 已验证`
- `拟探索 / 初步猜想 / 方法设想 / 后续验证`

Do not present application hypotheses as closed mechanisms.

## Output style
- Prefer concise Chinese suitable for oral delivery.
- Each slide should carry one dominant takeaway.
- Avoid proposal-style dense prose.
- Avoid meta language like `从原材料整理如下`.
- For expert briefings, prioritize narrative continuity over document completeness.

## Default no-template deck architecture
Use this when the user wants a scientific briefing deck but does not constrain you to a specific template:
1. title
2. research background
3. overall research idea
4. completed methodology foundation I
5. technical core / pipeline details
6. completed methodology foundation II or screening strategy
7. validation system / evidence chain
8. key mechanistic node / pivot
9. preliminary evidence for that node
10. application layer 1
11. application layer 2
12. application layer 3
13. innovation summary
14. next steps and expected outputs
15. closing / thanks

Compress to 10–12 slides only when the user explicitly wants a shorter executive version.

## Template-derived PPTX workflow
When the user provides a PPTX template:

1. Extract the narrative spine from the source content first.
2. Inspect the template before writing content.
   - extract visible text
   - inspect layout / placeholder structure
3. If the template is short, duplicate usable layouts rather than abandoning it.
4. Map content to actual shape capacity, not to source-document richness.
5. If replacement tooling reports overflow, compress wording before shrinking font.
6. Deliver a real PPTX plus a short verification summary.

### Tight-template compression tactics
- shorten wording before shrinking font
- remove connector phrases first
- compress mixed Chinese/English lines
- replace full sentences with short parallel noun/verb phrases
- for three-column layouts, keep each column to 2–3 short lines
- if a few low-priority boxes remain tight, save a readable draft and report the template constraint honestly

## JSON-first briefing workflow
Use when the user says `先写成json` or otherwise wants a machine-readable outline before slide editing.

Rules:
1. Build the JSON first.
2. Treat it as the authoritative narrative source for the deck rewrite.
3. Keep every slide within the user-specified macro sections.
4. Organize sections around `问题 / 方法 / 效果` unless the user requests a different split.
5. Preserve any exact user-specified cover title literally.

## Three-section Chinese expert-briefing pattern
When the user constrains the deck to exactly three macro sections such as:
- `研究背景`
- `研究思路`
- `研究方案`

then:
- keep every content slide explicitly inside one of those section labels
- use short on-screen bullets suitable for oral reporting
- split hidden dual-background structures instead of blending them into one vague summary
- if the user asks for `三个执行形式`, encode them explicitly as named execution forms under `研究方案`

## Evidence handling
- If the source includes a real phenotype or experiment, elevate it into its own support slide.
- Prefer one evidence slide that upgrades a mechanism from speculation to supported priority.
- Keep claims calibrated by evidence status.

## Verification rule
After creating a PPTX, verify by checking:
- the file exists and is non-empty
- the slide count matches expectation
- the slide titles/order reflect the intended storyline

If thumbnail or PDF conversion fails, do not treat that as proof that the deck failed. Fall back to direct PPTX structural inspection.

## Common pitfalls
- returning only an outline when the user explicitly asked for a finished PPTX
- abandoning a user template too early instead of duplicating layouts
- overfilling narrow template boxes with paragraph prose
- mixing completed work and future hypotheses without labels
- opening with applications before establishing the platform/method basis
- rewriting a user-specified cover title into a smoother but different title
- collapsing a deliberate two-background argument into one generic background slide

## References in this umbrella
Read these as needed:
- `references/narl-academician-briefing-example.md` — platform-first academician briefing structure
- `references/short-template-overflow-playbook.md` — how to expand and fit tight 3–4 slide templates
- `references/json-first-three-section-briefing.md` — JSON-first three-section workflow
- `references/narl-three-section-two-background-pages.md` — split-background pattern
- `references/narl-three-section-execution-forms-playbook.md` — explicit 三个执行形式 pattern
- `references/legacy-ppt-template-derived-artifacts.md` — handling legacy `.ppt` inputs via derived `.pptx` work artifacts

## Practical decision rule
If the user's real need is a leadership-facing scientific briefing deck, keep everything in this one skill family:
- narrative-only outline
- direct PPTX generation
- template-constrained rewriting
- JSON-first briefing intermediates

Treat those as one umbrella class with labeled subpatterns, not as separate narrowly named skills.