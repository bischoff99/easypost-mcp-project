import asyncio
import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from typing import Any

import easypost
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AddressModel(BaseModel):
    """Address model with input validation and length limits."""

    name: str = Field(..., max_length=100, description="Recipient name")
    street1: str = Field(..., max_length=200, description="Street address line 1")
    street2: str | None = Field(None, max_length=200, description="Street address line 2")
    city: str = Field(..., max_length=100, description="City name")
    state: str = Field(..., max_length=50, description="State or province")
    zip: str = Field(..., max_length=20, description="Postal/ZIP code")
    country: str = Field(default="US", max_length=2, description="2-letter ISO country code")
    phone: str | None = Field(None, max_length=20, description="Contact phone")
    email: str | None = Field(None, max_length=100, description="Contact email")
    company: str | None = Field(None, max_length=100, description="Company name")


class ParcelModel(BaseModel):
    """Parcel model with dimension and weight constraints."""

    length: float = Field(..., gt=0, le=108, description="Length in inches (max 108)")
    width: float = Field(..., gt=0, le=108, description="Width in inches (max 108)")
    height: float = Field(..., gt=0, le=108, description="Height in inches (max 108)")
    weight: float = Field(..., gt=0, le=2400, description="Weight in ounces (max 150 lbs)")


class ShipmentResponse(BaseModel):
    status: str
    shipment_id: str | None = None
    tracking_number: str | None = None
    label_url: str | None = None
    rate: str | None = None
    carrier: str | None = None
    error: str | None = None


class TrackingEvent(BaseModel):
    timestamp: str
    status: str
    message: str
    location: str | None = None


class TrackingResponse(BaseModel):
    status: str
    data: dict[str, Any] | None = None
    message: str | None = None
    timestamp: str


class RatesResponse(BaseModel):
    status: str
    data: list[dict[str, Any]] | None = None
    message: str | None = None
    timestamp: str


class EasyPostService:
    """
    Async wrapper for EasyPost SDK with parallel execution support.

    ASYNC/SYNC PATTERN EXPLANATION:
    --------------------------------
    The EasyPost SDK is synchronous (blocking I/O), but FastAPI and MCP servers
    are async. To prevent blocking the event loop, we use this pattern:

    1. PUBLIC API: Async methods (create_shipment, get_rates, etc.)
       - Called by FastAPI/MCP handlers
       - Use `await loop.run_in_executor()` to run sync code in thread pool
       - Don't block the event loop

    2. PRIVATE IMPLEMENTATION: Sync methods (_create_shipment_sync, etc.)
       - Actual EasyPost SDK calls
       - Run in ThreadPoolExecutor threads
       - Can safely block (not on event loop)

    WHY THIS PATTERN:
    - EasyPost SDK: Synchronous, blocks during HTTP requests
    - FastAPI: Async framework, expects non-blocking operations
    - ThreadPoolExecutor: Offloads blocking I/O to thread pool
    - Event loop: Stays responsive, handles other requests concurrently

    PERFORMANCE:
    - 32-40 parallel workers (scales with CPU cores)
    - Multiple shipment operations can run concurrently
    - Event loop never blocks on API calls
    - ~3-4 shipments/second on M3 Max

    EXAMPLE:
    ```python
    # Async method (public API) - doesn't block event loop
    async def create_shipment(...):
        result = await loop.run_in_executor(
            self.executor,
            self._create_shipment_sync,  # Sync method
            ...
        )
        return result

    # Sync method (private) - runs in thread pool, can block
    def _create_shipment_sync(...):
        shipment = self.client.shipment.create(...)  # Blocking SDK call
        return result
    ```

    This pattern is INTENTIONAL and necessary for proper async operation.
    Do not remove the sync methods or ThreadPoolExecutor.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = easypost.EasyPostClient(api_key)
        self.logger = logging.getLogger(__name__)

        # Scale ThreadPoolExecutor with CPU cores (M3 Max: 16 cores, 128GB RAM)
        cpu_count = multiprocessing.cpu_count()  # 16 cores
        max_workers = min(40, cpu_count * 2)  # 32-40 workers for I/O-bound tasks
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.logger.info(
            f"ThreadPoolExecutor initialized: {max_workers} workers on {cpu_count} cores"
        )

    async def create_shipment(
        self,
        to_address: dict[str, Any],
        from_address: dict[str, Any],
        parcel: dict[str, Any],
        carrier: str = "USPS",
        service: str | None = None,
        buy_label: bool = True,
        customs_info: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a shipment and optionally purchase label.

        Args:
            to_address: Destination address dict with name, street1, city, state, zip
            from_address: Origin address dict with same structure
            parcel: Package dimensions dict with length, width, height, weight
            carrier: Shipping carrier preference (default: "USPS")
            service: Specific service (e.g., "FEDEX_GROUND", "Priority") - if None, uses lowest rate
            buy_label: Whether to purchase label immediately (default: True)
            customs_info: Optional customs info for international shipments

        Returns:
            Dict with status, shipment data (id, tracking_code, rates, etc.)
        """
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                self.executor,
                self._create_shipment_sync,
                to_address,
                from_address,
                parcel,
                carrier,
                service,
                buy_label,
                customs_info,
            )
        except Exception as e:
            self.logger.error(f"Error creating shipment: {self._sanitize_error(e)}")
            return {"status": "error", "message": "Failed to create shipment"}

    def _create_shipment_sync(
        self,
        to_address: dict[str, Any],
        from_address: dict[str, Any],
        parcel: dict[str, Any],
        carrier: str,
        service: str | None,
        buy_label: bool,
        customs_info: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Synchronous shipment creation with optional label purchase."""
        try:
            service_info = f" / {service}" if service else ""
            self.logger.info(f"Creating shipment with {carrier}{service_info}")

            # For international shipments, create customs_info if not provided
            shipment_params = {
                "to_address": to_address,
                "from_address": from_address,
                "parcel": parcel,
            }

            if customs_info:
                # Pass CustomsInfo object directly (not the ID)
                shipment_params["customs_info"] = customs_info

            shipment = self.client.shipment.create(**shipment_params)

            # Get all rates
            rates = [
                {
                    "id": rate.id,
                    "carrier": rate.carrier,
                    "service": rate.service,
                    "rate": rate.rate,
                    "delivery_days": rate.delivery_days,
                }
                for rate in shipment.rates
            ]

            result = {
                "status": "success",
                "id": shipment.id,
                "tracking_code": shipment.tracking_code,
                "rates": rates,
            }

            # Optionally buy label
            if buy_label:
                rate = None

                # If specific service requested, find matching rate
                if service:
                    for r in shipment.rates:
                        # Flexible carrier matching: exact or partial match
                        # (e.g., "FedEx" matches "FedExDefault")
                        carrier_match = (
                            r.carrier == carrier
                            or carrier.lower() in r.carrier.lower()
                            or r.carrier.lower() in carrier.lower()
                        )
                        if carrier_match and r.service == service:
                            rate = r
                            self.logger.info(
                                f"Found matching rate: {r.carrier} {service} - ${r.rate} "
                                f"(matched carrier '{carrier}')"
                            )
                            break

                    if not rate:
                        self.logger.warning(
                            f"Service {service} not available for {carrier}, using lowest rate"
                        )

                # Fall back to lowest rate if service not found or not specified
                if not rate:
                    try:
                        rate = shipment.lowest_rate([carrier])
                    except Exception:
                        # If carrier not available, use absolute lowest rate
                        self.logger.warning(
                            f"No rates found for {carrier}, using lowest available rate"
                        )
                        rate = shipment.lowest_rate()

                # Buy the label using the client service
                bought_shipment = self.client.shipment.buy(shipment.id, rate=rate)
                result["postage_label_url"] = bought_shipment.postage_label.label_url
                result["purchased_rate"] = {
                    "carrier": rate.carrier,
                    "service": rate.service,
                    "rate": rate.rate,
                }
                result["tracking_code"] = bought_shipment.tracking_code

            self.logger.info(f"Shipment created: {shipment.id}")
            return result

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Failed to create shipment: {error_msg}", exc_info=True)
            # Include full error details for debugging
            return {"status": "error", "message": error_msg, "error_type": type(e).__name__}

    async def refund_shipment(self, shipment_id: str) -> dict[str, Any]:
        """
        Refund a shipment.

        Args:
            shipment_id: The shipment ID to refund

        Returns:
            Dict with status and refund information
        """
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                self.executor, self._refund_shipment_sync, shipment_id
            )
        except Exception as e:
            self.logger.error(f"Error refunding shipment: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "message": "Failed to refund shipment",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _refund_shipment_sync(self, shipment_id: str) -> dict[str, Any]:
        """Synchronous shipment refund."""
        try:
            self.logger.info(f"Refunding shipment {shipment_id}")
            shipment = self.client.shipment.retrieve(shipment_id)
            refund = self.client.shipment.refund(shipment.id)

            return {
                "status": "success",
                "data": {
                    "shipment_id": shipment.id,
                    "tracking_code": shipment.tracking_code,
                    "refund_status": (
                        refund.refund_status if hasattr(refund, "refund_status") else "submitted"
                    ),
                    "carrier": (
                        shipment.selected_rate.carrier if shipment.selected_rate else "unknown"
                    ),
                    "amount": shipment.selected_rate.rate if shipment.selected_rate else "unknown",
                },
                "message": "Refund request submitted successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Failed to refund shipment: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }

    async def buy_shipment(self, shipment_id: str, rate_id: str) -> dict[str, Any]:
        """
        Purchase a label for an existing shipment.

        Args:
            shipment_id: The shipment ID
            rate_id: The rate ID to purchase

        Returns:
            Dict with status and label information
        """
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                self.executor, self._buy_shipment_sync, shipment_id, rate_id
            )
        except Exception as e:
            self.logger.error(f"Error buying shipment: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "message": "Failed to purchase label",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _buy_shipment_sync(self, shipment_id: str, rate_id: str) -> dict[str, Any]:
        """Synchronous label purchase."""
        try:
            self.logger.info(f"Buying label for shipment {shipment_id}")
            shipment = self.client.shipment.retrieve(shipment_id)
            shipment.buy(rate=rate_id)

            return {
                "status": "success",
                "data": {
                    "shipment_id": shipment.id,
                    "tracking_code": shipment.tracking_code,
                    "postage_label_url": shipment.postage_label.label_url,
                    "rate": shipment.selected_rate.rate,
                    "carrier": shipment.selected_rate.carrier,
                },
                "message": "Label purchased successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Failed to buy shipment: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }

    async def get_tracking(self, tracking_number: str) -> dict[str, Any]:
        """
        Get tracking information for a shipment.

        Args:
            tracking_number: The tracking number to look up

        Returns:
            Dict with status, tracking data, and timestamp
        """
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                self.executor, self._get_tracking_sync, tracking_number
            )
        except Exception as e:
            self.logger.error(f"Error getting tracking: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": None,
                "message": "Failed to retrieve tracking information",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _get_tracking_sync(self, tracking_number: str) -> dict[str, Any]:
        """Synchronous tracking retrieval."""
        try:
            self.logger.info(f"Fetching tracking for {tracking_number}")
            tracker = self.client.tracker.retrieve(tracking_number)

            return {
                "status": "success",
                "data": {
                    "tracking_number": tracker.tracking_code,
                    "status_detail": tracker.status,
                    "updated_at": str(tracker.updated_at),
                    "events": (
                        [
                            {
                                "timestamp": str(
                                    getattr(
                                        event, "timestamp", getattr(event, "datetime", "unknown")
                                    )
                                ),
                                "status": getattr(event, "status", "unknown"),
                                "message": getattr(event, "message", "unknown"),
                                "location": getattr(event, "location", None),
                            }
                            for event in tracker.tracking_details
                        ]
                        if hasattr(tracker, "tracking_details") and tracker.tracking_details
                        else []
                    ),
                },
                "message": "Tracking retrieved successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Failed to get tracking: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": None,
                "message": "Failed to retrieve tracking information",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    async def get_rates(
        self, to_address: dict[str, Any], from_address: dict[str, Any], parcel: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Get available shipping rates.

        Args:
            to_address: Destination address dict
            from_address: Origin address dict
            parcel: Package dimensions dict

        Returns:
            Dict with status, rates data, and timestamp
        """
        try:
            loop = asyncio.get_running_loop()
            rates = await loop.run_in_executor(
                self.executor, self._get_rates_sync, to_address, from_address, parcel
            )
            return {
                "status": "success",
                "data": rates,
                "message": "Rates retrieved successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error getting rates: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": None,
                "message": "Failed to retrieve rates",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _get_rates_sync(
        self, to_address: dict[str, Any], from_address: dict[str, Any], parcel: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Synchronous rates retrieval."""
        try:
            self.logger.info("Calculating rates...")
            shipment = self.client.shipment.create(
                to_address=to_address, from_address=from_address, parcel=parcel
            )

            return [
                {
                    "id": rate.id,
                    "carrier": rate.carrier,
                    "service": rate.service,
                    "rate": rate.rate,
                    "delivery_days": rate.delivery_days,
                }
                for rate in shipment.rates
            ]
        except Exception as e:
            self.logger.error(f"Failed to get rates: {self._sanitize_error(e)}")
            return []

    async def list_shipments(
        self,
        page_size: int = 10,
        purchased: bool = True,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        before_id: str | None = None,  # noqa: ARG002 - Reserved for pagination
    ) -> dict[str, Any]:
        """
        Get list of shipments from EasyPost API.

        Args:
            page_size: Number of shipments to retrieve (max 100)
            purchased: Only include purchased shipments
            start_datetime: ISO 8601 datetime string for filtering
            end_datetime: ISO 8601 datetime string for filtering
            before_id: Pagination cursor (optional)

        Returns:
            Dict with shipments list and pagination info
        """
        return await self.get_shipments_list(
            page_size=page_size,
            purchased=purchased,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

    async def get_shipments_list(
        self,
        page_size: int = 10,
        purchased: bool = True,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
    ) -> dict[str, Any]:
        """
        Get list of shipments from EasyPost API (legacy name).

        Args:
            page_size: Number of shipments to retrieve (max 100)
            purchased: Only include purchased shipments
            start_datetime: ISO 8601 datetime string for filtering
            end_datetime: ISO 8601 datetime string for filtering

        Returns:
            Dict with shipments list and pagination info
        """
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                self.executor,
                self._get_shipments_list_sync,
                page_size,
                purchased,
                start_datetime,
                end_datetime,
            )
        except Exception as e:
            self.logger.error(f"Error getting shipments list: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": [],
                "message": "Failed to retrieve shipments list",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    async def retrieve_shipment(self, shipment_id: str) -> dict[str, Any]:
        """
        Retrieve detailed shipment information from EasyPost.

        Args:
            shipment_id: EasyPost shipment ID

        Returns:
            Dict with shipment details
        """
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                self.executor, self._retrieve_shipment_sync, shipment_id
            )
        except Exception as e:
            self.logger.error(f"Error retrieving shipment: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": None,
                "message": "Failed to retrieve shipment",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _get_shipments_list_sync(
        self,
        page_size: int,
        purchased: bool,
        start_datetime: str | None,
        end_datetime: str | None,
    ) -> dict[str, Any]:
        """Synchronous shipment list retrieval."""
        try:
            self.logger.info(
                f"Retrieving shipments list (page_size={page_size}, purchased={purchased})"
            )

            # Prepare parameters for EasyPost API
            params = {
                "page_size": min(page_size, 100),  # EasyPost max is 100
                "purchased": purchased,
            }

            if start_datetime:
                params["start_datetime"] = start_datetime
            if end_datetime:
                params["end_datetime"] = end_datetime

            # Get shipments from EasyPost using the client
            shipments_response = self.client.shipment.all(**params)

            # Transform shipments to our format
            shipments = [
                self._shipment_to_dict(shipment) for shipment in shipments_response.shipments
            ]

            self.logger.info(f"Retrieved {len(shipments)} shipments from EasyPost")

            return {
                "status": "success",
                "data": shipments,
                "message": f"Successfully retrieved {len(shipments)} shipments",
                "has_more": len(shipments) == page_size,  # Simple heuristic
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Failed to get shipments list: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": [],
                "message": "Failed to retrieve shipments list",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _retrieve_shipment_sync(self, shipment_id: str) -> dict[str, Any]:
        """Synchronous shipment retrieval."""
        try:
            self.logger.info(f"Retrieving shipment {shipment_id}")
            shipment = self.client.shipment.retrieve(shipment_id)
            shipment_data = self._shipment_to_dict(shipment)

            return {
                "status": "success",
                "data": shipment_data,
                "message": f"Shipment {shipment_id} retrieved",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Failed to retrieve shipment: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": None,
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _shipment_to_dict(self, shipment: Any) -> dict[str, Any]:
        """Normalize EasyPost shipment object to serializable dict."""

        def address_to_dict(address_obj: Any) -> dict[str, Any]:
            if not address_obj:
                return {}
            return {
                "name": getattr(address_obj, "name", "") or "",
                "company": getattr(address_obj, "company", "") or "",
                "street1": getattr(address_obj, "street1", "") or "",
                "street2": getattr(address_obj, "street2", "") or "",
                "city": getattr(address_obj, "city", "") or "",
                "state": getattr(address_obj, "state", "") or "",
                "zip": getattr(address_obj, "zip", "") or "",
                "country": getattr(address_obj, "country", "") or "",
                "phone": getattr(address_obj, "phone", "") or "",
                "email": getattr(address_obj, "email", "") or "",
            }

        selected_rate = getattr(shipment, "selected_rate", None)
        parcel = getattr(shipment, "parcel", None)
        from_address = address_to_dict(getattr(shipment, "from_address", None))
        to_address = address_to_dict(getattr(shipment, "to_address", None))

        def location_string(address: dict[str, Any]) -> str:
            city = address.get("city", "")
            state = address.get("state", "")
            if city and state:
                return f"{city}, {state}"
            return city or state or ""

        return {
            "id": getattr(shipment, "id", ""),
            "tracking_number": getattr(shipment, "tracking_code", "") or "",
            "status": getattr(shipment, "status", "unknown") or "unknown",
            "created_at": (
                str(shipment.created_at)
                if hasattr(shipment, "created_at") and shipment.created_at is not None
                else None
            ),
            "carrier": getattr(selected_rate, "carrier", "") if selected_rate else "",
            "service": getattr(selected_rate, "service", "") if selected_rate else "",
            "rate": getattr(selected_rate, "rate", "") if selected_rate else "",
            "from_address": from_address,
            "to_address": to_address,
            "parcel": {
                "length": getattr(parcel, "length", None) if parcel else None,
                "width": getattr(parcel, "width", None) if parcel else None,
                "height": getattr(parcel, "height", None) if parcel else None,
                "weight": getattr(parcel, "weight", None) if parcel else None,
            },
            "tracking_url": getattr(shipment, "public_url", None),
            "label_url": getattr(getattr(shipment, "postage_label", None), "label_url", None),
            "from": location_string(from_address),
            "to": location_string(to_address),
        }

    def _sanitize_error(self, error: Exception) -> str:
        """
        Remove sensitive data from error messages.

        Args:
            error: The exception to sanitize

        Returns:
            Sanitized error message without sensitive data
        """
        import re

        msg = str(error)

        # Remove API keys (EasyPost format: EZAKxxxx or EZTKxxxx)
        msg = re.sub(r"(EZAK|EZTK)[a-zA-Z0-9]{32,}", "[API_KEY_REDACTED]", msg, flags=re.IGNORECASE)

        # Remove Bearer tokens
        msg = re.sub(r"Bearer\s+[^\s]+", "Bearer [REDACTED]", msg)

        # Remove email addresses from error messages
        msg = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]", msg
        )

        # Truncate if too long
        if len(msg) > 200:
            msg = msg[:200] + "..."

        return msg
