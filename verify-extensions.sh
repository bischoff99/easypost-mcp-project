#!/bin/bash
# Verify VS Code Extensions Integration

set -e

echo "🔍 VS Code Extensions Integration Verification"
echo "=============================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        return 0
    else
        echo -e "${RED}✗${NC} $2 (Missing: $1)"
        return 1
    fi
}

check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $3"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $3 (Not found in $1)"
        return 1
    fi
}

echo "📁 Configuration Files"
echo "----------------------"
check_file ".vscode/settings.json" "VS Code settings"
check_file ".vscode/extensions.json" "Extension recommendations"
check_file ".vscode/launch.json" "Debug configurations"
check_file ".vscode/tasks.json" "Task definitions"
check_file ".vscode/snippets.code-snippets" "Custom snippets"
check_file ".prettierrc" "Prettier config"
check_file ".eslintrc.json" "ESLint config"
echo ""

echo "🐍 Python Extension Integration"
echo "--------------------------------"
check_content ".vscode/settings.json" "ms-python.black-formatter" "Black formatter configured"
check_content ".vscode/settings.json" "ruffEnabled" "Ruff linter enabled"
check_content ".vscode/settings.json" "pytestEnabled" "Pytest configured"
check_content ".vscode/launch.json" "Python: FastMCP Server" "Server debug config"
check_content ".vscode/launch.json" "Python: Tests" "Test debug config"
check_content ".vscode/tasks.json" "Backend: Watch Tests" "Watch tests task"
check_content ".vscode/snippets.code-snippets" "mcp-tool" "MCP tool snippet"
echo ""

echo "⚛️  React Extension Integration"
echo "--------------------------------"
check_content ".vscode/settings.json" "prettier-vscode" "Prettier configured"
check_content ".vscode/settings.json" "eslint" "ESLint configured"
check_content ".vscode/tasks.json" "Frontend: Dev Server" "Frontend dev task"
check_content ".vscode/snippets.code-snippets" "rfc-full" "React component snippet"
check_content ".prettierrc" "singleQuote" "Prettier rules"
check_content ".eslintrc.json" "react" "ESLint React rules"
echo ""

echo "🔧 Productivity Extensions"
echo "---------------------------"
check_content ".vscode/settings.json" "errorLens" "Error Lens configured"
check_content ".vscode/settings.json" "todo-tree" "Todo Tree configured"
check_content ".vscode/settings.json" "better-comments" "Better Comments configured"
check_content ".vscode/settings.json" "cSpell" "Spell checker configured"
check_content ".vscode/settings.json" "importCost" "Import Cost configured"
check_content ".vscode/settings.json" "autoDocstring" "Auto Docstring configured"
echo ""

echo "🎯 VS Code Tasks"
echo "----------------"
check_content ".vscode/tasks.json" "Backend: Watch Tests" "Watch tests"
check_content ".vscode/tasks.json" "Backend: Run Tests Once" "Run tests once"
check_content ".vscode/tasks.json" "Backend: Start Server" "Start backend server"
check_content ".vscode/tasks.json" "Frontend: Dev Server" "Start frontend server"
check_content ".vscode/tasks.json" "Format: Python" "Format Python"
check_content ".vscode/tasks.json" "Lint: Python" "Lint Python"
check_content ".vscode/tasks.json" "Lint: Frontend" "Lint Frontend"
check_content ".vscode/tasks.json" "Start All Dev Servers" "Start all servers"
echo ""

echo "📝 Custom Snippets"
echo "------------------"
check_content ".vscode/snippets.code-snippets" "mcp-tool" "FastMCP tool snippet"
check_content ".vscode/snippets.code-snippets" "fastapi-endpoint" "FastAPI endpoint snippet"
check_content ".vscode/snippets.code-snippets" "rfc-full" "React component snippet"
check_content ".vscode/snippets.code-snippets" "pytest-func" "Pytest function snippet"
echo ""

echo "🐍 Python Environment"
echo "---------------------"
if [ -d "backend/venv" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment exists"
    if [ -f "backend/venv/bin/python" ]; then
        PYTHON_VERSION=$(backend/venv/bin/python --version 2>&1)
        echo -e "${GREEN}✓${NC} Python interpreter: $PYTHON_VERSION"
    fi
    
    if backend/venv/bin/python -c "import pytest" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Pytest installed"
    else
        echo -e "${RED}✗${NC} Pytest not found"
    fi
    
    if backend/venv/bin/python -c "import pytest_watch" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Pytest-watch installed"
    else
        echo -e "${YELLOW}⚠${NC} Pytest-watch not found (run: pip install pytest-watch)"
    fi
    
    if backend/venv/bin/python -c "import black" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Black installed"
    else
        echo -e "${RED}✗${NC} Black not found"
    fi
    
    if backend/venv/bin/python -c "import ruff" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Ruff installed"
    else
        echo -e "${YELLOW}⚠${NC} Ruff not found"
    fi
else
    echo -e "${RED}✗${NC} Virtual environment not found"
fi
echo ""

echo "📦 Frontend Dependencies"
echo "------------------------"
if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✓${NC} Node modules installed"
    
    if [ -d "frontend/node_modules/eslint" ]; then
        echo -e "${GREEN}✓${NC} ESLint installed"
    else
        echo -e "${YELLOW}⚠${NC} ESLint not found (run: npm install)"
    fi
    
    if [ -d "frontend/node_modules/prettier" ]; then
        echo -e "${GREEN}✓${NC} Prettier installed"
    else
        echo -e "${YELLOW}⚠${NC} Prettier not found (run: npm install)"
    fi
    
    if [ -d "frontend/node_modules/vitest" ]; then
        echo -e "${GREEN}✓${NC} Vitest installed"
    else
        echo -e "${YELLOW}⚠${NC} Vitest not found (run: npm install)"
    fi
else
    echo -e "${RED}✗${NC} Node modules not found (run: cd frontend && npm install)"
fi
echo ""

echo "📚 Documentation"
echo "----------------"
check_file ".cursor/EXTENSION_INTEGRATION.md" "Extension integration guide"
check_file ".cursor/PROJECT_PROGRESS.md" "Project progress"
check_file ".cursor/TEST_REPORT.md" "Test report"
check_file "backend/watch-tests.sh" "Watch tests script"
check_file "start-dev.sh" "Start dev script"
check_file "quick-test.sh" "Quick test script"
echo ""

echo "=============================================="
echo "✅ Integration verification complete!"
echo ""
echo "📋 Next Steps:"
echo "  1. Reload Cursor: Cmd+Shift+P → 'Reload Window'"
echo "  2. Select Python interpreter: Cmd+Shift+P → 'Python: Select Interpreter'"
echo "     → Choose: backend/venv/bin/python"
echo "  3. Test tasks: Cmd+Shift+P → 'Tasks: Run Task'"
echo "  4. Test snippets: Type 'mcp-tool' + Tab in Python file"
echo "  5. Test debugging: Press F5 → Select debug config"
echo ""
echo "🎯 Quick Commands:"
echo "  • Cmd+Shift+B - Run default test task"
echo "  • F5 - Start debugging"
echo "  • Cmd+Shift+P → 'Tasks: Run Task' - Run any task"
echo "  • Type snippet prefix + Tab - Use code snippets"
echo ""
