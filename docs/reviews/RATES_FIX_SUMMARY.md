# Rates Issue - Root Cause & Fix

## Problem
`parse_and_get_bulk_rates` was returning empty rates despite valid EasyPost API key.

## Root Cause Analysis (Sequential Thinking)

### Discovery Process
1. **Initial observation**: Rates array empty in parse_and_get_bulk_rates response
2. **API key verification**: Confirmed key works directly with EasyPost SDK
3. **Architecture analysis**: Found TWO separate MCP instances:
   - **stdio mode** (`run_mcp.py` → `__init__.py`): Used by Cursor MCP connection
   - **HTTP mode** (`server.py`): Used by web server

### The Core Issue
```python
# __init__.py (stdio mode for Cursor)
easypost_service = EasyPostService(api_key=settings.EASYPOST_API_KEY)  # Line 15
register_tools(mcp, easypost_service)  # Line 23 - passes service

# server.py (HTTP mode)
register_tools(mcp, None)  # Line 196 - passes None, expects context
```

**Problem**: Tools need to access `easypost_service`, but the access pattern differed between modes:
- **stdio mode**: Service passed as parameter to `register_bulk_tools`
- **HTTP mode**: Service stored in lifespan context

My initial fix attempted to access from context only, breaking stdio mode.

## Solution Implemented

Updated `parse_and_get_bulk_rates` in `bulk_tools.py` to use **dual-mode access pattern**:

```python
# Get service from closure parameter (stdio mode) or context (HTTP mode)
service = easypost_service  # Try closure first (stdio)
if service is None and ctx:
    # Fallback to context (HTTP mode)
    lifespan_ctx = ctx.request_context.lifespan_context
    service = (
        lifespan_ctx.get("easypost_service")
        if isinstance(lifespan_ctx, dict)
        else lifespan_ctx.easypost_service
    )

if not service:
    return error_response("EasyPost service not initialized")
```

### Why This Works
- **stdio mode** (Cursor): Uses `easypost_service` from closure scope
- **HTTP mode** (FastAPI): Falls back to context when closure is None
- **Error handling**: Returns clear error if neither method works

## Next Steps

### 1. Restart Cursor
The MCP server runs as a subprocess of Cursor. To load the fixes:

```bash
# Quit Cursor completely
# Reopen Cursor
```

This will:
- Reload the fixed `bulk_tools.py` code
- Re-initialize MCP server with new API key from `.env`
- Reconnect stdio transport

### 2. Test the Fix
After restart:

```bash
# Test with your data
parse_and_get_bulk_rates(spreadsheet_data)
```

Expected: Rates populated with actual shipping options from EasyPost

## API Key Configuration

API key successfully added to `.env`:
```bash
EASYPOST_API_KEY=your_production_api_key_here
```

Verified working with direct SDK test (address creation successful).

## Files Modified
- `/backend/src/mcp_server/tools/bulk_tools.py` - Fixed service access pattern
- `/backend/.env` - Added valid API key

## Architecture Insight

This issue revealed an important architectural pattern:

**MCP tools must support both access patterns:**
1. **Closure scope** (parameter passed to register function)
2. **Context scope** (lifespan context for HTTP mode)

The solution: Try closure first, fallback to context. This ensures tools work in both stdio (Cursor MCP) and HTTP (web API) modes.
