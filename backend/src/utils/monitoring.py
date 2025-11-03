"""Monitoring utilities for health checks and metrics."""

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict

import psutil

logger = logging.getLogger(__name__)


class HealthCheck:
    """Health check utilities for monitoring application status."""

    async def check(self, easypost_service) -> Dict[str, Any]:
        """
        Comprehensive health check combining EasyPost and system checks.

        Args:
            easypost_service: EasyPostService instance

        Returns:
            Dict with overall health status
        """
        try:
            # Check system health
            system_health = self.check_system()

            # Check EasyPost API connectivity
            easypost_health = await self.check_easypost(easypost_service.api_key)

            # Determine overall status
            is_healthy = (
                system_health["status"] == "healthy" and easypost_health["status"] == "healthy"
            )

            return {
                "status": "healthy" if is_healthy else "unhealthy",
                "system": system_health,
                "easypost": easypost_health,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    @staticmethod
    async def check_easypost(api_key: str) -> Dict[str, Any]:
        """Check EasyPost API connectivity."""
        try:
            import easypost

            client = easypost.EasyPostClient(api_key)
            # Simple API call to verify connectivity
            await asyncio.get_event_loop().run_in_executor(None, client.carrier_account.all)
            return {"status": "healthy", "latency_ms": 0}
        except Exception as e:
            logger.error(f"EasyPost health check failed: {str(e)}")
            return {"status": "unhealthy", "error": str(e)}

    @staticmethod
    def check_system() -> Dict[str, Any]:
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
        self.request_count = 0
        self.error_count = 0
        self.shipment_count = 0
        self.tracking_count = 0
        self.api_calls = {}  # Track calls per endpoint

    def record_request(self):
        """Record an API request."""
        self.request_count += 1

    def record_error(self):
        """Record an error."""
        self.error_count += 1

    def record_shipment(self):
        """Record a shipment creation."""
        self.shipment_count += 1

    def record_tracking(self):
        """Record a tracking lookup."""
        self.tracking_count += 1

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

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        uptime_seconds = int(time.time() - self.start_time)
        return {
            "uptime_seconds": uptime_seconds,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "shipment_count": self.shipment_count,
            "tracking_count": self.tracking_count,
            "error_rate": round(self.error_count / max(self.request_count, 1), 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# Global metrics instance
metrics = MetricsCollector()
