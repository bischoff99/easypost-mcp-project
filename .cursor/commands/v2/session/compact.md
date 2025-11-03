---
name: compact
category: session
description: Compress conversation history while preserving key context
allowed-tools: []
requires-approval: false
context-aware: true
arguments:
  - name: focus
    type: string
    required: false
    default: "all"
    description: What to preserve (e.g., "code changes", "test results", "errors")
estimated-time: 2-3s
estimated-tokens: 500-1000
version: 2.0
---

# /session:compact

Intelligently compress conversation history to reduce token usage while preserving important context. Better than `/session:clear` when you want to keep relevant information.

## Usage

```bash
# Compact everything
/session:compact

# Preserve specific context
/session:compact "Keep only code changes and error messages"
/session:compact "Focus on authentication implementation"
/session:compact "Preserve test results and performance metrics"
```

## How It Works

1. **Analyzes** conversation history
2. **Identifies** key information based on focus
3. **Compresses** redundant or verbose content
4. **Preserves** critical context
5. **Continues** conversation with lighter context

## What Gets Compressed

✅ **Compressed**:
- Verbose explanations (keeps summaries)
- Repeated information
- Intermediate debugging steps
- Redundant code examples

✅ **Preserved**:
- Final code implementations
- Error messages and fixes
- Test results
- Key decisions and rationale
- Your focus area

## Compression Strategies

### Strategy 1: Code-Focused
```bash
/session:compact "Keep only code changes and implementation details"
```
**Result**: 60-70% token reduction, preserves all code

### Strategy 2: Error-Focused
```bash
/session:compact "Keep only errors and their fixes"
```
**Result**: 70-80% token reduction, preserves debugging trail

### Strategy 3: Test-Focused
```bash
/session:compact "Preserve test results and coverage reports"
```
**Result**: 65-75% token reduction, preserves quality metrics

### Strategy 4: Full Compression
```bash
/session:compact
```
**Result**: 50-60% token reduction, preserves overall context

## When to Use

| Situation | Command | Reason |
|-----------|---------|--------|
| Long session (30+ messages) | `/session:compact` | Reduce token bloat |
| Before complex command | `/session:compact "Keep X"` | Make room for new output |
| Switching sub-tasks | `/session:compact "Focus on Y"` | Maintain relevant context |
| Token warning | `/session:cost` → `/session:compact` | Stay within budget |

## Example Workflow

```bash
# Long authentication implementation
/gen:api /auth/login POST
/gen:api /auth/register POST
/test:run auth tests
/quality:fix auth errors
# ... 20 more messages ...

# Check token usage
/session:cost
# Output: 18,500 tokens (approaching limit)

# Compact with focus
/session:compact "Keep authentication code, tests, and final fixes"
# Output: Compressed to 7,200 tokens

# Continue work with lighter context
/gen:component LoginForm
```

## Industry Standard

**Source**: Claude Code documentation
- **Command**: `/compact [instructions]`
- **Use case**: Long-running sessions, token optimization
- **Recommendation**: Every 20-30 interactions or when >15K tokens

**Source**: GitHub Copilot
- Similar concept called "context pruning"
- Automatic in some cases, manual control recommended

## Performance

- **Time**: 2-3s (processes history)
- **Tokens**: 500-1000 (compression overhead)
- **Savings**: 50-80% of original token count
- **Effect**: Faster subsequent responses

## Smart Compression Examples

### Before Compression (12K tokens)
```
User: Implement auth
AI: [3K tokens of explanation]
User: Fix the error
AI: [2K tokens of debugging]
User: Add tests
AI: [2K tokens of test generation]
[... 5K more tokens of back-and-forth ...]
```

### After Compression (4K tokens)
```
Summary: Implemented authentication with JWT
Code: [Final implementation - 2K tokens]
Tests: [Test suite - 1.5K tokens]
Status: All tests passing ✓
```

## Advanced: Contextual Compression

Compression adapts to your focus:

```bash
# Security-focused
/session:compact "Security considerations and auth flow"
→ Keeps: Security patterns, auth implementation
→ Removes: Styling, UI details, debug steps

# Performance-focused
/session:compact "Performance optimizations and metrics"
→ Keeps: Optimization code, benchmark results
→ Removes: Explanations, intermediate attempts

# Testing-focused
/session:compact "Test results and coverage data"
→ Keeps: Test suites, coverage reports, failures
→ Removes: Implementation details, experiments
```

## Configuration

Add to `.dev-config.json`:
```json
{
  "session": {
    "autoCompact": {
      "enabled": true,
      "threshold": 15000,
      "strategy": "keep-code-and-tests"
    }
  }
}
```

## Comparison with Other Commands

| Command | Token Reduction | Keeps Context | Use When |
|---------|----------------|---------------|----------|
| `/session:clear` | 100% | ❌ No | Complete context switch |
| `/session:compact` | 50-80% | ✅ Yes | Long session, same topic |
| Continue normally | 0% | ✅ Yes | Short sessions |

## Tips

1. **Specify focus** - Generic compact is less effective than targeted
2. **Use before major operations** - Free up tokens for complex commands
3. **Check cost first** - Run `/session:cost` to see if needed
4. **Preserve checkpoints** - Use `/session:checkpoint` before compacting
5. **Don't over-compact** - Some context helps AI understand your goals

## Related Commands

- `/session:cost` - Check current token usage
- `/session:clear` - Complete reset
- `/session:checkpoint` - Save state before compacting
- `/session:resume` - Restore previous state

