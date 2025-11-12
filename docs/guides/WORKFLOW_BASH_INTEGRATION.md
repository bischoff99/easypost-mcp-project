# Workflow-Bash Integration Guide

**Purpose**: Document when to use workflows vs Makefile vs scripts, and how they integrate.

---

## Overview

This project has three ways to execute commands:

1. **Workflows** (`/workflow`): AI-powered command orchestration with state passing
2. **Makefile** (`make`): Standard build automation with script integration
3. **Scripts** (`scripts/*.sh`): Specialized operations and utilities

---

## When to Use What

### Use Workflows When:

- **Orchestrating multiple commands** with conditional execution
- **Need state passing** between commands
- **Want AI-powered error handling** and rollback
- **Working in Cursor IDE** with AI assistance
- **Need complex conditional logic** (`if-success`, `if-fails`)

**Examples**:
- `/workflow:pre-commit` - Full pre-commit checks
- `/workflow:error-resolution` - Fix errors systematically
- `/workflow:cleanup` - Comprehensive cleanup with verification

### Use Makefile When:

- **Standard build/test operations** (`make test`, `make build`)
- **Quick commands** from terminal (`make dev`, `make lint`)
- **CI/CD pipelines** (standard tooling)
- **Need script integration** (Makefile delegates to scripts)

**Examples**:
- `make test` - Run all tests with parallel execution
- `make dev` - Start development servers
- `make clean` - Clean build artifacts (delegates to script if available)

### Use Scripts When:

- **Specialized operations** not covered by Makefile
- **Platform-specific tasks** (macOS Terminal windows)
- **Complex setup** requiring multiple steps
- **One-off utilities** (benchmarking, monitoring)

**Examples**:
- `./scripts/benchmark.sh` - Performance benchmarks
- `./scripts/monitor-database.sh` - Database monitoring
- `./scripts/start-dev.sh` - macOS Terminal windows

---

## Integration Patterns

### 1. Test Execution

**Current State**:
- **Makefile**: `make test` uses `pytest -v -n auto` (parallel)
- **Workflows**: `/test` command uses `pytest -n auto` (parallel)
- **Scripts**: `quick-test.sh`, `test-full-functionality.sh`

**Consistency**: ✅ Both Makefile and workflows use parallel execution

**Usage**:
```bash
# From terminal
make test

# From Cursor IDE
/test

# Quick check
./scripts/quick-test.sh
```

### 2. Clean Execution

**Current State**:
- **Makefile**: `make clean` delegates to `scripts/clean_project_parallel.sh` if exists
- **Workflows**: `/clean` command does comprehensive MCP-based cleanup
- **Scripts**: `clean_project_parallel.sh` (if exists)

**Integration**: Workflows use `/clean` for comprehensive cleanup, Makefile uses script for basic cleanup

**Usage**:
```bash
# Basic cleanup (Makefile → script)
make clean

# Comprehensive cleanup (workflow)
/clean

# Deep clean (Makefile → script)
make clean-deep
```

### 3. Development Startup

**Current State**:
- **Makefile**: `make dev` starts servers directly
- **Scripts**: `start-dev.sh` (macOS Terminal), `dev.sh`, `dev_local.sh`, `dev-with-mcp.sh`
- **Workflows**: No direct development startup workflow

**Usage**:
```bash
# Standard startup (Makefile)
make dev

# macOS Terminal windows (script)
./scripts/start-dev.sh

# With MCP verification (script)
./scripts/dev-with-mcp.sh start
```

**Recommendation**: Use `make dev` for standard development, scripts for specialized needs.

### 4. Benchmarking

**Current State**:
- **Makefile**: `make benchmark` calls `./scripts/benchmark.sh`
- **Scripts**: `benchmark.sh` (comprehensive benchmarks)
- **Workflows**: No benchmarking workflow

**Usage**:
```bash
# From Makefile (delegates to script)
make benchmark

# Direct script execution
./scripts/benchmark.sh
```

**Note**: Workflows don't currently integrate with benchmarking, but could be added.

---

## Execution Path Comparison

### Test Execution

| Method | Command | Parallel? | When to Use |
|--------|---------|-----------|-------------|
| Makefile | `make test` | ✅ Yes (`-n auto`) | Terminal, CI/CD |
| Workflow | `/test` | ✅ Yes (`-n auto`) | Cursor IDE, AI assistance |
| Script | `quick-test.sh` | ⚠️ Partial | Quick checks |

### Clean Execution

| Method | Command | Scope | When to Use |
|--------|---------|-------|-------------|
| Makefile | `make clean` | Basic (delegates to script) | Terminal, CI/CD |
| Workflow | `/clean` | Comprehensive (MCP-based) | Cursor IDE, deep cleanup |
| Script | `clean_project_parallel.sh` | Basic (if exists) | Direct execution |

### Development Startup

| Method | Command | Features | When to Use |
|--------|---------|----------|-------------|
| Makefile | `make dev` | Standard servers | Terminal, standard dev |
| Script | `start-dev.sh` | macOS Terminal windows | macOS, separate windows |
| Script | `dev-with-mcp.sh` | MCP verification | MCP development |

---

## Best Practices

### 1. Consistency

- **Use Makefile** for standard operations (test, build, lint)
- **Use workflows** for complex orchestration (pre-commit, error resolution)
- **Use scripts** for specialized operations (benchmarking, monitoring)

### 2. Integration

- **Makefile delegates to scripts** when appropriate (clean, prod, benchmark)
- **Workflows execute commands directly** via MCP tools (no Makefile dependency)
- **Scripts are standalone** but can be called by Makefile

### 3. Documentation

- **Makefile**: Inline documentation (`make help`)
- **Workflows**: `.cursor/commands/WORKFLOW_USAGE_GUIDE.md`
- **Scripts**: `scripts/README.md`

### 4. Error Handling

- **Makefile**: Standard bash error handling (`set -e`, `|| exit 1`)
- **Workflows**: AI-powered error handling (rollback, retry, continue)
- **Scripts**: Varies (`set -euo pipefail` recommended)

---

## Future Integration Opportunities

### 1. Workflow → Makefile Integration

Workflows could call Makefile targets for consistency:

```yaml
# Example: Workflow calling Makefile
test:
  command: make test-fast  # Instead of direct pytest
```

**Benefits**: Consistency, leverages Makefile optimizations

### 2. Workflow → Script Integration

Workflows could integrate with specialized scripts:

```yaml
# Example: Workflow calling script
benchmark:
  command: ./scripts/benchmark.sh
```

**Benefits**: Access to specialized functionality

### 3. New Workflows

- **`benchmark`**: Performance analysis workflow
- **`development-startup`**: Start dev environment workflow
- **`database-health`**: Database monitoring workflow

---

## Troubleshooting

### Issue: Different behavior between `make test` and `/test`

**Solution**: Both now use parallel execution (`-n auto`). If you see differences, check:
- Makefile version (should have `-n auto`)
- `/test` command implementation (should use `-n auto`)

### Issue: `make clean` doesn't match `/clean` output

**Solution**: This is expected:
- `make clean`: Basic cleanup (delegates to script)
- `/clean`: Comprehensive MCP-based cleanup

Use the appropriate tool for your needs.

### Issue: Script not found when called by Makefile

**Solution**: Check:
- Script exists in `scripts/` directory
- Script is executable (`chmod +x scripts/script.sh`)
- Makefile path is correct (`./scripts/script.sh`)

---

## Summary

- **Workflows**: AI-powered orchestration for complex tasks
- **Makefile**: Standard build automation with script integration
- **Scripts**: Specialized operations and utilities

Use the right tool for the job, and understand how they integrate.

---

**Last Updated**: 2025-11-12
**Related Docs**:
- `.cursor/commands/WORKFLOW_USAGE_GUIDE.md`
- `scripts/README.md`
- `Makefile` (inline help: `make help`)
