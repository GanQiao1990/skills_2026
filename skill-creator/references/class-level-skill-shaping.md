# Class-level skill shaping

Use this note when deciding how to update the Hermes skill library.

## Preferred shape
- Build class-level umbrella skills for recurring task families.
- Keep SKILL.md rich enough to route the work, but not so detailed that it becomes a dump of one-session facts.
- Put session-specific detail, evidence, error transcripts, examples, and quick reference material in `references/`.
- Put reusable deterministic helpers in `scripts/`.
- Put copy/modify starters in `templates/`.

## What to avoid
- One-skill-per-session entries.
- Names that only make sense for one task, one run, one error, or one PR.
- Long flat lists of narrow skills when a broader umbrella would cover them.

## Rule of thumb
If the knowledge is useful for future work in the same class, keep it in the umbrella skill. If it is only evidence or detail from one run, move it to `references/`.
