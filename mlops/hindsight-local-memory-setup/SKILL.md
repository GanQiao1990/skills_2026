---
name: hindsight-local-memory-setup
description: Configure Hermes to use Hindsight as its long-term memory provider in local mode, backed by a pgvector/PostgreSQL database. Use when the user wants to wire up a running Hindsight API instance (local_external) or an embedded local instance (local_embedded) as Hermes memory, instead of the default holographic or cloud provider.
version: 1.0.0
author: Hermes Agent
tags: [hermes, memory, hindsight, pgvector, postgres, local]
---

# Hindsight Local Memory Setup for Hermes

Hindsight is a long-term memory plugin for Hermes with knowledge graph, entity resolution,
and multi-strategy vector retrieval. It supports three modes:

  cloud          — Hindsight cloud API (requires HINDSIGHT_API_KEY)
  local_embedded — Hermes auto-starts the hindsight-api daemon (downloads ~200MB)
  local_external — Point at an already-running hindsight-api instance (most common)

This skill covers the local_external path, which is what you want when:
- You have a pgvector/pg16 (or pg15/pg17) Docker container running
- You have a hindsight-api process already running on some port (default 8888)
- You just need to wire Hermes to use it

---

## Architecture (local_external)

  Hermes memory plugin
    -> ~/.hermes/hindsight/config.json  (mode: local_external)
    -> http://localhost:8888             (hindsight-api process)
    -> postgresql://user:pass@host:port/db  (pgvector container)

---

## Step 1: Verify the Hindsight API is running and healthy

  curl -s http://localhost:8888/health
  # Expected: {"status":"healthy","database":"connected"}

If not running, start it. From the hindsight repo:

  cd /path/to/hindsight
  uv run python -m hindsight_api.main --port 8888 --host 127.0.0.1

Or check if it's managed by a systemd service or background process.

---

## Step 2: Verify the Hindsight API is connected to the right database

Check the running process environment for HINDSIGHT_API_DATABASE_URL:

  cat /proc/<hindsight_pid>/environ | tr '\0' '\n' | grep DATABASE_URL

Expected format:
  HINDSIGHT_API_DATABASE_URL=postgresql://hindsight_user:PASSWORD@127.0.0.1:5433/hindsight_db

If using the pgvector Docker container, verify it's up:
  docker ps | grep hindsight-db

Check the DB has Hindsight's schema (15 tables including memory_units, entities, chunks):
  docker exec <container> psql -U hindsight_user -d hindsight_db -c '\dt'

---

## Step 3: Write ~/.hermes/hindsight/config.json

  mkdir -p ~/.hermes/hindsight
  cat > ~/.hermes/hindsight/config.json << 'EOF'
  {
    "mode": "local_external",
    "api_url": "http://localhost:8888",
    "bank_id": "hermes",
    "budget": "mid"
  }
  EOF

Key fields:
  mode      — "local_external" (API already running), "local_embedded" (auto-start), or "cloud"
  api_url   — URL of the hindsight-api (only used in local_external mode)
  bank_id   — Memory bank identifier; "hermes" is the default used by the plugin
  budget    — Recall budget: "low" / "mid" / "high" (affects retrieval depth)

The plugin also reads from env vars as fallback:
  HINDSIGHT_MODE, HINDSIGHT_API_URL, HINDSIGHT_API_KEY, HINDSIGHT_BANK_ID, HINDSIGHT_BUDGET

Profile-scoped path: $HERMES_HOME/hindsight/config.json
Legacy fallback:     ~/.hindsight/config.json

---

## Step 4: Set Hermes memory provider to hindsight

  hermes config set memory.provider hindsight

---

## Step 5: Verify

  hermes memory status

Expected output includes:
  Provider:  hindsight
  Plugin:    installed
  Status:    available
  ... hindsight  (API key / local) <- active

---

## Teardown / Removing Hindsight

To completely remove Hindsight and revert to holographic:

  1. Switch the provider:
     hermes config set memory.provider holographic

  2. Delete both config locations (both may exist):
     rm -rf ~/.hermes/hindsight/
     rm -rf ~/.hindsight/

  3. Stop any running processes:
     pkill -f hindsight_api.main
     pkill -f hindsight-embed

  4. Verify:
     hermes memory status
     # Should show: Provider: holographic ... holographic (local) <- active

Note: The hindsight plugin binary remains installed but inactive. No need to
uninstall it unless you want a clean slate.

---

## Holographic as Fallback Provider

Holographic is Hermes' built-in local memory plugin — no API key, no external DB.
It uses a local SQLite file (~/.hermes/memory_store.db, auto-created on first write).

Install the Python package if missing (required for the plugin to load):
  pip install holographic

If pip install fails with name resolution errors, try pypi.org directly:
  pip install holographic -i https://pypi.org/simple/

If a broken 'rich' package blocks installation:
  pip install rich --force-reinstall
  pip install holographic

Key difference from Hindsight:
  - Hindsight tools: hindsight_retain, hindsight_recall, hindsight_reflect
  - Holographic tools: fact_store, fact_feedback (available next session after /reset)
  - The hindsight_* tools are ONLY available when provider=hindsight. They will
    error with "No module named hindsight_client" when holographic is active.

---

## Pitfalls

- The pg16 Docker container's default superuser is NOT "postgres" if built with
  POSTGRES_USER=hindsight_user. Connect with: psql -U hindsight_user -d hindsight_db
- Hindsight may run as a different system user (e.g., "dell") than your agent user (root).
  Check process owner with: ps aux | grep hindsight_api
- The hindsight-embed daemon (hindsight-embed -p hermes daemon start) is a SEPARATE process
  from hindsight-api. Both may be running. The embed daemon handles embeddings; the API
  process handles the REST layer.
- If the API is running on a non-standard port, set api_url accordingly in config.json.
- Changes take effect on the NEXT Hermes session (/reset or restart). The provider is
  loaded at session start and not hot-swapped mid-conversation.
- pg0 is an embedded PostgreSQL library used by Hindsight as a fallback when no external
  DB is configured (DEFAULT_DATABASE_URL = "pg0"). The pg16 container bypasses pg0 entirely
  via HINDSIGHT_API_DATABASE_URL.

---

## Teardown / Full Removal

To completely remove all Hindsight configuration and switch back to holographic:

  # 1. Switch provider back to holographic (or any other provider)
  hermes config set memory.provider holographic

  # 2. Delete Hermes-scoped Hindsight config
  rm -rf ~/.hermes/hindsight/

  # 3. Delete legacy Hindsight config dir (also exists alongside the above)
  rm -rf ~/.hindsight/

  # 4. Verify
  hermes memory status
  # Expected: Provider: holographic, holographic <- active

Note: ~/.hindsight/ is a legacy/fallback path that Hindsight creates separately
from ~/.hermes/hindsight/. Both directories must be removed for a clean teardown.
The hindsight plugin remains installed but inactive after these steps.

---

## Useful diagnostic commands

  # Check hindsight-api health
  curl -s http://localhost:8888/health

  # Check which DB the hindsight-api is using
  cat /proc/$(pgrep -f 'hindsight_api.main')/environ | tr '\0' '\n' | grep DATABASE

  # List memory banks in the DB
  docker exec hindsight-db-v16 psql -U hindsight_user -d hindsight_db \
    -c 'SELECT id, name FROM banks;'

  # Count memory units
  docker exec hindsight-db-v16 psql -U hindsight_user -d hindsight_db \
    -c 'SELECT COUNT(*) FROM memory_units;'

  # Hermes memory status
  hermes memory status
