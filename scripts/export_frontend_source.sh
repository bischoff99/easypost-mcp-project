#!/usr/bin/env zsh
#
# Export frontend source code to timestamped zip archive
# Excludes build artifacts, caches, and dependencies
# Uses zsh for better macOS compatibility
# Outputs to Desktop
#

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
FRONTEND_DIR="$REPO_ROOT/apps/frontend"
DATE_TAG=$(date +%Y%m%d_%H%M%S)
DESKTOP="$HOME/Desktop"
OUTPUT_ZIP="$DESKTOP/frontend_src_$DATE_TAG.zip"

echo "🧩 Exporting frontend source from $FRONTEND_DIR → $OUTPUT_ZIP"

if [ ! -d "$FRONTEND_DIR/src" ]; then
  echo "❌ Error: $FRONTEND_DIR/src not found."
  exit 1
fi

cd "$FRONTEND_DIR"

zip -r "$OUTPUT_ZIP" src \
  -x "*/node_modules/*" "*.log" "*.tmp" "*.bak" "dist/*" "build/*" "*.next/*" \
     "*/.vite/*" "*/.svelte-kit/*" "*/.nuxt/*" "*/.cache/*" \
     "*/coverage/*" "*.test.js" "*.test.jsx" "*.spec.js" "*.spec.jsx"

cd "$REPO_ROOT"
echo "✅ Frontend archive created at: $OUTPUT_ZIP"
du -h "$OUTPUT_ZIP" | awk '{print "   ", $2, "→", $1}'

