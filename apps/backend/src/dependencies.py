"""FastAPI dependency injection providers."""

from typing import Annotated

from fastapi import Depends
from fastmcp.server.dependencies import get_context

from src.services.easypost_service import EasyPostService
from src.utils.config import Settings, get_settings


def get_easypost_service() -> EasyPostService:
    """
    Dependency provider for EasyPost service.

    Returns service from lifespan context (production) or
    can be overridden with mock (testing).
    """
    try:
        ctx = get_context()
        # Access dict state from lifespan
        lifespan_ctx = ctx.request_context.lifespan_context
        if isinstance(lifespan_ctx, dict):
            return lifespan_ctx["easypost_service"]
        return lifespan_ctx.easypost_service
    except (AttributeError, RuntimeError, KeyError):
        # Fallback for non-MCP requests or testing
        from src.utils.config import settings

        return EasyPostService(api_key=settings.EASYPOST_API_KEY)


def get_rate_limiter():
    """
    Dependency provider for API rate limiter.

    Returns semaphore for controlling concurrent EasyPost API calls.
    """
    import asyncio

    try:
        ctx = get_context()
        lifespan_ctx = ctx.request_context.lifespan_context
        if isinstance(lifespan_ctx, dict):
            return lifespan_ctx.get("rate_limiter", asyncio.Semaphore(16))
        return lifespan_ctx.rate_limiter
    except (AttributeError, RuntimeError, KeyError):
        # Fallback semaphore
        return asyncio.Semaphore(16)


# Type aliases for clean endpoint annotations
EasyPostDep = Annotated[EasyPostService, Depends(get_easypost_service)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
