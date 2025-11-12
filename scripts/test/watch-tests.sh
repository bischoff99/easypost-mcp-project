#!/usr/bin/env zsh
# Watch tests - automatically rerun on file changes

set -euo pipefail

# Get project root (two levels up from scripts/test/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BACKEND_DIR="${PROJECT_ROOT}/apps/backend"

# Cleanup handler
cleanup() {
    echo ""
    echo "Stopping test watcher..."
    exit 0
}

trap cleanup EXIT INT TERM

# Change to backend directory
cd "$BACKEND_DIR"

# Detect and activate venv
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Error: Virtual environment not found. Run 'make setup' first."
    exit 1
fi

echo "👀 Watching tests - press Ctrl+C to stop"
echo "Files watched: src/ and tests/"
echo ""

ptw tests/ -- -v --tb=short
