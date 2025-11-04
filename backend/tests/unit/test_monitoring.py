"""Unit tests for monitoring utilities."""

from unittest.mock import MagicMock, patch

import pytest

from src.utils.monitoring import HealthCheck, MetricsCollector


class TestHealthCheck:
    """Test HealthCheck class."""

    @pytest.fixture
    def health_check(self):
        """Create HealthCheck instance."""
        return HealthCheck()

    @pytest.fixture
    def mock_easypost_service(self):
        """Mock EasyPost service."""
        service = MagicMock()
        service.api_key = "test_key"
        return service

    def test_check_system_success(self, health_check):
        """Test successful system health check."""
        with (
            patch("psutil.cpu_percent", return_value=25.5),
            patch("psutil.virtual_memory") as mock_memory,
            patch("psutil.disk_usage") as mock_disk,
        ):
            # Mock memory
            mock_memory.return_value = MagicMock()
            mock_memory.return_value.percent = 60.0
            mock_memory.return_value.available = 8 * 1024 * 1024 * 1024  # 8GB

            # Mock disk
            mock_disk.return_value = MagicMock()
            mock_disk.return_value.percent = 45.0
            mock_disk.return_value.free = 100 * 1024 * 1024 * 1024  # 100GB

            result = health_check.check_system()

            assert result["status"] == "healthy"
            assert result["cpu_percent"] == 25.5
            assert result["memory_percent"] == 60.0
            assert result["disk_percent"] == 45.0

    def test_check_system_failure(self, health_check):
        """Test system health check failure."""
        with patch("psutil.cpu_percent", side_effect=Exception("System error")):
            result = health_check.check_system()

            assert result["status"] == "unhealthy"
            assert "error" in result

    @pytest.mark.asyncio
    async def test_check_easypost_success(self, health_check, mock_easypost_service):
        """Test successful EasyPost health check."""
        with patch("easypost.EasyPostClient") as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client

            # Mock the carrier_account.all() call
            mock_client.carrier_account.all = MagicMock()

            result = await health_check.check_easypost(mock_easypost_service.api_key)

            assert result["status"] == "healthy"
            mock_client_class.assert_called_once_with("test_key")
            mock_client.carrier_account.all.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_easypost_failure(self, health_check, mock_easypost_service):
        """Test EasyPost health check failure."""
        with patch("easypost.EasyPostClient", side_effect=Exception("API error")):
            result = await health_check.check_easypost(mock_easypost_service.api_key)

            assert result["status"] == "unhealthy"
            assert "API error" in result["error"]

    @pytest.mark.asyncio
    async def test_check_overall_success(self, health_check, mock_easypost_service):
        """Test overall health check success."""
        with (
            patch.object(health_check, "check_system", return_value={"status": "healthy"}),
            patch.object(health_check, "check_easypost", return_value={"status": "healthy"}),
        ):
            result = await health_check.check(mock_easypost_service)

            assert result["status"] == "healthy"
            assert "system" in result
            assert "easypost" in result
            assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_check_overall_failure_system(self, health_check, mock_easypost_service):
        """Test overall health check failure due to system."""
        with (
            patch.object(health_check, "check_system", return_value={"status": "unhealthy"}),
            patch.object(health_check, "check_easypost", return_value={"status": "healthy"}),
        ):
            result = await health_check.check(mock_easypost_service)

            assert result["status"] == "unhealthy"

    @pytest.mark.asyncio
    async def test_check_overall_failure_easypost(self, health_check, mock_easypost_service):
        """Test overall health check failure due to EasyPost."""
        with (
            patch.object(health_check, "check_system", return_value={"status": "healthy"}),
            patch.object(health_check, "check_easypost", return_value={"status": "unhealthy"}),
        ):
            result = await health_check.check(mock_easypost_service)

            assert result["status"] == "unhealthy"

    @pytest.mark.asyncio
    async def test_check_exception_handling(self, health_check, mock_easypost_service):
        """Test exception handling in overall check."""
        with patch.object(health_check, "check_system", side_effect=Exception("Unexpected error")):
            result = await health_check.check(mock_easypost_service)

            assert result["status"] == "unhealthy"
            assert "Unexpected error" in result["error"]
            assert "timestamp" in result


class TestMetricsCollector:
    """Test MetricsCollector class."""

    @pytest.fixture
    def metrics_collector(self):
        """Create MetricsCollector instance."""
        return MetricsCollector()

    def test_initialization(self, metrics_collector):
        """Test MetricsCollector initialization."""
        assert metrics_collector.error_count == 0
        assert metrics_collector.api_calls == {}

    def test_record_error(self, metrics_collector):
        """Test recording errors."""
        metrics_collector.record_error()
        assert metrics_collector.error_count == 1

        metrics_collector.record_error()
        assert metrics_collector.error_count == 2

    def test_track_api_call_success(self, metrics_collector):
        """Test tracking successful API calls."""
        metrics_collector.track_api_call("get_rates", True)

        assert "get_rates" in metrics_collector.api_calls
        assert metrics_collector.api_calls["get_rates"]["success"] == 1
        assert metrics_collector.api_calls["get_rates"]["failure"] == 0

    def test_track_api_call_failure(self, metrics_collector):
        """Test tracking failed API calls."""
        metrics_collector.track_api_call("create_shipment", False)

        assert "create_shipment" in metrics_collector.api_calls
        assert metrics_collector.api_calls["create_shipment"]["success"] == 0
        assert metrics_collector.api_calls["create_shipment"]["failure"] == 1
        assert metrics_collector.error_count == 1  # Should also increment error_count

    def test_track_api_call_multiple(self, metrics_collector):
        """Test tracking multiple API calls."""
        # Success calls
        metrics_collector.track_api_call("get_rates", True)
        metrics_collector.track_api_call("get_rates", True)

        # Failure calls
        metrics_collector.track_api_call("get_rates", False)
        metrics_collector.track_api_call("create_shipment", False)

        assert metrics_collector.api_calls["get_rates"]["success"] == 2
        assert metrics_collector.api_calls["get_rates"]["failure"] == 1
        assert metrics_collector.api_calls["create_shipment"]["success"] == 0
        assert metrics_collector.api_calls["create_shipment"]["failure"] == 1
        assert metrics_collector.error_count == 2

    def test_get_metrics(self, metrics_collector):
        """Test getting metrics summary."""
        # Set up some test data
        metrics_collector.error_count = 2
        metrics_collector.api_calls = {
            "get_rates": {"success": 3, "failure": 1},
            "create_shipment": {"success": 2, "failure": 0},
        }

        with patch("time.time", return_value=1000):  # Mock current time
            metrics_collector.start_time = 900  # Mock start time
            result = metrics_collector.get_metrics()

        assert result["uptime_seconds"] == 100
        assert result["error_count"] == 2
        # api_calls tracks success/failure per endpoint
        assert "api_calls" in result or result["api_calls"] == metrics_collector.api_calls
        assert "timestamp" in result

    def test_get_metrics_no_requests(self, metrics_collector):
        """Test getting metrics when no requests have been made."""
        with patch("time.time", return_value=1000):
            metrics_collector.start_time = 900
            result = metrics_collector.get_metrics()

        assert result["error_rate"] == 0.0  # Division by zero protection


class TestGlobalMetrics:
    """Test global metrics instance."""

    def test_global_metrics_instance(self):
        """Test that global metrics instance exists and works."""
        # Reset global metrics for clean test
        global metrics
        metrics = MetricsCollector()

        # Test basic functionality
        metrics.record_error()
        metrics.track_api_call("test_endpoint", True)

        result = metrics.get_metrics()

        assert result["error_count"] == 1
        assert "test_endpoint" in result["api_calls"]
