<<<<<<< HEAD
Run tests with auto-detected parallel execution, intelligent test selection, and comprehensive analysis.
||||||| 7a576da
Run tests with M3 Max parallel execution (16 workers).
=======
Run tests with auto-detected parallel execution.
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8

**Context-aware**: Uses `{{path}}` from arguments or defaults to project test directory. Automatically detects framework, selects relevant tests, and provides detailed analysis.

## How It Works

**Complete MCP Workflow (6 Stages):**

**Stage 0 - Framework Detection** (NEW):
- Detects test framework from project files
- Identifies test runner configuration
- Determines optimal execution strategy

**Stage 1 - Test Selection** (NEW):
- Supports `--changed`, `--failed`, `--coverage` flags
- Maps changed files to test files
- Retrieves previously failed tests
- Filters tests based on selection strategy

**Stage 2 - Context7 Enhancement** (ENHANCED):
- Loads framework-specific best practices
- Gets optimization patterns for parallel execution
- Caches documentation for 24 hours

**Stage 3 - Execute Tests** (ENHANCED):
- Runs tests with auto-detected workers (max 16)
- Framework-specific commands with exact parameters
- Comprehensive logging and progress reporting

**Stage 4 - Parse Results** (NEW):
- Extracts test counts, durations, failures
- Identifies slow tests and performance bottlenecks
- Structures output for analysis

**Stage 5 - Coverage Analysis** (NEW, if `--coverage`):
- Reads coverage reports
- Identifies uncovered critical paths
- Recommends additional tests

**Stage 6 - Failure Analysis** (ENHANCED):
- Deep analysis of test failures using Sequential-thinking
- Root cause identification
- Suggested fixes for each failure

## Auto-Detection

Automatically detects test framework from project:

**Python Projects:**
- Detects: `pytest.ini`, `import pytest`, `conftest.py`
<<<<<<< HEAD
- Runs: `pytest -n auto {{path}} -v --tb=short`
- Workers: Auto-detected based on CPU cores (max 16)
||||||| 7a576da
- Runs: `pytest -n {{workers.pytest}} {{path}} -v --tb=short`
- Workers: 16 on M3 Max (from .dev-config.json)
=======
- Runs: `pytest -n auto {{path}} -v --tb=short`
- Workers: Auto-detected based on CPU cores (from .dev-config.json)
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8

**JavaScript/TypeScript Projects:**
- Detects: `vitest.config.js`, `jest.config.js`
<<<<<<< HEAD
- Vitest: `vitest run --threads auto {{path}}`
- Jest: `jest --maxWorkers=auto {{path}} --verbose`
- Workers: Auto-detected based on system (max 16)
||||||| 7a576da
- Vitest: `vitest run --threads {{workers.vitest}} {{path}}`
- Jest: `jest --maxWorkers={{workers.jest}} {{path}} --verbose`
- Workers: 16-20 on M3 Max
=======
- Vitest: `vitest run --threads auto {{path}}`
- Jest: `jest --maxWorkers=auto {{path}} --verbose`
- Workers: Auto-detected based on system
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8

**Go Projects:**
<<<<<<< HEAD
- Detects: `*_test.go` files, `go.mod`
- Runs: `go test -parallel auto -v {{path}}/...`
- Workers: Auto-detected (max 16)
||||||| 7a576da
- Detects: `*_test.go` files
- Runs: `go test -parallel {{workers.go}} -v {{path}}/...`
- Workers: 16 on M3 Max
=======
- Detects: `*_test.go` files
- Runs: `go test -parallel auto -v {{path}}/...`
- Workers: Auto-detected
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8

**Rust Projects:**
- Detects: `Cargo.toml`, `tests/` directory
<<<<<<< HEAD
- Runs: `cargo test --jobs auto {{path}}`
- Workers: Auto-detected (max 16)
||||||| 7a576da
- Runs: `cargo test --jobs {{workers.rust}} {{path}}`
- Workers: 16 on M3 Max
=======
- Runs: `cargo test --jobs auto {{path}}`
- Workers: Auto-detected
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8

## MCP Integration

### Stage 0 - Framework Detection

```yaml
Tool: mcp_desktop-commander_read_file
Files to check (in order):
  - pytest.ini (Python)
  - vitest.config.js (JavaScript)
  - Cargo.toml (Rust)
  - go.mod (Go)
  - package.json (JavaScript fallback)

Action: Read each file, detect framework from content
  - pytest.ini → pytest
  - vitest.config.js → vitest
  - Cargo.toml → cargo test
  - go.mod → go test
  - package.json → check test script

Progress: await ctx.report_progress(0, 6, "Detecting test framework")
State: ctx.set_state("framework", detected_value)
  Examples: "pytest", "vitest", "jest", "go", "cargo"

Error handling:
  If all files fail:
    Tool: mcp_desktop-commander_start_search
    Pattern: "test_*.py" OR "*_test.go" OR "*.test.js"
    SearchType: "files"
    Find: Test files to infer framework

Logging: await ctx.info(f"Detected framework: {framework}")
```

### Stage 1 - Test Selection

```yaml
If --changed flag:
  Tool: mcp_desktop-commander_start_process
  Command: "git diff --name-only HEAD"
  Timeout: 5000ms
  
  Parse: Modified file paths
  Map: Source files → Test files
    Python: src/file.py → tests/test_file.py
    JS: src/file.js → src/file.test.js
    Go: file.go → file_test.go
    Rust: src/file.rs → tests/file.rs
  
  Tool: mcp_desktop-commander_start_search
  Pattern: Mapped test file names
  SearchType: "files"
  Find: Actual test files to run
  
  Progress: await ctx.report_progress(1, 6, "Selecting changed tests")
  State: ctx.set_state("test_files", [list of test files])
  Logging: await ctx.info(f"Found {len(test_files)} tests for changed files")

If --failed flag:
  Tool: mcp_desktop-commander_read_file
  Files (framework-specific):
    Python: .pytest_cache/v/cache/lastfailed
    JS: .vitest_cache/last-failed.json
    Go: (not supported, use --changed)
    Rust: (not supported, use --changed)
  
  Parse: Previously failed test identifiers
  Progress: await ctx.report_progress(1, 6, "Selecting failed tests")
  State: ctx.set_state("test_files", failed_tests)
  Logging: await ctx.info(f"Found {len(failed_tests)} previously failed tests")

If no flags (default):
  Tool: mcp_desktop-commander_start_search
  Pattern: Framework-specific test patterns
    Python: "**/test_*.py", "**/tests/**/*.py"
    JS: "**/*.test.js", "**/*.spec.js"
    Go: "**/*_test.go"
    Rust: "**/tests/**/*.rs"
  SearchType: "files"
  
  Progress: await ctx.report_progress(1, 6, "Finding all tests")
  State: ctx.set_state("test_files", all_tests)
```

### Stage 2 - Context7 Enhancement

```yaml
Tool: mcp_Context7_resolve-library-id
Query: ctx.get_state("framework")
Examples:
  "pytest" → /pytest-dev/pytest
  "vitest" → /vitest-dev/vitest
  "jest" → /facebook/jest

Tool: mcp_Context7_get-library-docs
Library: Resolved ID from previous step
Topic: "parallel execution best practices test fixtures optimization"
Tokens: 3000
Cache: 24h (store in ctx for reuse)

Progress: await ctx.report_progress(2, 6, "Loading testing best practices")
State: ctx.set_state("best_practices", docs_content)

Error handling:
  from fastmcp.exceptions import ToolError
  try:
    docs = await context7_call()
  except ToolError as e:
    await ctx.warning(f"Context7 unavailable: {e}")
    # Continue without enhancement
    ctx.set_state("best_practices", None)

Logging: await ctx.debug("Loaded best practices for {framework}")
```

### Stage 3 - Execute Tests

```yaml
Tool: mcp_desktop-commander_start_process
Command: Framework-specific with detected workers
  Python: "pytest -n auto {path} -v --tb=short"
  JS (vitest): "vitest run --threads auto {path}"
  JS (jest): "jest --maxWorkers=auto {path} --verbose"
  Go: "go test -parallel auto -v {path}/..."
  Rust: "cargo test --jobs auto {path}"

Timeout: 180000ms (3 minutes)
Verbose_timing: true

Progress: await ctx.report_progress(3, 6, f"Running {test_count} tests")
Logging:
  await ctx.info(f"Framework: {framework}, Workers: auto-detected (max 16)")
  await ctx.debug(f"Command: {full_command}")

State: ctx.set_state("test_process_pid", pid)

Error handling:
  If process fails to start:
    await ctx.error("Failed to start test process")
    return {"status": "error", "message": "Test execution failed"}
```

### Stage 4 - Parse Results

```yaml
Tool: mcp_desktop-commander_read_process_output
PID: ctx.get_state("test_process_pid")
Timeout: 10000ms

Parse output for:
  - Total tests run
  - Passed/Failed/Skipped counts
  - Failure details (file, line, assertion)
  - Performance metrics (duration, slowest tests)

Framework-specific parsing:
  Python (pytest):
    Pattern: "(\d+) passed, (\d+) failed"
    Extract: Test names, failure messages, durations
  JS (vitest):
    Pattern: "Test Files.*(\d+) passed.*(\d+) failed"
    Extract: Test suites, individual tests
  Go:
    Pattern: "ok.*(\d+\.\d+s)" OR "FAIL.*(\d+\.\d+s)"
    Extract: Package results, test durations
  Rust:
    Pattern: "test result:.*(\d+) passed.*(\d+) failed"
    Extract: Test names, failure messages

Progress: await ctx.report_progress(4, 6, "Parsing results")
State: ctx.set_state("test_results", {
  "total": total_count,
  "passed": passed_count,
  "failed": failed_count,
  "skipped": skipped_count,
  "duration": duration_seconds,
  "failures": [list of failure details],
  "slow_tests": [list of slowest tests]
})

Logging:
  await ctx.info(f"Results: {passed}/{total} passed in {duration}s")
  if failed_count > 0:
    await ctx.warning(f"{failed_count} tests failed")
```

### Stage 5 - Coverage Analysis (if --coverage flag)

```yaml
Tool: mcp_desktop-commander_read_file
Files (framework-specific):
  Python: coverage.json, coverage.xml, htmlcov/index.html
  JS: coverage/coverage-summary.json
  Go: coverage.out
  Rust: tarpaulin-report.json

Parse coverage data:
  - Overall coverage percentage
  - File-level coverage
  - Line-level coverage gaps
  - Uncovered critical paths

Tool: mcp_sequential-thinking_sequentialthinking
Input: Coverage data + test results
Thoughts: 6-8
Analysis:
  1. What code is covered?
  2. What critical paths are uncovered?
  3. Which tests should be added?
  4. Are there coverage gaps in error handling?
  5. Are edge cases tested?
  6. Recommendations for improving coverage

Progress: await ctx.report_progress(5, 6, "Analyzing coverage")
State: ctx.set_state("coverage_analysis", {
  "overall_coverage": percentage,
  "uncovered_files": [list],
  "recommendations": [list of specific test suggestions]
})

Output: Specific test recommendations with file paths and line numbers
Logging: await ctx.info(f"Coverage: {overall_coverage}%")
```

### Stage 6 - Failure Analysis (if tests failed)

```yaml
Condition: Only if ctx.get_state("test_results")["failed"] > 0

Tool: mcp_sequential-thinking_sequentialthinking
Input: ctx.get_state("test_results")["failures"]
Thoughts: 10-12 for comprehensive analysis
Questions to answer:
  1. Why did each test fail?
  2. Is it a code bug or test bug?
  3. Common pattern across failures?
  4. Suggested fixes for each
  5. Related code that needs checking
  6. Root cause analysis

Progress: await ctx.report_progress(6, 6, "Analyzing failures")
Logging: await ctx.error(f"{failed_count} tests failed, analyzing...")

State: ctx.set_state("failure_analysis", {
  "failures": [
    {
      "test_name": "test_example",
      "file": "tests/test_file.py",
      "line": 42,
      "error": "AssertionError: expected 5, got 3",
      "root_cause": "Mock not configured correctly",
      "suggested_fix": "Update mock setup at line 20",
      "related_code": ["src/service.py:100"]
    }
  ],
  "common_patterns": ["Mock configuration issues"],
  "recommendations": ["Review all mock setups"]
})

Output includes:
  - Root cause per failure
  - Suggested fix
  - Related code to check
  - Common patterns across failures
```

## Variables

```json
{{paths.tests}}              // "backend/tests" or auto-detect
<<<<<<< HEAD
{{workers.pytest}}           // Auto-detected from CPU cores (max 16)
{{workers.vitest}}           // Auto-detected from CPU cores (max 16)
{{workers.jest}}             // Auto-detected from CPU cores (max 16)
{{workers.go}}               // Auto-detected from CPU cores (max 16)
||||||| 7a576da
{{workers.pytest}}           // 16 (M3 Max)
{{workers.vitest}}           // 20 (M3 Max)
{{workers.jest}}             // 16 (M3 Max)
{{workers.go}}               // 16 (M3 Max)
=======
{{workers.pytest}}           // Auto-detected from CPU cores
{{workers.vitest}}           // Auto-detected from CPU cores
{{workers.jest}}             // Auto-detected from CPU cores
{{workers.go}}               // Auto-detected from CPU cores
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8
{{testing.backend.framework}} // "pytest", "vitest", etc.
```

<<<<<<< HEAD
||||||| 7a576da
## Performance Expectations

**M3 Max (16 cores, 128GB RAM):**
- Full test suite: 4-6 seconds
- Speedup: 15x vs sequential
- Worker utilization: 90%+

**Standard Hardware (4 cores):**
- Full test suite: 30-60 seconds
- Speedup: 4x vs sequential
- Workers: Auto-scaled to 4

=======
## Performance Expectations

**Auto-Detected Workers:**
- Full test suite: Scales with CPU cores
- Speedup: Proportional to available cores
- Worker utilization: Optimized for your system

**Example Performance:**
- High-end systems (16+ cores): 4-6 seconds, 15x speedup
- Standard systems (4 cores): 30-60 seconds, 4x speedup
- Workers: Auto-scaled to match your hardware

>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8
## Usage Examples

```bash
# Default - tests entire project
/test

# Specific path
/test backend/tests/

# Test only changed files
/test --changed

# Rerun failed tests
/test --failed

# With coverage analysis
/test --coverage

# Combined flags
/test backend/tests/ --changed --coverage

# Watch mode (if supported by framework)
/test backend/tests/ --watch

# Verbose output
/test --verbose
```

## Output Format

<<<<<<< HEAD
### Success Output
||||||| 7a576da
```
🧪 Running tests with 16 parallel workers...
Framework: pytest (auto-detected)
Path: backend/tests/
=======
```
🧪 Running tests with auto-detected parallel workers...
Framework: pytest (auto-detected)
Path: backend/tests/
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8

<<<<<<< HEAD
```
🔍 Framework Detection:
Detected: pytest (from pytest.ini)

📋 Test Selection:
Found: 45 tests in backend/tests/
Strategy: All tests (no flags)

📚 Best Practices (Context7):
Loaded: Parallel execution patterns for pytest
Cache: 24h

🧪 Running Tests:
Framework: pytest
Workers: Auto-detected (max 16)
Command: pytest -n auto backend/tests/ -v --tb=short

✅ Test Results:
45/45 tests passed in 4.2s
Workers: Auto-detected (max 16)
CPU Usage: Optimized
||||||| 7a576da
✅ 45/45 tests passed in 4.2s
Workers: 16
CPU Usage: 94%
Speedup: 14.3x vs sequential
=======
✅ 45/45 tests passed in 4.2s
Workers: Auto-detected
CPU Usage: Optimized
Speedup: Proportional to available cores
>>>>>>> 99314e0f7fef772f5a4f4779d02c1c7df730f0d8

Performance metrics:
- Fastest test: 0.02s
- Slowest test: 0.8s
- Average: 0.09s
- Total duration: 4.2s

✅ All tests passed!
```

### Failure Output

```
🔍 Framework Detection:
Detected: pytest (from pytest.ini)

📋 Test Selection:
Found: 45 tests in backend/tests/

🧪 Running Tests:
Framework: pytest
Workers: Auto-detected (max 16)

❌ Test Results:
42/45 tests passed, 3 failed in 5.1s

🔍 Failure Analysis (Sequential-thinking):
Analyzing 3 failures...

Failure 1: test_create_shipment
  File: tests/test_service.py:42
  Error: AssertionError: expected 200, got 404
  Root cause: Mock API response not configured correctly
  Suggested fix: Update mock at line 20 in test_service.py
  Related code: src/services/easypost_service.py:100

Failure 2: test_track_shipment
  File: tests/test_tracking.py:15
  Error: ImportError: No module named 're'
  Root cause: Missing import statement
  Suggested fix: Add 'import re' at top of easypost_service.py
  Related code: src/services/easypost_service.py:391

Failure 3: test_rate_calculation
  File: tests/test_rates.py:88
  Error: TypeError: 'NoneType' object is not subscriptable
  Root cause: API response not handled for None case
  Suggested fix: Add None check before accessing response['rates']
  Related code: src/services/easypost_service.py:250

Common patterns:
- Mock configuration issues (2 failures)
- Missing error handling (1 failure)

Recommendations:
1. Review all mock setups in test files
2. Add comprehensive error handling for API responses
```

### Coverage Output (with --coverage)

```
✅ Test Results:
45/45 tests passed in 4.2s

📊 Coverage Analysis:
Overall coverage: 78%

Uncovered critical paths:
- src/services/easypost_service.py:391-400 (error sanitization)
- src/utils/validation.py:50-60 (edge case validation)

Recommendations:
1. Add test for error sanitization edge cases
   File: tests/test_service.py
   Function: test_sanitize_error_edge_cases
   
2. Add test for validation boundary conditions
   File: tests/test_validation.py
   Function: test_validation_boundaries
```

## Performance

- Framework detection: <1s (Desktop Commander read_file)
- Test selection: 1-2s (git diff + search)
- Context7 lookup: 2-4s (cached after first use, optional)
- Test execution: 3-60s (depends on test suite size, parallelized)
- Result parsing: <1s (Desktop Commander read_process_output)
- Coverage analysis: 2-3s (if --coverage flag)
- Failure analysis: 5-8s (Sequential-thinking with 10-12 thoughts)
- **Total: 10-80s** depending on test suite size and flags

## Desktop Commander Tools Used

**Primary Tools:**
- `mcp_desktop-commander_start_process` - Execute test commands
- `mcp_desktop-commander_read_process_output` - Parse test results
- `mcp_desktop-commander_read_file` - Framework detection, coverage files
- `mcp_desktop-commander_start_search` - Find test files

**Supporting Tools:**
- `mcp_sequential-thinking_sequentialthinking` - Failure analysis, coverage recommendations
- `mcp_Context7_resolve-library-id` - Framework library resolution
- `mcp_Context7_get-library-docs` - Best practices loading

## Error Handling

**Framework Detection Failure:**
- Fallback to file search for test files
- Infer framework from test file patterns
- Continue with generic test execution

**Test Execution Failure:**
- Capture error output
- Report failure reason
- Suggest troubleshooting steps

**Coverage Analysis Failure:**
- Continue without coverage (if --coverage flag not critical)
- Report warning about missing coverage data

**Context7 Unavailability:**
- Continue without best practices enhancement
- Log warning message
- Use default test execution patterns

## Adapts To Any Project

Works automatically with:
- Python (pytest, unittest, nose)
- JavaScript/TypeScript (vitest, jest, mocha)
- Go (go test)
- Rust (cargo test)
- Ruby (rspec)
- Java (junit via gradle/maven)

**One command. Smart selection. Comprehensive analysis. Any framework.**
