# Repository Fix Plan - Cursor MCP Integration

**Date**: 2025-11-11  
**Branch**: `chore/repo-fix-cursor-mcp`  
**Target**: `main` (or `master` if main doesn't exist)

---

## Executive Summary

This plan addresses Cursor IDE integration for the EasyPost MCP server, ensuring:
1. Proper `.cursor/mcp.json` configuration for Cursor Desktop
2. Clean Git hygiene (vendor files untracked)
3. Working MCP server entry point
4. Frontend/backend dev workflow via Makefile
5. Type safety and code quality checks

---

## Current State

### Repository Structure
- **Backend**: `apps/backend/` with `src/mcp_server/` layout ✅
- **Frontend**: `apps/frontend/` (Vite + React) ✅
- **MCP Server**: Initialized in `apps/backend/src/mcp_server/__init__.py` ✅
- **Entry Point**: `apps/backend/run_mcp.py` exists ✅

### Issues Found
1. ❌ `.cursor/mcp.json` exists but `mcpServers` is empty
2. ❌ Need to verify vendor files are untracked
3. ⚠️ Frontend directory is `apps/frontend` not `apps/web` (using existing)
4. ⚠️ Current branch is `master`, need to check/create `main`
5. ⚠️ Need to verify `package.json` uses pnpm@9

---

## Remediation Steps

### 1. Git Hygiene ✅
- [x] Verify `.gitignore` contains all vendor patterns
- [x] Verify `.cursorignore` exists and matches
- [ ] Remove any tracked vendor files: `git rm -r --cached apps/backend/venv apps/frontend/node_modules apps/*/dist || true`

### 2. Cursor MCP Configuration
- [ ] Update `.cursor/mcp.json` with proper server config:
  ```json
  {
    "mcpServers": {
      "easypost-mcp": {
        "command": "python3",
        "args": ["-m", "mcp_server.server"],
        "cwd": "apps/backend",
        "env": {
          "EASYPOST_API_KEY": "${env:EASYPOST_API_KEY}"
        }
      }
    }
  }
  ```
- [ ] Create `apps/backend/src/mcp_server/server.py` entry point if needed

### 3. Backend Normalization
- [ ] Verify `apps/backend/pyproject.toml` has correct dependencies
- [ ] Ensure `run_mcp.py` works as entry point
- [ ] Verify MCP server can run standalone

### 4. Frontend Normalization
- [ ] Update root `package.json` to use `pnpm@9` as packageManager
- [ ] Verify `apps/frontend/package.json` is correct

### 5. Makefile Updates
- [ ] Add `setup` target: create venv, install backend, pnpm install frontend
- [ ] Add `dev` target: run backend + frontend concurrently
- [ ] Ensure existing targets work

### 6. Verification
- [ ] Backend: venv setup, type check, import test
- [ ] MCP: Run server smoke test
- [ ] Frontend: Build and dev server test
- [ ] Git: Clean status check

---

## Implementation Checklist

- [x] Create branch `chore/repo-fix-cursor-mcp` from `master`
- [x] Update `.cursor/mcp.json` with server configuration
- [x] Create `apps/backend/src/mcp_server/server.py` entry point
- [x] Update root `package.json` with `packageManager: "pnpm@9.0.0"`
- [x] Update Makefile with `setup` and `dev` targets (using pnpm)
- [x] Verify vendor files are untracked
- [x] Test backend MCP server import
- [x] Test server.py entry point
- [x] Commit changes
- [ ] Push branch and create PR

---

## Expected Outcomes

1. ✅ Cursor Desktop can connect to MCP server via `.cursor/mcp.json`
2. ✅ No vendor files tracked in Git
3. ✅ `make setup` installs all dependencies
4. ✅ `make dev` runs both servers
5. ✅ Type checks pass
6. ✅ Clean Git tree

---

## Notes

- Using existing `apps/frontend` instead of `apps/web` (as specified)
- MCP server entry point: `apps/backend/run_mcp.py` → `src.mcp_server`
- Backend Python version: 3.11+ (currently 3.13 in pyproject.toml)
- Package manager: pnpm@9

