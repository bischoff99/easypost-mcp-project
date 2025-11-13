"""FastAPI server with analytics endpoint."""

import logging
import os
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.dependencies import EasyPostDep
from src.lifespan import app_lifespan
from src.utils.config import settings
from src.utils.monitoring import metrics

# Constants
REQUEST_ID_HEADER = "X-Request-ID"
MAX_REQUEST_LOG_SIZE = 1000

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

from src.mcp_server.prompts import register_prompts
from src.mcp_server.resources import register_resources
from src.mcp_server.tools import register_tools

mcp = FastMCP(
    name="EasyPost Shipping Server",
    instructions="MCP server for managing shipments and tracking with EasyPost API",
    lifespan=app_lifespan,
)

# Register MCP components (will be registered after app init)

# Initialize FastAPI app with MCP lifespan
app = FastAPI(
    title="EasyPost MCP Server",
    description="MCP server for managing shipments and tracking with EasyPost API",
    version="1.0.0",
    lifespan=app_lifespan,
)

# CORS middleware (production-safe configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicit whitelist
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Request-ID",
        "Accept",
        "Origin",
        "X-CSRF-Token",
    ],
    expose_headers=["X-Request-ID"],
    max_age=600,  # Cache preflight requests for 10 minutes
)


# Request ID middleware (disabled by default for personal use)
# Set DEBUG=true to enable request tracing
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

if DEBUG_MODE:

    class RequestIDMiddleware(BaseHTTPMiddleware):
        """Add request ID to all requests for tracing (DEBUG mode only)."""

        async def dispatch(self, request: Request, call_next):
            request_id = str(uuid.uuid4())
            request.state.request_id = request_id

            # Add to response headers
            response = await call_next(request)
            response.headers[REQUEST_ID_HEADER] = request_id
            return response

    app.add_middleware(RequestIDMiddleware)
    logger.info("Request ID middleware enabled (DEBUG mode)")
else:
    # In production, use a simple no-op middleware to avoid breaking request.state.request_id access
    class RequestIDMiddleware(BaseHTTPMiddleware):
        """No-op middleware for production (request ID disabled)."""

        async def dispatch(self, request: Request, call_next):
            request.state.request_id = "disabled"
            return await call_next(request)


app.add_middleware(RequestIDMiddleware)


# Exception handlers for better debugging
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with detailed logging for debugging.

    Logs validation failures to help diagnose API integration issues.
    """
    request_id = getattr(request.state, "request_id", "unknown")

    # Log detailed validation errors for debugging
    logger.warning(
        f"[{request_id}] Validation error on {request.method} {request.url.path}: {exc.errors()}"
    )

    # Track validation failures
    metrics.track_api_call("validation_error", False)

    # Return user-friendly error with details
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid request data",
            "errors": exc.errors(),
            "request_id": request_id,
        },
    )


# Mount MCP server at /mcp endpoint for AI integration
# Note: MCP tools will access easypost_service via Context
app.mount("/mcp", mcp.http_app())

# Include routers (simplified for personal use)
from src.routers import analytics, shipments, tracking

app.include_router(shipments.rates_router, prefix="/api")
app.include_router(shipments.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(tracking.router, prefix="/api/tracking")

logger.info("Routers registered: shipments, analytics, tracking")

# Note: FastMCP middleware would need to be implemented using the Middleware base class
# For now, error handling is done at the tool level and via FastAPI exception handlers

# Register MCP components after mounting
# Pass None as service since tools will use Context
register_tools(mcp, None)  # Updated to use Context in Phase 4
register_resources(mcp, None)
register_prompts(mcp)

logger.info("MCP server mounted at /mcp (HTTP transport) with error handling and retry middleware")


# Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "EasyPost MCP Server",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Lightweight health check - no external dependencies."""
    return {"ok": True}


@app.get("/readyz")
async def readiness_check(service: EasyPostDep):
    """Readiness check - verifies EasyPost connectivity."""
    # EasyPost check (optional - can be disabled if API key not set)
    try:
        if service.api_key:
            # Simple noop check - service already initialized
            pass
    except Exception as e:
        logger.error(f"EasyPost readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="EasyPost service not ready") from e

    return {"ready": True}


@app.get("/metrics")
async def get_metrics():
    """Get performance metrics."""
    return metrics.get_metrics()


# Note: All API endpoints are handled by routers:
# - /api/rates, /api/shipments → routers/shipments.py
# - /api/analytics → routers/analytics.py
# - /api/tracking → routers/tracking.py
# Database-backed endpoints and webhooks removed for personal use.


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    # Development: 2 workers (safer for dev)
    # Production: (2 * cores) + 1 workers for M3 Max optimization
    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",  # noqa: S104 - Required for Docker deployment
        port=8000,
        workers=2,
        log_level="info",
        access_log=True,
    )
