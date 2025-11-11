#!/usr/bin/env bash
# Undo script for project normalization
# Generated automatically - DO NOT EDIT MANUALLY
set -euo pipefail
echo "→ Restoring apps/backend/..."
rsync -a apps/apps/backend/ apps/backend/
rm -rf apps/backend
echo "→ Restoring apps/frontend/..."
rsync -a apps/apps/frontend/ apps/frontend/
rm -rf apps/frontend
echo "→ Restoring Makefile..."
cp "/Users/andrejs/Projects/personal/easypost-mcp-project/.normalize_backup_20251111_050438/Makefile" Makefile
echo "→ Restoring GitHub workflows..."
cp -r "/Users/andrejs/Projects/personal/easypost-mcp-project/.normalize_backup_20251111_050438/.github_workflows"/* .github/workflows/
echo "→ Restoring .gitignore..."
cp "/Users/andrejs/Projects/personal/easypost-mcp-project/.normalize_backup_20251111_050438/.gitignore" .gitignore

echo ""
echo "✅ Undo complete. Original structure restored from backup."
echo "📦 Backup location: /Users/andrejs/Projects/personal/easypost-mcp-project/.normalize_backup_20251111_050438"
echo ""
echo "To permanently remove backup:"
echo "  rm -rf /Users/andrejs/Projects/personal/easypost-mcp-project/.normalize_backup_20251111_050438"
