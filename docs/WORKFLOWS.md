# EasyPost MCP - Workflow Combinations

**Practical workflow combinations for maximum productivity**

## 🚀 Quick Start Workflows

### Fresh Project Setup

```bash
# One-time setup
make setup

# Verify setup
./scripts/test/quick-test.sh
```

### Daily Development Start

**Option 1: Cursor AI Command (Recommended)**

```bash
# Start full stack (backend + frontend + MCP)
/ep-dev

# Backend only
/ep-dev backend

# Frontend only
/ep-dev frontend

# With JIT optimization
/ep-dev backend --jit

# With MCP verification
/ep-dev backend --mcp-verify
```

**Option 2: Makefile**

```bash
# Terminal 1: Start dev servers
make d

# Terminal 2: Watch tests (optional, for TDD)
./scripts/test/watch-tests.sh
```

### macOS Development (Separate Windows)

```bash
# Opens separate Terminal windows for backend/frontend
./scripts/dev/start-dev.sh
```

---

## 💻 Development Workflows

### Standard Development Cycle

**Option 1: Cursor AI Command (Recommended)**

```bash
/ep-dev
# Starts backend + frontend + MCP concurrently
# Auto-reload on changes
# Shows formatted output with service status
```

**Option 2: Makefile**

```bash
make d
# Backend + Frontend running
# Auto-reload on changes
```

**Terminal 2: Watch Tests (TDD)**

```bash
./scripts/test/watch-tests.sh
# Auto-reruns tests on file changes
# Perfect for test-driven development
```

**Terminal 3: Quick Validation**

```bash
# Run periodically (every 5-10 minutes)
./scripts/test/quick-test.sh
# ~10 second health check
```

### Backend-Only Development

**Option 1: Cursor AI Command (Recommended)**

```bash
# Standard mode
/ep-dev backend

# JIT mode (Performance Testing)
/ep-dev backend --jit
# Multi-worker, JIT compilation (Python 3.13+)
# Expect 10-20% performance boost

# With MCP verification
/ep-dev backend --mcp-verify
# Verifies MCP tools after startup
# Shows tool registration status

# Combined
/ep-dev backend --jit --mcp-verify
```

**Option 2: Scripts**

```bash
# Standard mode
./scripts/dev/start-backend.sh
# Single worker, hot reload

# JIT mode
./scripts/dev/start-backend.sh --jit --mcp-verify

# With MCP verification
./scripts/dev/start-backend.sh --mcp-verify
```

### Frontend-Only Development

**Option 1: Cursor AI Command**

```bash
/ep-dev frontend
# Starts React dev server
# Auto-reload on changes
```

**Option 2: Direct Command**

```bash
cd apps/frontend && npm run dev
# Direct Vite dev server
# Fastest option
```

### Docker + Database Development

```bash
./scripts/dev/dev_local.sh
# Starts PostgreSQL in Docker
# Then starts backend + frontend
# Use when you need database features
```

---

## 🧪 Testing Workflows

### Pre-Commit Testing

**Quick Pre-Commit Check**

```bash
make c
# Lint + format + test
# ~20-30 seconds
# Run before every commit
```

**Comprehensive Pre-Commit**

```bash
make c && ./scripts/test/test-full-functionality.sh
# Full quality check + comprehensive tests
# ~3-5 minutes
# Use before major commits
```

### Test-Driven Development (TDD)

**Setup**

```bash
# Terminal 1: Dev servers
make d

# Terminal 2: Watch tests
./scripts/test/watch-tests.sh
```

**Workflow:**

1. Write failing test
2. Watch tests auto-rerun (shows failure)
3. Write implementation
4. Watch tests auto-rerun (shows pass)
5. Refactor if needed

### Continuous Testing

**Quick Validation Loop**

```bash
# Run every 5-10 minutes during development
./scripts/test/quick-test.sh
# ~10 seconds
# Catches issues early
```

**Full Test Suite**

```bash
make t
# Full test suite with parallel execution
# ~30-60 seconds
# Run before committing
```

### Performance Testing

**Benchmark After Changes**

```bash
# After optimization changes
/ep-benchmark --compare
# Or
./scripts/test/benchmark.sh
# Validates performance improvements
# Detects regressions
```

### Coverage Analysis

```bash
make test COV=1
# Generates HTML coverage report
# Opens automatically in browser
# Review uncovered lines
```

---

## ✅ Code Quality Workflows

### Pre-Commit Quality Check

**Standard Pre-Commit**

```bash
make c
# Lint + format + test
# Sequential execution
```

**VS Code Pre-Commit**

```
Ctrl+Shift+P → "Tasks: Run Task" → "✅ Pre-Commit: Run All Checks"
# Same as 'make c' but IDE-integrated
# Problem matchers highlight issues
```

### Individual Quality Steps

**Lint Only**

```bash
make l
# Quick lint check
# ~5 seconds
```

**Format Only**

```bash
make f
# Auto-fix formatting
# ~3 seconds
```

**Lint + Format (No Tests)**

```bash
make l && make f
# Faster than 'make c'
# Use when you know tests pass
```

### Quality Workflow Chain

```bash
# 1. Format code
make f

# 2. Lint check
make l

# 3. Run tests
make t

# 4. If all pass, commit
git add .
git commit -m "feat: your message"
```

---

## 🚀 Release Workflows

### Pre-Release Validation

**Complete Release Check**

```bash
# 1. Code quality
make c

# 2. Comprehensive tests
./scripts/test/test-full-functionality.sh

# 3. Performance benchmarks
./scripts/test/benchmark.sh

# 4. Build production bundles
make build

# 5. Test production build locally
make prod
```

### Production Deployment

**Build + Deploy**

```bash
make build && make prod
# Builds production bundles
# Then starts production servers
```

**Custom Production**

```bash
./scripts/dev/start-prod.sh
# More control over production startup
# Custom environment variables
```

---

## 🔧 Troubleshooting Workflows

### Database Issues

**Reset Database**

```bash
make db-reset
# Drops all tables, recreates schema
# Use when migrations break
```

**Monitor Database**

```bash
./scripts/utils/monitor-database.sh
# Shows active connections
# Query statistics
# Performance monitoring
```

**Create Migration**

```bash
make db-migrate m="description of changes"
# Creates Alembic migration
# Auto-detects model changes
```

### MCP Tools Issues

**MCP Troubleshooting Chain**

```bash
# 1. Check MCP server health
./scripts/utils/mcp-utils.sh health

# 2. Verify tools are registered
./scripts/utils/mcp-utils.sh verify

# 3. Test tools with sample data
./scripts/utils/mcp-utils.sh test

# 4. Restart backend with MCP verification
./scripts/dev/start-backend.sh --mcp-verify
```

### Build Issues

**Clean + Rebuild**

```bash
make clean && make build
# Removes all artifacts
# Fresh build
```

**Clean + Setup**

```bash
make clean && make setup
# Complete reset
# Use when environment is corrupted
```

### Git Issues

**Clean Git History**

```bash
./scripts/utils/clean-git-history.sh
# Removes API keys from history
# ⚠️ Rewrites history (force push required)
```

**Quick Commit + Push**

```bash
make qcp m="feat: your message"
# Adds, commits, and pushes
# Use for quick fixes
```

---

## ⚡ Performance Optimization Workflows

### Benchmark Before/After

**Before Optimization**

```bash
./scripts/test/benchmark.sh > benchmarks-before.txt
# Save baseline
```

**After Optimization**

```bash
./scripts/test/benchmark.sh > benchmarks-after.txt
# Compare with baseline
diff benchmarks-before.txt benchmarks-after.txt
```

**With Cursor AI**

```bash
/ep-benchmark --compare
# Automatic baseline comparison
# Regression detection
```

### JIT Performance Testing

```bash
# Standard mode baseline
./scripts/dev/start-backend.sh
# Run benchmarks

# JIT mode comparison
./scripts/dev/start-backend.sh --jit
# Run benchmarks again
# Compare results (expect 10-20% improvement)
```

---

## 🎯 Context-Specific Workflows

### VS Code Development

**Full VS Code Workflow**

```
1. Option A: Cursor AI Command
   /ep-dev
   - Starts backend + frontend + MCP concurrently
   - Shows formatted output with service status
   - Health checks and environment validation

   Option B: VS Code Task
   Ctrl+Shift+P → "Tasks: Run Task" → "🚀 Dev: Full Stack"
   - Starts backend + frontend
   - IDE-integrated debugging
   - Problem matchers active

2. Develop with breakpoints
   - Set breakpoints in code
   - Debug directly in IDE

3. Ctrl+Shift+P → "Tasks: Run Task" → "🧪 Test: Backend"
   - Run tests with debugging
   - Step through test failures

4. Ctrl+Shift+P → "Tasks: Run Task" → "✅ Pre-Commit: Run All Checks"
   - Quality check before commit
   - IDE highlights issues
```

### Cursor AI Development

**AI-Enhanced Workflow**

```bash
# 1. Start development (Full Stack)
/ep-dev
# Starts backend + frontend + MCP concurrently
# Shows formatted output with service status
# Health checks and environment validation

# Or start specific services
/ep-dev backend --jit --mcp-verify
/ep-dev frontend
/ep-dev mcp

# 2. Context-aware testing
/ep-test
# Auto-detects test type from open file
# Runs relevant tests with parallel execution

# 3. Performance validation
/ep-benchmark
# AI-enhanced benchmarks
# Regression detection
# Compares before/after results
```

### Terminal-Based Development

**Multi-Terminal Setup**

```bash
# Terminal 1: Backend
./scripts/dev/start-backend.sh --mcp-verify

# Terminal 2: Frontend
cd apps/frontend && npm run dev

# Terminal 3: Watch Tests
./scripts/test/watch-tests.sh

# Terminal 4: Quick Checks
watch -n 60 ./scripts/test/quick-test.sh
# Runs quick test every 60 seconds
```

---

## 🔄 Continuous Integration Workflows

### CI/CD Pipeline Simulation

**Local CI Simulation**

```bash
# 1. Setup
make setup

# 2. Lint
make l

# 3. Format check
make f

# 4. Tests
make t

# 5. Build
make build

# 6. Production test
make prod
```

### Fast CI Feedback

**Quick CI Check**

```bash
make l && make f && ./scripts/test/quick-test.sh
# Fast feedback loop
# ~15-20 seconds total
```

---

## 📊 Monitoring Workflows

### Health Monitoring

**Continuous Health Check**

```bash
watch -n 30 ./scripts/test/quick-test.sh
# Runs health check every 30 seconds
# Use during development
```

### Performance Monitoring

**Database Performance**

```bash
./scripts/utils/monitor-database.sh
# Monitor database activity
# Query statistics
# Connection monitoring
```

### MCP Tools Monitoring

**MCP Health Check**

```bash
watch -n 60 ./scripts/utils/mcp-utils.sh health
# Checks MCP server health every minute
```

---

## 🎓 Learning Workflows

### Understanding Codebase

**Explore with Tests**

```bash
# 1. Run all tests to see what exists
make t

# 2. Watch tests to see what runs
./scripts/test/watch-tests.sh

# 3. Run specific test file
cd apps/backend && pytest tests/unit/test_specific.py -v
```

### Testing New Features

**Feature Development Workflow**

```bash
# 1. Start dev environment
make d

# 2. Watch tests
./scripts/test/watch-tests.sh

# 3. Write tests first (TDD)
# 4. Implement feature
# 5. Quick validation
./scripts/test/quick-test.sh

# 6. Full test suite
make t

# 7. Quality check
make c

# 8. Commit
git add . && git commit -m "feat: new feature"
```

---

## 🚨 Emergency Workflows

### Quick Recovery

**Reset Everything**

```bash
make clean && make setup && make d
# Complete reset
# Fresh start
```

### Database Recovery

```bash
make db-reset
# Resets database to clean state
# Use when data is corrupted
```

### Build Recovery

```bash
make clean && make build
# Removes corrupted artifacts
# Fresh build
```

---

## 💡 Pro Workflow Tips

### 1. Use Aliases Daily

```bash
make d    # Instead of 'make dev'
make t    # Instead of 'make test'
make c    # Instead of 'make check'
```

### 2. Parallel Terminals

- Terminal 1: Dev servers (`make d`)
- Terminal 2: Watch tests (`watch-tests.sh`)
- Terminal 3: Quick checks (`quick-test.sh`)

### 3. Pre-Commit Always

```bash
make c && git commit -m "feat: ..."
# Only commits if quality checks pass
```

### 4. Quick Validation Loop

```bash
# Run every 5-10 minutes
./scripts/test/quick-test.sh
# Catches issues early
```

### 5. Context-Aware Commands

- Use `/ep-test` when in Cursor (auto-detects file)
- Use VS Code tasks when debugging
- Use scripts when you need specific control

### 6. Performance Validation

```bash
# After optimization changes
/ep-benchmark --compare
# Validates improvements
```

---

## 📋 Workflow Checklist

### Daily Development

- [ ] `make d` - Start dev servers
- [ ] `./scripts/test/watch-tests.sh` - Watch tests (optional)
- [ ] Develop features
- [ ] `./scripts/test/quick-test.sh` - Quick validation (periodic)
- [ ] `make c` - Quality check before commit

### Pre-Commit

- [ ] `make c` - Lint + format + test
- [ ] Review changes
- [ ] Commit if all pass

### Pre-Release

- [ ] `make c` - Quality check
- [ ] `./scripts/test/test-full-functionality.sh` - Comprehensive tests
- [ ] `./scripts/test/benchmark.sh` - Performance validation
- [ ] `make build` - Production build
- [ ] `make prod` - Test production locally

### Troubleshooting

- [ ] Identify issue
- [ ] Run relevant diagnostic command
- [ ] Apply fix
- [ ] Verify with `quick-test.sh`
- [ ] Full validation with `make c`

---

## 🎯 Recommended Workflows by Scenario

### Scenario: "I'm starting a new feature"

```bash
make d                                    # Start dev
./scripts/test/watch-tests.sh            # Watch tests (separate terminal)
# Develop feature...
./scripts/test/quick-test.sh             # Quick validation
make c                                    # Quality check
git commit -m "feat: new feature"
```

### Scenario: "I'm fixing a bug"

```bash
make d                                    # Start dev
./scripts/test/watch-tests.sh            # Watch tests
# Fix bug...
./scripts/test/quick-test.sh             # Verify fix
make t                                    # Full test suite
make c                                    # Quality check
git commit -m "fix: bug description"
```

### Scenario: "I'm optimizing performance"

```bash
./scripts/test/benchmark.sh > before.txt  # Baseline
# Make optimizations...
./scripts/test/benchmark.sh > after.txt  # After
diff before.txt after.txt                # Compare
make c                                    # Quality check
git commit -m "perf: optimization description"
```

### Scenario: "I'm preparing for release"

```bash
make c                                    # Quality check
./scripts/test/test-full-functionality.sh # Comprehensive tests
./scripts/test/benchmark.sh              # Performance validation
make build                                # Production build
make prod                                 # Test production
git tag v1.0.0                           # Tag release
```

---

**Last Updated**: 2025-01-11
**Total Workflows**: 20+ combinations
**Status**: Production-ready workflows
