Review and simplify codebase by identifying enterprise features, overbloat, unnecessary complexity, and optimization overkill for personal use.

**Context-aware**: No arguments needed - automatically scans codebase for enterprise patterns, overbloat, complexity, and optimization overkill. Provides comprehensive analysis with prioritized recommendations and optional auto-simplification.

## How It Works

**Complete MCP Workflow (7 Stages):**

**Stage 1 - Scan Codebase**:

- Searches for enterprise patterns (webhooks, multi-tenancy, audit logs, complex caching, microservices)
- Identifies overbloat (unused code, excessive abstractions, premature optimizations)
- Detects complexity (long functions, deep nesting, large classes)
- Maps code structure and dependencies

**Stage 2 - Analyze Complexity**:

- Calculates cyclomatic complexity
- Measures dependency depth
- Identifies code smells and anti-patterns
- Analyzes optimization overkill

**Stage 3 - Get Simplification Patterns**:

- Loads best practices via Context7
- Gets patterns for personal-use applications
- Caches patterns for reuse

**Stage 4 - Classify Issues**:

- Categorizes findings (enterprise feature, overbloat, optimization overkill, complexity)
- Prioritizes by impact and effort
- Groups related issues
- Determines safe removal order

**Stage 5 - Generate Recommendations**:

- Creates prioritized simplification plan
- Estimates effort and impact
- Suggests safe removal order
- Includes optimization simplifications

**Stage 6 - Apply Simplifications** (Optional):

- Removes enterprise features safely
- Simplifies complex code
- Cleans up unused code
- Simplifies optimizations (workers, configs)
- Verifies changes don't break functionality

**Stage 7 - Verify**:

- Runs tests to ensure nothing broke
- Checks for broken imports/references
- Reports simplification results

## Enterprise Patterns Detected

**Webhook Systems:**

- Webhook handlers, webhook services
- Webhook event processing
- Webhook signature verification

**Multi-Tenancy:**

- Tenant isolation logic
- Tenant-specific configurations
- Multi-tenant database schemas

**Audit Logs:**

- Audit trail systems
- Change tracking
- Compliance logging

**Complex Caching:**

- Redis/memcached layers
- Cache invalidation strategies
- Distributed caching

**Microservices Patterns:**

- Service discovery
- API gateways
- Inter-service communication

**Other Enterprise Features:**

- Rate limiting middleware
- Complex authentication/authorization
- Event sourcing
- CQRS patterns
- Message queues
- Distributed systems

## Overbloat Patterns

**Unused Code:**

- Unused imports
- Dead functions/classes
- Unused dependencies
- Commented-out code

**Excessive Abstractions:**

- Unnecessary layers
- Over-abstracted patterns
- Premature generalization
- Factory patterns where simple constructors work

**Premature Optimizations:**

- Complex caching where simple in-memory works
- Parallel processing where sequential is fine
- Database optimizations for small datasets
- Micro-optimizations without profiling

**Documentation Bloat:**

- Excessive documentation files
- Redundant guides
- Over-detailed comments

## Optimization Overkill

**Worker Overkill:**

- Fixed high worker counts (32+) instead of auto-detection
- Excessive parallel processing
- Over-provisioned thread pools

**Config Overkill:**

- Heavy optimizations enabled unnecessarily
- Complex configuration layers
- Premature performance tuning

**Documentation Overkill:**

- Excessive optimization documentation
- Over-detailed performance guides
- Redundant optimization references

## MCP Integration

### Stage 1 - Scan Codebase

```yaml
Tool: mcp_desktop-commander_start_search
Patterns (multiple searches):
  Enterprise patterns:
    - "webhook" (case-insensitive)
    - "multi.?tenant" (regex)
    - "audit.?log"
    - "rate.?limit"
    - "service.?discovery"
    - "event.?sourcing"
    - "cqrs"
    - "message.?queue"

  Overbloat patterns:
    - "TODO|FIXME|XXX|HACK" (commented code markers)
    - "unused|deprecated|legacy" (comments)
    - "factory|builder|strategy" (design patterns)

  Complexity indicators:
    - Deep nesting (if/for/while chains)
    - Long functions (>100 lines)
    - Large classes (>500 lines)

  Optimization overkill:
    - Fixed worker counts (32, 40, 64)
    - "uvloop|threadPoolScaling" (heavy optimizations)

SearchType: "content"
ContextLines: 3

Progress: await ctx.report_progress(0, 7, "Scanning codebase")
State: ctx.set_state("scan_results", {
  "enterprise_patterns": [
    {
      "type": "webhook",
      "file": "src/routers/webhooks.py",
      "line": 10,
      "pattern": "webhook handler",
      "severity": "high"
    }
  ],
  "overbloat": [
    {
      "type": "unused_code",
      "file": "src/services/old_service.py",
      "line": 50,
      "pattern": "unused function",
      "severity": "medium"
    }
  ],
  "complexity": [
    {
      "type": "long_function",
      "file": "src/services/complex.py",
      "line": 100,
      "metric": "250 lines",
      "severity": "high"
    }
  ],
  "optimization_overkill": [
    {
      "type": "fixed_workers",
      "file": "pytest.ini",
      "line": 5,
      "pattern": "workers = 32",
      "severity": "medium"
    }
  ]
})

Logging:
  await ctx.info(f"Found {len(enterprise_patterns)} enterprise patterns")
  await ctx.info(f"Found {len(overbloat)} overbloat issues")
  await ctx.info(f"Found {len(complexity)} complexity issues")
  await ctx.info(f"Found {len(optimization_overkill)} optimization overkill issues")
```

### Stage 2 - Analyze Complexity

```yaml
Tool: mcp_desktop-commander_read_file
Files: All files with complexity issues
Read: Complete file content

Tool: mcp_sequential-thinking_sequentialthinking
Input: File content + complexity metrics
Thoughts: 8-10
Analyze:
  1. What makes this code complex?
  2. Can it be simplified?
  3. What dependencies does it have?
  4. What would break if simplified?
  5. What's the simplest equivalent?
  6. Are optimizations necessary or premature?
  7. Can worker counts be auto-detected?
  8. Are configs over-complicated?

Progress: await ctx.report_progress(1, 7, "Analyzing complexity")
State: ctx.set_state("complexity_analysis", {
  "files": [
    {
      "file": "src/services/complex.py",
      "cyclomatic_complexity": 25,
      "dependency_depth": 5,
      "simplification_opportunity": "Extract functions, reduce nesting",
      "effort": "medium",
      "impact": "high"
    }
  ],
  "optimizations": [
    {
      "file": "pytest.ini",
      "issue": "Fixed 32 workers instead of auto-detection",
      "simplification": "Use -n auto",
      "effort": "low",
      "impact": "medium"
    }
  ]
})

Logging:
  await ctx.info(f"Analyzed {len(files)} complex files")
  await ctx.info(f"Found {len(optimizations)} optimization simplifications")
```

### Stage 3 - Get Simplification Patterns

```yaml
Tool: mcp_Context7_resolve-library-id
Query: Detect framework from project
Examples:
  "fastapi" → /tiangolo/fastapi
  "react" → /facebook/react
  "gin" → /gin-gonic/gin

Tool: mcp_Context7_get-library-docs
Library: Resolved ID
Topic: "simplification patterns personal use applications best practices"
Tokens: 3000

Progress: await ctx.report_progress(2, 7, "Loading simplification patterns")
State: ctx.set_state("simplification_patterns", patterns_content)

Error handling:
  from fastmcp.exceptions import ToolError
  try:
    patterns = await context7_call()
  except ToolError as e:
    await ctx.warning("Context7 unavailable, using generic patterns")
    patterns = None

Logging:
  if patterns:
    await ctx.info("Loaded simplification patterns")
  else:
    await ctx.warning("Using generic simplification patterns")
```

### Stage 4 - Classify Issues

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Scan results + complexity analysis + simplification patterns
Thoughts: 10-12
Classify:
  1. Enterprise feature vs overbloat vs complexity vs optimization overkill
  2. Priority (critical/high/medium/low)
  3. Effort to fix (low/medium/high)
  4. Impact of removal (high/medium/low)
  5. Safe removal order
  6. Dependencies between issues
  7. What breaks if removed?
  8. Can it be simplified instead of removed?

Progress: await ctx.report_progress(3, 7, "Classifying issues")
State: ctx.set_state("classified_issues", {
  "enterprise_features": [
    {
      "type": "webhook",
      "file": "src/routers/webhooks.py",
      "priority": "high",
      "effort": "low",
      "impact": "high",
      "safe_to_remove": True,
      "dependencies": []
    }
  ],
  "overbloat": [
    {
      "type": "unused_code",
      "file": "src/services/old_service.py",
      "priority": "medium",
      "effort": "low",
      "impact": "medium",
      "safe_to_remove": True
    }
  ],
  "complexity": [
    {
      "type": "long_function",
      "file": "src/services/complex.py",
      "priority": "high",
      "effort": "medium",
      "impact": "high",
      "simplification": "Extract into smaller functions"
    }
  ],
  "optimization_overkill": [
    {
      "type": "fixed_workers",
      "file": "pytest.ini",
      "priority": "medium",
      "effort": "low",
      "impact": "medium",
      "simplification": "Use -n auto instead of fixed count"
    }
  ]
})

Logging:
  await ctx.info(f"Classified {len(enterprise_features)} enterprise features")
  await ctx.info(f"Classified {len(overbloat)} overbloat issues")
  await ctx.info(f"Classified {len(complexity)} complexity issues")
  await ctx.info(f"Classified {len(optimization_overkill)} optimization simplifications")
```

### Stage 5 - Generate Recommendations

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Classified issues + simplification patterns
Thoughts: 12-15
Generate: Prioritized simplification plan

Plan structure:
  1. Remove enterprise features (safe, high impact)
  2. Remove unused code (safe, medium impact)
  3. Simplify optimizations (low effort, medium impact)
  4. Simplify complex code (medium effort, high impact)
  5. Clean up documentation (low effort, low impact)

Progress: await ctx.report_progress(4, 7, "Generating recommendations")
State: ctx.set_state("recommendations", {
  "plan": [
    {
      "step": 1,
      "action": "remove",
      "target": "src/routers/webhooks.py",
      "reason": "Enterprise feature, not needed for personal use",
      "effort": "low",
      "impact": "high",
      "safe": True
    },
    {
      "step": 2,
      "action": "simplify",
      "target": "pytest.ini",
      "reason": "Fixed workers (32) → auto-detection (-n auto)",
      "effort": "low",
      "impact": "medium",
      "safe": True
    },
    {
      "step": 3,
      "action": "simplify",
      "target": "src/services/complex.py",
      "reason": "Long function (250 lines), extract into smaller functions",
      "effort": "medium",
      "impact": "high",
      "safe": True
    }
  ],
  "summary": {
    "total_issues": 15,
    "enterprise_features": 5,
    "overbloat": 7,
    "complexity": 3,
    "optimization_overkill": 3,
    "estimated_time": "2-3 hours",
    "risk": "low"
  }
})

Logging:
  await ctx.info(f"Generated {len(plan)} recommendations")
  await ctx.info(f"Estimated time: {estimated_time}")
```

### Stage 6 - Apply Simplifications (if --apply)

```yaml
For each recommendation:
  If action == "remove":
    # Check for imports/references first
    Tool: mcp_desktop-commander_start_search
    Pattern: Import/reference to target file
    SearchType: "content"
    Find: All references

    # Remove references
    For each reference:
      Tool: mcp_desktop-commander_edit_block
      Remove: Import/reference

    # Delete file
    Tool: mcp_desktop-commander_delete_file
    Path: Target file (absolute path)

  If action == "simplify":
    Tool: mcp_desktop-commander_read_file
    Read: File to simplify

    Tool: mcp_sequential-thinking_sequentialthinking
    Generate: Simplified version

    Tool: mcp_desktop-commander_edit_block
    Replace: Complex code with simplified version

    # For optimization simplifications:
    # Example: pytest.ini workers = 32 → -n auto
    # Example: .dev-config.json uvloop: true → false

  If action == "clean":
    Tool: mcp_desktop-commander_edit_block
    Remove: Unused imports, dead code, comments

Progress: await ctx.report_progress(5, 7, f"Applying simplification {i}/{total}")
Logging:
  await ctx.info(f"Applied: {action} on {target}")
```

### Stage 7 - Verify

```yaml
Tool: mcp_desktop-commander_start_process
Command: Run tests
  Python: "pytest -v"
  JS: "vitest run"
  Go: "go test ./..."
  Rust: "cargo test"

Timeout: 120000ms

Tool: mcp_desktop-commander_start_process
Command: Check for broken imports
  Python: "python -m py_compile **/*.py" or "mypy ."
  JS: "tsc --noEmit"
  Go: "go build ./..."
  Rust: "cargo check"

Progress: await ctx.report_progress(6, 7, "Verifying changes")

Success path:
  if tests_pass and no_broken_imports:
    await ctx.info("All simplifications verified")
    return {
      "status": "success",
      "simplified": count_simplified,
      "removed": count_removed,
      "tests": "passed"
    }

Failure path:
  await ctx.error("Some simplifications broke tests")
  # Report which changes caused issues
  return {
    "status": "partial",
    "simplified": count_simplified,
    "failed": count_failed,
    "issues": [list of issues]
  }

Progress: await ctx.report_progress(7, 7, "Complete")
```

## Usage Examples

```bash
# Analyze and show recommendations (default)
/simplify

# Apply simplifications automatically
/simplify --apply

# Focus on specific category
/simplify --focus=enterprise
/simplify --focus=overbloat
/simplify --focus=complexity
/simplify --focus=optimization

# Dry-run mode (show what would be done)
/simplify --dry-run

# Specific file or directory
/simplify backend/src/services/
```

## Output Format

### Analysis Output

```
🔍 Scanning Codebase:
Scanning for enterprise patterns, overbloat, complexity, and optimization overkill...

📊 Scan Results:
Found: 18 issues total
  - Enterprise features: 5
  - Overbloat: 7
  - Complexity: 3
  - Optimization overkill: 3

🧠 Analyzing Complexity:
Analyzing 3 complex files...
  - src/services/complex.py: Cyclomatic complexity 25, dependency depth 5
  - src/routers/analytics.py: Long function (250 lines)
  - src/utils/cache.py: Over-abstracted caching layer

📋 Classifying Issues:
Enterprise Features (5):
  1. src/routers/webhooks.py - Webhook handlers (high priority, safe to remove)
  2. src/services/webhook_service.py - Webhook service (high priority, safe to remove)
  3. src/middleware/rate_limit.py - Rate limiting (medium priority, safe to remove)
  4. src/models/audit.py - Audit logging (low priority, safe to remove)
  5. docs/architecture/webhooks.md - Webhook documentation (low priority, safe to remove)

Overbloat (7):
  1. src/services/old_service.py - Unused service (medium priority)
  2. src/utils/complex_cache.py - Over-engineered caching (high priority)
  3. src/models/tenant.py - Multi-tenancy models (high priority)
  4. Unused imports in 12 files (low priority)
  5. Commented-out code in 5 files (low priority)
  6. Redundant documentation files (low priority)
  7. Unused dependencies in package.json (medium priority)

Complexity (3):
  1. src/services/complex.py - Long function (250 lines) - Extract into smaller functions
  2. src/routers/analytics.py - Deep nesting (5 levels) - Flatten conditionals
  3. src/utils/cache.py - Over-abstracted - Simplify to direct calls

Optimization Overkill (3):
  1. pytest.ini - Fixed workers (32) → Use -n auto (low effort, medium impact)
  2. .dev-config.json - Heavy optimizations enabled → Disable for personal use
  3. docs/05-m3-max-optimizations.mdc - 475 lines → Reduce to ~100 lines

📚 Simplification Patterns:
Loaded: Personal-use application patterns

💡 Recommendations:
Priority Order:
  1. Remove webhook system (low effort, high impact)
  2. Simplify pytest.ini workers (low effort, medium impact)
  3. Remove multi-tenancy models (low effort, high impact)
  4. Simplify complex service (medium effort, high impact)
  5. Remove unused code (low effort, medium impact)
  6. Simplify optimization docs (low effort, low impact)
  7. Clean up documentation (low effort, low impact)

Estimated Time: 2-3 hours
Risk Level: Low (all changes are safe)

✅ Analysis Complete
```

### Applied Simplifications Output

```
🔍 Scanning Codebase:
Found: 18 issues

💡 Recommendations Generated:
5 enterprise features, 7 overbloat, 3 complexity, 3 optimization overkill

✅ Applying Simplifications:

Step 1/18: Removing webhook router...
  ✅ Deleted: src/routers/webhooks.py
  ✅ Removed 3 imports referencing webhooks
  ✅ Updated server.py to remove webhook routes

Step 2/18: Simplifying pytest.ini...
  ✅ Changed: workers = 32 → -n auto
  ✅ Updated: pytest.ini

Step 3/18: Removing webhook service...
  ✅ Deleted: src/services/webhook_service.py
  ✅ Removed 2 imports

Step 4/18: Simplifying complex service...
  ✅ Extracted 5 functions from long function
  ✅ Reduced from 250 to 50 lines per function
  ✅ Improved readability

...

Step 18/18: Cleaning up documentation...
  ✅ Removed 3 redundant documentation files

🧪 Verifying Changes:
Running: pytest -v
Result: ✅ All tests passed (45/45)

Checking imports...
Result: ✅ No broken imports

✅ Simplification Complete:
  - Removed: 8 files
  - Simplified: 6 files
  - Cleaned: 4 files
  - Tests: ✅ All passed
  - Imports: ✅ All valid

Summary:
  - Enterprise features removed: 5
  - Overbloat removed: 7
  - Complexity reduced: 3
  - Optimizations simplified: 3
  - Total time: 2.5 hours
```

## Performance

- Codebase scan: 5-10s (multiple searches)
- Complexity analysis: 3-5s per file (Sequential-thinking)
- Classification: 2-3s (Sequential-thinking)
- Pattern loading: 2-4s (Context7, cached 24h)
- Recommendation generation: 3-5s (Sequential-thinking)
- Application: 10-30s per item (depends on complexity)
- Verification: 10-30s (test execution)
- **Total: 30-90s** for analysis, **5-30 minutes** for full application

## Desktop Commander Tools Used

**Primary Tools:**

- `mcp_desktop-commander_start_search` - Find enterprise patterns, overbloat
- `mcp_desktop-commander_read_file` - Read files for analysis
- `mcp_desktop-commander_delete_file` - Remove enterprise features
- `mcp_desktop-commander_edit_block` - Simplify code, remove references, update configs
- `mcp_desktop-commander_start_process` - Run tests, check imports
- `mcp_desktop-commander_list_directory` - Scan directory structure

**Supporting Tools:**

- `mcp_sequential-thinking_sequentialthinking` - Complexity analysis, recommendations, simplification planning
- `mcp_Context7_resolve-library-id` - Framework detection
- `mcp_Context7_get-library-docs` - Simplification patterns

## Safety Features

- **Dry-run mode**: Show recommendations without applying
- **Test verification**: Run tests after each simplification
- **Import checking**: Verify no broken imports
- **Dependency tracking**: Check what depends on removed code
- **Rollback capability**: Can revert changes if tests fail
- **Priority ordering**: Apply safest changes first

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

## Adapts To Any Project

Works automatically with:

- Python projects (detects FastAPI, Django patterns)
- JavaScript projects (detects Express, React patterns)
- Go projects (detects Gin, Echo patterns)
- Rust projects (detects Actix, Tokio patterns)

**One command. Comprehensive analysis. Safe simplification. Personal-use focus.**
