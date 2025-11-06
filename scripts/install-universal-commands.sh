#!/bin/bash
# Universal Slash Commands Installer
# Copy this system to ANY project

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

TARGET_DIR=${1:-.}

echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Universal Slash Commands Installer      ║${NC}"
echo -e "${BLUE}║  M3 Max Optimized Development System     ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}Installing to: ${TARGET_DIR}${NC}"
echo ""

# Create target directory if doesn't exist
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# Copy core files
echo -e "${GREEN}[1/5] Copying configuration files...${NC}"
cp /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/.dev-config.template.json ./.dev-config.json
cp /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/.cursorrules ./
cp /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/Makefile ./

# Copy AI templates
echo -e "${GREEN}[2/5] Copying AI templates...${NC}"
mkdir -p .ai-templates
cp -r /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/.ai-templates/* .ai-templates/ 2>/dev/null || true

# Copy VS Code config
echo -e "${GREEN}[3/5] Copying VS Code configuration...${NC}"
mkdir -p .vscode
cp /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/.vscode/snippets.code-snippets .vscode/ 2>/dev/null || true

# Copy scripts
echo -e "${GREEN}[4/5] Copying utility scripts...${NC}"
mkdir -p scripts
cp /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/scripts/benchmark.sh scripts/ 2>/dev/null || true

# Copy pre-commit config
echo -e "${GREEN}[5/5] Copying development tools...${NC}"
cp /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/.pre-commit-config.yaml ./ 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ Universal command system installed!${NC}"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo ""
echo "1. Edit .dev-config.json with your project details"
echo "   ${BLUE}nano .dev-config.json${NC}"
echo ""
echo "2. Test the slash commands in Cursor:"
echo "   ${BLUE}/api /users POST${NC}"
echo "   ${BLUE}/component UserCard${NC}"
echo "   ${BLUE}/test myfile.py${NC}"
echo ""
echo "3. Use Makefile commands:"
echo "   ${BLUE}make help${NC}"
echo "   ${BLUE}make dev${NC}"
echo ""
echo "4. Check documentation:"
echo "   ${BLUE}cat UNIVERSAL_COMMANDS.md${NC}"
echo ""
echo -e "${YELLOW}💡 Pro Tip:${NC}"
echo "Create an alias in ~/.zshrc for quick installation:"
echo "  ${BLUE}alias dev-init='bash /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/install-universal-commands.sh'${NC}"
echo ""
echo "Then in ANY project directory:"
echo "  ${BLUE}dev-init${NC}"
echo ""
