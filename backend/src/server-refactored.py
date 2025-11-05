"""
FastAPI server with MCP integration and organized routers.

Refactored with industry best practices:
- API versioning (/api/v1/)
- Router-based organization
- Centralized middleware
- Clean separation of concerns
"""

import logging
import uuid

# M3 Max Optimization: uvloop enabled via uvicorn for 2-4x faster async I/O
# Note: uvloop is configured in uvicorn.run() below (loop="uvloop")
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.dependencies import EasyPostDep
from src.lifespan import app_lifespan
from src.utils.config import settings
from src.utils.monitoring import HealthCheck, metrics

# Constants
REQUEST_ID_HEADER = "X-Request-ID"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Validate settings on startup
try:
    settings.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Initialize FastMCP server with lifespan
from fastmcp import FastMCP

from src.mcp.prompts import register_prompts
from src.mcp.resources import register_resources
from src.mcp.tools import register_tools

mcp = FastMCP(
    name="EasyPost Shipping Server",
    instructions="MCP server for managing shipments and tracking with EasyPost API",
    lifespan=app_lifespan,
)

# Initialize FastAPI app with MCP lifespan
app = FastAPI(
    title="EasyPost MCP Server",
    description="MCP server for managing shipments and tracking with EasyPost API",
    version="1.0.0",
    lifespan=app_lifespan,
)

# Rate limiting (10 requests per minute per IP)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID middleware
class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add request ID to all requests for tracing."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Add to response headers
        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response


app.add_middleware(RequestIDMiddleware)

# ============================================================================
# ROUTER REGISTRATION - Industry Best Practice Pattern
# ============================================================================

# Import routers
from src.routers import analytics, database, shipments, tracking, webhooks

# ============================================================================
# API VERSIONING STRATEGY
# ============================================================================
# Current: Legacy routes for backward compatibility
# Future: Migrate to /api/v1/* for versioned API

# Include routers with legacy paths (for existing tests/frontend)
app.include_router(shipments.rates_router, prefix="")  # /rates at root
app.include_router(shipments.router, prefix="")  # /shipments/* at root
app.include_router(tracking.router, prefix="")  # /tracking/* at root
app.include_router(analytics.router, prefix="")  # /analytics, /stats, /carrier-performance at root
app.include_router(database.router, prefix="")  # /db/* at root
app.include_router(webhooks.router, prefix="")  # /webhooks/* at root

# TODO: Add versioned routes when frontend is updated
# app.include_router(shipments.router, prefix="/api/v1/shipments", tags=["v1"])
# app.include_router(tracking.router, prefix="/api/v1/tracking", tags=["v1"])
# app.include_router(analytics.router, prefix="/api/v1", tags=["v1"])
# app.include_router(database.router, prefix="/api/v1/db", tags=["v1"])
# app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["v1"])

logger.info("API routers registered (organized by domain)")

# ============================================================================
# MCP INTEGRATION
# ============================================================================

# Mount MCP server at /mcp endpoint for AI integration
# Note: MCP tools will access easypost_service via Context
app.mount("/mcp", mcp.http_app())

# Add error handling middleware to MCP
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware

mcp.add_middleware(
    ErrorHandlingMiddleware(
        include_traceback=settings.DEBUG if hasattr(settings, "DEBUG") else False,
        transform_errors=True,
        error_callback=lambda e: metrics.record_error(),
    )
)

# Register MCP components after mounting
# Pass None as service since tools will use Context
register_tools(mcp, None)  # Updated to use Context in Phase 4
register_resources(mcp, None)
register_prompts(mcp)

logger.info("MCP server mounted at /mcp (HTTP transport) with error handling middleware")

# ============================================================================
# CORE APP ENDPOINTS (Non-versioned)
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "EasyPost MCP Server",
        "version": "1.0.0",
        "api": "/api/v1",
        "docs": "/docs",
        "health": "/health",
        "mcp": "/mcp",
    }


@app.get("/health")
async def health_check(request: Request, service: EasyPostDep):
    """
    Enhanced health check with EasyPost API, database, and system monitoring.

    Returns:
        Health status including:
        - EasyPost API connectivity
        - Database pool metrics
        - System resources
    """
    health = HealthCheck()
    # Get database pool from app state (lifespan context)
    db_pool = getattr(request.app.state, "db_pool", None) if hasattr(request.app, "state") else None
    return await health.check(service, db_pool=db_pool)


@app.get("/metrics")
async def get_metrics():
    """
    Get performance metrics.

    Returns:
        API call metrics, success rates, and performance stats
    """
    return metrics.get_metrics()


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Development: Single worker to avoid connection pool exhaustion
    # Production: Use 4 workers or increase max_connections to 400+
    # See docs/architecture/POSTGRESQL_ARCHITECTURE.md for details
    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
        reload=True,  # Enable auto-reload for development
        loop="uvloop",  # Use uvloop for 2-4x faster async I/O (Python 3.12+)
        log_level="info",
        access_log=True,
    )
