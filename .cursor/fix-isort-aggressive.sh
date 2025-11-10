#!/bin/bash
# Aggressive isort removal script for Cursor IDE
# This script removes isort completely and forces Cursor to use Ruff only

set -e

echo "🔧 Aggressive isort Removal Script"
echo "===================================="
echo ""

# 1. Check and kill all Python language server processes
echo "1. Killing Python language server processes..."
pkill -f "python.*language.*server" 2>/dev/null || true
pkill -f "pylance" 2>/dev/null || true
pkill -f "pyright" 2>/dev/null || true
pkill -f "isort" 2>/dev/null || true
sleep 1
echo "   ✅ Processes killed"
echo ""

# 2. Check for isort in virtual environment
echo "2. Checking for isort in Python environment..."
if [ -f "backend/venv/bin/python" ]; then
    if backend/venv/bin/python -c "import isort" 2>/dev/null; then
        echo "   ⚠️  isort found in venv - removing..."
        backend/venv/bin/pip uninstall -y isort 2>/dev/null || true
        echo "   ✅ isort removed from venv"
    else
        echo "   ✅ isort not in venv"
    fi
else
    echo "   ⚠️  venv not found, skipping"
fi
echo ""

# 3. Verify settings.json configuration
echo "3. Verifying settings.json..."
if grep -q '"isort.enable": false' .vscode/settings.json 2>/dev/null; then
    echo "   ✅ isort.enable is disabled"
else
    echo "   ❌ isort.enable not found or not disabled"
fi

if grep -q '"python.sortImports.provider": "none"' .vscode/settings.json 2>/dev/null; then
    echo "   ✅ Python sort imports disabled"
else
    echo "   ❌ Python sort imports not disabled"
fi

if grep -q '"ruff.organizeImports": true' .vscode/settings.json 2>/dev/null; then
    echo "   ✅ Ruff organize imports enabled"
else
    echo "   ❌ Ruff organize imports not enabled"
fi
echo ""

# 4. Clear Cursor cache directories
echo "4. Clearing Cursor cache..."
CURSOR_CACHE="$HOME/Library/Application Support/Cursor/CachedExtensions"
CURSOR_WORKSPACE="$HOME/Library/Application Support/Cursor/User/workspaceStorage"
CURSOR_STATE="$HOME/Library/Application Support/Cursor/User/globalStorage"

if [ -d "$CURSOR_CACHE" ]; then
    echo "   Clearing extension cache..."
    rm -rf "$CURSOR_CACHE"/* 2>/dev/null || true
fi

if [ -d "$CURSOR_WORKSPACE" ]; then
    echo "   Clearing workspace storage..."
    find "$CURSOR_WORKSPACE" -name "*isort*" -type d -exec rm -rf {} + 2>/dev/null || true
fi

if [ -d "$CURSOR_STATE" ]; then
    echo "   Clearing global state..."
    find "$CURSOR_STATE" -name "*isort*" -type d -exec rm -rf {} + 2>/dev/null || true
fi
echo "   ✅ Cache cleared"
echo ""

# 5. Check extension installation
echo "5. Checking extensions..."
if command -v code >/dev/null 2>&1; then
    if code --list-extensions 2>/dev/null | grep -qi isort; then
        echo "   ⚠️  isort extension found - attempting to uninstall..."
        code --uninstall-extension ms-python.isort 2>/dev/null || true
        echo "   ✅ Extension uninstall attempted"
    else
        echo "   ✅ No isort extension installed"
    fi
else
    echo "   ⚠️  'code' command not found, skipping extension check"
fi
echo ""

# 6. Verify Ruff is installed
echo "6. Verifying Ruff setup..."
if [ -f "backend/venv/bin/ruff" ]; then
    echo "   ✅ Ruff installed in venv"
    backend/venv/bin/ruff --version 2>/dev/null || echo "   ⚠️  Ruff not working"
else
    echo "   ⚠️  Ruff not found in venv"
fi

if command -v code >/dev/null 2>&1; then
    if code --list-extensions 2>/dev/null | grep -qi "charliermarsh.ruff"; then
        echo "   ✅ Ruff extension installed"
    else
        echo "   ⚠️  Ruff extension not installed"
    fi
fi
echo ""

echo "===================================="
echo "✅ Aggressive cleanup complete!"
echo ""
echo "CRITICAL NEXT STEPS:"
echo "1. Close Cursor IDE completely (Cmd+Q)"
echo "2. Wait 5 seconds"
echo "3. Reopen Cursor IDE"
echo "4. Open this workspace"
echo "5. If errors persist, check Output panel:"
echo "   View → Output → Select 'Python' or 'isort'"
echo "   Copy the exact error message"
echo ""
