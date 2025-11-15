#!/usr/bin/env zsh
# Watch tests - automatically rerun on file changes

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/venv"

cleanup() {
    echo ""
    echo "Stopping test watcher..."
    exit 0
}

trap cleanup EXIT INT TERM

cd "$PROJECT_ROOT"

if [ -d "${VENV_DIR}" ]; then
    source "${VENV_DIR}/bin/activate"
else
    echo "❌ Error: Virtual environment not found. Run 'make setup' first."
    exit 1
fi

echo "👀 Watching tests - press Ctrl+C to stop"
echo "Files watched: src/ and tests/"
echo ""

ptw tests/ -- -v --tb=short
