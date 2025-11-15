Auto-fix visible errors using AI reasoning and MCP tools with comprehensive retry logic and backup mechanisms.

**Context-aware**: No arguments needed - automatically detects errors from terminal, editor, or linter output. Provides intelligent error analysis, framework-specific fixes, and verified solutions.

## How It Works

**Complete MCP Workflow (7 Stages):**

**Stage 1 - Error Detection** (ENHANCED):

- Scans terminal output for errors
- Reads linter errors from editor
- Checks recent command failures
- Identifies import errors, syntax errors, type errors
- Extracts precise error location and context

**Stage 2 - Root Cause Analysis** (ENHANCED):

- Deep Sequential-thinking analysis (10-15 thoughts)
- Step-by-step diagnosis
- Identifies prerequisites and side effects
- Determines fix strategy

**Stage 3 - Get Fix Patterns** (ENHANCED):

- Context7 framework-specific patterns
- Real-world examples and best practices
- Cached for 24 hours
- Graceful degradation if unavailable

**Stage 4 - Prepare Fix** (NEW):

- Generates exact old_string and new_string
- Validates fix won't break other code
- Ranks multiple fixes by safety
- Prepares surgical edits

**Stage 5 - Backup** (NEW):

- Creates backup snapshot before changes
- Stores complete file content
- Enables rollback if fix fails

**Stage 6 - Apply Fix** (ENHANCED):

- Surgical code editing with edit_block
- Character-level diff on close matches
- Handles multiple edits sequentially
- Comprehensive error handling

**Stage 7 - Verify + Retry** (ENHANCED):

- Runs tests to verify fix
- Automatic rollback on failure
- Tries alternative fixes if available
- Maximum 2 retry attempts

## Error Types Handled

**Python:**

- Import errors (`ModuleNotFoundError`, `ImportError`)
- Syntax errors (`SyntaxError`, `IndentationError`)
- Type errors (`TypeError`, `AttributeError`)
- Linter errors (ruff, pylint, mypy)
- Test failures (pytest assertions)
- Deprecation warnings

**JavaScript/TypeScript:**

- Module errors (`Cannot find module`)
- Syntax errors (parsing failures)
- Type errors (TypeScript)
- Linter errors (eslint, tsc)
- Test failures (vitest, jest)
- Runtime errors

**Go:**

- Import errors (`undefined:`)
- Compilation errors (`syntax error`)
- Type errors (`cannot use`)
- Test failures
- Package resolution errors

**Rust:**

- Compilation errors (`error[E`)
- Type errors (`mismatched types`)
- Borrow checker errors
- Test failures
- Crate resolution errors

**Universal:**

- Missing dependencies
- Configuration errors
- Path resolution errors
- Version conflicts
- Environment variable issues

## MCP Integration

### Stage 1 - Error Detection

```yaml
Tool: mcp_desktop-commander_read_process_output
PID: Last failed process (from mcp_desktop-commander_list_sessions)
Lines: 200 (last 200 lines)
Timeout: 5000ms

Parse for error patterns:
  Python:
    - "Error:" → Extract error type and message
    - "Traceback" → Extract full stack trace
    - 'File "' → Extract file path and line number
    - "line \d+" → Extract line number
  JS:
    - "Error:" → Extract error type
    - "at " → Extract stack trace locations
    - "Cannot find module" → Module resolution error
  Go:
    - "panic:" → Panic error
    - "Error:" → General error
    - "undefined:" → Import/undefined error
    - "cannot use" → Type error
  Rust:
    - "error[E" → Compilation error with code
    - "help:" → Compiler suggestions
    - "mismatched types" → Type error

Tool: mcp_desktop-commander_read_file (if file identified)
Path: Error file path (absolute path)
Offset: error_line - 50 (context before error)
Length: 100 (50 lines before + 50 lines after)

Progress: await ctx.report_progress(0, 7, "Detecting error")
State: ctx.set_state("error_context", {
  "type": error_type,  # "ImportError", "SyntaxError", etc.
  "file": file_path,
  "line": line_number,
  "message": error_message,
  "surrounding_code": code_context,
  "stack_trace": stack_trace  # if available
})

Logging:
  await ctx.info(f"Found {error_type} in {file}:{line}")
  await ctx.debug(f"Error message: {error_message}")

Error handling:
  If no process found:
    Tool: mcp_desktop-commander_start_search
    Pattern: Error patterns in recent files
    SearchType: "content"
    Find: Recent error messages
```

### Stage 2 - Root Cause Analysis

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: ctx.get_state("error_context")
Thoughts: 10-15 for deep analysis
Method: Chain-of-thought reasoning

Analysis steps:
  1. What does the error message say?
  2. Where does it occur (file, line, function)?
  3. Why does it occur (missing import, wrong type, etc.)?
  4. What's missing or wrong?
  5. What are prerequisites for fix?
  6. What are potential side effects?
  7. What's the safest fix approach?
  8. Are there multiple possible fixes?
  9. Which fix is least likely to break other code?
  10. What tests should verify the fix?

Progress: await ctx.report_progress(1, 7, "Analyzing root cause")
State: ctx.set_state("analysis", {
  "root_cause": root_cause_description,
  "prerequisites": [list of prerequisites],
  "fix_strategy": strategy_description,
  "possible_fixes": [list of alternative fixes],
  "safety_considerations": [list of concerns]
})

Logging:
  await ctx.debug("Analysis steps: {thought_summary}")
  await ctx.info(f"Root cause: {root_cause_description}")
```

### Stage 3 - Get Fix Patterns

```yaml
Tool: mcp_Context7_resolve-library-id
Query: Detect framework from file imports/package.json/go.mod/Cargo.toml
Examples:
  "fastapi" → /tiangolo/fastapi
  "react" → /facebook/react
  "gin" → /gin-gonic/gin
  "tokio" → /tokio-rs/tokio

Tool: mcp_Context7_get-library-docs
Library: Resolved ID from previous step
Topic: "{error_type} resolution patterns examples"
  Examples:
    "import error resolution"
    "async error handling"
    "type error fixes"
    "syntax error correction"
Tokens: 3000

Progress: await ctx.report_progress(2, 7, "Researching fix patterns")
State: ctx.set_state("fix_patterns", patterns_content)

Error handling:
  from fastmcp.exceptions import ToolError
  try:
    patterns = await context7_call()
  except ToolError as e:
    await ctx.warning(f"Context7 unavailable, using analysis only")
    patterns = None  # Continue without external patterns

Cache: 24h for common patterns
Logging:
  if patterns:
    await ctx.info("Loaded fix patterns from Context7")
  else:
    await ctx.warning("Continuing without external patterns")
```

### Stage 4 - Prepare Fix

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Root cause + fix patterns + surrounding code
Thoughts: 6-8
Generate: Exact old_string and new_string for edit_block

Analysis:
  1. What exact code needs to change?
  2. What's the minimal context needed for unique match?
  3. Will this fix break other code?
  4. Are there multiple places that need fixing?
  5. What's the safest order of edits?
  6. Should we fix one thing at a time?

Validation:
  - Fix won't break other code
  - Context is unique (3-5 lines minimum)
  - Multiple fixes ranked by safety

Progress: await ctx.report_progress(3, 7, "Preparing fix")
State: ctx.set_state("prepared_fixes", [
  {
    "old_string": exact_code_to_replace,
    "new_string": corrected_code,
    "safety_score": 0.95,  # 0.0 to 1.0
    "description": "Add missing import statement",
    "file": file_path,
    "line": line_number
  },
  # Alternative fixes with lower safety scores
])

Logging:
  await ctx.info(f"Prepared {len(prepared_fixes)} fix(es)")
  await ctx.debug(f"Primary fix: {prepared_fixes[0]['description']}")
```

### Stage 5 - Backup

```yaml
Tool: mcp_desktop-commander_read_file
Path: File to be fixed (absolute path)
Action: Read complete current content

State: ctx.set_state("backup", {
  "path": file_path,
  "content": current_content,
  "timestamp": datetime.now().isoformat(),
  "line_count": len(current_content.splitlines())
})

Progress: await ctx.report_progress(4, 7, "Creating backup")
Logging:
  await ctx.debug(f"Backed up {file_path} ({len(content)} chars, {line_count} lines)")

Best practice: Backup before any edits, enables rollback
```

### Stage 6 - Apply Fix

```yaml
Tool: mcp_desktop-commander_edit_block
Parameters:
  file_path: Absolute path (use Path(__file__).resolve() or absolute path)
  old_string: From prepared_fixes[0] (highest safety score)
  new_string: From prepared_fixes[0]
  expected_replacements: 1

Progress: await ctx.report_progress(5, 7, "Applying fix")
Logging:
  await ctx.info(f"Editing {file_path}: {prepared_fixes[0]['description']}")
  await ctx.debug(f"Old: {old_string[:100]}...")
  await ctx.debug(f"New: {new_string[:100]}...")

Error handling:
  from fastmcp.exceptions import ToolError
  try:
    result = await edit_block(...)
  except ToolError as e:
    error_msg = str(e)

    if "not unique" in error_msg:
      await ctx.error("Multiple matches found for old_string")
      # Try with more context lines
      await ctx.info("Retrying with more context...")
      expanded_old = add_more_context(old_string, file_content)
      await edit_block(file_path, expanded_old, new_string)

    elif "not found" in error_msg:
      await ctx.warning("Exact match failed, showing diff")
      # Show character-level diff
      diff = generate_char_diff(old_string, file_content)
      await ctx.error(f"Diff:\n{diff}")
      # Try with adjusted whitespace
      normalized_old = normalize_whitespace(old_string)
      await edit_block(file_path, normalized_old, new_string)

    else:
      raise  # Re-raise unexpected errors

Best practice: If multiple edits needed, make separate calls:
  for fix in prepared_fixes_list:
    await edit_block(
      file_path=fix["file"],
      old_string=fix["old_string"],
      new_string=fix["new_string"],
      expected_replacements=1
    )
    await ctx.info(f"Applied fix {i+1}/{len(prepared_fixes_list)}")
```

### Stage 7 - Verify + Retry

```yaml
Tool: mcp_desktop-commander_start_process
Command: Test command for affected file
  Python: "pytest {test_file} -v"
  JS: "cd apps/frontend && vitest run {test_file}"
  Go: "go test {package} -run {test_function}"
  Rust: "cargo test {test_name}"

Timeout: 60000ms (1 minute)
Progress: await ctx.report_progress(6, 7, "Verifying fix")

Success path:
  Tool: mcp_desktop-commander_read_process_output
  PID: Test process PID
  Parse: Test results

  if "passed" in output or "PASS" in output:
    await ctx.info("Fix verified, tests passed")
    ctx.clear_state("backup")  # No longer needed
    return {
      "status": "success",
      "message": "Fix applied and verified",
      "file": file_path,
      "fix_description": prepared_fixes[0]["description"]
    }

Failure path:
  await ctx.error("Fix failed verification, rolling back")

  # Rollback using backup
  backup = ctx.get_state("backup")
  current_content = await read_file(backup["path"])

  await mcp_desktop-commander_edit_block(
    file_path=backup["path"],
    old_string=current_content,
    new_string=backup["content"]
  )

  await ctx.info("Rolled back to backup")

  # Try alternative fix
  prepared_fixes = ctx.get_state("prepared_fixes")
  if len(prepared_fixes) > 1:
    await ctx.info("Trying alternative fix")
    # Use prepared_fixes[1] and repeat stages 6-7
    max_retries = 2
    retry_count = ctx.get_state("retry_count", 0)

    if retry_count < max_retries:
      ctx.set_state("retry_count", retry_count + 1)
      # Retry with alternative fix
      await edit_block(
        file_path=prepared_fixes[1]["file"],
        old_string=prepared_fixes[1]["old_string"],
        new_string=prepared_fixes[1]["new_string"]
      )
      # Re-verify
      await verify_fix()
    else:
      await ctx.error("No alternative fixes available")
      return {
        "status": "error",
        "message": "Fix failed verification and no alternatives",
        "suggestions": "Manual intervention required"
      }
  else:
    await ctx.error("No alternative fixes available")
    return {
      "status": "error",
      "message": "Fix failed verification",
      "suggestions": "Review error and fix manually"
    }

Progress: await ctx.report_progress(7, 7, "Complete")
```

## Smart Detection Examples

**Example 1: Import Error**

```
Terminal shows:
  ImportError: No module named 're'

AI detects:
  - File: src/services/easypost_service.py
  - Line: 391
  - Missing: import re
  - Context: Function uses re.sub() but re not imported

AI analyzes:
  - Root cause: Missing import statement
  - Fix: Add 'import re' at top of file
  - Safety: High (adding import is safe)

AI fixes:
  - Adds 'import re' at top (standard library section)
  - Verifies: Runs tests
  - Result: ✅ All tests passed
```

**Example 2: Type Error**

```
Editor shows:
  TypeError: 'datetime.utcnow()' is deprecated

AI detects:
  - File: src/utils.py
  - Line: 45
  - Issue: Deprecated method usage
  - Context: Python 3.12+ incompatibility

AI analyzes:
  - Root cause: Using deprecated datetime.utcnow()
  - Fix: Replace with datetime.now(timezone.utc)
  - Safety: Medium (need to import timezone)

AI fixes:
  - Adds 'from datetime import timezone'
  - Replaces datetime.utcnow() with datetime.now(timezone.utc)
  - Updates all instances in file
  - Verifies: Runs tests
  - Result: ✅ All tests passed
```

**Example 3: Test Failure**

```
pytest output:
  FAILED tests/test_service.py::test_create - AssertionError

AI detects:
  - Test: test_create
  - File: tests/test_service.py
  - Line: 42
  - Error: AssertionError: expected 200, got 404

AI analyzes:
  - Root cause: Mock not configured correctly
  - Expected call signature changed
  - Fix: Update mock setup

AI fixes:
  - Updates mock setup at line 20
  - Adjusts assertions
  - Verifies: Re-runs test
  - Result: ✅ Test passed
```

## Usage Examples

```bash
# No arguments - detects visible error
/fix

# With specific file (if error not visible)
/fix src/services/easypost_service.py

# With error type hint
/fix import-error
/fix type-error
/fix syntax-error

# Dry-run mode (shows fix without applying)
/fix --dry-run

# Force retry (if previous fix failed)
/fix --retry
```

## Output Format

### Success Output

```
🔍 Error Detection:
Found: ImportError in src/services/easypost_service.py:391
Message: No module named 're'
Context: Function _sanitize_error uses re.sub() but re not imported

🧠 AI Analysis (Sequential-thinking):
Step 1: Error occurs in _sanitize_error method
Step 2: Function uses re.sub() but re not imported
Step 3: Import should be at module level (line 11)
Step 4: Adding import is safe (no side effects)
Root cause: Missing import statement

📚 Best Practice (Context7):
Python imports should be grouped:
1. Standard library (import re)
2. Third-party (import easypost)
3. Local (from src.utils import)

✅ Fix Prepared:
File: src/services/easypost_service.py
Line 11: Add 'import re'
Safety score: 0.95 (high)

💾 Backup Created:
Backed up: src/services/easypost_service.py (1250 lines)

✅ Fix Applied:
File: src/services/easypost_service.py
Line 11: Added 'import re'
Change: Inserted in standard library imports section

🧪 Verification:
Running: pytest tests/unit/test_easypost_service.py -v
Result: ✅ All tests passed (45/45)

✅ Fix complete and verified!
```

### Failure with Retry Output

```
🔍 Error Detection:
Found: TypeError in src/utils.py:45
Message: 'datetime.utcnow()' is deprecated

🧠 AI Analysis:
Root cause: Using deprecated datetime.utcnow()
Fix strategy: Replace with datetime.now(timezone.utc)

✅ Fix Applied:
File: src/utils.py
Line 45: Replaced datetime.utcnow() with datetime.now(timezone.utc)

🧪 Verification:
Running: pytest tests/unit/test_utils.py -v
Result: ❌ 2 tests failed

🔄 Rollback:
Rolled back to backup

🔄 Retrying with Alternative Fix:
File: src/utils.py
Line 1: Added 'from datetime import timezone'
Line 45: Replaced datetime.utcnow() with datetime.now(timezone.utc)

🧪 Verification:
Running: pytest tests/unit/test_utils.py -v
Result: ✅ All tests passed (45/45)

✅ Fix complete and verified!
```

## Performance

- Error detection: <1s (Desktop Commander read_process_output)
- AI analysis: 3-5s (Sequential-thinking with 10-15 thoughts)
- Context7 lookup: 2-4s (cached after first use, optional)
- Fix preparation: 1-2s (Sequential-thinking with 6-8 thoughts)
- Backup creation: <1s (Desktop Commander read_file)
- Fix application: 1-2s (Desktop Commander edit_block)
- Test verification: 3-6s (Desktop Commander start_process)
- **Total: 10-20s** for complete fix cycle (longer with retry)

## Desktop Commander Tools Used

**Primary Tools:**

- `mcp_desktop-commander_edit_block` - Surgical code replacement
- `mcp_desktop-commander_read_process_output` - Detect errors from terminal
- `mcp_desktop-commander_read_file` - Gather context, create backups
- `mcp_desktop-commander_start_process` - Run test verification
- `mcp_desktop-commander_list_sessions` - Check running processes
- `mcp_desktop-commander_start_search` - Find error patterns

**Supporting Tools:**

- `mcp_sequential-thinking_sequentialthinking` - Root cause analysis, fix preparation
- `mcp_Context7_resolve-library-id` - Framework detection
- `mcp_Context7_get-library-docs` - Fix patterns and best practices

## Safety Features

- **Backup before changes**: Complete file snapshot stored
- **Test verification**: Runs tests before finalizing
- **Automatic rollback**: Reverts if tests fail
- **Retry logic**: Tries alternative fixes (max 2 attempts)
- **Dry-run mode**: Shows fix without applying
- **Character-level diff**: Shows exact changes for close matches
- **Multiple fix ranking**: Chooses safest fix first
- **Never overwrites without verification**: All changes tested

## Error Handling Patterns

**Tool Unavailability:**

- Context7 unavailable → Continue with analysis only
- Sequential-thinking unavailable → Use simpler analysis
- Desktop Commander unavailable → Report error, cannot proceed

**Fix Application Failures:**

- Multiple matches → Retry with more context
- No match found → Show character-level diff
- Permission errors → Report and suggest manual fix

**Verification Failures:**

- Tests fail → Rollback and try alternative
- No alternatives → Report manual intervention needed
- Test timeout → Report timeout, suggest manual verification

## Adapts To Any Language

Uses .dev-config.json to determine:

- Test command: `{{testing.backend.framework}}`
- Linter: Python (ruff), JS (eslint), Go (golangci-lint)
- File paths: `{{paths.backend}}`, `{{paths.tests}}`
- Conventions: Naming, formatting standards

**One command. Every error. Any language. Verified fixes.**
