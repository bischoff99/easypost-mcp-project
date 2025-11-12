# EasyPost MCP Project - Quick Development Commands
# Usage: make <command>
#
# Best Practice: ~12 commands for optimal maintainability
# Focus: Only the most essential daily-use commands

# Enable .ONESHELL for multi-line commands
.ONESHELL:

# ============================================================================
# Configuration
# ============================================================================

# Directories
BACKEND_DIR := apps/backend
FRONTEND_DIR := apps/frontend
SCRIPTS_DIR := scripts

# Detect venv location (prefers .venv, then venv)
VENV_BIN := $(shell if [ -d $(BACKEND_DIR)/.venv ]; then echo $(BACKEND_DIR)/.venv/bin; elif [ -d $(BACKEND_DIR)/venv ]; then echo $(BACKEND_DIR)/venv/bin; else echo "venv not found"; fi)

# ============================================================================
# Macros
# ============================================================================

# Check venv exists, exit if not found
define check_venv
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
endef

# ============================================================================
# Phony Targets
# ============================================================================

.PHONY: help help-all setup dev test lint format check build prod db-reset db-migrate clean qcp d t l f c

# ============================================================================
# Default Target
# ============================================================================

help:
	@echo "🚀 EasyPost MCP Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup        - Full environment setup (creates venv + installs dependencies)"
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start backend + frontend servers"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test COV=1   - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run linters (ruff, eslint)"
	@echo "  make format       - Auto-format code (ruff, prettier)"
	@echo "  make check        - Run lint + test"
	@echo ""
	@echo "Building:"
	@echo "  make build        - Build production bundles"
	@echo ""
	@echo "Production:"
	@echo "  make prod         - Start backend + frontend in production mode"
	@echo ""
	@echo "Database:"
	@echo "  make db-reset     - Reset database (downgrade + upgrade)"
	@echo "  make db-migrate   - Create migration (use: make db-migrate m=\"message\")"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Clean build artifacts"
	@echo ""
	@echo "Git:"
	@echo "  make qcp          - Quick commit + push (use: make qcp m=\"message\")"
	@echo ""
	@echo "Quick Aliases:"
	@echo "  make d            - Alias for 'make dev'"
	@echo "  make t            - Alias for 'make test'"
	@echo "  make l            - Alias for 'make lint'"
	@echo "  make f            - Alias for 'make format'"
	@echo "  make c            - Alias for 'make check'"
	@echo ""
	@echo "💡 Tip: Use 'make help-all' to see all commands (Makefile + Scripts + VS Code + Cursor)"
	@echo "      Use scripts/ for advanced workflows (backend-only, frontend-only,"
	@echo "      docker, benchmarks, health checks, reviews, etc.)"

# ============================================================================
# Setup Targets
# ============================================================================

setup:
	@echo "🔧 Setting up development environment..."
	@echo ""
	@echo "📦 Backend setup..."
	@if [ ! -d $(BACKEND_DIR)/.venv ] && [ ! -d $(BACKEND_DIR)/venv ]; then \
		echo "  Creating Python virtual environment..."; \
		cd $(BACKEND_DIR) && python3 -m venv .venv; \
	fi
	@echo "  Installing backend dependencies..."
	@cd $(BACKEND_DIR) && $(VENV_BIN)/pip install -U pip setuptools wheel
	@cd $(BACKEND_DIR) && $(VENV_BIN)/pip install -e .
	@echo ""
	@echo "📦 Frontend setup..."
	@if ! command -v pnpm >/dev/null 2>&1; then \
		echo "  Installing pnpm..."; \
		npm install -g pnpm@9; \
	fi
	@cd $(FRONTEND_DIR) && pnpm install
	@echo ""
	@echo "✅ Setup complete!"
	@echo "  Backend: $(VENV_BIN)/python"
	@echo "  Frontend: pnpm (in $(FRONTEND_DIR))"

# ============================================================================
# Development Targets
# ============================================================================

dev:
	@echo "🚀 Starting development servers..."
	@echo "📦 Backend: http://localhost:8000"
	@echo "⚡ Frontend: http://localhost:5173"
	$(check_venv)
	@trap 'kill 0' EXIT; \
	(cd $(BACKEND_DIR) && $(VENV_BIN)/uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload) & \
	(cd $(FRONTEND_DIR) && pnpm run dev) & \
	sleep 3 && \
	($(VENV_BIN)/python $(SCRIPTS_DIR)/python/mcp_tool.py get_tracking TEST 2>/dev/null | grep -q "status" && echo "✅ MCP tools verified" || echo "⚠️  MCP tools not yet accessible") & \
	wait

# ============================================================================
# Testing Targets
# ============================================================================

test:
	@if [ "$(COV)" = "1" ]; then \
		echo "📊 Running tests with coverage..."; \
		$(check_venv); \
		cd $(BACKEND_DIR) && $(VENV_BIN)/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html; \
		cd $(FRONTEND_DIR) && pnpm test:coverage; \
		echo "✅ Coverage reports generated:"; \
		echo "   Backend:  $(BACKEND_DIR)/htmlcov/index.html"; \
		echo "   Frontend: $(FRONTEND_DIR)/coverage/index.html"; \
	else \
		echo "🧪 Running all tests..."; \
		$(check_venv); \
		cd $(BACKEND_DIR) && $(VENV_BIN)/pytest tests/ -v -n auto; \
		cd $(FRONTEND_DIR) && pnpm test -- --run; \
	fi

# ============================================================================
# Code Quality Targets
# ============================================================================

lint:
	@echo "🔍 Running linters..."
	$(check_venv)
	@cd $(BACKEND_DIR) && if [ -f "$(VENV_BIN)/ruff" ]; then $(VENV_BIN)/ruff check src/ tests/ || exit 1; else echo "⚠️  ruff not found, skipping backend lint"; fi & \
	cd $(FRONTEND_DIR) && pnpm run lint || exit 1 & \
	wait

format:
	@echo "✨ Formatting code..."
	$(check_venv)
	@cd $(BACKEND_DIR) && if [ -f "$(VENV_BIN)/ruff" ]; then $(VENV_BIN)/ruff format src/ tests/ && $(VENV_BIN)/ruff check src/ tests/ --fix || exit 1; else echo "⚠️  ruff not found, skipping backend format"; fi & \
	cd $(FRONTEND_DIR) && pnpm run format || exit 1 & \
	wait

check: lint test
	@echo "✅ All checks passed!"

# ============================================================================
# Building Targets
# ============================================================================

build:
	@echo "📦 Building production bundles..."
	@if [ "$(VENV_BIN)" != "venv not found" ]; then \
		echo "  Compiling Python files..."; \
		cd $(BACKEND_DIR) && $(VENV_BIN)/python -m compileall -q src/ || true; \
		echo "  Type checking Python code..."; \
		cd $(BACKEND_DIR) && $(VENV_BIN)/mypy src/ --no-error-summary 2>/dev/null || echo "    (mypy not available or errors found)"; \
	fi
	@echo "  Building frontend..."
	@cd $(FRONTEND_DIR) && pnpm run build
	@if [ ! -d $(FRONTEND_DIR)/dist ]; then \
		echo "❌ Error: Build output directory not found!"; \
		exit 1; \
	fi
	@echo ""
	@echo "✅ Build complete!"
	@echo "  Frontend bundle size:"
	@du -sh $(FRONTEND_DIR)/dist 2>/dev/null || echo "    (dist directory not found)"

# ============================================================================
# Production Targets
# ============================================================================

prod:
	@echo "🚀 Starting production servers..."
	@./$(SCRIPTS_DIR)/dev/start-prod.sh

# ============================================================================
# Database Targets
# ============================================================================

db-reset:
	@echo "🔄 Resetting database..."
	$(check_venv)
	@cd $(BACKEND_DIR) && $(VENV_BIN)/alembic downgrade base && $(VENV_BIN)/alembic upgrade head
	@echo "✅ Database reset complete!"

db-migrate:
	@echo "📝 Creating migration..."
	@if [ -z "$(m)" ]; then \
		echo "❌ Error: Migration message required. Use: make db-migrate m=\"message\""; \
		exit 1; \
	fi
	$(check_venv)
	@cd $(BACKEND_DIR) && $(VENV_BIN)/alembic revision --autogenerate -m "$(m)"

# ============================================================================
# Maintenance Targets
# ============================================================================

clean:
	@echo "🧹 Cleaning build artifacts..."; \
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; \
	find . -type f -name "*.pyc" -delete; \
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true; \
	rm -rf $(BACKEND_DIR)/.pytest_cache $(BACKEND_DIR)/htmlcov $(BACKEND_DIR)/.coverage; \
	rm -rf $(FRONTEND_DIR)/dist $(FRONTEND_DIR)/node_modules/.vite $(FRONTEND_DIR)/coverage; \
	echo "✨ Cleaned!"

# ============================================================================
# Git Shortcuts
# ============================================================================

qcp:
	@if [ -z "$(m)" ]; then \
		echo "❌ Error: Commit message required. Use: make qcp m=\"message\""; \
		exit 1; \
	fi
	@git add -A && git commit -m "$(m)" && git push

# ============================================================================
# Command Aliases (Quick shortcuts for daily use)
# ============================================================================

d: dev
	@# Alias for 'make dev'

t: test
	@# Alias for 'make test'

l: lint
	@# Alias for 'make lint'

f: format
	@# Alias for 'make format'

c: check
	@# Alias for 'make check'

# ============================================================================
# Comprehensive Help (All Commands)
# ============================================================================

help-all:
	@echo "📚 Complete Command Reference"
	@echo "════════════════════════════════════════════════════════════"
	@echo ""
	@echo "🔧 MAKEFILE COMMANDS (12)"
	@echo "────────────────────────────────────────────────────────────"
	@make help | grep -v "^💡\|^───\|^Quick Aliases\|^make help-all" || true
	@echo ""
	@echo "📜 BASH SCRIPTS (13)"
	@echo "────────────────────────────────────────────────────────────"
	@echo "Development:"
	@echo "  ./scripts/dev/start-dev.sh          - macOS Terminal windows (backend + frontend)"
	@echo "  ./scripts/dev/start-backend.sh      - Backend only (standard, --jit, or --mcp-verify)"
	@echo "  ./scripts/dev/dev_local.sh          - Docker PostgreSQL + servers"
	@echo "  ./scripts/dev/start-prod.sh         - Production servers"
	@echo ""
	@echo "Testing:"
	@echo "  ./scripts/test/quick-test.sh         - Quick test suite (~30-60s)"
	@echo "  ./scripts/test/watch-tests.sh       - Watch mode (TDD)"
	@echo "  ./scripts/test/test-full-functionality.sh - Comprehensive tests"
	@echo "  ./scripts/test/benchmark.sh          - Performance benchmarks"
	@echo ""
	@echo "Utilities:"
	@echo "  ./scripts/utils/monitor-database.sh  - Database monitoring"
	@echo "  ./scripts/utils/setup-nginx-proxy.sh  - Nginx reverse proxy"
	@echo "  ./scripts/utils/clean-git-history.sh  - Remove API keys from git history"
	@echo "  ./scripts/utils/mcp-utils.sh {health|verify|test} - MCP utility commands"
	@echo ""
	@echo "Python Tools:"
	@echo "  python scripts/python/get-bulk-rates.py - Bulk rate testing"
	@echo "  python scripts/python/verify_mcp_server.py - MCP server verification"
	@echo "  python scripts/python/mcp_tool.py <tool> <args> - MCP tool CLI"
	@echo ""
	@echo "🎯 VS CODE TASKS (8)"
	@echo "────────────────────────────────────────────────────────────"
	@echo "  🚀 Dev: Full Stack          - Start backend + frontend (parallel)"
	@echo "  Dev: Backend                - Backend server only"
	@echo "  Dev: Frontend              - Frontend server only"
	@echo "  🧪 Test: Backend            - Run backend tests (parallel)"
	@echo "  🧪 Test: Frontend           - Run frontend tests"
	@echo "  🏗️ Build: Frontend          - Build frontend (default build)"
	@echo "  ✅ Pre-Commit: Run All Checks - Format + lint + test"
	@echo "  🗄️ Database: Create Migration - Create Alembic migration"
	@echo ""
	@echo "🤖 CURSOR WORKFLOWS (6)"
	@echo "────────────────────────────────────────────────────────────"
	@echo "  /workflow:pre-commit        - Pre-commit workflow (review → fix → test → commit)"
	@echo "  /workflow:feature-dev        - Feature development workflow"
	@echo "  /workflow:error-resolution   - Error resolution workflow"
	@echo "  /workflow:code-improvement  - Code improvement workflow"
	@echo "  /workflow:cleanup           - Cleanup workflow"
	@echo "  /workflow:pre-push          - Pre-push workflow"
	@echo ""
	@echo "⚡ UNIVERSAL COMMANDS (10)"
	@echo "────────────────────────────────────────────────────────────"
	@echo "  /test                       - Smart parallel testing"
	@echo "  /fix                        - Auto-repair errors"
	@echo "  /explain                    - AI code understanding"
	@echo "  /commit                     - Smart git commits"
	@echo "  /review                     - Automated code review"
	@echo "  /refactor                   - Safe code refactoring"
	@echo "  /docs                       - Documentation generation"
	@echo "  /debug                      - Interactive debugging"
	@echo "  /clean                      - Comprehensive cleanup"
	@echo "  /workflow                   - Command chain orchestration"
	@echo ""
	@echo "════════════════════════════════════════════════════════════"
	@echo "📖 Full Documentation: docs/COMMANDS_REFERENCE.md"
	@echo "🎯 Tool Selection Guide: docs/TOOL_SELECTION_GUIDE.md"
	@echo "════════════════════════════════════════════════════════════"
