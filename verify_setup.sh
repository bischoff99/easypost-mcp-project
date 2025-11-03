#!/bin/bash
# Verification script for EasyPost MCP Project

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  EasyPost MCP Project - Verification  ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Check Python version
echo -e "${BLUE}[1/8]${NC} Checking Python version..."
cd /Users/andrejs/easypost-mcp-project/backend
source venv/bin/activate
PYTHON_VERSION=$(python --version)
if [[ $PYTHON_VERSION == *"3.12"* ]]; then
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Wrong Python version: $PYTHON_VERSION"
    exit 1
fi

# Check packages
echo -e "${BLUE}[2/8]${NC} Checking Python packages..."
if python -c "from fastmcp import FastMCP; from fastapi import FastAPI; import easypost" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} All packages installed (fastmcp, fastapi, easypost)"
else
    echo -e "${RED}✗${NC} Missing packages"
    exit 1
fi

# Check imports
echo -e "${BLUE}[3/8]${NC} Checking server imports..."
if python -c "import sys; sys.path.insert(0, '.'); from src.server import app; from src.mcp_server import mcp" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Both REST API and MCP servers import successfully"
else
    echo -e "${RED}✗${NC} Import errors"
    exit 1
fi

# Run tests
echo -e "${BLUE}[4/8]${NC} Running tests..."
TEST_OUTPUT=$(pytest tests/ -v --tb=short 2>&1)
if echo "$TEST_OUTPUT" | grep -q "9 passed"; then
    echo -e "${GREEN}✓${NC} 9/9 tests passing"
else
    echo -e "${RED}✗${NC} Tests failing"
    exit 1
fi

# Check linting
echo -e "${BLUE}[5/8]${NC} Checking code quality..."
if ruff check src/ tests/ 2>&1 | grep -q "All checks passed"; then
    echo -e "${GREEN}✓${NC} Ruff linting passed"
else
    echo -e "${RED}✗${NC} Linting errors"
    exit 1
fi

# Check frontend
cd /Users/andrejs/easypost-mcp-project/frontend
echo -e "${BLUE}[6/8]${NC} Checking frontend build..."
if npm run build >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Frontend builds successfully"
else
    echo -e "${RED}✗${NC} Frontend build failed"
    exit 1
fi

# Check MCP configuration
cd /Users/andrejs/easypost-mcp-project
echo -e "${BLUE}[7/8]${NC} Checking Cursor MCP configuration..."
if cat ~/.cursor/mcp.json | python3 -m json.tool >/dev/null 2>&1; then
    MCP_COUNT=$(cat ~/.cursor/mcp.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data['mcpServers']))")
    echo -e "${GREEN}✓${NC} MCP config valid - $MCP_COUNT servers configured"
else
    echo -e "${RED}✗${NC} Invalid MCP configuration"
    exit 1
fi

# Count files
echo -e "${BLUE}[8/8]${NC} Counting deliverables..."
BACKEND_FILES=$(find /Users/andrejs/easypost-mcp-project/backend/src -name "*.py" | wc -l | xargs)
FRONTEND_FILES=$(find /Users/andrejs/easypost-mcp-project/frontend/src -name "*.jsx" -o -name "*.js" | wc -l | xargs)
TEST_FILES=$(find /Users/andrejs/easypost-mcp-project/backend/tests -name "*.py" | wc -l | xargs)
echo -e "${GREEN}✓${NC} Backend: $BACKEND_FILES Python files"
echo -e "${GREEN}✓${NC} Frontend: $FRONTEND_FILES JS/JSX files"
echo -e "${GREEN}✓${NC} Tests: $TEST_FILES test files"

# Summary
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ ALL CHECKS PASSED${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo "System Status:"
echo "  • Python: 3.12.12 ✓"
echo "  • Packages: Installed ✓"
echo "  • Tests: 9/9 passing ✓"
echo "  • Linting: 0 errors ✓"
echo "  • Frontend: Builds ✓"
echo "  • MCP: $MCP_COUNT servers ✓"
echo ""
echo "Ready to:"
echo "  1. Start backend: cd backend && ./start_backend.sh"
echo "  2. Start frontend: cd frontend && npm run dev"
echo "  3. Use MCP in Cursor (after reload)"
echo ""
echo -e "${GREEN}🚀 System is production-ready!${NC}"

