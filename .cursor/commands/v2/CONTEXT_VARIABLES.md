# Context Variables System

Context variables provide intelligent, automatic context detection for slash commands. Use `@` prefix to reference different types of context.

## Available Variables

### File Context

#### `@file`
**Current file in editor**
```bash
/context:explain @file
/quality:optimize @file
/test:run @file
```

**Resolves to**: Absolute path of currently active file

#### `@selection`
**Selected code in editor**
```bash
/context:explain @selection
/quality:fix @selection
/gen:component @selection
```

**Resolves to**: File path + line range (e.g., `auth.py:42-67`)

#### `@open-files`
**All open files in editor**
```bash
/context:improve @open-files
/test:run @open-files
/quality:secure @open-files
```

**Resolves to**: List of open file paths

### Git Context

#### `@git-diff`
**Files with uncommitted changes**
```bash
/test:run @git-diff
/quality:fix @git-diff
/context:explain @git-diff
```

**Resolves to**: List of modified files

#### `@git-status`
**Git working directory status**
```bash
/quality:fix @git-status
```

**Resolves to**: Modified, added, deleted files

#### `@git-staged`
**Staged files only**
```bash
/test:run @git-staged
```

**Resolves to**: Files in staging area

### Error Context

#### `@errors`
**Linter errors in visible files**
```bash
/quality:fix @errors
/context:explain @errors
```

**Resolves to**: Files with lint errors + error details

#### `@tests-failing`
**Currently failing tests**
```bash
/quality:fix @tests-failing
/context:explain @tests-failing
```

**Resolves to**: Test files with failures + failure details

### Project Context

#### `@config`
**Project configuration (.dev-config.json)**
```bash
/context:explain @config
```

**Resolves to**: .dev-config.json file path

#### `@package`
**Package/dependency files**
```bash
/context:explain @package
```

**Resolves to**: package.json, requirements.txt, go.mod, etc.

## Resolution Priority

When multiple variables could apply, priority order:

1. `@selection` (most specific)
2. `@errors` (immediate issue)
3. `@tests-failing` (quality issue)
4. `@file` (current context)
5. `@git-diff` (recent changes)
6. `@open-files` (broader context)

## Auto-Detection

Commands auto-detect context when no argument provided:

```bash
# User has code selected
/quality:fix
# → Resolves to: /quality:fix @selection

# User has linter errors
/quality:fix
# → Resolves to: /quality:fix @errors

# User has file open, no selection
/quality:optimize
# → Resolves to: /quality:optimize @file
```

## Combining Variables

```bash
# Multiple variables (OR logic)
/test:run @selection @git-diff
# Runs tests for selected file OR changed files

# Excluding variables (NOT logic)
/test:run @open-files !@tests-failing
# Test open files except already failing
```

## Smart Resolution Examples

### Example 1: Fix with Selection
```
User selects lines 42-67 in auth.py
User runs: /quality:fix

Resolution:
  @selection → /Users/project/backend/src/auth.py:42-67

AI reads only those lines, fixes specific issue.
```

### Example 2: Test with Git Diff
```
User modifies 3 files:
  - auth.py
  - user_service.py
  - test_auth.py

User runs: /test:run @git-diff

Resolution:
  @git-diff → [auth.py, user_service.py, test_auth.py]

AI finds associated test files:
  - test_auth.py (modified, include)
  - test_user_service.py (found via search, include)

Runs: pytest test_auth.py test_user_service.py
```

### Example 3: Fix Linter Errors
```
Linter reports 5 errors across 2 files:
  - auth.py: 3 errors
  - service.py: 2 errors

User runs: /quality:fix @errors

Resolution:
  @errors → {
    "auth.py": [line 42, 67, 89],
    "service.py": [line 156, 234]
  }

AI fixes each error specifically.
```

## Implementation Details

### Context Provider Interface
```python
class ContextVariable:
    name: str              # Variable name (e.g., "file", "selection")
    priority: int          # Resolution priority (1-10)

    def resolve(self) -> ContextResult:
        """Resolve variable to actual files/data"""
        pass

    def is_available(self) -> bool:
        """Check if context is available"""
        pass
```

### Resolution Process
```python
def resolve_context(command: str, args: List[str]) -> Context:
    # 1. Parse @variables from args
    variables = extract_variables(args)

    # 2. If no variables, auto-detect
    if not variables:
        variables = auto_detect_context(command)

    # 3. Resolve each variable
    context = {}
    for var in variables:
        context[var] = var.resolve()

    # 4. Return resolved context
    return Context(
        files=context.get("files", []),
        selection=context.get("selection"),
        errors=context.get("errors", []),
        metadata=context.get("metadata", {})
    )
```

## Configuration

Add to `.dev-config.json`:
```json
{
  "context": {
    "autoDetect": {
      "enabled": true,
      "priority": ["@selection", "@errors", "@file", "@git-diff"]
    },
    "variables": {
      "@file": {
        "enabled": true,
        "maxSize": "100KB"
      },
      "@open-files": {
        "enabled": true,
        "maxFiles": 10
      },
      "@git-diff": {
        "enabled": true,
        "includeUntracked": false
      }
    }
  }
}
```

## Best Practices

1. **Be Specific**: `@selection` > `@file` > `@open-files`
2. **Use Git Context**: Test only what changed with `@git-diff`
3. **Fix Errors First**: `@errors` immediately shows AI what to fix
4. **Combine Wisely**: `@selection @errors` for targeted fixes
5. **Let AI Auto-Detect**: Often `/command` is enough

## Context Variable Patterns

### Pattern 1: Incremental Testing
```bash
# Edit function
vim auth.py

# Test just that function
/test:run @selection

# Test affected files
/test:run @git-diff

# Full test suite
/test:run
```

### Pattern 2: Targeted Fixes
```bash
# Linter shows errors
npm run lint

# Fix visible errors
/quality:fix @errors

# Fix in current file only
/quality:fix @file

# Fix everything
/quality:fix
```

### Pattern 3: Contextual Explanations
```bash
# Quick explanation of selection
/context:explain @selection

# Explain current file
/context:explain @file

# Explain recent changes
/context:explain @git-diff
```

## Performance Impact

**With Context Variables**:
- Faster: AI only processes relevant code
- Cheaper: Fewer tokens (specific context)
- Accurate: Better understanding of intent

**Without**:
- Slower: AI processes entire codebase
- Expensive: More tokens needed
- Less Accurate: Too much context noise

### Example Token Savings
```
Command: /quality:fix

Without context (full codebase):
  Input: 25,000 tokens
  Time: 15s
  Cost: $0.38

With @selection:
  Input: 1,500 tokens
  Time: 5s
  Cost: $0.02

Savings: 94% tokens, 67% time
```

## Debugging Context Resolution

```bash
# Show what @variable resolves to
/context:debug @selection
# Output: /Users/project/backend/src/auth.py:42-67

/context:debug @git-diff
# Output: [auth.py, service.py, test_auth.py]

/context:debug @errors
# Output: auth.py:42 (undefined variable 'user_id')
#         service.py:156 (missing type hint)
```

## Future Enhancements

- `@ai-suggestions` - Code AI recently suggested
- `@recent-edits` - Last 10 edits
- `@dependencies` - Files that depend on current file
- `@similar` - Similar code patterns in codebase
- `@todos` - Files with TODO comments

