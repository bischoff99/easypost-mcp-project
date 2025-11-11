#!/bin/bash
# Project Structure Cleanup Script
# Based on: docs/reviews/PROJECT_STRUCTURE_REVIEW_2025.md
# Phase 1: Immediate Cleanup (< 1 hour)

set -e  # Exit on error

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🧹 EasyPost MCP - Project Structure Cleanup"
echo "=========================================="
echo ""

# Backup check
echo "⚠️  IMPORTANT: This script will remove files. Make sure you have a backup!"
echo "   Run: git status to see what would be removed"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "📋 Step 1: Removing cache directories..."
echo "----------------------------------------"

# Remove cache directories (safe - can be regenerated)
if [ -d ".pytest_cache" ]; then
    echo "  Removing .pytest_cache/"
    rm -rf .pytest_cache
fi

if [ -d ".ruff_cache" ]; then
    echo "  Removing .ruff_cache/"
    rm -rf .ruff_cache
fi

if [ -d "apps/backend/.pytest_cache" ]; then
    echo "  Removing apps/backend/.pytest_cache/"
    rm -rf apps/backend/.pytest_cache
fi

if [ -d "apps/backend/.mypy_cache" ]; then
    echo "  Removing apps/backend/.mypy_cache/"
    rm -rf apps/backend/.mypy_cache
fi

if [ -d "apps/backend/__pycache__" ]; then
    echo "  Removing apps/backend/__pycache__/"
    rm -rf apps/backend/__pycache__
fi

echo "  ✅ Cache directories removed"
echo ""

echo "📋 Step 2: Checking node_modules location..."
echo "-------------------------------------------"

if [ -d "node_modules" ]; then
    echo "  ⚠️  Found node_modules at project root"
    echo "  This should only exist in apps/frontend/"
    echo ""
    read -p "Remove root node_modules? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  Removing node_modules/"
        rm -rf node_modules
        echo "  ✅ Removed root node_modules"
        echo "  ℹ️  Run 'cd apps/frontend && npm install' to reinstall in correct location"
    else
        echo "  Skipped"
    fi
else
    echo "  ✅ No node_modules at root (correct)"
fi

echo ""

echo "📋 Step 3: Updating .gitignore..."
echo "---------------------------------"

# Check if patterns are already in .gitignore
if ! grep -q "^__pycache__/" .gitignore 2>/dev/null; then
    echo "  Adding Python cache patterns to .gitignore"
    cat >> .gitignore << 'EOF'

# Python cache directories (added by cleanup script)
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.ruff_cache/
.mypy_cache/
EOF
    echo "  ✅ Updated .gitignore"
else
    echo "  ✅ .gitignore already contains cache patterns"
fi

# Check for node_modules
if ! grep -q "^/node_modules" .gitignore 2>/dev/null; then
    echo "  Adding /node_modules to .gitignore"
    echo "/node_modules" >> .gitignore
    echo "  ✅ Added /node_modules pattern"
else
    echo "  ✅ .gitignore already contains /node_modules"
fi

echo ""

echo "📋 Step 4: Summary..."
echo "--------------------"
echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Actions taken:"
echo "  - Removed cache directories (.pytest_cache, .ruff_cache, etc.)"
echo "  - Checked node_modules location"
echo "  - Updated .gitignore with cache patterns"
echo ""
echo "📝 Next steps:"
echo "  1. Run: git status"
echo "  2. Run: git add .gitignore"
echo "  3. Run: git commit -m 'chore: cleanup project structure (remove caches, update gitignore)'"
echo "  4. Optional: cd apps/frontend && npm install (if node_modules was removed)"
echo ""
echo "📚 For more details, see:"
echo "   docs/reviews/PROJECT_STRUCTURE_REVIEW_2025.md"
echo ""

