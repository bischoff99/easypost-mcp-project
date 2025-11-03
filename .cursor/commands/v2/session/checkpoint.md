---
name: checkpoint
category: session
description: Save current conversation state for later resume
allowed-tools: [FileEdit]
requires-approval: false
context-aware: true
arguments:
  - name: checkpoint_name
    type: string
    required: false
    default: "auto-{timestamp}"
    description: Name for this checkpoint (e.g., 'auth-working', 'pre-refactor')
estimated-time: 1-2s
estimated-tokens: 100-200
version: 2.0
---

# /session:checkpoint

Save the current conversation state as a checkpoint that can be restored later. Essential for experimental work, major refactorings, or before risky changes.

## Usage

```bash
# Auto-named checkpoint
/session:checkpoint

# Named checkpoint
/session:checkpoint auth-implementation-complete
/session:checkpoint pre-refactor
/session:checkpoint working-state
```

## What Gets Saved

✅ **Saved in Checkpoint**:
- Conversation history (last 50 messages)
- Current file context
- Command history
- Token usage stats
- Timestamp and duration
- Current working state

❌ **Not Saved**:
- Open file contents (only references)
- Uncommitted code changes
- System state outside conversation

## Storage Location

```
.cursor/
├── checkpoints/
│   ├── auth-implementation-complete.json
│   ├── pre-refactor.json
│   └── 2025-11-03-14-30-45.json
└── checkpoint-index.json
```

## When to Use

### Before Risky Operations
```bash
# Before major refactoring
/session:checkpoint pre-refactor
/quality:refactor "Extract service layer from monolith"

# If it goes wrong, restore checkpoint
/session:resume pre-refactor
```

### At Key Milestones
```bash
# Feature complete
/session:checkpoint feature-auth-complete
/test:run --all
# ✅ Tests pass, checkpoint saved

# Continue to next feature
/gen:crud Product
```

### Before Context Switches
```bash
# Save backend work
/session:checkpoint backend-api-done

# Switch to frontend (clear context)
/session:clear

# Later, return to backend
/session:resume backend-api-done
```

### Experimental Work
```bash
# Save working state
/session:checkpoint working-baseline

# Try experimental approach
/quality:optimize --experimental
# Doesn't work well...

# Restore and try different approach
/session:resume working-baseline
/quality:optimize --conservative
```

## Checkpoint Information

List all checkpoints:
```bash
/session:checkpoints

# Output:
📁 Available Checkpoints

1. auth-implementation-complete
   Created: 2025-11-03 14:30
   Messages: 42
   Tokens: 15,234
   Duration: 38 minutes

2. pre-refactor
   Created: 2025-11-03 16:15
   Messages: 67
   Tokens: 22,456
   Duration: 1 hour 12 minutes

3. working-state
   Created: 2025-11-03 17:45
   Messages: 23
   Tokens: 8,123
   Duration: 15 minutes
```

## Restore Checkpoint

```bash
# Restore specific checkpoint
/session:resume auth-implementation-complete

# Restore most recent
/session:resume

# Restore with comparison
/session:diff working-state
```

## Industry Standard

**Source**: GitHub Copilot
- Called "session snapshots"
- Used for experimental features
- Recommended before major changes

**Source**: Claude Code best practices
- Checkpoint before risky operations
- Essential for iterative development
- Enables "try and revert" workflow

## Checkpoint Strategies

### Strategy 1: Time-Based
```bash
# Every hour during long sessions
/session:checkpoint hourly-$(date +%H)
```

### Strategy 2: Milestone-Based
```bash
# After completing features
/session:checkpoint feature-auth-done
/session:checkpoint feature-products-done
```

### Strategy 3: Experiment-Based
```bash
# Before trying new approaches
/session:checkpoint baseline
/session:checkpoint approach-a
/session:checkpoint approach-b
```

## Automatic Checkpoints

Configure in `.dev-config.json`:
```json
{
  "session": {
    "autoCheckpoint": {
      "enabled": true,
      "frequency": "every-hour",
      "maxCheckpoints": 10,
      "naming": "auto-{timestamp}"
    }
  }
}
```

## Checkpoint Diff

Compare current state with checkpoint:
```bash
/session:diff pre-refactor

# Output:
📊 Checkpoint Comparison

Checkpoint: pre-refactor (2 hours ago)
Current: Now

Changes:
+ 15 new messages
+ 3 files modified
+ 2 commands executed
+ 4,234 tokens used

Code Changes:
✓ backend/src/services/auth.py (refactored)
✓ backend/tests/test_auth.py (added tests)
! frontend/src/api/auth.js (potential issue)

Would you like to:
1. Continue current work
2. Restore checkpoint
3. Merge changes from checkpoint
```

## Storage Management

```bash
# List checkpoints
/session:checkpoints

# Delete old checkpoints
/session:checkpoint:clean --older-than 7days

# Export checkpoint
/session:checkpoint:export auth-complete backup.json
```

## Performance

- **Time**: 1-2s (saves to disk)
- **Tokens**: 100-200 (checkpoint metadata)
- **Storage**: ~50KB per checkpoint
- **Effect**: No impact on current session

## Example Workflow

```bash
# Starting authentication feature
/gen:api /auth/login POST
/gen:api /auth/register POST
# ... implementation work ...

# Feature working, checkpoint!
/session:checkpoint auth-mvp-working

# Now try adding OAuth
/gen:api /auth/oauth/google GET
/gen:api /auth/oauth/callback GET
# This breaks existing auth...

# Restore working state
/session:resume auth-mvp-working

# Try different approach
/quality:refactor "Add OAuth without breaking existing auth"
```

## Best Practices

1. **Name descriptively** - `auth-working` > `checkpoint1`
2. **Checkpoint before experiments** - Easy rollback
3. **Checkpoint at milestones** - Feature complete, tests passing
4. **Clean old checkpoints** - Keep last 10, delete older
5. **Use with version control** - Checkpoints supplement, don't replace Git

## Related Commands

- `/session:resume <name>` - Restore checkpoint
- `/session:checkpoints` - List all checkpoints
- `/session:diff <name>` - Compare with checkpoint
- `/session:checkpoint:clean` - Delete old checkpoints

## Tips

- **Before `/session:clear`** - Checkpoint if you might need to return
- **Before major refactors** - Safe experimentation
- **At feature completion** - Mark milestones
- **During learning** - Try → fail → restore → learn

