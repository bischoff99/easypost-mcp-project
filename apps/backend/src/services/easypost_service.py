import asyncio
import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from typing import Any

import easypost
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# Country name to ISO 2-letter code mapping for EasyPost API
COUNTRY_CODE_MAP = {
    "UNITED KINGDOM": "GB",
    "NORTHERN IRELAND": "GB",
    "ENGLAND": "GB",
    "SCOTLAND": "GB",
    "WALES": "GB",
    "GERMANY": "DE",
    "SPAIN": "ES",
    "FRANCE": "FR",
    "ITALY": "IT",
    "NETHERLANDS": "NL",
    "THE NETHERLANDS": "NL",
    "BELGIUM": "BE",
    "AUSTRIA": "AT",
    "SWITZERLAND": "CH",
    "POLAND": "PL",
    "SWEDEN": "SE",
    "DENMARK": "DK",
    "NORWAY": "NO",
    "FINLAND": "FI",
    "IRELAND": "IE",
    "PORTUGAL": "PT",
    "GREECE": "GR",
    "CZECH REPUBLIC": "CZ",
    "HUNGARY": "HU",
    "ROMANIA": "RO",
    "BULGARIA": "BG",
    "CROATIA": "HR",
    "SLOVAKIA": "SK",
    "SLOVENIA": "SI",
    "LUXEMBOURG": "LU",
    "ESTONIA": "EE",
    "LATVIA": "LV",
    "LITHUANIA": "LT",
    "MALTA": "MT",
    "CYPRUS": "CY",
    "CANADA": "CA",
    "MEXICO": "MX",
    "AUSTRALIA": "AU",
    "NEW ZEALAND": "NZ",
    "JAPAN": "JP",
    "SOUTH KOREA": "KR",
    "KOREA": "KR",
    "CHINA": "CN",
    "INDIA": "IN",
    "SINGAPORE": "SG",
    "HONG KONG": "HK",
    "TAIWAN": "TW",
    "THAILAND": "TH",
    "MALAYSIA": "MY",
    "INDONESIA": "ID",
    "PHILIPPINES": "PH",
    "VIETNAM": "VN",
    "BRAZIL": "BR",
    "ARGENTINA": "AR",
    "CHILE": "CL",
    "COLOMBIA": "CO",
    "PERU": "PE",
    "SOUTH AFRICA": "ZA",
    "ISRAEL": "IL",
    "TURKEY": "TR",
    "SAUDI ARABIA": "SA",
    "UAE": "AE",
    "UNITED ARAB EMIRATES": "AE",
    "USA": "US",
    "UNITED STATES": "US",
    "UNITED STATES OF AMERICA": "US",
    "US": "US",
}


def normalize_country_code(country: str) -> str:
    """
    Convert country name to ISO 2-letter code for EasyPost API.

    Args:
        country: Country name or code

    Returns:
        ISO 2-letter country code (uppercase)
    """
    if not country:
        return "US"  # Default to US

    country_upper = country.strip().upper()

    # If already a 2-letter code, return as-is
    if len(country_upper) == 2:
        return country_upper

    # Look up in mapping
    return COUNTRY_CODE_MAP.get(country_upper, country_upper)


def normalize_address(address: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize address data for EasyPost API.

    Ensures country codes are ISO 2-letter format and trims whitespace.

    Args:
        address: Address dictionary

    Returns:
        Normalized address dictionary
    """
    if not address:
        return address

    normalized = address.copy()

    # Normalize country code
    if "country" in normalized:
        normalized["country"] = normalize_country_code(normalized["country"])

    # Trim whitespace from all string fields (preserve None values)
    for key, value in normalized.items():
        if isinstance(value, str):
            normalized[key] = value.strip()
        elif value is None:
            # Keep None values (don't convert to empty string)
            pass

    return normalized


def preprocess_address_for_fedex(address: dict[str, Any]) -> dict[str, Any]:
    """
    Reformat address to meet FedEx/UPS international API requirements.

    Both FedEx and UPS have strict validation for international addresses:
    - State field must be removed for non-US addresses (max 5 chars, rejects long values)
    - FedEx doesn't accept descriptive text in street2 (building names like "FOUR WINDS")
    - street1 max 35 characters for FedEx
    - UPS Worldwide Economy has 36" girth limit (length + width + height)

    Args:
        address: Address dict to preprocess

    Returns:
        Preprocessed address dict with state removed for international addresses
    """
    result = address.copy()
    street1 = result.get("street1", "").strip()
    street2 = result.get("street2", "").strip()
    country = result.get("country", "").upper()

    # For non-US addresses, remove state field entirely (UPS/FedEx requirements)
    if country and country != "US" and "state" in result:
        del result["state"]  # Remove entirely, not just set to empty/None

    # Handle descriptive street2 (building names, etc.)
    # FedEx often rejects these, so combine with street1 or drop
    if street2:
        # If street2 is short (likely a building name), try combining
        if len(street2.split()) <= 3 and len(street1) + len(street2) + 2 <= 35:
            # Combine into street1 if it fits
            result["street1"] = f"{street1}, {street2}"
            result["street2"] = ""
        elif len(street2.split()) <= 3:
            # Too long to combine - drop street2
            result["street1"] = street1
            result["street2"] = ""
        else:
            # Keep longer street2 (likely apartment/suite number)
            result["street1"] = street1[:35]
            result["street2"] = street2[:35]

    return result


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

    # Carrier accounts: Specific carrier account IDs for this API key
    # These accounts are linked to the production API key
    CARRIER_ACCOUNTS = [
        "ca_8d3eea38c88c408c8d351859d1ed3a1a",  # DHL eCommerce
        "ca_cc276f79f2c04640bcc2623f6790cde7",  # DHL Express
        "ca_4dd19ccfd9cf425bbe90fb6e13ebbf6c",  # FedEx Wallet
        "ca_39ef64ac3d674f2b9e332efe5bec379e",  # UPS (UPSDAP: 09E1D3)
        "ca_5e187e0f2e2f419fb347822000e141b8",  # USA Export - Powered by Asendia
        "ca_058c52faac6144a3bbc5f653364cb981",  # USPS
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

        # Validate API key format before initialization
        if not api_key:
            raise ValueError("EasyPost API key is required")

        if not (api_key.startswith("EZAK") or api_key.startswith("EZTK")):
            self.logger.warning(f"API key format unexpected: {api_key[:10]}...")

        self.logger.info(f"Initializing EasyPost client with key: {api_key[:10]}...")
        self.client = easypost.EasyPostClient(api_key)

        # Add HTTP hooks for monitoring
        self.client.subscribe_to_request_hook(self._log_api_request)
        self.client.subscribe_to_response_hook(self._log_api_response)

        # Simplified for personal use: 4 workers (plenty for API concurrency)
        cpu_count = multiprocessing.cpu_count()
        max_workers = 4  # Fixed 4 workers for I/O-bound tasks
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.logger.info(
            f"ThreadPoolExecutor initialized: {max_workers} workers on {cpu_count} cores"
        )

    def shutdown(self):
        """Shutdown ThreadPoolExecutor gracefully."""
        if hasattr(self, "executor"):
            self.logger.info("Shutting down EasyPost service ThreadPoolExecutor...")
            self.executor.shutdown(wait=True, cancel_futures=False)
            self.logger.info("ThreadPoolExecutor shutdown complete")

    async def _api_call_with_retry(self, func: callable, *args, max_retries: int = 3) -> Any:
        """
        Execute API call with exponential backoff on rate limits.

        Handles 429 (rate limit) errors with progressive delays.

        Args:
            func: Sync function to execute in thread pool
            *args: Positional arguments for func
            max_retries: Maximum retry attempts (default: 3)

        Returns:
            Function result

        Raises:
            Exception: If max retries exceeded or non-retryable error
        """
        import random

        for attempt in range(max_retries):
            try:
                loop = asyncio.get_running_loop()
                return await loop.run_in_executor(self.executor, func, *args)
            except Exception as e:
                # Check if it's a rate limit error (429)
                is_rate_limit = (
                    hasattr(e, "http_status") and e.http_status == 429
                ) or "429" in str(e).lower()

                if is_rate_limit and attempt < max_retries - 1:
                    # Exponential backoff: 2^attempt + random jitter
                    wait_time = (2**attempt) + random.uniform(0, 1)  # noqa: S311
                    self.logger.warning(
                        f"Rate limit hit (attempt {attempt + 1}/{max_retries}), "
                        f"waiting {wait_time:.1f}s..."
                    )
                    await asyncio.sleep(wait_time)
                    continue

                # Non-retryable error or max retries exceeded
                raise

        raise Exception(f"Max retries ({max_retries}) exceeded")

    def _log_api_request(self, **kwargs):
        """Log outgoing API requests for debugging."""
        try:
            method = kwargs.get("method", "UNKNOWN")
            url = kwargs.get("url", "UNKNOWN")
            self.logger.debug(f"EasyPost API Request: {method} {url}")
        except Exception as e:
            self.logger.error(f"Error in request hook: {e}")

    def _log_api_response(self, **kwargs):
        """Log API responses and track errors."""
        try:
            status = kwargs.get("http_status", 0)
            url = kwargs.get("url", "UNKNOWN")

            if status >= 400:
                response_body = kwargs.get("response_body", "N/A")
                self.logger.error(
                    f"EasyPost API Error: {status} - {url}\nResponse: {response_body}"
                )
            elif 200 <= status < 300:
                self.logger.debug(f"EasyPost API Success: {status} - {url}")
        except Exception as e:
            self.logger.error(f"Error in response hook: {e}")

    async def create_shipment(
        self,
        to_address: dict[str, Any] | str,
        from_address: dict[str, Any],
        parcel: dict[str, Any],
        carrier: str = "USPS",
        service: str | None = None,
        buy_label: bool = True,
        rate_id: str | None = None,
        customs_info: dict[str, Any] | None = None,
        duty_payment: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a shipment and optionally purchase label.

        Args:
            to_address: Destination address dict with name, street1, city,
                state, zip, OR address ID string
            from_address: Origin address dict with same structure
            parcel: Package dimensions dict with length, width, height, weight
            carrier: Shipping carrier preference (default: "USPS")
            service: Specific service (e.g., "FEDEX_GROUND", "Priority") - if None, uses lowest rate
            buy_label: Whether to purchase label immediately (default: True)
            rate_id: Required if buy_label=True - the rate ID to use for purchase
            customs_info: Optional customs info for international shipments
            duty_payment: Optional duty payment info for DDP/DDU

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
                rate_id,
                customs_info,
                duty_payment,
            )
        except Exception as e:
            self.logger.error(f"Error creating shipment: {self._sanitize_error(e)}")
            return {"status": "error", "message": "Failed to create shipment"}

    def _create_shipment_sync(
        self,
        to_address: dict[str, Any] | str,
        from_address: dict[str, Any],
        parcel: dict[str, Any],
        carrier: str,
        service: str | None,
        buy_label: bool,
        rate_id: str | None = None,
        customs_info: dict[str, Any] | None = None,
        duty_payment: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Synchronous shipment creation with optional label purchase."""
        try:
            service_info = f" / {service}" if service else ""
            self.logger.info(f"Creating shipment with {carrier}{service_info}")

            # Normalize addresses before API call - don't normalize if already preprocessed
            # EasyPost SDK accepts address dicts
            # Note: to_address may already be preprocessed (state removed for international)
            if isinstance(to_address, dict):
                # Only normalize country code, don't re-add state field
                to_address_param = normalize_address(to_address)
            else:
                to_address_param = to_address

            # Normalize from_address (always a dict)
            from_address_param = normalize_address(from_address)

            # For international shipments, create customs_info if not provided
            shipment_params = {
                "to_address": to_address_param,
                "from_address": from_address_param,
                "parcel": parcel,
            }

            # Add carrier_accounts only if specified (None = use all enabled accounts)
            if self.CARRIER_ACCOUNTS is not None:
                shipment_params["carrier_accounts"] = self.CARRIER_ACCOUNTS

            if customs_info:
                # Create CustomsInfo object using EasyPost SDK
                # customs_info dict should have: customs_items (list), customs_certify,
                # customs_signer, etc.
                # Note: EasyPost API requires 'weight' for each customs_item
                customs_items = []
                total_value = 0.0
                for item in customs_info.get("customs_items", customs_info.get("contents", [])):
                    # Weight is REQUIRED by EasyPost API - use item weight or parcel weight
                    item_weight = item.get("weight")
                    if item_weight is None:
                        # Fallback: use parcel weight if item weight not specified
                        item_weight = parcel.get("weight", 16.0)  # Default 1 lb if missing

                    # Calculate total value for EEL/PFC validation
                    quantity = item.get("quantity", 1)
                    value = item.get("value", 50.0)
                    total_value += quantity * value

                    customs_item = self.client.customs_item.create(
                        description=item.get("description", "General Merchandise"),
                        quantity=quantity,
                        value=value,
                        weight=item_weight,  # REQUIRED by EasyPost API
                        hs_tariff_number=item.get("hs_tariff_number"),
                        origin_country=item.get("origin_country", "US"),
                    )
                    customs_items.append(customs_item)

                # Validate EEL/PFC requirement (per EasyPost customs guide)
                eel_pfc = customs_info.get("eel_pfc")
                if eel_pfc is None:
                    if total_value >= 2500:
                        raise ValueError(
                            f"Shipment value ${total_value:.2f} ≥ $2,500 requires AES ITN. "
                            "Get ITN from https://aesdirect.census.gov or use "
                            "smart_customs.extract_customs_smart() for automatic validation. "
                            "Example: 'AES X20120502123456'"
                        )
                    eel_pfc = "NOEEI 30.37(a)"

                customs_info_obj = self.client.customs_info.create(
                    customs_items=customs_items,
                    customs_certify=customs_info.get("customs_certify", True),
                    customs_signer=customs_info.get("customs_signer", ""),
                    contents_type=customs_info.get("contents_type", "merchandise"),
                    restriction_type=customs_info.get("restriction_type", "none"),
                    restriction_comments=customs_info.get("restriction_comments", ""),
                    eel_pfc=eel_pfc,
                    non_delivery_option=customs_info.get("non_delivery_option", "return"),
                )
                shipment_params["customs_info"] = customs_info_obj

            # Add duty_payment for DDP/DDU (FedEx/UPS international shipments)
            if duty_payment:
                shipment_params["duty_payment"] = duty_payment

            shipment = self.client.shipment.create(**shipment_params)

            # Retrieve shipment fresh to ensure all rates are populated from carrier_accounts
            shipment = self.client.shipment.retrieve(shipment.id)

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

            # Optionally buy label - REQUIRES explicit rate_id
            if buy_label:
                if not rate_id:
                    raise ValueError(
                        "rate_id is required when buy_label=True. "
                        "Create shipment first, select a rate, then purchase with buy_shipment()."
                    )

                # Find the rate object matching the rate_id
                rate_obj = None
                for r in shipment.rates:
                    if r.id == rate_id:
                        rate_obj = r
                        break

                if not rate_obj:
                    raise ValueError(
                        f"Rate {rate_id} not found in shipment rates. "
                        f"Available rates: {[r.id for r in shipment.rates]}"
                    )

                # Buy the label using the selected rate
                bought_shipment = self.client.shipment.buy(shipment.id, rate={"id": rate_id})
                result["postage_label_url"] = bought_shipment.postage_label.label_url
                result["purchased_rate"] = {
                    "carrier": rate_obj.carrier,
                    "service": rate_obj.service,
                    "rate": rate_obj.rate,
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
            return await self._api_call_with_retry(self._refund_shipment_sync, shipment_id)
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
            return await self._api_call_with_retry(self._buy_shipment_sync, shipment_id, rate_id)
        except Exception as e:
            self.logger.error(f"Error buying shipment: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "message": "Failed to purchase label",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    async def verify_address(
        self, address: dict[str, Any], carrier: str | None = None
    ) -> dict[str, Any]:
        """
        Verify address with optional carrier-specific verification.

        Args:
            address: Address dictionary to verify
            carrier: Optional carrier name for carrier-grade verification ("fedex", "ups")

        Returns:
            Dict with verification status and verified address
        """
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                self.executor,
                self._verify_address_sync,
                address,
                carrier,
            )
        except Exception as e:
            error_msg = self._sanitize_error(e)
            self.logger.error(f"Error verifying address: {error_msg}")
            return {
                "status": "error",
                "message": f"Failed to verify address: {error_msg}",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _verify_address_sync(
        self, address: dict[str, Any], carrier: str | None = None
    ) -> dict[str, Any]:
        """Synchronous address verification."""
        try:
            # Normalize address first
            normalized = normalize_address(address)

            # Prepare verification params
            verify_params = {"verify": True}  # Always enable standard verification
            if carrier and carrier.lower() in ["fedex", "ups"]:
                # Carrier verification requires verify=True to be set first
                verify_params["verify_carrier"] = carrier.lower()

            # Create and verify address - EasyPost SDK accepts kwargs directly
            verified_address = self.client.address.create(
                street1=normalized.get("street1"),
                street2=normalized.get("street2"),
                city=normalized.get("city"),
                state=normalized.get("state"),
                zip=normalized.get("zip"),
                country=normalized.get("country"),
                name=normalized.get("name"),
                company=normalized.get("company"),
                phone=normalized.get("phone"),
                email=normalized.get("email"),
                **verify_params,
            )

            # Check verification results
            verifications = (
                verified_address.verifications if hasattr(verified_address, "verifications") else {}
            )
            delivery_verification = verifications.get("delivery", {}) if verifications else {}
            carrier_verification = verifications.get("carrier", {}) if carrier else {}

            # Log detailed verification results for debugging
            delivery_success = delivery_verification.get("success", "N/A")
            carrier_success = carrier_verification.get("success", "N/A") if carrier else "N/A"
            self.logger.info("Address verification results:")
            self.logger.info(f"  - Delivery success: {delivery_success}")
            self.logger.info(f"  - Delivery errors: {delivery_verification.get('errors', [])}")
            if carrier:
                self.logger.info(f"  - Carrier ({carrier}) success: {carrier_success}")
                self.logger.info(
                    f"  - Carrier ({carrier}) errors: {carrier_verification.get('errors', [])}"
                )
            self.logger.info(f"  - Original street1: '{normalized.get('street1')}'")
            self.logger.info(f"  - Verified street1: '{verified_address.street1}'")
            self.logger.info(f"  - Original street2: '{normalized.get('street2')}'")
            self.logger.info(f"  - Verified street2: '{verified_address.street2}'")

            success = True
            errors = []

            if delivery_verification and not delivery_verification.get("success", True):
                success = False
                errors.extend(delivery_verification.get("errors", []))

            if carrier_verification and not carrier_verification.get("success", True):
                success = False
                errors.extend(carrier_verification.get("errors", []))

            # Log the verified address street1 for debugging FedEx issues
            self.logger.info(f"Verified address street1: '{verified_address.street1}'")

            status_value = "success" if success else "warning"
            message = (
                "Address verified successfully" if success else "Address verification had warnings"
            )

            return {
                "status": status_value,
                "data": {
                    "address": {
                        "id": verified_address.id,
                        "street1": verified_address.street1,
                        "street2": verified_address.street2,
                        "city": verified_address.city,
                        "state": verified_address.state,
                        "zip": verified_address.zip,
                        "country": verified_address.country,
                        "name": verified_address.name,
                        "company": verified_address.company,
                        "phone": verified_address.phone,
                        "email": verified_address.email,
                    },
                    "verification_success": success,
                    "errors": errors,
                },
                "message": message,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Address verification failed: {self._sanitize_error(e)}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _buy_shipment_sync(self, shipment_id: str, rate_id: str) -> dict[str, Any]:
        """Synchronous label purchase."""
        try:
            self.logger.info(f"Buying label for shipment {shipment_id} with rate {rate_id}")
            shipment = self.client.shipment.retrieve(shipment_id)

            # Find the rate object matching the rate_id
            rate_obj = None
            for rate in shipment.rates:
                if rate.id == rate_id:
                    rate_obj = rate
                    break

            if not rate_obj:
                raise ValueError(f"Rate {rate_id} not found in shipment rates")

            # Log shipment details for debugging - especially address for FedEx
            to_addr = shipment.to_address if hasattr(shipment, "to_address") else None
            street1 = to_addr.street1 if to_addr and hasattr(to_addr, "street1") else None
            has_duty = hasattr(shipment, "duty_payment") and shipment.duty_payment is not None
            self.logger.info(
                f"Shipment details: id={shipment.id}, status={shipment.status}, "
                f"carrier={rate_obj.carrier}, service={rate_obj.service}, "
                f"has_customs={shipment.customs_info is not None}, "
                f"has_duty_payment={has_duty}, "
                f"to_address_street1='{street1}', "
                f"to_address_city='{to_addr.city if to_addr else None}', "
                f"to_address_country='{to_addr.country if to_addr else None}'"
            )

            # Validate address before purchase (especially for FedEx)
            if to_addr and (not street1 or not street1.strip()):
                addr_dict = to_addr.__dict__ if hasattr(to_addr, "__dict__") else "N/A"
                error_msg = f"Invalid address: street1 is empty or None. Address: {addr_dict}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            # Buy the shipment with the rate ID
            # EasyPost API expects: { "rate": { "id": "rate_..." } }
            # Python SDK accepts rate object or rate dict
            bought_shipment = self.client.shipment.buy(shipment_id, rate={"id": rate_id})

            # bought_shipment is the updated shipment object returned by buy()
            return {
                "status": "success",
                "data": {
                    "shipment_id": bought_shipment.id,
                    "tracking_code": bought_shipment.tracking_code,
                    "postage_label_url": (
                        bought_shipment.postage_label.label_url
                        if bought_shipment.postage_label
                        else None
                    ),
                    "purchased_rate": {
                        "rate": (
                            bought_shipment.selected_rate.rate
                            if bought_shipment.selected_rate
                            else None
                        ),
                        "carrier": (
                            bought_shipment.selected_rate.carrier
                            if bought_shipment.selected_rate
                            else None
                        ),
                        "service": (
                            bought_shipment.selected_rate.service
                            if bought_shipment.selected_rate
                            else None
                        ),
                    },
                },
                "message": "Label purchased successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            # Capture detailed error information
            error_msg = str(e)
            error_details = {"message": error_msg}

            # Try to extract more details from EasyPost error object
            if hasattr(e, "message"):
                error_details["message"] = e.message
            if hasattr(e, "errors"):
                error_details["errors"] = e.errors
            if hasattr(e, "http_status"):
                error_details["http_status"] = e.http_status
            if hasattr(e, "json_body"):
                error_details["json_body"] = e.json_body

            self.logger.error(f"Buy error details: {error_details}")
            self.logger.error(f"Failed to buy shipment: {self._sanitize_error(e)}")

            # Return detailed error message
            detailed_error = error_msg
            if error_details.get("errors"):
                detailed_error = f"{error_msg} | Details: {error_details['errors']}"

            return {
                "status": "error",
                "message": detailed_error,
                "error_details": error_details,
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
        self,
        to_address: dict[str, Any],
        from_address: dict[str, Any],
        parcel: dict[str, Any],
        customs_info: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Get available shipping rates.

        Args:
            to_address: Destination address dict
            from_address: Origin address dict
            parcel: Package dimensions dict
            customs_info: Optional customs info dict for international shipments

        Returns:
            Dict with status, rates data, and timestamp
        """
        try:
            loop = asyncio.get_running_loop()
            rates = await loop.run_in_executor(
                self.executor,
                self._get_rates_sync,
                to_address,
                from_address,
                parcel,
                customs_info,
            )
            return {
                "status": "success",
                "data": rates,
                "message": "Rates retrieved successfully",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        except Exception as e:
            error_msg = self._sanitize_error(e)
            self.logger.error(f"Error getting rates: {error_msg}")
            return {
                "status": "error",
                "data": None,
                "message": f"Failed to retrieve rates: {error_msg}",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    def _get_rates_sync(
        self,
        to_address: dict[str, Any],
        from_address: dict[str, Any],
        parcel: dict[str, Any],
        customs_info: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Synchronous rates retrieval."""
        try:
            self.logger.info(f"Calculating rates... (API key: {self.api_key[:10]}...)")

            # Normalize addresses before API call
            to_address = normalize_address(to_address)
            from_address = normalize_address(from_address)

            from_city = from_address.get("city")
            from_state = from_address.get("state")
            from_country = from_address.get("country")
            self.logger.info(f"From: {from_city}, {from_state}, {from_country}")
            to_city = to_address.get("city")
            to_state = to_address.get("state")
            to_country = to_address.get("country")
            self.logger.info(f"To: {to_city}, {to_state}, {to_country}")
            length = parcel.get("length")
            width = parcel.get("width")
            height = parcel.get("height")
            weight = parcel.get("weight")
            self.logger.info(f"Parcel: {length}x{width}x{height}, {weight}oz")

            shipment_params = {
                "to_address": to_address,
                "from_address": from_address,
                "parcel": parcel,
            }

            # Add carrier_accounts only if specified (None = use all enabled accounts)
            if self.CARRIER_ACCOUNTS is not None:
                shipment_params["carrier_accounts"] = self.CARRIER_ACCOUNTS

            # Add customs_info if provided (for international shipments)
            if customs_info:
                # Create CustomsInfo object using EasyPost SDK (same as _create_shipment_sync)
                # Note: EasyPost API requires 'weight' for each customs_item
                customs_items = []
                for item in customs_info.get("customs_items", customs_info.get("contents", [])):
                    # Weight is REQUIRED by EasyPost API - use item weight or parcel weight
                    item_weight = item.get("weight")
                    if item_weight is None:
                        # Fallback: use parcel weight if item weight not specified
                        item_weight = parcel.get("weight", 16.0)  # Default 1 lb if missing

                    customs_item = self.client.customs_item.create(
                        description=item.get("description", "General Merchandise"),
                        quantity=item.get("quantity", 1),
                        value=item.get("value", 50.0),
                        weight=item_weight,  # REQUIRED by EasyPost API
                        hs_tariff_number=item.get("hs_tariff_number"),
                        origin_country=item.get("origin_country", "US"),
                    )
                    customs_items.append(customs_item)

                customs_info_obj = self.client.customs_info.create(
                    customs_items=customs_items,
                    customs_certify=customs_info.get("customs_certify", True),
                    customs_signer=customs_info.get("customs_signer", ""),
                    contents_type=customs_info.get("contents_type", "merchandise"),
                    restriction_type=customs_info.get("restriction_type", "none"),
                    restriction_comments=customs_info.get("restriction_comments", ""),
                    eel_pfc=customs_info.get("eel_pfc", "NOEEI 30.37(a)"),
                    non_delivery_option=customs_info.get("non_delivery_option", "return"),
                )
                shipment_params["customs_info"] = customs_info_obj

            shipment = self.client.shipment.create(**shipment_params)

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
            raise

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
