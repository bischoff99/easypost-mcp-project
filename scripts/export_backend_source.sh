#!/usr/bin/env zsh
#
# Export backend source code to timestamped zip archive
# Excludes build artifacts, caches, tests, and dependencies
# Uses zsh for better macOS compatibility
# Outputs to Desktop
#

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
BACKEND_DIR="$REPO_ROOT/apps/backend"
DATE_TAG=$(date +%Y%m%d_%H%M%S)
DESKTOP="$HOME/Desktop"
OUTPUT_ZIP="$DESKTOP/backend_src_$DATE_TAG.zip"

echo "🧩 Exporting backend source from $BACKEND_DIR → $OUTPUT_ZIP"

if [ ! -d "$BACKEND_DIR/src" ]; then
  echo "❌ Error: $BACKEND_DIR/src not found."
  exit 1
fi

cd "$BACKEND_DIR"

zip -r "$OUTPUT_ZIP" src \
  -x "*/__pycache__/*" "*.pyc" "*.pyo" "*.so" "*.dylib" \
     "*/.venv/*" "*/venv/*" "*/tests/*" "*.log" "*.tmp" "*.bak" \
     "*/.pytest_cache/*" "*/.mypy_cache/*" "*/.ruff_cache/*" \
     "*/htmlcov/*" "*/.coverage" "*/dist/*" "*/build/*"

cd "$REPO_ROOT"
echo "✅ Backend archive created at: $OUTPUT_ZIP"
du -h "$OUTPUT_ZIP" | awk '{print "   ", $2, "→", $1}'

