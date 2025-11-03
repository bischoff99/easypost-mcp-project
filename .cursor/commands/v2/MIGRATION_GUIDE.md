# Migration Guide: v1 → v2

Step-by-step guide to migrate from flat command structure (v1) to categorized, enhanced system (v2).

## Overview

**Migration Time**: 10-15 minutes  
**Difficulty**: Easy  
**Backward Compatibility**: Yes (v1 commands still work)  
**Recommended Approach**: Gradual migration

## What's Changing

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| **Structure** | Flat (`/api`, `/test`) | Categorized (`/gen:api`, `/test:run`) |
| **Context** | Manual paths | @variables + auto-detect |
| **Execution** | Single-shot | Multi-step agent mode |
| **Tracking** | None | Comprehensive metrics |
| **Chaining** | No | Yes (&&, \|\|, ;, &) |
| **MCP** | Basic | Auto-discovery + routing |

## Migration Steps

### Step 1: Backup Current Configuration (1 min)

```bash
# Backup your current setup
cp .dev-config.json .dev-config.v1.backup.json
cp -r .cursor/commands .cursor/commands.v1.backup/

# Create checkpoint
/session:checkpoint "pre-v2-migration"
```

### Step 2: Update .dev-config.json (3 min)

Add new v2 configuration sections:

```json
{
  // Existing configuration (keep)
  "hardware": {
    "cpuCores": 16,
    "workers": {
      "pytest": 16,
      "vitest": 20
    }
  },
  
  // ADD: Smart defaults
  "smartDefaults": {
    "enabled": true,
    "autoDetectContext": true,
    "autoDetectFramework": true,
    "autoDetectWorkers": true,
    "promptOnAmbiguity": true
  },
  
  // ADD: Session tracking
  "session": {
    "tracking": {
      "enabled": true,
      "warnAt": 50000,
      "stopAt": 100000
    },
    "costAlerts": {
      "enabled": true,
      "warnAt": 1.00,
      "stopAt": 5.00
    }
  },
  
  // ADD: Context variables
  "context": {
    "autoDetect": {
      "enabled": true,
      "priority": ["@selection", "@errors", "@file", "@git-diff"]
    },
    "variables": {
      "@file": {"enabled": true, "maxSize": "100KB"},
      "@open-files": {"enabled": true, "maxFiles": 10},
      "@git-diff": {"enabled": true, "includeUntracked": false}
    }
  },
  
  // ADD: Workflows
  "workflows": {
    "ship": "/quality:fix && /test:run && /quality:optimize",
    "tdd": "/gen:test @selection && /test:watch",
    "review": "/quality:fix @git-diff && /test:run @git-diff && /quality:secure @git-diff"
  },
  
  // ADD: MCP configuration
  "mcp": {
    "servers": {
      "context7": {"enabled": true, "priority": "high"},
      "desktopCommander": {"enabled": true, "priority": "critical"},
      "sequentialThinking": {"enabled": true, "priority": "medium"}
    },
    "autoDiscovery": {
      "enabled": true,
      "scanInterval": 300,
      "generateCommands": true
    }
  }
}
```

### Step 3: Test Backward Compatibility (2 min)

```bash
# Test old commands still work
/api /users POST
# ✓ Should work

/test backend/tests/
# ✓ Should work

/fix
# ✓ Should work
```

### Step 4: Try New Namespaced Commands (3 min)

```bash
# Try categorized versions
/gen:api /users POST
# Same as /api but with enhanced features

/test:run backend/tests/
# Same as /test but with context awareness

/quality:fix
# Same as /fix but with agent mode
```

### Step 5: Test Context Variables (2 min)

```bash
# Select some code in editor
/context:explain @selection
# ✓ Should explain selection

# Make some changes
/test:run @git-diff
# ✓ Should test only changed files

# Check linter errors
/quality:fix @errors
# ✓ Should fix visible errors
```

### Step 6: Test Command Chaining (2 min)

```bash
# Simple chain
/test:run && /quality:fix

# ✓ Should run tests, then fix if pass
# ✗ Should stop if tests fail

# Fallback chain
/test:run || /quality:fix @tests-failing

# ✗ If tests fail
# ✓ Then fix failing tests
```

### Step 7: Create First Workflow (2 min)

```bash
# Add to .dev-config.json workflows:
{
  "workflows": {
    "my-workflow": "/quality:fix && /test:run && /session:stats"
  }
}

# Test it
/workflow:my-workflow
# ✓ Should execute all commands
```

### Step 8: Verify Everything Works (1 min)

```bash
# Run verification
/mcp:status
# ✓ Should show connected servers

/session:stats
# ✓ Should show session metrics

/workflow:list
# ✓ Should show available workflows
```

## Command Mapping

### Direct Equivalents

| v1 Command | v2 Command | Notes |
|------------|------------|-------|
| `/api` | `/gen:api` | Enhanced with Context7 |
| `/component` | `/gen:component` | Enhanced with Context7 |
| `/test` | `/test:run` | Now with parallel optimization |
| `/fix` | `/quality:fix` | Now with agent mode |
| `/optimize` | `/quality:optimize` | Enhanced with metrics |
| `/explain` | `/context:explain` | Now with deep analysis |

### New Commands (no v1 equivalent)

| Command | Purpose |
|---------|---------|
| `/session:clear` | Reset conversation |
| `/session:cost` | View token usage |
| `/session:checkpoint` | Save state |
| `/session:stats` | Analytics |
| `/session:compact` | Compress history |
| `/test:watch` | Watch mode |
| `/test:coverage` | Coverage report |
| `/quality:refactor` | Smart refactoring |
| `/quality:secure` | Security audit |
| `/context:improve` | Suggest improvements |
| `/workflow:*` | Workflow management |
| `/mcp:*` | MCP server management |

## Common Migration Patterns

### Pattern 1: Update Test Workflow

**Before (v1)**:
```bash
/test backend/tests/
/test frontend/src/
```

**After (v2)**:
```bash
# Sequential
/test:run backend/ && /test:run frontend/

# Or parallel (faster)
/test:run backend/ & /test:run frontend/

# Or smart (test only changes)
/test:run @git-diff
```

### Pattern 2: Fix & Verify Loop

**Before (v1)**:
```bash
/fix
# Wait for completion
/test
# Wait for completion
```

**After (v2)**:
```bash
# Chained (automatic)
/quality:fix && /test:run

# Or with agent mode (interactive)
/quality:fix
# AI asks: Run tests to verify? [y/n]
```

### Pattern 3: Code Generation

**Before (v1)**:
```bash
/api /users POST
# Copy file path
/test backend/src/routes/users.py
```

**After (v2)**:
```bash
# All-in-one
/gen:api /users POST && /test:run @file

# Or with context
/gen:api /users POST
# AI auto-detects and suggests:
# "Run /test:run @file to verify?"
```

### Pattern 4: Daily Workflow

**Before (v1)**:
```bash
# Manual sequence
/test
/fix
/optimize
```

**After (v2)**:
```bash
# Save as workflow
/workflow:save morning "/test:run && /quality:fix && /quality:optimize && /session:stats"

# Use daily
/workflow:morning
```

## Gradual Migration Strategy

### Week 1: Learn & Explore
- ✅ Keep using v1 commands
- ✅ Try v2 equivalents occasionally
- ✅ Test context variables
- ✅ Check /session:stats after work

### Week 2: Adopt New Features
- ✅ Start using namespaced commands
- ✅ Add context variables to workflow
- ✅ Create first workflow
- ✅ Use /session:cost regularly

### Week 3: Full v2 Adoption
- ✅ Use v2 commands primarily
- ✅ Command chaining for common tasks
- ✅ Multiple workflows saved
- ✅ Leverage agent mode

### Week 4: Optimize & Refine
- ✅ Review /session:stats for insights
- ✅ Optimize workflows based on data
- ✅ Share workflows with team
- ✅ Full v2 proficiency

## Troubleshooting

### Issue: Old command doesn't work

**Solution**:
```bash
# Use v2 equivalent
/api → /gen:api
/test → /test:run
/fix → /quality:fix
```

### Issue: Context variable not resolving

**Solution**:
```bash
# Check configuration
cat .dev-config.json | grep context

# Enable if disabled
# In .dev-config.json:
"context": {
  "autoDetect": {"enabled": true}
}
```

### Issue: Command chaining not working

**Solution**:
```bash
# Ensure proper syntax
/test:run && /quality:fix  # ✓ Correct
/test:run & /quality:fix   # ✗ Wrong (use && not &)

# Check for errors in first command
/test:run --verbose && /quality:fix
```

### Issue: Workflow not saving

**Solution**:
```bash
# Check .dev-config.json syntax
python -c "import json; json.load(open('.dev-config.json'))"

# Ensure workflows section exists
{
  "workflows": {
    "name": "command"
  }
}
```

### Issue: MCP servers not connecting

**Solution**:
```bash
# Check status
/mcp:status

# Restart MCP servers
# (Method depends on your MCP setup)

# Disable if needed
# In .dev-config.json:
"mcp": {
  "servers": {
    "context7": {"enabled": false}
  }
}
```

## Rollback Procedure

If you need to revert to v1:

```bash
# 1. Restore backup
cp .dev-config.v1.backup.json .dev-config.json
rm -rf .cursor/commands
cp -r .cursor/commands.v1.backup/ .cursor/commands/

# 2. Resume checkpoint
/session:resume "pre-v2-migration"

# 3. Verify
/test
# Should work as before
```

## Feature Adoption Checklist

Track your v2 adoption:

- [ ] Updated .dev-config.json
- [ ] Tested backward compatibility
- [ ] Used namespaced commands
- [ ] Tried context variables
- [ ] Executed command chain
- [ ] Created first workflow
- [ ] Checked /session:stats
- [ ] Used /session:cost
- [ ] Tried agent mode
- [ ] Leveraged MCP tools
- [ ] Optimized based on metrics
- [ ] Shared workflows with team

## Benefits Tracking

Monitor improvements:

```bash
/session:stats --compare

# Before v2 (typical session):
# - 52 commands
# - 68,400 tokens ($1.03)
# - Manual workflows
# - ~3-4 hours work

# After v2 (same work):
# - 38 commands (27% fewer)
# - 45,200 tokens ($0.68, 34% cheaper)
# - Automated workflows
# - ~2-2.5 hours work (33% faster)
```

## Support

If you encounter issues:

1. **Check documentation**
   - `COMPLETE_GUIDE.md` - Comprehensive reference
   - Individual command `.md` files
   - `SMART_DEFAULTS.md` for auto-detection
   - `COMMAND_CHAINING.md` for workflows

2. **Use help commands**
   ```bash
   /help [category]
   /mcp:docs [server]
   /workflow:list
   ```

3. **Review metrics**
   ```bash
   /session:stats --verbose
   /mcp:status
   ```

4. **Test in isolation**
   ```bash
   /session:clear
   # Test one command at a time
   ```

## Next Steps

After migration:

1. **Optimize workflows** - Review /session:stats for insights
2. **Create team workflows** - Share .dev-config.json
3. **Leverage context variables** - Save 60% tokens
4. **Use agent mode** - Interactive development
5. **Monitor metrics** - Track improvements
6. **Explore MCP** - Discover new capabilities

---

**Migration complete! Welcome to v2.0** 🎉


