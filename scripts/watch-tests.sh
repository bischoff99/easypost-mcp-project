#!/usr/bin/env zsh
# Watch tests - automatically rerun on file changes

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

echo "👀 Watching tests - press Ctrl+C to stop"
echo "Files watched: src/ and tests/"
echo ""

ptw tests/ -- -v --tb=short
