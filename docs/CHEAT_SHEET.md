# EasyPost MCP - Command Cheat Sheet

**Quick Reference for Maximum Productivity**

## 🚀 Quick Reference Table

| Task | Fastest Command | Alternative | When to Use Alternative |
|------|----------------|-------------|------------------------|
| **Start Development** | `make d` | `./scripts/dev/start-dev.sh` | Need macOS Terminal windows |
| **Run Tests** | `make t` | `/ep-test` | Using Cursor AI, want context-aware |
| **Quick Health Check** | `./scripts/test/quick-test.sh` | `make test` | Need full test suite |
| **Watch Tests** | `./scripts/test/watch-tests.sh` | VS Code "Test: Backend" | Need IDE debugging |
| **Code Quality** | `make check` | VS Code "Pre-Commit" | In VS Code, want IDE integration |
| **Production** | `make prod` | `./scripts/dev/start-prod.sh` | Need custom production config |
| **Benchmark** | `/ep-benchmark` | `./scripts/test/benchmark.sh` | Not using Cursor AI |

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Daily Development](#daily-development)
3. [Testing Workflows](#testing-workflows)
4. [Code Quality](#code-quality)
5. [Production & Deployment](#production--deployment)
6. [Troubleshooting](#troubleshooting)
7. [Power User Tips](#power-user-tips)

---

## 🎯 Getting Started

### First Time Setup

```bash
# Complete environment setup (one command)
make setup

# What it does:
# - Creates Python venv
# - Installs backend dependencies
# - Installs frontend dependencies
# - Sets up database
```

**Pro Tip:** Run once, then use `make dev` for daily development.

### Start Development Environment

**Option 1: Single Terminal (Fastest)**
```bash
make d          # Alias for 'make dev'
# Starts backend + frontend in parallel
# Single terminal, background processes
# ~3 seconds to start
```

**Option 2: macOS Terminal Windows**
```bash
./scripts/dev/start-dev.sh
# Opens separate Terminal windows
# Better for viewing logs separately
# macOS only
```

**Option 3: Docker + Local Development**
```bash
./scripts/dev/dev_local.sh
# Starts PostgreSQL in Docker
# Then starts backend + frontend
# Use when you need database
```

**Option 4: VS Code Integration**
```
Ctrl+Shift+P → "Tasks: Run Task" → "🚀 Dev: Full Stack"
# IDE-integrated, debugging support
# Problem matchers for errors
```

**Option 5: Cursor AI Enhanced**
```bash
/ep-dev
# AI-enhanced startup
# Desktop Commander integration
# Context-aware execution
```

**When to Use Which:**
- **Quick start**: `make d` (fastest, single terminal)
- **macOS + separate logs**: `start-dev.sh`
- **Need database**: `dev_local.sh`
- **VS Code debugging**: VS Code task
- **AI-enhanced**: `/ep-dev`

---

## 💻 Daily Development

### Backend Only Development

**Standard Mode (Hot Reload)**
```bash
./scripts/dev/start-backend.sh
# Single worker, auto-reload on changes
# Best for: Regular development
```

**JIT Mode (Performance Boost)**
```bash
./scripts/dev/start-backend.sh --jit
# Multi-worker, JIT compilation (Python 3.13+)
# 10-20% performance boost
# Best for: Performance testing
```

**With Enhanced MCP Verification**
```bash
./scripts/dev/start-backend.sh --mcp-verify
# Verifies MCP tools are accessible
# Shows tool registration status
# Best for: MCP development
```

**Pro Tip:** Combine flags: `./scripts/dev/start-backend.sh --jit --mcp-verify`

### Frontend Only Development

```bash
cd apps/frontend && npm run dev
# Direct command (no wrapper needed)
# Fastest option
```

**VS Code Alternative:**
```
Ctrl+Shift+P → "Tasks: Run Task" → "Dev: Frontend"
# IDE-integrated, problem matchers
```

### Quick Commands (Makefile Aliases)

```bash
make d    # dev - Start development servers
make t    # test - Run all tests
make l    # lint - Check code quality
make f    # format - Auto-format code
make c    # check - Lint + format + test
```

**Pro Tip:** These aliases save 3-5 keystrokes per command. Use them!

---

## 🧪 Testing Workflows

### Quick Health Check (~10 seconds)

```bash
./scripts/test/quick-test.sh
# Checks: Backend health, Frontend, Nginx, API endpoints, Quick unit tests
# Use: Before committing, quick validation
```

**When to Use:**
- Pre-commit checks
- Quick validation after changes
- CI/CD pipeline (fast feedback)

### Full Test Suite

**Standard Execution**
```bash
make t          # Alias for 'make test'
# Runs pytest with auto-detected workers
# Parallel execution
# ~30-60 seconds
```

**With Coverage**
```bash
make test COV=1
# Generates HTML coverage report
# Shows uncovered lines
# Opens report automatically
```

**VS Code Integration**
```
Ctrl+Shift+P → "Tasks: Run Task" → "🧪 Test: Backend"
# IDE-integrated, debugging support
# Can set breakpoints
```

**Cursor AI Enhanced**
```bash
/ep-test
# Auto-detects test type from open file
# Context-aware execution
# Desktop Commander integration
```

### Watch Mode (TDD Workflow)

```bash
./scripts/test/watch-tests.sh
# Auto-reruns on file changes
# Perfect for TDD
# Press Ctrl+C to stop
```

**Pro Tip:** Run in separate terminal while developing. Tests run automatically on save.

### Comprehensive Testing

```bash
./scripts/test/test-full-functionality.sh
# Full integration test suite
# Tests: Unit, Integration, Frontend, API, MCP, Performance
# Duration: 2-5 minutes
# Use: Before major commits, release validation
```

### Performance Benchmarks

**Cursor AI Enhanced**
```bash
/ep-benchmark
# AI-enhanced benchmark execution
# Performance regression detection
# Baseline comparison
```

**Standard Script**
```bash
./scripts/test/benchmark.sh
# Comprehensive performance tests
# Sequential vs parallel comparison
# M3 Max optimized
```

**Pro Tip:** Run benchmarks after optimization changes to validate improvements.

---

## ✅ Code Quality

### Quick Quality Check

```bash
make c          # Alias for 'make check'
# Runs: lint → format → test
# Sequential execution
# ~20-30 seconds
```

**What It Does:**
1. Lints backend (ruff) and frontend (eslint)
2. Formats code (ruff + prettier)
3. Runs tests (pytest + vitest)

### Individual Quality Commands

**Linting Only**
```bash
make l          # Alias for 'make lint'
# Checks code quality
# No auto-fix
# ~5 seconds
```

**Formatting Only**
```bash
make f          # Alias for 'make format'
# Auto-fixes formatting
# ~3 seconds
```

**VS Code Pre-Commit**
```
Ctrl+Shift+P → "Tasks: Run Task" → "✅ Pre-Commit: Run All Checks"
# Same as 'make check' but IDE-integrated
# Problem matchers highlight issues
```

**Pro Tip:** Run `make c` before every commit. Catches issues early.

---

## 🚀 Production & Deployment

### Build Production Bundles

```bash
make build
# Builds backend (if needed) + frontend
# Optimized production bundles
# ~30-60 seconds
```

**VS Code Alternative:**
```
Ctrl+Shift+P → "Tasks: Run Task" → "🏗️ Build: Frontend"
# IDE-integrated build
# Problem matchers for build errors
```

### Start Production Servers

```bash
make prod
# Starts backend + frontend in production mode
# No hot reload
# Production environment variables
```

**Custom Production Script**
```bash
./scripts/dev/start-prod.sh
# More control over production startup
# Custom configurations
# Environment variable overrides
```

---

## 🔧 Troubleshooting

### Database Operations

**Reset Database**
```bash
make db-reset
# Drops all tables, recreates schema
# Use: When schema changes break migrations
```

**Create Migration**
```bash
make db-migrate m="add user table"
# Creates Alembic migration
# Auto-detects model changes
```

**VS Code Migration**
```
Ctrl+Shift+P → "Tasks: Run Task" → "🗄️ Database: Create Migration"
# Prompts for migration message
# IDE-integrated
```

### Database Monitoring

```bash
./scripts/utils/monitor-database.sh
# Shows active connections
# Query statistics
# Performance monitoring
```

### MCP Tools Verification

**Quick Check**
```bash
./scripts/utils/mcp-utils.sh health
# Checks if MCP server is accessible
```

**Verify Tools**
```bash
./scripts/utils/mcp-utils.sh verify
# Lists registered MCP tools
# Verifies tool registration
```

**Test Tools**
```bash
./scripts/utils/mcp-utils.sh test
# Tests MCP tools with sample data
# Validates tool responses
```

**Pro Tip:** Use these when MCP tools aren't working. Helps debug integration issues.

### Git History Cleanup

```bash
./scripts/utils/clean-git-history.sh
# Removes API keys from git history
# Uses git-filter-repo
# ⚠️ Rewrites history (requires force push)
```

**Pro Tip:** Run this if you accidentally committed secrets. Then force push.

### Clean Build Artifacts

```bash
make clean
# Removes: __pycache__, .pyc, .egg-info, .pytest_cache, dist, build
# Use: When builds are corrupted or need fresh start
```

---

## ⚡ Power User Tips

### Command Combinations

**Start Dev + Watch Tests**
```bash
# Terminal 1
make d

# Terminal 2
./scripts/test/watch-tests.sh
```

**Quick Test Before Commit**
```bash
make c && git commit -m "feat: your message"
# Runs quality checks, only commits if all pass
```

**Production Build + Deploy**
```bash
make build && make prod
# Builds then starts production servers
```

### Parallel Execution

**Makefile Commands**
- `make dev` - Backend + Frontend in parallel
- `make test` - Tests run with auto-detected workers (parallel)
- `make lint` - Backend + Frontend linting in parallel

**Pro Tip:** Makefile commands are optimized for parallel execution. Use them for speed.

### Cursor AI Commands (Maximum Value)

**Context-Aware Testing**
```bash
/ep-test
# If file open: Tests that file
# If in backend/: Tests backend
# If in frontend/: Tests frontend
# Otherwise: Tests everything
```

**AI-Enhanced Development**
```bash
/ep-dev
# Starts all services
# Verifies health
# Shows real-time logs
# Desktop Commander integration
```

**Performance Validation**
```bash
/ep-benchmark --compare
# Runs benchmarks
# Compares with baseline
# Detects regressions
```

**Pro Tip:** Cursor commands are context-aware. They adapt to your current file/context.

### Python Tools

**Bulk Rate Testing**
```bash
python scripts/python/get-bulk-rates.py
# Tests bulk shipment rate retrieval
# Validates bulk operations
```

**MCP Tool CLI**
```bash
python scripts/python/mcp_tool.py get_tracking EZ1234567890
python scripts/python/mcp_tool.py create_shipment --data "..." --dry-run
# Direct MCP tool access
# Useful for debugging
```

**MCP Server Verification**
```bash
python scripts/python/verify_mcp_server.py
# Validates MCP server setup
# Tests tool registration
# Checks resource providers
```

### Workflow Chains

**Pre-Commit Workflow**
```bash
make c          # Lint + format + test
# If passes:
git add .
git commit -m "feat: your message"
```

**Feature Development Workflow**
```bash
# Terminal 1: Development
make d

# Terminal 2: Watch Tests
./scripts/test/watch-tests.sh

# Terminal 3: Quick checks
./scripts/test/quick-test.sh  # Run periodically
```

**Release Workflow**
```bash
make c                              # Quality checks
./scripts/test/test-full-functionality.sh  # Comprehensive tests
./scripts/test/benchmark.sh         # Performance validation
make build                          # Production build
make prod                           # Start production
```

### Environment Variables

**Custom Ports**
```bash
API_PORT=9000 ./scripts/dev/start-backend.sh
PORT=3000 cd apps/frontend && npm run dev
```

**Production Mode**
```bash
ENVIRONMENT=production ./scripts/dev/start-backend.sh
```

**Pro Tip:** Set environment variables before commands for custom configurations.

### Quick Git Operations

```bash
make qcp m="feat: add new feature"
# Quick commit + push
# Combines: git add, commit, push
```

---

## 📊 Command Speed Reference

| Command | Duration | Parallel | Use Case |
|---------|----------|----------|----------|
| `make d` | ~3s | ✅ | Daily development |
| `make t` | 30-60s | ✅ | Full test suite |
| `./scripts/test/quick-test.sh` | ~10s | ❌ | Quick validation |
| `make c` | 20-30s | ⚠️ | Pre-commit |
| `make build` | 30-60s | ⚠️ | Production build |
| `./scripts/test/test-full-functionality.sh` | 2-5min | ⚠️ | Comprehensive testing |
| `./scripts/test/benchmark.sh` | 2-5min | ❌ | Performance testing |

**Legend:**
- ✅ Fully parallel
- ⚠️ Partially parallel
- ❌ Sequential

---

## 🎯 Common Scenarios

### "I want to start developing"
→ `make d` (fastest, single terminal)

### "I want to test before committing"
→ `make c` (lint + format + test)

### "I want quick validation"
→ `./scripts/test/quick-test.sh` (~10s)

### "I want to watch tests while developing"
→ `./scripts/test/watch-tests.sh` (separate terminal)

### "I want comprehensive testing"
→ `./scripts/test/test-full-functionality.sh` (2-5min)

### "I want performance benchmarks"
→ `/ep-benchmark` (Cursor) or `./scripts/test/benchmark.sh`

### "I want macOS Terminal windows"
→ `./scripts/dev/start-dev.sh`

### "I need Docker database"
→ `./scripts/dev/dev_local.sh`

### "I want IDE debugging"
→ VS Code tasks (Ctrl+Shift+P)

### "I want AI-enhanced commands"
→ Cursor commands (`/ep-dev`, `/ep-test`, `/ep-benchmark`)

---

## 💡 Pro Tips Summary

1. **Use aliases**: `make d`, `make t`, `make l`, `make f`, `make c` save keystrokes
2. **Parallel execution**: Makefile commands are optimized for parallel execution
3. **Context-aware**: Cursor commands adapt to your current file/context
4. **Watch mode**: Run `watch-tests.sh` in separate terminal for TDD
5. **Quick checks**: Use `quick-test.sh` before commits (~10s)
6. **Pre-commit**: Always run `make c` before committing
7. **Terminal windows**: Use `start-dev.sh` for separate log viewing (macOS)
8. **Docker**: Use `dev_local.sh` when you need database
9. **IDE integration**: VS Code tasks provide debugging and problem matchers
10. **AI enhancement**: Cursor commands provide context-aware execution

---

## 📚 Related Documentation

- **Full Command Reference**: `docs/COMMANDS_REFERENCE.md`
- **Tool Selection Guide**: `docs/TOOL_SELECTION_GUIDE.md`
- **Consolidation Rationale**: `docs/reviews/CONSOLIDATION_RATIONALE.md`
- **Scripts README**: `scripts/README.md`

---

**Last Updated**: 2025-01-11
**Total Commands**: 52
**Status**: Optimized and production-ready
