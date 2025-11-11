# Universal Commands Workflow Chaining Analysis

**Date**: November 2025
**Status**: Research Complete - Implementation Recommendations Ready

---

## Executive Summary

After comprehensive research using Sequential-thinking, Context7, Desktop Commander, and industry best practices, this document provides:

1. **8 High-Value Workflow Chains** for enhanced development productivity
2. **State Passing Mechanisms** for seamless command integration
3. **Conditional Execution Patterns** for intelligent workflow automation
4. **Error Handling Strategies** for robust workflow execution
5. **Implementation Recommendations** for workflow orchestration

---

## Research Methodology

### Tools Used

1. **Sequential-thinking**: Deep analysis of command relationships and workflow patterns
2. **Context7**: Pre-commit framework best practices and workflow patterns
3. **Desktop Commander**: File system analysis of existing commands
4. **Exa Search**: Industry workflow patterns and command chaining examples (2025)

### Key Findings

- **Pre-commit patterns**: lint → format → test → commit (industry standard)
- **CI/CD patterns**: test → lint → build → deploy (automated quality gates)
- **Feature development**: explain → implement → test → review → refactor → docs → commit
- **Command chaining**: State passing between commands is critical for workflow automation
- **Error handling**: Conditional execution and rollback mechanisms are essential

---

## Current State Analysis

### Existing Command Integration

**Current Integration Points:**

- `/fix` → calls `/test` in Stage 7 (verification)
- `/refactor` → calls `/test` in Stage 5 (verification)
- Commands are independent (no state passing between separate invocations)

**Gaps Identified:**

1. No workflow orchestration command
2. No state passing mechanism between commands
3. No conditional execution (if-fails, if-success)
4. No workflow-level error handling (rollback entire chain)
5. Manual command chaining required

---

## High-Value Workflow Chains

### 1. Pre-Commit Workflow ⭐⭐⭐⭐⭐

**Purpose**: Ensure code quality before committing

**Chain**: `review → fix → test → commit`

**When to use**: Before every commit

**Benefits**:

- Catches issues before they enter repository
- Ensures tests pass before commit
- Maintains code quality standards

**Execution Flow**:

```
1. /review → Static analysis, linting, best practices
2. If issues found → /fix → Auto-fix issues
3. /test → Verify fixes didn't break anything
4. If tests pass → /commit → Commit with conventional message
5. If any step fails → Stop and report
```

**Estimated Time**: 30-60s (review: 17-34s, fix: 10-20s, test: 10-80s, commit: 6-15s)

---

### 2. Feature Development Workflow ⭐⭐⭐⭐⭐

**Purpose**: Complete feature development lifecycle

**Chain**: `explain → refactor → test → review → docs → commit`

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
2. /refactor → Improve code structure (if needed)
3. /test → Verify refactoring didn't break functionality
4. /review → Code quality check
5. /docs → Document new features
6. /commit → Commit feature with conventional message
```

**Estimated Time**: 60-180s (explain: 12-20s, refactor: 12-28s, test: 10-80s, review: 17-34s, docs: 8-20s, commit: 6-15s)

---

### 3. Error Resolution Workflow ⭐⭐⭐⭐⭐

**Purpose**: Fix errors with quality checks

**Chain**: `fix → test → review → commit`

**When to use**: When fixing bugs or errors

**Benefits**:

- Fix errors automatically
- Verify fixes with tests
- Ensure code quality maintained
- Commit fixes properly

**Execution Flow**:

```
1. /fix → Auto-detect and fix errors
2. /test → Verify fixes work
3. /review → Ensure code quality
4. /commit → Commit fixes
```

**Estimated Time**: 40-130s (fix: 10-20s, test: 10-80s, review: 17-34s, commit: 6-15s)

---

### 4. Code Improvement Workflow ⭐⭐⭐⭐

**Purpose**: Improve code quality systematically

**Chain**: `review → refactor → test → docs → commit`

**When to use**: When improving existing code

**Benefits**:

- Identify improvement opportunities
- Refactor safely with test verification
- Document improvements
- Commit improvements

**Execution Flow**:

```
1. /review → Identify code quality issues
2. /refactor → Improve code structure
3. /test → Verify improvements
4. /docs → Document changes
5. /commit → Commit improvements
```

**Estimated Time**: 55-175s (review: 17-34s, refactor: 12-28s, test: 10-80s, docs: 8-20s, commit: 6-15s)

---

### 5. Debugging Workflow ⭐⭐⭐⭐

**Purpose**: Systematic bug resolution

**Chain**: `debug → fix → test → commit`

**When to use**: When debugging issues

**Benefits**:

- Add debug instrumentation
- Fix identified issues
- Verify fixes
- Commit resolution

**Execution Flow**:

```
1. /debug → Add debug instrumentation, analyze output
2. /fix → Fix identified issues
3. /test → Verify fixes
4. /commit → Commit resolution
```

**Estimated Time**: 30-120s (debug: 10-23s, fix: 10-20s, test: 10-80s, commit: 6-15s)

---

### 6. Cleanup Workflow ⭐⭐⭐

**Purpose**: Project cleanup and simplification

**Chain**: `simplify → clean → test → commit`

**When to use**: Periodic project cleanup

**Benefits**:

- Remove enterprise features
- Clean up unnecessary files
- Verify cleanup didn't break anything
- Commit cleanup

**Execution Flow**:

```
1. /simplify → Identify overbloat and enterprise features
2. /clean → Remove unnecessary files
3. /test → Verify cleanup
4. /commit → Commit cleanup
```

**Estimated Time**: 2-5 minutes (simplify: 30-90s, clean: 30-90s analysis + 1-3min execution, test: 10-80s, commit: 6-15s)

---

### 7. Morning Routine Workflow ⭐⭐⭐

**Purpose**: Quick project health check

**Chain**: `test → fix → commit`

**When to use**: Start of day, after pulling changes

**Benefits**:

- Verify project health
- Fix any issues
- Commit overnight changes

**Execution Flow**:

```
1. /test → Check project health
2. If failures → /fix → Fix issues
3. /commit → Commit any fixes
```

**Estimated Time**: 20-100s (test: 10-80s, fix: 10-20s if needed, commit: 6-15s)

---

### 8. Pre-Push Workflow ⭐⭐⭐⭐

**Purpose**: Final quality check before pushing

**Chain**: `review → test → commit`

**When to use**: Before pushing to remote

**Benefits**:

- Final code quality check
- Ensure tests pass
- Commit with proper message

**Execution Flow**:

```
1. /review → Final code review
2. /test → Ensure tests pass
3. /commit → Commit (if not already committed)
```

**Estimated Time**: 30-130s (review: 17-34s, test: 10-80s, commit: 6-15s)

---

## State Passing Mechanism

### Design

**State Format** (JSON):

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
  "next_command": "suggested_command",
  "context": {
    "workflow": "pre-commit|feature-dev|...",
    "step": 1,
    "total_steps": 4
  },
  "timestamp": "2025-11-11T20:00:00Z"
}
```

### Implementation

**State Storage**:

- MCP state management (`ctx.set_state()`, `ctx.get_state()`)
- Workflow-scoped state (persists across command invocations)
- Command-scoped state (for individual command state)

**State Passing**:

```python
# Command outputs state
state = {
    "status": "success",
    "command": "test",
    "data": {"test_results": {...}},
    "next_command": "commit"
}
ctx.set_state("workflow:pre-commit:test", state)

# Next command reads state
previous_state = ctx.get_state("workflow:pre-commit:test")
if previous_state["status"] == "error":
    # Handle error case
    pass
```

---

## Conditional Execution

### Syntax Options

**Option 1: Workflow Command** (Recommended)

```bash
/workflow:pre-commit              # Run pre-commit workflow
/workflow:feature-dev             # Run feature development workflow
/workflow:error-resolution        # Run error resolution workflow
```

**Option 2: Chain Syntax**

```bash
/review && /fix && /test && /commit    # Sequential execution
/review || /fix || /test || /commit   # Stop on first success
```

**Option 3: Pipeline Syntax**

```bash
/review | /fix | /test | /commit      # Pipeline execution
```

### Conditional Logic

**If-Fails**:

```bash
/workflow:pre-commit --if-fails=fix   # Run fix if review fails
```

**If-Success**:

```bash
/workflow:pre-commit --if-success=commit  # Run commit if test succeeds
```

**Parallel Execution**:

```bash
/workflow:pre-commit --parallel=review,test  # Run review and test in parallel
```

---

## Error Handling Strategies

### Stop on Error (Default)

**Behavior**: Stop workflow if any command fails

**Use Case**: Pre-commit, pre-push (quality gates)

**Example**:

```
review → [FAILS] → STOP
```

### Continue on Error

**Behavior**: Continue workflow even if command fails

**Use Case**: Analysis workflows (gather all information)

**Syntax**:

```bash
/workflow:analysis --continue-on-error
```

**Example**:

```
review → [FAILS] → CONTINUE → test → [FAILS] → CONTINUE → commit
```

### Rollback on Error

**Behavior**: Rollback all changes if workflow fails

**Use Case**: Feature development (ensure atomicity)

**Syntax**:

```bash
/workflow:feature-dev --rollback-on-error
```

**Example**:

```
explain → refactor → test → [FAILS] → ROLLBACK refactor → STOP
```

### Retry Failed

**Behavior**: Retry failed commands

**Use Case**: Flaky tests, transient errors

**Syntax**:

```bash
/workflow:pre-commit --retry-failed=2
```

**Example**:

```
test → [FAILS] → RETRY → [FAILS] → RETRY → [SUCCESS] → CONTINUE
```

---

## Implementation Recommendations

### Phase 1: Workflow Command (High Priority)

**Create**: `.cursor/commands/universal/workflow.md`

**Features**:

1. Define 8 high-value workflows
2. Implement state passing
3. Support conditional execution
4. Error handling (stop/continue/rollback)

**Estimated Effort**: 400-500 lines, comprehensive MCP integration

### Phase 2: Enhance Existing Commands (Medium Priority)

**Enhancements**:

1. Add `--chain` flag to commands (read previous state)
2. Add state output to all commands
3. Add `--if-fails` and `--if-success` flags

**Estimated Effort**: Update 9 command files

### Phase 3: Workflow Documentation (Low Priority)

**Documentation**:

1. Update README.md with workflow examples
2. Create workflow guide
3. Add workflow examples to each command

**Estimated Effort**: Documentation updates

---

## Workflow Performance Analysis

### Sequential Execution

**Pre-commit**: 30-60s (review: 17-34s, fix: 10-20s, test: 10-80s, commit: 6-15s)

**Feature Development**: 60-180s (explain: 12-20s, refactor: 12-28s, test: 10-80s, review: 17-34s, docs: 8-20s, commit: 6-15s)

### Parallel Execution Opportunities

**Review + Test**: Can run in parallel (independent operations)

- Sequential: 27-114s
- Parallel: 17-80s (saves 10-34s)

**Explain + Docs**: Can run in parallel (both analysis operations)

- Sequential: 20-40s
- Parallel: 12-20s (saves 8-20s)

---

## Best Practices from Industry

### Pre-commit Framework Patterns

**Standard Sequence**:

1. Lint (code quality)
2. Format (code style)
3. Test (functionality)
4. Type-check (type safety)
5. Security-scan (vulnerabilities)
6. Commit (if all pass)

**Our Mapping**:

- Lint/Format → `/review`
- Test → `/test`
- Type-check → `/review` (type errors)
- Security-scan → `/review --focus=security`
- Commit → `/commit`

### CI/CD Pipeline Patterns

**Standard Sequence**:

1. Test (unit tests)
2. Lint (code quality)
3. Build (compilation)
4. Integration Tests
5. Deploy (if all pass)

**Our Mapping**:

- Test → `/test`
- Lint → `/review`
- Build → (not in scope)
- Integration Tests → `/test --integration`
- Deploy → (not in scope)

---

## Conclusion

### Key Recommendations

1. **Implement `/workflow` command** for orchestration
2. **Add state passing** to all commands
3. **Support conditional execution** (if-fails, if-success)
4. **Implement error handling** (stop/continue/rollback)
5. **Document workflows** comprehensively

### Expected Benefits

- **Productivity**: 30-50% reduction in manual command chaining
- **Quality**: Automated quality gates before commits
- **Consistency**: Standardized workflows across team
- **Reliability**: Error handling and rollback mechanisms

### Next Steps

1. Create workflow command implementation plan
2. Design state passing API
3. Implement workflow command
4. Update documentation
5. Test workflows with real projects

---

**Research Complete** ✅
**Ready for Implementation** ✅
