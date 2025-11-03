#!/bin/bash

# Project Structure Verification Script
# Ensures strict structure compliance

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🔍 Verifying Project Structure"
echo "=============================================="
echo ""

ERRORS=0
WARNINGS=0

# 1. Check root markdown file count (max 6: README, QUICK_REFERENCE, BULK_TOOL_USAGE, DEPENDENCY_AUDIT, PROJECT_STRUCTURE, CLEANUP_COMPLETE)
echo "${BLUE}[1/8] Checking root markdown files...${NC}"
ROOT_MD_COUNT=$(ls -1 *.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$ROOT_MD_COUNT" -gt "6" ]; then
    echo "   ${RED}✗ Too many markdown files at root: $ROOT_MD_COUNT (max 6)${NC}"
    echo "   Files:"
    ls -1 *.md | sed 's/^/     - /'
    ERRORS=$((ERRORS + 1))
else
    echo "   ${GREEN}✓ Root markdown count OK: $ROOT_MD_COUNT/6${NC}"
fi

# 2. Check for scripts outside scripts/
echo "${BLUE}[2/8] Checking script organization...${NC}"
MISPLACED_SCRIPTS=$(find . -maxdepth 2 -name "*.sh" -not -path "./scripts/*" -not -path "./backend/venv/*" -not -path "./.git/*" | wc -l | tr -d ' ')
if [ "$MISPLACED_SCRIPTS" -gt "0" ]; then
    echo "   ${RED}✗ Scripts found outside scripts/: $MISPLACED_SCRIPTS${NC}"
    find . -maxdepth 2 -name "*.sh" -not -path "./scripts/*" -not -path "./backend/venv/*" -not -path "./.git/*" | sed 's/^/     - /'
    ERRORS=$((ERRORS + 1))
else
    echo "   ${GREEN}✓ All scripts in scripts/: $(ls scripts/*.sh 2>/dev/null | wc -l | tr -d ' ') files${NC}"
fi

# 3. Check for empty directories
echo "${BLUE}[3/8] Checking for empty directories...${NC}"
EMPTY_DIRS=$(find . -type d -empty -not -path "./backend/venv/*" -not -path "./.git/*" -not -path "./node_modules/*" 2>/dev/null | wc -l | tr -d ' ')
if [ "$EMPTY_DIRS" -gt "0" ]; then
    echo "   ${YELLOW}⚠ Empty directories found: $EMPTY_DIRS${NC}"
    find . -type d -empty -not -path "./backend/venv/*" -not -path "./.git/*" -not -path "./node_modules/*" 2>/dev/null | sed 's/^/     - /'
    WARNINGS=$((WARNINGS + 1))
else
    echo "   ${GREEN}✓ No empty directories${NC}"
fi

# 4. Check backend structure
echo "${BLUE}[4/8] Checking backend structure...${NC}"
BACKEND_ISSUES=0

# Check backend/src/ exists
if [ ! -d "backend/src" ]; then
    echo "   ${RED}✗ backend/src/ missing${NC}"
    BACKEND_ISSUES=$((BACKEND_ISSUES + 1))
fi

# Check backend/tests/ exists
if [ ! -d "backend/tests" ]; then
    echo "   ${RED}✗ backend/tests/ missing${NC}"
    BACKEND_ISSUES=$((BACKEND_ISSUES + 1))
fi

# Check no scripts in backend root
BACKEND_SCRIPTS=$(find backend -maxdepth 1 -name "*.sh" 2>/dev/null | wc -l | tr -d ' ')
if [ "$BACKEND_SCRIPTS" -gt "0" ]; then
    echo "   ${RED}✗ Scripts in backend root: $BACKEND_SCRIPTS (should be in scripts/)${NC}"
    find backend -maxdepth 1 -name "*.sh" 2>/dev/null | sed 's/^/     - /'
    BACKEND_ISSUES=$((BACKEND_ISSUES + 1))
fi

if [ "$BACKEND_ISSUES" -eq "0" ]; then
    echo "   ${GREEN}✓ Backend structure OK${NC}"
else
    ERRORS=$((ERRORS + BACKEND_ISSUES))
fi

# 5. Check frontend structure
echo "${BLUE}[5/8] Checking frontend structure...${NC}"
FRONTEND_ISSUES=0

# Check frontend/src/ exists
if [ ! -d "frontend/src" ]; then
    echo "   ${RED}✗ frontend/src/ missing${NC}"
    FRONTEND_ISSUES=$((FRONTEND_ISSUES + 1))
fi

# Check no scripts in frontend root
FRONTEND_SCRIPTS=$(find frontend -maxdepth 1 -name "*.sh" 2>/dev/null | wc -l | tr -d ' ')
if [ "$FRONTEND_SCRIPTS" -gt "0" ]; then
    echo "   ${RED}✗ Scripts in frontend root: $FRONTEND_SCRIPTS (should be in scripts/)${NC}"
    find frontend -maxdepth 1 -name "*.sh" 2>/dev/null | sed 's/^/     - /'
    FRONTEND_ISSUES=$((FRONTEND_ISSUES + 1))
fi

# Check no unused CSS files
if [ -f "frontend/src/App.css" ]; then
    # Check if it's imported
    if ! grep -r "App.css" frontend/src/*.jsx frontend/src/*.js 2>/dev/null; then
        echo "   ${RED}✗ Unused CSS file: frontend/src/App.css${NC}"
        FRONTEND_ISSUES=$((FRONTEND_ISSUES + 1))
    fi
fi

if [ "$FRONTEND_ISSUES" -eq "0" ]; then
    echo "   ${GREEN}✓ Frontend structure OK${NC}"
else
    ERRORS=$((ERRORS + FRONTEND_ISSUES))
fi

# 6. Check documentation organization
echo "${BLUE}[6/8] Checking documentation...${NC}"
DOCS_ISSUES=0

# Check docs/ directory exists
if [ ! -d "docs" ]; then
    echo "   ${RED}✗ docs/ directory missing${NC}"
    DOCS_ISSUES=$((DOCS_ISSUES + 1))
else
    # Check required subdirectories
    for subdir in setup guides reports architecture; do
        if [ ! -d "docs/$subdir" ]; then
            echo "   ${YELLOW}⚠ docs/$subdir/ missing${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi
    done
fi

if [ "$DOCS_ISSUES" -eq "0" ]; then
    echo "   ${GREEN}✓ Documentation structure OK${NC}"
else
    ERRORS=$((ERRORS + DOCS_ISSUES))
fi

# 7. Check for cache files
echo "${BLUE}[7/8] Checking for cache files...${NC}"
PYCACHE_COUNT=$(find backend/src -type d -name "__pycache__" 2>/dev/null | wc -l | tr -d ' ')
PYC_COUNT=$(find backend/src -type f -name "*.pyc" 2>/dev/null | wc -l | tr -d ' ')

if [ "$PYCACHE_COUNT" -gt "0" ] || [ "$PYC_COUNT" -gt "0" ]; then
    echo "   ${YELLOW}⚠ Cache files found: $PYCACHE_COUNT __pycache__ dirs, $PYC_COUNT .pyc files${NC}"
    echo "   ${BLUE}Run: ./scripts/cleanup-unused-code.sh${NC}"
    WARNINGS=$((WARNINGS + 1))
else
    echo "   ${GREEN}✓ No cache files in source${NC}"
fi

# 8. Check test discovery
echo "${BLUE}[8/8] Checking test discovery...${NC}"
if [ -d "backend/venv" ]; then
    cd backend
    source venv/bin/activate
    TEST_COUNT=$(pytest tests/ --collect-only -q 2>&1 | tail -1 | grep -o '[0-9]\+ test' | grep -o '[0-9]\+' || echo "0")
    if [ "$TEST_COUNT" -gt "0" ]; then
        echo "   ${GREEN}✓ $TEST_COUNT tests discoverable${NC}"
    else
        echo "   ${YELLOW}⚠ No tests found${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
    cd ..
else
    echo "   ${YELLOW}⚠ Backend venv not found, skipping test check${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Summary
echo ""
echo "=============================================="
echo "📊 Verification Summary"
echo "=============================================="

if [ "$ERRORS" -eq "0" ] && [ "$WARNINGS" -eq "0" ]; then
    echo "${GREEN}✅ All checks passed!${NC}"
    echo ""
    echo "Your project structure is strict and compliant! 🎉"
    exit 0
elif [ "$ERRORS" -eq "0" ]; then
    echo "${YELLOW}⚠️  Passed with $WARNINGS warning(s)${NC}"
    echo ""
    echo "Project structure is mostly compliant."
    echo "Address warnings to achieve perfect compliance."
    exit 0
else
    echo "${RED}❌ Failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    echo ""
    echo "Required actions:"
    if [ "$ROOT_MD_COUNT" -gt "6" ]; then
        echo "  • Move extra markdown files from root to docs/"
    fi
    if [ "$MISPLACED_SCRIPTS" -gt "0" ]; then
        echo "  • Move scripts to scripts/ directory"
    fi
    if [ "$BACKEND_SCRIPTS" -gt "0" ] || [ "$FRONTEND_SCRIPTS" -gt "0" ]; then
        echo "  • Consolidate all scripts to scripts/"
    fi
    echo ""
    echo "See PROJECT_STRUCTURE.md for detailed guidelines."
    exit 1
fi

