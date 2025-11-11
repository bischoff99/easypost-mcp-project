#!/usr/bin/env zsh
#
# verify_dev_environment.sh
# Quick verification script for development environment
# Checks backend, frontend, database, and Docker setup
# Uses zsh for better macOS compatibility
#

# Don't use set -e here - we handle errors in check() function
set -o pipefail

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

echo "🔍 Verifying Development Environment..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

typeset -i PASSED=0
typeset -i FAILED=0
typeset -i WARNINGS=0

check() {
    local name="$1"
    local command="$2"
    local expected="${3:-0}"
    
    if eval "$command" >/dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $name"
        ((PASSED++))
        return 0
    else
        if [ "$expected" = "warn" ]; then
            echo -e "${YELLOW}⚠️${NC} $name (optional)"
            ((WARNINGS++))
            return 0
        else
            echo -e "${RED}❌${NC} $name"
            ((FAILED++))
            return 0
        fi
    fi
}

# Backend checks
echo "📦 Backend:"
check "Backend directory exists" "test -d $BACKEND_PATH"
check "Backend venv exists" "test -d $BACKEND_PATH/venv"
check "Backend Python executable" "test -f $BACKEND_PATH/venv/bin/python"
check "Backend requirements.txt" "test -f $BACKEND_PATH/requirements.txt"
check "Backend src directory" "test -d $BACKEND_PATH/src"
check "Backend server.py" "test -f $BACKEND_PATH/src/server.py"
check "Backend tests directory" "test -d $BACKEND_PATH/tests"

# Frontend checks
echo ""
echo "🎨 Frontend:"
check "Frontend directory exists" "test -d $FRONTEND_PATH"
check "Frontend package.json" "test -f $FRONTEND_PATH/package.json"
check "Frontend src directory" "test -d $FRONTEND_PATH/src"
check "Frontend node_modules" "test -d $FRONTEND_PATH/node_modules" "warn"
check "Frontend vite.config.js" "test -f $FRONTEND_PATH/vite.config.js"

# Docker checks
echo ""
echo "🐳 Docker:"
check "Docker directory exists" "test -d $DOCKER_PATH"
check "Docker Compose file" "test -f $DOCKER_PATH/docker-compose.yml"
check "Docker Compose prod file" "test -f $DOCKER_PATH/docker-compose.prod.yml"

# Database checks
echo ""
echo "🗄️  Database:"
check "Alembic config" "test -f $BACKEND_PATH/alembic.ini"
check "Alembic versions directory" "test -d $BACKEND_PATH/alembic/versions"

# Configuration checks
echo ""
echo "⚙️  Configuration:"
check ".envrc exists" "test -f .envrc"
check ".cursor/config.json exists" "test -f .cursor/config.json"
check "Makefile exists" "test -f Makefile"
check ".gitignore exists" "test -f .gitignore"

# Environment checks
echo ""
echo "🔐 Environment:"
if [ -f ".env" ]; then
    echo -e "${GREEN}✅${NC} .env file exists"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️${NC} .env file missing (copy from .env.example)"
    ((WARNINGS++))
fi

# Python version check
if [ -f "$BACKEND_PATH/venv/bin/python" ]; then
    PYTHON_VERSION=$($BACKEND_PATH/venv/bin/python --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✅${NC} Python version: $PYTHON_VERSION"
    ((PASSED++))
fi

# Package checks
echo ""
echo "📚 Packages:"
if [ -f "$BACKEND_PATH/venv/bin/python" ]; then
    if $BACKEND_PATH/venv/bin/python -c "import fastapi" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} FastAPI installed"
        ((PASSED++))
    else
        echo -e "${RED}❌${NC} FastAPI not installed"
        ((FAILED++))
    fi
    
    if $BACKEND_PATH/venv/bin/python -c "import easypost" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} EasyPost SDK installed"
        ((PASSED++))
    else
        echo -e "${RED}❌${NC} EasyPost SDK not installed"
        ((FAILED++))
    fi
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Summary:"
echo "  ✅ Passed: $PASSED"
echo "  ❌ Failed: $FAILED"
echo "  ⚠️  Warnings: $WARNINGS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ Environment looks good!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Start backend: cd apps/backend && source venv/bin/activate && uvicorn src.server:app --reload"
    echo "  2. Start frontend: cd apps/frontend && npm run dev"
    echo "  3. Or use Makefile: make dev"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please fix the issues above.${NC}"
    exit 1
fi
