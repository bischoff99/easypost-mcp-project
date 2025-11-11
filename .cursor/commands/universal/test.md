Run tests with auto-detected parallel execution.

**Context-aware**: Uses `{{path}}` from arguments or defaults to project test directory.

## Auto-Detection

Automatically detects test framework from project:

**Python Projects:**
- Detects: `pytest.ini`, `import pytest`, `conftest.py`
- Runs: `pytest -n auto {{path}} -v --tb=short`
- Workers: Auto-detected based on CPU cores (from .dev-config.json)

**JavaScript/TypeScript Projects:**
- Detects: `vitest.config.js`, `jest.config.js`
- Vitest: `vitest run --threads auto {{path}}`
- Jest: `jest --maxWorkers=auto {{path}} --verbose`
- Workers: Auto-detected based on system

**Go Projects:**
- Detects: `*_test.go` files
- Runs: `go test -parallel auto -v {{path}}/...`
- Workers: Auto-detected

**Rust Projects:**
- Detects: `Cargo.toml`, `tests/` directory
- Runs: `cargo test --jobs auto {{path}}`
- Workers: Auto-detected

## MCP Integration

**Stage 1 - Enhance** (Optional, cached 24h):
- Server: Context7
- Action: Get testing best practices for detected framework
- Library: `/{{stack.backend.framework}}/{{stack.backend.framework}}`
- Topic: "parallel testing optimization performance"

**Stage 2 - Execute** (Required):
- Server: Desktop Commander
- Action: `start_process` with parallel workers
- Timeout: 180000ms (3 minutes)
- Verbose timing: true (show performance)

**Stage 3 - Analyze Failures** (If tests fail):
- Server: Sequential-thinking
- Purpose: Analyze test failures and suggest fixes
- Output: Root cause + recommended actions

## Variables

```json
{{paths.tests}}              // "backend/tests" or auto-detect
{{workers.pytest}}           // Auto-detected from CPU cores
{{workers.vitest}}           // Auto-detected from CPU cores
{{workers.jest}}             // Auto-detected from CPU cores
{{workers.go}}               // Auto-detected from CPU cores
{{testing.backend.framework}} // "pytest", "vitest", etc.
```

## Performance Expectations

**Auto-Detected Workers:**
- Full test suite: Scales with CPU cores
- Speedup: Proportional to available cores
- Worker utilization: Optimized for your system

**Example Performance:**
- High-end systems (16+ cores): 4-6 seconds, 15x speedup
- Standard systems (4 cores): 30-60 seconds, 4x speedup
- Workers: Auto-scaled to match your hardware

## Usage Examples

```bash
# Default - tests entire project
/test

# Specific path
/test backend/tests/

# With options
/test backend/tests/ --coverage
/test . --verbose-timing
/test src/ --workers=8

# Context-aware - uses open file's test directory
# (If TrackingPage.jsx is open, tests frontend/src/)
/test
```

## Output Format

```
🧪 Running tests with auto-detected parallel workers...
Framework: pytest (auto-detected)
Path: backend/tests/

✅ 45/45 tests passed in 4.2s
Workers: Auto-detected
CPU Usage: Optimized
Speedup: Proportional to available cores

Performance metrics:
- Fastest test: 0.02s
- Slowest test: 0.8s
- Average: 0.09s
```

## Failure Analysis

If tests fail, automatically triggers Sequential-thinking analysis:

```
❌ 3/45 tests failed

🔍 AI Analysis (Sequential-thinking):
- Root cause: Import error in easypost_service.py line 391
- Missing: re module import
- Fix: Add 'import re' at top of file
- Related: API key sanitization function uses regex
```

## Adapts To Any Project

Works automatically with:
- Python (pytest, unittest, nose)
- JavaScript/TypeScript (vitest, jest, mocha)
- Go (go test)
- Rust (cargo test)
- Ruby (rspec)
- Java (junit via gradle/maven)

Just reads `.dev-config.json` and detects framework!
