# Contributing HyperFrames to Agent Skills Repos

How to adapt the HyperFrames skill (or any Hermes skill) to the [Agent Skills](https://agentskills.io) standard for contribution to external repos like [warpdotdev/oz-skills](https://github.com/warpdotdev/oz-skills).

## Agent Skills Format

Each skill is a folder containing a single `SKILL.md`:

```
.agents/skills/
└── your-skill-name/
    └── SKILL.md
```

### Frontmatter (Required)

```yaml
---
name: skill-name          # kebab-case, matches directory name
description: >-
  Imperative verb + what the skill does.
  Use when the user asks for the workflow this skill handles.
license: MIT
---
```

**Description rules (strict):**
- Exactly two sentences
- Sentence 1: starts with imperative verb (`Build`, `Audit`, `Test`, `Optimize`, `Generate`, etc.)
- Sentence 2: starts with `Use when...`
- Keep concise and concrete; no filler

### Body

- Single H1 in Title Case reflecting the skill's purpose
- Sections: When to Use, Workflow, Examples, Pitfalls, etc.
- Self-contained — no linked reference files (unlike Hermes skills which use `references/`, `templates/`, `scripts/`)

## Adaptation Workflow

### 1. Clone the target repo

```bash
git clone https://github.com/warpdotdev/oz-skills.git /tmp/oz-skills
cd /tmp/oz-skills
```

### 2. Analyze existing skills for conventions

Read 2-3 existing `SKILL.md` files to understand length, section structure, and detail level. Oz-skills skills are typically 80-250 lines — significantly shorter than Hermes skills.

### 3. Condense the Hermes skill

The Hermes HyperFrames skill has:
- Main SKILL.md (~400 lines with YAML frontmatter in Hermes format)
- 11 reference files (captions, tts, audio-reactive, typography, transitions, etc.)
- House style, visual styles, patterns, data-in-motion docs

For Agent Skills, condense to a single SKILL.md that covers:
- **Core rules** (non-negotiable constraints)
- **Structure** (data attributes, timeline contract, composition layout)
- **Workflow** (layout-before-animation, scene transitions)
- **Quality checks** (contrast, animation map)
- **Key pitfalls** (environment traps, common mistakes)

Drop: visual style presets, palette catalogs, TTS details, advanced caption techniques. These are too niche for a general-purpose skill.

### 4. Fork and create PR

```bash
# Add your fork as remote
git remote add fork https://github.com/YOUR_USER/oz-skills.git
git checkout -b add-hyperframes-skill

# Create the skill
mkdir -p .agents/skills/hyperframes
# Write SKILL.md following the format above

git add .agents/skills/hyperframes/SKILL.md
git commit -m "feat: Add hyperframes skill for HTML-based video composition"

git push fork add-hyperframes-skill

# Create PR via gh CLI
gh pr create --repo warpdotdev/oz-skills \
  --head YOUR_USER:add-hyperframes-skill \
  --title "feat: Add hyperframes skill" \
  --body-file /tmp/pr_body.md
```

### PR body template

```markdown
## What
Adds a **hyperframes** skill for [brief description].

## Why
[2-3 sentences on what the skill enables for agents]

## Skill format
Follows the Agent Skills standard with YAML frontmatter and self-contained markdown.
```

## Key Differences: Hermes vs Agent Skills

| Aspect | Hermes Skill | Agent Skills (oz-skills) |
|--------|-------------|-------------------------|
| Location | `~/.hermes/skills/<name>/` | `.agents/skills/<name>/` |
| Frontmatter | YAML with `name`, `description`, `tags`, `related_skills` | YAML with `name`, `description`, `license` |
| Description | Freeform | Strict 2-sentence pattern |
| Support files | `references/`, `templates/`, `scripts/` | None (single SKILL.md) |
| Length | 200-500+ lines with linked refs | 80-250 lines, self-contained |
| License | Not in frontmatter | Required field |
