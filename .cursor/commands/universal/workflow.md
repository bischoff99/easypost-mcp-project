Orchestrate universal commands into high-value workflow chains with intelligent state passing, conditional execution, and comprehensive error handling.

**Context-aware**: No arguments needed - automatically detects workflow from context or accepts workflow name. Orchestrates existing universal commands (test, fix, review, commit, etc.) into powerful workflow chains with state passing and error handling.

## How It Works

**Complete MCP Workflow (5 Stages):**

**Stage 1 - Parse Workflow Definition**:

- Reads workflow name from arguments
- Loads workflow configuration
- Validates workflow exists
- Parses workflow chain, conditions, error handling

**Stage 2 - Plan Execution** (Sequential-thinking):

- Analyzes workflow chain
- Identifies parallel execution opportunities
- Determines execution order
- Plans error handling strategy
- Estimates execution time

**Stage 3 - Execute Commands**:

- For each command in chain:
  - Checks conditions (if-fails, if-success)
  - Executes command via MCP tools
  - Reads command output/state
  - Stores state for next command
  - Handles parallel execution if applicable

**Stage 4 - Handle Errors**:

- Checks command execution status
- Applies error handling strategy (stop/continue/rollback)
- Rollbacks file changes if needed
- Generates error report

**Stage 5 - Generate Report**:

- Summarizes workflow execution
- Reports successes and failures
- Suggests next steps
- Provides execution metrics

## Available Workflows

### 1. Pre-Commit Workflow (`pre-commit`)

**Purpose**: Ensure code quality before committing

**Chain**: `review → fix → test → commit`

**Conditions**:

- `review.if-fails=fix` - Run fix if review finds issues
- `test.if-success=commit` - Run commit if tests pass

**Error Handling**: `stop` (default)

**Estimated Time**: 30-60s

**When to use**: Before every commit

**Benefits**:

- Catches issues before they enter repository
- Ensures tests pass before commit
- Maintains code quality standards

**Execution Flow**:

```
1. /review → Static analysis, linting, best practices
   - Detects: Linter errors, type errors, security issues
   - Output: List of issues found
   - State: {status: "success|error", issues: [...], next_command: "fix"}

2. If issues found → /fix → Auto-fix issues
   - Condition: review.if-fails=fix (if review finds issues)
   - Auto-fixes: Issues with known solutions
   - Output: Fixed issues count
   - State: {status: "success", fixed: [...], next_command: "test"}

3. /test → Verify fixes didn't break anything
   - Runs: Framework-specific tests
   - Verifies: All tests pass
   - State: {status: "success|error", test_results: {...}, next_command: "commit"}

4. If tests pass → /commit → Commit with conventional message
   - Condition: test.if-success=commit (if tests pass)
   - Generates: Conventional commit message
   - Commits: All changes
   - State: {status: "success", commit_hash: "..."}

5. If any step fails → Stop and report
   - Error handling: stop (default)
   - Reports: Failed step and error details
```

---

### 2. Feature Development Workflow (`feature-dev`)

**Purpose**: Complete feature development lifecycle

**Chain**: `explain → refactor → test → review → docs → commit`

**Conditions**:

- `test.if-success=review` - Run review if tests pass
- `review.if-success=docs` - Run docs if review passes

**Error Handling**: `rollback` (ensures atomicity)

**Estimated Time**: 60-180s

**When to use**: When implementing new features

**Benefits**:

- Understand existing code before changes
- Refactor for maintainability
- Ensure quality with tests and review
- Document new features
- Commit with proper message

**Execution Flow**:

```
1. /explain → Understand existing codebase
   - Analyzes: Code structure, dependencies, patterns
   - Output: Code understanding summary
   - State: {status: "success", understanding: {...}, next_command: "refactor"}

2. /refactor → Improve code structure (if needed)
   - Refactors: Code for maintainability
   - Backs up: Files before changes
   - State: {status: "success", files_changed: [...], next_command: "test"}

3. /test → Verify refactoring didn't break functionality
   - Condition: test.if-success=review (if tests pass)
   - Runs: All tests
   - Verifies: No regressions
   - State: {status: "success|error", test_results: {...}, next_command: "review"}

4. /review → Code quality check
   - Condition: review.if-success=docs (if review passes)
   - Checks: Code quality, best practices
   - State: {status: "success|error", review_results: {...}, next_command: "docs"}

5. /docs → Document new features
   - Generates: Docstrings, README sections
   - Documents: New features and changes
   - State: {status: "success", docs_generated: [...], next_command: "commit"}

6. /commit → Commit feature with conventional message
   - Generates: Feature commit message
   - Commits: All changes atomically
   - State: {status: "success", commit_hash: "..."}

Error handling: rollback (if any step fails, rollback all changes)
```

---

### 3. Error Resolution Workflow (`error-resolution`)

**Purpose**: Fix errors with quality checks

**Chain**: `fix → test → review → commit`

**Conditions**:

- `test.if-success=review` - Run review if tests pass
- `review.if-success=commit` - Run commit if review passes

**Error Handling**: `stop` (default)

**Estimated Time**: 40-130s

**When to use**: When fixing bugs or errors

**Benefits**:

- Fix errors automatically
- Verify fixes with tests
- Ensure code quality maintained
- Commit fixes properly

**Execution Flow**:

```
1. /fix → Auto-detect and fix errors
   - Detects: Errors from terminal/editor/linter
   - Fixes: Errors automatically
   - Verifies: Fixes with tests
   - State: {status: "success", fixed: [...], next_command: "test"}

2. /test → Verify fixes work
   - Condition: test.if-success=review (if tests pass)
   - Runs: Tests for fixed code
   - Verifies: All tests pass
   - State: {status: "success|error", test_results: {...}, next_command: "review"}

3. /review → Ensure code quality
   - Condition: review.if-success=commit (if review passes)
   - Checks: Code quality maintained
   - State: {status: "success|error", review_results: {...}, next_command: "commit"}

4. /commit → Commit fixes
   - Generates: Fix commit message
   - Commits: Fixes with proper message
   - State: {status: "success", commit_hash: "..."}
```

---

### 4. Code Improvement Workflow (`code-improvement`)

**Purpose**: Improve code quality systematically

**Chain**: `review → refactor → test → docs → commit`

**Conditions**:

- `review.if-fails=refactor` - Run refactor if review finds issues
- `test.if-success=docs` - Run docs if tests pass

**Error Handling**: `rollback` (ensures atomicity)

**Estimated Time**: 55-175s

**When to use**: When improving existing code

**Benefits**:

- Identify improvement opportunities
- Refactor safely with test verification
- Document improvements
- Commit improvements

**Execution Flow**:

```
1. /review → Identify code quality issues
   - Finds: Improvement opportunities
   - Condition: review.if-fails=refactor (if issues found)
   - State: {status: "success|error", issues: [...], next_command: "refactor"}

2. /refactor → Improve code structure
   - Improves: Code based on review findings
   - Backs up: Files before changes
   - State: {status: "success", refactored: [...], next_command: "test"}

3. /test → Verify improvements
   - Condition: test.if-success=docs (if tests pass)
   - Verifies: Improvements didn't break functionality
   - State: {status: "success|error", test_results: {...}, next_command: "docs"}

4. /docs → Document changes
   - Documents: Improvements made
   - Generates: Updated documentation
   - State: {status: "success", docs_updated: [...], next_command: "commit"}

5. /commit → Commit improvements
   - Commits: All improvements atomically
   - State: {status: "success", commit_hash: "..."}

Error handling: rollback (if any step fails, rollback all changes)
```

---

### 5. Debugging Workflow (`debugging`)

**Purpose**: Systematic bug resolution

**Chain**: `debug → fix → test → commit`

**Conditions**:

- `debug.if-success=fix` - Run fix if debug identifies issue
- `test.if-success=commit` - Run commit if tests pass

**Error Handling**: `stop` (default)

**Estimated Time**: 30-120s

**When to use**: When debugging issues

**Benefits**:

- Add debug instrumentation
- Fix identified issues
- Verify fixes
- Commit resolution

**Execution Flow**:

```
1. /debug → Add debug instrumentation, analyze output
   - Adds: Debug logging, breakpoints
   - Analyzes: Debug output
   - Condition: debug.if-success=fix (if issue identified)
   - State: {status: "success", issue_identified: {...}, next_command: "fix"}

2. /fix → Fix identified issues
   - Fixes: Issues found by debug
   - Verifies: Fixes work
   - State: {status: "success", fixed: [...], next_command: "test"}

3. /test → Verify fixes
   - Condition: test.if-success=commit (if tests pass)
   - Verifies: All tests pass
   - State: {status: "success|error", test_results: {...}, next_command: "commit"}

4. /commit → Commit resolution
   - Commits: Bug fix with proper message
   - State: {status: "success", commit_hash: "..."}
```

---

### 6. Cleanup Workflow (`cleanup`)

**Purpose**: Project cleanup and simplification with comprehensive code analysis

**Chain**: `simplify → clean → test → commit`

**Enhanced Chain** (with `--with-code-improvement`): `simplify → clean → code-improvement → test → commit`

**Conditions**:

- `simplify.if-success=clean` - Run clean if simplify finds targets
- `clean.if-success=code-improvement` - Run code-improvement if clean finds code issues (optional)
- `test.if-success=commit` - Run commit if tests pass

**Error Handling**: `rollback` (ensures atomicity)

**Estimated Time**: 2-5 minutes (3-7 minutes with code-improvement)

**When to use**: Periodic project cleanup

**Benefits**:

- Remove enterprise features
- Clean up unnecessary files
- Improve code quality (with code-improvement)
- Verify cleanup didn't break anything
- Commit cleanup

**Execution Flow**:

```
1. /simplify → Identify overbloat and enterprise features
   - Scans: Codebase for enterprise patterns
   - Identifies: Overbloat, unused code, complexity
   - Condition: simplify.if-success=clean (if targets found)
   - State: {status: "success", targets: [...], next_command: "clean"}

2. /clean → Comprehensive cleanup (enhanced)
   - Removes: Files identified by simplify
   - Cleans: Temporary files, build artifacts
   - Removes: Unused imports, dead code (code quality cleanup)
   - Removes: Unused dependencies
   - Cleans: Configuration files
   - Condition: clean.if-success=code-improvement (if code issues found, optional)
   - State: {status: "success", cleaned: [...], code_issues: [...], next_command: "code-improvement|test"}

3. If code issues found → /code-improvement (optional)
   - Condition: clean.if-success=code-improvement (if enabled)
   - Applies: Code refactoring, complexity reduction
   - State: {status: "success", improved: [...], next_command: "test"}

4. /test → Verify cleanup
   - Condition: test.if-success=commit (if tests pass)
   - Verifies: Cleanup didn't break anything
   - State: {status: "success|error", test_results: {...}, next_command: "commit"}

5. /commit → Commit cleanup
   - Commits: Cleanup changes
   - State: {status: "success", commit_hash: "..."}

Error handling: rollback (if cleanup breaks tests, rollback changes)
```

---

### 7. Morning Routine Workflow (`morning-routine`)

**Purpose**: Quick project health check

**Chain**: `test → fix → commit`

**Conditions**:

- `test.if-fails=fix` - Run fix if tests fail
- `fix.if-success=commit` - Run commit if fix succeeds

**Error Handling**: `continue` (gather all information)

**Estimated Time**: 20-100s

**When to use**: Start of day, after pulling changes

**Benefits**:

- Verify project health
- Fix any issues
- Commit overnight changes

**Execution Flow**:

```
1. /test → Check project health
   - Runs: All tests
   - Condition: test.if-fails=fix (if tests fail)
   - State: {status: "success|error", test_results: {...}, next_command: "fix"}

2. If failures → /fix → Fix issues
   - Condition: fix.if-success=commit (if fix succeeds)
   - Fixes: Test failures automatically
   - State: {status: "success", fixed: [...], next_command: "commit"}

3. /commit → Commit any fixes
   - Commits: Overnight changes and fixes
   - State: {status: "success", commit_hash: "..."}

Error handling: continue (gather all information even if steps fail)
```

---

### 8. Pre-Push Workflow (`pre-push`)

**Purpose**: Final quality check before pushing

**Chain**: `review → test → commit`

**Conditions**:

- `review.if-success=test` - Run test if review passes
- `test.if-success=commit` - Run commit if tests pass

**Error Handling**: `stop` (default)

**Estimated Time**: 30-130s

**When to use**: Before pushing to remote

**Benefits**:

- Final code quality check
- Ensure tests pass
- Commit with proper message

**Execution Flow**:

```
1. /review → Final code review
   - Condition: review.if-success=test (if review passes)
   - Checks: Final code quality
   - State: {status: "success|error", review_results: {...}, next_command: "test"}

2. /test → Ensure tests pass
   - Condition: test.if-success=commit (if tests pass)
   - Verifies: All tests pass
   - State: {status: "success|error", test_results: {...}, next_command: "commit"}

3. /commit → Commit (if not already committed)
   - Commits: Changes with proper message
   - State: {status: "success", commit_hash: "..."}

Error handling: stop (quality gate - must pass before push)
```

---

## MCP Integration

### Stage 1 - Parse Workflow Definition

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Workflow name from arguments or context
Thoughts: 3-5
Analysis:
  1. What workflow was requested?
  2. Does workflow exist?
  3. What are workflow parameters?
  4. What conditions apply?
  5. What error handling strategy?

Workflow definitions (hardcoded):
  workflows = {
    "pre-commit": {
      "chain": ["review", "fix", "test", "commit"],
      "conditions": {
        "review": {"if-fails": "fix"},
        "test": {"if-success": "commit"}
      },
      "error_handling": "stop",
      "estimated_time": "30-60s"
    },
    # ... other workflows
  }

Progress: await ctx.report_progress(0, 5, "Parsing workflow definition")
State: ctx.set_state("workflow", {
  "name": workflow_name,
  "chain": workflow_chain,
  "conditions": workflow_conditions,
  "error_handling": error_handling_strategy,
  "total_steps": len(workflow_chain)
})

Logging:
  await ctx.info(f"Workflow: {workflow_name}")
  await ctx.info(f"Chain: {' → '.join(workflow_chain)}")
  await ctx.info(f"Error handling: {error_handling_strategy}")

Error handling:
  If workflow not found:
    await ctx.error(f"Workflow '{workflow_name}' not found")
    await ctx.info("Available workflows: pre-commit, feature-dev, error-resolution, code-improvement, debugging, cleanup, morning-routine, pre-push")
    return {"status": "error", "message": "Workflow not found"}
```

### Stage 2 - Plan Execution

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Workflow definition + project context
Thoughts: 10-15
Analysis:
  1. What commands are in the chain?
  2. Which commands can run in parallel?
  3. What are the dependencies between commands?
  4. What conditions need to be checked?
  5. What error handling applies?
  6. What is the execution order?
  7. How long will this take?
  8. What files will be modified?
  9. What backups are needed?
  10. What rollback strategy?

Parallel execution identification:
  - Commands that don't modify same files can run in parallel
  - Example: review + test (both read-only)
  - Example: explain + docs (both analysis)

Execution order:
  - Sequential for dependent commands
  - Parallel for independent commands
  - Conditional based on previous results

Progress: await ctx.report_progress(1, 5, "Planning execution")
State: ctx.set_state("execution_plan", {
  "order": [list of commands in execution order],
  "parallel": [list of command groups that can run in parallel],
  "conditions": [list of conditions to check],
  "backups_needed": [list of files that will be modified],
  "estimated_time": estimated_time,
  "rollback_strategy": rollback_strategy
})

Logging:
  await ctx.info(f"Execution plan: {execution_order}")
  if parallel_groups:
    await ctx.info(f"Parallel execution: {parallel_groups}")
  await ctx.info(f"Estimated time: {estimated_time}")
```

### Stage 3 - Execute Commands

```yaml
For each command in workflow chain:

  # Check conditions
  previous_state = ctx.get_state(f"workflow:{workflow_name}:{previous_command}")

  if condition == "if-fails":
    if previous_state["status"] != "error":
      await ctx.info(f"Skipping {command} (condition not met)")
      continue

  if condition == "if-success":
    if previous_state["status"] != "success":
      await ctx.info(f"Skipping {command} (condition not met)")
      if error_handling == "stop":
        break
      continue

  # Execute command via MCP tools
  # Each command execution follows its own MCP workflow

  # Example: Execute "review" command
  if command == "review":
    # Stage 1: Gather code
    Tool: mcp_desktop-commander_read_file
    Path: Current file or git diff
    Read: Code content

    # Stage 2: Static analysis (parallel)
    Tool: mcp_desktop-commander_start_process
    Commands: ["ruff check", "mypy", "bandit"]
    Parallel: True

    # Stage 3: Best practices
    Tool: mcp_Context7_get-library-docs
    Library: Detected framework
    Topic: "best practices code review"

    # Stage 4: AI review
    Tool: mcp_sequential-thinking_sequentialthinking
    Input: Code + analysis results
    Thoughts: 15-20

    # Stage 5: Generate report
    # Stage 6: Auto-fix (if enabled)

  # Example: Execute "test" command
  if command == "test":
    # Stage 0: Framework detection
    Tool: mcp_desktop-commander_read_file
    Files: ["pytest.ini", "vitest.config.js", "Cargo.toml", "go.mod"]

    # Stage 1: Test selection
    # Stage 2: Context7 enhancement
    # Stage 3: Execute tests
    Tool: mcp_desktop-commander_start_process
    Command: Framework-specific test command
    Timeout: 120000ms

    # Stage 4: Parse results
    Tool: mcp_desktop-commander_read_process_output
    PID: Test process PID

    # Stage 5: Coverage analysis (if --coverage)
    # Stage 6: Failure analysis

  # Example: Execute "fix" command
  if command == "fix":
    # Stage 1: Error detection
    Tool: mcp_desktop-commander_read_process_output
    PID: Last failed process

    # Stage 2: Root cause analysis
    Tool: mcp_sequential-thinking_sequentialthinking
    Input: Error context
    Thoughts: 10-15

    # Stage 3: Get fix patterns
    Tool: mcp_Context7_get-library-docs
    Library: Detected framework
    Topic: "error resolution patterns"

    # Stage 4: Prepare fix
    Tool: mcp_sequential-thinking_sequentialthinking
    Input: Root cause + patterns
    Thoughts: 6-8

    # Stage 5: Backup
    Tool: mcp_desktop-commander_read_file
    Path: File to fix
    Read: Complete content

    # Stage 6: Apply fix
    Tool: mcp_desktop-commander_edit_block
    Parameters: old_string, new_string

    # Stage 7: Verify + Retry

  # Example: Execute "commit" command
  if command == "commit":
    # Stage 1: Detect changes
    Tool: mcp_desktop-commander_start_process
    Command: "git status --porcelain"

    # Stage 2: Analyze changes
    Tool: mcp_sequential-thinking_sequentialthinking
    Input: Git diff
    Thoughts: 5-8

    # Stage 3: Generate message
    # Stage 4: Stage files
    Tool: mcp_desktop-commander_start_process
    Command: "git add ."

    # Stage 5: Commit
    Tool: mcp_desktop-commander_start_process
    Command: "git commit -m '{message}'"

  # Store command state
  command_state = {
    "status": "success|error",
    "command": command_name,
    "data": command_output_data,
    "next_command": suggested_next,
    "timestamp": datetime.now().isoformat()
  }

  ctx.set_state(f"workflow:{workflow_name}:{command_name}", command_state)

  # Store backup if command modifies files
  if command in ["fix", "refactor", "clean", "simplify"]:
    backups = ctx.get_state(f"workflow:{workflow_name}:backups", [])
    backups.append({
      "command": command_name,
      "files": modified_files,
      "backups": file_backups
    })
    ctx.set_state(f"workflow:{workflow_name}:backups", backups)

  Progress: await ctx.report_progress(2, 5, f"Executing {command} ({step}/{total_steps})")
  Logging:
    await ctx.info(f"Step {step}/{total_steps}: {command}")
    await ctx.debug(f"Command state: {command_state}")

Parallel execution:
  If commands can run in parallel:
    Tool: Execute commands concurrently
    Wait for all to complete
    Merge results and states
```

### Stage 4 - Handle Errors

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: Command execution results + error handling strategy
Thoughts: 5-8
Analysis:
  1. Did any command fail?
  2. What is the error handling strategy?
  3. Should we stop, continue, or rollback?
  4. What files need to be restored?
  5. What error message to report?

For each command that failed:
  error_state = ctx.get_state(f"workflow:{workflow_name}:{command_name}")

  if error_handling == "stop":
    await ctx.error(f"Workflow stopped: {command_name} failed")
    await ctx.info(f"Error: {error_state['data']['error_message']}")

    # Optionally rollback
    if rollback_enabled:
      await rollback_changes(workflow_name)

    return {
      "status": "error",
      "failed_at": command_name,
      "error": error_state["data"]["error_message"],
      "suggestion": "Fix errors and retry workflow"
    }

  if error_handling == "continue":
    await ctx.warning(f"Command {command_name} failed, continuing...")
    await ctx.error(f"Error: {error_state['data']['error_message']}")
    # Continue to next command

  if error_handling == "rollback":
    await ctx.error(f"Workflow failed: {command_name}")
    await ctx.info("Rolling back all changes...")

    # Restore all backups
    backups = ctx.get_state(f"workflow:{workflow_name}:backups", [])
    for backup in backups:
      for file_backup in backup["backups"]:
        Tool: mcp_desktop-commander_edit_block
        file_path: file_backup["path"]
        old_string: current_content
        new_string: file_backup["content"]

    await ctx.info("Rollback complete")
    return {
      "status": "error",
      "failed_at": command_name,
      "error": error_state["data"]["error_message"],
      "rollback": "completed"
    }

Progress: await ctx.report_progress(3, 5, "Handling errors")
Logging:
  await ctx.info(f"Error handling: {error_handling_strategy}")
```

### Stage 5 - Generate Report

```yaml
Tool: mcp_sequential-thinking_sequentialthinking
Input: All command states + execution metrics
Thoughts: 5-8
Generate: Comprehensive workflow report

Collect all command states:
  states = []
  for command in workflow_chain:
    state = ctx.get_state(f"workflow:{workflow_name}:{command}")
    states.append(state)

Calculate metrics:
  total_time = sum(state["execution_time"] for state in states)
  success_count = sum(1 for state in states if state["status"] == "success")
  error_count = sum(1 for state in states if state["status"] == "error")
  total_steps = len(states)

Generate report:
  report = {
    "workflow": workflow_name,
    "chain": workflow_chain,
    "status": "success" if error_count == 0 else "error",
    "steps": {
      "total": total_steps,
      "succeeded": success_count,
      "failed": error_count
    },
    "execution_time": total_time,
    "command_details": [
      {
        "command": state["command"],
        "status": state["status"],
        "time": state["execution_time"],
        "summary": state["data"]["summary"]
      }
      for state in states
    ],
    "suggestions": generate_suggestions(states)
  }

Progress: await ctx.report_progress(4, 5, "Generating report")
State: ctx.set_state(f"workflow:{workflow_name}:report", report)

Logging:
  await ctx.info(f"Workflow complete: {success_count}/{total_steps} steps succeeded")
  await ctx.info(f"Total time: {total_time}s")
  if error_count > 0:
    await ctx.error(f"Failed steps: {error_count}")
```

## State Passing Mechanism

### State Format

```json
{
  "status": "success|error|partial",
  "command": "test|fix|review|...",
  "data": {
    "test_results": {...},
    "issues": [...],
    "files_changed": [...],
    "summary": "..."
  },
  "next_command": "suggested_command",
  "context": {
    "workflow": "pre-commit",
    "step": 1,
    "total_steps": 4
  },
  "execution_time": 12.5,
  "timestamp": "2025-11-11T20:00:00Z"
}
```

### State Storage

**Workflow-scoped**: `workflow:{workflow_name}:{command_name}`

- Persists across command invocations
- Accessible by subsequent commands
- Example: `workflow:pre-commit:review`

**Command-scoped**: `command:{command_name}`

- Temporary state for individual commands
- Cleared after command completes
- Example: `command:test:framework`

**Backup storage**: `workflow:{workflow_name}:backups`

- Stores file backups for rollback
- Format: `[{command, files, backups}]`
- Example: `workflow:pre-commit:backups`

### State Retrieval

```python
# Get previous command state
previous_state = ctx.get_state(f"workflow:{workflow_name}:{previous_command}")

# Check status
if previous_state["status"] == "success":
    # Proceed with next command
    pass
elif previous_state["status"] == "error":
    # Handle error based on error handling strategy
    pass

# Use data from previous command
test_results = previous_state["data"]["test_results"]
```

## Conditional Execution

### If-Fails Condition

**Syntax**: `command.if-fails=next_command`

**Logic**:

- Check previous command status == "error"
- If matches, execute next command
- Else skip or stop based on error handling

**Example**:

```yaml
Chain: review → fix → test → commit
Conditions: review.if-fails=fix # Run fix if review finds issues
```

**Implementation**:

```python
if condition == "if-fails":
    previous_state = ctx.get_state(f"workflow:{workflow_name}:{previous_command}")
    if previous_state["status"] == "error":
        # Execute next command
        execute_command(next_command)
    else:
        # Skip next command
        skip_command(next_command)
```

### If-Success Condition

**Syntax**: `command.if-success=next_command`

**Logic**:

- Check previous command status == "success"
- If matches, execute next command
- Else skip or stop based on error handling

**Example**:

```yaml
Chain: test → review → commit
Conditions:
  test.if-success=review  # Run review if tests pass
  review.if-success=commit  # Run commit if review passes
```

**Implementation**:

```python
if condition == "if-success":
    previous_state = ctx.get_state(f"workflow:{workflow_name}:{previous_command}")
    if previous_state["status"] == "success":
        # Execute next command
        execute_command(next_command)
    else:
        # Skip or stop
        if error_handling == "stop":
            stop_workflow()
        else:
            skip_command(next_command)
```

## Error Handling Strategies

### Stop on Error (Default)

**Behavior**: Stop workflow if any command fails

**Use Case**: Pre-commit, pre-push (quality gates)

**Implementation**:

```python
if command_state["status"] == "error":
    await ctx.error(f"Workflow stopped: {command_name} failed")
    return {"status": "error", "failed_at": command_name}
```

**Example**:

```
review → [SUCCESS] → fix → [SUCCESS] → test → [FAILS] → STOP
```

### Continue on Error

**Behavior**: Continue workflow even if command fails

**Use Case**: Morning routine, analysis workflows

**Implementation**:

```python
if command_state["status"] == "error":
    await ctx.warning(f"Command {command_name} failed, continuing...")
    # Continue to next command
    continue
```

**Example**:

```
test → [FAILS] → CONTINUE → fix → [SUCCESS] → commit → [SUCCESS]
```

### Rollback on Error

**Behavior**: Rollback all changes if workflow fails

**Use Case**: Feature development, code improvement (atomicity)

**Implementation**:

```python
if command_state["status"] == "error":
    await ctx.error("Workflow failed, rolling back...")
    backups = ctx.get_state(f"workflow:{workflow_name}:backups", [])
    for backup in backups:
        restore_files(backup["backups"])
    return {"status": "error", "rollback": "completed"}
```

**Example**:

```
explain → [SUCCESS] → refactor → [SUCCESS] → test → [FAILS] → ROLLBACK → STOP
```

## Usage Examples

```bash
# Pre-commit workflow
/workflow:pre-commit

# Feature development workflow
/workflow:feature-dev

# Error resolution workflow
/workflow:error-resolution

# Code improvement workflow
/workflow:code-improvement

# Debugging workflow
/workflow:debugging

# Cleanup workflow
/workflow:cleanup

# Morning routine workflow
/workflow:morning-routine

# Pre-push workflow
/workflow:pre-push

# With error handling override
/workflow:pre-commit --error-handling=continue

# With dry-run mode
/workflow:pre-commit --dry-run

# List available workflows
/workflow --list
```

## Output Format

### Success Output

```
🔄 Workflow: pre-commit
📋 Chain: review → fix → test → commit
⚙️ Error handling: stop

✅ Step 1/4: Review
   Status: Success
   Issues found: 2 (auto-fixed)
   Time: 18s

✅ Step 2/4: Fix
   Status: Success
   Fixed: 2 issues
   Time: 12s

✅ Step 3/4: Test
   Status: Success
   Tests: 45/45 passed
   Time: 25s

✅ Step 4/4: Commit
   Status: Success
   Commit: feat: add user authentication
   Time: 8s

✅ Workflow complete: 4/4 steps succeeded
⏱️ Total time: 63s
```

### Failure Output

```
🔄 Workflow: pre-commit
📋 Chain: review → fix → test → commit
⚙️ Error handling: stop

✅ Step 1/4: Review
   Status: Success
   Issues found: 2
   Time: 18s

✅ Step 2/4: Fix
   Status: Success
   Fixed: 2 issues
   Time: 12s

❌ Step 3/4: Test
   Status: Error
   Failures: 2 tests failed
   Error: AssertionError in test_auth.py:42
   Time: 15s

🛑 Workflow stopped: Test step failed
💡 Suggestion: Fix test failures and retry workflow
⏱️ Total time: 45s
```

### Rollback Output

```
🔄 Workflow: feature-dev
📋 Chain: explain → refactor → test → review → docs → commit
⚙️ Error handling: rollback

✅ Step 1/6: Explain
   Status: Success
   Time: 15s

✅ Step 2/6: Refactor
   Status: Success
   Files modified: 3
   Time: 20s

❌ Step 3/6: Test
   Status: Error
   Failures: 3 tests failed
   Error: ImportError in refactored module
   Time: 12s

🔄 Rolling back changes...
   Restored: 3 files
   Status: Complete

🛑 Workflow stopped: Test step failed (rollback completed)
💡 Suggestion: Review refactoring changes and fix import errors
⏱️ Total time: 47s
```

## Performance

- Workflow parsing: <1s (Sequential-thinking)
- Execution planning: 2-3s (Sequential-thinking with 10-15 thoughts)
- Command execution: Varies by command (10-80s per command)
- Error handling: <1s (Sequential-thinking with 5-8 thoughts)
- Report generation: 1-2s (Sequential-thinking with 5-8 thoughts)
- **Total**: Sum of individual command times + 5-10s overhead

**Workflow Times**:

- Pre-commit: 30-60s
- Feature-dev: 60-180s
- Error-resolution: 40-130s
- Code-improvement: 55-175s
- Debugging: 30-120s
- Cleanup: 2-5 minutes
- Morning-routine: 20-100s
- Pre-push: 30-130s

## Desktop Commander Tools Used

**Primary Tools:**

- `mcp_desktop-commander_start_process` - Execute commands (git, test, lint)
- `mcp_desktop-commander_read_file` - Read files, read state
- `mcp_desktop-commander_read_process_output` - Read command output
- `mcp_desktop-commander_edit_block` - Rollback file changes
- `mcp_desktop-commander_list_sessions` - Check running processes
- `mcp_desktop-commander_start_search` - Find files, search content

**Supporting Tools:**

- `mcp_sequential-thinking_sequentialthinking` - Workflow planning, decision making, error analysis, report generation
- `mcp_Context7_resolve-library-id` - Framework detection
- `mcp_Context7_get-library-docs` - Workflow best practices

## Safety Features

- **State persistence**: All command states stored for debugging
- **Backup mechanism**: File backups before modifications
- **Rollback capability**: Restore all changes on error
- **Conditional execution**: Smart command chaining based on results
- **Error handling**: Multiple strategies (stop/continue/rollback)
- **Progress reporting**: Real-time workflow progress
- **Comprehensive logging**: Detailed execution logs

## Error Handling Patterns

**Workflow Not Found**:

- Report error with available workflows
- Suggest similar workflow names

**Command Execution Failure**:

- Apply error handling strategy
- Report failure with context
- Optionally rollback changes

**State Retrieval Failure**:

- Use default state if previous command state unavailable
- Log warning and continue

**Rollback Failure**:

- Report rollback failure
- Suggest manual restoration
- Provide backup locations

## Adapts To Any Project

Works automatically with:

- Python projects (pytest, ruff, mypy)
- JavaScript projects (vitest, eslint, tsc)
- Go projects (go test, golangci-lint)
- Rust projects (cargo test, cargo clippy)

**One command. Eight workflows. Complete automation.**

---

## Workflow Integration Examples

### Pre-Commit Integration

```bash
# Before every commit
/workflow:pre-commit

# Ensures:
# 1. Code passes review
# 2. Issues are fixed
# 3. Tests pass
# 4. Changes are committed
```

### Feature Development Integration

```bash
# When implementing features
/workflow:feature-dev

# Ensures:
# 1. Code is understood
# 2. Code is refactored
# 3. Tests pass
# 4. Code is reviewed
# 5. Code is documented
# 6. Changes are committed
```

### Error Resolution Integration

```bash
# When fixing errors
/workflow:error-resolution

# Ensures:
# 1. Errors are fixed
# 2. Fixes are tested
# 3. Code quality maintained
# 4. Fixes are committed
```

**Comprehensive workflow automation with intelligent state passing and error handling.**
