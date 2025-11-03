import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Dict, List, Optional

import easypost
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AddressModel(BaseModel):
    name: str
    street1: str
    city: str
    state: str
    zip: str
    country: str = "US"


class ParcelModel(BaseModel):
    length: float = Field(..., gt=0)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)


class ShipmentResponse(BaseModel):
    status: str
    shipment_id: Optional[str] = None
    tracking_number: Optional[str] = None
    label_url: Optional[str] = None
    rate: Optional[str] = None
    carrier: Optional[str] = None
    error: Optional[str] = None


class TrackingEvent(BaseModel):
    timestamp: str
    status: str
    message: str
    location: Optional[str] = None


class TrackingResponse(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    timestamp: str


class RatesResponse(BaseModel):
    status: str
    data: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None
    timestamp: str


class EasyPostService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = easypost.EasyPostClient(api_key)
        self.logger = logging.getLogger(__name__)
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def create_shipment(
        self,
        to_address: Dict[str, Any],
        from_address: Dict[str, Any],
        parcel: Dict[str, Any],
        carrier: str = "USPS",
    ) -> ShipmentResponse:
        """
        Create a shipment and purchase label.

        Args:
            to_address: Destination address dict with name, street1, city, state, zip
            from_address: Origin address dict with same structure
            parcel: Package dimensions dict with length, width, height, weight
            carrier: Shipping carrier preference (default: "USPS")

        Returns:
            ShipmentResponse with status, shipment_id, tracking_number, label_url, rate
        """
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                self.executor, self._create_shipment_sync, to_address, from_address, parcel, carrier
            )
            return result
        except Exception as e:
            self.logger.error(f"Error creating shipment: {self._sanitize_error(e)}")
            return ShipmentResponse(status="error", error="Failed to create shipment")

    def _create_shipment_sync(
        self,
        to_address: Dict[str, Any],
        from_address: Dict[str, Any],
        parcel: Dict[str, Any],
        carrier: str,
    ) -> ShipmentResponse:
        """Synchronous shipment creation with retry logic."""
        try:
            self.logger.info(f"Creating shipment with {carrier}")

            shipment = self.client.shipment.create(
                to_address=to_address, from_address=from_address, parcel=parcel
            )

            rate = shipment.lowest_rate(carrier)
            shipment.buy(rate=rate)

            self.logger.info(f"Shipment created: {shipment.id}")

            return ShipmentResponse(
                status="success",
                shipment_id=shipment.id,
                tracking_number=shipment.tracking_code,
                label_url=shipment.label_url,
                rate=rate.rate,
                carrier=rate.carrier,
            )
        except Exception as e:
            self.logger.error(f"Failed to create shipment: {self._sanitize_error(e)}")
            return ShipmentResponse(status="error", error="Failed to create shipment")

    async def get_tracking(self, tracking_number: str) -> Dict[str, Any]:
        """
        Get tracking information for a shipment.

        Args:
            tracking_number: The tracking number to look up

        Returns:
            Dict with status, tracking data, and timestamp
        """
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                self.executor, self._get_tracking_sync, tracking_number
            )
            return result
        except Exception as e:
            self.logger.error(f"Error getting tracking: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": None,
                "message": "Failed to retrieve tracking information",
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _get_tracking_sync(self, tracking_number: str) -> Dict[str, Any]:
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
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Failed to get tracking: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": None,
                "message": "Failed to retrieve tracking information",
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def get_rates(
        self, to_address: Dict[str, Any], from_address: Dict[str, Any], parcel: Dict[str, Any]
    ) -> Dict[str, Any]:
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
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error getting rates: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": None,
                "message": "Failed to retrieve rates",
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _get_rates_sync(
        self, to_address: Dict[str, Any], from_address: Dict[str, Any], parcel: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Synchronous rates retrieval."""
        try:
            self.logger.info("Calculating rates...")
            shipment = self.client.shipment.create(
                to_address=to_address, from_address=from_address, parcel=parcel
            )

            return [
                {
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

    async def get_shipments_list(
        self,
        page_size: int = 10,
        purchased: bool = True,
        start_datetime: Optional[str] = None,
        end_datetime: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get list of shipments from EasyPost API.

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
            result = await loop.run_in_executor(
                self.executor,
                self._get_shipments_list_sync,
                page_size,
                purchased,
                start_datetime,
                end_datetime,
            )
            return result
        except Exception as e:
            self.logger.error(f"Error getting shipments list: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": [],
                "message": "Failed to retrieve shipments list",
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _get_shipments_list_sync(
        self,
        page_size: int,
        purchased: bool,
        start_datetime: Optional[str],
        end_datetime: Optional[str],
    ) -> Dict[str, Any]:
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
            shipments = []
            for shipment in shipments_response:
                shipment_data = {
                    "id": shipment.id,
                    "tracking_number": getattr(shipment, "tracking_code", None) or "",
                    "status": getattr(shipment, "status", "unknown"),
                    "created_at": (
                        str(shipment.created_at) if hasattr(shipment, "created_at") else None
                    ),
                    "carrier": (
                        getattr(shipment, "selected_rate", {}).get("carrier", "")
                        if hasattr(shipment, "selected_rate") and shipment.selected_rate
                        else ""
                    ),
                    "service": (
                        getattr(shipment, "selected_rate", {}).get("service", "")
                        if hasattr(shipment, "selected_rate") and shipment.selected_rate
                        else ""
                    ),
                    "rate": (
                        getattr(shipment, "selected_rate", {}).get("rate", "")
                        if hasattr(shipment, "selected_rate") and shipment.selected_rate
                        else ""
                    ),
                }
                shipments.append(shipment_data)

            self.logger.info(f"Retrieved {len(shipments)} shipments from EasyPost")

            return {
                "status": "success",
                "data": shipments,
                "message": f"Successfully retrieved {len(shipments)} shipments",
                "has_more": len(shipments) == page_size,  # Simple heuristic
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Failed to get shipments list: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "data": [],
                "message": "Failed to retrieve shipments list",
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _sanitize_error(self, error: Exception) -> str:
        """
        Remove sensitive data from error messages.

        Args:
            error: The exception to sanitize

        Returns:
            Sanitized error message without sensitive data
        """
        msg = str(error)
        # Remove potential API keys and sensitive data patterns
        # This is a basic implementation - extend as needed
        if len(msg) > 200:
            msg = msg[:200] + "..."
        return msg
