#!/bin/bash
# Research Pipeline - Web Frontend Launcher
# Usage: bash run_web.sh [--port 8501]
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT="${1:-8501}"

echo "[1/2] Checking dependencies..."
pip install -q streamlit python-dotenv pyyaml 2>/dev/null || pip install streamlit python-dotenv pyyaml

echo "[2/2] Launching Web UI..."
echo "  Open: http://localhost:${PORT}"
exec streamlit run web_app.py \
    --server.port "$PORT" \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false \
    --theme.primaryColor "#6366f1" \
    --theme.backgroundColor "#0f172a" \
    --theme.secondaryBackgroundColor "#1e293b" \
    --theme.textColor "#f8fafc"
