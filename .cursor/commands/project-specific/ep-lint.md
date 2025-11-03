Check and fix code quality (linting, formatting, type checking).

**Domain**: Code quality
**Performance**: Parallel linting on M3 Max

## Usage

```bash
# Check all code
/ep-lint

# Fix automatically
/ep-lint --fix

# Backend only
/ep-lint backend

# Frontend only
/ep-lint frontend

# Specific file
/ep-lint src/server.py
```

## What It Does

**Multi-Tool Quality Check:**
1. **Python**: ruff (linter), black (formatter), mypy (type checker)
2. **JavaScript**: eslint (linter), prettier (formatter)
3. **SQL**: sqlfluff (if database queries exist)
4. Runs checks in parallel (3 concurrent processes)

## Tools Used

### Backend (Python)
```bash
# Linting (fast, comprehensive)
ruff check backend/src/

# Formatting
black backend/src/

# Type checking
mypy backend/src/
```

### Frontend (JavaScript)
```bash
# Linting
eslint frontend/src/

# Formatting
prettier --check frontend/src/
```

## MCP Integration

**Server**: Desktop Commander
**Tool**: `start_process` (parallel execution)

**Parallel Execution:**
```python
# Run 3 tools simultaneously
tasks = [
    dc.start_process("ruff check backend/src/"),
    dc.start_process("eslint frontend/src/"),
    dc.start_process("prettier --check frontend/src/")
]
results = await asyncio.gather(*tasks)
```

## Output Format

```
╔═══════════════════════════════════════════════════════════╗
║            EASYPOST CODE QUALITY CHECK                    ║
╚═══════════════════════════════════════════════════════════╝

Running checks in parallel...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BACKEND (Python)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Ruff] Linting...
  ✅ No issues found (287 files checked)

[Black] Formatting...
  ✅ All files formatted correctly

[Mypy] Type checking...
  ⚠️ 3 warnings found:
    backend/src/server.py:145 - Missing return type annotation
    backend/src/mcp/tools/bulk_tools.py:89 - Type mismatch
    backend/src/services/easypost_service.py:203 - Optional[str] expected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FRONTEND (JavaScript)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ESLint] Linting...
  ✅ No issues found (45 files checked)

[Prettier] Formatting...
  ✅ All files formatted correctly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SUMMARY

Total files: 332
Issues found: 3
Auto-fixable: 0
Manual fixes needed: 3

Status: ⚠️ WARNINGS (review type hints)

Duration: 1.2s (parallel execution on M3 Max)
```

## Auto-Fix Mode

With `--fix` flag:

```
╔═══════════════════════════════════════════════════════════╗
║         EASYPOST CODE QUALITY FIX (Auto)                  ║
╚═══════════════════════════════════════════════════════════╝

[Ruff] Auto-fixing...
  ✓ Fixed 12 import sorting issues
  ✓ Fixed 5 unused imports
  ✓ Fixed 3 line length violations

[Black] Auto-formatting...
  ✓ Reformatted 8 files
  ✓ No changes needed: 279 files

[Prettier] Auto-formatting...
  ✓ Reformatted 4 files
  ✓ No changes needed: 41 files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ AUTO-FIX COMPLETE

Fixed: 32 issues
Remaining: 3 (manual fixes needed)

Manual fixes required:
  1. backend/src/server.py:145 - Add return type
  2. backend/src/mcp/tools/bulk_tools.py:89 - Fix type
  3. backend/src/services/easypost_service.py:203 - Handle Optional

Run /ep-lint again to verify fixes
```

## Configuration Files

### Ruff (`backend/pyproject.toml`)
```toml
[tool.ruff]
line-length = 100
target-version = "py312"
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]
```

### Black (`backend/pyproject.toml`)
```toml
[tool.black]
line-length = 100
target-version = ['py312']
```

### ESLint (`frontend/.eslintrc.json`)
```json
{
  "extends": ["react-app", "prettier"],
  "rules": {
    "no-unused-vars": "warn",
    "no-console": "off"
  }
}
```

### Prettier (`frontend/.prettierrc`)
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "printWidth": 100
}
```

## Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Auto-run linting before commits

echo "Running code quality checks..."
/ep-lint --fix

if [ $? -ne 0 ]; then
    echo "❌ Linting failed. Fix issues before committing."
    exit 1
fi

echo "✅ All checks passed!"
```

## IDE Integration

### VS Code Settings
```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true
}
```

## Related Commands

```bash
/ep-lint               # Check quality (this)
/ep-lint --fix         # Auto-fix issues
/ep-test               # Run tests
/fix                   # Universal fix command
```

**Keep code clean - automated quality checks!**

