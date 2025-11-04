"""FastAPI dependency injection providers."""

from typing import Annotated

import asyncpg
from fastapi import Depends
from fastmcp.server.dependencies import get_context

from src.services.easypost_service import EasyPostService


def get_easypost_service() -> EasyPostService:
    """
    Dependency provider for EasyPost service.

    Returns service from lifespan context (production) or
    can be overridden with mock (testing).
    """
    try:
        ctx = get_context()
        return ctx.request_context.lifespan_context.easypost_service
    except (AttributeError, RuntimeError):
        # Fallback for non-MCP requests or testing
        from src.utils.config import settings

        return EasyPostService(api_key=settings.EASYPOST_API_KEY)


def get_db_pool() -> asyncpg.Pool | None:
    """
    Dependency provider for database connection pool.

    Returns None if database is not configured.
    """
    try:
        ctx = get_context()
        return ctx.request_context.lifespan_context.db_pool
    except (AttributeError, RuntimeError):
        return None


def get_rate_limiter():
    """
    Dependency provider for API rate limiter.

    Returns semaphore for controlling concurrent EasyPost API calls.
    """
    import asyncio

    try:
        ctx = get_context()
        return ctx.request_context.lifespan_context.rate_limiter
    except (AttributeError, RuntimeError):
        # Fallback semaphore
        return asyncio.Semaphore(16)


# Type aliases for clean endpoint annotations
EasyPostDep = Annotated[EasyPostService, Depends(get_easypost_service)]
DBPoolDep = Annotated[asyncpg.Pool | None, Depends(get_db_pool)]
