# Prettier Configuration Review

**Date**: 2025-11-12
**Files Reviewed**: `.prettierrc`, `.prettierignore`, `apps/frontend/.prettierignore`
**Reference**: [Prettier Configuration Documentation](https://prettier.io/docs/configuration)

---

## Current Configuration

### `.prettierrc` (Root)

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf",
  "bracketSpacing": true,
  "jsxSingleQuote": false,
  "bracketSameLine": false
}
```

### `.prettierignore` (Root)

- Dependencies (node_modules, .pnp)
- Build outputs (dist, build, .next, out, .nuxt, .cache)
- Lock files (package-lock.json, pnpm-lock.yaml, yarn.lock)
- Coverage (coverage, .nyc_output)
- Logs (*.log, npm-debug.log*, etc.)
- Environment files (.env*)
- IDE files (.vscode, .idea)
- OS files (.DS_Store, Thumbs.db)
- Python files (__pycache__, *.pyc, venv, .venv, htmlcov, .pytest_cache, .mypy_cache, .ruff_cache)
- Generated files (*.min.js, *.min.css)

### `apps/frontend/.prettierignore`

- node_modules
- dist
- build
- coverage
- .vite
- *.log
- package-lock.json

---

## Analysis

### ✅ Strengths

1. **Good Defaults**: Most settings are sensible defaults
2. **Consistent Line Endings**: `endOfLine: "lf"` ensures cross-platform consistency
3. **Modern Settings**: Uses `trailingComma: "es5"` for better git diffs
4. **JSX Configuration**: Proper JSX settings (`jsxSingleQuote: false`, `bracketSameLine: false`)
5. **Comprehensive Ignore**: Root `.prettierignore` covers most common patterns

### ⚠️ Issues Found

#### 1. **Deprecated Option: `bracketSameLine`**

**Current**: `"bracketSameLine": false`

**Issue**: This option was renamed in Prettier 2.4.0. The correct option is `jsxBracketSameLine` (which is what you have), but `bracketSameLine` is deprecated and may cause warnings.

**Status**: Actually, `bracketSameLine` is the new name (since Prettier 2.4.0), and `jsxBracketSameLine` is deprecated. Your config is correct! ✅

**Note**: Prettier 2.4.0+ uses `bracketSameLine` (not `jsxBracketSameLine`). Your config is correct.

#### 2. **Redundant Ignore Files**

**Issue**: Two `.prettierignore` files (root and `apps/frontend/`)

**Analysis**:
- Root `.prettierignore` is comprehensive
- Frontend `.prettierignore` is mostly redundant
- Frontend-specific: `.vite` (not in root)

**Recommendation**:
- Keep root `.prettierignore` (covers everything)
- Add `.vite` to root `.prettierignore`
- Remove `apps/frontend/.prettierignore` (redundant)

#### 3. **Missing File Extensions**

**Current**: Frontend format script only formats `js,jsx,json,css`

**Missing**:
- TypeScript files (`.ts`, `.tsx`) - if using TypeScript
- Markdown files (`.md`)
- YAML files (`.yaml`, `.yml`)
- JSON files in root (package.json, etc.)

**Recommendation**: Expand format script to include all relevant file types

#### 4. **Pre-commit Hook Limitation**

**Current**: Pre-commit hook only formats YAML files

**Issue**: Prettier should format JavaScript/JSX files before commit, not just YAML

**Recommendation**: Add Prettier hook for JS/JSX files (or use lint-staged)

#### 5. **No Override Configurations**

**Issue**: No file-specific overrides (e.g., different settings for JSON vs JS)

**Recommendation**: Consider adding overrides for specific file types if needed

#### 6. **Missing Schema Reference**

**Issue**: No `$schema` attribute for IntelliSense

**Recommendation**: Add `$schema` for better IDE support (optional but helpful)

---

## Recommended Improvements

### 1. Consolidate Ignore Files

**Action**:
- Add `.vite` to root `.prettierignore`
- Remove `apps/frontend/.prettierignore`

**Reason**: Single source of truth, easier maintenance

### 2. Expand Format Script

**Current**:
```json
"format": "prettier --write \"src/**/*.{js,jsx,json,css}\""
```

**Recommended**:
```json
"format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,json,css,md}\" \"*.{json,md}\""
```

**Reason**: Format all relevant file types, including root config files

### 3. Add Pre-commit Hook for JS/JSX

**Current**: Only YAML files formatted in pre-commit

**Recommended**: Add Prettier hook for JavaScript files:

```yaml
- repo: https://github.com/pre-commit/mirrors-prettier
  rev: v4.0.0-alpha.8
  hooks:
    - id: prettier
      files: \.(js|jsx|json|css|md)$
      exclude: |
        (?x)^(
          .*\.lock$|
          node_modules/.*|
          venv/.*|
          \.venv/.*|
          dist/.*|
          build/.*
        )
```

**Reason**: Ensure all code is formatted before commit

### 4. Add Schema Reference (Optional)

**Action**: Add `$schema` to `.prettierrc`:

```json
{
  "$schema": "https://json.schemastore.org/prettierrc.json",
  ...
}
```

**Reason**: Better IntelliSense and validation in VS Code

### 5. Consider File-Specific Overrides

**Example**: Different settings for JSON files:

```json
{
  "overrides": [
    {
      "files": "*.json",
      "options": {
        "printWidth": 120
      }
    }
  ]
}
```

**Reason**: Some file types benefit from different settings

---

## Best Practices Comparison

### ✅ Following Best Practices

1. ✅ **Consistent Configuration**: Single config file at root
2. ✅ **Line Endings**: Explicit `endOfLine: "lf"` for cross-platform
3. ✅ **Trailing Commas**: Using `es5` for better git diffs
4. ✅ **Comprehensive Ignore**: Good coverage of build artifacts
5. ✅ **Modern Options**: Using current Prettier options

### ⚠️ Not Following Best Practices

1. ⚠️ **Pre-commit Integration**: Only formatting YAML, not JS/JSX
2. ⚠️ **Format Script Scope**: Limited file types in format script
3. ⚠️ **Redundant Config**: Two ignore files
4. ⚠️ **No Schema Reference**: Missing `$schema` for IntelliSense

---

## Configuration Details

### Current Settings Explained

| Option | Value | Meaning |
|--------|-------|---------|
| `semi` | `true` | Add semicolons at end of statements |
| `trailingComma` | `"es5"` | Add trailing commas where valid in ES5 (objects, arrays, etc.) |
| `singleQuote` | `true` | Use single quotes instead of double quotes |
| `printWidth` | `100` | Wrap lines at 100 characters (default: 80) |
| `tabWidth` | `2` | Use 2 spaces for indentation |
| `useTabs` | `false` | Use spaces, not tabs |
| `arrowParens` | `"always"` | Always include parentheses around arrow function parameters |
| `endOfLine` | `"lf"` | Use LF line endings (Unix-style) |
| `bracketSpacing` | `true` | Add spaces inside object brackets `{ foo: bar }` |
| `jsxSingleQuote` | `false` | Use double quotes in JSX |
| `bracketSameLine` | `false` | Put closing bracket on new line in JSX |

### Alignment with Project Standards

**Python Backend**: Uses Ruff (not Prettier) - ✅ Correct
**Frontend**: Uses Prettier - ✅ Correct
**YAML**: Uses Prettier in pre-commit - ✅ Correct
**Line Length**: 100 chars (matches Python Ruff config) - ✅ Consistent

---

## Recommendations Summary

### High Priority

1. **Consolidate ignore files** - Remove redundant frontend ignore file
2. **Expand format script** - Include all relevant file types
3. **Add Prettier to pre-commit** - Format JS/JSX files before commit

### Medium Priority

4. **Add schema reference** - Better IDE support
5. **Consider file overrides** - Different settings for different file types

### Low Priority

6. **Document configuration** - Add comments explaining choices
7. **Add format:check script** - Verify formatting without changing files

---

## Comparison with Industry Standards

### Common Prettier Configurations

**React Projects** (typical):
- `printWidth: 80` (default)
- `singleQuote: true` ✅
- `trailingComma: "es5"` ✅
- `semi: true` ✅

**Your Config**:
- `printWidth: 100` (wider, matches Python style)
- `singleQuote: true` ✅
- `trailingComma: "es5"` ✅
- `semi: true` ✅

**Verdict**: Your config is modern and appropriate for a monorepo with Python backend (100 char width matches Ruff).

---

## Files to Update

1. `.prettierrc` - Add schema reference (optional)
2. `.prettierignore` - Add `.vite` pattern
3. `apps/frontend/.prettierignore` - Remove (redundant)
4. `apps/frontend/package.json` - Expand format script
5. `.pre-commit-config.yaml` - Add Prettier hook for JS/JSX

---

## References

- [Prettier Configuration](https://prettier.io/docs/configuration)
- [Prettier Options](https://prettier.io/docs/options)
- [Prettier Ignore Files](https://prettier.io/docs/ignore)
- [Prettier Schema Store](https://json.schemastore.org/prettierrc.json)

---

**Reviewer**: AI Assistant (Claude)
**Date**: 2025-11-12
**Status**: Ready for implementation
