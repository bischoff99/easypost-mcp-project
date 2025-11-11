# Cursor Settings Comparison

**Current vs. Official Recommendations**  
**Date**: November 11, 2025  
**Sources**: Official repositories only (Trust Score ≥9.0)

---

## Comparison Overview

| Category | Current Status | Official Recommendation | Priority |
|----------|---------------|------------------------|----------|
| Python Language Server | ❌ "None" (disabled) | ✅ "Pylance" | 🔴 Critical |
| Security Settings | ❌ Missing | ✅ Required | 🔴 Critical |
| Format on Save | ❌ Not configured | ✅ Standard practice | 🟡 High |
| Auto-save Mode | ⚠️ "afterDelay" | ✅ "onFocusChange" | 🟢 Medium |
| File Exclusions | ❌ Not configured | ✅ Performance benefit | 🟢 Medium |
| Editor Rulers | ❌ Not configured | ✅ Visual guidance | 🟢 Low |
| Python Analysis | ❌ Not configured | ✅ Enhanced features | 🟢 Low |

---

## Detailed Comparison

### 1. Python Language Server

#### Current Setting

```json
{
  "python.languageServer": "None"
}
```

**Status**: ❌ **CRITICAL ISSUE**

**Impact**:
- No code completion (IntelliSense)
- No type checking
- No go-to-definition
- No find references
- No import suggestions
- No error detection
- No hover documentation

#### Official Recommendation

**Source**: `/microsoft/pylance-release` (Trust Score: 9.9)

```json
{
  "python.languageServer": "Pylance"
}
```

**Benefits**:
- ✅ Full IntelliSense support
- ✅ Type checking with configurable modes
- ✅ Auto-import completions
- ✅ Parameter hints
- ✅ Error detection
- ✅ Code navigation (go-to-definition, find references)

**Priority**: 🔴 **Critical** - Apply immediately

---

### 2. Security Settings

#### Current Setting

```json
{}  // Not configured
```

**Status**: ❌ **Missing official recommendation**

#### Official Recommendation

**Source**: `/getcursor/docs` - Agent Security Documentation

```json
{
  "security.workspace.trust.enabled": true
}
```

**Benefits**:
- ✅ Protects against untrusted code execution
- ✅ Prompts when opening new workspaces
- ✅ Prevents unauthorized file modifications
- ✅ Guards against prompt injections

**Priority**: 🔴 **Critical** - Official Cursor security recommendation

---

### 3. Format on Save

#### Current Setting

```json
{}  // Not configured
```

**Status**: ❌ **Not configured**

**Impact**:
- Manual formatting required
- Inconsistent code style
- No automatic cleanup

#### Official Recommendation

**Source**: `/microsoft/vscode-docs` (Trust Score: 9.9)

```json
{
  "editor.formatOnSave": true,
  "editor.formatOnPaste": true
}
```

**Benefits**:
- ✅ Automatic code formatting
- ✅ Consistent style across team
- ✅ Cleaner commits (no formatting-only changes)

**Priority**: 🟡 **High** - Standard practice across all projects

---

### 4. Auto-save Configuration

#### Current Setting

```json
{
  "files.autoSave": "afterDelay"
}
```

**Status**: ⚠️ **Works, but not optimal**

**Behavior**:
- Saves after a delay (default 1000ms)
- Saves even when not switching context
- Can interrupt typing flow

#### Official Recommendation

**Source**: `/microsoft/vscode-docs` (Trust Score: 9.9)

```json
{
  "files.autoSave": "onFocusChange"
}
```

**Benefits**:
- ✅ More intuitive (saves when switching files/apps)
- ✅ Doesn't interrupt typing
- ✅ Clearer mental model

**Priority**: 🟢 **Medium** - Quality of life improvement

---

### 5. Python Analysis Settings

#### Current Setting

```json
{}  // Not configured
```

**Status**: ❌ **Missing Pylance features**

**Impact**:
- Basic IntelliSense only (when not "None")
- No type hints displayed
- No auto-import suggestions
- No function parameter completion

#### Official Recommendation

**Source**: `/microsoft/pylance-release` (Trust Score: 9.9)

```json
{
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.completeFunctionParens": true,
  "python.analysis.inlayHints.functionReturnTypes": true,
  "python.analysis.inlayHints.variableTypes": true
}
```

**Benefits**:
- ✅ Type checking for error prevention
- ✅ Auto-import suggestions
- ✅ Automatic parentheses for functions
- ✅ Inline type hints for better understanding

**Priority**: 🟢 **Medium** - Enhanced development experience

---

### 6. File Exclusion Patterns

#### Current Setting

```json
{}  // Not configured
```

**Status**: ❌ **Not configured**

**Impact**:
- Slower file tree rendering
- Unnecessary file system monitoring
- Cluttered search results
- Reduced performance with large projects

#### Official Recommendation

**Source**: `/microsoft/vscode-docs` (Trust Score: 9.9)

```json
{
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true,
    "**/.mypy_cache": true,
    "**/.ruff_cache": true,
    "**/node_modules": true,
    "**/.venv": true,
    "**/venv": true,
    "**/dist": true,
    "**/build": true
  },
  "files.watcherExclude": {
    "**/__pycache__/**": true,
    "**/.venv/**": true,
    "**/node_modules/**": true,
    "**/.git/objects/**": true,
    "**/dist/**": true,
    "**/build/**": true
  },
  "search.exclude": {
    "**/__pycache__": true,
    "**/.venv": true,
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true
  }
}
```

**Benefits**:
- ✅ Faster file operations
- ✅ Reduced memory usage
- ✅ Cleaner search results
- ✅ Better performance on large projects

**Priority**: 🟢 **Medium** - Performance optimization

---

### 7. Editor Visual Guides

#### Current Setting

```json
{}  // Not configured
```

**Status**: ❌ **Not configured**

**Impact**:
- No visual guide for line length
- Inconsistent line lengths
- Harder to maintain style guide compliance

#### Official Recommendation

**Source**: `/microsoft/vscode-docs` (Trust Score: 9.9) + Project standard

```json
{
  "editor.rulers": [100]
}
```

**Benefits**:
- ✅ Visual guidance at 100 characters (project standard)
- ✅ Helps maintain consistent line lengths
- ✅ Aligns with project's pyproject.toml (line-length = 100)

**Priority**: 🟢 **Low** - Visual guidance

---

### 8. Bracket Colorization

#### Current Setting

```json
{}  // Not configured
```

**Status**: ❌ **Not configured**

#### Official Recommendation

**Source**: `/microsoft/vscode-docs` (Trust Score: 9.9)

```json
{
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true
}
```

**Benefits**:
- ✅ Color-coded matching brackets
- ✅ Vertical guides for bracket pairs
- ✅ Easier to read nested code
- ✅ Faster visual navigation

**Priority**: 🟢 **Low** - Quality of life

---

### 9. Language-Specific Formatting

#### Current Setting

```json
{}  // Not configured
```

**Status**: ❌ **Not configured**

**Impact**:
- No automatic formatter selection
- Manual formatting configuration per file
- Inconsistent formatting across languages

#### Official Recommendation

**Source**: `/microsoft/vscode-docs` (Trust Score: 9.9)

```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.tabSize": 4,
    "editor.rulers": [100],
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true,
    "editor.tabSize": 2,
    "editor.rulers": [100]
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true,
    "editor.tabSize": 2,
    "editor.rulers": [100]
  }
}
```

**Benefits**:
- ✅ Automatic formatter selection per language
- ✅ Consistent tab sizes (4 for Python, 2 for JS)
- ✅ Auto-organize imports (Python)
- ✅ Format on save per language

**Priority**: 🟢 **Medium** - Language-specific best practices

---

## Settings That Are Already Correct

### ✅ Cursor-Specific Settings

**Current**:
```json
{
  "cursor.terminal.usePreviewBox": true,
  "cursor.composer.shouldAllowCustomModes": true,
  "cursor.cpp.enablePartialAccepts": true
}
```

**Status**: ✅ **Correct** - Aligns with Cursor documentation

**Source**: `/getcursor/docs`

---

### ✅ Makefile Integration

**Current**:
```json
{
  "makefile.configureOnOpen": true
}
```

**Status**: ✅ **Correct** - Appropriate for project

---

### ✅ GitLens AI Configuration

**Current**:
```json
{
  "gitlens.ai.model": "ollama:llama-fast-custom:latest",
  "gitlens.ai.gitkraken.model": "gemini:gemini-2.0-flash",
  "gitlens.ai.ollama.url": "http://localhost:11434"
}
```

**Status**: ✅ **Correct** - Privacy-focused (local Ollama)

**Benefits**:
- ✅ No external API calls
- ✅ Data stays local
- ✅ Properly configured

---

### ✅ Builder Settings

**Current**:
```json
{
  "builder.serverUrl": "http://localhost:5173",
  "builder.command": "make dev",
  "builder.openInBrowser": false
}
```

**Status**: ✅ **Correct** - Aligned with project's Makefile

**Benefits**:
- ✅ Matches frontend port (5173)
- ✅ Uses project's dev command
- ✅ Appropriate browser behavior

---

## Summary Table

### Changes Needed

| Setting | Current | Recommended | Source | Priority |
|---------|---------|------------|--------|----------|
| `python.languageServer` | `"None"` | `"Pylance"` | microsoft/pylance-release | 🔴 Critical |
| `security.workspace.trust.enabled` | Missing | `true` | getcursor/docs | 🔴 Critical |
| `editor.formatOnSave` | Missing | `true` | microsoft/vscode-docs | 🟡 High |
| `files.autoSave` | `"afterDelay"` | `"onFocusChange"` | microsoft/vscode-docs | 🟢 Medium |
| `python.analysis.*` | Missing | Configure | microsoft/pylance-release | 🟢 Medium |
| `files.exclude` | Missing | Configure | microsoft/vscode-docs | 🟢 Medium |
| `editor.rulers` | Missing | `[100]` | Project standard | 🟢 Low |
| `editor.bracketPairColorization.enabled` | Missing | `true` | microsoft/vscode-docs | 🟢 Low |
| Language-specific formatting | Missing | Configure | microsoft/vscode-docs | 🟢 Medium |

### Settings to Keep

| Setting | Value | Source | Status |
|---------|-------|--------|--------|
| `cursor.terminal.usePreviewBox` | `true` | getcursor/docs | ✅ Correct |
| `cursor.composer.shouldAllowCustomModes` | `true` | getcursor/docs | ✅ Correct |
| `cursor.cpp.enablePartialAccepts` | `true` | getcursor/docs | ✅ Correct |
| `makefile.configureOnOpen` | `true` | Extension | ✅ Correct |
| `gitlens.ai.*` | Local Ollama | Extension | ✅ Correct |
| `builder.*` | Project-specific | Extension | ✅ Correct |

---

## Implementation Recommendations

### Minimal Fix (Critical Only)

**Change these 2 settings**:

```json
{
  "python.languageServer": "Pylance",  // Change from "None"
  "security.workspace.trust.enabled": true  // Add
}
```

**Reload Cursor**: `Cmd + Shift + P` → "Reload Window"

---

### Recommended Full Update

Apply all recommendations from the official sources comparison table. See `.cursor/recommended-settings-official.json` for complete configuration.

---

## Verification Steps

### 1. Verify Python IntelliSense Works

```python
# Type this in a .py file:
import 
# You should see autocomplete suggestions
```

### 2. Verify Format on Save

```python
# Type poorly formatted code and save:
def test(  ):pass
# Should auto-format to:
def test():
    pass
```

### 3. Verify File Exclusions

- Open file explorer
- Verify `__pycache__`, `.venv`, `node_modules` are hidden

### 4. Verify Security Setting

- Open a new workspace
- Should see workspace trust prompt

---

## Sources Referenced

All comparisons based on:
- ✅ Official Cursor docs (`/getcursor/docs`)
- ✅ Microsoft Pylance (`/microsoft/pylance-release`, Trust: 9.9)
- ✅ Microsoft VS Code Python (`/microsoft/vscode-python`, Trust: 9.9)
- ✅ Microsoft VS Code (`/microsoft/vscode`, Trust: 9.9)
- ✅ Microsoft VS Code Docs (`/microsoft/vscode-docs`, Trust: 9.9)

**No unofficial sources used.**

---

**Report Date**: November 11, 2025  
**Status**: ✅ Complete comparison with official sources only



