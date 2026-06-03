# Legacy `.ppt` template handling via derived project artifacts

Use this pattern when the user explicitly provides a legacy `.ppt` template but the working project already contains editable PPTX-side artifacts that clearly derive from that template.

## When this applies
- Input template is `.ppt`, not `.pptx`
- The project directory already contains one or more of:
  - `*_template_working.pptx`
  - `*_inventory.json`
  - `*_replacements.json`
  - `*_content.md` or other template-text extraction files
  - an earlier template-based report deck that matches the same visual system
- The user wants a finished PPT, not just an outline

## Recommended workflow
1. Treat the user-supplied `.ppt` as the visual source of truth.
2. Search the project for already-derived editable artifacts.
3. If such artifacts exist, use the best derived `.pptx` or template-working deck as the editing base.
4. Cross-check the narrative against the source `.docx` (or a verified same-basename `.md` extraction if present).
5. Preserve the template’s visual system while remapping the scientific storyline into the available slide layouts.
6. In the final note to the user, explicitly say that the deck was generated from project-local derived template artifacts corresponding to the supplied legacy template.

## Why this matters
- It keeps the output aligned with the user’s requested template even when the raw `.ppt` is not the most editable artifact.
- It avoids discarding valuable prior template analysis work already present in the repository.
- It is often the fastest way to produce a faithful finished deck instead of restarting template inspection from zero.

## Pitfalls
- Do not silently switch templates; disclose that a project-local derived working template was used.
- Do not rely only on old PPT content drafts; re-ground the slide narrative in the current source document.
- Do not treat an old application-layer order or stale storyline as authoritative if the source summary has since been updated.
