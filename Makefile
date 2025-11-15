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
PROJECT_ROOT := .
SRC_DIR := src
TESTS_DIR := tests
CONFIG_DIR := config
SCRIPTS_DIR := scripts
VENV_DIR := venv

# Detect venv location (uses venv only)
VENV_BIN := $(VENV_DIR)/bin

# ============================================================================
# Macros
# ============================================================================

# Check venv exists, exit if not found
define check_venv
	@if [ ! -d "$(VENV_BIN)" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make setup' first."; \
		exit 1; \
	fi
endef

# ============================================================================
# Phony Targets
# ============================================================================

.PHONY: help help-all setup dev test lint format check build prod clean qcp d t l f c

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
	@echo "  make dev          - Start backend server"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test COV=1   - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run linters (ruff)"
	@echo "  make format       - Auto-format code (ruff)"
	@echo "  make check        - Run lint + test"
	@echo ""
	@echo "Building:"
	@echo "  make build        - Build production bundles"
	@echo ""
	@echo "Production:"
	@echo "  make prod         - Start backend in production mode"
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
	@echo "      Use scripts/ for advanced workflows (docker, benchmarks, MCP verification,"
	@echo "      monitoring, etc.)"

# ============================================================================
# Setup Targets
# ============================================================================

setup:
	@echo "🔧 Setting up development environment..."
	@echo ""
	@echo "📦 Backend setup..."
	@if [ ! -d $(VENV_DIR) ]; then \
		echo "  Creating Python virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
	fi
	@echo "  Installing backend dependencies..."
	@$(VENV_BIN)/pip install -U pip setuptools wheel
	@if [ -f $(CONFIG_DIR)/requirements.txt ]; then \
		$(VENV_BIN)/pip install -r $(CONFIG_DIR)/requirements.txt; \
	fi
	@echo ""
	@echo "✅ Setup complete!"
	@echo "  Backend: $(VENV_BIN)/python"

# ============================================================================
# Development Targets
# ============================================================================

dev:
	@echo "🚀 Starting development server..."
	@echo "📦 Backend: http://localhost:8000"
	@echo "📚 API Docs: http://localhost:8000/docs"
	$(check_venv)
	@$(VENV_BIN)/uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload

# ============================================================================
# Testing Targets
# ============================================================================

test:
	@if [ "$(COV)" = "1" ]; then \
		echo "📊 Running tests with coverage..."; \
		$(check_venv); \
		$(VENV_BIN)/pytest $(TESTS_DIR)/ -v --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html; \
		echo "✅ Coverage report generated:"; \
		echo "   HTML: htmlcov/index.html"; \
	else \
		echo "🧪 Running backend tests..."; \
		$(check_venv); \
		$(VENV_BIN)/pytest $(TESTS_DIR)/ -v -n auto; \
	fi

# ============================================================================
# Code Quality Targets
# ============================================================================

lint:
	@echo "🔍 Running linters..."
	$(check_venv)
	@if [ -f "$(VENV_BIN)/ruff" ]; then $(VENV_BIN)/ruff check $(SRC_DIR)/ $(TESTS_DIR)/ || exit 1; else echo "⚠️  ruff not found, skipping lint"; fi

format:
	@echo "✨ Formatting code..."
	$(check_venv)
	@if [ -f "$(VENV_BIN)/ruff" ]; then \
		$(VENV_BIN)/ruff format $(SRC_DIR)/ $(TESTS_DIR)/ && \
		$(VENV_BIN)/ruff check $(SRC_DIR)/ $(TESTS_DIR)/ --fix || exit 1; \
	else \
		echo "⚠️  ruff not found, skipping format"; \
	fi

check: lint test
	@echo "✅ All checks passed!"

# ============================================================================
# Building Targets
# ============================================================================

build:
	@echo "📦 Building production backend..."
	$(check_venv)
	@echo "  Compiling Python files..."
	@$(VENV_BIN)/python -m compileall -q $(SRC_DIR)/ || true
	@echo "  Type checking Python code..."
	@$(VENV_BIN)/mypy $(SRC_DIR)/ --no-error-summary 2>/dev/null || echo "    (mypy not available or errors found)"
	@echo ""
	@echo "✅ Build complete!"

# ============================================================================
# Production Targets
# ============================================================================

prod:
	@echo "🚀 Starting production servers..."
	@./$(SCRIPTS_DIR)/dev/start-prod.sh

# ============================================================================
# Maintenance Targets
# ============================================================================

clean:
	@echo "🧹 Cleaning build artifacts..."; \
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; \
	find . -type f -name "*.pyc" -delete; \
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true; \
	rm -rf .pytest_cache htmlcov .coverage; \
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
	@echo "📜 BASH SCRIPTS (10)"
	@echo "────────────────────────────────────────────────────────────"
	@echo "Development:"
	@echo "  ./scripts/dev/start-dev.sh          - macOS Terminal launcher (backend server)"
	@echo "  ./scripts/dev/start-backend.sh      - Backend server (standard, --jit, --mcp-verify)"
	@echo "  ./scripts/dev/start-prod.sh         - Production backend (multi-worker)"
	@echo ""
	@echo "Testing:"
	@echo "  ./scripts/test/quick-test.sh        - Backend + MCP health checks"
	@echo "  ./scripts/test/test-full-functionality.sh - Comprehensive backend/MCP battery"
	@echo "  ./scripts/test/benchmark.sh         - Performance benchmarks"
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
	@echo "🎯 VS CODE TASKS (6)"
	@echo "────────────────────────────────────────────────────────────"
	@echo "  Dev: Backend                - Start backend server"
	@echo "  Dev: Backend (Prod)         - Backend with production settings"
	@echo "  🧪 Test: Backend            - Run backend tests (parallel)"
	@echo "  🧪 Test: MCP Tools          - Run MCP verification workflow"
	@echo "  ✅ Pre-Commit: Run All Checks - Format + lint + test"
	@echo "  🚑 Health Check             - Quick backend/MCP health probes"
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
