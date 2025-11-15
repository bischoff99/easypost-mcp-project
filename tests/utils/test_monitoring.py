from __future__ import annotations

from types import SimpleNamespace

import pytest

from src.utils.monitoring import HealthCheck, MetricsCollector


@pytest.mark.asyncio
async def test_health_check_reports_healthy(monkeypatch):
    async def fake_easypost(api_key: str):  # noqa: ARG001
        return {"status": "healthy"}

    async def fake_db():
        return {"status": "disabled"}

    monkeypatch.setattr(HealthCheck, "check_easypost", staticmethod(fake_easypost))
    monkeypatch.setattr(HealthCheck, "check_database", staticmethod(fake_db))

    service = SimpleNamespace(api_key="test")
    result = await HealthCheck().check(service)

    assert result["status"] == "healthy"
    assert result["easypost"]["status"] == "healthy"
    assert result["database"]["status"] == "disabled"


@pytest.mark.asyncio
async def test_health_check_handles_exception(monkeypatch):
    async def failing_easypost(api_key: str):  # noqa: ARG001
        raise RuntimeError("boom")

    monkeypatch.setattr(HealthCheck, "check_easypost", staticmethod(failing_easypost))

    result = await HealthCheck().check(SimpleNamespace(api_key="bad"))

    assert result["status"] == "unhealthy"
    assert "boom" in result["error"]


def test_metrics_collector_tracks_calls():
    collector = MetricsCollector()

    collector.track_api_call("rates", True)
    collector.track_api_call("rates", False)

    metrics = collector.get_metrics()

    assert metrics["error_count"] == 1
    assert metrics["api_calls"]["rates"]["success"] == 1
    assert metrics["api_calls"]["rates"]["failure"] == 1
