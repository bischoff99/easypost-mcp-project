"""MCP Server for EasyPost shipping operations."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator, Callable

from fastmcp import FastMCP

from src.mcp_server.prompts import register_prompts
from src.mcp_server.resources import register_resources
from src.mcp_server.tools import register_tools
from src.services.easypost_service import EasyPostService
from src.utils.config import settings

logger = logging.getLogger(__name__)

LifespanHook = Callable[[FastMCP], AsyncIterator[dict]]


def build_mcp_server(
    *, lifespan: LifespanHook | None = None, name_suffix: str | None = None
) -> tuple[FastMCP, EasyPostService]:
    """
    Construct a fully registered FastMCP server instance.

    Args:
        lifespan: Optional lifespan hook shared with FastAPI.
        name_suffix: Optional override for server name suffix (defaults to environment).

    Returns:
        Tuple of (FastMCP instance, EasyPost service) ready for execution.
    """
    environment = settings.ENVIRONMENT.upper()
    suffix = name_suffix or environment

    if settings.ENVIRONMENT == "production":
        logger.warning("MCP server starting in PRODUCTION mode – real EasyPost requests will run.")
    else:
        logger.info("MCP server starting in %s mode", environment)

    mcp_instance = FastMCP(
        name=f"EasyPost Shipping Server ({suffix})",
        instructions=(
            "MCP server for managing shipments and tracking with EasyPost API. "
            f"Environment: {settings.ENVIRONMENT}"
        ),
        lifespan=lifespan,
    )

    easypost_service = EasyPostService(api_key=settings.EASYPOST_API_KEY)

    register_tools(mcp_instance, easypost_service)
    register_resources(mcp_instance, easypost_service)
    register_prompts(mcp_instance)

    return mcp_instance, easypost_service


mcp, easypost_service = build_mcp_server()

__all__ = ["build_mcp_server", "mcp", "easypost_service"]
