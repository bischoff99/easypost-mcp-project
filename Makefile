# EasyPost MCP Project - Quick Development Commands
# Usage: make <command>

# Enable .ONESHELL for multi-line commands
.ONESHELL:

.PHONY: help setup dev dev-mock backend frontend test test-fast test-watch test-cov build build-sourcemap build-analyze build-preview build-docker prod prod-docker lint format check install clean clean-deep health benchmark audit security validate-structure sync commit push qcp db-reset db-migrate db-upgrade review review-json export-backend export-frontend

# Default target
help:
	@echo "🚀 EasyPost MCP Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup        - Install all dependencies (backend venv + frontend pnpm)"
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start backend + frontend servers"
	@echo "  make dev-mock     - Start with mock EasyPost API"
	@echo "  make backend      - Start backend only"
	@echo "  make frontend     - Start frontend only"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-fast    - Run tests for changed files only"
	@echo "  make test-watch   - Run tests in watch mode"
	@echo "  make test-cov     - Run tests with coverage report"
	@echo ""
	@echo "Building:"
	@echo "  make build           - Build production bundles"
	@echo "  make build-sourcemap - Build with sourcemaps (for debugging)"
	@echo "  make build-analyze   - Build and analyze bundle size"
	@echo "  make build-preview   - Preview production build locally"
	@echo "  make build-docker    - Build Docker images"
	@echo ""
	@echo "Production:"
	@echo "  make prod         - Start backend + frontend in production mode"
	@echo "  make prod-docker  - Start production with Docker Compose"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run linters (ruff, eslint)"
	@echo "  make format       - Auto-format code (black, prettier)"
	@echo "  make check        - Run lint + test"
	@echo ""
	@echo "Repository Review:"
	@echo "  make review       - Full repository review (human-readable)"
	@echo "  make review-json  - Full repository review (JSON output)"
	@echo ""
	@echo "Export:"
	@echo "  make export-backend  - Export backend source to zip"
	@echo "  make export-frontend - Export frontend source to zip"
	@echo ""
	@echo "Other:"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make install      - Install dependencies"
	@echo "  make health       - Check system health"
	@echo "  make db-reset     - Reset database"
	@echo "  make audit        - Security audit"
	@echo "  make validate-structure - Validate project structure"

# Repository Review
review:
	@echo "🔍 Running full repository review..."
	@python3 scripts/full_repo_review.py

review-json:
	@echo "🔍 Running full repository review (JSON output)..."
	@python3 scripts/full_repo_review.py --json > docs/reviews/REPO_REVIEW_$$(date +%Y%m%d_%H%M%S).json
	@echo "✅ JSON report saved to docs/reviews/"

# Export backend source code
export-backend:
	@zsh scripts/export_backend_source.sh

# Export frontend source code
export-frontend:
	@zsh scripts/export_frontend_source.sh

# Detect venv location (prefers .venv, then venv)
VENV_BIN = $(shell if [ -d apps/backend/.venv ]; then echo apps/backend/.venv/bin; elif [ -d apps/backend/venv ]; then echo apps/backend/venv/bin; else echo "venv not found"; fi)

# Setup: Create venv and install dependencies
setup:
	@echo "🔧 Setting up development environment..."
	@echo ""
	@echo "📦 Backend setup..."
	@if [ ! -d apps/backend/.venv ] && [ ! -d apps/backend/venv ]; then \
		echo "  Creating Python virtual environment..."; \
		cd apps/backend && python3 -m venv .venv; \
	fi
	@echo "  Installing backend dependencies..."
	@cd apps/backend && $(VENV_BIN)/pip install -U pip setuptools wheel
	@cd apps/backend && $(VENV_BIN)/pip install -e .
	@echo ""
	@echo "📦 Frontend setup..."
	@if ! command -v pnpm >/dev/null 2>&1; then \
		echo "  Installing pnpm..."; \
		npm install -g pnpm@9; \
	fi
	@cd apps/frontend && pnpm install
	@echo ""
	@echo "✅ Setup complete!"
	@echo "  Backend: $(VENV_BIN)/python"
	@echo "  Frontend: pnpm (in apps/frontend)"

# Start both servers in parallel (with MCP verification)
dev:
	@echo "🚀 Starting development servers..."
	@echo "📦 Backend: http://localhost:8000"
	@echo "⚡ Frontend: http://localhost:5173"
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@trap 'kill 0' EXIT; \
	(cd apps/backend && $(VENV_BIN)/uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload) & \
	(cd apps/frontend && pnpm run dev) & \
	sleep 3 && \
	($(VENV_BIN)/python scripts/mcp_tool.py get_tracking TEST 2>/dev/null | grep -q "status" && echo "✅ MCP tools verified" || echo "⚠️  MCP tools not yet accessible") & \
	wait

# Start with mock mode (faster development)
dev-mock:
	@echo "🎭 Starting with mock EasyPost API..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@trap 'kill 0' EXIT; \
	(cd apps/backend && MOCK_MODE=true $(VENV_BIN)/uvicorn src.server:app --reload) & \
	(cd apps/frontend && pnpm run dev) & \
	wait

# Backend only
backend:
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/uvicorn src.server:app --reload

# Frontend only
frontend:
	@cd apps/frontend && pnpm run dev

# Run all tests
test:
	@echo "🧪 Running all tests..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/pytest tests/ -v
	@cd apps/frontend && pnpm test -- --run

# Fast tests (changed files only, parallel execution)
test-fast:
	@echo "⚡ Running fast tests..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/pytest tests/ -v --lf --ff -n auto || echo "⚠️  Backend tests had failures" & \
	cd apps/frontend && pnpm test -- --run --changed || echo "⚠️  Frontend tests had failures" & \
	wait

# Watch mode for tests
test-watch:
	@echo "👀 Starting test watch mode..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@trap 'kill 0' EXIT; \
	(cd apps/backend && $(VENV_BIN)/pytest-watch tests/ --clear) & \
	(cd apps/frontend && pnpm test) & \
	wait

# Coverage report
test-cov:
	@echo "📊 Running tests with coverage..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@cd apps/frontend && pnpm test:coverage
	@echo "✅ Coverage reports generated:"
	@echo "   Backend:  apps/backend/htmlcov/index.html"
	@echo "   Frontend: apps/frontend/coverage/index.html"

# Production build
build:
	@echo "📦 Building production bundles..."
	@if [ "$(VENV_BIN)" != "venv not found" ]; then \
		echo "  Compiling Python files..."; \
		cd apps/backend && $(VENV_BIN)/python -m compileall -q src/ || true; \
		echo "  Type checking Python code..."; \
		cd apps/backend && $(VENV_BIN)/mypy src/ --no-error-summary 2>/dev/null || echo "    (mypy not available or errors found)"; \
	fi
	@echo "  Building frontend..."
	@cd apps/frontend && pnpm run build || (echo "❌ Frontend build failed!" && exit 1)
	@if [ ! -d apps/frontend/dist ]; then \
		echo "❌ Error: Build output directory not found!"; \
		exit 1; \
	fi
	@echo ""
	@echo "✅ Build complete!"
	@echo "  Frontend bundle size:"
	@du -sh apps/frontend/dist 2>/dev/null || echo "    (dist directory not found)"
	@if [ -d apps/frontend/dist ]; then \
		echo "  Bundle breakdown:"; \
		find apps/frontend/dist -type f -name "*.js" -exec sh -c 'echo "    {}: $$(du -h "{}" | cut -f1)"' \; | head -10; \
	fi

# Build with sourcemaps (for production debugging)
build-sourcemap:
	@echo "📦 Building with sourcemaps..."
	@cd apps/frontend && BUILD_SOURCEMAP=true pnpm run build
	@echo "✅ Build with sourcemaps complete!"

# Build analysis
build-analyze:
	@echo "📊 Analyzing build..."
	@cd apps/frontend && pnpm run build:analyze || pnpm run build
	@if [ -d apps/frontend/dist ]; then \
		echo ""; \
		echo "📈 Build Statistics:"; \
		echo "  Total size: $$(du -sh apps/frontend/dist | cut -f1)"; \
		echo "  JS files: $$(find apps/frontend/dist -name '*.js' | wc -l | tr -d ' ')"; \
		echo "  CSS files: $$(find apps/frontend/dist -name '*.css' | wc -l | tr -d ' ')"; \
		echo "  Assets: $$(find apps/frontend/dist -type f ! -name '*.js' ! -name '*.css' ! -name '*.html' | wc -l | tr -d ' ')"; \
		echo ""; \
		echo "  Largest files:"; \
		find apps/frontend/dist -type f -exec du -h {} + | sort -rh | head -10 | awk '{print "    " $$2 ": " $$1}'; \
	fi

# Preview production build
build-preview:
	@echo "👀 Previewing production build..."
	@if [ ! -d apps/frontend/dist ]; then \
		echo "  Building first..."; \
		cd apps/frontend && pnpm run build; \
	fi
	@cd apps/frontend && pnpm run preview

# Docker build
build-docker:
	@echo "🐳 Building Docker images..."
	@docker compose -f deploy/docker-compose.yml build --parallel
	@echo "✅ Docker images built!"

# Production mode (local)
prod:
	@echo "🚀 Starting production servers..."
	@./scripts/start-prod.sh

# Production mode (Docker)
prod-docker:
	@echo "🐳 Starting production with Docker..."
	@if [ ! -f .env.production ]; then \
		echo "⚠️  .env.production not found. Creating from .env.example..."; \
		cp .env.example .env.production 2>/dev/null || true; \
		echo "📝 Please edit .env.production with production values"; \
	fi
	@docker compose -f deploy/docker-compose.prod.yml --env-file .env.production up -d
	@echo "✅ Production services started!"
	@echo "   Backend:  http://localhost:8000"
	@echo "   Frontend: http://localhost:80"
	@echo "   View logs: docker compose -f deploy/docker-compose.prod.yml logs -f"

# Linting (parallel backend/frontend)
lint:
	@echo "🔍 Running linters..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/ruff check src/ tests/ || exit 1 & \
	cd apps/frontend && pnpm run lint || exit 1 & \
	wait

# Auto-format (parallel backend/frontend)
format:
	@echo "✨ Formatting code..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/black src/ tests/ && $(VENV_BIN)/ruff check src/ tests/ --fix || exit 1 & \
	cd apps/frontend && pnpm run format || exit 1 & \
	wait

# Full quality check
check: lint test
	@echo "✅ All checks passed!"

# Install dependencies
install:
	@echo "📥 Installing dependencies..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "  Creating Python virtual environment..."; \
		cd apps/backend && python3 -m venv .venv; \
	fi
	@cd apps/backend && $(VENV_BIN)/pip install -r requirements.txt
	@if ! command -v pnpm >/dev/null 2>&1; then \
		echo "  Installing pnpm..."; \
		npm install -g pnpm@9; \
	fi
	@cd apps/frontend && pnpm install
	@echo "✅ Dependencies installed!"

# Clean artifacts (uses parallel script for M3 Max optimization)
clean:
	@if [ -f scripts/clean_project_parallel.sh ]; then \
		bash scripts/clean_project_parallel.sh; \
	else \
		echo "🧹 Cleaning build artifacts..."; \
		find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; \
		find . -type f -name "*.pyc" -delete; \
		find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true; \
		rm -rf apps/backend/.pytest_cache apps/backend/htmlcov apps/backend/.coverage; \
		rm -rf apps/frontend/dist apps/frontend/node_modules/.vite apps/frontend/coverage; \
		echo "✨ Cleaned!"; \
	fi

# Deep clean (parallel, removes Docker images and user caches)
clean-deep:
	@bash scripts/clean_project_parallel.sh --deep

# Health check (with MCP verification)
health:
	@echo "🏥 Checking server health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ Backend not running"
	@curl -s http://localhost:5173 > /dev/null && echo "✅ Frontend: OK" || echo "❌ Frontend not running"
	@if [ "$(VENV_BIN)" != "venv not found" ]; then \
		echo "🔍 Verifying MCP tools..."; \
		$(VENV_BIN)/python scripts/mcp_tool.py get_tracking TEST 2>/dev/null | grep -q "status" && echo "✅ MCP tools accessible" || echo "⚠️  MCP tools not accessible (server may not be running)"; \
	fi

# Database operations
db-reset:
	@echo "🔄 Resetting database..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/alembic downgrade base && $(VENV_BIN)/alembic upgrade head
	@echo "✅ Database reset complete!"

db-migrate:
	@echo "📝 Creating migration..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/alembic revision --autogenerate -m "$(m)"

db-upgrade:
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/alembic upgrade head

# Performance benchmark (with MCP tool testing)
benchmark:
	@echo "⚡ Running benchmarks..."
	@./scripts/benchmark.sh
	@if [ "$(VENV_BIN)" != "venv not found" ]; then \
		echo ""; \
		echo "🧪 Testing MCP tool performance..."; \
		time $(VENV_BIN)/python scripts/mcp_tool.py get_tracking TEST 2>/dev/null > /dev/null && echo "✅ MCP tool call: OK" || echo "⚠️  MCP tool test skipped"; \
	fi

# Security audit
audit:
	@echo "🔒 Running security audits..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "📦 Auditing Python dependencies..."
	@cd apps/backend && $(VENV_BIN)/pip install pip-audit 2>/dev/null || pip install pip-audit
	@cd apps/backend && $(VENV_BIN)/pip-audit --requirement requirements.txt || true
	@echo ""
	@echo "📦 Auditing Node.js dependencies..."
	@cd apps/frontend && pnpm audit --audit-level=moderate || true
	@echo ""
	@echo "✅ Security audit complete!"

# Security scan (comprehensive)
security: audit
	@echo "🛡️ Running comprehensive security scan..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@echo "🔍 Checking for secrets..."
	@cd apps/backend && $(VENV_BIN)/pip install detect-secrets 2>/dev/null || pip install detect-secrets
	@detect-secrets scan --baseline .secrets.baseline || true
	@echo "✅ Security scan complete!"

# Structure validation
validate-structure:
	@echo "🔍 Validating project structure..."
	@python3 scripts/validate-project-structure.py

# Git shortcuts
sync:
	@git fetch origin
	@git rebase origin/main

commit:
	@git add -A
	@git commit -m "$(m)"

push: sync
	@git push origin $(shell git branch --show-current)

# Quick commit and push
qcp:
	@git add -A && git commit -m "$(m)" && git push
