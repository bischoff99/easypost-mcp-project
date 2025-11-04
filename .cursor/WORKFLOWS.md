# Workflow System - Complete Guide

**Status:** ✅ 22 workflows configured  
**Location:** `.dev-config.json` → `workflows`  
**M3 Max Optimized:** 16 parallel workers

---

## Quick Start

```bash
# List all workflows
/workflow:list

# Run workflow
/workflow:morning
/workflow:pre-commit
/workflow:ep-test

# Chain workflows
/workflow:morning && /workflow:ep-dev
```

---

## 📊 Workflow Categories

### Universal Workflows (10)
Work across ANY project - Python, JS, Go, Rust, etc.

### EasyPost Workflows (12)
Domain-specific for shipping/logistics operations

---

## 🌍 Universal Workflows

### Daily Workflows (2)

#### `/workflow:morning` (10s)
**Purpose:** Start-of-day routine  
**Commands:** `/clean --cache-only && /test --fast`  
**What it does:**
- Cleans cache files (parallel)
- Runs fast tests on critical paths
- Ensures clean state

#### `/workflow:tdd` (continuous)
**Purpose:** Test-driven development  
**Commands:** `/test @selection --watch`  
**What it does:**
- Watches selected test file
- Auto-runs on changes
- Continuous feedback

### Quality Workflows (4)

#### `/workflow:pre-commit` (15s)
**Purpose:** Before committing code  
**Commands:** `make format && make lint && /test @git-staged`  
**What it does:**
- Auto-formats code (Black/Prettier)
- Runs linters (Ruff/ESLint)
- Tests only staged changes
**Use:** Before every `git commit`

#### `/workflow:pre-push` (25s)
**Purpose:** Before pushing to remote  
**Commands:** `/test --coverage && make lint && /fix`  
**What it does:**
- Full test suite with coverage
- Lint check
- Auto-fix issues
**Use:** Before `git push`

#### `/workflow:pre-pr` (40s)
**Purpose:** Before creating pull request  
**Commands:** `make format && make lint && /test --coverage && /secure @git-diff`  
**What it does:**
- Format + lint entire codebase
- Full test suite with coverage report
- Security audit on changes
**Use:** Before creating PR

#### `/workflow:full-check` (60s)
**Purpose:** Complete codebase validation  
**Commands:** `/clean && make format && make lint && /test --coverage && /optimize`  
**What it does:**
- Cleans project
- Formats all code
- Lints all code
- Full test suite with coverage
- Performance optimization
**Use:** Before major releases

### Development Workflows (2)

#### `/workflow:debug` (20s)
**Purpose:** Debug failing code  
**Commands:** `/test || (/explain @errors && /fix @errors)`  
**What it does:**
- Runs tests
- If fails: Explains error + suggests fix
**Use:** When tests are failing

#### `/workflow:optimize` (30s)
**Purpose:** Performance optimization  
**Commands:** `/optimize @selection && /test --benchmark`  
**What it does:**
- Applies M3 Max optimizations
- Runs performance benchmarks
**Use:** When optimizing code

### Release Workflows (2)

#### `/workflow:ship` (45s)
**Purpose:** Prepare for deployment  
**Commands:** `/fix && /test --coverage && /optimize && make lint`  
**What it does:**
- Fixes all issues
- Full test coverage
- Performance optimization
- Final lint check
**Use:** Before deploying to production

#### `/workflow:security` (25s)
**Purpose:** Security audit  
**Commands:** `/secure @file && make lint && /test`  
**What it does:**
- Security vulnerability scan
- Lint for security issues
- Run security-related tests
**Use:** Regular security checks

---

## 🚢 EasyPost-Specific Workflows

### Development Workflows (2)

#### `/workflow:ep-dev` (5s)
**Purpose:** Start EasyPost dev environment  
**Commands:** `make dev`  
**What it does:**
- Starts backend (FastMCP server on :8000)
- Starts frontend (React/Vite on :5173)
- Hot-reload enabled
**Use:** Daily development startup

#### `/workflow:ep-mcp-tool <Model> <name>` (30s)
**Purpose:** Create new MCP tool  
**Commands:** `/ep-mcp $1 $2 && /test backend/tests/`  
**Example:** `/workflow:ep-mcp-tool RefundRequest refund_shipment`  
**What it does:**
- Generates Pydantic model
- Creates tool function
- Adds tests
- Registers in server.py
**Use:** Adding new MCP tools

### Testing Workflows (4)

#### `/workflow:ep-test` (6s)
**Purpose:** Standard test suite  
**Commands:** `/ep-test`  
**What it does:**
- Runs pytest with 16 workers
- Unit + integration tests
- Fast feedback
**Use:** After code changes

#### `/workflow:ep-test-all` (8s)
**Purpose:** Parallel test execution  
**Commands:** `/ep-test unit & /ep-test integration`  
**What it does:**
- Runs unit & integration in parallel
- Uses 2 processes × 16 workers each
- Maximum parallelization
**Use:** Full validation

#### `/workflow:ep-parallel-test` (8s)
**Purpose:** All test types simultaneously  
**Commands:** `/test backend/tests/unit & /test backend/tests/integration & /ep-benchmark`  
**What it does:**
- 3 parallel processes
- Unit, integration, benchmarks
- Max M3 Max utilization
**Use:** Complete parallel testing

#### `/workflow:ep-full` (30s)
**Purpose:** Complete functionality test  
**Commands:** `/ep-test && /ep-benchmark && /bulk-create test && /track-batch test`  
**What it does:**
- All tests
- Performance benchmarks
- Bulk operations test
- Tracking test
**Use:** Pre-deployment validation

### Performance Workflows (2)

#### `/workflow:ep-benchmark` (15s)
**Purpose:** Performance benchmarking  
**Commands:** `/ep-benchmark && make benchmark`  
**What it does:**
- Bulk creation benchmark
- Tracking benchmark
- Analytics benchmark
- Parsing performance
**Use:** After optimization changes

#### `/workflow:ep-optimize` (25s)
**Purpose:** Optimize shipping operations  
**Commands:** `/shipping-optimize && /ep-benchmark`  
**What it does:**
- Analyzes shipping code
- Applies optimizations
- Benchmarks improvements
**Use:** Performance optimization

### Domain Testing (2)

#### `/workflow:ep-bulk-test` (12s)
**Purpose:** Test bulk operations  
**Commands:** `/bulk-create test-data.csv && /track-batch tracking-numbers.txt`  
**What it does:**
- Tests bulk shipment creation
- Tests batch tracking
- Validates parallel processing
**Use:** Bulk operation validation

#### `/workflow:ep-rate-check` (18s)
**Purpose:** Verify rate accuracy  
**Commands:** `/carrier-compare test-shipment && /analytics-deep rates`  
**What it does:**
- Compares rates across carriers
- Deep analytics on pricing
- Validates rate calculation
**Use:** Rate accuracy verification

### Debugging Workflows (1)

#### `/workflow:ep-debug` (20s)
**Purpose:** Debug EasyPost API issues  
**Commands:** `/ep-lint && /test integration || /explain @errors`  
**What it does:**
- Runs EasyPost-specific linting
- Runs integration tests
- If fails: Explains errors
**Use:** API troubleshooting

### Release Workflows (1)

#### `/workflow:ep-pre-release` (60s)
**Purpose:** Pre-release quality gate  
**Commands:** `make format && make lint && /ep-test --coverage && /ep-benchmark && /secure backend/src/`  
**What it does:**
- Format all code
- Lint all code
- Full coverage report (target: 80%)
- Performance benchmarks
- Security audit
**Use:** Before every release

---

## 🔗 Chaining Workflows

### Sequential Execution
```bash
# Morning → Dev → Test
/workflow:morning && /workflow:ep-dev && /workflow:ep-test

# Pre-commit → Pre-push
/workflow:pre-commit && /workflow:pre-push
```

### Parallel Execution
```bash
# Test + Benchmark simultaneously
/workflow:ep-test & /workflow:ep-benchmark

# Multiple tools
/workflow:ep-mcp-tool Refund refund & /workflow:ep-mcp-tool CustomsInfo customs
```

### Fallback Execution
```bash
# Test, or debug if fails
/workflow:ep-test || /workflow:ep-debug

# Optimize, or explain if fails
/workflow:optimize || /explain @selection
```

---

## ⚡ Performance Metrics

```
Workflow               Sequential    Parallel    Speedup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ep-test                30s           6s          5.0x
ep-test-all            14s           8s          1.8x
ep-parallel-test       25s           8s          3.1x
ep-full                90s           30s         3.0x
```

---

## 📋 Workflow Checklist

### Daily Development
- [ ] `/workflow:morning` - Start of day
- [ ] `/workflow:ep-dev` - Start servers
- [ ] `/workflow:ep-test` - After changes
- [ ] `/workflow:pre-commit` - Before commits

### Before Push
- [ ] `/workflow:pre-push` - Quality check
- [ ] `/workflow:ep-test-all` - Full tests

### Before PR
- [ ] `/workflow:pre-pr` - Complete check
- [ ] `/workflow:ep-full` - All functionality

### Before Release
- [ ] `/workflow:ep-pre-release` - Quality gate
- [ ] `/workflow:ship` - Final validation

---

## 🎯 Best Practices

1. **Use specific workflows** - Don't run full-check for every commit
2. **Chain appropriately** - Use && for dependencies, & for parallelism
3. **Watch output** - Monitor which steps fail
4. **Customize** - Add your own workflows to config
5. **Profile** - Check estimated_time vs actual

---

**22 workflows configured and ready! 🚀**
