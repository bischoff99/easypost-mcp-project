"""MCP Server for EasyPost shipping operations."""

from fastmcp import FastMCP

from src.services.easypost_service import EasyPostService
from src.utils.config import settings

# Initialize FastMCP server
mcp = FastMCP(
    name="EasyPost Shipping Server",
    instructions="MCP server for managing shipments and tracking with EasyPost API",
)

# Initialize shared EasyPost service
easypost_service = EasyPostService(api_key=settings.EASYPOST_API_KEY)

# Import and register all components
from src.mcp_server.prompts import register_prompts
from src.mcp_server.resources import register_resources
from src.mcp_server.tools import register_tools

# Register all MCP components
register_tools(mcp, easypost_service)
register_resources(mcp, easypost_service)
register_prompts(mcp)

__all__ = ["mcp", "easypost_service"]
