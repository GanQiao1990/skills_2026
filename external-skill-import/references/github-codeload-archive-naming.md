# GitHub codeload archive naming and import hygiene

Use this note when importing skills from a GitHub zip archive instead of a git clone.

## Durable lessons

1. Do not assume the extracted directory matches the zip filename you chose locally.
   - GitHub codeload archives normally unpack as `<repo>-<branch>`.
   - Example: downloading `https://codeload.github.com/google/skills/zip/refs/heads/main` produced an extracted root directory named `skills-main`, not `google-skills-main`.

2. After extraction, inspect the actual extracted tree before scripting copy logic.
   - A wrong root-directory assumption is easy to make and causes avoidable path failures.

3. For external skill imports, combine archive inspection with collision-safe copying.
   - Enumerate all remote directories containing `SKILL.md`.
   - Compare remote skill names against the full local skill library, not only the target category directory.
   - Copy only missing skills and preserve existing local variants unless the user explicitly asks to overwrite.

4. Verify installed results on disk by checking each copied `SKILL.md` path.

## Minimal checklist

- download archive
- extract archive
- inspect real extracted root name
- locate installable `SKILL.md` directories
- compare against all local installed skill names
- copy only missing skills
- verify copied `SKILL.md` files exist
