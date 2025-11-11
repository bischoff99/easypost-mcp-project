Automated code review with static analysis, best practices checking, AI-powered review, and optional auto-fixes.

**Context-aware**: No arguments needed - automatically reviews selected code, open file, or git diff. Provides comprehensive analysis with categorized findings and actionable recommendations.

## How It Works

**Complete MCP Workflow (6 Stages):**

**Stage 1 - Gather Code**:
- Reads selected code or file
- Optionally reads git diff
- Prepares code for analysis

**Stage 2 - Static Analysis**:
- Runs linter (ruff, eslint, golangci-lint, cargo clippy)
- Runs type checker (mypy, tsc, go vet)
- Runs security scanner (bandit, npm audit, gosec)
- Parallel execution for speed

**Stage 3 - Best Practices Check**:
- Loads framework-specific best practices via Context7
- Compares code against patterns
- Identifies violations

**Stage 4 - AI Review**:
- Comprehensive Sequential-thinking analysis (15-20 thoughts)
- Checks correctness, security, performance, maintainability
- Identifies edge cases and error handling gaps

**Stage 5 - Generate Report**:
- Categorizes findings (critical/warning/suggestion)
- Structures report with actionable recommendations
- Prioritizes fixes by impact

**Stage 6 - Auto-Fix** (Optional):
- Automatically fixes issues with known solutions
- Verifies each fix
- Reports what was fixed

## MCP Integration

### Stage 1 - Gather Code

```yaml
If file specified:
  Tool: mcp_desktop-commander_read_file
  Path: Specified file (absolute path)
  Read: Complete file content
  
If git diff mode:
  Tool: mcp_desktop-commander_start_process
  Command: "git diff HEAD~1" or "git diff main...feature-branch"
  Timeout: 10000ms
  
If no arguments (default):
  Tool: mcp_desktop-commander_read_file
  Path: Current open file or selected code
  Read: Selected code block or entire file

Progress: await ctx.report_progress(0, 6, "Gathering code for review")
State: ctx.set_state("review_code", {
  "content": code_content,
  "file_path": file_path,
  "language": detected_language
})

Logging:
  await ctx.info(f"Reviewing: {file_path}")
  await ctx.debug(f"Language: {detected_language}")
```

### Stage 2 - Static Analysis

```yaml
Parallel execution (3 tools):

1. Linter check:
   Tool: mcp_desktop-commander_start_process
   Commands by language:
     Python: "ruff check {file}"
     JS: "eslint {file} --format json"
     Go: "golangci-lint run {file} --out-format json"
     Rust: "cargo clippy --message-format json"
   Timeout: 30000ms
   
2. Type check:
   Tool: mcp_desktop-commander_start_process
   Commands:
     Python: "mypy {file} --show-error-codes"
     JS: "tsc --noEmit {file}"
     Go: "go vet {file}"
     Rust: "cargo check --message-format json"
   Timeout: 30000ms

3. Security scan:
   Tool: mcp_desktop-commander_start_process
   Commands:
     Python: "bandit -r {file} -f json"
     JS: "npm audit --json" (if package.json exists)
     Go: "gosec {file} -fmt json"
     Rust: "cargo audit --json"
   Timeout: 30000ms

Progress: await ctx.report_progress(1, 6, "Running static analysis")
State: ctx.set_state("static_analysis", {
  "linter": {
    "errors": [list of linter errors],
    "warnings": [list of warnings]
  },
  "types": {
    "errors": [list of type errors],
    "warnings": [list of type warnings]
  },
  "security": {
    "vulnerabilities": [list of security issues],
    "warnings": [list of security warnings]
  }
})

Logging:
  await ctx.info("Running linter, type checker, and security scanner...")
  await ctx.debug(f"Linter: {len(linter_errors)} errors")
  await ctx.debug(f"Types: {len(type_errors)} errors")
  await ctx.debug(f"Security: {len(security_issues)} issues")

Error handling:
  If tool unavailable:
    await ctx.warning(f"{tool_name} not available, skipping")
    Continue with other tools
```

### Stage 3 - Best Practices Check

```yaml
Tool: mcp_Context7_resolve-library-id
Detect framework from imports or file structure
Examples:
  "fastapi" → /tiangolo/fastapi
  "react" → /facebook/react
  "gin" → /gin-gonic/gin

Tool: mcp_Context7_get-library-docs
Library: Resolved ID
Topic: "code review checklist best practices patterns"
Tokens: 3000

Progress: await ctx.report_progress(2, 6, "Loading best practices")
State: ctx.set_state("best_practices", docs_content)

Error handling:
  from fastmcp.exceptions import ToolError
  try:
    practices = await context7_call()
  except ToolError as e:
    await ctx.warning("Context7 unavailable, using generic best practices")
    practices = None

Logging:
  if practices:
    await ctx.info("Loaded framework-specific best practices")
  else:
    await ctx.warning("Using generic best practices")
```

### Stage 4 - AI Review

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Code + static analysis + best practices
Thoughts: 15-20 (comprehensive review)

Check categories:
  1. Correctness
     - Does it work as intended?
     - Are there logic errors?
     - Edge cases handled?
  
  2. Security
     - Vulnerabilities?
     - Input validation?
     - Authentication/authorization?
     - Sensitive data exposure?
  
  3. Performance
     - Bottlenecks?
     - Unnecessary computations?
     - Memory leaks?
     - Database query optimization?
  
  4. Maintainability
     - Readable code?
     - Well documented?
     - Consistent style?
     - DRY principles?
  
  5. Testing
     - Adequate coverage?
     - Edge cases tested?
     - Error cases tested?
  
  6. Best Practices
     - Follows conventions?
     - Uses framework patterns?
     - Error handling?
     - Logging?

Progress: await ctx.report_progress(3, 6, "Performing AI review")
State: ctx.set_state("ai_review", {
  "findings": [
    {
      "category": "security",
      "severity": "critical",
      "message": "SQL injection vulnerability",
      "line": 42,
      "suggestion": "Use parameterized queries"
    },
    {
      "category": "performance",
      "severity": "warning",
      "message": "N+1 query problem",
      "line": 100,
      "suggestion": "Use eager loading"
    }
  ],
  "summary": "Overall assessment"
})

Output: Categorized findings (critical/warning/suggestion)
Logging:
  await ctx.info(f"Found {len(critical)} critical, {len(warning)} warnings, {len(suggestion)} suggestions")
```

### Stage 5 - Generate Report

```yaml
Format findings into structured report:
  - Summary (overall assessment)
  - Critical issues (must fix)
  - Warnings (should fix)
  - Suggestions (consider)
  - Security findings
  - Performance recommendations
  - Best practice violations

Progress: await ctx.report_progress(4, 6, "Generating report")
State: ctx.set_state("report", {
  "summary": summary_text,
  "critical": [list of critical issues],
  "warnings": [list of warnings],
  "suggestions": [list of suggestions],
  "security": [list of security issues],
  "performance": [list of performance issues],
  "best_practices": [list of violations]
})

Output: Formatted markdown report
Logging: await ctx.info("Report generated")
```

### Stage 6 - Auto-Fix (Optional)

```yaml
If --auto-fix flag:
  For each critical/warning with known fix:
    Tool: mcp_desktop-commander_edit_block
    Apply: Fix automatically
    Verify: Run linter/type checker again
    
    Tool: mcp_desktop-commander_start_process
    Command: Run linter to verify fix
    Check: Issue resolved
    
    Progress: await ctx.report_progress(5, 6, f"Applying fix {i}/{total}")
    Logging:
      await ctx.info(f"Fixed: {issue_description}")
      if verified:
        await ctx.info("Fix verified")
      else:
        await ctx.warning("Fix applied but verification failed")
  
  Progress: await ctx.report_progress(6, 6, "Complete")
```

## Usage Examples

```bash
# Review selected code or open file
/review

# Review specific file
/review backend/src/services/easypost_service.py

# Review git diff
/review --diff HEAD~1
/review --diff main...feature-branch

# Auto-fix issues
/review --auto-fix

# Review with focus
/review --focus=security
/review --focus=performance
```

## Output Format

### Review Report

```
📋 Code Review Report
File: backend/src/services/easypost_service.py
Language: Python
Framework: FastAPI

📊 Summary:
Overall assessment: Good code quality with minor improvements needed.
Found 2 critical issues, 5 warnings, 8 suggestions.

🔴 Critical Issues (Must Fix):

1. Security: SQL Injection Vulnerability
   Line: 142
   Issue: Direct string interpolation in SQL query
   Code: query = f"SELECT * FROM shipments WHERE id = {shipment_id}"
   Risk: High - Allows SQL injection attacks
   Fix: Use parameterized queries
   Suggestion:
     query = "SELECT * FROM shipments WHERE id = %s"
     cursor.execute(query, (shipment_id,))

2. Security: Hardcoded API Key
   Line: 28
   Issue: API key hardcoded in source code
   Code: api_key = "ep_test_123456789"
   Risk: Critical - Exposes credentials
   Fix: Use environment variable
   Suggestion:
     import os
     api_key = os.getenv("EASYPOST_API_KEY")

⚠️ Warnings (Should Fix):

1. Performance: N+1 Query Problem
   Line: 100-105
   Issue: Query executed in loop
   Code:
     for shipment in shipments:
         address = get_address(shipment.address_id)
   Fix: Use eager loading or batch query
   Suggestion:
     addresses = get_addresses_batch([s.address_id for s in shipments])
     for shipment in shipments:
         shipment.address = addresses[shipment.address_id]

2. Maintainability: Long Function
   Line: 50-200
   Issue: Function exceeds 150 lines
   Code: def create_shipment(...)
   Fix: Extract into smaller functions
   Suggestion: Extract validation, API call, response formatting

3. Error Handling: Missing Try-Catch
   Line: 80
   Issue: API call without error handling
   Code: response = easypost.Shipment.create(...)
   Fix: Add try-except block
   Suggestion:
     try:
         response = easypost.Shipment.create(...)
     except easypost.Error as e:
         logger.error(f"EasyPost API error: {e}")
         raise

💡 Suggestions (Consider):

1. Documentation: Missing Docstring
   Line: 50
   Issue: Function lacks docstring
   Suggestion: Add Google-style docstring

2. Type Hints: Missing Return Type
   Line: 50
   Issue: Function missing return type hint
   Suggestion: Add -> ShipmentResponse

3. Testing: Missing Edge Case Test
   Issue: No test for empty address list
   Suggestion: Add test_empty_address_list()

📚 Best Practices:

✅ Good:
- Uses async/await correctly
- Proper error logging
- Type hints present (mostly)

❌ Violations:
- Missing docstrings
- Long functions (>100 lines)
- Direct SQL queries (should use ORM)

🔒 Security Findings:

Critical:
- SQL injection vulnerability (line 142)
- Hardcoded API key (line 28)

Warnings:
- No input validation on user input
- Sensitive data in logs

⚡ Performance Recommendations:

1. N+1 query problem (line 100)
2. Missing database indexes
3. No caching for repeated queries

✅ Auto-Fixes Applied (if --auto-fix):

1. ✅ Fixed: Added try-except block (line 80)
2. ✅ Fixed: Added missing import (line 5)
3. ⚠️ Skipped: SQL injection (requires manual review)
```

## Performance

- Code gathering: <1s (read_file or git diff)
- Static analysis: 5-15s (parallel execution of 3 tools)
- Best practices: 2-4s (Context7 lookup, cached 24h)
- AI review: 8-12s (Sequential-thinking with 15-20 thoughts)
- Report generation: 1-2s
- Auto-fix: 5-10s per fix (if --auto-fix)
- **Total: 17-34s** for complete review (longer with auto-fix)

## Desktop Commander Tools Used

**Primary Tools:**
- `mcp_desktop-commander_read_file` - Read code for review
- `mcp_desktop-commander_start_process` - Run linters, type checkers, security scanners
- `mcp_desktop-commander_edit_block` - Apply auto-fixes
- `mcp_sequential-thinking_sequentialthinking` - AI-powered review
- `mcp_Context7_resolve-library-id` - Framework detection
- `mcp_Context7_get-library-docs` - Best practices loading

## Error Handling

**File Not Found:**
- Report error: "File not found"
- Suggest checking file path

**Tool Unavailability:**
- Skip unavailable tools
- Report warning
- Continue with available tools

**Analysis Failures:**
- Report error with tool output
- Continue with other analysis tools
- Provide partial results

## Adapts To Any Language

Works automatically with:
- Python (ruff, mypy, bandit)
- JavaScript/TypeScript (eslint, tsc, npm audit)
- Go (golangci-lint, go vet, gosec)
- Rust (cargo clippy, cargo check, cargo audit)

**One command. Comprehensive review. Any language. Actionable fixes.**
