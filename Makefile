# EasyPost MCP Project - Quick Development Commands
# Usage: make <command>

.PHONY: help setup dev test test-fast build clean install health db-reset lint format prod prod-docker review review-json export-backend export-frontend

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
	@echo "  make build        - Build production bundles"
	@echo "  make build-docker - Build Docker images"
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

# Detect venv location (supports both venv and .venv)
VENV_BIN = $(shell if [ -d apps/backend/venv ]; then echo apps/backend/venv/bin; elif [ -d apps/backend/.venv ]; then echo apps/backend/.venv/bin; else echo "venv not found"; fi)

# Setup: Create venv and install dependencies
setup:
	@echo "🔧 Setting up development environment..."
	@echo ""
	@echo "📦 Backend setup..."
	@if [ ! -d apps/backend/venv ] && [ ! -d apps/backend/.venv ]; then \
		echo "  Creating Python virtual environment..."; \
		cd apps/backend && python3 -m venv venv; \
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

# Start both servers in parallel
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
	@cd apps/frontend && npm run dev

# Run all tests
test:
	@echo "🧪 Running all tests..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/pytest tests/ -v
	@cd apps/frontend && npm test -- --run

# Fast tests (changed files only, parallel execution)
test-fast:
	@echo "⚡ Running fast tests..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/pytest tests/ -v --lf --ff -n auto
	@cd apps/frontend && npm test -- --run --changed

# Watch mode for tests
test-watch:
	@echo "👀 Starting test watch mode..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@trap 'kill 0' EXIT; \
	(cd apps/backend && $(VENV_BIN)/pytest-watch tests/ --clear) & \
	(cd apps/frontend && npm test) & \
	wait

# Coverage report
test-cov:
	@echo "📊 Running tests with coverage..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@cd apps/frontend && npm run test:coverage
	@echo "✅ Coverage reports generated:"
	@echo "   Backend:  apps/backend/htmlcov/index.html"
	@echo "   Frontend: apps/frontend/coverage/index.html"

# Production build
build:
	@echo "📦 Building production bundles..."
	@cd apps/frontend && npm run build
	@if [ "$(VENV_BIN)" != "venv not found" ]; then \
		cd apps/backend && $(VENV_BIN)/python -m compileall src/; \
	fi
	@echo "✅ Build complete!"
	@du -sh apps/frontend/dist

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

# Linting
lint:
	@echo "🔍 Running linters..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/ruff check src/ tests/
	@cd apps/frontend && npm run lint

# Auto-format
format:
	@echo "✨ Formatting code..."
	@if [ "$(VENV_BIN)" = "venv not found" ]; then \
		echo "❌ Error: Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	@cd apps/backend && $(VENV_BIN)/black src/ tests/ && $(VENV_BIN)/ruff check src/ tests/ --fix
	@cd apps/frontend && npx prettier --write src/

# Full quality check
check: lint test
	@echo "✅ All checks passed!"

# Install dependencies
install:
	@echo "📥 Installing dependencies..."
	@cd apps/backend && pip install -r requirements.txt
	@cd apps/frontend && npm install
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

# Health check
health:
	@echo "🏥 Checking server health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ Backend not running"
	@curl -s http://localhost:5173 > /dev/null && echo "✅ Frontend: OK" || echo "❌ Frontend not running"

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

# Performance benchmark
benchmark:
	@echo "⚡ Running benchmarks..."
	@./scripts/benchmark.sh

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
	@cd apps/frontend && npm audit --audit-level=moderate || true
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
