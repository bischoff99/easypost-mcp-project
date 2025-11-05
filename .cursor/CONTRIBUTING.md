# Contributing to Cursor IDE Configuration

Guide for maintaining and extending the Cursor IDE setup for this project.

---

## Overview

This project uses a highly optimized Cursor IDE configuration with:
- 8 core slash commands (reduced from 22)
- 14 comprehensive coding standards (`.cursor/rules/`)
- Hardware-optimized workflows (M3 Max with 16 cores)
- Configuration-driven development (`.dev-config.json`)

---

## Adding a New Slash Command

### 1. Determine Command Type

**Universal Command**: Works across any project
- Location: `.cursor/commands/universal/`
- Examples: `/test`, `/fix`, `/explain`
- Use when: Command applies to all codebases

**Project-Specific Command**: EasyPost domain logic
- Location: `.cursor/commands/project-specific/`
- Examples: `/ep-test`, `/ep-dev`, `/ep-benchmark`
- Use when: Command specific to shipping/EasyPost

### 2. Create Command File

```bash
# Universal command
touch .cursor/commands/universal/my-command.md

# Project-specific command
touch .cursor/commands/project-specific/ep-my-feature.md
```

### 3. Write Command Prompt

Use this template:

```markdown
# /my-command - Brief Description

## Purpose
[One sentence: what this command does]

## Usage
\`\`\`bash
/my-command [args]
/my-command --option
\`\`\`

## Configuration
Uses `.dev-config.json` for:
- Workers: {{hardware.workers.python}}
- Path: {{paths.backend}}
- Framework: {{stack.backend.framework}}

## Steps
1. [What it does first]
2. [What it does second]
3. [What it does third]

## Expected Output
\`\`\`
✓ [Expected result]
Time: Xs
Workers: Y
\`\`\`

## Examples

### Example 1: [Scenario]
\`\`\`bash
/my-command input
\`\`\`

Output:
\`\`\`
[Expected output]
\`\`\`

## Performance
- Time: X-Ys
- Workers: Z (M3 Max optimized)
- Use case: [When to use this command]

## Related Commands
- `/other-command` - [How it relates]
```

### 4. Test the Command

```bash
# In Cursor chat
/my-command
```

Verify:
- Command appears in `/` autocomplete
- Variables resolve correctly
- Output format is correct
- Performance meets expectations

### 5. Document in COMMANDS.md

Add entry to `.cursor/COMMANDS.md`:

```markdown
### X. `/my-command [args]` - Brief Description
**Description**

\`\`\`bash
/my-command arg
\`\`\`

**Performance**: X-Ys | **Workers**: Z
```

### 6. Update Command Count

Keep the 8 core command limit. If adding a new command:
1. Archive an existing command to `.cursor/archive/commands/`
2. Document why it was replaced
3. Update `.cursor/COMMANDS.md` archived section

---

## Adding a Coding Rule

### 1. Choose Rule Number

Existing rules: 01-14

For new rule: `15-[category].mdc`

Categories:
- Core Standards (01-06): Code, structure, naming
- Domain Standards (07-09): Git, security, API
- Quality Standards (10-13): Docs, performance, deployment
- Reference (14): Quick patterns

### 2. Create Rule File

```bash
touch .cursor/rules/15-my-rule.mdc
```

### 3. Write Rule Content

Template:

```markdown
# [Rule Name]

## Purpose
[What this rule ensures]

## Standards

### [Sub-section 1]
- Rule 1
- Rule 2
- Rule 3

### [Sub-section 2]
- Rule 1
- Rule 2

## Examples

### Good ✓
\`\`\`[language]
[Good example]
\`\`\`

### Bad ✗
\`\`\`[language]
[Bad example]
\`\`\`

## Rationale
[Why this rule exists]

## Exceptions
[When rules can be bent]

## Related Rules
- [Related rule file]
```

### 4. Update 00-INDEX.mdc

Add entry to `.cursor/rules/00-INDEX.mdc`:

```markdown
### 15-my-rule.mdc
**[Brief description]**
- [Key point 1]
- [Key point 2]
```

### 5. Test Rule Application

Write code that violates the rule and verify:
- Linters catch it (if applicable)
- Cursor AI references the rule
- Team members can find the rule

---

## Updating Configuration

### .dev-config.json Sections

**metadata**: Version tracking
```json
{
  "version": "X.Y.Z",
  "lastUpdated": "YYYY-MM-DD",
  "changelog": [...]
}
```

**project**: Basic info
```json
{
  "name": "Project Name",
  "type": "fullstack|backend|frontend",
  "description": "Brief description"
}
```

**stack**: Technology stack
```json
{
  "backend": { "framework": "fastapi", ... },
  "frontend": { "framework": "react", ... }
}
```

**hardware**: M3 Max specifications
```json
{
  "cpuCores": 16,
  "workers": {
    "pytest": 16,
    "python": 32
  }
}
```

**workflows**: Multi-step workflows only
```json
{
  "workflow-name": {
    "description": "What it does",
    "commands": "command1 && command2",
    "estimated_time": "Xs",
    "category": "development|testing|release"
  }
}
```

### When to Update

**metadata.version**:
- Increment on significant changes
- Follow semantic versioning

**workflows**:
- Only add multi-step workflows
- Remove single-command workflows (use slash commands)
- Keep total under 10

**hardware.workers**:
- Update if CPU core count changes
- Maintain 2x CPU cores for I/O workers

---

## Workflow Guidelines

### Keep Workflows If:
- Multi-step (2+ commands)
- Conditional logic (||, &&)
- Team frequently uses it
- Demonstrates M3 Max parallelism

### Archive Workflows If:
- Single command (use slash command instead)
- Rarely used
- Duplicates Makefile target
- Uses archived commands

### Workflow Naming:
- `pre-commit`, `pre-push`: Git hooks
- `ep-*`: EasyPost domain-specific
- `debug`, `ship`: Development phases

---

## VS Code Integration

### Adding Extensions

Edit `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "publisher.extension-id"  // Add here
  ]
}
```

Categories:
- Python/Backend
- React/Frontend
- Testing
- Docker
- Markdown
- Optional

### Adding Tasks

Edit `.vscode/tasks.json`:

```json
{
  "label": "🔧 My Task",
  "type": "shell",
  "command": "make target",
  "options": {
    "cwd": "${workspaceFolder}"
  }
}
```

### Adding Debug Configurations

Edit `.vscode/launch.json`:

```json
{
  "name": "Debug: My Feature",
  "type": "python",
  "request": "launch",
  "module": "src.my_feature"
}
```

### Adding Snippets

Edit `.vscode/snippets.code-snippets`:

```json
{
  "My Snippet": {
    "prefix": "my",
    "scope": "python",
    "body": [
      "code line 1",
      "code line 2"
    ],
    "description": "Brief description"
  }
}
```

---

## Documentation Standards

### File Locations

- **Entry point**: `.cursor/START_HERE.md`
- **Command reference**: `.cursor/COMMANDS.md`
- **This guide**: `.cursor/CONTRIBUTING.md`
- **Rules index**: `.cursor/rules/00-INDEX.mdc`
- **Project guide**: `CLAUDE.md` (root)

### Writing Style

- **Concise**: Get to the point
- **Examples**: Always include code examples
- **Performance**: State timing expectations
- **M3 Max**: Mention worker counts
- **Configuration**: Reference `.dev-config.json` variables

### Updating Docs

When changing:
- **Commands**: Update `.cursor/COMMANDS.md`
- **Rules**: Update `.cursor/rules/00-INDEX.mdc`
- **Configuration**: Update `.dev-config.json` metadata
- **Project**: Update `CLAUDE.md`

---

## Code Review Checklist

Before committing Cursor IDE configuration changes:

- [ ] `.cursorrules` under 200 lines
- [ ] Total commands ≤ 8
- [ ] Total workflows ≤ 10
- [ ] All commands tested
- [ ] Documentation updated
- [ ] `.dev-config.json` metadata updated
- [ ] Commit message follows conventions
- [ ] No secrets in configuration files

---

## Archiving

### When to Archive

- Commands no longer used (usage < 1/month)
- Documentation outdated (> 6 months)
- Workflows replaced by better alternatives
- Experimental features that didn't work

### How to Archive

```bash
# Commands
mv .cursor/commands/[type]/command.md .cursor/archive/commands/

# Documentation
mv .cursor/docs/file.md .cursor/archive/docs/

# Update .gitignore to exclude archive
# Already configured: .cursor/archive/ is ignored
```

### Archive Structure

```
.cursor/archive/
├── commands/
│   ├── [archived-command].md
│   └── v2-migration-docs/
├── docs/
│   └── [old-documentation].md
└── backup-YYYY-MM-DD/
    └── [backup files]
```

---

## Performance Optimization

### Command Performance Targets

| Command Type | Target Time | Workers |
|--------------|-------------|---------|
| Simple (test, fix) | < 20s | 16 |
| Medium (api, optimize) | < 30s | AI |
| Complex (benchmark) | < 60s | 16 |

### Workflow Performance Targets

- Pre-commit: < 20s
- Pre-push: < 30s
- Full quality gate: < 60s

### If Performance Degrades

1. Check worker count in `.dev-config.json`
2. Verify pytest.ini: `-n 16`
3. Check CPU usage during execution
4. Profile with `/ep-benchmark`

---

## Troubleshooting

### Commands Not Appearing

1. Check `.cursorrules` exists
2. Verify `.cursor/commands/` structure
3. Restart Cursor IDE
4. Check file permissions

### Variables Not Resolving

1. Verify `.dev-config.json` syntax
2. Check variable path: `{{section.subsection.key}}`
3. Test with simple command

### Performance Issues

1. Check CPU core count in `.dev-config.json`
2. Verify worker configuration
3. Check for resource contention
4. Profile with system monitor

### Git Tracking Issues

1. Review `.gitignore` for `.cursor/` rules
2. Check that rules/ and commands/ are tracked
3. Verify archive/ and docs/ are ignored

---

## Version Control

### What to Commit

✓ `.cursor/rules/` - Team standards
✓ `.cursor/commands/` - Slash commands
✓ `.cursor/config/` - Templates
✓ `.cursor/START_HERE.md` - Onboarding
✓ `.cursor/COMMANDS.md` - Command reference
✓ `.cursor/CONTRIBUTING.md` - This guide
✓ `.cursorrules` - IDE configuration
✓ `.dev-config.json` - Project configuration

### What to Ignore

✗ `.cursor/archive/` - Old files
✗ `.cursor/docs/` - Generated docs
✗ `.cursor/*STATUS*.md` - Temporary files
✗ `.cursor/*COMPLETE*.md` - Status markers

---

## Getting Help

### Resources

- **Command examples**: `.cursor/commands/README.md`
- **Configuration template**: `.cursor/config/dev-config.template.json`
- **Project guide**: `CLAUDE.md`
- **Quick reference**: `.cursor/rules/00-INDEX.mdc`

### Questions?

1. Check `.cursor/START_HERE.md`
2. Review `.cursor/COMMANDS.md`
3. Read relevant `.cursor/rules/*.mdc`
4. Check `.dev-config.json` for current settings

---

## Best Practices Summary

1. **Keep it simple**: 8 commands, 10 workflows, 14 rules
2. **Document everything**: Update docs with changes
3. **Test thoroughly**: Verify commands work as expected
4. **Performance matters**: Target < 20s for common tasks
5. **Configuration-driven**: Use `.dev-config.json` variables
6. **Archive liberally**: Move unused items to archive
7. **Version tracking**: Update metadata in `.dev-config.json`
8. **Team consistency**: Follow existing patterns

---

**Questions? Check `.cursor/START_HERE.md` or read `CLAUDE.md`**
