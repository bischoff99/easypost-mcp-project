"""MCP Server for EasyPost shipping operations."""

import logging

from fastmcp import FastMCP

from src.services.easypost_service import EasyPostService
from src.utils.config import settings

logger = logging.getLogger(__name__)

# Log environment on startup
if settings.ENVIRONMENT == "production":
    logger.warning("⚠️  MCP SERVER RUNNING IN PRODUCTION MODE - Real API calls will be made!")
    logger.warning(f"⚠️  Using API key: {settings.EASYPOST_API_KEY[:15]}...")
else:
    logger.info(f"✓ MCP Server running in {settings.ENVIRONMENT.upper()} mode")
    logger.info(f"✓ Using API key: {settings.EASYPOST_API_KEY[:15]}...")

# Initialize FastMCP server
mcp = FastMCP(
    name=f"EasyPost Shipping Server ({settings.ENVIRONMENT.upper()})",
    instructions=(
        f"MCP server for managing shipments and tracking with EasyPost API. "
        f"Environment: {settings.ENVIRONMENT}"
    ),
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
