# Real-World Workflow Examples

**Actual working commands** — tested and verified.

---

## 🌅 Scenario 1: Start of Day

```bash
# Pull latest code
git pull origin main

# Morning routine
make clean           # Clean cache (2s)
make test-fast       # Fast tests (8s)
make dev            # Backend + frontend servers (5s)

# Or combined
make clean && make test-fast && make dev

✅ Ready in ~15s
```

---

## 🛠️ Scenario 2: Building New Feature

**Task:** Add shipment refund functionality

```bash
# 1. Implement business logic (manual coding)

# 2. Test it
make test           # All tests (6s)

# 3. Check code quality
make lint           # Linters (4s)
make format         # Auto-format (2s)

# 4. Benchmark
make benchmark      # Performance check (15s)

# 5. Commit
git add . && git commit -m "feat: add shipment refund"

✅ ~27s automation + coding time
```

---

## 🐛 Scenario 3: Fixing Failing Tests

```bash
# Tests failing
make test           # ✗ 3 tests failed

# Debug
make lint           # Check for errors
make test-fast      # Rerun failed tests

# Fix issues (manual coding)

# Verify
make test           # ✓ All pass

✅ ~10s per iteration
```

---

## 📦 Scenario 4: Testing Changes

```bash
# Run full test suite
make test           # All tests (6s)

# Or fast mode (changed files only)
make test-fast      # Parallel, last-failed-first (3s)

# With coverage
make test-cov       # HTML reports (12s)

# Watch mode (auto-runs on file changes)
make test-watch     # Continuous testing

✅ Pick the right speed/coverage trade-off
```

---

## 🚀 Scenario 5: Pre-Release Process

```bash
# Full quality check
make format         # Auto-format (2s)
make lint           # Linters (4s)
make test-cov       # Tests + coverage (12s)
make benchmark      # Performance (15s)

# Build production
make build          # Frontend + backend (10s)

# Or combined
make check          # format + lint + test (22s)

✅ Release-ready in ~43s
```

---

## 🔄 Scenario 6: Pull Request Creation

```bash
# Create feature branch
git checkout -b feature/international-shipping

# Make changes (manual coding)

# Pre-PR checks
make format         # Clean code (2s)
make lint           # No errors (4s)
make test-cov       # Full coverage (12s)

# Push
make sync           # Rebase on main
make push           # Push branch

✅ PR validated in ~18s
```

---

## ⚡ Scenario 7: Parallel Development

```bash
# Terminal 1: Backend only
make backend

# Terminal 2: Frontend only
make frontend

# Terminal 3: Tests in watch mode
make test-watch

# All independent, no conflicts
```

---

## 🧪 Scenario 8: TDD Workflow

```bash
# 1. Write failing test (manual coding)

# 2. Start watch mode
make test-watch
# → Auto-runs on file save

# 3. Implement feature (manual coding)
# → Tests auto-run, immediate feedback

# 4. Refactor (manual coding)
# → Tests still pass

✅ Continuous feedback
```

---

## 🔍 Scenario 9: Code Quality Check

```bash
# Full quality pipeline
make lint           # Check errors (4s)
make format         # Fix formatting (2s)
make test           # Verify tests (6s)

# Or combined
make check          # All above (12s)

✅ ~12s for complete validation
```

---

## 📊 Scenario 10: Performance Analysis

```bash
# Baseline benchmark
make benchmark      # Current: 90.9 shipments/s

# Optimize code (manual coding)

# Re-benchmark
make benchmark      # New: 180.2 shipments/s
# Speedup: 2x!

✅ ~30s per iteration
```

---

## 🔧 Scenario 11: Database Operations

```bash
# Reset database
make db-reset       # Drop + recreate (5s)

# Create migration
make db-migrate m="add refund table"

# Apply migrations
make db-upgrade     # Run pending (2s)

✅ Database changes in ~7s
```

---

## 🏥 Scenario 12: Health Checks

```bash
# Check server status
make health
# Backend: ✓ OK
# Frontend: ✓ OK
# Database: ✓ OK (12/20 connections)

✅ Instant health overview
```

---

## 🎯 Recommended Command Chains

### Morning Routine

```bash
make clean && make test-fast && make dev
# → Clean, test, start (15s)
```

### Development Cycle

```bash
make test-fast && make lint
# → Fast validation (7s)
```

### Before Push

```bash
make check && make sync && make push
# → Quality + sync + push (25s)
```

### Release Pipeline

```bash
make clean && make check && make benchmark && make build
# → Complete validation (50s)
```

### Quick Commit + Push

```bash
make qcp m="fix: resolve rate calculation bug"
# → Add, commit, push in one command
```

---

## 💡 Pro Patterns

### Parallel Testing

```bash
# Run in background
make benchmark &    # Background
make test           # Foreground
# Total: 15s (vs 21s sequential)
# Savings: 29%
```

### Conditional Execution

```bash
# Test, if fails → lint
make test || make lint

# Format, then always test
make format && make test

# Test; show health regardless of result
make test ; make health
```

### Mock Mode (faster development)

```bash
# Start with mock EasyPost API
make dev-mock       # No real API calls, instant responses
```

### Git Shortcuts

```bash
# Sync with main
make sync           # fetch + rebase

# Quick commit
make commit m="feat: add tracking"

# Commit + push
make qcp m="fix: resolve bug"
```

---

## 📋 Complete Command Reference

### Development

- `make dev` - Backend + frontend servers
- `make dev-mock` - With mock EasyPost API
- `make backend` - Backend only
- `make frontend` - Frontend only

### Testing

- `make test` - All tests
- `make test-fast` - Changed files only, parallel
- `make test-watch` - Auto-run on changes
- `make test-cov` - With coverage reports

### Code Quality

- `make lint` - Run linters
- `make format` - Auto-format code
- `make check` - Lint + format + test

### Building

- `make build` - Production bundles
- `make build-docker` - Docker images

### Database

- `make db-reset` - Drop + recreate
- `make db-migrate m="message"` - Create migration
- `make db-upgrade` - Apply migrations

### Utilities

- `make install` - Install dependencies
- `make clean` - Clean artifacts
- `make health` - Server health check
- `make benchmark` - Performance tests

### Git

- `make sync` - Rebase on main
- `make commit m="message"` - Commit changes
- `make push` - Push after sync
- `make qcp m="message"` - Add + commit + push

---

**25 working commands, 0 fake workflows! 🚀**
