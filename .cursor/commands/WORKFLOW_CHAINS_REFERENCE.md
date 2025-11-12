# All Workflow Chains Reference

**Complete reference for all 6 workflow chains available in `/workflow` command.**

**Consolidated from 8 workflows** (optimized for usability):

- `debugging` → Merged into `error-resolution` with `--debug` flag
- `morning-routine` → Merged into `pre-commit` with `--quick` flag

---

## Quick Reference Table

| #   | Workflow           | Chain                                                                                                  | Steps | Time                          | Error Handling | Use Case                 | Flags                     |
| --- | ------------------ | ------------------------------------------------------------------------------------------------------ | ----- | ----------------------------- | -------------- | ------------------------ | ------------------------- |
| 1   | `pre-commit`       | `review → fix → test → commit` (default)<br>`test → fix → commit` (quick)                              | 4/3   | 30-60s / 20-50s               | stop           | Before every commit      | `--quick`                 |
| 2   | `feature-dev`      | `explain → refactor → test → review → docs → commit`                                                   | 6     | 60-180s                       | rollback       | New feature development  | -                         |
| 3   | `error-resolution` | `[debug] → fix → test → review → commit`                                                               | 4-5   | 40-130s / 50-150s             | stop           | Bug fixing               | `--debug`                 |
| 4   | `code-improvement` | `review → refactor → test → docs → commit`                                                             | 5     | 55-175s                       | rollback       | Code quality improvement | -                         |
| 5   | `cleanup`          | `simplify → clean → test → commit`<br>`simplify → clean → code-improvement → test → commit` (enhanced) | 4-5   | 2-5 min<br>(3-7 min enhanced) | rollback       | Project cleanup          | `--with-code-improvement` |
| 6   | `pre-push`         | `review → test → commit`                                                                               | 3     | 30-130s                       | stop           | Before pushing           | -                         |

---

## 1. Pre-Commit Workflow ⭐⭐⭐⭐⭐

**Command**: `/workflow:pre-commit` or `/workflow:pre-commit --quick`

**Chain**: `review → fix → test → commit` (default) or `test → fix → commit` (quick mode)

**Purpose**: Ensure code quality before committing

**When to use**:

- Default: Before every commit (full quality check)
- Quick mode: Start of day, after pulling changes (quick health check)

**Estimated Time**:

- Default: 30-60s
- Quick mode: 20-50s

**Flags**:

- `--quick` - Skip review step for faster execution (quick health check)

**Error Handling**: `stop` (default)

**Conditions**:

- `review.if-fails=fix` - Run fix if review finds issues (default mode)
- `test.if-fails=fix` - Run fix if tests fail (quick mode)
- `test.if-success=commit` - Run commit if tests pass

**Execution Flow**:

```
Step 1: /review
  → Static analysis, linting, best practices
  → Detects: Linter errors, type errors, security issues
  → Output: List of issues found
  → State: {status: "success|error", issues: [...], next_command: "fix"}

Step 2: If issues found → /fix
  → Condition: review.if-fails=fix
  → Auto-fixes: Issues with known solutions
  → Output: Fixed issues count
  → State: {status: "success", fixed: [...], next_command: "test"}

Step 3: /test
  → Runs: Framework-specific tests
  → Verifies: All tests pass
  → State: {status: "success|error", test_results: {...}, next_command: "commit"}

Step 4: If tests pass → /commit
  → Condition: test.if-success=commit
  → Generates: Conventional commit message
  → Commits: All changes
  → State: {status: "success", commit_hash: "..."}

If any step fails → Stop and report
```

**Benefits**:

- Catches issues before they enter repository
- Ensures tests pass before commit
- Maintains code quality standards

---

## 2. Feature Development Workflow ⭐⭐⭐⭐⭐

**Command**: `/workflow:feature-dev`

**Chain**: `explain → refactor → test → review → docs → commit`

**Purpose**: Complete feature development lifecycle

**When to use**: When implementing new features

**Estimated Time**: 60-180s

**Error Handling**: `rollback` (ensures atomicity)

**Conditions**:

- `test.if-success=review` - Run review if tests pass
- `review.if-success=docs` - Run docs if review passes

**Execution Flow**:

```
Step 1: /explain
  → Analyzes: Code structure, dependencies, patterns
  → Output: Code understanding summary
  → State: {status: "success", understanding: {...}, next_command: "refactor"}

Step 2: /refactor
  → Refactors: Code for maintainability
  → Backs up: Files before changes
  → State: {status: "success", files_changed: [...], next_command: "test"}

Step 3: /test
  → Condition: test.if-success=review
  → Runs: All tests
  → Verifies: No regressions
  → State: {status: "success|error", test_results: {...}, next_command: "review"}

Step 4: /review
  → Condition: review.if-success=docs
  → Checks: Code quality, best practices
  → State: {status: "success|error", review_results: {...}, next_command: "docs"}

Step 5: /docs
  → Generates: Docstrings, README sections
  → Documents: New features and changes
  → State: {status: "success", docs_generated: [...], next_command: "commit"}

Step 6: /commit
  → Generates: Feature commit message
  → Commits: All changes atomically
  → State: {status: "success", commit_hash: "..."}

Error handling: rollback (if any step fails, rollback all changes)
```

**Benefits**:

- Understand existing code before changes
- Refactor for maintainability
- Ensure quality with tests and review
- Document new features
- Commit with proper message

---

## 3. Error Resolution Workflow ⭐⭐⭐⭐⭐

**Command**: `/workflow:error-resolution`

**Chain**: `fix → test → review → commit`

**Purpose**: Fix errors with quality checks

**When to use**: When fixing bugs or errors

**Estimated Time**: 40-130s

**Error Handling**: `stop` (default)

**Conditions**:

- `test.if-success=review` - Run review if tests pass
- `review.if-success=commit` - Run commit if review passes

**Execution Flow**:

```
Step 1: /fix
  → Detects: Errors from terminal/editor/linter
  → Fixes: Errors automatically
  → Verifies: Fixes with tests
  → State: {status: "success", fixed: [...], next_command: "test"}

Step 2: /test
  → Condition: test.if-success=review
  → Runs: Tests for fixed code
  → Verifies: All tests pass
  → State: {status: "success|error", test_results: {...}, next_command: "review"}

Step 3: /review
  → Condition: review.if-success=commit
  → Checks: Code quality maintained
  → State: {status: "success|error", review_results: {...}, next_command: "commit"}

Step 4: /commit
  → Generates: Fix commit message
  → Commits: Fixes with proper message
  → State: {status: "success", commit_hash: "..."}
```

**Benefits**:

- Fix errors automatically
- Verify fixes with tests
- Ensure code quality maintained
- Commit fixes properly

---

## 4. Code Improvement Workflow ⭐⭐⭐⭐

**Command**: `/workflow:code-improvement`

**Chain**: `review → refactor → test → docs → commit`

**Purpose**: Improve code quality systematically

**When to use**: When improving existing code

**Estimated Time**: 55-175s

**Error Handling**: `rollback` (ensures atomicity)

**Conditions**:

- `review.if-fails=refactor` - Run refactor if review finds issues
- `test.if-success=docs` - Run docs if tests pass

**Execution Flow**:

```
Step 1: /review
  → Finds: Improvement opportunities
  → Condition: review.if-fails=refactor (if issues found)
  → State: {status: "success|error", issues: [...], next_command: "refactor"}

Step 2: /refactor
  → Improves: Code based on review findings
  → Backs up: Files before changes
  → State: {status: "success", refactored: [...], next_command: "test"}

Step 3: /test
  → Condition: test.if-success=docs
  → Verifies: Improvements didn't break functionality
  → State: {status: "success|error", test_results: {...}, next_command: "docs"}

Step 4: /docs
  → Documents: Improvements made
  → Generates: Updated documentation
  → State: {status: "success", docs_updated: [...], next_command: "commit"}

Step 5: /commit
  → Commits: All improvements atomically
  → State: {status: "success", commit_hash: "..."}

Error handling: rollback (if any step fails, rollback all changes)
```

**Benefits**:

- Identify improvement opportunities
- Refactor safely with test verification
- Document improvements
- Commit improvements

---

## 5. Cleanup Workflow ⭐⭐⭐⭐⭐

**Command**: `/workflow:cleanup`

**Chain**: `simplify → clean → test → commit`

**Enhanced Chain** (with `--with-code-improvement`): `simplify → clean → code-improvement → test → commit`

**Purpose**: Project cleanup and simplification with comprehensive code analysis

**When to use**: Periodic project cleanup

**Estimated Time**: 2-5 minutes (3-7 minutes with code-improvement)

**Error Handling**: `rollback` (ensures atomicity)

**Conditions**:

- `simplify.if-success=clean` - Run clean if simplify finds targets
- `clean.if-success=code-improvement` - Run code-improvement if clean finds code issues (optional)
- `test.if-success=commit` - Run commit if tests pass

**Execution Flow**:

```
Step 1: /simplify
  → Scans: Codebase for enterprise patterns
  → Identifies: Overbloat, unused code, complexity
  → Condition: simplify.if-success=clean (if targets found)
  → State: {status: "success", targets: [...], next_command: "clean"}

Step 2: /clean (enhanced)
  → Removes: Files identified by simplify
  → Cleans: Temporary files, build artifacts
  → Removes: Unused imports, dead code (code quality cleanup)
  → Removes: Unused dependencies
  → Cleans: Configuration files
  → Condition: clean.if-success=code-improvement (if code issues found, optional)
  → State: {status: "success", cleaned: [...], code_issues: [...], next_command: "code-improvement|test"}

Step 3: If code issues found → /code-improvement (optional)
  → Condition: clean.if-success=code-improvement (if enabled)
  → Applies: Code refactoring, complexity reduction
  → State: {status: "success", improved: [...], next_command: "test"}

Step 4: /test
  → Condition: test.if-success=commit (if tests pass)
  → Verifies: Cleanup didn't break anything
  → State: {status: "success|error", test_results: {...}, next_command: "commit"}

Step 5: /commit
  → Commits: Cleanup changes
  → State: {status: "success", commit_hash: "..."}

Error handling: rollback (if cleanup breaks tests, rollback changes)
```

**Benefits**:

- Remove enterprise features
- Clean up unnecessary files
- Improve code quality (with code-improvement)
- Verify cleanup didn't break anything
- Commit cleanup

---

## 6. Pre-Push Workflow ⭐⭐⭐⭐

**Command**: `/workflow:pre-push`

**Chain**: `review → test → commit`

**Purpose**: Final quality check before pushing

**When to use**: Before pushing to remote

**Estimated Time**: 30-130s

**Error Handling**: `stop` (default)

**Conditions**:

- `review.if-success=test` - Run test if review passes
- `test.if-success=commit` - Run commit if tests pass

**Execution Flow**:

```
Step 1: /review
  → Condition: review.if-success=test (if review passes)
  → Checks: Final code quality
  → State: {status: "success|error", review_results: {...}, next_command: "test"}

Step 2: /test
  → Condition: test.if-success=commit (if tests pass)
  → Verifies: All tests pass
  → State: {status: "success|error", test_results: {...}, next_command: "commit"}

Step 3: /commit
  → Commits: Changes with proper message
  → State: {status: "success", commit_hash: "..."}

Error handling: stop (quality gate - must pass before push)
```

**Benefits**:

- Final code quality check
- Ensure tests pass
- Commit with proper message

---

## State Passing Format

All workflows use JSON state format:

```json
{
  "status": "success|error|partial",
  "command": "test|fix|review|...",
  "data": {
    "failures": [...],
    "issues": [...],
    "files_changed": [...],
    "test_results": {...},
    "review_results": {...}
  },
  "next_command": "fix|test|review|...",
  "timestamp": "2025-11-11T21:00:00Z"
}
```

**State Storage**: `workflow:{workflow_name}:{command_name}`

**State Access**: Commands read previous state via `ctx.get_state()`

---

## Conditional Execution

### If-Fails Condition

Runs next command only if previous failed:

```yaml
review.if-fails=fix
# If review finds issues → run fix
```

### If-Success Condition

Runs next command only if previous succeeded:

```yaml
test.if-success=commit
# If tests pass → run commit
```

---

## Error Handling Strategies

### Stop (Default)

Stops workflow on first error:

```yaml
error_handling: stop
# Workflow stops immediately on error
```

**Use cases**: Pre-commit, pre-push (quality gates)

### Continue

Continues workflow even if steps fail:

```yaml
error_handling: continue
# Gathers all information even if steps fail
```

**Use cases**: Morning routine (health check)

### Rollback

Rolls back all changes if workflow fails:

```yaml
error_handling: rollback
# Restores all files if any step fails
```

**Use cases**: Feature development, code improvement (atomicity)

---

## Usage Examples

### Basic Usage

```bash
# Run workflow by name
/workflow:pre-commit
/workflow:feature-dev
/workflow:error-resolution
```

### With Error Handling

```bash
# Stop on error (default)
/workflow:pre-commit

# Continue on error
/workflow:morning-routine --error-handling=continue

# Rollback on error
/workflow:feature-dev --error-handling=rollback
```

### Dry-Run Mode

```bash
# Preview workflow without executing
/workflow:pre-commit --dry-run
```

### Parallel Execution

```bash
# Run independent commands in parallel
/workflow:pre-push --parallel=review,test
```

---

## Workflow Selection Guide

| Scenario           | Recommended Workflow       | Why                           |
| ------------------ | -------------------------- | ----------------------------- |
| Before commit      | `pre-commit`               | Ensures quality before commit |
| Quick health check | `pre-commit --quick`       | Fast feedback (skip review)   |
| New feature        | `feature-dev`              | Complete lifecycle            |
| Bug fix            | `error-resolution`         | Fix with quality checks       |
| Debugging          | `error-resolution --debug` | With debug instrumentation    |
| Code improvement   | `code-improvement`         | Systematic improvement        |
| Project cleanup    | `cleanup`                  | Remove bloat                  |
| Before push        | `pre-push`                 | Final quality gate            |

---

## Performance Comparison

| Workflow         | Sequential Time | Parallel Time | Savings                         |
| ---------------- | --------------- | ------------- | ------------------------------- |
| pre-commit       | 30-60s          | 30-60s        | 0s (no parallel ops)            |
| feature-dev      | 60-180s         | 60-180s       | 0s (sequential required)        |
| error-resolution | 40-130s         | 40-130s       | 0s (sequential required)        |
| code-improvement | 55-175s         | 55-175s       | 0s (sequential required)        |
| cleanup          | 2-5 min         | 2-5 min       | 0s (sequential required)        |
| pre-push         | 30-130s         | 20-96s        | 10-34s (review + test parallel) |

---

## Summary

**6 workflows** covering all development scenarios (optimized from 8):

1. **Pre-commit** - Quality gate before commit (with `--quick` flag for health checks)
2. **Feature-dev** - Complete feature lifecycle
3. **Error-resolution** - Bug fixing with quality checks (with `--debug` flag for debugging)
4. **Code-improvement** - Systematic code quality improvement
5. **Cleanup** - Project cleanup and simplification
6. **Pre-push** - Final quality gate before push

**Consolidation Notes**:

- `debugging` workflow → Merged into `error-resolution` with `--debug` flag
- `morning-routine` workflow → Merged into `pre-commit` with `--quick` flag

**All workflows feature**:

- State passing between commands
- Conditional execution (if-fails, if-success)
- Error handling (stop/continue/rollback)
- Comprehensive reporting
- Performance metrics

**Start using workflows**:

```bash
/workflow:pre-commit  # Most common workflow
```
