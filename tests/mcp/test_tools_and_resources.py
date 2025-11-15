from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.mcp_server.resources.shipment_resources import register_shipment_resources
from src.mcp_server.resources.stats_resources import register_stats_resources
from src.mcp_server.tools.rate_tools import register_rate_tools
from src.mcp_server.tools.tracking_tools import register_tracking_tools


class DummyMCP:
    def __init__(self) -> None:
        self.tools: dict[str, callable] = {}
        self.resources: dict[str, callable] = {}

    def tool(self, **_):
        def decorator(func):
            self.tools[func.__name__] = func
            return func

        return decorator

    def resource(self, name: str):
        def decorator(func):
            self.resources[name] = func
            return func

        return decorator


class DummyCtx:
    def __init__(self, service):
        self.request_context = SimpleNamespace(lifespan_context={"easypost_service": service})
        self.info_messages: list[str] = []
        self.progress_updates: list[tuple[int, int]] = []

    async def info(self, message: str) -> None:
        self.info_messages.append(message)

    async def report_progress(self, current: int, total: int) -> None:
        self.progress_updates.append((current, total))


@pytest.fixture
def rate_tool():
    mcp = DummyMCP()
    register_rate_tools(mcp)
    return mcp.tools["get_rates"]


@pytest.fixture
def tracking_tool():
    mcp = DummyMCP()
    register_tracking_tools(mcp)
    return mcp.tools["get_tracking"]


@pytest.mark.asyncio
async def test_rate_tool_returns_service_data(rate_tool):
    service = MagicMock()
    service.get_rates = AsyncMock(return_value={"status": "success", "data": ["rate"]})
    ctx = DummyCtx(service)

    payload = {
        "name": "Jane",
        "street1": "123 Main",
        "city": "Austin",
        "state": "TX",
        "zip": "78701",
        "country": "US",
    }
    parcel = {"length": 10, "width": 5, "height": 4, "weight": 16}

    result = await rate_tool(payload, payload, parcel, ctx)

    assert result["data"] == ["rate"]
    service.get_rates.assert_awaited_once()
    assert ctx.info_messages[-1] == "Calculating rates..."


@pytest.mark.asyncio
async def test_rate_tool_handles_timeout(rate_tool, monkeypatch):
    service = MagicMock()
    service.get_rates = AsyncMock()
    ctx = DummyCtx(service)

    async def raise_timeout(awaitable, *, timeout):  # noqa: ARG001
        await awaitable
        raise TimeoutError

    monkeypatch.setattr(
        "src.mcp_server.tools.rate_tools.asyncio.wait_for", raise_timeout
    )

    address = {
        "name": "Jane",
        "street1": "123 Main",
        "city": "Austin",
        "state": "TX",
        "zip": "78701",
        "country": "US",
    }

    result = await rate_tool(address, address, {"length": 1, "width": 1, "height": 1, "weight": 1}, ctx)

    assert result["status"] == "error"
    assert "timed out" in result["message"]


@pytest.mark.asyncio
async def test_tracking_tool_returns_payload(tracking_tool):
    service = MagicMock()
    service.get_tracking = AsyncMock(return_value={"status": "success", "data": {}})
    ctx = DummyCtx(service)

    result = await tracking_tool("9400", ctx)

    assert result["status"] == "success"
    service.get_tracking.assert_awaited_once_with("9400")
    assert ctx.info_messages[0].startswith("Fetching tracking")


@pytest.mark.asyncio
async def test_tracking_tool_timeout(monkeypatch, tracking_tool):
    service = MagicMock()
    service.get_tracking = AsyncMock()
    ctx = DummyCtx(service)

    async def raise_timeout(awaitable, *, timeout):  # noqa: ARG001
        await awaitable
        raise TimeoutError

    monkeypatch.setattr(
        "src.mcp_server.tools.tracking_tools.asyncio.wait_for", raise_timeout
    )

    result = await tracking_tool("9400", ctx)

    assert result["status"] == "error"
    assert "timed out" in result["message"]


@pytest.mark.asyncio
async def test_shipment_resource_success(monkeypatch):
    mcp = DummyMCP()
    service = MagicMock()
    service.get_shipments_list = AsyncMock(return_value={"status": "success", "data": []})
    register_shipment_resources(mcp, service)
    resource = mcp.resources["easypost://shipments/recent"]

    async def immediate_wait(coro, *, timeout):  # noqa: ARG001
        return await coro

    monkeypatch.setattr(
        "src.mcp_server.resources.shipment_resources.asyncio.wait_for", immediate_wait
    )

    payload = await resource()

    data = json.loads(payload)
    assert data["status"] == "success"
    service.get_shipments_list.assert_awaited_once_with(page_size=10, purchased=True)


@pytest.mark.asyncio
async def test_stats_resource_calculates_metrics(monkeypatch):
    mcp = DummyMCP()
    service = MagicMock()
    service.get_shipments_list = AsyncMock(
        return_value={
            "status": "success",
            "data": [
                {
                    "selected_rate": {"rate": "5.5", "carrier": "USPS"},
                    "status": "delivered",
                },
                {
                    "selected_rate": {"rate": "7.0", "carrier": "UPS"},
                    "status": "in_transit",
                },
            ],
        }
    )
    register_stats_resources(mcp, service)
    resource = mcp.resources["easypost://stats/overview"]

    async def immediate_wait(coro, *, timeout):  # noqa: ARG001
        return await coro

    monkeypatch.setattr(
        "src.mcp_server.resources.stats_resources.asyncio.wait_for", immediate_wait
    )

    payload = await resource()

    data = json.loads(payload)
    assert data["status"] == "success"
    assert data["data"]["total_shipments"] == 2
    assert "carriers_used" in data["data"]
