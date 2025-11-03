# Enhanced Slash Commands v2.0

**Based on**: Industry research (GitHub Copilot, Claude Code, Anthropic best practices)
**Created**: 2025-11-03
**Status**: Production Ready

## 🎯 What's New

### 1. Command Categorization
Commands organized by purpose with namespacing:
- `session:*` - Session management
- `gen:*` - Code generation
- `quality:*` - Code quality & fixes
- `test:*` - Testing workflows
- `context:*` - Context-aware operations

### 2. Context Variables
Use `@` to reference context:
- `@file` - Currently selected file
- `@selection` - Selected code
- `@open-files` - All open files
- `@git-diff` - Git changes
- `@errors` - Linter errors

### 3. Tool Permissions
Every command declares allowed tools for safety

### 4. Metadata Standard
Commands include execution time, token usage, arguments

### 5. Agent Mode
Multi-step execution with feedback loops

## 📂 Directory Structure

```
.cursor/commands/v2/
├── README.md (this file)
├── session/           # Session management
│   ├── clear.md
│   ├── compact.md
│   ├── cost.md
│   └── checkpoint.md
├── gen/               # Code generation
│   ├── api.md
│   ├── component.md
│   ├── model.md
│   └── crud.md
├── quality/           # Code quality
│   ├── fix.md
│   ├── refactor.md
│   ├── optimize.md
│   └── secure.md
├── test/              # Testing
│   ├── run.md
│   ├── watch.md
│   ├── coverage.md
│   └── mock.md
└── context/           # Context-aware
    ├── explain.md
    ├── improve.md
    └── doc.md
```

## 🚀 Quick Examples

```bash
# Session management
/session:clear                    # Reset conversation
/session:cost                     # Show token usage
/session:checkpoint save-point-1  # Save state

# Code generation with context
/gen:api /users POST              # Generate API endpoint
/gen:component @selection         # Generate from selected code

# Quality improvements
/quality:fix @errors              # Fix linter errors
/quality:optimize @file           # Optimize current file

# Testing
/test:run @git-diff               # Test changed files
/test:coverage backend/           # Coverage report

# Context-aware
/context:explain @selection       # Explain selected code
/context:improve @open-files      # Improve all open files
```

## 📊 Command Metadata Format

All commands follow this metadata standard:

```markdown
---
name: command-name
category: session|gen|quality|test|context
description: Brief description
allowed-tools: [Read, FileEdit, Bash]
requires-approval: true|false
context-aware: true|false
arguments:
  - name: arg_name
    type: string|path|integer|boolean
    required: true|false
    default: value
    description: Argument description
estimated-time: 5-10s
estimated-tokens: 1000-2000
version: 2.0
---

# Command Documentation

Detailed command description and usage...
```

## 🔧 Migration from v1

Old flat structure (`/api`, `/test`) still works via aliases.
New commands use namespace (`/gen:api`, `/test:run`).

To migrate:
1. Old commands remain functional
2. Start using new namespaced commands
3. Adopt context variables gradually
4. Review tool permissions

## 📈 Performance Impact

**M3 Max Optimized**:
- Parallel execution: 16-32 workers
- Context caching: Faster repeated commands
- Smart defaults: Less typing, same results

**Metrics Tracked**:
- Execution time per command
- Token usage per command
- Success rate (% completing without errors)
- Context hit rate (when variables are useful)

## 🔐 Security

**Tool Permission Levels**:
- `Read` - Read files only
- `Grep` - Search codebase
- `FileEdit` - Modify files
- `Bash(pattern)` - Execute shell commands (scoped)
- `Network` - External API calls

Commands declare needed permissions upfront.

## 🎓 Learning Resources

- See individual command files for detailed docs
- Check `QUICK_REFERENCE.md` for command cheat sheet
- Review `.dev-config.json` for project customization

