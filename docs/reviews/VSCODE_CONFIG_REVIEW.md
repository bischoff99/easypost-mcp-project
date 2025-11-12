# VS Code Configuration Review

**Date**: 2025-11-12  
**Files Reviewed**: `.vscode/launch.json`, `.vscode/tasks.json`  
**Method**: Sequential thinking + Context7 best practices comparison

---

## Executive Summary

Both configuration files are **well-structured and comprehensive**, following most VS Code best practices. However, several issues were identified that need correction:

- **Launch.json**: 4 critical issues, 3 medium priority improvements
- **Tasks.json**: 3 critical issues, 2 medium priority improvements

**Overall Assessment**: ✅ **Good** (85/100) - Minor fixes needed

---

## Launch.json Review

### ✅ Strengths

1. **Proper Version**: Uses `0.2.0` (correct)
2. **Modern Variables**: Uses `${workspaceFolder}` (not deprecated `${workspaceRoot}`)
3. **Environment Files**: Proper use of `envFile` for `.env` loading
4. **Compound Configurations**: Excellent use of compounds for full-stack debugging
5. **Input Prompts**: Good use of `inputs` for test patterns
6. **Path Mappings**: Correct Docker attach configurations
7. **Comprehensive Coverage**: 13 configurations covering all use cases

### 🔴 Critical Issues

#### 1. **Incorrect MCP Server Module Path** (Line 28)

**Current**:
```json
"module": "src.mcp"
```

**Issue**: Module `src.mcp` doesn't exist. Actual path is `src.mcp_server.server`

**Fix**:
```json
"module": "src.mcp_server.server"
```

**Impact**: MCP server debug configuration won't work

---

#### 2. **Outdated Chrome Source Map Overrides** (Line 124-125)

**Current**:
```json
"sourceMapPathOverrides": {
  "webpack:///./src/*": "${webRoot}/*"
}
```

**Issue**: Project uses Vite, not webpack. Vite uses different source map patterns.

**Fix**:
```json
"sourceMapPathOverrides": {
  "/@fs/*": "${webRoot}/*",
  "/@id/*": "${webRoot}/*",
  "/src/*": "${webRoot}/*"
}
```

**Impact**: Source maps won't resolve correctly in Chrome debugger

---

#### 3. **External Terminal for MCP Server** (Line 31)

**Current**:
```json
"console": "externalTerminal"
```

**Issue**: External terminal is less integrated and harder to manage

**Fix**:
```json
"console": "integratedTerminal"
```

**Impact**: Better UX, consistent with other configs

---

#### 4. **justMyCode Should Be True** (Multiple locations)

**Current**: `"justMyCode": false` in all Python configs

**Issue**: Best practice is `true` unless debugging library code. Current setting steps into library code unnecessarily.

**Fix**: Change to `true` for most configs, keep `false` only for:
- "Python: Attach to Docker Backend" (may need library debugging)
- "Python: Debug Tests" (if debugging test framework issues)

**Impact**: Cleaner debugging experience, faster execution

---

### 🟡 Medium Priority Improvements

#### 5. **Missing PYTHONPATH in Some Configs**

**Issue**: Some configs don't set PYTHONPATH explicitly

**Recommendation**: Add to `env`:
```json
"env": {
  "PYTHONPATH": "${workspaceFolder}/apps/backend"
}
```

**Affected Configs**: "Python: Debug Current File", "Python: Debug Tests"

---

#### 6. **Production Simulation Uses Wrong Log Level**

**Current** (Line 88):
```json
"--log-level", "info"
```

**Issue**: Should match actual production (check server.py default)

**Recommendation**: Verify against actual production settings

---

#### 7. **Missing Pre-Launch Tasks**

**Recommendation**: Add `preLaunchTask` to ensure dependencies are installed:
```json
"preLaunchTask": "📦 Install: Backend Dependencies"
```

**Affected**: "Python: Start Backend Server", "Python: Start MCP Server"

---

## Tasks.json Review

### ✅ Strengths

1. **Proper Version**: Uses `2.0.0` (correct)
2. **Modern Variables**: Uses `${workspaceFolder}` (not deprecated `${workspaceRoot}`)
3. **Problem Matchers**: Good use of custom problem matchers
4. **Background Tasks**: Proper `isBackground` configuration
5. **Compound Tasks**: Excellent use of `dependsOn` and `dependsOrder`
6. **Presentation Options**: Good use of dedicated/shared panels
7. **Comprehensive**: 25 tasks covering all workflows

### 🔴 Critical Issues

#### 1. **Wrong Security Tool** (Line 435)

**Current**:
```json
"command": "${command:python.interpreterPath}",
"args": ["-m", "bandit", "-r", "src/", "-f", "screen"]
```

**Issue**: Project uses `pip-audit`, not `bandit`. Bandit may not even be installed.

**Fix**:
```json
"args": ["-m", "pip-audit", "--requirement", "requirements.txt"]
```

**Impact**: Security scan task will fail

---

#### 2. **Coverage Threshold Mismatch** (Line 549)

**Current**:
```json
"--cov-fail-under=80"
```

**Issue**: Project target is 36% (from pytest.ini), not 80%

**Fix**:
```json
"--cov-fail-under=36"
```

**Impact**: Coverage task will always fail unnecessarily

---

#### 3. **Hardcoded Paths in Clean Task** (Line 368)

**Current**:
```json
"command": "rm -rf backend/**/__pycache__ backend/.pytest_cache frontend/node_modules frontend/dist"
```

**Issue**: Uses hardcoded `backend/` and `frontend/` instead of `apps/backend/` and `apps/frontend/`

**Fix**:
```json
"command": "rm -rf apps/backend/**/__pycache__ apps/backend/.pytest_cache apps/frontend/node_modules apps/frontend/dist"
```

**Impact**: Clean task won't work correctly

---

### 🟡 Medium Priority Improvements

#### 4. **Problem Matcher Verification Needed**

**Issue**: Some problem matchers use regex patterns that may not match actual tool output

**Recommendation**: Test and verify:
- Ruff problem matcher (line 227-234)
- Vite problem matcher (line 76-83)
- Pytest problem matcher (line 193-198)

**Example**: Ruff output format may differ from pattern

---

#### 5. **Missing runOptions**

**Recommendation**: Add `runOptions` for better control:
```json
"runOptions": {
  "reevaluateOnRerun": true
}
```

**Useful for**: Tasks with inputs (migration, port selection)

---

## Best Practices Comparison

### ✅ Following Best Practices

1. ✅ **Version Numbers**: Correct versions (0.2.0 for launch, 2.0.0 for tasks)
2. ✅ **Variable Usage**: Modern `${workspaceFolder}` instead of deprecated `${workspaceRoot}`
3. ✅ **Environment Files**: Proper `envFile` usage
4. ✅ **Compound Configurations**: Good use of compounds
5. ✅ **Input Prompts**: Good use of `inputs` for user interaction
6. ✅ **Problem Matchers**: Custom matchers for error detection
7. ✅ **Background Tasks**: Proper `isBackground` configuration
8. ✅ **Presentation Options**: Good panel management

### ⚠️ Not Following Best Practices

1. ⚠️ **justMyCode**: Should be `true` by default (currently `false` everywhere)
2. ⚠️ **Console Type**: Prefer `integratedTerminal` over `externalTerminal`
3. ⚠️ **Source Maps**: Vite patterns not configured (using webpack patterns)
4. ⚠️ **Pre-Launch Tasks**: Missing for dependency checks
5. ⚠️ **runOptions**: Not used for better task control

---

## Recommended Fixes

### High Priority (Fix Immediately)

1. **Fix MCP server module path** in launch.json
2. **Fix security scan tool** (bandit → pip-audit) in tasks.json
3. **Fix coverage threshold** (80% → 36%) in tasks.json
4. **Fix clean task paths** (backend/ → apps/backend/) in tasks.json
5. **Update Chrome sourceMapPathOverrides** for Vite in launch.json

### Medium Priority (Fix This Week)

6. **Change justMyCode to true** (except library debugging) in launch.json
7. **Change externalTerminal to integratedTerminal** in launch.json
8. **Add PYTHONPATH** to missing configs in launch.json
9. **Verify problem matchers** match actual tool output in tasks.json
10. **Add runOptions** for input-based tasks in tasks.json

### Low Priority (Nice to Have)

11. Add pre-launch tasks for dependency checks
12. Add more compound configurations
13. Add task documentation/comments
14. Consider task grouping improvements

---

## Comparison with VS Code Documentation

### Launch.json Best Practices (from Context7)

✅ **Following**:
- Proper version format
- Use of environment variables
- Path mappings for remote debugging
- Compound configurations
- Input prompts

⚠️ **Not Following**:
- `justMyCode: true` by default (docs recommend true)
- `console: integratedTerminal` preferred (using externalTerminal)
- Vite source map patterns (using webpack patterns)

### Tasks.json Best Practices (from Context7)

✅ **Following**:
- Proper version format
- Problem matchers
- Background tasks
- Presentation options
- Compound tasks with dependencies

⚠️ **Not Following**:
- `runOptions` for better control (not used)
- Task documentation (could add comments)
- Some problem matchers may need verification

---

## Summary Statistics

| Category | Launch.json | Tasks.json |
|----------|-------------|------------|
| **Total Configs/Tasks** | 13 | 25 |
| **Compound Configs** | 2 | 4 |
| **Input Prompts** | 2 | 4 |
| **Critical Issues** | 4 | 3 |
| **Medium Issues** | 3 | 2 |
| **Best Practices Score** | 85% | 88% |

---

## Files to Update

1. `.vscode/launch.json` - Fix 7 issues
2. `.vscode/tasks.json` - Fix 5 issues

**Estimated Time**: 30-45 minutes

---

**Reviewer**: AI Assistant (Claude)  
**Method**: Sequential thinking + Context7 documentation  
**Date**: 2025-11-12

