# Command Chaining & Workflow Composition

Execute multiple commands in sequence or parallel, create reusable workflows, and automate common development tasks.

## Overview

Command chaining allows combining multiple slash commands into powerful workflows using familiar Unix-style operators:
- `&&` - Sequential execution (stop on failure)
- `||` - Fallback execution (continue on failure)
- `;` - Always execute next (ignore status)
- `&` - Parallel execution (non-blocking)
- `|` - Pipe output between commands

## Sequential Execution (`&&`)

Execute commands one after another. Stop if any command fails.

```bash
# Test, then fix, then test again
/test:run && /quality:fix && /test:run

# Execution:
✓ /test:run → Pass (4.2s)
✓ /quality:fix → Applied 3 fixes (10.5s)
✓ /test:run → All pass (4.1s)
Total: 18.8s
```

### Real-World Examples

#### Pre-Commit Workflow
```bash
/quality:fix @git-diff && /test:run @git-diff && /quality:optimize @git-diff

# Ensures:
# 1. All changes are fixed
# 2. Tests pass
# 3. Code is optimized
# Before committing
```

#### Feature Development
```bash
/gen:api /products POST && /gen:component ProductForm && /test:run

# Generates:
# 1. Backend API endpoint
# 2. Frontend form component
# 3. Runs all tests
```

#### Code Quality Pipeline
```bash
/quality:fix @errors && /test:run --coverage && /quality:secure @file

# Quality checks:
# 1. Fix linter errors
# 2. Run tests with coverage
# 3. Security audit
```

## Fallback Execution (`||`)

Execute next command only if previous fails. Useful for error recovery.

```bash
# Try to fix automatically, or explain if can't
/quality:fix || /context:explain @errors

# Execution:
✗ /quality:fix → Complex error, can't auto-fix
✓ /context:explain @errors → Explains the issue
```

### Error Recovery Patterns

```bash
# Try optimistic fix, fall back to analysis
/quality:fix @selection || /context:explain @selection

# Try cached run, fall back to full run
/test:run --cached || /test:run

# Try fast tests, fall back to slow
/test:run --fast || /test:run
```

## Always Execute (`;`)

Execute commands regardless of previous status.

```bash
# Run tests; then show stats regardless of outcome
/test:run ; /session:stats

# Execution:
✗ /test:run → 3 tests failed (4.2s)
✓ /session:stats → Shows session metrics
# Both execute even though tests failed
```

## Parallel Execution (`&`)

Run commands simultaneously (non-blocking).

```bash
# Run backend and frontend tests in parallel
/test:run backend/ & /test:run frontend/

# Execution:
[Process 1] /test:run backend/ (4.2s) ✓
[Process 2] /test:run frontend/ (3.8s) ✓
Total: 4.2s (vs 8.0s sequential)
# 47% time savings
```

### Parallel Patterns

```bash
# Generate multiple components simultaneously
/gen:component UserCard & /gen:component ProductCard & /gen:component OrderCard

# Analyze multiple files in parallel
/quality:optimize auth.py & /quality:optimize service.py & /quality:optimize utils.py

# Run multiple test suites
/test:run unit/ & /test:run integration/ & /test:run e2e/
```

## Pipe Operator (`|`)

Pass output from one command to another (advanced).

```bash
# Find errors, then fix them
/context:debug @errors | /quality:fix

# Generate code, then test it
/gen:api /users POST | /test:run

# Analyze code, then optimize based on analysis
/context:explain @file --focus=performance | /quality:optimize @file
```

## Saved Workflows

Define reusable workflow aliases in `.dev-config.json`:

```json
{
  "workflows": {
    "ship": {
      "description": "Prepare code for shipping",
      "commands": "/quality:fix && /test:run && /quality:optimize && /test:coverage"
    },
    "tdd": {
      "description": "Test-driven development cycle",
      "commands": "/gen:test @selection && /test:run --watch"
    },
    "review": {
      "description": "Pre-code-review checklist",
      "commands": "/quality:fix @git-diff && /test:run @git-diff && /quality:secure @git-diff && /context:explain @git-diff"
    },
    "debug": {
      "description": "Debug failing tests",
      "commands": "/test:run || (/context:explain @tests-failing && /quality:fix @tests-failing)"
    },
    "feature": {
      "description": "Complete feature workflow",
      "commands": "/gen:api $1 $2 && /gen:component $3 && /test:run && /quality:optimize"
    }
  }
}
```

### Using Saved Workflows

```bash
# Execute saved workflow
/workflow:ship

# Runs: /quality:fix && /test:run && /quality:optimize && /test:coverage
# Outputs:
✓ Fixing code... (10.5s)
✓ Running tests... (4.2s)
✓ Optimizing... (8.3s)
✓ Coverage report... (5.1s)
Total: 28.1s
Ready to ship! 🚀
```

### Workflow with Arguments

```bash
# Define in config:
"feature": "/gen:api $1 $2 && /gen:component $3 && /test:run"

# Use:
/workflow:feature /users POST UserForm

# Executes:
/gen:api /users POST && /gen:component UserForm && /test:run
```

## Complex Workflow Examples

### Example 1: Complete Feature Development
```bash
# Save as "new-feature" workflow
/gen:api $1 $2 && \
/gen:component $3 && \
/gen:test @file && \
/test:run && \
/quality:fix && \
/test:run --coverage && \
/quality:optimize && \
/context:explain "Summarize what was built"

# Usage:
/workflow:new-feature /products POST ProductForm

# Generates:
# ✓ API endpoint
# ✓ React component
# ✓ Tests
# ✓ Runs tests
# ✓ Fixes issues
# ✓ Re-tests with coverage
# ✓ Optimizes code
# ✓ Summarizes feature
# All in ~45 seconds
```

### Example 2: Git Pre-Commit Hook
```bash
# Save as "pre-commit" workflow
/quality:fix @git-staged && \
/test:run @git-staged && \
/quality:secure @git-staged && \
(/session:checkpoint "pre-commit-$(date +%s)" ; echo "Ready to commit") || \
(echo "Fix issues before committing" && exit 1)

# Usage (in git hook):
/workflow:pre-commit
```

### Example 3: Morning Routine
```bash
# Save as "morning" workflow
/session:clear && \
/test:run && \
/quality:fix @errors && \
/session:stats && \
echo "Good morning! Codebase is healthy ✓"

# Usage:
/workflow:morning
# Runs full health check in ~20s
```

### Example 4: Continuous Testing
```bash
# Save as "watch-and-fix" workflow
/test:watch & \
(while true; do \
  /test:run --failing && /quality:fix @tests-failing; \
  sleep 5; \
done)

# Auto-fixes failing tests in watch mode
```

## Conditional Execution

Use parentheses for grouping and conditionals:

```bash
# If tests pass, optimize; else, fix
(/test:run && /quality:optimize) || (/quality:fix && /test:run)

# Try quick fix, then deep analysis
(/quality:fix --quick && /test:run) || \
(/context:explain @errors && /quality:fix --aggressive && /test:run)
```

## Workflow Management Commands

### List Workflows
```bash
/workflow:list

Available Workflows:
├─ ship          - Prepare code for shipping
├─ tdd           - Test-driven development cycle
├─ review        - Pre-code-review checklist
├─ debug         - Debug failing tests
├─ feature       - Complete feature workflow
└─ morning       - Morning health check

Use: /workflow:<name> [args]
```

### Create Workflow
```bash
/workflow:save cleanup "/quality:fix && /test:run && /quality:optimize"

# Saves to .dev-config.json
✓ Workflow 'cleanup' saved
Use: /workflow:cleanup
```

### Update Workflow
```bash
/workflow:update ship "/quality:fix && /test:run --coverage && /quality:optimize && /session:checkpoint"

✓ Workflow 'ship' updated
```

### Delete Workflow
```bash
/workflow:delete old-workflow

✓ Workflow 'old-workflow' deleted
```

## Performance Optimization

### Parallel vs Sequential

```bash
# Sequential (slow)
/test:run backend/ && /test:run frontend/
# Total: 8.0s

# Parallel (fast)
/test:run backend/ & /test:run frontend/
# Total: 4.2s (max of both)
# 47% faster
```

### Smart Ordering

```bash
# Fast commands first (psychological)
/test:run --fast && /quality:fix && /test:run

# Heavy commands in parallel
(/gen:api $1 POST & /gen:component $2) && /test:run
```

## Error Handling

### Automatic Rollback
```bash
/session:checkpoint backup && \
/quality:refactor @file --aggressive && \
/test:run || \
(/session:resume backup && echo "Rollback complete")

# If refactor breaks tests, automatically restores
```

### Retry Logic
```bash
# Retry failed tests 3 times
/test:run || /test:run || /test:run || \
(/context:explain @tests-failing && echo "Tests still failing after 3 attempts")
```

## Monitoring & Feedback

### Progress Tracking
```bash
/workflow:ship --progress

Executing Workflow: ship
[1/4] Fixing code... ✓ (10.5s)
[2/4] Running tests... ✓ (4.2s)
[3/4] Optimizing... ⏳ (5.3s elapsed)
[4/4] Coverage report... ⏸️ (pending)

Time: 19.8s / ~28s estimated
```

### Detailed Output
```bash
/workflow:ship --verbose

[10:15:23] Starting workflow: ship
[10:15:23] Command 1/4: /quality:fix
[10:15:23]   → Analyzing codebase...
[10:15:25]   → Found 3 issues
[10:15:28]   → Applied fixes
[10:15:33] ✓ Command 1/4 complete (10.5s)
[10:15:33] Command 2/4: /test:run
...
```

## Best Practices

✅ **Test workflows before saving** - Verify they work
✅ **Use checkpoints before risky operations** - Enable rollback
✅ **Parallelize independent commands** - Save time
✅ **Add error handling** - Use `||` for fallbacks
✅ **Name workflows clearly** - Describe what they do

## Integration with .cursorrules

Add workflow shortcuts to `.cursorrules`:

```markdown
## Workflow Shortcuts

When user types:
- "ship it" → Execute /workflow:ship
- "new feature" → Execute /workflow:feature
- "morning check" → Execute /workflow:morning
- "debug this" → Execute /workflow:debug
```

## Metrics & Analytics

Track workflow usage:

```bash
/session:stats --workflows

Workflow Usage:
┌────────────┬───────┬─────────┬──────────┐
│ Workflow   │ Runs  │ Avg Time│ Success  │
├────────────┼───────┼─────────┼──────────┤
│ ship       │ 23    │ 28.1s   │ 96%      │
│ tdd        │ 45    │ 12.3s   │ 89%      │
│ review     │ 12    │ 35.4s   │ 100%     │
│ debug      │ 8     │ 18.7s   │ 75%      │
│ morning    │ 15    │ 20.2s   │ 93%      │
└────────────┴───────┴─────────┴──────────┘

Most Used: tdd (45 runs)
Most Reliable: review (100% success)
Fastest: tdd (12.3s avg)
```

## Tips

1. **Start simple** - Chain 2-3 commands, then expand
2. **Test individually first** - Ensure each command works
3. **Use saved workflows** - Don't type chains repeatedly
4. **Parallelize smartly** - Independent operations only
5. **Add checkpoints** - Before destructive operations
6. **Monitor performance** - Track workflow metrics
7. **Share with team** - Export .dev-config.json workflows

## Related Commands

- `/workflow:list` - Show available workflows
- `/workflow:save` - Create new workflow
- `/session:checkpoint` - Save state before workflow
- `/session:stats --workflows` - Workflow analytics


