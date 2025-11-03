Run tests with M3 Max parallel execution (16 workers).

**Context-aware**: Uses `{{path}}` from arguments or defaults to project test directory.

## Auto-Detection

Automatically detects test framework from project:

**Python Projects:**
- Detects: `pytest.ini`, `import pytest`, `conftest.py`
- Runs: `pytest -n {{workers.pytest}} {{path}} -v --tb=short`
- Workers: 16 on M3 Max (from .dev-config.json)

**JavaScript/TypeScript Projects:**
- Detects: `vitest.config.js`, `jest.config.js`
- Vitest: `vitest run --threads {{workers.vitest}} {{path}}`
- Jest: `jest --maxWorkers={{workers.jest}} {{path}} --verbose`
- Workers: 16-20 on M3 Max

**Go Projects:**
- Detects: `*_test.go` files
- Runs: `go test -parallel {{workers.go}} -v {{path}}/...`
- Workers: 16 on M3 Max

**Rust Projects:**
- Detects: `Cargo.toml`, `tests/` directory
- Runs: `cargo test --jobs {{workers.rust}} {{path}}`
- Workers: 16 on M3 Max

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
{{workers.pytest}}           // 16 (M3 Max)
{{workers.vitest}}           // 20 (M3 Max)
{{workers.jest}}             // 16 (M3 Max)
{{workers.go}}               // 16 (M3 Max)
{{testing.backend.framework}} // "pytest", "vitest", etc.
```

## Performance Expectations

**M3 Max (16 cores, 128GB RAM):**
- Full test suite: 4-6 seconds
- Speedup: 15x vs sequential
- Worker utilization: 90%+

**Standard Hardware (4 cores):**
- Full test suite: 30-60 seconds
- Speedup: 4x vs sequential
- Workers: Auto-scaled to 4

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
🧪 Running tests with 16 parallel workers...
Framework: pytest (auto-detected)
Path: backend/tests/

✅ 45/45 tests passed in 4.2s
Workers: 16
CPU Usage: 94%
Speedup: 14.3x vs sequential

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
