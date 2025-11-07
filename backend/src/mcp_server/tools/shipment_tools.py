"""Shipment creation MCP tool."""

import asyncio
import logging
from datetime import UTC, datetime

from fastmcp import Context
from pydantic import ValidationError

from src.database import get_db
from src.services.database_service import DatabaseService
from src.services.easypost_service import AddressModel, ParcelModel

logger = logging.getLogger(__name__)


def register_shipment_tools(mcp, easypost_service=None):
    """Register shipment-related tools with MCP server."""

    @mcp.tool(tags=["shipping", "core", "create"])
    async def create_shipment(
        to_address: dict,
        from_address: dict,
        parcel: dict,
        carrier: str = "USPS",
        contents: str = "General Merchandise",
        value: float = 50.0,
        ctx: Context = None,
    ) -> dict:
        """
        Create a new shipment and purchase a label.

        Args:
            to_address: Destination address (name, street1, city, state, zip, country)
            from_address: Origin address (same structure)
            parcel: Package dimensions (length, width, height, weight in inches/ounces)
            carrier: Preferred carrier (default: USPS)
            contents: Item description for customs (default: "General Merchandise")
            value: Item value in USD for customs (default: 50.0)
            ctx: MCP context

        Returns:
            Standardized response with status, data, message, timestamp
        """
        try:
            # Get service from context or use provided
            if ctx:
                lifespan_ctx = ctx.request_context.lifespan_context
                service = (
                    lifespan_ctx.get("easypost_service")
                    if isinstance(lifespan_ctx, dict)
                    else lifespan_ctx.easypost_service
                )
            elif easypost_service:
                service = easypost_service
            else:
                raise ValueError("No EasyPost service available")

            # Validate inputs
            to_addr = AddressModel(**to_address)
            from_addr = AddressModel(**from_address)
            parcel_obj = ParcelModel(**parcel)

            if ctx:
                await ctx.info(f"Creating shipment with {carrier}")

            # Check if international shipment
            is_international = to_addr.country != from_addr.country
            customs_info = None

            if is_international:
                # Create customs info for international shipment
                customs_item = service.client.customs_item.create(
                    description=contents,
                    hs_tariff_number="9999.00.0000",  # Generic code
                    origin_country=from_addr.country,
                    quantity=1,
                    value=value,
                    weight=parcel_obj.weight,
                )
                customs_info = service.client.customs_info.create(customs_items=[customs_item])

            # Add timeout to prevent SSE timeout errors
            result = await asyncio.wait_for(
                service.create_shipment(
                    to_addr.dict(), from_addr.dict(), parcel_obj.dict(), carrier, True, customs_info
                ),
                timeout=30.0,
            )

            # Database persistence for successful shipments
            if result.get("status") == "success":
                try:
                    async for session in get_db():
                        db_service = DatabaseService(session)

                        # Store addresses
                        from_address_data = {
                            "name": from_addr.name or "",
                            "company": from_addr.company or "",
                            "street1": from_addr.street1,
                            "street2": from_addr.street2 or "",
                            "city": from_addr.city,
                            "state": from_addr.state or "",
                            "zip": from_addr.zip,
                            "country": from_addr.country,
                            "phone": from_addr.phone or "",
                            "email": from_addr.email or "",
                        }

                        to_address_data = {
                            "name": to_addr.name or "",
                            "company": to_addr.company or "",
                            "street1": to_addr.street1,
                            "street2": to_addr.street2 or "",
                            "city": to_addr.city,
                            "state": to_addr.state or "",
                            "zip": to_addr.zip,
                            "country": to_addr.country,
                            "phone": to_addr.phone or "",
                            "email": to_addr.email or "",
                        }

                        from_addr_db = await db_service.create_address(from_address_data)
                        to_addr_db = await db_service.create_address(to_address_data)

                        # Store shipment
                        shipment_data = {
                            "easypost_id": result.get("id"),
                            "status": "created",
                            "mode": "test",
                            "reference": f"single_{result.get('id')}",
                            "from_address_id": from_addr_db.id,
                            "to_address_id": to_addr_db.id,
                            "carrier": result.get("carrier"),
                            "service": result.get("service"),
                            "total_cost": result.get("rate"),
                            "currency": "USD",
                            "tracking_code": result.get("tracking_code"),
                            "metadata": {
                                "contents": contents,
                                "value": value,
                                "is_international": is_international,
                                "customs_created": is_international,
                            },
                        }

                        db_shipment = await db_service.create_shipment(shipment_data)

                        # Log user activity
                        await db_service.log_user_activity(
                            {
                                "action": "create_shipment",
                                "resource": "shipment",
                                "resource_id": db_shipment.id,
                                "method": "POST",
                                "endpoint": "/mcp/create_shipment",
                                "status_code": 200,
                                "response_time_ms": 0,  # Not tracked for individual shipments
                                "metadata": {
                                    "carrier": result.get("carrier"),
                                    "cost": result.get("rate"),
                                    "is_international": is_international,
                                },
                            }
                        )

                        if ctx:
                            await ctx.info("💾 Shipment data persisted to database")

                        break

                except Exception as db_error:
                    logger.error(f"Failed to persist shipment to database: {db_error}")
                    # Don't fail the shipment creation if database persistence fails
                    if ctx:
                        await ctx.info("⚠️ Shipment created but database persistence failed")

            if ctx and result.get("status") == "success":
                await ctx.info(f"Shipment created: {result.get('id')}")

            return {
                "status": result.get("status", "error"),
                "data": result if result.get("status") == "success" else None,
                "message": (
                    "Shipment created successfully"
                    if result.get("status") == "success"
                    else result.get("message", "Unknown error")
                ),
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except TimeoutError:
            logger.error("Shipment creation timed out after 30 seconds")
            return {
                "status": "error",
                "data": None,
                "message": "Shipment creation timed out. Please try again.",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return {
                "status": "error",
                "data": None,
                "message": f"Validation error: {str(e)}",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            logger.error(f"Tool error: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "data": None,
                "message": f"Error: {str(e)}",
                "timestamp": datetime.now(UTC).isoformat(),
            }
