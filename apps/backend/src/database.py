"""
Database configuration and session management for EasyPost MCP.
"""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .utils.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


def create_engine() -> AsyncEngine | None:
    """
    Create async database engine with error handling.

    Returns None if database configuration is invalid or unavailable.
    This allows the application to start without a database connection.
    """
    try:
        # Validate DATABASE_URL exists
        if not settings.DATABASE_URL:
            logger.warning("DATABASE_URL not configured. Database features disabled.")
            return None

        # Create async engine with comprehensive optimizations
        # Prevents connection storms and long stalls with proper timeouts
        engine = create_async_engine(
            settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
            echo=settings.ENVIRONMENT == "development",
            # Connection pool settings (configurable via env vars)
            # Default: 10 base + 5 overflow = 15 total connections per worker
            pool_size=settings.DATABASE_POOL_SIZE,  # Base pool size (default: 10)
            max_overflow=settings.DATABASE_MAX_OVERFLOW,  # Burst capacity (default: 5)
            pool_recycle=settings.DATABASE_POOL_RECYCLE,  # Recycle connections (default: 1800s)
            pool_pre_ping=True,  # Verify connections before use
            pool_timeout=settings.DATABASE_POOL_TIMEOUT,  # Wait for connection (default: 10s)
            # asyncpg-specific optimizations
            connect_args={
                "server_settings": {
                    "application_name": "easypost_mcp",
                    "jit": "on",  # Enable JIT compilation for complex queries
                    "timezone": "UTC",
                    # Set statement timeout at connection level (PostgreSQL)
                    "statement_timeout": str(settings.DATABASE_STATEMENT_TIMEOUT_MS),
                },
                "timeout": settings.DATABASE_CONNECT_TIMEOUT,  # Connection timeout (default: 10s)
                "command_timeout": settings.DATABASE_COMMAND_TIMEOUT,  # Query timeout (60s)
                "statement_cache_size": 500,  # Prepared statement cache
            },
            # Execution options
            execution_options={
                "postgresql_readonly": False,  # Set True for read replicas
                "postgresql_deferrable": False,
            },
        )

        logger.info("SQLAlchemy engine created successfully")
        return engine

    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        logger.warning("Application will continue without ORM database features")
        return None


# Create engine (may be None if database unavailable)
engine = create_engine()

# Create async session factory (only if engine exists)
async_session = None
if engine:
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession]:
    """
    Dependency for getting async database session.

    Raises RuntimeError if database is not configured.
    """
    if async_session is None:
        raise RuntimeError("Database not configured. Please set DATABASE_URL environment variable.")

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables() -> None:
    """
    Create all database tables.

    Raises RuntimeError if database is not configured.
    """
    if engine is None:
        raise RuntimeError("Cannot create tables: database engine not initialized")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")


async def drop_tables() -> None:
    """
    Drop all database tables.

    Raises RuntimeError if database is not configured.
    """
    if engine is None:
        raise RuntimeError("Cannot drop tables: database engine not initialized")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database tables dropped successfully")


def is_database_available() -> bool:
    """Check if database is configured and available."""
    return engine is not None and async_session is not None
