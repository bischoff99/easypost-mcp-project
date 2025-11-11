Safe, verified code refactoring with automatic test verification and rollback capabilities.

**Context-aware**: No arguments needed - automatically refactors selected code or open file. Identifies refactoring opportunities, applies transformations safely, and verifies with tests.

## How It Works

**Complete MCP Workflow (6 Stages):**

**Stage 1 - Analyze Code**:
- Reads code to refactor
- Identifies refactoring opportunities
- Categorizes improvements needed

**Stage 2 - Get Best Practices**:
- Loads refactoring patterns via Context7
- Gets framework-specific guidelines
- Caches patterns for reuse

**Stage 3 - Plan Refactoring**:
- Generates step-by-step refactoring plan
- Orders transformations by safety
- Validates plan won't break code

**Stage 4 - Backup + Apply**:
- Creates backup of original code
- Applies refactoring transformations
- One edit at a time for safety

**Stage 5 - Test Verification**:
- Runs tests for refactored code
- Verifies all tests still pass
- Automatic rollback on failure

**Stage 6 - Generate Report**:
- Reports what was refactored
- Shows improvements made
- Confirms test status

## MCP Integration

### Stage 1 - Analyze Code

```yaml
Tool: mcp_desktop-commander_read_file
Path: File or selection to refactor (absolute path)
Read: Complete code content

Tool: mcp_sequential-thinking_sequentialthinking
Thoughts: 10-12
Identify refactoring opportunities:
  1. Duplicate code (DRY violations)
  2. Long functions (>50 lines)
  3. Complex conditionals
  4. Poor naming
  5. Missing abstractions
  6. Unused code
  7. Magic numbers/strings
  8. Tight coupling
  9. Low cohesion
  10. Missing error handling

Progress: await ctx.report_progress(0, 6, "Analyzing code")
State: ctx.set_state("refactor_opportunities", [
  {
    "type": "extract_function",
    "description": "Extract validation logic into separate function",
    "location": {"file": file_path, "line": 50, "end_line": 80},
    "priority": "high",
    "safety": 0.9
  },
  {
    "type": "rename_variable",
    "description": "Rename 'x' to 'shipment_id'",
    "location": {"file": file_path, "line": 25},
    "priority": "medium",
    "safety": 0.95
  },
  {
    "type": "remove_duplication",
    "description": "Extract common error handling pattern",
    "location": {"file": file_path, "lines": [100, 150, 200]},
    "priority": "high",
    "safety": 0.85
  }
])

Logging:
  await ctx.info(f"Found {len(opportunities)} refactoring opportunities")
  await ctx.debug(f"High priority: {len([o for o in opportunities if o['priority'] == 'high'])}")
```

### Stage 2 - Get Best Practices

```yaml
Tool: mcp_Context7_resolve-library-id
Detect framework from file imports or structure
Examples:
  "fastapi" → /tiangolo/fastapi
  "react" → /facebook/react

Tool: mcp_Context7_get-library-docs
Library: Resolved ID
Topic: "refactoring patterns clean code principles"
Tokens: 2500

Progress: await ctx.report_progress(1, 6, "Loading refactoring patterns")
State: ctx.set_state("refactoring_patterns", patterns_content)

Error handling:
  from fastmcp.exceptions import ToolError
  try:
    patterns = await context7_call()
  except ToolError as e:
    await ctx.warning("Context7 unavailable, using generic patterns")
    patterns = None

Logging:
  if patterns:
    await ctx.info("Loaded refactoring patterns")
  else:
    await ctx.warning("Using generic refactoring patterns")
```

### Stage 3 - Plan Refactoring

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Opportunities + best practices
Thoughts: 8-10
Generate: Step-by-step refactoring plan

Plan structure:
  1. Extract function X (safe, high impact)
  2. Rename variable Y (safe, improves readability)
  3. Remove duplication Z (medium safety, high impact)
  4. Add docstring (safe, improves documentation)
  5. Extract constant (safe, removes magic number)

Order: Safe transformations first
  - Rename operations (safest)
  - Extract constants
  - Extract functions
  - Remove duplication
  - Restructure (riskiest)

Progress: await ctx.report_progress(2, 6, "Planning refactoring")
State: ctx.set_state("refactor_plan", [
  {
    "step": 1,
    "type": "extract_function",
    "description": "Extract validation logic",
    "old_string": "exact code to replace",
    "new_string": "refactored code",
    "safety_score": 0.9,
    "test_after": True
  },
  # More steps...
])

Logging:
  await ctx.info(f"Planned {len(plan)} refactoring steps")
  await ctx.debug("Order: Safe transformations first")
```

### Stage 4 - Backup + Apply

```yaml
Tool: mcp_desktop-commander_read_file
Path: File to refactor
Action: Read complete current content
Backup: Store in state

State: ctx.set_state("backup", {
  "path": file_path,
  "content": current_content,
  "timestamp": datetime.now().isoformat()
})

For each refactoring step:
  Tool: mcp_desktop-commander_edit_block
  Parameters:
    file_path: Absolute path
    old_string: From refactor_plan step
    new_string: From refactor_plan step
    expected_replacements: 1
  
  Verify: Syntax still valid (if language supports)
    Tool: mcp_desktop-commander_start_process
    Command: Syntax check
      Python: "python -m py_compile {file}"
      JS: "node --check {file}"
      Go: "go build {file}"
      Rust: "cargo check"
  
  Progress: await ctx.report_progress(3, 6, f"Applying step {i}/{total}")
  Logging:
    await ctx.info(f"Applied: {step_description}")
    if syntax_valid:
      await ctx.debug("Syntax valid")
    else:
      await ctx.error("Syntax error, rolling back")
      # Rollback this step
      await rollback_step()

Best practice: One edit_block per logical change
Error handling:
  If edit fails:
    await ctx.error(f"Failed to apply step {i}")
    await rollback_to_backup()
    return {"status": "error", "message": "Refactoring failed"}
```

### Stage 5 - Test Verification

```yaml
Tool: mcp_desktop-commander_start_process
Command: Run tests for refactored code
  Python: "pytest {test_file} -v"
  JS: "vitest run {test_file}"
  Go: "go test {package} -v"
  Rust: "cargo test"

Timeout: 60000ms

Progress: await ctx.report_progress(4, 6, "Verifying refactoring")

Success path:
  Tool: mcp_desktop-commander_read_process_output
  PID: Test process PID
  Parse: Test results
  
  if "passed" in output or "PASS" in output:
    await ctx.info("All tests passed, refactoring successful")
    ctx.clear_state("backup")  # No longer needed
    return {
      "status": "success",
      "message": "Refactoring complete and verified",
      "changes": refactor_plan
    }

Failure path:
  await ctx.error("Refactoring broke tests, rolling back")
  
  # Rollback using backup
  backup = ctx.get_state("backup")
  current_content = await read_file(backup["path"])
  
  await mcp_desktop-commander_edit_block(
    file_path=backup["path"],
    old_string=current_content,
    new_string=backup["content"]
  )
  
  await ctx.info("Rolled back to backup")
  return {
    "status": "error",
    "message": "Refactoring broke tests, rolled back",
    "test_output": test_output
  }

Logging:
  await ctx.info("Running tests to verify refactoring...")
```

### Stage 6 - Generate Report

```yaml
Report what was refactored:
  - Functions extracted
  - Variables renamed
  - Code removed
  - Improvements made
  - Test status

Progress: await ctx.report_progress(5, 6, "Generating report")
State: ctx.set_state("report", {
  "summary": summary_text,
  "changes": [
    {
      "type": "extract_function",
      "description": "Extracted validation logic",
      "before": "50 lines in main function",
      "after": "30 lines + 20 lines in extracted function"
    }
  ],
  "test_status": "passed",
  "improvements": [
    "Reduced function length from 80 to 30 lines",
    "Improved code reusability",
    "Added documentation"
  ]
})

Output: Formatted markdown report
Logging: await ctx.info("Report generated")
```

## Refactoring Types Supported

**Extract Function:**
- Long functions → Smaller, focused functions
- Duplicate code → Shared function
- Complex logic → Separate function

**Extract Variable:**
- Magic numbers → Named constants
- Complex expressions → Intermediate variables

**Rename:**
- Poor names → Descriptive names
- Abbreviations → Full words
- Generic names → Specific names

**Remove Duplication:**
- Repeated code → Shared function
- Similar patterns → Parameterized function

**Simplify Conditionals:**
- Complex if/else → Early returns
- Nested conditions → Guard clauses
- Boolean logic → Clearer expressions

**Extract Class:**
- Large classes → Smaller, focused classes
- Mixed responsibilities → Single responsibility

## Usage Examples

```bash
# Refactor selected code or open file
/refactor

# Refactor specific file
/refactor backend/src/services/easypost_service.py

# Refactor with focus
/refactor --focus=functions
/refactor --focus=naming
/refactor --focus=duplication

# Dry-run (show plan without applying)
/refactor --dry-run
```

## Output Format

### Success Output

```
🔍 Analyzing Code:
File: backend/src/services/easypost_service.py
Found: 5 refactoring opportunities

📚 Refactoring Patterns:
Loaded: FastAPI refactoring best practices

📋 Refactoring Plan:
1. Extract validation function (high priority, safe)
2. Rename variable 'x' to 'shipment_id' (medium priority, safe)
3. Extract common error handling (high priority, medium safety)
4. Add docstring (low priority, safe)
5. Extract constant for API endpoint (medium priority, safe)

💾 Backup Created:
Backed up: backend/src/services/easypost_service.py (1250 lines)

✅ Applying Refactoring:
Step 1/5: Extracting validation function...
  ✅ Applied: Extracted validate_address() function
  ✅ Syntax valid

Step 2/5: Renaming variable...
  ✅ Applied: Renamed 'x' to 'shipment_id'
  ✅ Syntax valid

Step 3/5: Extracting error handling...
  ✅ Applied: Extracted handle_api_error() function
  ✅ Syntax valid

Step 4/5: Adding docstring...
  ✅ Applied: Added Google-style docstring
  ✅ Syntax valid

Step 5/5: Extracting constant...
  ✅ Applied: Extracted API_ENDPOINT constant
  ✅ Syntax valid

🧪 Verifying Refactoring:
Running: pytest backend/tests/unit/test_service.py -v
Result: ✅ All tests passed (45/45)

✅ Refactoring Complete:
- Functions extracted: 2
- Variables renamed: 1
- Constants extracted: 1
- Docstrings added: 1
- Test status: ✅ All passed

Improvements:
- Reduced function length from 80 to 30 lines
- Improved code reusability
- Enhanced readability
- Added documentation
```

### Failure with Rollback Output

```
🔍 Analyzing Code:
Found: 3 refactoring opportunities

📋 Refactoring Plan:
1. Extract function (safe)
2. Rename variable (safe)
3. Restructure logic (risky)

✅ Applying Refactoring:
Step 1/3: ✅ Applied
Step 2/3: ✅ Applied
Step 3/3: ✅ Applied

🧪 Verifying Refactoring:
Running: pytest backend/tests/unit/test_service.py -v
Result: ❌ 2 tests failed

🔄 Rollback:
Rolled back to backup
File restored: backend/src/services/easypost_service.py

❌ Refactoring Failed:
Reason: Tests failed after step 3
Suggestion: Review step 3 (restructure logic) - may have changed behavior
```

## Performance

- Code analysis: 3-5s (Sequential-thinking with 10-12 thoughts)
- Best practices: 2-4s (Context7 lookup, cached 24h)
- Planning: 2-3s (Sequential-thinking with 8-10 thoughts)
- Backup: <1s (read_file)
- Apply refactoring: 2-5s per step (edit_block + syntax check)
- Test verification: 3-10s (test execution)
- Report generation: <1s
- **Total: 12-28s** for complete refactoring cycle

## Desktop Commander Tools Used

**Primary Tools:**
- `mcp_desktop-commander_read_file` - Read code, create backups
- `mcp_desktop-commander_edit_block` - Apply refactoring transformations
- `mcp_desktop-commander_start_process` - Run tests, syntax checks
- `mcp_desktop-commander_read_process_output` - Parse test results
- `mcp_sequential-thinking_sequentialthinking` - Code analysis, planning
- `mcp_Context7_resolve-library-id` - Framework detection
- `mcp_Context7_get-library-docs` - Refactoring patterns

## Safety Features

- **Backup before changes**: Complete file snapshot
- **One edit at a time**: Apply transformations sequentially
- **Syntax validation**: Check syntax after each edit
- **Test verification**: Run tests before finalizing
- **Automatic rollback**: Revert if tests fail
- **Safe ordering**: Apply safest transformations first
- **Dry-run mode**: Show plan without applying

## Error Handling

**Syntax Errors:**
- Rollback failed step
- Report error
- Continue with remaining steps (if possible)

**Test Failures:**
- Rollback all changes
- Report which step caused failure
- Suggest manual review

**Tool Unavailability:**
- Skip unavailable tools
- Continue with available analysis
- Report warnings

## Adapts To Any Language

Works automatically with:
- Python (pytest for verification)
- JavaScript/TypeScript (vitest for verification)
- Go (go test for verification)
- Rust (cargo test for verification)

**One command. Safe refactoring. Verified changes. Any language.**
