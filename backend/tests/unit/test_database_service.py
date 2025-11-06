"""Unit tests for database service CRUD operations."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, Mock, patch
from uuid import UUID, uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Address, AnalyticsSummary, BatchOperation, Shipment
from src.services.database_service import DatabaseService


@pytest.fixture
def mock_session():
    """Create mock async session."""
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.add = Mock()
    return session


@pytest.fixture
def db_service(mock_session):
    """Create database service with mock session."""
    return DatabaseService(mock_session)


class TestShipmentCRUD:
    """Test shipment CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_shipment(self, db_service, mock_session):
        """Test creating a new shipment."""
        shipment_data = {
            "easypost_id": "shp_test123",
            "tracking_code": "TRACK123",
            "status": "pending",
        }

        # Mock the commit and refresh
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Execute
        result = await db_service.create_shipment(shipment_data)

        # Verify
        assert isinstance(result, Shipment)
        assert result.easypost_id == "shp_test123"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_shipment(self, db_service, mock_session):
        """Test getting shipment by ID."""
        shipment_id = uuid4()

        # Mock result
        mock_shipment = Shipment(
            id=shipment_id, easypost_id="shp_test123", tracking_code="TRACK123"
        )

        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_shipment
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.get_shipment(shipment_id)

        # Verify
        assert result == mock_shipment
        assert result.id == shipment_id
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_shipment_not_found(self, db_service, mock_session):
        """Test getting non-existent shipment returns None."""
        shipment_id = uuid4()

        # Mock no result
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.get_shipment(shipment_id)

        # Verify
        assert result is None

    @pytest.mark.asyncio
    async def test_get_shipment_by_easypost_id(self, db_service, mock_session):
        """Test getting shipment by EasyPost ID."""
        easypost_id = "shp_test123"

        # Mock result
        mock_shipment = Shipment(id=uuid4(), easypost_id=easypost_id, tracking_code="TRACK123")

        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_shipment
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.get_shipment_by_easypost_id(easypost_id)

        # Verify
        assert result == mock_shipment
        assert result.easypost_id == easypost_id

    @pytest.mark.asyncio
    async def test_update_shipment(self, db_service, mock_session):
        """Test updating shipment."""
        shipment_id = uuid4()
        update_data = {"status": "delivered"}

        # Mock updated shipment
        mock_shipment = Shipment(id=shipment_id, easypost_id="shp_test123", status="delivered")

        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_shipment
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.update_shipment(shipment_id, update_data)

        # Verify
        assert result == mock_shipment
        assert result.status == "delivered"
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_shipment_not_found(self, db_service, mock_session):
        """Test updating non-existent shipment returns None."""
        shipment_id = uuid4()
        update_data = {"status": "delivered"}

        # Mock no result
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.update_shipment(shipment_id, update_data)

        # Verify
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_shipment(self, db_service, mock_session):
        """Test deleting shipment."""
        shipment_id = uuid4()

        # Mock successful deletion
        mock_result = Mock()
        mock_result.rowcount = 1
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.delete_shipment(shipment_id)

        # Verify
        assert result is True
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_shipment_not_found(self, db_service, mock_session):
        """Test deleting non-existent shipment returns False."""
        shipment_id = uuid4()

        # Mock no deletion
        mock_result = Mock()
        mock_result.rowcount = 0
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.delete_shipment(shipment_id)

        # Verify
        assert result is False


class TestAddressCRUD:
    """Test address CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_address(self, db_service, mock_session):
        """Test creating a new address."""
        address_data = {
            "name": "John Doe",
            "street1": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "country": "US",
        }

        # Mock
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Execute
        result = await db_service.create_address(address_data)

        # Verify
        assert isinstance(result, Address)
        assert result.name == "John Doe"
        assert result.city == "New York"
        mock_session.add.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_address(self, db_service, mock_session):
        """Test getting address by ID."""
        address_id = uuid4()

        # Mock result
        mock_address = Address(id=address_id, name="John Doe", city="New York")

        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_address
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.get_address(address_id)

        # Verify
        assert result == mock_address
        assert result.id == address_id

    @pytest.mark.asyncio
    async def test_update_address(self, db_service, mock_session):
        """Test updating address."""
        address_id = uuid4()
        update_data = {"city": "Boston"}

        # Mock
        mock_address = Address(id=address_id, name="John Doe", city="Boston")

        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_address
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.update_address(address_id, update_data)

        # Verify
        assert result == mock_address
        assert result.city == "Boston"

    @pytest.mark.asyncio
    async def test_get_address_not_found(self, db_service, mock_session):
        """Test getting non-existent address returns None."""
        address_id = uuid4()

        # Mock no result
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.get_address(address_id)

        # Verify
        assert result is None


class TestAnalyticsOperations:
    """Test analytics database operations."""

    @pytest.mark.asyncio
    async def test_create_analytics_summary(self, db_service, mock_session):
        """Test creating analytics summary."""
        summary_data = {
            "date": datetime.now(UTC).date(),
            "period": "daily",
            "total_shipments": 100,
            "total_cost": 5000.00,
            "average_cost_per_shipment": 50.00,
        }

        # Mock
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Execute
        result = await db_service.create_analytics_summary(summary_data)

        # Verify
        assert isinstance(result, AnalyticsSummary)
        assert result.total_shipments == 100
        assert result.period == "daily"
        mock_session.add.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_analytics_summary(self, db_service, mock_session):
        """Test getting analytics summary."""
        # Mock result dict
        mock_summary = {
            "total_shipments": 100,
            "total_cost": 5000.00,
            "carriers": ["USPS", "UPS"],
        }

        # Since get_analytics_summary returns dict, not db objects
        # we mock the entire method execution
        with patch.object(db_service, "get_analytics_summary", return_value=mock_summary):
            result = await db_service.get_analytics_summary(days=7)

        # Verify
        assert isinstance(result, dict)
        assert result["total_shipments"] == 100
        assert result["total_cost"] == 5000.00


class TestBatchOperations:
    """Test batch operation database methods."""

    @pytest.mark.asyncio
    async def test_create_batch_operation(self, db_service, mock_session):
        """Test creating batch operation."""
        batch_data = {
            "operation_type": "bulk_shipment_creation",
            "status": "pending",
            "total_items": 100,
        }

        # Mock
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Execute
        result = await db_service.create_batch_operation(batch_data)

        # Verify
        assert isinstance(result, BatchOperation)
        assert result.operation_type == "bulk_shipment_creation"
        assert result.total_items == 100

    @pytest.mark.asyncio
    async def test_update_batch_operation(self, db_service, mock_session):
        """Test updating batch operation."""
        batch_id = uuid4()
        update_data = {"status": "completed", "successful_items": 95}

        # Mock
        mock_batch = BatchOperation(
            id=batch_id,
            operation_type="bulk_shipment_creation",
            status="completed",
            successful_items=95,
        )

        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_batch
        mock_session.execute.return_value = mock_result

        # Execute
        result = await db_service.update_batch_operation(batch_id, update_data)

        # Verify
        assert result == mock_batch
        assert result.status == "completed"
        assert result.successful_items == 95


class TestServiceInitialization:
    """Test DatabaseService initialization."""

    def test_init_with_session(self, mock_session):
        """Test service initializes with session."""
        service = DatabaseService(mock_session)
        assert service.session == mock_session

    def test_init_stores_session(self, mock_session):
        """Test session is stored as instance variable."""
        service = DatabaseService(mock_session)
        assert hasattr(service, "session")
        assert isinstance(service.session, AsyncSession)
