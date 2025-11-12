# Command Consolidation Rationale

## Overview

This document explains why similar commands exist across different contexts (Makefile, Bash Scripts, VS Code Tasks, Cursor Commands) and when to use each.

## Command Categories

### 1. Development Startup

**Available Commands:**
- `make dev` - Parallel execution in single terminal
- `./scripts/dev/start-dev.sh` - macOS Terminal windows (separate windows)
- `./scripts/dev/dev_local.sh` - Docker PostgreSQL + servers
- `./scripts/dev/start-backend.sh` - Backend only (standard, --jit, or --mcp-verify)
- VS Code "Dev: Full Stack" - IDE-integrated
- `/ep-dev` - Cursor command (Desktop Commander integration)

**Rationale:**
- **Makefile**: Quick command, runs in current terminal, good for CI/CD
- **Bash Scripts**: More control, macOS-specific features (Terminal windows), Docker integration
- **VS Code Tasks**: IDE integration, debugging support, problem matchers
- **Cursor Commands**: AI-enhanced, context-aware, Desktop Commander integration

**When to Use:**
- **Makefile**: Quick start, CI/CD, automation
- **Bash Scripts**: macOS Terminal windows, Docker setup, custom configurations
- **VS Code Tasks**: When developing in VS Code, need debugging
- **Cursor Commands**: When using Cursor AI, want context-aware execution

### 2. Testing

**Available Commands:**
- `make test` - Full test suite
- `./scripts/test/quick-test.sh` - Quick health checks (~30-60s)
- `./scripts/test/watch-tests.sh` - Watch mode (TDD)
- `./scripts/test/test-full-functionality.sh` - Comprehensive integration
- `./scripts/test/benchmark.sh` - Performance benchmarks
- VS Code "Test: Backend" / "Test: Frontend" - IDE-integrated
- `/ep-test` - Cursor command (auto-detects test type, parallel execution)
- `/ep-benchmark` - Cursor command (performance benchmarks)

**Rationale:**
- **Makefile**: Standard test execution, CI/CD integration
- **Bash Scripts**: Quick checks, watch mode, comprehensive testing, benchmarks
- **VS Code Tasks**: IDE integration, debugging support, problem matchers
- **Cursor Commands**: AI-enhanced, context-aware (auto-detects test type from open file), Desktop Commander integration

**When to Use:**
- **Makefile**: Standard test runs, CI/CD
- **Bash Scripts**: Quick checks, watch mode, comprehensive testing, benchmarks
- **VS Code Tasks**: When developing in VS Code, need debugging
- **Cursor Commands**: When using Cursor AI, want context-aware test execution

### 3. Code Quality

**Available Commands:**
- `make lint` - Lint both backend and frontend
- `make format` - Format code
- `make check` - Lint + format + test
- VS Code "Pre-Commit: Run All Checks" - IDE-integrated

**Rationale:**
- **Makefile**: Standard quality checks, CI/CD integration
- **VS Code Tasks**: IDE integration, problem matchers

**When to Use:**
- **Makefile**: Standard quality checks, CI/CD, pre-commit hooks
- **VS Code Tasks**: When developing in VS Code, want IDE integration

### 4. Build & Production

**Available Commands:**
- `make build` - Build both backend and frontend
- `make prod` - Start production servers
- `./scripts/dev/start-prod.sh` - Production startup script
- VS Code "Build: Frontend" - IDE-integrated

**Rationale:**
- **Makefile**: Standard build process, CI/CD integration
- **Bash Scripts**: More control, custom configurations
- **VS Code Tasks**: IDE integration

**When to Use:**
- **Makefile**: Standard builds, CI/CD
- **Bash Scripts**: Custom production configurations
- **VS Code Tasks**: When developing in VS Code

## Consolidation Decisions

### What Was Consolidated

1. **Removed `dev-with-mcp.sh`**: Merged into `start-backend.sh` with `--mcp-verify` flag
   - **Reason**: Redundant functionality, better to have one script with flags

2. **Organized Scripts into Subdirectories**:
   - `scripts/dev/` - Development scripts
   - `scripts/test/` - Testing scripts
   - `scripts/utils/` - Utility scripts
   - `scripts/python/` - Python tools
   - **Reason**: Better organization, easier to find scripts

3. **Removed `start-frontend.sh`**: Redundant wrapper for `npm run dev`
   - **Reason**: Too simple, direct command is clearer

4. **Extracted Common Functions**: Created `scripts/lib/common.sh`
   - **Reason**: Reduce duplication, improve maintainability

### What Was NOT Consolidated

1. **Cursor Commands (`/ep-dev`, `/ep-test`, `/ep-benchmark`)**: Kept separate
   - **Reason**: Provide unique value through AI enhancement and context-awareness
   - **Value**: Auto-detects test types, integrates with Desktop Commander, context-aware execution

2. **VS Code Tasks**: Kept separate
   - **Reason**: IDE integration, debugging support, problem matchers
   - **Value**: Better developer experience within VS Code

3. **Makefile vs Scripts**: Both kept
   - **Reason**: Different use cases (CI/CD vs interactive development)
   - **Value**: Makefile for automation, scripts for interactive use

## Decision Tree

### Development Startup

```
Need macOS Terminal windows?
├─ Yes → ./scripts/dev/start-dev.sh
└─ No → Need Docker PostgreSQL?
    ├─ Yes → ./scripts/dev/dev_local.sh
    └─ No → Using Cursor AI?
        ├─ Yes → /ep-dev
        └─ No → Using VS Code?
            ├─ Yes → VS Code "Dev: Full Stack"
            └─ No → make dev
```

### Testing

```
Need watch mode?
├─ Yes → ./scripts/test/watch-tests.sh
└─ No → Need quick check?
    ├─ Yes → ./scripts/test/quick-test.sh
    └─ No → Need benchmarks?
        ├─ Yes → Using Cursor AI?
        │   ├─ Yes → /ep-benchmark
        │   └─ No → ./scripts/test/benchmark.sh
        └─ No → Need comprehensive tests?
            ├─ Yes → ./scripts/test/test-full-functionality.sh
            └─ No → Using Cursor AI?
                ├─ Yes → /ep-test
                └─ No → Using VS Code?
                    ├─ Yes → VS Code "Test: Backend" / "Test: Frontend"
                    └─ No → make test
```

## Best Practices

1. **Use Makefile for**: CI/CD, automation, standard workflows
2. **Use Bash Scripts for**: Custom configurations, macOS-specific features, Docker integration
3. **Use VS Code Tasks for**: IDE-integrated development, debugging
4. **Use Cursor Commands for**: AI-enhanced, context-aware execution

## Summary

The command ecosystem is intentionally diverse to serve different contexts:
- **Makefile**: Automation and CI/CD
- **Bash Scripts**: Interactive development, custom configurations
- **VS Code Tasks**: IDE integration
- **Cursor Commands**: AI-enhanced, context-aware execution

Each serves a specific purpose, and the overlaps are intentional to provide flexibility for different workflows and preferences.
