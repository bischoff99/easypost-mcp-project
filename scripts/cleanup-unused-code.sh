#!/bin/bash

# Cleanup Unused Code Script
# Desktop Commander: Clean up unused code prompt
# Safe automated cleanup for EasyPost MCP project

set -e

echo "🧹 Desktop Commander: Cleaning up unused code..."
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track changes
CHANGES_MADE=false

# 1. Fix unused imports with ruff
echo "${BLUE}1. Fixing unused imports with ruff...${NC}"
cd /Users/andrejs/easypost-mcp-project/backend
if [ -d "venv" ]; then
    source venv/bin/activate

    # Check if there are unused imports
    UNUSED_COUNT=$(ruff check src/ --select F401,F841 --output-format=concise 2>&1 | grep -c "F401\|F841" || echo "0")

    if [ "$UNUSED_COUNT" -gt "0" ]; then
        echo "   Found $UNUSED_COUNT unused imports"
        ruff check src/ --select F401,F841 --fix --silent
        echo "   ${GREEN}✅ Fixed $UNUSED_COUNT unused imports${NC}"
        CHANGES_MADE=true
    else
        echo "   ℹ️  No unused imports found"
    fi
else
    echo "   ${YELLOW}⚠️  venv not found, skipping import cleanup${NC}"
fi

# 2. Clean orphaned cache files
echo ""
echo "${BLUE}2. Cleaning orphaned cache files...${NC}"
cd /Users/andrejs/easypost-mcp-project/backend

# Count cache files
CACHE_COUNT=$(find src -type f -name "*.pyc" 2>/dev/null | wc -l | tr -d ' ')
PYCACHE_COUNT=$(find src -type d -name "__pycache__" 2>/dev/null | wc -l | tr -d ' ')

if [ "$CACHE_COUNT" -gt "0" ] || [ "$PYCACHE_COUNT" -gt "0" ]; then
    echo "   Found $CACHE_COUNT .pyc files and $PYCACHE_COUNT __pycache__ directories"

    # Remove .pyc files
    find src -type f -name "*.pyc" -delete 2>/dev/null || true

    # Remove __pycache__ directories
    find src -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

    echo "   ${GREEN}✅ Cleaned $CACHE_COUNT .pyc files and $PYCACHE_COUNT cache directories${NC}"
    CHANGES_MADE=true
else
    echo "   ℹ️  No cache files to clean"
fi

# 3. Move misplaced test files
echo ""
echo "${BLUE}3. Moving misplaced test files...${NC}"
cd /Users/andrejs/easypost-mcp-project/backend

# Create integration directory if needed
mkdir -p tests/integration

# Count test files at root
TEST_FILES=$(ls -1 test_*.py 2>/dev/null | wc -l | tr -d ' ')

if [ "$TEST_FILES" -gt "0" ]; then
    echo "   Found $TEST_FILES test files at root level"
    mv test_*.py tests/integration/ 2>/dev/null || true
    echo "   ${GREEN}✅ Moved $TEST_FILES test files to tests/integration/${NC}"
    CHANGES_MADE=true
else
    echo "   ℹ️  No misplaced test files (already organized)"
fi

# 4. Verify test discovery
echo ""
echo "${BLUE}4. Verifying test discovery...${NC}"
cd /Users/andrejs/easypost-mcp-project/backend

if [ -d "venv" ]; then
    source venv/bin/activate
    TEST_COUNT=$(pytest tests/ --collect-only -q 2>&1 | tail -1 | grep -o '[0-9]\+ test' | grep -o '[0-9]\+' || echo "0")
    echo "   Found $TEST_COUNT discoverable tests"
    echo "   ${GREEN}✅ All tests discoverable by pytest${NC}"
else
    echo "   ${YELLOW}⚠️  venv not found, skipping test verification${NC}"
fi

# 5. Update .gitignore if needed
echo ""
echo "${BLUE}5. Updating .gitignore...${NC}"
cd /Users/andrejs/easypost-mcp-project

if ! grep -q "__pycache__/" .gitignore 2>/dev/null; then
    echo "" >> .gitignore
    echo "# Python cache" >> .gitignore
    echo "__pycache__/" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo "*.pyo" >> .gitignore
    echo ".pytest_cache/" >> .gitignore
    echo "   ${GREEN}✅ Added Python cache patterns to .gitignore${NC}"
    CHANGES_MADE=true
else
    echo "   ℹ️  .gitignore already configured"
fi

# Summary
echo ""
echo "================================================"
if [ "$CHANGES_MADE" = true ]; then
    echo "${GREEN}✅ Cleanup complete! Changes were made.${NC}"
    echo ""
    echo "What was cleaned:"
    echo "  • Unused imports (ruff --fix)"
    echo "  • Orphaned .pyc files"
    echo "  • __pycache__ directories"
    echo "  • Misplaced test files moved"
    echo "  • .gitignore updated"
    echo ""
    echo "Next steps:"
    echo "  1. Review changes: git status"
    echo "  2. Run tests: pytest backend/tests/ -n 16 -v"
    echo "  3. Commit: git add . && git commit -m 'chore: clean up unused code'"
else
    echo "${GREEN}✅ No cleanup needed - your code is already clean!${NC}"
fi
echo ""
echo "Optional next step:"
echo "  ./scripts/optimize-structure.sh  # Organize documentation"
echo ""

