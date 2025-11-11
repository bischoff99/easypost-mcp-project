"""Monitoring utilities for health checks and metrics."""

import asyncio
import logging
import time
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class HealthCheck:
    """Health check utilities for monitoring application status."""

    async def check(self, easypost_service) -> dict[str, Any]:
        """
        Comprehensive health check combining EasyPost and database checks.

        Args:
            easypost_service: EasyPostService instance

        Returns:
            Dict with overall health status
        """
        try:
            # Check EasyPost API connectivity
            easypost_health = await self.check_easypost(easypost_service.api_key)

            # Check database health (SQLAlchemy ORM only)
            database_health = await self.check_database()

            # Determine overall status
            is_healthy = (
                easypost_health["status"] == "healthy"
                and database_health["status"] in ["healthy", "disabled"]
            )

            return {
                "status": "healthy" if is_healthy else "unhealthy",
                "easypost": easypost_health,
                "database": database_health,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }

    @staticmethod
    async def check_database() -> dict[str, Any]:
        """
        Check database connectivity using SQLAlchemy ORM pool.

        Returns:
            Dict with database health status
        """
        # Check if ORM database is available
        try:
            from src.database import is_database_available, async_session
        except ImportError:
            return {"status": "disabled", "reason": "database module not available"}

        if not is_database_available():
            return {
                "status": "disabled",
                "orm_available": False,
                "reason": "DATABASE_URL not configured",
            }

        # Test SQLAlchemy connection
        try:
            from sqlalchemy import text

            async with async_session() as session:
                result = await session.execute(text("SELECT 1"))
                if result.scalar() != 1:
                    raise Exception("Database query test failed")

            return {
                "status": "healthy",
                "orm_available": True,
                "connectivity": "connected",
            }
        except Exception as e:
            logger.error(f"Database check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "orm_available": True,
                "error": str(e)[:100],
            }

    @staticmethod
    async def check_easypost(api_key: str) -> dict[str, Any]:
        """Check EasyPost API connectivity."""
        try:
            import easypost

            client = easypost.EasyPostClient(api_key)
            # Simple API call to verify connectivity
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, client.carrier_account.all)
            return {"status": "healthy", "latency_ms": 0}
        except Exception as e:
            logger.error(f"EasyPost health check failed: {str(e)}")
            return {"status": "unhealthy", "error": str(e)}


class MetricsCollector:
    """Collect and track application metrics."""

    def __init__(self):
        self.start_time = time.time()
        self.error_count = 0
        self.api_calls = {}  # Track calls per endpoint

    def record_error(self):
        """Record an error."""
        self.error_count += 1

    def track_api_call(self, endpoint: str, success: bool):
        """
        Track API call success/failure by endpoint.

        Args:
            endpoint: API endpoint name
            success: Whether the call succeeded
        """
        if endpoint not in self.api_calls:
            self.api_calls[endpoint] = {"success": 0, "failure": 0}

        if success:
            self.api_calls[endpoint]["success"] += 1
        else:
            self.api_calls[endpoint]["failure"] += 1
            self.record_error()

    def get_metrics(self) -> dict[str, Any]:
        """Get current metrics."""
        uptime_seconds = int(time.time() - self.start_time)
        total_calls = sum(stats["success"] + stats["failure"] for stats in self.api_calls.values())
        return {
            "uptime_seconds": uptime_seconds,
            "total_calls": total_calls,
            "error_count": self.error_count,
            "error_rate": round(self.error_count / max(total_calls, 1), 4),
            "api_calls": self.api_calls,
            "timestamp": datetime.now(UTC).isoformat(),
        }


# Global metrics instance
metrics = MetricsCollector()
