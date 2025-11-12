#!/usr/bin/env zsh
# Watch tests - automatically rerun on file changes

<<<<<<< HEAD
set -euo pipefail

# Get project root (parent of scripts directory)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
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
||||||| 7a576da
cd "$(dirname "$0")"
source venv/bin/activate
=======
set -euo pipefail

# Cleanup handler
cleanup() {
    echo ""
    echo "Stopping test watcher..."
    exit 0
}

trap cleanup EXIT INT TERM

cd "$(dirname "$0")"
source venv/bin/activate
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8

echo "👀 Watching tests - press Ctrl+C to stop"
echo "Files watched: src/ and tests/"
echo ""

ptw tests/ -- -v --tb=short
