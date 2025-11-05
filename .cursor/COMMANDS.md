# Slash Commands Reference

**Status**: 8 core commands (22 archived)
**Auto-loaded**: Yes, Cursor watches `.cursor/commands/`
**Configuration**: `.dev-config.json`

---

## The 8 Core Commands

### Universal Commands (5)

#### 1. `/test [path]` - Smart Parallel Testing
**Most used - 16 workers on M3 Max**

```bash
/test                    # Test everything (auto-detect)
/test backend/tests/     # Specific path
/test --coverage         # With coverage
```

**Performance**: 4-6s for full suite
**Auto-detects**: pytest, vitest, jest, go test
**Workers**: 16 (from `{{hardware.workers.pytest}}`)

**What it does**:
1. Detects test framework from files
2. Runs tests in parallel (16 workers)
3. Shows coverage if requested
4. Reports results with timing

---

#### 2. `/fix` - Auto-Repair Errors
**AI-powered error fixing**

```bash
/fix                     # Auto-detect visible error
```

**Performance**: 10-18s for complete fix cycle

**How it works**:
1. Reads errors from terminal/editor
2. Analyzes with AI reasoning
3. Applies fix with proper patterns
4. Verifies fix with tests
5. Reports changes made

---

#### 3. `/explain [focus]` - AI Code Understanding
**Deep analysis with reasoning**

```bash
/explain                 # Explain selected code
/explain --focus=performance
/explain --focus=security
```

**Performance**: 10-15s

**Provides**:
- Step-by-step logic explanation
- Architecture context
- Best practices alignment
- Optimization suggestions
- Security considerations

---

#### 4. `/optimize [file]` - M3 Max Optimizations
**Hardware-specific performance improvements**

```bash
/optimize                # Optimize selected code
/optimize backend/src/services/batch.py
```

**Applies**:
- Parallel processing patterns (16 workers)
- Async/await optimizations
- Connection pooling
- Batch processing
- Memory optimization

**Uses**:
- `{{hardware.workers.python}}` → 32
- `{{hardware.optimization.batchSizeOptimal}}` → 150

---

#### 5. `/api [path] [method]` - Generate API Endpoint
**FastAPI endpoint generation**

```bash
/api /users GET
/api /shipments POST
```

**Generates**:
1. Pydantic request/response models
2. FastAPI route handler with validation
3. Error handling with logging
4. Request ID middleware integration
5. pytest tests with mocks
6. OpenAPI documentation

**Uses conventions from**:
- `{{stack.backend.framework}}` → fastapi
- `{{conventions.python.functions}}` → snake_case
- `{{testing.backend.framework}}` → pytest

---

### Project-Specific Commands (3)

#### 6. `/ep-test [type]` - EasyPost Tests
**Run project tests with EasyPost patterns**

```bash
/ep-test                 # All tests (16 workers)
/ep-test unit            # Unit tests only
/ep-test integration     # Integration tests (live API)
```

**Performance**: 4-6s (unit), 8-12s (integration)

**Runs**:
```bash
cd backend && pytest tests/ -n 16 -v --tb=short
```

---

#### 7. `/ep-dev` - Start Development Environment
**Launch full stack**

```bash
/ep-dev                  # Backend + Frontend + PostgreSQL
```

**Starts**:
1. PostgreSQL (if not running)
2. Backend (FastAPI on :8000)
3. Frontend (React on :5173)

**Equivalent to**:
```bash
make dev
```

---

#### 8. `/ep-benchmark` - Performance Benchmarks
**Test M3 Max optimizations**

```bash
/ep-benchmark            # All benchmarks
/ep-benchmark bulk       # Bulk operations only
```

**Tests**:
- Bulk shipment creation (100 in 30-40s)
- Batch tracking (50 in 2-3s)
- Analytics processing (1000 in 1-2s)
- Parallel vs sequential comparison

**Runs**:
```bash
pytest tests/integration/test_bulk_performance.py -v -s
```

---

## Context-Aware Magic

Commands use smart defaults - **no arguments needed**:

```bash
# Select code in editor → /explain explains it
# Terminal shows error → /fix fixes it
# Any file open → /test runs related tests
# No context → Commands ask for clarification
```

**Context sources**:
- Selected code in editor
- Open files
- Terminal output (errors)
- `.dev-config.json` (paths, conventions)
- Git status (changed files)

---

## Variable System

All commands use `.dev-config.json` for configuration:

```markdown
**Hardware**:
- {{hardware.cpuCores}} → 16
- {{hardware.workers.pytest}} → 16
- {{hardware.workers.python}} → 32

**Stack**:
- {{stack.backend.framework}} → "fastapi"
- {{stack.frontend.framework}} → "react"

**Paths**:
- {{paths.backend}} → "backend/src"
- {{paths.tests.backend}} → "backend/tests"
- {{paths.components}} → "frontend/src/components"

**Conventions**:
- {{conventions.python.functions}} → "snake_case"
- {{conventions.javascript.files}} → "PascalCase.jsx"

**Testing**:
- {{testing.backend.framework}} → "pytest"
- {{testing.frontend.framework}} → "vitest"
```

---

## Command Architecture

All commands follow this pattern:

```
User Input
    ↓
Parse & Detect Stack (from files or .dev-config.json)
    ↓
Enhance with Project Context (conventions, paths)
    ↓
Execute with Proper Tools (parallel when possible)
    ↓
Standardized Output
```

**Key insight**: Commands are interfaces. Logic uses project patterns.

---

## Performance (M3 Max)

| Command | Time | Workers | Use Case |
|---------|------|---------|----------|
| `/test` | 4-6s | 16 | Full test suite |
| `/fix` | 10-18s | AI | Error repair |
| `/explain` | 10-15s | AI | Code understanding |
| `/optimize` | 15-30s | AI | Performance tuning |
| `/api` | 8-12s | AI | Endpoint generation |
| `/ep-test` | 4-6s | 16 | EasyPost tests |
| `/ep-dev` | 2-3s | - | Start servers |
| `/ep-benchmark` | 30-60s | 16 | Performance tests |

**Total productivity gain**: 10-15x faster development

---

## Common Workflows

### Morning Startup (10s)
```bash
/ep-dev            # 3s - Start everything
/test              # 4s - Verify tests pass
```

### Feature Development (2 min)
```bash
/api /endpoint POST      # 10s - Generate endpoint
# Implement business logic
/test backend/tests/     # 4s - Test it
/fix                     # 10s - Fix any issues
```

### Debugging (30s)
```bash
/test                    # 4s - Run tests
# See error in terminal
/fix                     # 18s - Fix automatically
/test                    # 4s - Verify
```

### Code Review
```bash
# Select code block
/explain           # 10s - Understand code
/optimize          # 20s - Check optimizations
```

### Performance Tuning
```bash
/ep-benchmark      # 60s - Run benchmarks
/optimize backend/src/services/batch.py
/ep-benchmark      # 60s - Verify improvement
```

---

## Adding Custom Commands

### 1. Create File
```bash
touch .cursor/commands/project-specific/my-command.md
```

### 2. Write Prompt
```markdown
[Command description]

Usage: /my-command [args]

Uses configuration:
- Workers: {{hardware.workers.python}}
- Path: {{paths.backend}}
- Framework: {{stack.backend.framework}}

Steps:
1. [What it does]
2. [How it works]
3. [Expected output]
```

### 3. Use Immediately
```bash
/my-command
```

**No restart needed** - Cursor watches the directory!

---

## Archived Commands (14)

Available in `.cursor/archive/commands/`:

**Universal**:
- `/clean` - Project organization
- `/mcp-add` - Scaffold MCP tools
- `/component` - Generate UI components
- `/crud` - Full CRUD generation
- `/refactor` - Code refactoring
- `/workflow` - Workflow execution

**Project-Specific**:
- `/analytics-deep` - Deep analytics
- `/bulk-create` - Bulk shipment creation
- `/bulk-ship` - Bulk shipping
- `/carrier-compare` - Carrier comparison
- `/ep-lint` - Linting (use `make lint`)
- `/ep-mcp` - MCP operations
- `/shipping-optimize` - Shipping optimization
- `/track-batch` - Batch tracking
- `/workflow-ep` - EasyPost workflows

**Why archived**: Reduced from 22 to 8 core commands for better discoverability.
**Restoration**: Copy from archive to `.cursor/commands/` if needed.

---

## Verification

Type `/` in Cursor chat - you should see 8 commands:

**Universal (5)**:
- test
- fix
- explain
- optimize
- api

**Project-Specific (3)**:
- ep-test
- ep-dev
- ep-benchmark

**Try one**:
```bash
/test backend/tests/
# Expected: 4-6s with "16 workers" in output
```

---

## Documentation Hierarchy

1. **This file** (`COMMANDS.md`): Command reference
2. **START_HERE.md**: Onboarding guide
3. **Individual command files**: `.cursor/commands/universal/*.md`, `.cursor/commands/project-specific/*.md`
4. **`.cursorrules`**: IDE configuration
5. **`CLAUDE.md`**: Comprehensive project documentation

---

## Design Principles

1. **Simplicity**: 8 focused commands cover 95% of use cases
2. **Context-aware**: Smart defaults from IDE and config
3. **Performance**: M3 Max parallel processing (16 cores)
4. **Universal**: Core commands work across all projects
5. **Project-specific**: EasyPost commands for domain logic

**Sources**:
- GitHub Copilot research: Most used are /fix, /explain, /test
- Anthropic guidelines: Low-level and unopinionated
- MCP architecture: Thin wrappers, rich integrations
- User research: ~7 commands is cognitive limit

---

**Ready to use!** Type `/` in Cursor chat. 🚀

**Simple. Fast. Powerful.**
