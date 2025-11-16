"""FastMCP server entrypoint for EasyPost shipping operations.

This module serves as the standalone MCP server entrypoint, following FastMCP guidelines.
The `mcp` instance is exported here for use by FastMCP tooling and clients.

For FastAPI integration, see src/server.py which mounts this MCP server.
"""

from __future__ import annotations

from src.mcp_server import build_mcp_server

# Build MCP server instance (no lifespan for standalone MCP server)
# Lifespan is only used when integrated with FastAPI
mcp, _easypost_service = build_mcp_server(lifespan=None)

# Export mcp as the entrypoint for FastMCP tooling
__all__ = ["mcp"]
