# Virtual Environment Review

**Date:** 2025-11-11  
**Location:** `backend/venv`  
**Status:** ⚠️ Functional but has path issues

---

## Overview

- **Location:** `backend/venv/`
- **Size:** 135 MB
- **Python Version:** 3.14.0
- **Status:** ✅ Functional (Python works, packages installed)
- **Git Status:** ✅ Properly gitignored

---

## Configuration

### pyvenv.cfg

```
home = /opt/homebrew/opt/python@3.14/bin
include-system-site-packages = false
version = 3.14.0
executable = /opt/homebrew/Cellar/python@3.14/3.14.0_1/Frameworks/Python.framework/Versions/3.14/bin/python3.14
command = /opt/homebrew/opt/python@3.14/bin/python3.14 -m venv /Users/andrejs/Developer/github/andrejs/easypost-mcp-project/backend/venv
```

**Issue:** venv was created with old path (`/Users/andrejs/Developer/github/...`) but project is now at `/Users/andrejs/Projects/personal/...`

### Python Version

- **Installed:** Python 3.14.0
- **Status:** ✅ Working
- **Note:** Very new version - ensure all dependencies support it

---

## Package Status

### Installed Packages

✅ **Core packages detected:**
- FastAPI 0.121.0
- FastMCP (installed)
- EasyPost (installed)
- Alembic (installed)
- pytest, black, ruff (installed)

### Package Count

- **Site-packages directories:** ~50+ packages detected
- **Python files:** 4,420 files in venv/lib
- **Status:** ✅ Packages appear installed

---

## Issues Found

### 1. ⚠️ Path Mismatch in pyvenv.cfg

**Problem:** venv was created when project was at:
```
/Users/andrejs/Developer/github/andrejs/easypost-mcp-project
```

**Current location:**
```
/Users/andrejs/Projects/personal/easypost-mcp-project
```

**Impact:** 
- venv still works (uses absolute paths)
- pip scripts may have broken shebangs
- Could cause issues if Python path changes

**Fix:** Recreate venv or update paths

### 2. ⚠️ pip Command Issues

**Problem:** Direct `pip` calls fail with:
```
bad interpreter: /Users/andrejs/Developer/github/.../python3.14: no such file
```

**Workaround:** Use `python -m pip` instead (works correctly)

**Root Cause:** pip scripts have hardcoded old path in shebang

### 3. ⚠️ Dual Python Environments

**Current Setup:**
- `backend/venv/` - 135 MB (project venv)
- `.direnv/python-3.13/` - direnv Python 3.13
- `.direnv/python-3.14/` - direnv Python 3.14

**Conflict:** `.envrc` uses `layout python python3` which creates its own Python environment, but also adds `backend/venv/bin` to PATH.

**Recommendation:** Choose one approach:
- **Option A:** Use direnv's layout python (remove backend/venv)
- **Option B:** Use backend/venv (remove `layout python` from .envrc)

---

## Current Usage

### Makefile Integration

✅ **Working:** Makefile correctly detects and uses `backend/venv/bin`
- VENV_BIN detection works
- All make targets use venv correctly

### direnv Integration

⚠️ **Mixed:** `.envrc` does both:
- `layout python python3` - Creates direnv Python env
- `PATH_add backend/venv/bin` - Adds project venv to PATH

**Result:** Both environments available, but confusing

---

## Recommendations

### Immediate Actions

1. **Fix pip shebang issue:**
   ```bash
   # Recreate venv with correct path
   cd backend
   rm -rf venv
   python3.14 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Resolve direnv conflict:**
   - **Recommended:** Remove `layout python python3` from `.envrc`
   - Keep `PATH_add backend/venv/bin`
   - This uses project venv consistently

### Optional Improvements

3. **Consider Python version:**
   - Python 3.14.0 is very new (released Oct 2024)
   - Consider Python 3.13 or 3.12 for better compatibility
   - Check if all dependencies support 3.14

4. **Cleanup .direnv:**
   ```bash
   # Remove direnv Python environments if not using layout python
   rm -rf .direnv/python-3.13 .direnv/python-3.14
   ```

5. **Verify package installation:**
   ```bash
   cd backend
   source venv/bin/activate
   pip check  # Check for dependency conflicts
   pip list --outdated  # Check for outdated packages
   ```

---

## Health Check

| Check | Status | Notes |
|-------|--------|-------|
| venv exists | ✅ | `backend/venv/` |
| Python works | ✅ | Python 3.14.0 functional |
| Packages installed | ✅ | FastAPI, FastMCP, etc. |
| Git ignored | ✅ | Properly excluded |
| Makefile integration | ✅ | VENV_BIN detection works |
| pip direct calls | ⚠️ | Use `python -m pip` instead |
| Path consistency | ⚠️ | Old path in pyvenv.cfg |
| direnv conflict | ⚠️ | Dual Python environments |

---

## Size Analysis

- **backend/venv:** 135 MB
- **.direnv:** 13 MB
- **Total:** 148 MB

**Breakdown:**
- Python standard library: ~50 MB
- Installed packages: ~85 MB
- Reasonable size for a FastAPI project

---

## Verification Commands

```bash
# Check Python version
backend/venv/bin/python --version

# List packages (use python -m pip)
backend/venv/bin/python -m pip list

# Check specific package
backend/venv/bin/python -c "import fastapi; print(fastapi.__version__)"

# Verify venv is gitignored
git check-ignore backend/venv

# Check venv size
du -sh backend/venv
```

---

## Summary

The venv is **functional** but has **path consistency issues** from a project move. The main problems are:

1. ⚠️ Old path in pyvenv.cfg (cosmetic, doesn't break functionality)
2. ⚠️ pip shebang issues (use `python -m pip` workaround)
3. ⚠️ Dual Python environments (direnv + venv conflict)

**Priority:** Medium - venv works but should be fixed for consistency.

**Recommended Fix:** Recreate venv with correct path and resolve direnv conflict.

