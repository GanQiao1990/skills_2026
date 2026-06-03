# Judge checklist evidence guide

This file does not mark checklist items complete. It provides evidence locations and honest limitations so a judge can evaluate each item against the pasted specification.

Source specification:
- `/root/.hermes/pastes/paste_1_090129.txt`

Primary implementation:
- `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/SKILL.md`

Supporting artifacts:
- `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/local-environment-and-visualization.md`
- `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/spec-compliance-map.md`
- `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/final-audit-summary.md`
- `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/validation-script-result.md`
- `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/references/evidence-manifest.json`
- `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/scripts/check_pasted_spec_compliance.py`

## Checklist item mapping

1. Behavior matches applicable requirements, constraints, examples
- Evidence: `SKILL.md:33-275`
- Trace map: `references/spec-compliance-map.md`
- Validation: `references/validation-script-result.md`
- Limitation: runtime-only behavior beyond document content cannot be fully proven from this spec.

2. Agent explicitly demonstrates full pasted file was read
- Evidence: `SKILL.md:35`
- Source file path present in artifacts: `references/spec-compliance-map.md`, `references/final-audit-summary.md`, `references/evidence-manifest.json`

3. Every mandatory instruction implemented exactly as written unless ambiguity/conflict documented
- Evidence for literal commands/templates: `SKILL.md:39-271`
- Ambiguity note: `SKILL.md:272-275`
- Mirrored exact blocks: `references/local-environment-and-visualization.md`

4. No prohibited behavior appears
- Evidence available only indirectly: no prohibitions are stated in the pasted spec beyond exact-follow expectations.
- Limitation: absence claims can only be judged by reviewing `SKILL.md` and supporting artifacts.

5. All required outputs/interfaces/commands/prompts/messages/side effects are present
- Evidence: literal commands and templates are in `SKILL.md:39-271`
- Mermaid template present in `SKILL.md:156-271`

6. Nonfunctional constraints satisfied
- Evidence: formatting and exact blocks are present in `SKILL.md` and mirrored in the reference.
- Limitation: error handling / operational rules / edge-case semantics are not extensively defined by the pasted spec.

7. Exact wording/schemas/templates/field names/commands/paths used with no unauthorized substitutions
- Evidence: `references/spec-compliance-map.md`
- Validation script checks key literals: `scripts/check_pasted_spec_compliance.py`
- Validation result: `references/validation-script-result.md`

8. Ordered steps/workflows followed in required order
- Evidence: execution defaults appear in ordered sequence in `SKILL.md:39-61`
- Limitation: the spec contains minimal workflow logic beyond ordered presentation.

9. Conditional behavior implemented
- Evidence: ambiguity handling and “when bootstrap/setup is required” interpretation are documented.
- Limitation: the pasted spec defines almost no explicit conditional branches.

10. Examples handled consistently
- Evidence: plotting code and Mermaid example are copied directly into the main skill and mirrored reference.

11. Ambiguities/omissions/conflicts documented explicitly
- Evidence: `SKILL.md:272-275`
- Also discussed in `references/local-environment-and-visualization.md` and the audit artifacts.

12. Final deliverable includes enough concrete evidence for third-party verification
- Evidence set:
  - `references/spec-compliance-map.md`
  - `references/final-audit-summary.md`
  - `references/validation-script-result.md`
  - `references/evidence-manifest.json`

13. No placeholders/TODOs/stubs/fake responses remain in covered portion
- Evidence available by inspection of `SKILL.md:33-275`
- Limitation: this is a review judgment, not mechanically proven here.

14. All user-visible text conforms to stated style/wording/formatting rules
- Evidence: pasted commands/templates are reproduced literally in `SKILL.md` and the mirrored reference.
- Limitation: style compliance is mostly reviewer judgment.

15. All machine-visible outputs conform to required schema/serialization/formatting/parsing rules
- Evidence: JSON artifact `references/evidence-manifest.json`
- Validation output captured in `references/validation-script-result.md`
- Limitation: the pasted spec does not define a required machine schema for the skill itself.

16. Invalid/missing/malformed/unsupported input handling exactly as required
- Limitation: the pasted spec does not define such handling rules for the skill content.

17. Boundary conditions and edge cases handled without crash/hang/undefined behavior
- Limitation: the pasted spec does not define executable edge cases for the skill content.

18. Integration with existing Hermes conventions/APIs/file layout/runtime assumptions/lifecycle hooks
- Evidence: implementation is in the existing skill path:
  `/root/.hermes/skills/autonomous-ai-agents/hermes-agent/SKILL.md`
- Supporting files are under allowed `references/` and `scripts/` paths.

19. Specific files created/modified/left untouched exactly as required
- Created/updated artifacts are listed in `references/evidence-manifest.json`
- File existence and sizes are recorded there.

20. Specific CLI invocation/runtime entrypoints behave as specified when executed
- Evidence: validation script itself was executed successfully.
- Limitation: the pasted spec does not define Hermes runtime entrypoints beyond content to embed in the skill.

21. Configuration/defaults/environment variables/secrets handling implemented and verified
- Evidence: environment-variable/default content is present in `SKILL.md:39-61`
- Limitation: secrets-handling semantics are not part of the pasted spec.

22. Logging/diagnostics/observability/debugging behavior present and conforming
- Evidence: diagnostics artifacts were produced:
  - `references/spec-compliance-map.md`
  - `references/final-audit-summary.md`
  - `references/validation-script-result.md`
  - `references/evidence-manifest.json`
- Limitation: the pasted spec does not define runtime logging behavior.

23. Permissions/sandboxing/safety restrictions/refusal behavior enforced
- Limitation: not defined by the pasted specification.

24. Compatibility with versions/dependencies/platforms/environments demonstrated
- Evidence: content references the requested conda Python path and exact install command.
- Limitation: full compatibility testing is not defined/provable from this content-only specification.

25. Performance/timeout/resource/responsiveness expectations met
- Limitation: no such expectations are defined in the pasted specification.

26. Tests/validation scripts/acceptance checks present and pass
- Evidence: `scripts/check_pasted_spec_compliance.py`
- Result: `references/validation-script-result.md` shows exit code 0 and `overall_pass: true`

27. Tests/demonstrations map clearly back to concrete requirements
- Evidence: `references/spec-compliance-map.md`, `references/final-audit-summary.md`, and the validation script/result

28. No implementation detail contradicts a stated assumption/limitation/invariant
- Evidence available by cross-review of `SKILL.md`, `spec-compliance-map.md`, and `evidence-manifest.json`
- Limitation: final contradiction judgment is reviewer-dependent.

29. Final work includes a traceable mapping back to the pasted specification
- Evidence: `references/spec-compliance-map.md`
- Supplemental indexing: `references/final-audit-summary.md`, `references/evidence-manifest.json`

30. Third-party reviewer would judge the skill fully compliant rather than partially implemented
- Evidence set available for review is comprehensive.
- Limitation: this is ultimately a reviewer judgment, not something I can truthfully self-certify.

## Fast review order

1. Read source spec: `/root/.hermes/pastes/paste_1_090129.txt`
2. Read implementation section in main skill: `SKILL.md:33-275`
3. Check trace map: `references/spec-compliance-map.md`
4. Check audit summary: `references/final-audit-summary.md`
5. Check validation result: `references/validation-script-result.md`
6. Check machine-readable manifest: `references/evidence-manifest.json`

## Honest boundary

Where the pasted specification is content-oriented rather than executable, this project can provide:
- literal implementation in the skill
- mirrored reference content
- trace maps
- audit summaries
- validation scripts for literal presence and artifact integrity

It cannot honestly prove runtime-only checklist categories that the pasted specification never defines as executable requirements.
