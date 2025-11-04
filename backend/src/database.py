"""
Database configuration and session management for EasyPost MCP.
"""

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .utils.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


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

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")


async def drop_tables() -> None:
    """Drop all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database tables dropped successfully")
