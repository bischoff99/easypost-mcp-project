---
name: fix
category: quality
description: Auto-detect and fix errors in code with verification
allowed-tools: [Read, Grep, FileEdit, Bash, read_lints, mcp_sequential-thinking_sequentialthinking]
requires-approval: true
context-aware: true
arguments:
  - name: target
    type: string
    required: false
    default: "@errors || @file"
    description: What to fix (file path, @errors, @selection)
  - name: verify
    type: boolean
    required: false
    default: true
    description: Run tests after fix
estimated-time: 10-18s
estimated-tokens: 2000-4000
m3-max-optimized: true
version: 2.0
---

# /quality:fix

Automatically detect, analyze, and fix errors in your code with multi-step reasoning and verification. Context-aware and uses Sequential Thinking MCP for deep analysis.

## Usage

```bash
# Auto-detect errors
/quality:fix

# Fix specific file
/quality:fix backend/src/service.py

# Fix linter errors
/quality:fix @errors

# Fix selection
/quality:fix @selection

# Fix without verification
/quality:fix --no-verify
```

## Auto-Detection Priority

1. **Linter errors** (@errors) - Highest priority
2. **Test failures** (@tests-failing) - High priority
3. **Open file** (@file) - If errors visible
4. **Git changes** (@git-diff) - Modified files
5. **Selection** (@selection) - If code selected

## How It Works (Agent Mode)

### Step 1: Detection (2-3s)
```
Analyzing codebase...
🔍 Found 3 issues:
  1. TypeError in auth.py:42
  2. Undefined variable in service.py:156
  3. Import error in __init__.py:8

Analyzing with Sequential Thinking...
```

### Step 2: Root Cause Analysis (3-5s)
```
Using mcp_sequential-thinking for deep analysis...

Thought 1: Error indicates missing import
Thought 2: Variable should be user_id not userId
Thought 3: auth module not initialized properly

Root causes identified. Planning fixes...
```

### Step 3: Fix Generation (2-4s)
```
Generating fixes:

Fix 1: auth.py
  - Add missing import: from typing import Optional
  - Fix variable name: user_id
  - Handle None case

Fix 2: service.py
  - Initialize variable before use
  - Add type hint

Fix 3: __init__.py
  - Import auth module correctly

Preview changes? [y/n/apply]
```

### Step 4: Verification (3-6s)
```
User: y

Applying fixes...
✅ auth.py (3 changes)
✅ service.py (2 changes)
✅ __init__.py (1 change)

Running tests with 16 workers...
✅ All 45 tests pass (4.2s)

Verifying linter...
✅ No linter errors

Fix complete! 🎉
```

## Context-Aware Fixes

### Using @errors
```bash
/quality:fix @errors

# Reads linter output automatically
# Fixes all reported issues
# Re-runs linter to verify
```

### Using @selection
```bash
# Select problematic code in editor
/quality:fix @selection

# AI analyzes just the selection
# Provides targeted fix
# Updates selection in place
```

### Using @git-diff
```bash
# After making changes that break tests
/quality:fix @git-diff

# Analyzes recent changes
# Identifies what broke
# Fixes issues in changed files only
```

## Fix Strategies

### Strategy 1: Conservative
```bash
/quality:fix --conservative

# Makes minimal changes
# Prefers safe refactors
# Adds defensive checks
```

### Strategy 2: Aggressive
```bash
/quality:fix --aggressive

# Modernizes code
# Applies best practices
# May refactor significantly
```

### Strategy 3: Performance
```bash
/quality:fix --performance

# Fixes errors AND optimizes
# Adds caching where applicable
# Improves algorithmic efficiency
```

## Error Types Handled

### Syntax Errors
- Missing colons, parentheses
- Indentation issues
- Invalid syntax

### Type Errors
- Type mismatches
- Missing type hints
- Incompatible operations

### Import Errors
- Missing imports
- Circular imports
- Wrong module paths

### Logic Errors
- Undefined variables
- Attribute errors
- Index out of range

### Runtime Errors
- Null pointer exceptions
- Division by zero
- File not found

## Sequential Thinking Integration

Uses `mcp_sequential-thinking` for complex issues:

```
Thought 1: Analyzing error context
  → Error occurs in async function

Thought 2: Checking dependencies
  → Missing await keyword

Thought 3: Impact analysis
  → Affects 3 downstream functions

Thought 4: Solution design
  → Add await + refactor callers

Thought 5: Verification plan
  → Test async flow end-to-end
```

## M3 Max Optimization

**Parallel Analysis** (16 workers):
- Multiple files analyzed simultaneously
- Tests run in parallel after fixes
- Linter checks concurrent

**Performance**: 10-18s for multi-file fixes (vs 60-90s sequential)

## Smart Defaults from .dev-config.json

```json
{
  "quality": {
    "autoFix": {
      "enabled": true,
      "verify": true,
      "testAfterFix": true
    }
  },
  "testing": {
    "framework": "pytest",
    "parallel": true,
    "workers": 16
  }
}
```

## Example Workflows

### Workflow 1: TDD Fix Loop
```bash
# Write test that fails
/test:run new_feature_test.py
# ❌ Test fails

# Auto-fix implementation
/quality:fix @tests-failing
# ✅ Test passes

# Refactor
/quality:refactor @file "Extract logic"
# ✅ Tests still pass
```

### Workflow 2: Linter Cleanup
```bash
# Check linter
npm run lint
# 15 errors found

# Fix all
/quality:fix @errors
# Fixes applied

# Verify
npm run lint
# ✅ 0 errors
```

### Workflow 3: Git Pre-Commit
```bash
# Before commit
git add .

# Fix any issues in staged files
/quality:fix @git-diff

# Run tests
/test:run @git-diff

# Commit if passing
git commit -m "feat: add feature"
```

## Comparison with Manual Fixing

| Approach | Time | Accuracy | Testing |
|----------|------|----------|---------|
| Manual | 30-60min | 85% | Manual |
| /quality:fix | 10-18s | 95% | Automatic |
| Copilot inline | 5-10min | 80% | Manual |

## Performance Metrics

### Single File
- Detection: 2s
- Analysis: 3s
- Fix generation: 2s
- Verification: 3s
- **Total**: ~10s

### Multiple Files (3-5)
- Detection: 3s (parallel)
- Analysis: 5s (sequential thinking)
- Fix generation: 4s (parallel)
- Verification: 6s (16 workers)
- **Total**: ~18s

## Best Practices

✅ **Use with context** - More context = better fixes
✅ **Review changes** - Preview before applying
✅ **Run tests** - Always verify with `--verify`
✅ **Commit often** - Small fixes > large refactors
✅ **Learn from fixes** - See what AI caught

## Related Commands

- `/context:explain @errors` - Understand errors first
- `/test:run --failing` - See what fails
- `/quality:refactor` - Fix + improve structure
- `/session:checkpoint` - Save before risky fixes

## Tips

1. **Let AI detect** - `/quality:fix` finds issues automatically
2. **Use preview** - Review changes before applying
3. **Enable verification** - Catch regressions immediately
4. **Fix incrementally** - One file at a time for complex issues
5. **Chain commands** - `/quality:fix && /test:run && /quality:optimize`

