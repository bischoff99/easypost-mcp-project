"""
I/O operations for bulk shipment creation.

These functions handle all external I/O (EasyPost API, database).
Separated from pure transforms for testability.
"""

import asyncio
import logging

from fastmcp import Context

from src.models.bulk_dto import (
    AddressDTO,
    CustomsInfoDTO,
    ShipmentRequestDTO,
    ShipmentResultDTO,
    VerifiedAddressDTO,
)
from src.services.easypost_service import EasyPostService
from src.services.smart_customs import get_or_create_customs

logger = logging.getLogger(__name__)


async def verify_address_if_needed(
    address: AddressDTO,
    easypost_service: EasyPostService,
    is_international: bool,
    carrier_preference: str | None,
    ctx: Context | None = None,
) -> VerifiedAddressDTO:
    """
    Verify address if international FedEx/UPS shipment.

    I/O operation - calls EasyPost API.
    Complexity: 8
    """
    # Skip verification for domestic or non-FedEx/UPS
    if not is_international:
        return VerifiedAddressDTO(
            address=address, verification_success=True, errors=[], warnings=[]
        )

    preferred_carrier = (carrier_preference or "").upper()
    if "FEDEX" not in preferred_carrier and "UPS" not in preferred_carrier:
        return VerifiedAddressDTO(
            address=address, verification_success=True, errors=[], warnings=[]
        )

    # Preprocess for FedEx
    from src.services.easypost_service import preprocess_address_for_fedex

    # Convert to dict with defaults for None values
    address_dict = address.model_dump(exclude_none=False)
    # Ensure all string fields have defaults (not None)
    for key in ["street1", "street2", "country", "name"]:
        if address_dict.get(key) is None:
            address_dict[key] = ""

    preprocessed = preprocess_address_for_fedex(address_dict)

    if ctx:
        name = preprocessed.get("name", "recipient")
        await ctx.info(f"🔍 Verifying FedEx-preprocessed address for {name}...")

    verify_result = await easypost_service.verify_address(preprocessed, carrier="fedex")

    # Extract verification data
    data = verify_result.get("data", {})
    verification_success = data.get("verification_success", False)
    verified_addr = data.get("address", {})
    errors = data.get("errors", [])
    warnings = data.get("warnings", [])

    if verify_result.get("status") == "success" and verified_addr and verification_success:
        # Use verified address
        verified_address = AddressDTO(**verified_addr)
        if ctx:
            await ctx.info("✅ Address verified and corrected by FedEx")
        return VerifiedAddressDTO(
            address=verified_address,
            verification_success=True,
            errors=[],
            warnings=warnings,
        )

    if verify_result.get("status") == "warning" or (verified_addr and not verification_success):
        # Warnings but still usable
        verified_address = AddressDTO(**verified_addr) if verified_addr else address
        if ctx:
            await ctx.info(f"⚠️  Address verification warnings: {errors}")
        return VerifiedAddressDTO(
            address=verified_address,
            verification_success=False,
            errors=errors,
            warnings=warnings,
        )

    # Verification failed
    error_msg = verify_result.get("message", "Unknown verification error")
    logger.error(f"FedEx address verification FAILED: {error_msg}, Errors: {errors}")
    if ctx:
        await ctx.info(f"❌ Address verification failed: {error_msg}")
    return VerifiedAddressDTO(
        address=address,
        verification_success=False,
        errors=errors,
        warnings=[],
    )


async def prepare_customs_if_international(
    contents: str,
    weight_oz: float,
    easypost_service: EasyPostService,
    from_address: AddressDTO,
    carrier_preference: str | None,
    ctx: Context | None = None,  # noqa: ARG001
) -> CustomsInfoDTO | None:
    """
    Prepare customs info for international shipments.

    I/O operation - calls customs service.
    Complexity: 6
    """
    from src.mcp_server.tools.bulk_tools import get_customs_signer

    incoterm = "DDP" if carrier_preference and "FEDEX" in carrier_preference.upper() else "DDU"
    customs_signer = get_customs_signer(from_address.model_dump())

    loop = asyncio.get_running_loop()
    customs_dict = await loop.run_in_executor(
        None,
        get_or_create_customs,
        contents,
        weight_oz,
        easypost_service.client,
        None,  # Auto-detect value
        customs_signer,
        incoterm,
    )

    if customs_dict:
        return CustomsInfoDTO(**customs_dict)
    return None


async def create_shipment_with_rates(
    request: ShipmentRequestDTO,
    easypost_service: EasyPostService,
    purchase_labels: bool,
    carrier: str | None,
    ctx: Context | None = None,  # noqa: ARG001
) -> ShipmentResultDTO:
    """
    Create shipment via EasyPost API and optionally purchase label.

    I/O operation - calls EasyPost API.
    Complexity: 7
    """
    try:
        # Convert DTOs to dicts for API
        to_dict = request.to_address.model_dump(exclude_none=True)
        from_dict = request.from_address.model_dump(exclude_none=True)
        parcel_dict = request.parcel.model_dump()
        customs_dict = (
            request.customs_info.model_dump(exclude_none=True) if request.customs_info else None
        )

        # Create shipment
        result = await easypost_service.create_shipment(
            to_address=to_dict,
            from_address=from_dict,
            parcel=parcel_dict,
            customs_info=customs_dict,
        )

        if result.get("status") != "success":
            error_msg = result.get("message", "Unknown error")
            return ShipmentResultDTO(
                shipment_id=None,
                errors=[error_msg],
                line_number=0,
            )

        shipment_data = result.get("data", {})
        shipment_id = shipment_data.get("id", "")
        rates = shipment_data.get("rates", [])

        # Purchase label if requested
        selected_rate = None
        tracking_code = None
        label_url = None

        if purchase_labels:
            if carrier:
                # Find rate for specific carrier
                selected_rate = next((r for r in rates if r.get("carrier") == carrier), None)
            else:
                # Use cheapest rate
                selected_rate = (
                    min(rates, key=lambda r: r.get("rate", float("inf"))) if rates else None
                )

            if selected_rate:
                buy_result = await easypost_service.buy_shipment(
                    shipment_id, selected_rate.get("id")
                )
                if buy_result.get("status") == "success":
                    buy_data = buy_result.get("data", {})
                    tracking_code = buy_data.get("tracking_code")
                    label_url = buy_data.get("postage_label", {}).get("label_url")

        return ShipmentResultDTO(
            shipment_id=shipment_id,
            rates=rates,
            selected_rate=selected_rate,
            tracking_code=tracking_code,
            label_url=label_url,
            errors=[],
            line_number=0,
        )

    except Exception as e:
        logger.error(f"Error creating shipment: {e}")
        return ShipmentResultDTO(
            shipment_id=None,
            errors=[str(e)],
            line_number=0,
        )
