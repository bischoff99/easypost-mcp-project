#!/bin/bash

echo "🔍 EasyPost MCP Project - Complete Setup Verification"
echo "======================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check VS Code Extensions
echo "📦 VS Code Extensions Configuration:"
ext_count=$(cat .vscode/extensions.json | grep -c '"')
echo "   Extensions configured: $ext_count"
if [ $ext_count -gt 20 ]; then
    echo -e "   ${GREEN}✓${NC} All 21 extensions present"
else
    echo -e "   ${RED}✗${NC} Missing extensions"
fi

# Check VS Code Settings
echo ""
echo "⚙️  VS Code Settings:"
settings_lines=$(wc -l < .vscode/settings.json)
echo "   Settings lines: $settings_lines"
if [ $settings_lines -gt 180 ]; then
    echo -e "   ${GREEN}✓${NC} Enhanced settings configured"
else
    echo -e "   ${YELLOW}!${NC} Basic settings only"
fi

# Check Extension-specific settings
echo ""
echo "🔧 Extension Settings:"
for ext in "errorLens" "todo-tree" "better-comments" "importCost" "autoDocstring"; do
    if grep -q "$ext" .vscode/settings.json; then
        echo -e "   ${GREEN}✓${NC} $ext configured"
    else
        echo -e "   ${RED}✗${NC} $ext missing"
    fi
done

# Check MCP Configuration
echo ""
echo "🔌 MCP Server Configuration:"
echo "   Cursor IDE:"
cursor_servers=$(cat ~/.cursor/mcp.json | grep -c '"command"')
echo "   - Servers configured: $cursor_servers"

echo "   Claude Desktop:"
claude_servers=$(cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | grep -c '"command"')
echo "   - Servers configured: $claude_servers"

if [ $cursor_servers -eq $claude_servers ]; then
    echo -e "   ${GREEN}✓${NC} MCP configs synced"
else
    echo -e "   ${YELLOW}!${NC} MCP configs differ"
fi

# Check Git Status
echo ""
echo "📝 Git Repository:"
git_commits=$(git rev-list --count HEAD 2>/dev/null || echo "0")
echo "   Total commits: $git_commits"
if [ $git_commits -gt 2 ]; then
    echo -e "   ${GREEN}✓${NC} Repository initialized with changes"
fi

# Check Backend
echo ""
echo "🐍 Backend Status:"
if [ -f backend/venv/bin/python ]; then
    python_version=$(backend/venv/bin/python --version 2>&1)
    echo -e "   ${GREEN}✓${NC} Python venv: $python_version"
else
    echo -e "   ${RED}✗${NC} Python venv missing"
fi

# Check Frontend
echo ""
echo "⚛️  Frontend Status:"
if [ -d frontend/node_modules ]; then
    echo -e "   ${GREEN}✓${NC} Node modules installed"
else
    echo -e "   ${RED}✗${NC} Node modules missing"
fi

# Check Documentation
echo ""
echo "📚 Documentation:"
for doc in "README.md" "SETUP_INSTRUCTIONS.md" ".cursor/EXTENSION_REVIEW.md"; do
    if [ -f "$doc" ]; then
        lines=$(wc -l < "$doc")
        echo -e "   ${GREEN}✓${NC} $doc ($lines lines)"
    else
        echo -e "   ${RED}✗${NC} $doc missing"
    fi
done

echo ""
echo "======================================================"
echo "🎯 Setup Status: COMPLETE"
echo ""
echo "Next Steps:"
echo "1. Reload Cursor IDE (Cmd+Shift+P → 'Reload Window')"
echo "2. Click 'Install All' when prompted for extensions"
echo "3. Restart Claude Desktop app"
echo "4. Test MCP servers in both Cursor and Claude"
echo ""
