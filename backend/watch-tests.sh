#!/bin/bash
# Watch tests - automatically rerun on file changes

cd "$(dirname "$0")"
source venv/bin/activate

echo "👀 Watching tests - press Ctrl+C to stop"
echo "Files watched: src/ and tests/"
echo ""

ptw tests/ -- -v --tb=short
