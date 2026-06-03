---
name: byterover-local-markdown-memory
description: Install byterover-cli (brv) and configure a local markdown memory swarm for offline use — no cloud account required. Use when the user wants to set up ByteRover as a local knowledge/memory backend for Hermes or other agents.
version: 1.0.0
author: Hermes Agent
tags: [byterover, memory, local, markdown, swarm, brv]
---

# ByteRover Local Markdown Memory Setup

ByteRover CLI (brv) is a knowledge/memory CLI for agents. It supports multiple
"swarm" providers including cloud, GBrain, Obsidian, Hindsight, and local markdown.
This skill covers the fully local, no-login path using the local_markdown provider.

---

## Step 1: Install byterover-cli globally via npm

  npm install -g byterover-cli

The binary is NOT called `byterover` — it is called `brv`.

PITFALL: If npm is the conda-managed npm (under ~/anaconda3/bin/npm), the binary
lands at ~/anaconda3/bin/brv and may NOT be on the shell PATH used by the agent.
Always use the full path if `brv` is not found:

  /home/qiao/anaconda3/bin/brv --help

Engine warnings about node <22 are non-fatal for local markdown usage.

---

## Step 2: Check status

  brv status
  # or full path:
  /home/qiao/anaconda3/bin/brv status

Expected output when not yet initialized:
  Context Tree: Not initialized
  Space: Not connected

---

## Step 3: Create the swarm config manually

The `brv swarm onboard` wizard requires interactive input. For automated setup,
write the config directly.

PITFALL: The config schema is strict (validated by Zod). Two common errors:
  - providers.byterover: Required  <- byterover key is ALWAYS required even if disabled
  - providers.localMarkdown.folders.0.name: Required  <- each folder needs a `name` field

Correct minimal config for local-only use:

  mkdir -p ~/.brv/swarm ~/.brv/memory
  cat > ~/.brv/swarm/config.yaml << 'EOF'
  providers:
    byterover:
      enabled: false
    local_markdown:
      enabled: true
      folders:
        - name: hermes-memory
          path: /home/qiao/.brv/memory
          read_only: false
          follow_wikilinks: true
  EOF

Key fields for local_markdown folders:
  name            — required string label
  path            — absolute path to markdown folder
  read_only       — false = agent can write new notes (default: true)
  follow_wikilinks — traverse [[wikilinks]] in search (default: true)

---

## Step 4: Verify

  brv swarm status

Expected output:
  ✗ ByteRover       context-tree (disabled/not connected)
  ✓ Local .md       1 folder(s)
  Write Targets: local-markdown:hermes-memory (note, general)
  Swarm is operational (1/2 providers configured).

---

## Step 5: Test store and query

  # Store a fact
  brv swarm curate "The project path is /home/qiao/myproject"

  # Query
  brv swarm query "project path"

---

## Config schema reference (key fields only)

Top-level sections (all optional except providers):
  providers   — required; must include byterover key even if disabled
  routing     — search strategy settings
  performance — cache and concurrency settings
  provenance  — audit trail settings
  budget      — monthly cost caps (for cloud providers)
  enrichment  — edges for cross-provider enrichment

LocalMarkdown folder fields:
  name             string   REQUIRED
  path             string   REQUIRED (absolute path)
  enabled          bool     (top-level provider field)
  read_only        bool     default true; set false to allow writes
  follow_wikilinks bool     default true

---

## Pitfalls

- `brv` binary name: NOT `byterover` or `byterover-cli`. It is `brv`.
- conda npm installs to ~/anaconda3/bin/brv — may not be in PATH. Use full path.
- providers.byterover is REQUIRED in config.yaml even when set to enabled: false.
- Each folder under local_markdown.folders MUST have a `name` field.
- YAML key is `local_markdown` (snake_case); the Zod schema maps it to `localMarkdown` internally.
- `read_only` defaults to true — set it to false if you want the agent to write notes.
- Node <22 warnings are non-fatal for local markdown functionality.
- `brv swarm onboard` is interactive; skip it and write config.yaml directly for automation.
