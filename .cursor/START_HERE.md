# 🚀 Cursor IDE Setup - Start Here

**Welcome to the EasyPost MCP Project!**

This guide will get you productive with Cursor AI in 2 minutes.

---

## Quick Start (2 minutes)

### 1. Install Recommended Extensions
```
Cmd+Shift+P → "Extensions: Show Recommended Extensions" → Install All
```

### 2. Verify Setup
Open Cursor chat (Cmd+L) and type:
```
/test
```

If you see the 8 commands listed, you're ready! 🎉

### 3. Try Your First Command
```bash
/test backend/tests/
# Expected: Tests run with 16 workers in 4-6s
```

---

## The 5 Commands You'll Use Daily

### 1. `/test` - Run Tests (16 workers)
```bash
/test                    # All tests
/test backend/tests/     # Specific path
/test --coverage         # With coverage
```
**Time**: 4-6s | **Workers**: 16

### 2. `/fix` - Auto-Fix Errors
```bash
# See error in terminal
/fix                     # Automatically repairs it
```
**Time**: 10-18s | **AI-powered**

### 3. `/explain` - Understand Code
```bash
# Select code in editor
/explain                 # Get detailed explanation
/explain --focus=performance
```
**Time**: 10-15s | **With reasoning**

### 4. `/optimize` - M3 Max Optimizations
```bash
/optimize                # Optimize selected code
/optimize backend/src/services/batch.py
```
**Time**: 15-30s | **16-32 workers**

### 5. `/api [path] [method]` - Generate Endpoint
```bash
/api /users GET
/api /shipments POST
```
**Time**: 8-12s | **Full CRUD**

---

## Project-Specific Commands (3)

### 6. `/ep-test` - EasyPost Tests
```bash
/ep-test                 # All tests
/ep-test unit            # Unit only
/ep-test integration     # With live API
```

### 7. `/ep-dev` - Start Everything
```bash
/ep-dev                  # Backend + Frontend + PostgreSQL
```

### 8. `/ep-benchmark` - Performance Tests
```bash
/ep-benchmark            # M3 Max optimization tests
```

---

## Your Learning Path

### Day 1: Master the Basics
Focus on these 3 commands:
- `/test` - Run tests frequently
- `/fix` - Let AI fix errors
- `/explain` - Understand unfamiliar code

**Practice**: Run `/test`, break something, use `/fix` to repair it.

### Week 1: Add Power Tools
Expand to these 2:
- `/optimize` - Improve performance
- `/api` - Generate endpoints

**Practice**: Generate a new API endpoint with `/api`, optimize it with `/optimize`.

### Month 1: Project Commands
Use EasyPost-specific commands:
- `/ep-test` - Domain testing
- `/ep-dev` - Quick startup
- `/ep-benchmark` - Performance validation

**Practice**: Start your day with `/ep-dev`, check performance with `/ep-benchmark`.

---

## Project Structure Overview

```
easypost-mcp-project/
├── backend/               # FastAPI + PostgreSQL
│   ├── src/
│   │   ├── server.py      # HTTP API
│   │   ├── mcp/           # MCP server
│   │   ├── services/      # Business logic
│   │   └── models.py      # Database (9 tables)
│   └── tests/             # pytest (16 workers)
│
├── frontend/              # React + Vite
│   ├── src/
│   │   ├── pages/         # React pages
│   │   ├── components/    # UI components
│   │   └── services/      # API client
│   └── tests/             # vitest (20 workers)
│
└── .cursor/               # Cursor configuration
    ├── rules/             # Coding standards (14 files)
    ├── commands/          # Slash commands (8)
    ├── config/            # Templates
    └── archive/           # Archived docs
```

---

## Configuration Files

### `.cursorrules` (166 lines)
IDE instructions loaded automatically by Cursor.
- Commands reference
- Project standards
- Key patterns
- Performance expectations

### `.dev-config.json` (280 lines)
Project configuration used by all commands.
- Hardware specs (M3 Max)
- Stack details (FastAPI + React)
- Paths and conventions
- Worker configuration

### `.cursor/rules/` (14 files)
Coding standards for the project.
- 01-code-standards.mdc
- 02-file-structure.mdc
- 03-naming-conventions.mdc
- ...and 11 more

### `.cursor/commands/` (8 commands)
Slash command definitions.
- universal/ (5): test, fix, explain, optimize, api
- project-specific/ (3): ep-test, ep-dev, ep-benchmark

---

## Common Workflows

### Morning Routine (10s)
```bash
/ep-dev            # Start servers (3s)
/test              # Verify tests pass (4s)
```

### Feature Development
```bash
/api /feature POST           # Generate endpoint (10s)
# Implement business logic
/test backend/tests/         # Test it (4s)
/fix                         # Fix any issues (10s)
```

### Debugging
```bash
/test                        # Run tests (4s)
# See error
/fix                         # Auto-fix (18s)
/test                        # Verify (4s)
```

### Code Review
```bash
# Select code
/explain                     # Understand (10s)
/optimize                    # Check perf (20s)
```

### Performance Tuning
```bash
/ep-benchmark                # Baseline (60s)
/optimize backend/src/services/batch.py
/ep-benchmark                # Verify (60s)
```

---

## Pro Tips

### 1. Context is King
Commands read from:
- Selected code in editor
- Open files
- Terminal errors
- Git status
- `.dev-config.json`

**Tip**: Select code before running `/explain` or `/optimize`.

### 2. No Arguments Needed
```bash
# DON'T: /test backend/tests/unit/test_user.py
# DO: /test              # Auto-detects from context
```

### 3. Chain Commands
```bash
/test && /fix && /test
# Test → Fix → Verify
```

### 4. Use VS Code Tasks
```
Cmd+Shift+P → "Run Task" → "🚀 Dev: Full Stack"
```
Faster than typing commands!

### 5. Check Performance
All commands show timing:
```
✓ Tests passed in 4.2s (16 workers)
```

If slower than expected, check pytest.ini or .dev-config.json.

---

## Troubleshooting

### Commands Not Appearing
**Check**:
1. `.cursorrules` file exists
2. `.cursor/commands/` directory exists
3. Restart Cursor IDE

### Tests Running Slow
**Check**:
```bash
cat backend/pytest.ini | grep workers
# Should show: -n 16
```

### Wrong Stack Detected
**Fix**:
```bash
# Edit .dev-config.json
"stack": {
  "backend": {
    "framework": "fastapi"  # Ensure correct
  }
}
```

### Variables Not Resolving
**Debug**:
```bash
cat .dev-config.json | grep "workers"
# Should show: "pytest": 16
```

### Command Execution Fails
**Solutions**:
1. Check file paths in `.dev-config.json`
2. Verify tools installed (pytest, ruff, black)
3. Check environment activated (`source venv/bin/activate`)

---

## Get Help

### Documentation
- **Command Reference**: `.cursor/COMMANDS.md`
- **Project Guide**: `CLAUDE.md`
- **Database**: `POSTGRESQL_IMPLEMENTATION_REVIEW.md`
- **Quick Ref**: `.cursor/commands/README.md`

### VS Code Tasks
```
Cmd+Shift+P → "Tasks: Run Task"
```
- 🚀 Dev: Full Stack
- 🧪 Test: Backend
- 🔍 Lint: Backend/Frontend
- 🎨 Format: All

### Rules Reference
```
.cursor/rules/00-INDEX.mdc  # Index of all rules
.cursor/rules/*.mdc         # Individual standards
```

---

## What's Different About This Setup?

### 1. Hardware-Optimized
**M3 Max (16 cores)** everywhere:
- pytest: 16 workers
- Bulk operations: 16 workers
- PostgreSQL: 16 parallel workers
- Analytics: 16 chunks

**Result**: 10-15x faster than default setup.

### 2. Configuration-Driven
All commands read `.dev-config.json`:
- No hardcoded paths
- No hardcoded conventions
- Adapts to your project

**Result**: Commands work correctly without configuration.

### 3. Minimal Command Set
8 core commands (down from 22):
- Easier to remember
- Covers 95% of use cases
- Less overwhelming

**Result**: You actually use them.

### 4. Context-Aware
Commands use IDE context:
- Selected code
- Open files
- Terminal errors
- Git status

**Result**: Fewer arguments needed.

---

## Next Steps

### ✅ You're Ready!
1. Commands installed ✓
2. Documentation read ✓
3. First command tested ✓

### 📚 Deepen Your Knowledge
- Read `.cursor/COMMANDS.md` for detailed command reference
- Explore `.cursor/rules/` for coding standards
- Check `CLAUDE.md` for comprehensive project guide

### 🚀 Start Building
```bash
/ep-dev              # Start development
/test                # Verify everything works
# Start coding!
```

---

## Quick Command Cheatsheet

| Command | Purpose | Time | Usage |
|---------|---------|------|-------|
| `/test` | Run tests | 4-6s | Daily, after changes |
| `/fix` | Auto-fix errors | 10-18s | When errors occur |
| `/explain` | Understand code | 10-15s | Code review, learning |
| `/optimize` | Performance | 15-30s | Bottlenecks, bulk ops |
| `/api` | Generate endpoint | 8-12s | New features |
| `/ep-test` | EasyPost tests | 4-6s | Domain testing |
| `/ep-dev` | Start servers | 2-3s | Morning routine |
| `/ep-benchmark` | Performance | 30-60s | Optimization validation |

---

**Welcome aboard! Let's build something amazing.** 🚀

*Questions? Check `.cursor/COMMANDS.md` or `CLAUDE.md` for comprehensive guides.*
