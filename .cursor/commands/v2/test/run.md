---
name: run
category: test
description: Run tests with parallel execution and smart detection
allowed-tools: [Read, Grep, Bash, mcp_Desktop_Commander_start_process]
requires-approval: false
context-aware: true
arguments:
  - name: target
    type: string
    required: false
    default: "@git-diff || ."
    description: Test target (path, @git-diff, @file, @selection)
  - name: workers
    type: integer
    required: false
    default: 16
    min: 1
    max: 64
    description: Parallel workers (M3 Max: 16-32)
  - name: coverage
    type: boolean
    required: false
    default: false
    description: Generate coverage report
estimated-time: 4-6s
estimated-tokens: 800-1500
m3-max-optimized: true
version: 2.0
---

# /test:run

Execute tests with intelligent parallel processing, automatic framework detection, and context-aware test selection. Optimized for M3 Max with 16-32 worker processes.

## Usage

```bash
# Auto-detect and run all tests
/test:run

# Specific directory
/test:run backend/tests/

# Changed files only
/test:run @git-diff

# Current file
/test:run @file

# With coverage
/test:run --coverage

# Custom workers
/test:run --workers=32
```

## Auto-Detection

Automatically detects test framework and runs appropriately:

### Python (pytest)
```bash
/test:run backend/tests/

# Executes:
pytest backend/tests/ -n 16 -v --tb=short
# 16 parallel workers on M3 Max
# ✅ 45 tests pass in 4.2s
```

### JavaScript (vitest)
```bash
/test:run frontend/src/

# Executes:
vitest run --threads 20 frontend/src/
# 20 parallel threads
# ✅ 128 tests pass in 3.8s
```

### Go
```bash
/test:run ./...

# Executes:
go test -parallel 16 -v ./...
# 16 parallel tests
# ✅ All tests pass in 2.1s
```

## Context-Aware Test Selection

### @git-diff - Changed Files
```bash
/test:run @git-diff

# Finds:
# - auth.py (modified)
# - service.py (modified)
#
# Runs:
# - test_auth.py (related test)
# - test_service.py (related test)
# - test_integration.py (integration tests)
#
# Smart: Runs affected tests only
# ✅ 12 tests pass in 1.8s (vs 45 tests in 4.2s)
```

### @selection - Current Selection
```bash
# User selects function in editor:
def calculate_total(items, discount=0):
    return sum(item.price for item in items) * (1 - discount)

# Command:
/test:run @selection

# AI finds:
# - test_calculate_total in test_pricing.py
# Runs only that test
# ✅ 3 tests pass in 0.5s
```

### @file - Current File
```bash
# Editor open: backend/src/services/auth_service.py
/test:run @file

# Runs: backend/tests/services/test_auth_service.py
# ✅ 8 tests pass in 1.2s
```

## Parallel Optimization (M3 Max)

### Performance Cores
```bash
/test:run --workers=12

# Uses 12 performance cores
# Optimal for CPU-bound tests
# Result: 4.2s (vs 45s sequential)
```

### All Cores
```bash
/test:run --workers=16

# Uses all 16 cores
# Optimal for I/O-bound tests
# Result: 3.8s (vs 60s sequential)
```

### Hyperthreading
```bash
/test:run --workers=32

# Uses 32 threads (2x cores)
# Optimal for async/network tests
# Result: 2.9s (vs 60s sequential)
```

## Smart Test Detection

### Detects Related Tests
```python
# Modified: backend/src/auth.py
/test:run @git-diff

# AI finds related tests:
✓ test_auth.py (direct test)
✓ test_login_flow.py (uses auth)
✓ test_permissions.py (uses auth)
✓ test_api_integration.py (integration)

# Runs all affected: 18 tests in 2.4s
```

### Detects Test Patterns
```bash
# Patterns recognized:
# - test_*.py, *_test.py (Python)
# - *.test.ts, *.spec.ts (TypeScript)
# - *_test.go (Go)
# - test_*.rb (Ruby)
```

## Coverage Reports

```bash
/test:run --coverage

# Generates:
# ✅ 45 tests pass (4.2s)
#
# Coverage Report:
# Name                    Stmts   Miss  Cover
# -------------------------------------------
# src/auth.py              156      8    95%
# src/service.py           234     23    90%
# src/utils.py              89      4    96%
# -------------------------------------------
# TOTAL                    479     35    93%
#
# Report: coverage/index.html
```

## Failure Handling

### On Failure
```bash
/test:run

# Output:
❌ 3 tests failed (4.2s)

Failures:
1. test_auth.py::test_login_invalid_password
   AssertionError: Expected 401, got 200

2. test_service.py::test_async_timeout
   TimeoutError: Request exceeded 5s

3. test_integration.py::test_end_to_end
   ConnectionError: Database not available

Suggestions:
• Run /quality:fix @tests-failing
• Check test environment: /context:explain @errors
• Debug specific: /test:debug test_auth.py::test_login_invalid_password
```

### Auto-Fix Integration
```bash
# Tests fail
/test:run
# ❌ 3 failures

# Auto-fix
/quality:fix @tests-failing

# Re-test
/test:run
# ✅ All pass
```

## Watch Mode

```bash
/test:watch

# Watches for file changes
# Re-runs affected tests automatically
# 
# Watching: backend/src/
# 
# Modified: auth.py
# Running: test_auth.py
# ✅ 8 tests pass (1.2s)
#
# Modified: service.py
# Running: test_service.py
# ✅ 12 tests pass (1.8s)
```

## Test Filtering

### By Pattern
```bash
/test:run -k "auth"

# Runs only tests matching "auth":
# ✅ test_auth_login
# ✅ test_auth_logout
# ✅ test_auth_permissions
```

### By Marker
```bash
/test:run -m "integration"

# Runs tests marked as integration:
# ✅ test_api_integration
# ✅ test_db_integration
# ✅ test_end_to_end
```

### By Speed
```bash
/test:run --fast

# Runs only fast tests (<1s)
# Skips slow integration tests
# ✅ 38 tests pass (2.1s)
```

## Smart Defaults from .dev-config.json

```json
{
  "testing": {
    "backend": {
      "framework": "pytest",
      "parallel": true,
      "workers": 16,
      "coverage": {
        "enabled": true,
        "threshold": 80
      }
    },
    "frontend": {
      "framework": "vitest",
      "parallel": true,
      "workers": 20
    }
  },
  "hardware": {
    "cpuCores": 16,
    "workers": {
      "pytest": 16,
      "vitest": 20
    }
  }
}
```

## Desktop Commander Integration

Uses `mcp_Desktop_Commander_start_process` for parallel execution:

```
Starting 16 parallel test processes...

Process 1: pytest backend/tests/test_auth.py
Process 2: pytest backend/tests/test_service.py
...
Process 16: pytest backend/tests/test_utils.py

All processes complete in 4.2s
```

## Performance Comparison

| Approach | Tests | Time | Speedup |
|----------|-------|------|---------|
| Sequential | 45 | 45s | 1x |
| Parallel (4) | 45 | 12s | 3.8x |
| Parallel (8) | 45 | 6.5s | 6.9x |
| Parallel (16) | 45 | 4.2s | 10.7x |
| Parallel (32) | 45 | 3.8s | 11.8x |

**M3 Max Optimal**: 16-32 workers

## Example Workflows

### Workflow 1: TDD Loop
```bash
# 1. Write test
/gen:test calculate_discount

# 2. Run (fail)
/test:run @file
# ❌ test_calculate_discount FAILED

# 3. Implement
# ... write code ...

# 4. Run (pass)
/test:run @file
# ✅ test_calculate_discount PASSED

# 5. Refactor
/quality:refactor @file

# 6. Verify
/test:run @file
# ✅ Still passing
```

### Workflow 2: Pre-Commit
```bash
# Before commit
/test:run @git-diff

# ✅ All affected tests pass
# Ready to commit
git add .
git commit -m "feat: add feature"
```

### Workflow 3: CI/CD Simulation
```bash
# Full suite with coverage
/test:run --coverage --workers=32

# ✅ 245 tests pass (8.4s)
# ✅ Coverage: 94%
# Ready for CI
```

## Related Commands

- `/quality:fix @tests-failing` - Fix failing tests
- `/gen:test @file` - Generate tests
- `/test:coverage` - Coverage report
- `/test:watch` - Watch mode
- `/test:debug` - Debug specific test

## Best Practices

✅ **Test changed code** - Use `@git-diff`
✅ **Parallel by default** - 10-15x faster
✅ **Watch during development** - Instant feedback
✅ **Coverage for features** - Track test quality
✅ **Fix immediately** - Don't accumulate failures

## Tips

1. **Use context variables** - Test only what changed
2. **Leverage parallelism** - M3 Max can handle 32 workers
3. **Watch mode for flow** - Stay in the zone
4. **Coverage for confidence** - Know what's tested
5. **Chain with fix** - `/test:run && /quality:fix`


