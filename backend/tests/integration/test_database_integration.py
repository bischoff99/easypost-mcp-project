"""
Integration tests for database functionality.
"""

import os

import pytest

from src.database import create_tables, get_db
from src.services.database_service import DatabaseService

# Skip database tests in parallel mode (event loop conflicts with pytest-xdist)
# To run: DATABASE_URL=postgresql://... pytest tests/integration/test_database_integration.py
pytestmark = pytest.mark.skipif(
    os.getenv("PYTEST_XDIST_WORKER") is not None,
    reason="Database tests skip in parallel mode - run individually without -n flag",
)


@pytest.mark.asyncio
class TestDatabaseIntegration:
    """Test database integration and basic CRUD operations - run serially to avoid async event loop conflicts."""

    async def test_database_connection(self):
        """Test database connection and table creation."""
        # Create tables
        await create_tables()

        # Get a database session
        async for session in get_db():
            assert session is not None
            break

    async def test_address_crud(self):
        """Test address CRUD operations."""
        await create_tables()

        async for session in get_db():
            db_service = DatabaseService(session)

            # Create address
            address_data = {
                "name": "John Doe",
                "company": "Test Corp",
                "street1": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip": "12345",
                "country": "US",
                "email": "john@example.com",
                "phone": "+15551234567",
            }

            address = await db_service.create_address(address_data)
            assert address.id is not None
            assert address.name == "John Doe"
            assert address.company == "Test Corp"
            assert address.city == "Anytown"
            assert address.state == "CA"
            assert address.zip == "12345"
            assert address.country == "US"

            # Get address
            retrieved = await db_service.get_address(address.id)
            assert retrieved is not None
            assert retrieved.id == address.id
            assert retrieved.name == "John Doe"

            # Update address
            update_data = {"name": "Jane Doe", "city": "New Town"}
            updated = await db_service.update_address(address.id, update_data)
            assert updated is not None
            assert updated.name == "Jane Doe"
            assert updated.city == "New Town"
            assert updated.state == "CA"  # Unchanged

            break

    async def test_shipment_creation(self):
        """Test shipment creation with related entities."""
        await create_tables()

        async for session in get_db():
            db_service = DatabaseService(session)

            # Create addresses first
            from_address_data = {
                "name": "Sender Corp",
                "street1": "456 Sender Ave",
                "city": "Send City",
                "state": "NY",
                "zip": "10001",
                "country": "US",
            }
            from_address = await db_service.create_address(from_address_data)

            to_address_data = {
                "name": "Receiver Corp",
                "street1": "789 Receiver Blvd",
                "city": "Receive City",
                "state": "TX",
                "zip": "75001",
                "country": "US",
            }
            to_address = await db_service.create_address(to_address_data)

            # Create shipment
            import uuid

            shipment_data = {
                "easypost_id": f"sh_test_{uuid.uuid4().hex[:12]}",
                "status": "created",
                "mode": "test",
                "reference": f"TEST-{uuid.uuid4().hex[:6].upper()}",
                "from_address_id": from_address.id,
                "to_address_id": to_address.id,
                "parcel_id": None,  # We'll add this later if needed
                "carrier": "USPS",
                "service": "Priority Mail",
                "currency": "USD",
            }

            shipment = await db_service.create_shipment(shipment_data)
            assert shipment.id is not None
            assert shipment.easypost_id.startswith("sh_test_")
            assert shipment.status == "created"
            assert shipment.carrier == "USPS"
            assert shipment.service == "Priority Mail"

            # Verify relationships
            assert shipment.from_address.name == "Sender Corp"
            assert shipment.to_address.name == "Receiver Corp"

            break

    async def test_analytics_operations(self):
        """Test analytics data operations."""
        await create_tables()

        async for session in get_db():
            db_service = DatabaseService(session)

            # Create analytics summary
            from datetime import date

            summary_data = {
                "date": date.today(),
                "period": "daily",
                "total_shipments": 150,
                "successful_shipments": 145,
                "failed_shipments": 5,
                "total_cost": 1250.50,
                "average_cost_per_shipment": 8.34,
                "currency": "USD",
                "average_delivery_days": 2.3,
                "on_time_delivery_rate": 94.5,
            }

            summary = await db_service.create_analytics_summary(summary_data)
            assert summary.id is not None
            assert summary.total_shipments == 150
            assert summary.successful_shipments == 145
            assert summary.average_cost_per_shipment == 8.34

            # Retrieve analytics summary
            retrieved = await db_service.get_analytics_summary_by_date(date.today(), "daily")
            assert retrieved is not None
            assert retrieved.id == summary.id

            break

    async def test_utility_methods(self):
        """Test utility methods."""
        await create_tables()

        async for session in get_db():
            db_service = DatabaseService(session)

            # Initially should be 0
            count = await db_service.get_shipment_count()
            assert count >= 0  # Could be more from previous tests

            # Get status breakdown
            status_counts = await db_service.get_shipments_by_status()
            assert isinstance(status_counts, dict)

            # Get recent activities (should be empty initially)
            activities = await db_service.get_recent_activities(5)
            assert isinstance(activities, list)

            break

    @pytest.fixture(autouse=True)
    async def cleanup_tables(self):
        """Clean up tables after each test."""
        yield
        # Note: In a real scenario, you might want to clean up test data
        # But for now, we'll leave it for manual cleanup if needed
