"""Monitoring utilities for health checks and metrics."""

import asyncio
import logging
import time
from datetime import UTC, datetime
from typing import Any

import psutil

logger = logging.getLogger(__name__)


class HealthCheck:
    """Health check utilities for monitoring application status."""

    async def check(self, easypost_service, db_pool=None) -> dict[str, Any]:
        """
        Comprehensive health check combining EasyPost, database, and system checks.

        Args:
            easypost_service: EasyPostService instance
            db_pool: Optional asyncpg connection pool for database monitoring

        Returns:
            Dict with overall health status
        """
        try:
            # Check system health
            system_health = self.check_system()

            # Check EasyPost API connectivity
            easypost_health = await self.check_easypost(easypost_service.api_key)

            # Check database health (if pool available)
            database_health = await self.check_database(db_pool)

            # Determine overall status
            is_healthy = (
                system_health["status"] == "healthy"
                and easypost_health["status"] == "healthy"
                and database_health["status"] in ["healthy", "disabled"]
            )

            return {
                "status": "healthy" if is_healthy else "unhealthy",
                "system": system_health,
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
    async def check_database(db_pool: Any | None) -> dict[str, Any]:
        """
        Check database connectivity and connection pool health.

        Args:
            db_pool: asyncpg connection pool (optional)

        Returns:
            Dict with database health status and connection metrics
        """
        # Check if ORM database is available
        try:
            from src.database import is_database_available
        except ImportError:
            return {"status": "disabled", "reason": "database module not available"}

        if not is_database_available():
            return {
                "status": "disabled",
                "orm_available": False,
                "reason": "DATABASE_URL not configured",
            }

        # Check asyncpg pool (if provided)
        pool_metrics = {}
        if db_pool:
            try:
                pool_metrics = {
                    "pool_size": db_pool.get_size(),
                    "pool_free": db_pool.get_idle_size(),
                    "pool_used": db_pool.get_size() - db_pool.get_idle_size(),
                    "pool_max": db_pool.get_max_size(),
                    "pool_utilization_percent": round(
                        ((db_pool.get_size() - db_pool.get_idle_size()) / db_pool.get_max_size())
                        * 100,
                        2,
                    ),
                }

                # Test connection
                async with db_pool.acquire() as conn:
                    result = await conn.fetchval("SELECT 1")
                    if result != 1:
                        raise Exception("Database query test failed")

                pool_metrics["connectivity"] = "connected"

            except Exception as e:
                logger.error(f"Database pool check failed: {str(e)}")
                return {
                    "status": "unhealthy",
                    "orm_available": True,
                    "asyncpg_pool": "error",
                    "error": str(e)[:100],
                    **pool_metrics,
                }

        return {
            "status": "healthy",
            "orm_available": True,
            "asyncpg_pool": "available" if db_pool else "not configured",
            **pool_metrics,
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

    @staticmethod
    def check_system() -> dict[str, Any]:
        """Check system resources."""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            return {
                "status": "healthy",
                "cpu_percent": round(cpu_percent, 2),
                "memory_percent": round(memory.percent, 2),
                "memory_available_mb": round(memory.available / 1024 / 1024, 2),
                "disk_percent": round(disk.percent, 2),
                "disk_free_gb": round(disk.free / 1024 / 1024 / 1024, 2),
            }
        except Exception as e:
            logger.error(f"System health check failed: {str(e)}")
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
