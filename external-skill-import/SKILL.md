---
name: external-skill-import
description: Import Agent Skills from external GitHub repositories into Hermes. Use when the user shares a GitHub repo URL containing skills, asks to add/install/import skills from a repo, or references the agentskills.io standard.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, import, github, agents, curation]
    related_skills: [skill-creator, hermes-agent-skill-authoring]
---

# Importing External Agent Skills

## Overview

External repos following the [Agent Skills](https://agentskills.io) standard use the same `SKILL.md` format as Hermes. This skill covers discovering, evaluating, conflict-checking, and installing skills from those repos into `~/.hermes/skills/`.

## When to Use

- User shares a GitHub repo URL and says "add these skills"
- User references `agentskills.io` or `.agents/skills/` convention
- User asks to import/sync skills from an external source

## Workflow

### 1. Explore the Repo (without cloning)

Use the GitHub API to list contents. Faster than cloning for initial inspection:

```bash
# List top-level structure
curl -sL https://api.github.com/repos/<owner>/<repo>/contents/ | \
  python3 -c "import json,sys; [print(f'{d[\"type\"]:6s} {d[\"name\"]}') for d in json.load(sys.stdin)]"

# Skills are usually under .agents/skills/
curl -sL https://api.github.com/repos/<owner>/<repo>/contents/.agents/skills/ | \
  python3 -c "import json,sys; [print(f'{d[\"type\"]:6s} {d[\"name\"]}') for d in json.load(sys.stdin)]"
```

For repos using a flat structure or different convention, check `README.md` first:
```bash
curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/README.md | head -80
```

### 2. Read Skill Metadata

Read each skill's `SKILL.md` frontmatter to understand what it does before installing:

```bash
curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/.agents/skills/<name>/SKILL.md | head -10
```

### 3. Conflict Detection

Check for name collisions with existing skills:

```bash
# List existing skills
ls ~/.hermes/skills/

# For any collision, compare content size and quality
wc -c ~/.hermes/skills/<name>/SKILL.md
```

**Decision rules:**
- **No collision** → install
- **Collision, same content** → skip silently
- **Collision, local is larger/richer** → skip, log as "already customized"
- **Collision, user explicitly asked to import/sync the repo and upstream copy is clearly the canonical richer copy** → backup the local skill directory, then replace with the upstream version; report the backup path explicitly
- **Collision, unclear which copy should win** → ask before overwriting

**Practical overwrite pattern when the user asked for repo sync/import:**
- move the existing skill to `<name>_backup_before_import`
- copy the incoming skill into `~/.hermes/skills/<name>/`
- verify the new `SKILL.md` exists
- report both the replacement and the backup path

### 4. Install New Skills

```python
import shutil, os

src = "/tmp/<repo>/.agents/skills/<name>"
dst = os.path.expanduser("~/.hermes/skills/<name>")
if not os.path.exists(dst):
    shutil.copytree(src, dst)
```

For batch installs, use `execute_code` to loop through all non-conflicting skills.

### 5. Verify Installation

```bash
for s in skill1 skill2 ...; do
  [ -f ~/.hermes/skills/$s/SKILL.md ] && echo "✓ $s" || echo "✗ $s MISSING"
done
```

## Pitfalls

1. **Don't blindly overwrite customized local skills.** Always compare sizes/content first. Local skills may have Hermes-specific adaptations that upstream lacks.

2. **Agent Skills repos may use `.agents/skills/` or `skills/` or flat structure.** Check the repo layout before assuming the path.

3. **Hermes taps expect a top-level skill layout.** `hermes skills tap add owner/repo` can register a repo even when its real skills are nested somewhere like `plugins/.../skills/`, but Hermes may not expose those nested skills through normal search/inspect/install flows. For nonstandard repos, either copy/install the needed skill manually, create a local wrapper skill in `~/.hermes/skills/`, or add a repo-local top-level `skills/<name>/SKILL.md` entrypoint.

4. **A wrapper skill is often the cleanest bridge for plugin-style repos.** Keep the wrapper class-level: it should route future agents to the correct nested skill directories rather than duplicate every upstream skill inline.

5. **The session skill loader is cached.** Newly installed skills won't appear in `skills_list` until the next session. This is expected.

6. **Some repos include non-SKILL.md files** (LICENSE.txt, examples/, scripts/). Copy the entire skill directory — these supporting files are often needed.

7. **Rate limits.** The unauthenticated GitHub API allows 60 requests/hour. For repos with many skills, clone instead of making dozens of API calls.

8. **Large class-level repos may contain many collisions with richer local umbrella skills.** In that case, preserve clearly richer local copies for broad database/knowledge skills, but when the user explicitly requests importing the external library, it is acceptable to replace a local skill with the upstream copy if you first create a clearly named backup directory and report the replacement.

9. **When the user wants imported skills to become project base logic, installation alone is not enough.** Add a project-level `AGENTS.md` (or equivalent project rule file) that names the base logic skill(s) and tells future agents to treat them as the default behavioral/factual layer.

10. **Distinguish project-scoped base logic from Hermes-global base logic.**
- For a specific repo/project, add the guidance to that project's `AGENTS.md` or `HERMES.md`.
- For Hermes-global behavior across future sessions, write the guidance to `~/.hermes/HERMES.md` so it becomes global project context for Hermes itself.
- If the user wants an external skill repository to stay visible globally, add its stable directory to `skills.external_dirs` in `~/.hermes/config.yaml`.

11. **Do not leave `skills.external_dirs` pointing at transient clone paths like `/tmp/...` when the user expects a durable install.**
Use a persistent location such as `~/.hermes/external-skills/<repo>/skills` (or another stable user-owned path), then point `skills.external_dirs` there. Temporary clone paths are acceptable only for one-shot inspection or migration.

## Additional reference

- `references/github-archive-import-fallback.md` — archive-download workflow for importing skills when `git clone` is blocked or unnecessary, with collision checks and a real `google/skills` layout example.
- `references/github-codeload-archive-naming.md` — durable note on GitHub codeload zip extraction naming (`<repo>-<branch>`), plus a minimal checklist for collision-safe archive imports.
- `references/manual-archive-install-and-runtime-verification.md` — use when an upstream skill's documented install path is zip/manual rather than Hermes-native, or when `hermes skills install <raw-url>` fails and you need the durable fallback plus runtime selection/verification steps.

## One-Shot Recipes

### Quick import (small repo, <20 skills)

```bash
cd /tmp && git clone --depth 1 https://github.com/<owner>/<repo>.git
# Then use execute_code to copy non-conflicting skills
```

### Selective import (user specified skills)

```bash
cd /tmp && git clone --depth 1 https://github.com/<owner>/<repo>.git
# Copy only the named skills
for s in skill-a skill-b; do
  cp -r /tmp/<repo>/.agents/skills/$s ~/.hermes/skills/
done
```
