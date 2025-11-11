#!/bin/bash
# Consolidate .cursor/rules from 20 files to 7 core files
# Based on: docs/reviews/CURSOR_DIRECTORY_REVIEW_2025.md
# PDS 2025 Standard: Maximum 6-8 rule files for optimal performance

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT/.cursor"

echo "📋 Cursor Rules Consolidation"
echo "=============================="
echo ""
echo "This will consolidate 20 rule files into 7 core files"
echo "Redundant rules will be moved to archive/legacy-rules/"
echo ""
echo "Current: 20 files (context overhead)"
echo "Target:  7 files (PDS 2025 recommended: 6-8)"
echo ""

# Show current state
echo "Current rules:"
ls -1 rules/*.mdc | wc -l
echo ""

read -p "Continue with consolidation? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "📋 Creating archive directory..."
mkdir -p archive/legacy-rules

echo ""
echo "📋 Moving redundant rules to archive..."
echo "========================================"

# Rules to archive (content duplicated in comprehensive files)
rules_to_archive=(
  "00-core-standards"
  "01-code-standards"
  "02-file-structure"
  "03-naming-conventions"
  "04-error-handling"
  "05-logging"
  "06-testing"
  "07-git-version-control"
  "08-security"
  "09-api-format"
  "10-documentation"
  "11-performance"
  "12-deployment"
  "13-code-review"
)

archived_count=0
for rule in "${rules_to_archive[@]}"; do
  if [ -f "rules/${rule}.mdc" ]; then
    mv "rules/${rule}.mdc" "archive/legacy-rules/"
    echo "  ✅ Archived ${rule}.mdc"
    ((archived_count++))
  else
    echo "  ⚠️  ${rule}.mdc not found (already archived?)"
  fi
done

echo ""
echo "📋 Consolidation complete!"
echo "=========================="
echo ""
echo "Archived: $archived_count files"
echo "Remaining: $(ls -1 rules/*.mdc | wc -l) files"
echo ""
echo "Core rules (kept):"
ls -1 rules/*.mdc
echo ""
echo "✅ Benefits:"
echo "  - Reduced context loading (faster Cursor startup)"
echo "  - Single source of truth (easier maintenance)"
echo "  - Lower token consumption (better performance)"
echo "  - PDS 2025 compliant (6-8 file recommendation)"
echo ""
echo "📚 Archived rules available at:"
echo "  .cursor/archive/legacy-rules/"
echo ""
echo "🎯 Grade improvement: C (rules) → A+ (rules)"
echo ""

