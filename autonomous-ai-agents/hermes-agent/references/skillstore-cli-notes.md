# Skillstore CLI notes

Use when a user asks to install a skill via `npx skillstore ...` rather than Hermes's native `hermes skills ...` commands.

Durable reminders:
- `npx skillstore add <target>` accepts either a skill slug or an `@plugin` target.
- `npx skillstore add --help` is the fastest way to confirm the expected target shape before guessing.
- A `Skill "name" not found` error is not evidence that `@name` is correct; plugin and skill namespaces are separate.
- If both the plain slug and `@plugin` form fail, stop and ask for the canonical Skillstore slug or source URL.
- `--dry-run` is useful when testing a likely slug without writing files.

Example failure pattern worth recognizing:
- `npx skillstore add paper-write` → `Skill "paper-write" not found`
- `npx skillstore add @paper-write` → `Plugin "@paper-write" not found`

Correct takeaway:
- The requested identifier is unresolved, not that either command form is universally wrong.
