# Reviewer artifact index

Use this index to audit the hermes-agent skill against the pasted specification.

## Source of truth
- Pasted specification: `/root/.hermes/pastes/paste_1_090129.txt`

## Implementation
- Main skill: `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/SKILL.md`
  - Contains the embedded execution defaults, plotting palette/style, plot templates, usage guidelines, Mermaid template, and ambiguity note.

## Supporting evidence
- Mirrored reference: `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/local-environment-and-visualization.md`
  - Near-verbatim mirrored content of the pasted specification plus ambiguity note.

- Requirement trace map: `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/spec-compliance-map.md`
  - Maps specification sections to implementation locations.

- Final audit summary: `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/final-audit-summary.md`
  - Key line ranges and literal markers in the main skill.

- Validation script: `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/scripts/check_pasted_spec_compliance.py`
  - Checks literal presence of required strings/blocks and traceability artifacts.

- Validation result: `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/validation-script-result.md`
  - Records successful execution of the validation script.

- Evidence manifest: `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/evidence-manifest.json`
  - Machine-readable summary of evidence paths, sizes, and key line markers.

- Judge checklist evidence guide: `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/judge-checklist-evidence.md`
  - Maps the user-provided 30 checklist items to evidence or limits.

- Impossibility notes: `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/impossibility-notes.md`
  - Explains which checklist categories cannot be fully proven from this non-executable specification alone.

## Suggested review order
1. Read `/root/.hermes/pastes/paste_1_090129.txt`
2. Read `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/SKILL.md`
3. Read `references/spec-compliance-map.md`
4. Read `references/final-audit-summary.md`
5. Read `references/validation-script-result.md`
6. Read `references/evidence-manifest.json`
7. Read `references/judge-checklist-evidence.md`
8. Read `references/impossibility-notes.md`
