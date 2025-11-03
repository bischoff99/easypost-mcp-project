Auto-fix visible errors using AI reasoning and MCP tools.

**Context-aware**: No arguments needed - automatically detects errors from terminal, editor, or linter output.

## How It Works

**Intelligent Error Detection:**
1. Scans terminal output for errors
2. Reads linter errors from editor
3. Checks recent command failures
4. Identifies import errors, syntax errors, type errors

**MCP Reasoning Chain:**
1. **Sequential-thinking**: Analyze root cause step-by-step
2. **Context7**: Get framework-specific fix patterns
3. **Desktop Commander**: Apply fix to files
4. **Desktop Commander**: Run tests to verify fix

## Error Types Handled

**Python:**
- Import errors (`ModuleNotFoundError`, `ImportError`)
- Syntax errors (`SyntaxError`, `IndentationError`)
- Type errors (`TypeError`, `AttributeError`)
- Linter errors (ruff, pylint, mypy)
- Test failures (pytest assertions)

**JavaScript/TypeScript:**
- Module errors (`Cannot find module`)
- Syntax errors (parsing failures)
- Type errors (TypeScript)
- Linter errors (eslint, tsc)
- Test failures (vitest, jest)

**Go:**
- Import errors (`undefined:`)
- Compilation errors (`syntax error`)
- Type errors (`cannot use`)
- Test failures

**Universal:**
- Missing dependencies
- Configuration errors
- Path resolution errors
- Version conflicts

## MCP Integration

**Stage 1 - Detect Error**:
- Server: Desktop Commander
- Tool: `read_process_output` from last command
- Action: Parse error message, extract location and context
- Output: Error type, file path, line number, message

**Stage 2 - Analyze Root Cause**:
- Server: Sequential-thinking
- Tool: `sequentialthinking` with error context
- Method: 6-12 thought analysis of root cause
- Output: Step-by-step diagnosis and solution approach

**Stage 3 - Get Fix Pattern** (Optional, cached):
- Server: Context7
- Tool: `get-library-docs`
- Library: Auto-detect from error (`/fastapi/fastapi`, `/react/react`)
- Topic: Specific error type (e.g., "import error resolution")
- Tokens: 2000
- Cache: 24h for common patterns

**Stage 4 - Apply Fix** (Desktop Commander):
- Server: Desktop Commander
- Tool: `edit_block` for surgical code editing
- Method: 
  ```python
  edit_block(
    file_path="path/to/file.py",
    old_string="exact code to replace (3-5 lines context)",
    new_string="corrected code with fix applied"
  )
  ```
- Safety Features:
  - Validates unique match before applying
  - Character-level diff on close matches
  - Creates backup before changes
  - Shows what would change in dry-run mode

**Stage 5 - Verify Fix**:
- Server: Desktop Commander
- Tool: `start_process` to run tests
- Action: Run relevant tests (pytest, vitest, go test)
- Success: Fix complete
- Failure: Rollback using backup, try alternative fix

## Smart Detection Examples

**Example 1: Import Error**
```
Terminal shows:
  ImportError: No module named 're'

AI detects:
  - File: easypost_service.py
  - Line: 391
  - Missing: import re

AI fixes:
  - Adds 'import re' at top
  - Verifies: Runs tests
```

**Example 2: Type Error**
```
Editor shows:
  TypeError: 'datetime.utcnow()' is deprecated

AI detects:
  - Deprecated method usage
  - Python 3.12+ incompatibility

AI fixes:
  - Replaces with datetime.now(timezone.utc)
  - Updates all instances
```

**Example 3: Test Failure**
```
pytest output:
  FAILED tests/test_service.py::test_create - AssertionError

AI analyzes:
  - Mock not configured correctly
  - Expected call signature changed

AI fixes:
  - Updates mock setup
  - Adjusts assertions
```

## Usage Examples

```bash
# No arguments - detects visible error
/fix

# With specific file (if error not visible)
/fix backend/src/services/easypost_service.py

# With error type hint
/fix import-error
/fix type-error

# Dry-run mode (shows fix without applying)
/fix --dry-run
```

## Output Format

```
🔍 Error Detection:
Found: ImportError in backend/src/services/easypost_service.py:391
Message: No module named 're'

🧠 AI Analysis (Sequential-thinking):
Step 1: Error occurs in _sanitize_error method
Step 2: Function uses re.sub() but re not imported
Step 3: Import should be at module level (line 11)
Root cause: Missing import statement

📚 Best Practice (Context7):
Python imports should be grouped:
1. Standard library (import re)
2. Third-party (import easypost)
3. Local (from src.utils import)

✅ Fix Applied:
File: backend/src/services/easypost_service.py
Line 11: Added 'import re'
Change: Inserted in standard library imports section

🧪 Verification:
Running: pytest backend/tests/unit/test_easypost_service.py -v
Result: ✅ All tests passed

✅ Fix complete and verified!
```

## Performance

- Error detection: <1s (Desktop Commander read_process_output)
- AI analysis: 3-5s (Sequential-thinking with 6-12 thoughts)
- Context7 lookup: 2-4s (cached after first use, optional)
- Fix application: 1-2s (Desktop Commander edit_block)
- Test verification: 3-6s (Desktop Commander start_process, parallel)
- **Total: 10-18s** for complete fix cycle

## Desktop Commander Tools Used

**Primary Tool: `edit_block`**
- Surgical code replacement with minimal context (3-5 lines)
- Validates unique match before applying
- Character-level diff shown for near matches
- Safe and precise edits

**Supporting Tools:**
- `read_process_output` - Detect errors from terminal
- `start_process` - Run test verification  
- `read_file` - Gather context for analysis
- `list_sessions` - Check running processes

## Safety Features

- Creates backup snapshot before changes
- Runs tests before finalizing
- Rollback if tests fail
- Shows diff before applying (in dry-run)
- Never overwrites without verification

## Adapts To Any Language

Uses .dev-config.json to determine:
- Test command: `{{testing.backend.framework}}`
- Linter: Python (ruff), JS (eslint), Go (golangci-lint)
- File paths: `{{paths.backend}}`, `{{paths.tests}}`
- Conventions: Naming, formatting standards

**One command. Every error. Any language.**
