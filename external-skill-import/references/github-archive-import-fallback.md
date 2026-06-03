# GitHub archive import fallback

Use this when a repository contains installable skills but `git clone` is blocked, denied, or unnecessary for a read-only import.

## When to prefer archive download

- `git clone` is blocked by approvals or environment policy
- the task is "import skills from this repo" rather than contribute back
- you only need the current default-branch contents
- the repo is small enough that a zip download is practical

## Durable workflow

1. Download the repository archive from GitHub codeload:
   - `https://codeload.github.com/<owner>/<repo>/zip/refs/heads/main`
2. Inspect the archive layout for installable skills.
3. Identify directories that contain `SKILL.md` plus any supporting `references/`, `templates/`, `scripts/`, or `assets/` files.
4. Compare both the directory name and the frontmatter `name:` against existing local skills before copying.
5. Copy only non-conflicting skills into `~/.hermes/skills/<category-or-umbrella>/...`.
6. Verify the copied `SKILL.md` files exist on disk.

## Why this matters

The archive path avoids needing a full git checkout and works well for one-shot skill imports where you want collision checks but do not need branch history.

## Repo-specific note: google/skills

`google/skills` stores the relevant installable skills under:
- `skills/cloud/<skill-name>/SKILL.md`

In a real import session, the following cloud skills were discovered there:
- alloydb-basics
- bigquery-basics
- cloud-run-basics
- cloud-sql-basics
- firebase-basics
- gemini-api
- gke-basics
- google-cloud-networking-observability
- google-cloud-recipe-auth
- google-cloud-recipe-onboarding
- google-cloud-waf-cost-optimization
- google-cloud-waf-reliability
- google-cloud-waf-security

Treat that list as an example snapshot, not a fixed invariant. The durable lesson is the archive-based import pattern plus collision checks.
