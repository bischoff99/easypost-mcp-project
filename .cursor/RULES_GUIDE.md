# Cursor Rules System - Official Documentation Summary

## Overview

Based on [Cursor's official documentation](https://docs.cursor.com/en/context/rules), rules provide persistent, reusable context that guides the AI in generating code, interpreting edits, and assisting with workflows.

## Rule Types

### 1. **Project Rules** (Recommended)
- Location: `.cursor/rules/` directory
- Version-controlled with your codebase
- Can be organized in subdirectories
- Use `.mdc` format (Markdown with frontmatter)

### 2. **User Rules**
- Global settings in Cursor preferences
- Apply across all projects
- Good for personal preferences

### 3. **Legacy `.cursorrules`**
- Deprecated, but still supported
- Single file at project root
- Migrate to Project Rules for better control

## .MDC File Format

Each rule file should have **frontmatter metadata** at the top:

```markdown
---
description: "Brief description of what this rule does"
globs: ["**/*.py", "backend/**/*.py"]
alwaysApply: false
---

# Rule Title

Rule content here...
```

### Metadata Fields

- **`description`**: Required for Agent Requested rules. Helps AI understand when to use this rule.
- **`globs`**: File patterns to auto-attach the rule. Uses glob syntax (e.g., `**/*.py`, `frontend/**/*.jsx`)
- **`alwaysApply`**: Boolean. If `true`, rule is always included in context.

## Rule Application Types

### 1. **Always** (`alwaysApply: true`)
- Included in model context for ALL operations
- Use sparingly (impacts token usage)
- Good for: Project-wide conventions

### 2. **Auto Attached** (with `globs`)
- Automatically included when matching files are referenced
- Most common type
- Good for: Language-specific or directory-specific rules

### 3. **Agent Requested**
- AI decides whether to include it
- Requires descriptive `description` field
- Good for: Optional specialized knowledge

### 4. **Manual** (Reference with `@ruleName`)
- Only included when explicitly mentioned
- Good for: Rare or specialized workflows

## Best Practices from Official Docs

### ✅ DO:
1. **Keep rules focused** - One clear purpose per rule
2. **Stay concise** - Under 500 lines per rule
3. **Include examples** - Concrete code examples
4. **Write clearly** - Clear internal documentation
5. **Use descriptive names** - Easy to reference with `@ruleName`
6. **Split large rules** - Multiple composable rules instead of one massive file

### ❌ DON'T:
1. **Over-apply** - Don't use `alwaysApply: true` everywhere
2. **Be vague** - Avoid vague guidance
3. **Mix concerns** - Don't combine unrelated topics
4. **Ignore organization** - Use subdirectories for structure

## File Organization

```
.cursor/
├── rules/
│   ├── 00-INDEX.mdc                 # Overview/index
│   ├── 01-fastapi-python.mdc        # Backend rules
│   ├── 02-react-vite-frontend.mdc   # Frontend rules
│   ├── 03-testing-best-practices.mdc
│   ├── 04-mcp-development.mdc
│   ├── 05-m3-max-optimizations.mdc
│   └── backend/                     # Nested rules
│       └── api-specific.mdc         # Auto-attach for backend/ files
```

## Glob Pattern Examples

```yaml
# Python files anywhere
globs: ["**/*.py"]

# Only backend Python files
globs: ["backend/**/*.py"]

# Multiple patterns
globs: ["backend/**/*.py", "src/**/*.py"]

# Test files
globs: ["**/test_*.py", "**/*.test.js"]

# Frontend files
globs: ["frontend/**/*.jsx", "frontend/**/*.js"]

# Specific directory
globs: ["src/mcp_server/**/*.py"]
```

## Usage in Cursor

### Referencing Rules Manually
In chat or composer, use `@` to reference a rule:
```
@01-fastapi-python help me create a new API endpoint
```

### Generating Rules from Chat
Use the `/Generate Cursor Rules` command to create rules from conversations.

### Viewing Active Rules
Check which rules are currently applied in the context panel.

## Our Implementation

### Essential Rules (Cursor.Directory Optimized)

1. **`01-fastapi-python.mdc`** ⭐
   - Auto-attaches: `backend/**/*.py`, `**/*.py`
   - Comprehensive FastAPI patterns
   - 400+ lines of examples

2. **`02-react-vite-frontend.mdc`** ⭐
   - Auto-attaches: `frontend/**/*.jsx`, `frontend/**/*.js`
   - Complete React + Vite guide
   - Performance patterns

3. **`03-testing-best-practices.mdc`** ⭐
   - Auto-attaches: `**/test_*.py`, `**/*.test.js`
   - pytest + vitest strategies
   - Parallel testing (16-20 workers)

4. **`04-mcp-development.mdc`** ⭐
   - Auto-attaches: `**/mcp_server/**/*.py`
   - FastMCP patterns
   - Tool design for AI agents

5. **`05-m3-max-optimizations.mdc`** ⭐
   - Manual reference (no globs)
   - Hardware-specific optimizations
   - Performance benchmarks

### Why These Are Better

✅ **Proper metadata** - Auto-attach to relevant files
✅ **Comprehensive** - 400-500 lines with examples
✅ **Organized** - Clear categories and structure
✅ **Optimized** - From cursor.directory + project-specific
✅ **Documented** - Clear descriptions for AI context

## Token Management

**Important**: Rules consume tokens!

- Each rule included = tokens from context window
- Use `globs` to auto-attach only when relevant
- Avoid `alwaysApply: true` unless critical
- Keep rules under 500 lines

**Example Token Usage**:
- Small rule (100 lines) ≈ 500 tokens
- Medium rule (300 lines) ≈ 1500 tokens
- Large rule (500 lines) ≈ 2500 tokens

With smart glob patterns, you only pay for rules you're actually using.

## Migration from Legacy

If you have a `.cursorrules` file:

1. Create `.cursor/rules/` directory
2. Split content into focused `.mdc` files
3. Add frontmatter metadata
4. Test with relevant files
5. Delete `.cursorrules` when confident

## Further Reading

- [Official Cursor Rules Docs](https://docs.cursor.com/en/context/rules)
- [Cursor Directory](https://cursor.directory) - Community rules
- Project-specific: See `.cursor/rules/00-INDEX.mdc`

---

**Created**: 2025-11-07
**Based on**: Cursor Official Documentation + cursor.directory best practices
