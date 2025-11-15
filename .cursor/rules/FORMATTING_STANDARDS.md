# Cursor Rules Formatting Standards

**Date**: 2025-11-18
**Version**: 1.0.0
**Status**: Official Project Standard

---

## Frontmatter Format Standard

All `.mdc` rule files in `.cursor/rules/` must follow this format:

### Standard Template

```yaml
---
description: 'Brief description of rule purpose (max 80 chars)'
globs: ['pattern1', 'pattern2']
alwaysApply: false
version: '1.0.0'
lastUpdated: '2025-11-18'
---
```

---

## Formatting Rules

### 1. Quote Style

**Rule**: Use single quotes for all string values

```yaml
✅ Correct:
description: 'My rule description'
version: '1.0.0'
lastUpdated: '2025-11-18'

❌ Incorrect:
description: "My rule description"
version: "1.0.0"
lastUpdated: "2025-11-18"
```

**Applies To**:

- `description` field
- `version` field
- `lastUpdated` field
- Glob patterns within arrays

---

### 2. Array Format

**Rule**: Use multiline format for arrays with 2+ items

```yaml
✅ Correct (2+ items):
globs:
  [
    'apps/frontend/**/*.js',
    'apps/frontend/**/*.jsx',
    'apps/frontend/**/*.ts',
    'apps/frontend/**/*.tsx',
  ]

✅ Acceptable (single item):
globs: ['src/**/*.py']

✅ Acceptable (empty):
globs: []
```

**Format Details**:

- Opening bracket on same line as key
- One item per line
- 2-space indentation
- Trailing comma after each item
- Closing bracket on new line with trailing comma

---

### 3. Boolean Values

**Rule**: No quotes for boolean values

```yaml
✅ Correct:
alwaysApply: false
alwaysApply: true

❌ Incorrect:
alwaysApply: 'false'
alwaysApply: "true"
```

---

### 4. Field Order

**Standard Order**:

1. `description`
2. `globs`
3. `alwaysApply`
4. `version`
5. `lastUpdated`

```yaml
✅ Correct:
---
description: 'Rule description'
globs: []
alwaysApply: false
version: '1.0.0'
lastUpdated: '2025-11-18'
---
```

---

## Complete Examples

### Example 1: Always Applied Rule (Empty Globs)

```yaml
---
description: 'Quick reference for naming conventions, code patterns, and common standards'
globs: []
alwaysApply: true
version: '1.0.0'
lastUpdated: '2025-11-18'
---
```

**Use Case**: Rules that apply to all files (quick reference, project knowledge)

---

### Example 2: Single Pattern Rule

```yaml
---
description: 'Comprehensive FastAPI and Python best practices for backend development'
globs: ['src/**/*.py']
alwaysApply: false
version: '1.0.0'
lastUpdated: '2025-11-18'
---
```

**Use Case**: Rules for specific directory/file type

---

### Example 3: Multiple Pattern Rule

```yaml
---
description: 'MCP (Model Context Protocol) development patterns and best practices'
globs: ['**/mcp_server/**/*.py', '**/mcp/**/*.py']
alwaysApply: false
version: '1.0.0'
lastUpdated: '2025-11-18'
---
```

**Use Case**: Rules for multiple directories or patterns

---

### Example 4: Complex Test Patterns

```yaml
---
description: 'Comprehensive testing strategy for pytest and vitest'
globs:
  [
    '**/test_*.py',
    '**/tests/**/*.py',
    '**/*.spec.js',
    '**/*.spec.jsx',
    '**/*.test.js',
    '**/*.test.jsx',
    '**/*.test.ts',
    '**/*.test.tsx',
  ]
alwaysApply: false
version: '1.0.0'
lastUpdated: '2025-11-18'
---
```

**Use Case**: Rules covering multiple languages/patterns

---

## Glob Pattern Best Practices

### 1. Be Specific

```yaml
✅ Correct (specific):
globs: ['src/**/*.py']

❌ Incorrect (too broad):
globs: ['**/*.py']
```

### 2. Logical Ordering

Group related patterns together:

```yaml
✅ Correct (grouped and alphabetical):
globs: [
    # Python patterns
    '**/test_*.py',
    '**/tests/**/*.py',
    # JavaScript patterns
    '**/*.spec.js',
    '**/*.test.js',
    '**/*.test.jsx',
  ]
```

### 3. Alphabetical Within Groups

```yaml
✅ Correct:
globs:
  [
    'apps/frontend/**/*.js',
    'apps/frontend/**/*.jsx',
    'apps/frontend/**/*.ts',
    'apps/frontend/**/*.tsx',
  ]
```

---

## Version Management

### Version Field

- Format: `'MAJOR.MINOR.PATCH'`
- Current standard: `'1.0.0'`
- Increment when:
  - Major: Breaking changes to rule structure
  - Minor: New rules or significant updates
  - Patch: Small fixes or clarifications

### Last Updated Field

- Format: `'YYYY-MM-DD'`
- Update when: Any change to the file
- Current: `'2025-11-18'`

---

## Creating New Rule Files

### Template

```yaml
---
description: 'Brief description (max 80 chars)'
globs: ['pattern1', 'pattern2']
alwaysApply: false
version: '1.0.0'
lastUpdated: 'YYYY-MM-DD'
---

# Rule Title

You are an expert in [domain/technology].

## Core Principles

- Principle 1
- Principle 2

## [Section Name]

[Content with examples]

---

[Closing note or reference]
```

---

## Validation Checklist

Before committing changes to rule files:

- [ ] All strings use single quotes
- [ ] Arrays with 2+ items use multiline format
- [ ] Boolean values have no quotes
- [ ] Field order is correct
- [ ] Description is under 80 characters
- [ ] Globs patterns are specific and accurate
- [ ] Version follows semantic versioning
- [ ] LastUpdated matches current date
- [ ] No YAML syntax errors
- [ ] No linter warnings

---

## Tools Integration

### Prettier Compatibility

This format is fully compatible with Prettier:

- 2-space indentation
- Trailing commas
- Single quotes
- Consistent bracket placement

### YAML Linter

Validate files with:

```bash
# Check YAML syntax
yamllint .cursor/rules/*.mdc
```

---

## Common Pitfalls

### ❌ Mixed Quotes

```yaml
description: 'Mixed quotes'
version: '1.0.0' # ❌ Should be single quotes
```

### ❌ Inline Complex Arrays

```yaml
globs: ['pattern1', 'pattern2', 'pattern3', 'pattern4'] # ❌ Hard to read
```

### ❌ Missing Trailing Commas

```yaml
globs: [
    'pattern1',
    'pattern2', # ❌ Missing trailing comma
  ]
```

---

## Maintenance

### When to Update

- **description**: When rule purpose changes
- **globs**: When file structure changes or new patterns added
- **alwaysApply**: Rarely (only if rule scope changes)
- **version**: On significant changes
- **lastUpdated**: On any change

### Review Schedule

- **Quarterly**: Review all globs patterns for accuracy
- **On structural changes**: Update patterns immediately
- **Version bumps**: Document changes in commit message

---

## References

- **Official Docs**: https://github.com/getcursor/docs
- **Community Best Practices**: https://cursor.directory/
- **YAML Spec**: https://yaml.org/spec/
- **Prettier**: https://prettier.io/

---

**Maintained By**: Project Team
**Last Review**: 2025-11-18
**Next Review**: 2026-02-18
