# Current Working Workflows

**Status:** ✅ All commands in this file are fully implemented and tested

Last updated: 2025-11-04

---

## Quick Reference

| Command | What It Does | Time |
|---------|-------------|------|
| `make dev` | Start backend + frontend | 5s |
| `make test` | Run all tests | 15s |
| `make test-fast` | Fast tests (changed files) | 6s |
| `make benchmark` | Performance benchmarks | 15s |
| `make format` | Auto-format code | 3s |
| `make lint` | Run linters | 4s |
| `make check` | Format + lint + test | 22s |
| `make build` | Production build | 30s |
| `make clean` | Clean artifacts | 2s |
| `make health` | Server health check | 1s |

---

## 🌅 Scenario 1: Start of Day

```bash
# Pull latest code
git pull origin main

# Clean and start
make clean && make dev
# Total: ~7s to running servers
```

---

## 🛠️ Scenario 2: Building a Feature

```bash
# 1. Start development servers
make dev

# 2. Work on your code
# (manual coding in another terminal)

# 3. Test your changes
make test-fast
# → Runs tests for changed files only (6s)

# 4. Format and lint
make format && make lint
# → Auto-format + check (7s)

# 5. Full validation before commit
make check
# → Format + lint + full test suite (22s)

# 6. Commit
git add . && git commit -m "feat: your feature"
```

---

## 🐛 Scenario 3: Fixing Failing Tests

```bash
# Run tests to see failures
make test

# Fix the code
# (manual editing)

# Fast re-test (only changed files)
make test-fast
# → Much faster feedback loop

# Full test once working
make test
```

---

## 📦 Scenario 4: Testing API Changes

```bash
# Start backend only
make backend

# In another terminal: test the API
curl -X POST http://localhost:8000/shipments \
  -H "Content-Type: application/json" \
  -d @test-data.json

# Check health
make health
```

---

## 🚀 Scenario 5: Pre-Release Process

```bash
# Clean everything
make clean

# Full quality check
make check
# → Format + lint + test (22s)

# Run benchmarks
make benchmark
# → Performance validation (15s)

# Build production
make build
# → Creates optimized bundles (30s)

# Total: ~67s to release-ready
```

---

## 🔄 Scenario 6: Pull Request Creation

```bash
# Before creating PR
make format  # Auto-format (3s)
make lint    # Check style (4s)
make test    # Run tests (15s)

# Or use the combined command
make check   # All of the above (22s)

# Push
git push origin feature/my-feature
```

---

## ⚡ Scenario 7: Parallel Development

```bash
# Terminal 1: Run development servers
make dev

# Terminal 2: Watch tests
make test-watch
# → Auto-runs tests on file changes

# Terminal 3: Edit code
# (your favorite editor)
```

---

## 🧪 Scenario 8: TDD Workflow

```bash
# Start test watch mode
make test-watch
# → Tests auto-run on every file save

# Now code:
# 1. Write failing test
# 2. See it fail (automatic)
# 3. Write implementation
# 4. See it pass (automatic)
# 5. Refactor
# 6. Tests still pass (automatic)
```

---

## 📊 Scenario 9: Performance Testing

```bash
# Run full benchmark suite
make benchmark

# Results saved to:
# - backend/benchmark-results.json
# - Console output with timing

# Start servers and test manually
make dev
# (test your endpoints)
```

---

## 🔨 Scenario 10: Database Operations

```bash
# Reset database
make db-reset
# → Downgrade to base, upgrade to head

# Create new migration
make db-migrate m="add user table"
# → Creates migration file

# Apply migrations
make db-upgrade
# → Runs all pending migrations
```

---

## 🎯 Recommended Chains

### Morning Routine
```bash
make clean && make test-fast && make dev
# → Clean, quick test, start (13s)
```

### Development Cycle
```bash
make test-fast && make format
# → Test + format (9s)
```

### Before Commit
```bash
make check
# → Format + lint + test (22s)
```

### Before Push
```bash
make check && make benchmark
# → Quality + performance validation (37s)
```

### Release Pipeline
```bash
make clean && make check && make benchmark && make build
# → Complete release validation (69s)
```

---

## 💡 Pro Patterns

### Command Chaining

**Sequential execution** (stop on error):
```bash
make test && make build
# Runs build only if tests pass
```

**Sequential execution** (always continue):
```bash
make test ; make build
# Runs build regardless of test result
```

**Conditional execution** (run second if first fails):
```bash
make test || echo "Tests failed, continuing anyway"
```

### Parallel Execution

**Background jobs** (run multiple commands simultaneously):
```bash
make test & make lint & wait
# Runs test and lint in parallel, waits for both
# Time: ~15s (vs 19s sequential)
# Savings: 21%
```

**In scripts** (proper cleanup):
```zsh
#!/usr/bin/env zsh
set -euo pipefail

cleanup() {
    kill 0 2>/dev/null || true
}

trap cleanup EXIT INT TERM

cmd1 & cmd2 & wait
```

### Makefile Parallel Execution

**Use `make -jN` for parallel targets:**
```bash
make -j4 test-fast lint format
# Runs 4 targets in parallel
```

**Built-in parallel targets** (already optimized):
- `make test-fast` - Backend and frontend run in parallel
- `make lint` - Backend and frontend run in parallel
- `make format` - Backend and frontend run in parallel

### Git Shortcuts
```bash
# Quick commit and push
make qcp m="your commit message"
# → Add all, commit, push

# Sync with main
make sync
# → Fetch and rebase
```

---

## 🔍 Health Monitoring

### Check Server Health
```bash
make health
# Shows:
# - Backend status (JSON health data)
# - Frontend status (OK/Not running)
```

### Full Status Check
```bash
# Check everything
curl http://localhost:8000/health | jq '.'
# Shows:
# - Status
# - Database connection pool
# - Request ID
# - Timestamp
```

---

## 📦 Available Make Targets

### Development
- `make dev` - Start backend + frontend servers
- `make dev-mock` - Start with mock EasyPost API
- `make backend` - Start backend only
- `make frontend` - Start frontend only

### Testing
- `make test` - Run all tests
- `make test-fast` - Run tests for changed files only
- `make test-watch` - Run tests in watch mode
- `make test-cov` - Run tests with coverage report

### Building
- `make build` - Build production bundles
- `make build-docker` - Build Docker images

### Code Quality
- `make lint` - Run linters
- `make format` - Auto-format code
- `make check` - Run all quality checks (format + lint + test)

### Utilities
- `make install` - Install all dependencies
- `make clean` - Clean build artifacts
- `make health` - Check server health
- `make benchmark` - Run performance benchmarks

### Database
- `make db-reset` - Reset database to clean state
- `make db-migrate m="message"` - Create new migration
- `make db-upgrade` - Apply pending migrations

### Git
- `make sync` - Fetch and rebase with origin/main
- `make commit m="message"` - Stage all and commit
- `make push` - Sync and push current branch
- `make qcp m="message"` - Quick commit and push

---

## 🔧 Best Practices

### zsh Script Structure

**Standard template:**
```zsh
#!/usr/bin/env zsh

# Exit on error, undefined vars, pipe failures
set -euo pipefail

# Cleanup handler
cleanup() {
    echo "Cleaning up..."
    kill 0 2>/dev/null || true
}

trap cleanup EXIT INT TERM

# Your script logic here
```

### Error Handling

**Always use `set -euo pipefail`:**
- `-e`: Exit immediately if command fails
- `-u`: Exit on undefined variables
- `-o pipefail`: Exit if any command in pipeline fails

**Check exit codes:**
```zsh
if command; then
    echo "Success"
else
    echo "Failed" >&2
    exit 1
fi
```

**Intentional failures:**
```zsh
rm -f file.txt || true  # Don't fail if file doesn't exist
```

### Parallel Execution Patterns

**Background jobs with cleanup:**
```zsh
#!/usr/bin/env zsh
set -euo pipefail

cleanup() {
    kill $PID1 $PID2 2>/dev/null || true
}

trap cleanup EXIT INT TERM

cmd1 & PID1=$!
cmd2 & PID2=$!
wait
```

**Makefile parallel:**
- Use `&` + `wait` for background processes
- Use `make -jN` for parallel targets
- Always use `trap` for cleanup

---

## 📚 Additional Resources

- **Full Makefile:** See `Makefile` in project root
- **Cursor Commands:** See `.cursor/commands/` directory
- **Project Config:** See `.cursor/rules/` for coding standards
- **Future Workflows:** See `WORKFLOW-EXAMPLES.md` for aspirational templates

---

**All commands tested and working as of 2025-11-04** ✅
