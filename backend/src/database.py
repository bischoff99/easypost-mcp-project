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

        # Create async engine with comprehensive optimizations for M3 Max
        # Based on best practices from Lyft Engineering, FastAPI + asyncpg, and PostgreSQL docs
        engine = create_async_engine(
            settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
            echo=settings.ENVIRONMENT == "development",
            # Connection pool settings
            pool_size=settings.DATABASE_POOL_SIZE,  # 20 concurrent connections
            max_overflow=settings.DATABASE_MAX_OVERFLOW,  # 30 burst capacity
            pool_recycle=settings.DATABASE_POOL_RECYCLE,  # 1 hour
            pool_pre_ping=True,  # Verify connections before use
            pool_timeout=30,  # Wait 30s for connection from pool
            # asyncpg-specific optimizations
            connect_args={
                "server_settings": {
                    "application_name": "easypost_mcp",
                    "jit": "on",  # Enable JIT compilation for complex queries
                    "timezone": "UTC",
                },
                "timeout": 10,  # Connection timeout (seconds)
                "command_timeout": 60,  # Query timeout (seconds)
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
