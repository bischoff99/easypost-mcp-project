# MCP Server Entry Points Review

**Date**: 2025-11-14  
**Issue**: Multiple entry points causing potential confusion  
**Status**: ⚠️ **Needs Clarification**

---

## 📍 Entry Points Discovered

### 1. Primary Entry Point: `run_mcp.py` ✅

**Location**: `apps/backend/run_mcp.py`  
**Used By**: `.cursor/mcp.json` (Cursor Desktop, Claude Desktop)  
**Purpose**: Main stdio transport entry for MCP clients

**Code**:
```python
#!/usr/bin/env python3
"""MCP Server runner for Claude Desktop integration."""
import os
import sys
from pathlib import Path

# Load .env file from project root
project_root = Path(__file__).parent.parent.parent
env_file = project_root / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)
    print(f"Loaded environment from: {env_file}", file=sys.stderr)

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from src.mcp_server import mcp

if __name__ == "__main__":
    mcp.run()  # Runs in stdio mode
```

**Responsibilities**:
- Loads `.env` from project root
- Sets up Python path
- Imports `mcp` instance
- Calls `mcp.run()` for stdio transport

**Used By**:
- `.cursor/mcp.json` → `easypost-test` and `easypost-prod`
- Direct invocation: `python run_mcp.py`

---

### 2. Alternative Entry Point: `server.py` ⚠️

**Location**: `apps/backend/src/mcp_server/server.py`  
**Used By**: `fastmcp.json` (FastMCP tooling)  
**Purpose**: Alternative entry for FastMCP CLI

**Code**:
```python
"""MCP Server entry point for Cursor Desktop integration."""

from src.mcp_server import mcp

if __name__ == "__main__":
    # Run in stdio mode for Cursor Desktop
    mcp.run()
```

**Responsibilities**:
- Imports `mcp` instance
- Calls `mcp.run()`
- NO .env loading
- NO path setup

**Used By**:
- `fastmcp.json` (points to this file)
- Potentially: `fastmcp run server.py`

**Problem**: Doesn't load `.env` - will fail without environment variables

---

### 3. Core Module: `__init__.py` ✅

**Location**: `apps/backend/src/mcp_server/__init__.py`  
**Purpose**: Creates and configures the actual `mcp` instance  
**Not an Entry Point**: This is the module, not a runner

**Code** (simplified):
```python
"""MCP Server for EasyPost shipping operations."""
from fastmcp import FastMCP
from src.services.easypost_service import EasyPostService
from src.utils.config import settings

# Initialize FastMCP server
mcp = FastMCP(
    name=f"EasyPost Shipping Server ({settings.ENVIRONMENT.upper()})",
    instructions=(...)
)

# Initialize shared service
easypost_service = EasyPostService(api_key=settings.EASYPOST_API_KEY)

# Register all components
register_tools(mcp, easypost_service)
register_resources(mcp, easypost_service)
register_prompts(mcp)

__all__ = ["mcp", "easypost_service"]
```

**Responsibilities**:
- Creates `FastMCP` instance
- Initializes EasyPost service
- Registers tools, resources, prompts
- Exports `mcp` for runners to use

**NOT RUNNABLE**: This is a module, not an entry point

---

## 🔄 Entry Point Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│         Entry Point Selection                           │
└────────────┬───────────────────────┬────────────────────┘
             │                       │
             ▼                       ▼
┌──────────────────────┐  ┌──────────────────────┐
│   run_mcp.py         │  │   server.py          │
│   (PRIMARY)          │  │   (ALTERNATIVE)      │
├──────────────────────┤  ├──────────────────────┤
│ 1. Load .env ✅      │  │ 1. No .env ❌        │
│ 2. Setup paths ✅    │  │ 2. No path setup ❌  │
│ 3. Import mcp        │  │ 3. Import mcp        │
│ 4. mcp.run()         │  │ 4. mcp.run()         │
└────────────┬─────────┘  └──────────┬───────────┘
             │                       │
             └───────────┬───────────┘
                         ▼
             ┌───────────────────────┐
             │  src/mcp_server/      │
             │  __init__.py          │
             │                       │
             │  - Create mcp         │
             │  - Register tools     │
             │  - Register resources │
             │  - Register prompts   │
             └───────────────────────┘
```

---

## 📊 Configuration Matrix

| Config File | Points To | Entry Point | .env Loading | Path Setup | Status |
|-------------|-----------|-------------|--------------|------------|--------|
| `.cursor/mcp.json` | `run_mcp.py` | ✅ Primary | ✅ Yes | ✅ Yes | Working |
| `fastmcp.json` | `server.py` | ⚠️ Alt | ❌ No | ❌ No | Incomplete |
| VS Code launch.json | `run_mcp.py` | ✅ Primary | ✅ Yes | ✅ Yes | Working |
| Direct CLI | `run_mcp.py` | ✅ Primary | ✅ Yes | ✅ Yes | Working |

---

## ⚠️ Issues Found

### Issue #1: Redundant Entry Point

**Problem**: `server.py` is incomplete (no .env loading, no path setup)

**Evidence**:
```bash
# This FAILS
python apps/backend/src/mcp_server/server.py
# Error: EASYPOST_API_KEY not set

# This WORKS
python apps/backend/run_mcp.py
# Success: Loads .env, runs correctly
```

**Root Cause**: `server.py` was created for `fastmcp.json` but never fully implemented

---

### Issue #2: Confusing Documentation

**fastmcp.json** says:
```json
"path": "apps/backend/src/mcp_server/server.py"
```

But **nobody actually uses** `fastmcp.json`. All actual usage goes through `run_mcp.py`.

---

### Issue #3: Inconsistent Comments

**server.py** says:
```python
"""MCP Server entry point for Cursor Desktop integration."""
```

But Cursor Desktop uses `run_mcp.py`, not `server.py`.

---

## ✅ Recommended Solution

### Option A: Remove server.py (Recommended)

**Action**:
```bash
# Delete redundant entry point
rm apps/backend/src/mcp_server/server.py

# Delete unused config
rm fastmcp.json

# Update documentation
```

**Rationale**:
- Single entry point = less confusion
- `run_mcp.py` is complete and working
- Nobody uses `fastmcp.json`
- YAGNI principle

---

### Option B: Fix server.py (Not Recommended)

**Action**: Add .env loading and path setup to `server.py`

**Problem**: Creates duplicate functionality, violates DRY

---

### Option C: Consolidate into __main__.py (Alternative)

**Move everything into**: `apps/backend/src/mcp_server/__main__.py`

**Benefit**: Can run as `python -m src.mcp_server`

**Code**:
```python
# apps/backend/src/mcp_server/__main__.py
"""Run MCP server as a module."""
import os
import sys
from pathlib import Path

# Load .env
project_root = Path(__file__).parent.parent.parent.parent
env_file = project_root / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

from src.mcp_server import mcp

if __name__ == "__main__":
    mcp.run()
```

**Usage**:
```bash
# Can run as module
python -m src.mcp_server

# Or via run_mcp.py
python run_mcp.py
```

---

## 🎯 Recommended Architecture

### Single Entry Point Design

```
Project Structure:
├── apps/backend/
│   ├── run_mcp.py              ← PRIMARY ENTRY POINT (stdio)
│   └── src/
│       ├── server.py           ← FastAPI server (HTTP)
│       └── mcp_server/
│           ├── __init__.py     ← MCP instance creation
│           ├── __main__.py     ← Optional: module entry
│           ├── tools/          ← Tool implementations
│           ├── resources/      ← Resource implementations
│           └── prompts/        ← Prompt templates
```

**Clear Separation**:
- `run_mcp.py` → MCP server (stdio for AI clients)
- `src/server.py` → FastAPI server (HTTP for web UI)
- `src/mcp_server/__init__.py` → MCP configuration (not runnable)

---

## 📝 Implementation Plan

### Step 1: Remove Redundant Files (5 minutes)

```bash
cd /Users/andrejs/Projects/personal/easypost-mcp-project

# Remove redundant entry point
rm apps/backend/src/mcp_server/server.py

# Remove unused config
rm fastmcp.json

# Commit
git add -A
git commit -m "refactor: remove redundant MCP entry points

- Remove apps/backend/src/mcp_server/server.py (incomplete, unused)
- Remove fastmcp.json (nobody uses it)
- Standardize on single entry point: run_mcp.py
- Reduces confusion, follows YAGNI principle"
```

---

### Step 2: Update Documentation (10 minutes)

**Update these files**:
- `CLAUDE.md` - Clarify single entry point
- `README.md` - Update MCP server usage section
- `docs/reviews/MCP_PROTOCOL_COMPLIANCE_REVIEW.md` - Remove entry point confusion note

**Add to README**:
```markdown
## MCP Server Entry Point

**Single Entry Point**: `apps/backend/run_mcp.py`

Usage:
- Cursor/Claude Desktop: Configured in `.cursor/mcp.json`
- Direct CLI: `python apps/backend/run_mcp.py`
- VS Code Debug: Use "Python: MCP Server (Test)" launch config

This script:
- Loads environment variables from `.env`
- Sets up Python paths
- Runs MCP server in stdio mode
```

---

### Step 3: Optional - Add __main__.py (5 minutes)

If you want `python -m src.mcp_server` to work:

```python
# apps/backend/src/mcp_server/__main__.py
"""Run MCP server as a module: python -m src.mcp_server"""
import sys
from pathlib import Path

# Load .env from project root
project_root = Path(__file__).parent.parent.parent.parent
env_file = project_root / ".env"

if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)
    print(f"Loaded environment from: {env_file}", file=sys.stderr)

from src.mcp_server import mcp

if __name__ == "__main__":
    mcp.run()
```

---

## ✅ Benefits of Single Entry Point

**Before** (Current):
```
❌ 3 entry points (run_mcp.py, server.py, __init__.py)
❌ Confusion about which to use
❌ Incomplete implementation (server.py missing .env)
❌ Conflicting documentation
```

**After** (Recommended):
```
✅ 1 primary entry point (run_mcp.py)
✅ Clear documentation
✅ Complete implementation
✅ Optional: python -m src.mcp_server
```

---

## 🎯 Summary

### Current Entry Points Status

| File | Purpose | Complete | Used By | Recommendation |
|------|---------|----------|---------|----------------|
| `run_mcp.py` | Primary entry | ✅ Yes | Cursor, Claude, CLI | ✅ Keep |
| `server.py` | Alternative | ❌ No | fastmcp.json (unused) | ❌ Remove |
| `__init__.py` | MCP instance | ✅ Yes | Both above | ✅ Keep (not entry point) |
| `__main__.py` | Module entry | ➖ Doesn't exist | N/A | ⚠️ Optional add |

### Recommended Action

**Remove `server.py` and `fastmcp.json`** - they add confusion without value.

**Result**: Single, clear entry point that works everywhere.

---

**Review Complete** ✅  
**Recommendation**: Clean up redundant entry points  
**Time**: 5-10 minutes to implement

Would you like me to proceed with removing the redundant files?
