# FastMCP Project Structure

This document describes the project structure following FastMCP guidelines.

## Overview

The project has been restructured to comply with FastMCP best practices while maintaining backward compatibility with existing code.

## Entrypoint Structure

### FastMCP Entrypoint (Primary)

**File**: `src/mcp_server/server.py`

This is the standalone MCP server entrypoint that FastMCP tooling expects. It exports a `mcp` instance that can be used directly by FastMCP clients and tooling.

```python
from src.mcp_server import build_mcp_server

# Build MCP server instance (no lifespan for standalone MCP server)
mcp, _easypost_service = build_mcp_server(lifespan=None)

__all__ = ["mcp"]
```

**Configuration**: `fastmcp.json` points to this file:

```json
{
  "source": {
    "type": "filesystem",
    "path": "src/mcp_server/server.py",
    "entrypoint": "mcp"
  }
}
```

### FastAPI Integration

**File**: `src/server.py`

The FastAPI application builds its own MCP server instance with lifespan support for shared resources:

```python
from src.mcp_server import build_mcp_server

mcp, mcp_service = build_mcp_server(lifespan=app_lifespan)
app.mount("/mcp", mcp.http_app())
```

### Backward Compatibility

**File**: `src/mcp_server/__init__.py`

Maintains exports for backward compatibility:

```python
mcp, easypost_service = build_mcp_server()

__all__ = ["build_mcp_server", "mcp", "easypost_service"]
```

This allows existing code to continue using:
- `from src.mcp_server import mcp`
- `from src.mcp_server import build_mcp_server`

## Project Structure

```
src/
├── mcp_server/
│   ├── __init__.py          # Build function + backward compatibility exports
│   ├── server.py            # FastMCP entrypoint (exports mcp)
│   ├── tools/               # MCP tools registration
│   ├── resources/           # MCP resources registration
│   └── prompts/             # MCP prompts registration
├── server.py                # FastAPI app (mounts MCP server)
└── ...
```

## Usage Patterns

### Standalone MCP Server (FastMCP Tooling)

FastMCP tooling uses `fastmcp.json` to locate the entrypoint:

```bash
# FastMCP automatically uses src/mcp_server/server.py
fastmcp install cursor src/mcp_server/server.py --project .
```

### Claude Desktop Integration

**File**: `scripts/python/run_mcp.py`

Uses the FastMCP entrypoint directly:

```python
from src.mcp_server.server import mcp

if __name__ == "__main__":
    mcp.run()
```

### FastAPI Integration

**File**: `src/server.py`

Builds MCP server with lifespan for shared resources:

```python
from src.mcp_server import build_mcp_server

mcp, mcp_service = build_mcp_server(lifespan=app_lifespan)
app.mount("/mcp", mcp.http_app())
```

### Backward Compatible Imports

Existing scripts can continue using:

```python
from src.mcp_server import mcp, easypost_service
from src.mcp_server import build_mcp_server
```

## FastMCP Guidelines Compliance

✅ **Standalone Entrypoint**: `src/mcp_server/server.py` exports `mcp`
✅ **Configuration**: `fastmcp.json` points to correct entrypoint
✅ **Module Structure**: Tools, resources, prompts organized in subdirectories
✅ **Backward Compatibility**: `__init__.py` maintains existing exports
✅ **FastAPI Integration**: Separate MCP instance with lifespan support

## Key Differences

| Aspect | Old Structure | New Structure |
|--------|---------------|---------------|
| Entrypoint | `src/server.py` (FastAPI app) | `src/mcp_server/server.py` (standalone MCP) |
| FastMCP Config | Pointed to wrong file | Points to correct entrypoint |
| Backward Compat | N/A | Maintained via `__init__.py` |
| FastAPI Integration | Mixed with MCP | Separate instance with lifespan |

## Migration Notes

- ✅ `fastmcp.json` updated to point to `src/mcp_server/server.py`
- ✅ `run_mcp.py` updated to use new entrypoint
- ✅ `verify_mcp_server.py` updated to check new entrypoint
- ✅ Existing imports continue to work via `__init__.py`
- ✅ FastAPI integration unchanged (uses `build_mcp_server`)

## References

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [FastMCP Server Configuration](https://github.com/jlowin/fastmcp/blob/main/docs/deployment/server-configuration.mdx)
- [FastMCP Tutorial](https://github.com/jlowin/fastmcp/blob/main/docs/tutorials/create-mcp-server.mdx)


