
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Import the tools to be tested
from src.mcp.tools.shipment_tools import create_shipment
from src.mcp.tools.tracking_tools import get_tracking
from src.mcp.tools.rate_tools import get_rates
from src.mcp.tools.bulk_tools import parse_and_get_bulk_rates
from src.mcp.tools.bulk_creation_tools import create_bulk_shipments, buy_bulk_shipments

# Mock data
TO_ADDRESS = {
    "name": "Test Recipient",
    "street1": "123 Test St",
    "city": "Testville",
    "state": "CA",
    "zip": "12345",
    "country": "US",
}
FROM_ADDRESS = {
    "name": "Test Sender",
    "street1": "456 Test Ave",
    "city": "Testburg",
    "state": "CA",
    "zip": "67890",
    "country": "US",
}
PARCEL = {
    "length": 10,
    "width": 8,
    "height": 4,
    "weight": 16,
}
TRACKING_NUMBER = "1234567890"
SPREADSHEET_DATA = "CA	USPS	Test	Recipient	555-555-5555	test@test.com	123 Test St		Testville	CA	12345	US		10x8x4	1 lbs	Test Item"

@pytest.fixture
def mock_mcp_context():
    """Fixture for a mocked MCP context."""
    ctx = MagicMock()
    ctx.info = AsyncMock()
    ctx.report_progress = AsyncMock()
    ctx.request_context.lifespan_context.easypost_service = AsyncMock()
    return ctx

@pytest.mark.asyncio
async def test_create_shipment(mock_mcp_context):
    """Test the create_shipment tool."""
    mock_mcp_context.request_context.lifespan_context.easypost_service.create_shipment.return_value = {"status": "success", "id": "shp_123"}
    result = await create_shipment(TO_ADDRESS, FROM_ADDRESS, PARCEL, ctx=mock_mcp_context)
    assert result["status"] == "success"
    assert result["data"]["id"] == "shp_123"
    mock_mcp_context.info.assert_called()

@pytest.mark.asyncio
async def test_get_tracking(mock_mcp_context):
    """Test the get_tracking tool."""
    mock_mcp_context.request_context.lifespan_context.easypost_service.get_tracking.return_value = {"status": "success", "tracking_code": TRACKING_NUMBER}
    result = await get_tracking(TRACKING_NUMBER, ctx=mock_mcp_context)
    assert result["status"] == "success"
    assert result["tracking_code"] == TRACKING_NUMBER
    mock_mcp_context.info.assert_called_with(f"Fetching tracking for {TRACKING_NUMBER}...")

@pytest.mark.asyncio
async def test_get_rates(mock_mcp_context):
    """Test the get_rates tool."""
    mock_mcp_context.request_context.lifespan_context.easypost_service.get_rates.return_value = {"status": "success", "rates": []}
    result = await get_rates(TO_ADDRESS, FROM_ADDRESS, PARCEL, ctx=mock_mcp_context)
    assert result["status"] == "success"
    assert "rates" in result
    mock_mcp_context.info.assert_called_with("Calculating rates...")

@pytest.mark.asyncio
async def test_parse_and_get_bulk_rates(mock_mcp_context):
    """Test the parse_and_get_bulk_rates tool."""
    mock_mcp_context.request_context.lifespan_context.easypost_service.get_rates.return_value = {"status": "success", "data": []}
    result = await parse_and_get_bulk_rates(SPREADSHEET_DATA, ctx=mock_mcp_context)
    assert result["status"] == "success"
    assert "shipments" in result["data"]
    mock_mcp_context.info.assert_called()

@pytest.mark.asyncio
async def test_create_bulk_shipments(mock_mcp_context):
    """Test the create_bulk_shipments tool."""
    mock_mcp_context.request_context.lifespan_context.easypost_service.create_shipment.return_value = {"status": "success", "id": "shp_123"}
    with patch("src.mcp.tools.bulk_creation_tools.get_db", new_callable=AsyncMock):
        result = await create_bulk_shipments(SPREADSHEET_DATA, ctx=mock_mcp_context)
        assert result["status"] == "success"
        assert "shipments" in result["data"]
        mock_mcp_context.info.assert_called()

@pytest.mark.asyncio
async def test_buy_bulk_shipments(mock_mcp_context):
    """Test the buy_bulk_shipments tool."""
    mock_mcp_context.request_context.lifespan_context.easypost_service.client.shipment.retrieve.return_value = MagicMock()
    mock_mcp_context.request_context.lifespan_context.easypost_service.client.shipment.buy.return_value = MagicMock()
    with patch("src.mcp.tools.bulk_creation_tools.get_or_create_customs", new_callable=MagicMock):
        result = await buy_bulk_shipments(["shp_123"], ctx=mock_mcp_context)
        assert result["status"] == "success"
        assert "purchased" in result["data"]
        mock_mcp_context.info.assert_called()
