# Cursor IDE Crash Analysis & Fixes

## Critical Issues Found & Fixed

### 1. ❌ Python Language Server Misconfiguration (CRITICAL)
**Problem:** `python.languageServer` was set to `"None"` instead of `"Pylance"`
- **Impact:** Cursor was trying to use a non-existent language server, causing crashes
- **Fix:** Changed to `"Pylance"` (Microsoft's official Python language server)
- **Location:** `.vscode/settings.json` line 58

### 2. ❌ Excessive Python Cache Files
**Problem:** 5,333 `__pycache__` directories found
- **Impact:** File watcher overload, high memory usage, slow indexing
- **Fix:** Removed all `__pycache__` directories and `.pyc` files
- **Prevention:** Already excluded in `files.watcherExclude`

### 3. ⚠️ Incomplete File Watcher Exclusions
**Problem:** Missing exclusions for test coverage and cache directories
- **Impact:** File watcher monitoring unnecessary files, consuming resources
- **Fix:** Added exclusions for:
  - `.pytest_cache/**`
  - `.mypy_cache/**`
  - `.ruff_cache/**`
  - `htmlcov/**`
  - `coverage/**`
  - `*.pyc`
  - `.DS_Store`

## Current Resource Usage

- **Project Size:** 627MB total
- **Python venv:** 139MB
- **Node modules:** 15MB
- **Total Files:** ~41,250 (excluding .git)
- **Cursor Renderer Memory:** ~750MB
- **Cursor Plugin Host Memory:** ~543MB

## Recommendations

1. **Restart Cursor IDE** to apply language server change
2. **Monitor memory usage** - if crashes persist, check:
   - Extensions consuming memory
   - Large files being indexed
   - Background processes
3. **Disable unused extensions** if crashes continue
4. **Clear workspace storage** if needed:
   ```bash
   rm -rf ~/Library/Application\ Support/Cursor/User/workspaceStorage/*
   ```

## Settings Applied

All fixes are in `.vscode/settings.json`:
- ✅ Python language server: `Pylance`
- ✅ Enhanced file watcher exclusions
- ✅ Proper cache directory exclusions

## Next Steps

1. Restart Cursor IDE
2. Verify Python IntelliSense works (should see type hints)
3. Monitor for crashes - should be resolved
4. If crashes persist, check Cursor logs:
   ```bash
   log show --predicate 'process == "Cursor"' --last 1h
   ```
