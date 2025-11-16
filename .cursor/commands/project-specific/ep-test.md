Run EasyPost project tests with auto-detected parallel workers.

**Domain**: EasyPost MCP development
**Performance**: Auto-detects optimal worker count based on your system

## Usage

```bash
# Run all tests
/ep-test

# Run specific test file
/ep-test bulk_performance

# Run with coverage
/ep-test --coverage

# Run integration tests only
/ep-test integration

# Run unit tests only
/ep-test unit

# Benchmark mode
/ep-test --benchmark
```

## What It Does

**Smart Test Execution:**

1. Auto-detects test type from filename/path
2. Runs with pytest -n auto (auto-detects optimal workers)
3. Shows clear pass/fail summary
4. Backend-only tests (frontend is not part of this repo)

## Test Categories

### Backend Tests

```bash
# Integration tests (slower, real API)
/ep-test integration

# Unit tests (fast, mocked)
/ep-test unit

# Performance benchmarks
/ep-test benchmark
```

<!-- Frontend tests section removed: project is backend-only -->

## MCP Integration

**Server**: Desktop Commander
**Tool**: `start_process` with pytest

**Execution**:

```bash
cd backend
source venv/bin/activate
pytest -n auto -v --tb=short tests/
```

**For specific file:**

```bash
pytest -n auto tests/integration/test_bulk_performance.py::test_parsing_performance -v
```

## Output Format

```
╔═══════════════════════════════════════════════════════════╗
║            EASYPOST PROJECT TESTS                         ║
╚═══════════════════════════════════════════════════════════╝

Test Suite: Integration Tests
Workers: Auto-detected (pytest-xdist)

Running tests...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

tests/integration/test_bulk_performance.py::test_parsing_performance ✓
tests/integration/test_bulk_performance.py::test_sequential_vs_parallel_creation ✓
tests/integration/test_bulk_performance.py::test_sequential_vs_parallel_tracking ✓
tests/integration/test_bulk_performance.py::test_analytics_parallel_processing ✓
tests/integration/test_easypost_integration.py::test_create_shipment ✓
tests/integration/test_easypost_integration.py::test_get_tracking ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Results:
   Passed: 6/6
   Failed: 0
   Duration: 2.4s
   Workers: Auto-detected

📊 Coverage: 87%
   backend/src/services/easypost_service.py: 92%
   backend/src/mcp/tools/: 84%
   backend/src/server.py: 89%
```

## Performance Benchmarks

When running benchmarks (`/ep-test --benchmark`):

```
╔═══════════════════════════════════════════════════════════╗
║         PERFORMANCE BENCHMARKS                            ║
╚═══════════════════════════════════════════════════════════╝

BULK SHIPMENT CREATION BENCHMARK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Shipments: 10
Sequential: 1.05s (9.5 shipments/s)
Parallel:   0.11s (90.9 shipments/s)
Speedup:    9.5x ✓

BATCH TRACKING BENCHMARK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Packages: 50
Sequential: 2.51s (19.9 packages/s)
Parallel:   0.28s (178.6 packages/s)
Speedup:    9.0x ✓

ANALYTICS PROCESSING BENCHMARK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Shipments: 10000
Sequential: 45.2ms (221238 shipments/s)
Parallel:   8.7ms (1149425 shipments/s)
Speedup:    5.2x ✓

PARSING PERFORMANCE BENCHMARK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Iterations: 1000
parse_spreadsheet_line: 24.15ms (41406/s)
parse_dimensions:       6.82ms (146628/s)
parse_weight:           5.43ms (184162/s)
Total:                  36.40ms (27472/s)

✅ All benchmarks passed!
```

## Smart Features

**Auto-detects context:**

- If file open: Runs tests for that file
- If in backend/: Runs backend tests
- If in frontend/: Runs frontend tests
- Otherwise: Runs all tests

**Fast feedback:**

- Shows failures immediately
- Stops on first error with `-x` flag
- Clear error messages with `--tb=short`

**Coverage integration:**

- Generates HTML report
- Shows uncovered lines
- Warns if coverage drops

## Related Commands

```bash
/ep-test               # Run tests (this)
/ep-benchmark          # Run benchmarks only
/ep-lint               # Check code quality
/ep-dev                # Start dev environment
```

**Fast, parallel, auto-optimized testing!**
