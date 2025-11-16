from __future__ import annotations

from fastmcp import Context
from fastmcp.exceptions import ToolError

from src.services.easypost_service import EasyPostService


def resolve_service(
    ctx: Context | None, injected: EasyPostService | None
) -> EasyPostService:
    """
    Resolve EasyPostService from MCP Context lifespan or injected fallback.

    Raises:
        ToolError: when service cannot be resolved
    """
    if ctx:
        lifespan_ctx = ctx.request_context.lifespan_context
        service = (
            lifespan_ctx.get("easypost_service")
            if isinstance(lifespan_ctx, dict)
            else getattr(lifespan_ctx, "easypost_service", None)
        )
        if service:
            return service
    if injected:
        return injected
    raise ToolError("EasyPost service not available. Check server configuration.")
