# Workflow Command Usage Guide

**Complete guide for using `/workflow` command to orchestrate universal commands into powerful workflow chains.**

---

## Quick Start

```bash
# Most common workflow - pre-commit
/workflow:pre-commit

# Feature development
/workflow:feature-dev

# Fix errors
/workflow:error-resolution
```

---

## Available Workflows

### 1. Pre-Commit Workflow ⭐⭐⭐⭐⭐

**When to use**: Before every commit

**What it does**: Ensures code quality before committing

```bash
/workflow:pre-commit
```

**Chain**: `review → fix → test → commit`

**Step-by-step**:

1. Runs code review (linting, type checking, security)
2. If issues found → Auto-fixes them
3. Runs tests to verify fixes
4. If tests pass → Commits with conventional message
5. If any step fails → Stops and reports

**Example Output**:

```
🔄 Workflow: pre-commit
📋 Chain: review → fix → test → commit

✅ Step 1/4: Review
   Status: Success
   Issues found: 2 (auto-fixed)

✅ Step 2/4: Fix
   Status: Success
   Fixed: 2 issues

✅ Step 3/4: Test
   Status: Success
   Tests: 45/45 passed

✅ Step 4/4: Commit
   Status: Success
   Commit: feat: add user authentication

✅ Workflow complete: 4/4 steps succeeded
⏱️ Total time: 45s
```

**Best for**: Daily development, ensuring quality before commits

---

### 2. Feature Development Workflow ⭐⭐⭐⭐⭐

**When to use**: When implementing new features

**What it does**: Complete feature development lifecycle

```bash
/workflow:feature-dev
```

**Chain**: `explain → refactor → test → review → docs → commit`

**Step-by-step**:

1. Explains existing codebase (understand context)
2. Refactors code for maintainability
3. Tests to verify refactoring
4. Reviews code quality
5. Documents new features
6. Commits with proper message

**Example Output**:

```
🔄 Workflow: feature-dev
📋 Chain: explain → refactor → test → review → docs → commit

✅ Step 1/6: Explain
   Status: Success
   Understanding: Code structure analysed

✅ Step 2/6: Refactor
   Status: Success
   Files changed: 3

✅ Step 3/6: Test
   Status: Success
   Tests: 45/45 passed

✅ Step 4/6: Review
   Status: Success
   Code quality: Good

✅ Step 5/6: Docs
   Status: Success
   Documentation: Generated

✅ Step 6/6: Commit
   Status: Success
   Commit: feat: implement user dashboard

✅ Workflow complete: 6/6 steps succeeded
⏱️ Total time: 120s
```

**Best for**: New feature implementation, major refactoring

---

### 3. Error Resolution Workflow ⭐⭐⭐⭐⭐

**When to use**: When fixing bugs or errors

**What it does**: Fixes errors with quality checks

```bash
/workflow:error-resolution
```

**Chain**: `fix → test → review → commit`

**Step-by-step**:

1. Auto-detects and fixes errors
2. Tests to verify fixes work
3. Reviews to ensure code quality maintained
4. Commits fixes with proper message

**Example Output**:

```
🔄 Workflow: error-resolution
📋 Chain: fix → test → review → commit

✅ Step 1/4: Fix
   Status: Success
   Fixed: ImportError in service.py:42

✅ Step 2/4: Test
   Status: Success
   Tests: 45/45 passed

✅ Step 3/4: Review
   Status: Success
   Code quality: Maintained

✅ Step 4/4: Commit
   Status: Success
   Commit: fix: resolve import error in service

✅ Workflow complete: 4/4 steps succeeded
⏱️ Total time: 35s
```

**Best for**: Bug fixes, error resolution

---

### 4. Code Improvement Workflow ⭐⭐⭐⭐

**When to use**: When improving existing code

**What it does**: Systematically improves code quality

```bash
/workflow:code-improvement
```

**Chain**: `review → refactor → test → docs → commit`

**Step-by-step**:

1. Reviews code to identify improvements
2. Refactors based on findings
3. Tests to verify improvements
4. Documents changes
5. Commits improvements

**Example Output**:

```
🔄 Workflow: code-improvement
📋 Chain: review → refactor → test → docs → commit

✅ Step 1/5: Review
   Status: Success
   Issues found: 3 improvement opportunities

✅ Step 2/5: Refactor
   Status: Success
   Refactored: 2 functions

✅ Step 3/5: Test
   Status: Success
   Tests: 45/45 passed

✅ Step 4/5: Docs
   Status: Success
   Documentation: Updated

✅ Step 5/5: Commit
   Status: Success
   Commit: refactor: improve code structure

✅ Workflow complete: 5/5 steps succeeded
⏱️ Total time: 90s
```

**Best for**: Code quality improvements, technical debt reduction

---

### 5. Debugging Workflow ⭐⭐⭐⭐

**When to use**: When debugging issues

**What it does**: Systematic bug resolution

```bash
/workflow:debugging
```

**Chain**: `debug → fix → test → commit`

**Step-by-step**:

1. Adds debug instrumentation
2. Analyses debug output
3. Fixes identified issues
4. Tests to verify fixes
5. Commits resolution

**Example Output**:

```
🔄 Workflow: debugging
📋 Chain: debug → fix → test → commit

✅ Step 1/4: Debug
   Status: Success
   Issue identified: Null pointer exception

✅ Step 2/4: Fix
   Status: Success
   Fixed: Added null check

✅ Step 3/4: Test
   Status: Success
   Tests: 45/45 passed

✅ Step 4/4: Commit
   Status: Success
   Commit: fix: resolve null pointer exception

✅ Workflow complete: 4/4 steps succeeded
⏱️ Total time: 50s
```

**Best for**: Debugging complex issues, systematic problem solving

---

### 6. Cleanup Workflow ⭐⭐⭐

**When to use**: Periodic project cleanup

**What it does**: Comprehensive cleanup with code analysis

```bash
/workflow:cleanup
```

**Enhanced version** (with code improvements):

```bash
/workflow:cleanup --with-code-improvement
```

**Chain**: `simplify → clean → test → commit` (or `simplify → clean → code-improvement → test → commit`)

**Step-by-step**:

1. Identifies overbloat and enterprise features
2. Removes unnecessary files and improves code quality
3. Optionally applies code improvements (refactoring, complexity reduction)
4. Tests to verify cleanup
5. Commits cleanup changes

**Example Output**:

```
🔄 Workflow: cleanup
📋 Chain: simplify → clean → code-improvement → test → commit

✅ Step 1/5: Simplify
   Status: Success
   Targets found: 5 enterprise features

✅ Step 2/5: Clean
   Status: Success
   Files removed: 12
   Code quality issues fixed: 12
   Dependencies removed: 5

✅ Step 3/5: Code Improvement
   Status: Success
   Code refactored: 3 patterns
   Complexity reduced: 2 functions

✅ Step 4/5: Test
   Status: Success
   Tests: 45/45 passed

✅ Step 5/5: Commit
   Status: Success
   Commit: chore: comprehensive cleanup and code improvements

✅ Workflow complete: 5/5 steps succeeded
⏱️ Total time: 4.5 min
```

**Best for**: Periodic cleanup, code quality improvement

---

## Advanced Usage

### Error Handling Options

**Stop on Error (Default)**:

```bash
/workflow:pre-commit
# Stops if any command fails
```

**Continue on Error**:

```bash
/workflow:morning-routine --error-handling=continue
# Continues even if commands fail
```

**Rollback on Error**:

```bash
/workflow:feature-dev --error-handling=rollback
# Rolls back all changes if workflow fails
```

### Dry-Run Mode

Preview what would happen without executing:

```bash
/workflow:pre-commit --dry-run
```

**Output**:

```
🔄 Workflow: pre-commit (DRY-RUN)
📋 Chain: review → fix → test → commit

Would execute:
1. /review → Static analysis
2. /fix → Auto-fix issues (if found)
3. /test → Verify fixes
4. /commit → Commit changes

Estimated time: 30-60s
```

### Parallel Execution

Some workflows can run commands in parallel:

```bash
/workflow:pre-push --parallel=review,test
# Runs review and test simultaneously
```

**Performance**: Saves 10-34s on pre-push workflow

---

## How State Passing Works

Commands pass state between each other automatically:

**Example**: Pre-commit workflow

```
Step 1: /review
Output State:
{
  "status": "success",
  "command": "review",
  "data": {
    "issues": ["lint error", "type error"],
    "files": ["src/service.py"]
  },
  "next_command": "fix"
}

Step 2: /fix (reads previous state)
Input: Previous review state
Action: Fixes issues found in review
Output State:
{
  "status": "success",
  "command": "fix",
  "data": {
    "fixed": ["lint error", "type error"],
    "files_changed": ["src/service.py"]
  },
  "next_command": "test"
}

Step 3: /test (reads previous state)
Input: Previous fix state
Action: Tests fixed files
Output State:
{
  "status": "success",
  "command": "test",
  "data": {
    "test_results": {"passed": 45, "failed": 0},
    "files_tested": ["src/service.py"]
  },
  "next_command": "commit"
}

Step 4: /commit (reads previous state)
Input: Previous test state
Action: Commits all changes
Output State:
{
  "status": "success",
  "command": "commit",
  "data": {
    "commit_hash": "abc123",
    "message": "fix: resolve lint and type errors"
  }
}
```

---

## Conditional Execution

### If-Fails Condition

Runs next command only if previous failed:

```bash
# In pre-commit workflow
review → [FAILS] → fix (runs because review failed)
```

**Example**:

```
Step 1: /review
Status: Error (found 2 issues)
Next: /fix (condition: if-fails)

Step 2: /fix (executes because review failed)
Status: Success (fixed 2 issues)
```

### If-Success Condition

Runs next command only if previous succeeded:

```bash
# In pre-commit workflow
test → [SUCCESS] → commit (runs because test passed)
```

**Example**:

```
Step 3: /test
Status: Success (all tests passed)
Next: /commit (condition: if-success)

Step 4: /commit (executes because test succeeded)
Status: Success (committed changes)
```

---

## Common Scenarios

### Scenario 1: Daily Development

**Morning**:

```bash
/workflow:morning-routine
# Quick health check
```

**During Development**:

```bash
# Make changes
# Test frequently
/test --changed

# Fix errors
/fix

# Before commit
/workflow:pre-commit
```

**End of Day**:

```bash
/workflow:pre-push
# Final check before push
```

---

### Scenario 2: Feature Development

**Start Feature**:

```bash
/workflow:feature-dev
# Complete lifecycle: explain → refactor → test → review → docs → commit
```

**During Development**:

```bash
# Make changes
# Test incrementally
/test --changed

# Fix issues
/workflow:error-resolution
```

**Complete Feature**:

```bash
/workflow:pre-push
# Final quality check
```

---

### Scenario 3: Bug Fixing

**Identify Bug**:

```bash
/debug
# Add instrumentation, analyse
```

**Fix Bug**:

```bash
/workflow:error-resolution
# fix → test → review → commit
```

**Verify Fix**:

```bash
/test
# Ensure fix works
```

---

### Scenario 4: Code Quality Improvement

**Identify Improvements**:

```bash
/review
# Find improvement opportunities
```

**Improve Code**:

```bash
/workflow:code-improvement
# review → refactor → test → docs → commit
```

**Verify**:

```bash
/test
# Ensure improvements work
```

---

### Scenario 5: Project Cleanup

**Periodic Cleanup**:

```bash
/workflow:cleanup
# simplify → clean → test → commit
```

**After Cleanup**:

```bash
/test
# Verify cleanup didn't break anything
```

---

## Best Practices

### 1. Use Pre-Commit Before Every Commit

```bash
# Always run before committing
/workflow:pre-commit
```

**Benefits**:

- Catches issues early
- Ensures tests pass
- Maintains code quality

---

### 2. Use Feature-Dev for New Features

```bash
# When starting new features
/workflow:feature-dev
```

**Benefits**:

- Understands existing code
- Ensures quality
- Documents features
- Commits properly

---

### 3. Use Error-Resolution for Bug Fixes

```bash
# When fixing bugs
/workflow:error-resolution
```

**Benefits**:

- Fixes errors automatically
- Verifies fixes
- Maintains quality
- Commits properly

---

### 4. Use Pre-Push Before Pushing

```bash
# Before pushing to remote
/workflow:pre-push
```

**Benefits**:

- Final quality check
- Ensures tests pass
- Prevents bad commits

---

### 5. Use Morning-Routine Daily

```bash
# Start of each day
/workflow:morning-routine
```

**Benefits**:

- Quick health check
- Fixes overnight issues
- Commits changes

---

## Troubleshooting

### Workflow Fails at Test Step

**Problem**: Tests fail during workflow

**Solution**:

```bash
# Fix test failures manually
/fix

# Or run error-resolution workflow
/workflow:error-resolution
```

---

### Workflow Fails at Review Step

**Problem**: Review finds issues that can't be auto-fixed

**Solution**:

```bash
# Review issues manually
/review

# Fix issues
/fix

# Continue workflow
/workflow:pre-commit
```

---

### Workflow Takes Too Long

**Problem**: Workflow execution is slow

**Solution**:

```bash
# Use parallel execution
/workflow:pre-push --parallel=review,test

# Or use faster workflows
/workflow:morning-routine  # Faster than feature-dev
```

---

### State Not Passing Between Commands

**Problem**: Commands don't see previous state

**Solution**:

- Ensure workflow completes fully
- Check state storage: `workflow:{workflow_name}:{command_name}`
- Re-run workflow if interrupted

---

## Performance Tips

### 1. Use Changed Tests

```bash
# In workflows, use --changed flag for tests
/test --changed  # Faster than full test suite
```

### 2. Use Parallel Execution

```bash
# Run independent commands in parallel
/workflow:pre-push --parallel=review,test
```

### 3. Use Faster Workflows When Possible

```bash
# Morning routine is faster than feature-dev
/workflow:pre-commit --quick  # 20-50s
/workflow:feature-dev      # 60-180s
```

---

## Integration with Other Commands

### Standalone Commands Still Work

```bash
# You can still use commands individually
/test
/fix
/review
/commit
```

### Workflows Orchestrate Commands

```bash
# Workflows call commands in sequence
/workflow:pre-commit
# Internally calls: /review → /fix → /test → /commit
```

---

## Examples

### Example 1: Pre-Commit Success

```bash
$ /workflow:pre-commit

🔄 Workflow: pre-commit
📋 Chain: review → fix → test → commit

✅ Step 1/4: Review
   Status: Success
   Issues found: 0

✅ Step 2/4: Fix
   Status: Skipped (no issues)

✅ Step 3/4: Test
   Status: Success
   Tests: 45/45 passed

✅ Step 4/4: Commit
   Status: Success
   Commit: feat: add user authentication

✅ Workflow complete: 4/4 steps succeeded
⏱️ Total time: 35s
```

---

### Example 2: Pre-Commit with Fixes

```bash
$ /workflow:pre-commit

🔄 Workflow: pre-commit
📋 Chain: review → fix → test → commit

✅ Step 1/4: Review
   Status: Success
   Issues found: 2

✅ Step 2/4: Fix
   Status: Success
   Fixed: 2 issues (lint errors)

✅ Step 3/4: Test
   Status: Success
   Tests: 45/45 passed

✅ Step 4/4: Commit
   Status: Success
   Commit: fix: resolve lint errors

✅ Workflow complete: 4/4 steps succeeded
⏱️ Total time: 42s
```

---

### Example 3: Pre-Commit Failure

```bash
$ /workflow:pre-commit

🔄 Workflow: pre-commit
📋 Chain: review → fix → test → commit

✅ Step 1/4: Review
   Status: Success
   Issues found: 0

✅ Step 2/4: Fix
   Status: Skipped (no issues)

❌ Step 3/4: Test
   Status: Error
   Failures: 2 tests failed
   Error: AssertionError in test_auth.py:42

🛑 Workflow stopped: Test step failed
💡 Suggestion: Fix test failures and retry workflow
⏱️ Total time: 28s
```

---

### Example 4: Feature Development with Rollback

```bash
$ /workflow:feature-dev

🔄 Workflow: feature-dev
📋 Chain: explain → refactor → test → review → docs → commit

✅ Step 1/6: Explain
   Status: Success

✅ Step 2/6: Refactor
   Status: Success
   Files changed: 3

❌ Step 3/6: Test
   Status: Error
   Failures: 3 tests failed
   Error: ImportError in refactored module

🔄 Rolling back changes...
   Restored: 3 files
   Status: Complete

🛑 Workflow stopped: Test step failed (rollback completed)
💡 Suggestion: Review refactoring changes and fix import errors
⏱️ Total time: 45s
```

---

## Quick Reference

### Workflow Selection Guide

| Scenario         | Workflow           | Time    |
| ---------------- | ------------------ | ------- |
| Before commit    | `pre-commit`       | 30-60s  |
| New feature      | `feature-dev`      | 60-180s |
| Bug fix          | `error-resolution` | 40-130s |
| Code improvement | `code-improvement` | 55-175s |
| Debugging        | `debugging`        | 30-120s |
| Project cleanup  | `cleanup`          | 2-5 min |
| Before push      | `pre-push`         | 30-130s |

### Command Flags

```bash
/workflow:{name}                    # Run workflow
/workflow:{name} --dry-run          # Preview without executing
/workflow:{name} --error-handling=stop|continue|rollback
/workflow:{name} --parallel=cmd1,cmd2  # Run commands in parallel
```

---

## Getting Help

### List Available Workflows

```bash
/workflow --list
```

**Output**:

```
Available workflows:
1. pre-commit - Ensure code quality before committing
2. feature-dev - Complete feature development lifecycle
3. error-resolution - Fix errors with quality checks
4. code-improvement - Improve code quality systematically
5. debugging - Systematic bug resolution
6. cleanup - Project cleanup and simplification
7. pre-push - Final quality check before pushing
```

### Workflow Details

```bash
/workflow:pre-commit --help
```

**Output**:

```
Workflow: pre-commit
Chain: review → fix → test → commit
Error handling: stop
Estimated time: 30-60s
Conditions:
  - review.if-fails=fix
  - test.if-success=commit
```

---

## Summary

The `/workflow` command orchestrates universal commands into powerful workflow chains:

- **6 workflows** for different scenarios
- **State passing** between commands
- **Conditional execution** based on results
- **Error handling** with stop/continue/rollback
- **Parallel execution** for performance
- **Comprehensive reporting** with metrics

**Start using workflows today**:

```bash
/workflow:pre-commit  # Most common workflow
```

**Comprehensive. Intelligent. Automated.**
