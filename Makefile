# EasyPost MCP Project - Quick Development Commands
# Usage: make <command>

.PHONY: help dev test test-fast build clean install health db-reset lint format

# Default target
help:
	@echo "🚀 EasyPost MCP Development Commands"
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
	@echo "Code Quality:"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Auto-format code"
	@echo "  make check        - Run all quality checks"
	@echo ""
	@echo "Utilities:"
	@echo "  make install      - Install all dependencies"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make health       - Check server health"
	@echo "  make benchmark    - Run performance benchmarks"

# Start both servers in parallel
dev:
	@echo "🚀 Starting development servers..."
	@trap 'kill 0' EXIT; \
	(cd backend && source venv/bin/activate && uvicorn src.server:app --reload --log-level warning) & \
	(cd frontend && npm run dev) & \
	wait

# Start with mock mode (faster development)
dev-mock:
	@echo "🎭 Starting with mock EasyPost API..."
	@trap 'kill 0' EXIT; \
	(cd backend && source venv/bin/activate && MOCK_MODE=true uvicorn src.server:app --reload) & \
	(cd frontend && npm run dev) & \
	wait

# Backend only
backend:
	@cd backend && source venv/bin/activate && uvicorn src.server:app --reload

# Frontend only
frontend:
	@cd frontend && npm run dev

# Run all tests
test:
	@echo "🧪 Running all tests..."
	@cd backend && source venv/bin/activate && pytest tests/ -v
	@cd frontend && npm test -- --run

# Fast tests (changed files only, parallel execution)
test-fast:
	@echo "⚡ Running fast tests..."
	@cd backend && source venv/bin/activate && pytest tests/ -v --lf --ff -n auto
	@cd frontend && npm test -- --run --changed

# Watch mode for tests
test-watch:
	@echo "👀 Starting test watch mode..."
	@trap 'kill 0' EXIT; \
	(cd backend && source venv/bin/activate && pytest-watch tests/ --clear) & \
	(cd frontend && npm test) & \
	wait

# Coverage report
test-cov:
	@echo "📊 Running tests with coverage..."
	@cd backend && source venv/bin/activate && pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@cd frontend && npm run test:coverage
	@echo "✅ Coverage reports generated:"
	@echo "   Backend:  backend/htmlcov/index.html"
	@echo "   Frontend: frontend/coverage/index.html"

# Production build
build:
	@echo "📦 Building production bundles..."
	@cd frontend && npm run build
	@cd backend && source venv/bin/activate && python -m compileall src/
	@echo "✅ Build complete!"
	@du -sh frontend/dist

# Docker build
build-docker:
	@echo "🐳 Building Docker images..."
	@docker-compose build --parallel
	@echo "✅ Docker images built!"

# Linting
lint:
	@echo "🔍 Running linters..."
	@cd backend && source venv/bin/activate && ruff check src/ tests/
	@cd frontend && npm run lint

# Auto-format
format:
	@echo "✨ Formatting code..."
	@cd backend && source venv/bin/activate && black src/ tests/ && ruff check src/ tests/ --fix
	@cd frontend && npx prettier --write src/

# Full quality check
check: lint test
	@echo "✅ All checks passed!"

# Install dependencies
install:
	@echo "📥 Installing dependencies..."
	@cd backend && pip install -r requirements.txt
	@cd frontend && npm install
	@echo "✅ Dependencies installed!"

# Clean artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf backend/.pytest_cache backend/htmlcov backend/.coverage
	@rm -rf frontend/dist frontend/node_modules/.vite frontend/coverage
	@echo "✨ Cleaned!"

# Health check
health:
	@echo "🏥 Checking server health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ Backend not running"
	@curl -s http://localhost:5173 > /dev/null && echo "✅ Frontend: OK" || echo "❌ Frontend not running"

# Database operations (when implemented)
db-reset:
	@echo "🔄 Resetting database..."
	@cd backend && source venv/bin/activate && alembic downgrade base && alembic upgrade head
	@echo "✅ Database reset complete!"

db-migrate:
	@echo "📝 Creating migration..."
	@cd backend && source venv/bin/activate && alembic revision --autogenerate -m "$(m)"

db-upgrade:
	@cd backend && source venv/bin/activate && alembic upgrade head

# Performance benchmark
benchmark:
	@echo "⚡ Running benchmarks..."
	@./scripts/benchmark.sh

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
