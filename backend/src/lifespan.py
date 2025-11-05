"""Application lifespan management for FastMCP + FastAPI integration."""

import asyncio
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass

import asyncpg

from src.services.easypost_service import EasyPostService
from src.utils.config import settings

logger = logging.getLogger(__name__)


@dataclass
class AppResources:
    """Shared application resources initialized during lifespan."""

    easypost_service: EasyPostService
    db_pool: asyncpg.Pool | None
    rate_limiter: asyncio.Semaphore


@asynccontextmanager
async def app_lifespan(server):  # noqa: ARG001 - FastAPI lifespan interface
    """
    Manage application startup and shutdown lifecycle.

    Initializes:
    - EasyPost API service (shared across all requests)
    - Database connection pool (32 connections for M3 Max)
    - Rate limiter semaphore (16 concurrent API calls)
    """
    logger.info("Starting EasyPost MCP Server...")

    # Initialize EasyPost service
    easypost_service = EasyPostService(api_key=settings.EASYPOST_API_KEY)
    logger.info("EasyPost service initialized")

    # Initialize database pool (if DATABASE_URL is configured)
    db_pool = None
    if hasattr(settings, "DATABASE_URL") and settings.DATABASE_URL:
        try:
            # Convert SQLAlchemy-style URL to asyncpg format
            db_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
            db_pool = await asyncpg.create_pool(
                db_url,
                min_size=2,  # Start small to avoid connection exhaustion
                max_size=20,  # Conservative max for multiple workers
                max_inactive_connection_lifetime=300,  # 5 min idle timeout
                command_timeout=60,
                timeout=10,  # Connection acquire timeout
            )
            logger.info(
                f"Database pool created: {db_pool.get_size()} connections "
                f"(min={db_pool.get_min_size()}, max={db_pool.get_max_size()})"
            )
        except Exception as e:
            logger.warning(f"Database pool creation failed: {e}. Continuing without DB.")

    # Initialize rate limiter (16 concurrent EasyPost API calls)
    rate_limiter = asyncio.Semaphore(16)

    # Create resources object
    resources = AppResources(
        easypost_service=easypost_service,
        db_pool=db_pool,
        rate_limiter=rate_limiter,
    )

    try:
        # Yield dict for FastAPI lifespan state (Starlette requirement)
        yield {
            "easypost_service": resources.easypost_service,
            "db_pool": resources.db_pool,
            "rate_limiter": resources.rate_limiter,
        }
    finally:
        # Cleanup
        logger.info("Shutting down EasyPost MCP Server...")

        if db_pool:
            await db_pool.close()
            logger.info("Database pool closed")

        logger.info("Shutdown complete")
