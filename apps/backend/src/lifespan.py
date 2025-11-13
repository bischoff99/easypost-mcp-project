"""Application lifespan management for FastMCP + FastAPI integration."""

import asyncio
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass

from src.services.easypost_service import EasyPostService
from src.utils.config import settings

logger = logging.getLogger(__name__)


@dataclass
class AppResources:
    """Shared application resources initialized during lifespan."""

    easypost_service: EasyPostService
    rate_limiter: asyncio.Semaphore


@asynccontextmanager
async def app_lifespan(server):  # noqa: ARG001 - FastAPI lifespan interface
    """
    Manage application startup and shutdown lifecycle.

    Initializes:
    - EasyPost API service (shared across all requests)
    - Rate limiter semaphore (16 concurrent API calls)

    Note: SQLAlchemy pool (for ORM) is configured separately in database.py
    """
    logger.info("Starting EasyPost MCP Server...")

    # Initialize EasyPost service
    easypost_service = EasyPostService(api_key=settings.EASYPOST_API_KEY)
    logger.info("EasyPost service initialized")

    # Database removed for personal use (YAGNI)

    # Initialize rate limiter (16 concurrent EasyPost API calls)
    rate_limiter = asyncio.Semaphore(16)

    # Create resources object
    resources = AppResources(
        easypost_service=easypost_service,
        rate_limiter=rate_limiter,
    )

    try:
        # Yield dict for FastAPI lifespan state (Starlette requirement)
        yield {
            "easypost_service": resources.easypost_service,
            "rate_limiter": resources.rate_limiter,
        }
    finally:
        # Cleanup
        logger.info("Shutting down EasyPost MCP Server...")
        logger.info("Shutdown complete")
