#!/bin/bash
# Comprehensive Cleanup Script
# Removes duplicates and archives old files

set -e

PROJECT_ROOT="/Users/andrejs/Developer/github/andrejs/easypost-mcp-project"
ARCHIVE_DIR="$PROJECT_ROOT/docs/archive/cleanup-2025-11-10"

echo "🧹 Starting comprehensive cleanup..."

# Create archive directory
mkdir -p "$ARCHIVE_DIR/manual-tests"
mkdir -p "$ARCHIVE_DIR/test-responses"
mkdir -p "$ARCHIVE_DIR/duplicates"

# Phase 1: Remove duplicate documentation
echo "📄 Phase 1: Removing duplicate documentation..."
if [ -f "$PROJECT_ROOT/docs/reviews/BULK_RATES_DATA.md" ]; then
    mv "$PROJECT_ROOT/docs/reviews/BULK_RATES_DATA.md" "$ARCHIVE_DIR/duplicates/"
    echo "  ✓ Archived duplicate BULK_RATES_DATA.md"
fi

if [ -f "$PROJECT_ROOT/docs/reviews/archived-reviews/CLAUDE.md" ]; then
    mv "$PROJECT_ROOT/docs/reviews/archived-reviews/CLAUDE.md" "$ARCHIVE_DIR/duplicates/"
    echo "  ✓ Archived duplicate CLAUDE.md"
fi

# Phase 2: Archive old test files
echo "🧪 Phase 2: Archiving old test files..."
if [ -d "$PROJECT_ROOT/apps/backend/tests/manual" ]; then
    mv "$PROJECT_ROOT/apps/backend/tests/manual"/* "$ARCHIVE_DIR/manual-tests/" 2>/dev/null || true
    echo "  ✓ Archived manual test files"
fi

# Phase 3: Archive old captured responses (>7 days)
echo "📦 Phase 3: Archiving old test responses..."
find "$PROJECT_ROOT/apps/backend/tests/captured_responses" -name "*.json" -mtime +7 -exec mv {} "$ARCHIVE_DIR/test-responses/" \; 2>/dev/null || true
echo "  ✓ Archived old captured responses"

# Phase 4: Create cleanup log
cat > "$ARCHIVE_DIR/CLEANUP_LOG.md" << EOF
# Cleanup Log - November 10, 2025

## Files Archived

### Duplicates
- docs/reviews/BULK_RATES_DATA.md
- docs/reviews/archived-reviews/CLAUDE.md

### Manual Tests
- apps/backend/tests/manual/* (all files)

### Old Test Responses
- apps/backend/tests/captured_responses/*.json (>7 days old)

## Archive Location
\`docs/archive/cleanup-2025-11-10/\`

## Recovery
If needed, files can be restored from archive directory.
EOF

echo ""
echo "✅ Cleanup complete!"
echo "📁 Archive location: $ARCHIVE_DIR"
echo "📋 See CLEANUP_LOG.md for details"
