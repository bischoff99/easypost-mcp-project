# Real-World Workflow Examples

Based on research: GitHub, StackOverflow, industry best practices

---

## 🌅 Scenario 1: Start of Day

```bash
# Pull latest code
git pull origin main

# Run morning workflow
/workflow:morning
# → Cleans cache (2s)
# → Fast tests (8s)
# Total: 10s

# Start development
/workflow:ep-dev
# → Backend + frontend servers
# Total: 5s

# Verify everything works
/workflow:ep-test
# → 28/28 tests passed in 6s

✅ Ready to code in 21 seconds
```

---

## 🛠️ Scenario 2: Building New Feature

**Task:** Add shipment refund functionality

```bash
# 1. Create MCP tool
/workflow:ep-mcp-tool RefundRequest create_refund
# → Generates model, tool, tests (30s)

# 2. Implement business logic
# (manual coding)

# 3. Test it
/workflow:ep-test
# → All tests pass (6s)

# 4. Optimize
/workflow:optimize backend/src/mcp/tools/refund_tools.py
# → Applies M3 Max optimizations (30s)

# 5. Benchmark
/workflow:ep-benchmark
# → Performance validated (15s)

# 6. Pre-commit check
/workflow:pre-commit
# → Format, lint, test (15s)

# 7. Commit
git add . && git commit -m "feat: add shipment refund functionality"

✅ Complete feature in ~96s automation + coding time
```

---

## 🐛 Scenario 3: Fixing Failing Tests

```bash
# Tests are failing
/workflow:ep-test
# ✗ 3 tests failed

# Debug workflow
/workflow:ep-debug
# → Lints code
# → Runs integration tests
# → Explains errors with AI

# Apply suggested fix
/fix @errors
# → Auto-fixes issues

# Verify fix
/workflow:ep-test
# ✓ All tests pass

✅ Debug cycle: ~40s
```

---

## 📦 Scenario 4: Testing Bulk Operations

```bash
# Test bulk shipment creation (parallel)
/workflow:ep-bulk-test
# → Creates 10 shipments with 32 workers (0.11s)
# → Tracks 50 packages with 32 workers (0.28s)
# Total: 12s

# Verify rate accuracy
/workflow:ep-rate-check
# → Compares USPS vs UPS vs FedEx
# → Analytics on pricing trends
# Total: 18s

# Run benchmarks
/workflow:ep-benchmark
# → Full performance suite
# Total: 15s

✅ Complete bulk validation in 45s
```

---

## 🚀 Scenario 5: Pre-Release Process

```bash
# Full pre-release check
/workflow:ep-pre-release
# Steps:
#   1. make format (3s)
#   2. make lint (4s)
#   3. /ep-test --coverage (12s)
#   4. /ep-benchmark (15s)
#   5. /secure backend/src/ (20s)
# Total: 60s

# Additional validation
/workflow:ep-full
# → All functionality tests (30s)

# Final ship check
/workflow:ship
# → Complete quality pipeline (45s)

✅ Release-ready in 135s
```

---

## 🔄 Scenario 6: Pull Request Creation

```bash
# Create feature branch
git checkout -b feature/international-shipping

# Make changes
# (manual coding)

# Before creating PR
/workflow:pre-pr
# → make format (3s)
# → make lint (4s)
# → /test --coverage (15s)
# → /secure @git-diff (12s)
# Total: 40s

# Push and create PR
git push origin feature/international-shipping

✅ PR ready with full validation
```

---

## ⚡ Scenario 7: Parallel Development

```bash
# Work on multiple features simultaneously

# Terminal 1: Create shipment refund tool
/workflow:ep-mcp-tool RefundRequest refund

# Terminal 2: Create customs info tool  
/workflow:ep-mcp-tool CustomsInfo customs

# Terminal 3: Run tests in watch mode
/workflow:tdd

# All run in parallel - no waiting!
```

---

## 🧪 Scenario 8: TDD Workflow

```bash
# 1. Write failing test
# (edit test file)

# 2. Start TDD workflow
/workflow:tdd
# → Runs tests in watch mode
# → Auto-runs on file changes

# 3. Implement feature
# (edit code)
# → Tests auto-run
# → See immediate feedback

# 4. Refactor
# (improve code)
# → Tests still pass

# 5. Done!
# Exit watch mode, commit

✅ Continuous feedback loop
```

---

## 🔒 Scenario 9: Security Audit

```bash
# Run security workflow
/workflow:security
# → /secure @file (15s)
# → make lint (4s)
# → /test (6s)
# Total: 25s

# If issues found
/fix @security-issues

# Verify fix
/workflow:security
# ✓ All checks pass

✅ Security validated in 50s
```

---

## 📊 Scenario 10: Performance Optimization

```bash
# Profile current performance
/workflow:ep-benchmark
# Baseline: 90.9 shipments/s

# Optimize code
/workflow:optimize backend/src/mcp/tools/bulk_tools.py
# → Applies M3 Max optimizations (30s)

# Re-benchmark
/workflow:ep-benchmark
# Improved: 180.2 shipments/s
# Speedup: 2x!

✅ Performance doubled in 45s
```

---

## 🎯 Recommended Chains

### Morning Routine
```bash
/workflow:morning && /workflow:ep-dev
# → Clean, test, start servers (15s)
```

### Development Cycle
```bash
/workflow:ep-test && /workflow:pre-commit
# → Test + quality check (21s)
```

### Before Push
```bash
/workflow:pre-commit && /workflow:pre-push
# → Double validation (40s)
```

### Release Pipeline
```bash
/workflow:ship && /workflow:ep-pre-release && /workflow:full-check
# → Triple validation (165s)
```

---

## 💡 Pro Patterns

### Parallel Testing
```bash
# Test + benchmark simultaneously
/workflow:ep-test & /workflow:ep-benchmark
# Time: 15s (vs 21s sequential)
# Savings: 29%
```

### Conditional Execution
```bash
# Test, if fails → debug
/workflow:ep-test || /workflow:ep-debug

# Optimize, if fails → explain
/workflow:optimize || /explain @selection
```

### Always Execute
```bash
# Test; show stats regardless
/workflow:ep-test ; /session:stats

# Benchmark; show results even if fails
/workflow:ep-benchmark ; cat benchmark-results.json
```

---

**22 workflows ready for production use! 🚀**
