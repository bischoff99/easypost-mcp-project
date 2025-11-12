# Unified Commands Reference

**Complete reference for all commands across Makefile, Scripts, VS Code Tasks, and Cursor Workflows.**

**Last Updated**: 2025-11-12
**Total Commands**: 50

---

## Quick Navigation

- [Makefile Commands](#makefile-commands) (12)
- [Bash Scripts](#bash-scripts) (14)
- [VS Code Tasks](#vs-code-tasks) (8)
- [Cursor Workflows](#cursor-workflows) (6)
- [Universal Commands](#universal-commands) (10)
- [Command Selection Guide](#command-selection-guide)

---

## Makefile Commands

**Location**: `Makefile`
**Usage**: `make <command>`
**Best Practice**: 12 commands (optimal range 10-15)

### Setup
```bash
make setup        # Full environment setup (creates venv + installs dependencies)
```

### Development
```bash
make dev          # Start backend + frontend servers (parallel, includes MCP verification)
```

### Testing
```bash
make test         # Run all tests (parallel, auto-detected workers)
make test COV=1   # Run tests with coverage report
```

### Code Quality
```bash
make lint         # Run linters (ruff, eslint) - parallel execution
make format       # Auto-format code (ruff, prettier) - parallel execution
make check        # Run lint + test (sequential)
```

### Building
```bash
make build        # Build production bundles (frontend + backend type check)
```

### Production
```bash
make prod         # Start backend + frontend in production mode
```

### Database
```bash
make db-reset     # Reset database (downgrade + upgrade)
make db-migrate   # Create migration (use: make db-migrate m="message")
```

### Maintenance
```bash
make clean        # Clean build artifacts (__pycache__, dist, coverage, etc.)
```

### Git
```bash
make qcp          # Quick commit + push (use: make qcp m="message")
```

---

## Bash Scripts

**Location**: `scripts/`
**Usage**: `./scripts/<script-name>.sh`
**Total**: 14 scripts

### Development Scripts

#### `start-dev.sh`
Start both backend and frontend servers in separate terminal windows (macOS only).

```bash
./scripts/dev/start-dev.sh
```

**What it does**:
- Opens new Terminal window for backend (port 8000)
- Opens new Terminal window for frontend (port 5173)
- Shows URLs and test commands

**Requirements**: macOS Terminal

---

#### `start-backend.sh`
Start only the backend FastAPI server.

```bash
./scripts/dev/start-backend.sh          # Standard mode (single worker, reload)
./scripts/dev/start-backend.sh --jit   # JIT mode (Python 3.13+, multi-worker)
./scripts/dev/start-backend.sh --mcp-verify  # Enhanced MCP verification
```

**What it does**:
- Activates Python virtual environment
- Standard mode: Starts uvicorn with hot reload (single worker)
- JIT mode: Multi-worker setup with JIT compilation (Python 3.13+)
  - Calculates workers: (2 × CPU cores) + 1
  - Uses uvloop for better performance
  - Expects 10-20% performance boost
- Port: 8000

---

**Note**: For frontend-only development, use `cd apps/frontend && npm run dev` directly or use VS Code task "Dev: Frontend".

---

#### `dev_local.sh`
Development startup script with Docker PostgreSQL.

```bash
./scripts/dev/dev_local.sh
```

**What it does**:
- Starts PostgreSQL Docker container
- Setup and start backend server
- Setup and start frontend server
- Includes error checking and user feedback
- Handles cleanup on exit

---

#### `mcp-utils.sh`
MCP utility commands for verification and testing.

```bash
./scripts/utils/mcp-utils.sh health   # Check MCP server health
./scripts/utils/mcp-utils.sh verify   # Verify MCP tools are registered
./scripts/utils/mcp-utils.sh test     # Test MCP tools with sample data
```

**What it does**:
- Standalone MCP verification utilities
- Can be used independently of server startup
- Useful for debugging MCP integration

**Note**: MCP verification is also integrated into `start-backend.sh` with `--mcp-verify` flag.

---

#### `start-prod.sh`
Start production servers.

```bash
./scripts/dev/start-prod.sh
```

**What it does**:
- Starts backend in production mode
- Starts frontend production build
- Uses production environment variables

---

### Testing Scripts

#### `quick-test.sh`
Run quick test suite for both backend and frontend.

```bash
./scripts/test/quick-test.sh
```

**What it does**:
- Backend: Runs pytest with minimal output
- Frontend: Runs Vitest in run mode
- Shows test results summary

**Duration**: ~30-60 seconds

---

#### `watch-tests.sh`
Run tests in watch mode for active development.

```bash
./scripts/test/watch-tests.sh
```

**What it does**:
- Backend: Starts pytest-watch (re-runs on file changes)
- Frontend: Starts Vitest in watch mode
- Useful for TDD workflow

**Stop**: Ctrl+C

---

#### `test-full-functionality.sh`
Run comprehensive functionality tests.

```bash
./scripts/test/test-full-functionality.sh
```

**What it does**:
- Runs full test suite
- Tests API endpoints
- Validates database operations
- Checks frontend functionality

---

#### `benchmark.sh`
Run comprehensive performance benchmarks (M3 Max optimized).

```bash
./scripts/test/benchmark.sh
```

**What it does**:
- System information (CPU, RAM, cores)
- Backend performance (build speed, test speed)
- Frontend performance (build speed, test speed)
- Docker build speed (if available)
- Performance summary with expected gains

**Duration**: 2-5 minutes

---

### Utility Scripts

#### `monitor-database.sh`
Monitor PostgreSQL database activity.

```bash
./scripts/utils/monitor-database.sh
```

**What it does**:
- Shows active connections
- Displays query statistics
- Monitors database performance

---

#### `setup-nginx-proxy.sh`
Setup Nginx reverse proxy for production.

```bash
./scripts/utils/setup-nginx-proxy.sh
```

**What it does**:
- Configures Nginx for frontend/backend routing
- Sets up SSL certificates (if available)
- Configures proxy headers

---

#### `clean-git-history.sh`
Clean API keys from git history using git-filter-repo.

```bash
./scripts/utils/clean-git-history.sh
```

**What it does**:
- Removes `.vscode/thunder-client-settings.json` from git history
- Cleans up reflog
- Verifies keys are removed

**Warning**: Rewrites git history (requires force push)

---

### Python Scripts

#### `get-bulk-rates.py`
Python script for bulk rate testing.

```bash
python scripts/python/get-bulk-rates.py
```

**What it does**:
- Tests bulk shipment rate retrieval
- Validates bulk operations
- Useful for debugging bulk tools

---

#### `verify_mcp_server.py`
Verify MCP server configuration.

```bash
python scripts/python/verify_mcp_server.py
```

**What it does**:
- Validates MCP server setup
- Tests tool registration
- Checks resource providers

---

#### `mcp_tool.py`
MCP tool testing utility.

```bash
python scripts/python/mcp_tool.py get_tracking TEST
```

**What it does**:
- Tests MCP tools
- Validates tool responses
- Useful for debugging MCP integration

---

## VS Code Tasks

**Location**: `.vscode/tasks.json`
**Usage**: `Ctrl+Shift+P` → "Tasks: Run Task"
**Total**: 8 tasks

### Development (3)

#### 🚀 Dev: Full Stack
Compound task: Starts both backend and frontend servers in parallel.

**Features**:
- Background tasks with problem matchers
- Error detection and inline error display
- IDE integration

---

#### Dev: Backend
Individual backend server task.

**Features**:
- Background task with problem matcher
- Configurable port (input prompt)
- Python error detection

---

#### Dev: Frontend
Individual frontend server task.

**Features**:
- Background task with problem matcher
- Vite error detection
- Hot reload support

---

### Testing (2)

#### 🧪 Test: Backend
Quick test runner with VS Code test group integration.

**Features**:
- Parallel execution (`-n auto`)
- Problem matcher for test failures
- VS Code test explorer integration

---

#### 🧪 Test: Frontend
Quick test runner with VS Code test group integration.

**Features**:
- Problem matcher for test failures
- VS Code test explorer integration

---

### Build (1)

#### 🏗️ Build: Frontend
Default build task (VS Code build group).

**Features**:
- Default build task (`Ctrl+Shift+B`)
- Problem matcher for build errors

---

### Workflows (1)

#### ✅ Pre-Commit: Run All Checks
Pre-commit workflow using Makefile.

**Features**:
- Uses `make check` for consistency
- Runs format, lint, and test
- Single source of truth

---

### Database (1)

#### 🗄️ Database: Create Migration
Database migration creation with input prompt.

**Features**:
- Input prompt for migration message
- Alembic integration
- IDE integration

---

## Cursor Workflows

**Location**: `.cursor/commands/`
**Usage**: `/workflow:<name> [flags]`
**Total**: 6 workflows

### 1. Pre-Commit Workflow ⭐⭐⭐⭐⭐

```bash
/workflow:pre-commit              # Full: review → fix → test → commit (30-60s)
/workflow:pre-commit --quick      # Quick: test → fix → commit (20-50s)
```

**Chain**: `review → fix → test → commit` (default) or `test → fix → commit` (quick)

**When to use**: Before every commit

---

### 2. Feature Development Workflow ⭐⭐⭐⭐⭐

```bash
/workflow:feature-dev
```

**Chain**: `explain → refactor → test → review → docs → commit`

**When to use**: When implementing new features

**Duration**: 60-180s

---

### 3. Error Resolution Workflow ⭐⭐⭐⭐

```bash
/workflow:error-resolution        # Standard: fix → test → review → commit (40-130s)
/workflow:error-resolution --debug # With debug: debug → fix → test → review → commit (50-150s)
```

**Chain**: `[debug] → fix → test → review → commit`

**When to use**: When fixing bugs or errors

---

### 4. Code Improvement Workflow ⭐⭐⭐⭐

```bash
/workflow:code-improvement
```

**Chain**: `review → refactor → test → docs → commit`

**When to use**: When improving existing code

**Duration**: 55-175s

---

### 5. Cleanup Workflow ⭐⭐⭐⭐⭐

```bash
/workflow:cleanup                 # Standard: simplify → clean → test → commit (2-5 min)
/workflow:cleanup --with-code-improvement # Enhanced (3-7 min)
```

**Chain**: `simplify → clean → test → commit` (default) or `simplify → clean → code-improvement → test → commit` (enhanced)

**When to use**: Periodic project cleanup

---

### 6. Pre-Push Workflow ⭐⭐⭐⭐

```bash
/workflow:pre-push
```

**Chain**: `review → test → commit`

**When to use**: Before pushing to remote

**Duration**: 30-130s

---

## Universal Commands

**Location**: `.cursor/commands/`
**Usage**: `/<command> [flags]`
**Total**: 10 commands

### 1. `/test` - Smart Parallel Testing

```bash
/test                    # Test everything (auto-detect)
/test --changed          # Only test changed files
/test --failed           # Rerun failed tests
/test --coverage         # With coverage analysis
```

**Performance**: 10-80s
**Auto-detects**: pytest, vitest, jest, go test, cargo test

---

### 2. `/fix` - Auto-Repair Errors

```bash
/fix                     # Auto-detect visible error
/fix --dry-run           # Preview fix
/fix --retry             # Force retry
```

**Performance**: 10-20s

---

### 3. `/explain` - AI Code Understanding

```bash
/explain                 # Explain selected code
/explain --focus=performance
/explain --focus=architecture
```

**Performance**: 12-20s

---

### 4. `/commit` - Smart Git Commits

```bash
/commit                  # Auto-detect and commit all changes
/commit --push           # Commit and push
/commit --type=fix       # Override commit type
```

**Performance**: 6-15s

---

### 5. `/review` - Automated Code Review

```bash
/review                  # Review selected code or open file
/review --auto-fix       # Auto-fix issues
/review --focus=security
```

**Performance**: 17-34s

---

### 6. `/refactor` - Safe Code Refactoring

```bash
/refactor                # Refactor selected code
/refactor --dry-run      # Show plan without applying
/refactor --focus=functions
```

**Performance**: 12-28s

---

### 7. `/docs` - Documentation Generation

```bash
/docs                    # Document selected code
/docs --readme           # Generate README sections
/docs --style=google     # Specify docstring style
```

**Performance**: 8-20s

---

### 8. `/debug` - Interactive Debugging

```bash
/debug                   # Debug selected code
/debug --test            # Debug with test
/debug --keep-logs       # Keep debug logging
```

**Performance**: 10-23s

---

### 9. `/clean` - Comprehensive Project Cleanup

```bash
/clean                   # Clean up everything (default)
/clean --from-simplify   # Clean files identified by simplify
/clean --category=temporary
/clean --category=code-quality
/clean --category=dependencies
/clean --with-code-improvement
/clean --dry-run         # Show what would be deleted
```

**Performance**: 85-225s for analysis, 2-5 minutes for full cleanup

---

### 10. `/workflow` - Command Chain Orchestration

```bash
/workflow:pre-commit              # Pre-commit workflow
/workflow:pre-commit --quick      # Quick mode
/workflow:feature-dev             # Feature development workflow
/workflow:error-resolution        # Error resolution workflow
/workflow:error-resolution --debug # With debug instrumentation
/workflow:code-improvement        # Code improvement workflow
/workflow:cleanup                 # Cleanup workflow
/workflow:pre-push                # Pre-push workflow
```

**Performance**: Varies by workflow (30s - 5 minutes)

---

## Command Selection Guide

### When to Use Makefile

✅ **Use for**:
- Daily development tasks
- Quick commands (< 30s)
- Parallel execution needed
- Simple command chains
- CI/CD pipelines

**Examples**:
- `make dev` - Start development servers
- `make test` - Run tests
- `make lint` - Check code quality
- `make check` - Full quality check

---

### When to Use Scripts

✅ **Use for**:
- Complex workflows
- macOS-specific features (Terminal windows)
- Docker operations
- Database monitoring
- Performance benchmarks
- Specialized use cases

**Examples**:
- `./scripts/start-dev.sh` - macOS Terminal windows
- `./scripts/test/benchmark.sh` - Performance benchmarks
- `./scripts/utils/monitor-database.sh` - Database monitoring
- `./scripts/dev_local.sh` - Docker + servers

---

### When to Use VS Code Tasks

✅ **Use for**:
- IDE integration (problem matchers)
- Background tasks
- Quick access from IDE
- Pre-launch tasks for debugging
- Input prompts (migration messages, ports)

**Examples**:
- "Dev: Full Stack" - Start servers from IDE
- "Test: Backend" - Run tests with IDE integration
- "Database: Create Migration" - Input prompt for message

---

### When to Use Cursor Workflows

✅ **Use for**:
- AI-powered workflows
- Complex multi-step processes
- Code understanding and refactoring
- Automated fixes and improvements
- Documentation generation

**Examples**:
- `/workflow:pre-commit` - Before committing
- `/workflow:feature-dev` - Feature development
- `/workflow:error-resolution` - Bug fixing

---

### When to Use Universal Commands

✅ **Use for**:
- AI-powered assistance
- Code understanding (`/explain`)
- Automated fixes (`/fix`)
- Complex refactoring (`/refactor`)
- Documentation generation (`/docs`)
- Interactive debugging (`/debug`)

**Examples**:
- `/test` - Smart parallel testing
- `/fix` - Auto-repair errors
- `/explain` - Understand codebase
- `/refactor` - Improve code quality

---

## Common Workflows

### Morning Routine

```bash
# Option 1: Makefile (fastest)
make clean && make test && make dev

# Option 2: Scripts (macOS Terminal windows)
./scripts/start-dev.sh

# Option 3: VS Code
# Run "Dev: Full Stack" task
```

---

### Before Commit

```bash
# Option 1: Makefile (standard)
make format && make lint && make test

# Option 2: Makefile (all-in-one)
make check

# Option 3: VS Code
# Run "Pre-Commit: Run All Checks" task

# Option 4: Cursor workflow (AI-powered)
/workflow:pre-commit
```

---

### Feature Development

```bash
# Option 1: Cursor workflow (recommended)
/workflow:feature-dev

# Option 2: Manual steps
make dev
# ... code changes ...
make test
make lint
make format
git commit -m "feat: feature"
```

---

### Bug Fixing

```bash
# Option 1: Cursor workflow (recommended)
/workflow:error-resolution

# Option 2: Universal commands
/fix
/test
/commit

# Option 3: Manual steps
make test
# ... fix code ...
make test
make check
git commit -m "fix: bug"
```

---

### Testing

```bash
# Quick test
make test

# With coverage
make test COV=1

# Watch mode (TDD)
./scripts/test/watch-tests.sh

# Quick test suite
./scripts/test/quick-test.sh

# AI-powered
/test
```

---

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Full check
make check

# AI-powered review
/review
```

---

## Performance Comparison

| Command | Time | Parallel | Notes |
|---------|------|----------|-------|
| `make dev` | 5s | ✅ | Starts both servers |
| `make test` | 15s | ✅ | Auto-detected workers |
| `make lint` | 4s | ✅ | Parallel execution |
| `make format` | 3s | ✅ | Parallel execution |
| `make check` | 22s | ⚠️ | Sequential (lint → test) |
| `/workflow:pre-commit` | 30-60s | ⚠️ | Sequential chain |
| `/workflow:feature-dev` | 60-180s | ⚠️ | Sequential chain |
| `./scripts/test/benchmark.sh` | 2-5 min | ⚠️ | Sequential |

---

## Integration Points

### Makefile → Scripts
- `make prod` → `./scripts/start-prod.sh`
- `make clean` → Delegates to script if exists

### VS Code → Makefile
- "Pre-Commit" task → `make check`
- Tasks can call Makefile commands

### Cursor Workflows → Commands
- Workflows call universal commands (`/test`, `/fix`)
- Workflows orchestrate multiple commands

### Scripts → Makefile
- Scripts can call Makefile commands (not currently used)
- Opportunity for future consolidation

---

## Best Practices

### Consistency
- ✅ Use Makefile for standard operations
- ✅ Use scripts for specialized workflows
- ✅ Use VS Code tasks for IDE integration
- ✅ Use Cursor workflows for AI-powered assistance

### Error Handling
- ✅ Makefile: Uses `check_venv` macro consistently
- ✅ Scripts: Use `set -euo pipefail`
- ✅ VS Code: Problem matchers for error detection

### Documentation
- ✅ Makefile: Inline help (`make help`)
- ✅ Scripts: `scripts/README.md`
- ✅ VS Code: Inline comments
- ✅ Cursor: Separate workflow docs

---

## Quick Reference

### Most Used Commands

**Daily Development**:
1. `make dev` - Start development servers
2. `make test` - Run tests
3. `make format` - Format code
4. `make lint` - Check code quality

**Before Commit**:
1. `/workflow:pre-commit` - Full pre-commit workflow
2. `make check` - Quick quality check
3. `make qcp m="message"` - Quick commit + push

**Feature Development**:
1. `/workflow:feature-dev` - Complete feature workflow
2. `/explain` - Understand codebase
3. `/refactor` - Improve code quality

---

**Last Updated**: 2025-11-12
**Status**: ✅ Complete - Single source of truth for all commands
