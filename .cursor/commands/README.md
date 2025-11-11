# Universal Slash Commands - Complete System

**Location**: `.cursor/commands/`
**Auto-loaded**: Yes, Cursor watches this directory
**Status**: Production ready for personal development

---

## 🎯 THE 10 UNIVERSAL COMMANDS

Comprehensive suite of MCP-enhanced developer commands that work across any tech stack.

### 1. `/test` - Smart Parallel Testing ✅

**Enhanced with framework detection, test selection, and coverage analysis**

```bash
/test                    # Test everything (auto-detect)
/test --changed          # Only test changed files
/test --failed           # Rerun failed tests
/test --coverage         # With coverage analysis
```

**Performance**: 10-80s depending on test suite size
**Auto-detects**: pytest, vitest, jest, go test, cargo test (workers auto-detected, max 16)
**MCP**: Desktop Commander + Sequential-thinking + Context7
**Stages**: 6 (Framework Detection → Test Selection → Context7 → Execute → Parse → Coverage/Failure Analysis)

---

### 2. `/fix` - Auto-Repair Errors ✅

**Enhanced with retry logic, backup, and comprehensive error handling**

```bash
/fix                     # Auto-detect visible error
/fix --dry-run           # Preview fix
/fix --retry             # Force retry
```

**How**: Error Detection → Root Cause Analysis → Fix Patterns → Prepare Fix → Backup → Apply → Verify + Retry
**Performance**: 10-20s for complete fix cycle (longer with retry)
**MCP**: Sequential-thinking + Context7 + Desktop Commander
**Stages**: 7 (Detect → Analyze → Patterns → Prepare → Backup → Apply → Verify)

---

### 3. `/explain` - AI Code Understanding ✅

**Enhanced with architecture mapping, call graphs, and performance profiling**

```bash
/explain                 # Explain selected code
/explain --focus=performance
/explain --focus=architecture
```

**Provides**: Step-by-step logic, architecture context, call graphs, performance analysis, best practices
**Performance**: 12-20s for comprehensive explanation
**MCP**: Sequential-thinking + Context7 + Desktop Commander
**Stages**: 5 (Sequential-thinking → Framework Context → Architecture Mapping → Performance → Report)

---

### 4. `/commit` - Smart Git Commits ✅

**Conventional commit messages with automatic change detection**

```bash
/commit                  # Auto-detect and commit all changes
/commit --push           # Commit and push
/commit --type=fix       # Override commit type
```

**How**: Detect Changes → Analyze → Generate Message → Stage → Commit
**Performance**: 6-15s for complete commit cycle
**MCP**: Desktop Commander + Sequential-thinking
**Stages**: 5 (Detect → Analyze → Generate → Stage → Commit)

---

### 5. `/review` - Automated Code Review ✅

**Static analysis, best practices, and AI-powered review**

```bash
/review                  # Review selected code or open file
/review --auto-fix       # Auto-fix issues
/review --focus=security
```

**Provides**: Linter errors, type errors, security issues, best practice violations, AI review
**Performance**: 17-34s for complete review (longer with auto-fix)
**MCP**: Desktop Commander + Sequential-thinking + Context7
**Stages**: 6 (Gather → Static Analysis → Best Practices → AI Review → Report → Auto-Fix)

---

### 6. `/refactor` - Safe Code Refactoring ✅

**Verified refactoring with automatic test verification**

```bash
/refactor                # Refactor selected code
/refactor --dry-run      # Show plan without applying
/refactor --focus=functions
```

**How**: Analyze → Best Practices → Plan → Backup + Apply → Verify → Report
**Performance**: 12-28s for complete refactoring cycle
**MCP**: Desktop Commander + Sequential-thinking + Context7
**Stages**: 6 (Analyze → Best Practices → Plan → Backup + Apply → Verify → Report)

---

### 7. `/docs` - Documentation Generation ✅

**Comprehensive documentation with docstrings and README sections**

```bash
/docs                    # Document selected code
/docs --readme           # Generate README sections
/docs --style=google     # Specify docstring style
```

**Provides**: Docstrings, README sections, API documentation, examples
**Performance**: 8-20s depending on number of items
**MCP**: Desktop Commander + Sequential-thinking + Context7
**Stages**: 4 (Analyze → Generate Docstrings → README → Verify)

---

### 8. `/debug` - Interactive Debugging ✅

**Intelligent breakpoint placement and output analysis**

```bash
/debug                   # Debug selected code
/debug --test            # Debug with test
/debug --keep-logs       # Keep debug logging
```

**How**: Identify Issue → Add Instrumentation → Execute + Capture → Analyze
**Performance**: 10-23s for complete debug cycle
**MCP**: Desktop Commander + Sequential-thinking
**Stages**: 4 (Identify → Instrument → Execute → Analyze)

---

### 9. `/clean` - Comprehensive Project Cleanup ✅

**Enhanced with deep code analysis, dependency cleanup, and code quality improvements**

**Remove unnecessary files, build artifacts, dead code, unused dependencies, and clean project structure with comprehensive code analysis**

```bash
/clean                   # Clean up everything (default)
/clean --from-simplify   # Clean files identified by simplify
/clean --category=temporary
/clean --category=code-quality
/clean --category=dependencies
/clean --with-code-improvement  # Include code improvements
/clean --dry-run         # Show what would be deleted
```

**How**: 10-stage workflow with deep code analysis, dependency analysis, and code quality cleanup
**Performance**: 60-180s for analysis, 2-5 minutes for full cleanup (3-7 minutes with code-improvement)
**MCP**: Desktop Commander + Sequential-thinking + Context7
**Stages**: 10 (Scan → Deep Code Analysis → Dependency Analysis → Patterns → Classify → Plan → Backup → Apply → Verify)
**Categories**: 12 (temporary, build artifacts, unused, duplicates, large, documentation, code quality, dependencies, configuration, tests, git)

---

### 10. `/workflow` - Command Chain Orchestration ✅

**Orchestrate universal commands into high-value workflow chains**

```bash
/workflow:pre-commit      # Pre-commit workflow (review → fix → test → commit)
/workflow:feature-dev     # Feature development workflow
/workflow:error-resolution # Error resolution workflow
/workflow:code-improvement # Code improvement workflow
/workflow:debugging       # Debugging workflow
/workflow:cleanup         # Cleanup workflow
/workflow:morning-routine # Morning routine workflow
/workflow:pre-push        # Pre-push workflow
```

**How**: Parse → Plan → Execute → Handle Errors → Report
**Performance**: Varies by workflow (30s - 5 minutes)
**MCP**: Sequential-thinking + Desktop Commander + Context7
**Stages**: 5 (Parse → Plan → Execute → Handle Errors → Report)

**Features**:

- State passing between commands
- Conditional execution (if-fails, if-success)
- Error handling (stop/continue/rollback)
- Parallel execution support
- Comprehensive reporting

---

## 🔧 HOW THEY WORK

### Thin MCP Wrappers (Research-backed pattern)

All commands follow this architecture:

```
User Input
    ↓
Parse & Detect Stack (auto from files or .dev-config.json)
    ↓
Enhance with Context7 (framework best practices)
    ↓
Analyze with Sequential-thinking (AI reasoning)
    ↓
Execute with Desktop Commander (auto-detected workers)
    ↓
Standardized Output
```

**Key insight**: Commands are just interfaces. Logic lives in MCP servers.

---

## 📊 CONTEXT-AWARE MAGIC

**No arguments needed** - commands use smart defaults:

```bash
# Select code in editor
/explain        # → Explains selected code

# Terminal shows error
/fix            # → Fixes visible error

# Any file open
/test           # → Tests related test directory

# No file open
/clean          # → Cleans entire project
```

**Reads context from:**

- Selected code in editor
- Open files
- Terminal output (errors)
- .dev-config.json (paths, conventions)
- Git status (changed files)

---

## 🚀 MULTI-STACK ADAPTATION

### Auto-Detection Patterns

Commands automatically detect your stack:

**Python Projects:**

- Detects: `from fastapi import` → FastAPI
- Tests: `pytest -n auto`
- Linter: `ruff --fix`
- Format: `black`

**JavaScript Projects:**

- Detects: `import React` → React
- Tests: `vitest --threads auto`
- Linter: `eslint --fix`
- Format: `prettier`

**Go Projects:**

- Detects: `import "github.com/gin-gonic/gin"` → Gin
- Tests: `go test -parallel auto`
- Linter: `golangci-lint run`
- Format: `gofmt`

**See detection patterns**: `.dev-config.json` → `stack.detection`

---

## ⚡ M3 MAX OPTIMIZATION

All commands leverage your hardware:

**Tier 1 - Light (1-4 cores):**

- Analysis, parsing, single operations
- Examples: Error detection, file scanning

**Tier 2 - Medium (4-8 cores):**

- Code generation, refactoring
- Examples: Generating components, applying fixes

**Tier 3 - Heavy (8-16 cores):**

- Parallel execution, bulk operations
- Examples: `/test` (auto-detected workers), `/clean` (auto-detected workers)

**Workers from config:**

```json
{{hardware.workers.pytest}}  // auto-detected
{{hardware.workers.vitest}}  // auto-detected
{{hardware.workers.python}}  // auto-detected (max 16)
```

---

## 📦 COMMAND FILES

```
.cursor/commands/
├── universal/              # Work across ANY project
│   ├── test.md            # Smart parallel testing (enhanced)
│   ├── fix.md             # Auto-repair errors (enhanced)
│   ├── explain.md         # AI code understanding (enhanced)
│   ├── commit.md          # Smart git commits (new)
│   ├── review.md          # Automated code review (new)
│   ├── refactor.md        # Safe code refactoring (new)
│   ├── docs.md            # Documentation generation (new)
│   ├── debug.md           # Interactive debugging (new)
│   ├── clean.md           # Project cleanup (new)
│   ├── workflow.md        # Command chain orchestration (new)
│   ├── api.md             # Generate endpoints (bonus)
│   ├── component.md       # Generate UI (bonus)
│   ├── crud.md            # Full CRUD (bonus)
│   ├── optimize.md        # M3 Max patterns (bonus)
│   └── simplify.md       # Simplify project - enterprise removal & overbloat cleanup (bonus)
│
└── project-specific/       # Add EasyPost customs here
```

**Universal 10**: test, fix, explain, commit, review, refactor, docs, debug, clean, workflow
**Bonus**: api, component, crud, optimize, simplify

---

## ➕ ADDING CUSTOM COMMANDS

### 1. Create File

```bash
touch .cursor/commands/project-specific/bulk-rates.md
```

### 2. Add Prompt with Variables

```markdown
Process bulk shipping rates using EasyPost MCP.

Arguments: /bulk-rates [spreadsheet_data]

Uses MCP:

- Server: easypost-shipping
- Tool: parse_and_get_bulk_rates
- Workers: {{hardware.workers.python}}

Adapts from .dev-config.json:

- Workers: {{hardware.workers.python}}
- Batch size: {{hardware.optimization.batchSizeOptimal}}
```

### 3. Use Immediately

```bash
/bulk-rates [paste data]
```

**No restart needed** - Cursor watches the directory!

---

## 🔧 VARIABLES SYSTEM

**Available in all commands:**

```json
// Hardware
{{hardware.cpuCores}}              // auto-detected
{{hardware.workers.pytest}}        // auto-detected
{{hardware.workers.python}}        // auto-detected (max 16)

// Stack
{{stack.backend.framework}}        // "fastapi"
{{stack.frontend.framework}}       // "react"

// Paths
{{paths.backend}}                  // "backend/src"
{{paths.tests.backend}}            // "backend/tests"
{{paths.components}}               // "frontend/src/components"

// Conventions
{{conventions.python.functions}}   // "snake_case"
{{conventions.javascript.files}}   // "PascalCase.jsx"

// Testing
{{testing.backend.framework}}      // "pytest"
{{testing.frontend.framework}}     // "vitest"
```

**Auto-resolved** from `.dev-config.json`!

---

## 📈 PERFORMANCE COMPARISON

| Command     | Time (M3 Max)                                        | Stages | Workers                |
| ----------- | ---------------------------------------------------- | ------ | ---------------------- |
| `/test`     | 10-80s                                               | 6      | auto-detected (max 16) |
| `/fix`      | 10-20s                                               | 7      | AI chain               |
| `/explain`  | 12-20s                                               | 5      | AI chain               |
| `/commit`   | 6-15s                                                | 5      | N/A                    |
| `/review`   | 17-34s                                               | 6      | Parallel (3 tools)     |
| `/refactor` | 12-28s                                               | 6      | Sequential             |
| `/docs`     | 8-20s                                                | 4      | Sequential             |
| `/debug`    | 10-23s                                               | 4      | Sequential             |
| `/clean`    | 60-180s (analysis), 2-5min (full), 3-7min (enhanced) | 10     | Sequential             |
| `/workflow` | 30s - 5min (varies by workflow)                      | 5      | Sequential/Parallel    |

**Total productivity gain**: Comprehensive development workflow with AI-powered assistance

---

## 🎓 USAGE WORKFLOWS

### Morning Routine

```bash
/test              # Verify everything works
/fix               # Fix any lingering issues
/commit            # Commit overnight changes
```

### Feature Development

```bash
# Start feature
/explain           # Understand existing code
# Implement business logic
/test --changed    # Test new code
/fix               # Fix any issues
/review            # Review code quality
/refactor          # Clean up code
/docs              # Document new code
/commit            # Commit feature
```

### Code Review Workflow

```bash
/review            # Comprehensive code review
/explain           # Understand code logic
/test              # Run tests
/fix --auto-fix    # Auto-fix issues
/refactor          # Improve code structure
```

### Debugging Workflow

```bash
/debug             # Add debug instrumentation
# Run code
/debug             # Analyze output
/fix               # Apply fix based on analysis
/test              # Verify fix
```

### Simplification Workflow

```bash
/simplify          # Analyze enterprise features and overbloat
/simplify --apply   # Auto-remove enterprise features and simplify
/clean --from-simplify  # Clean up files identified by simplify
/clean              # General cleanup (temporary files, build artifacts)
/test              # Verify simplifications didn't break anything
```

### Cleanup Workflow

```bash
/clean             # Clean up everything (temporary files, build artifacts)
/clean --dry-run   # Preview what would be deleted
/clean --category=temporary  # Clean specific category
/clean --from-simplify  # Clean files from simplify recommendations
```

### Workflow Orchestration

**8 High-Value Workflow Chains:**

```bash
# Pre-commit (most common)
/workflow:pre-commit      # review → fix → test → commit

# Feature development (most comprehensive)
/workflow:feature-dev     # explain → refactor → test → review → docs → commit

# Error resolution
/workflow:error-resolution # fix → test → review → commit

# Code improvement
/workflow:code-improvement # review → refactor → test → docs → commit

# Debugging
/workflow:debugging       # debug → fix → test → commit

# Cleanup
/workflow:cleanup         # simplify → clean → test → commit

# Morning routine
/workflow:morning-routine # test → fix → commit

# Pre-push
/workflow:pre-push        # review → test → commit
```

**Features**:

- State passing between commands
- Conditional execution (if-fails, if-success)
- Error handling (stop/continue/rollback)
- Parallel execution where safe
- Comprehensive reporting

---

## ✅ VERIFICATION

Type `/` in Cursor chat - you should see:

**Universal Commands (10 total):**

- test ✅ (enhanced - 6 stages, framework detection, coverage analysis)
- fix ✅ (enhanced - 7 stages, retry logic, backup)
- explain ✅ (enhanced - 5 stages, architecture mapping, performance)
- commit ✅ (new - 5 stages, conventional commits)
- review ✅ (new - 6 stages, static analysis, auto-fix)
- refactor ✅ (new - 6 stages, safe refactoring, test verification)
- docs ✅ (new - 4 stages, docstrings, README)
- debug ✅ (new - 4 stages, intelligent debugging)
- clean ✅ (new - 8 stages, file cleanup, simplify integration)
- workflow ✅ (new - 5 stages, command orchestration, 8 workflow chains)

**All commands support:**

- Python, JavaScript/TypeScript, Go, Rust
- Exact MCP tool names
- Progress reporting
- Comprehensive error handling
- State management
- Universal language support

**Try one:**

```bash
/test backend/tests/
# Expected: Framework detection, test selection, coverage analysis

/fix
# Expected: Error detection, root cause analysis, fix application, verification

/explain
# Expected: Sequential-thinking analysis, architecture mapping, performance analysis
```

---

## 📚 DOCUMENTATION

- **This file**: Quick command reference
- **Workflow Chains Reference**: `WORKFLOW_CHAINS_REFERENCE.md` - Complete reference for all 8 workflow chains
- **Workflow Usage Guide**: `WORKFLOW_USAGE_GUIDE.md` - Complete guide for using `/workflow` command
- **Workflow Analysis**: `WORKFLOW_CHAINING_ANALYSIS.md` - Research and implementation details
- **Workflows (Current)**: `WORKFLOWS-CURRENT.md` - ✅ All working workflows
- **Workflows (Future)**: `WORKFLOW-EXAMPLES.md` - 🔴 Aspirational templates
- **Full guide**: `.cursor/docs/UNIVERSAL_COMMANDS_GUIDE.md`
- **Quick ref**: `.cursor/docs/COMMANDS_QUICK_REF.md`
- **Configuration**: `.cursor/config/universal-commands.json`
- **Main README**: `.cursor/README.md`

---

## 🔄 WORKFLOWS

### ✅ Currently Working (See WORKFLOWS-CURRENT.md)

**Real commands you can use right now:**

```bash
# Development
make dev              # Start servers (5s)
make test             # Run all tests (15s)
make test-fast        # Fast tests (6s)
make test-watch       # TDD mode

# Quality
make format           # Auto-format (3s)
make lint             # Linters (4s)
make check            # All checks (22s)

# Build
make build            # Production (30s)
make benchmark        # Performance (15s)

# Chains
make check && make benchmark  # Pre-push (37s)
```

### 🔴 Future Templates (See WORKFLOW-EXAMPLES.md)

Aspirational workflow patterns for future implementation:

- `/workflow:morning` - Morning routine
- `/workflow:pre-commit` - Git hooks
- `/workflow:security` - Security audit
- And 14 more...

**Status:** 4/17 workflows implemented (24%)

---

## 🎯 DESIGN PRINCIPLES (Research-Based)

1. **Comprehensive**: 10 universal commands cover complete development workflow
2. **Context-aware**: Smart defaults from IDE context
3. **MCP-native**: Exact tool names with full integration
4. **Performance**: Auto-detected parallel processing (max 16 workers)
5. **Universal**: Adapts to Python, JS, Go, Rust equally
6. **Safe**: Backup, verification, rollback mechanisms
7. **Intelligent**: Sequential-thinking + Context7 for best practices

**Sources:**

- Anthropic: "Low-level and unopinionated"
- GitHub Copilot: Most used are /fix, /explain, /test
- MCP architecture: Expose capabilities once, use everywhere
- Academic research: Context-aware > syntax memorization

---

**Ready to use!** Type `/` in Cursor chat. 🚀

**Comprehensive. Intelligent. Universal.**
