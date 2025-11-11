"""Application lifespan management for FastMCP + FastAPI integration."""

import asyncio
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

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

    # Verify database migrations are up to date (if database configured)
    if hasattr(settings, "DATABASE_URL") and settings.DATABASE_URL:
        try:
            await _check_database_migrations()
        except Exception as e:
            logger.warning(f"Database migration check failed: {e}. Continuing.")

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


async def _check_database_migrations():
    """
    Verify database migrations are up to date before starting app.

    Prevents starting server with outdated database schema.
    Raises RuntimeError if migrations are not applied.
    """
    try:
        # Find alembic.ini relative to this file
        backend_dir = Path(__file__).parent.parent
        alembic_ini_path = backend_dir / "alembic.ini"

        if not alembic_ini_path.exists():
            logger.warning(
                f"alembic.ini not found at {alembic_ini_path}. Skipping migration check."
            )
            return

        # Load Alembic configuration
        alembic_cfg = Config(str(alembic_ini_path))
        script = ScriptDirectory.from_config(alembic_cfg)

        # Get expected head revision
        head_rev = script.get_current_head()

        # Connect to database to check current revision
        from src.database import engine

        if engine is None:
            logger.warning("Database engine not initialized. Skipping migration check.")
            return

        async with engine.begin() as conn:
            # Get current database revision
            current_rev = await conn.run_sync(_get_current_revision)

        # Compare revisions
        if current_rev != head_rev:
            error_msg = (
                f"Database migration mismatch!\n"
                f"Current revision: {current_rev or 'None (empty database)'}\n"
                f"Expected revision: {head_rev}\n"
                f"Run 'alembic upgrade head' before starting the server."
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        logger.info(f"Database migrations up to date: {current_rev}")

    except RuntimeError:
        # Re-raise migration errors
        raise
    except Exception as e:
        logger.warning(f"Migration check failed: {e}. Proceeding with caution.")


def _get_current_revision(connection):
    """
    Get current database revision (sync helper for run_sync).

    Args:
        connection: SQLAlchemy sync connection

    Returns:
        Current revision string or None
    """
    context = MigrationContext.configure(connection)
    return context.get_current_revision()
