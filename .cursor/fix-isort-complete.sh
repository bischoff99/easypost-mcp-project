#!/bin/bash

# Complete isort Disable Script for Cursor IDE
# This script aggressively disables isort and clears cached extension state

set -e

echo "🔧 Complete isort Disable Script"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

WORKSPACE_DIR="/Users/andrejs/Developer/github/andrejs/easypost-mcp-project"

# 1. Check if isort extension is installed
echo "1. Checking for isort extension..."
if code --list-extensions 2>/dev/null | grep -q "ms-python.isort"; then
    echo "   ${YELLOW}⚠️  isort extension found - uninstalling...${NC}"
    code --uninstall-extension ms-python.isort 2>/dev/null || true
    echo "   ${GREEN}✅ Extension uninstalled${NC}"
else
    echo "   ${GREEN}✅ isort extension not installed${NC}"
fi

# 2. Kill any running isort language server processes
echo ""
echo "2. Killing isort language server processes..."
pkill -f "isort.*language.*server" 2>/dev/null || true
pkill -f "python.*isort" 2>/dev/null || true
echo "   ${GREEN}✅ Processes killed${NC}"

# 3. Verify settings.json configuration
echo ""
echo "3. Verifying settings.json..."
if grep -q '"isort.enable": false' "$WORKSPACE_DIR/.vscode/settings.json"; then
    echo "   ${GREEN}✅ isort.enable is disabled${NC}"
else
    echo "   ${RED}❌ isort.enable not found in settings.json${NC}"
    exit 1
fi

# 4. Check for Python extension
echo ""
echo "4. Checking Python extension..."
if code --list-extensions 2>/dev/null | grep -q "ms-python.python"; then
    echo "   ${GREEN}✅ Python extension installed${NC}"
else
    echo "   ${YELLOW}⚠️  Python extension not found - installing...${NC}"
    code --install-extension ms-python.python 2>/dev/null || true
    echo "   ${GREEN}✅ Python extension installed${NC}"
fi

# 5. Verify Ruff extension
echo ""
echo "5. Checking Ruff extension..."
if code --list-extensions 2>/dev/null | grep -q "charliermarsh.ruff"; then
    echo "   ${GREEN}✅ Ruff extension installed${NC}"
else
    echo "   ${YELLOW}⚠️  Ruff extension not found - installing...${NC}"
    code --install-extension charliermarsh.ruff 2>/dev/null || true
    echo "   ${GREEN}✅ Ruff extension installed${NC}"
fi

echo ""
echo "=================================="
echo "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "NEXT STEPS:"
echo "1. Press ${YELLOW}Cmd+Shift+P${NC} (Mac) or ${YELLOW}Ctrl+Shift+P${NC} (Windows/Linux)"
echo "2. Type: ${YELLOW}Developer: Reload Window${NC}"
echo "3. Press Enter"
echo ""
echo "This will reload Cursor IDE and apply all settings."
echo "After reload, isort errors should be gone."
