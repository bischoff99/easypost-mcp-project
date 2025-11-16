"""
Pure helper functions for bulk shipment operations.

These functions contain no I/O operations - they only transform data.
All functions are testable in isolation and have complexity ≤10.
"""

from typing import Any

from src.mcp_server.tools.bulk_tools import (
    detect_product_category,
    get_warehouse_address,
    parse_dimensions,
    parse_weight,
)
from src.models.bulk_dto import (
    AddressDTO,
    ParcelDTO,
    ShipmentDataDTO,
    ShipmentRequestDTO,
    ValidationResultDTO,
)


def validate_shipment_data(
    data: ShipmentDataDTO, line_number: int
) -> ValidationResultDTO:
    """
    Validate shipment data and parse dimensions/weight.

    Pure function - no I/O operations.
    Complexity: 5
    """
    errors: list[str] = []

    try:
        # Check if dimensions string contains any numbers before parsing
        import re

        if not re.search(r"\d", data.dimensions):
            errors.append(
                f"Invalid dimensions format: '{data.dimensions}' contains no numbers"
            )
            return ValidationResultDTO(
                line=line_number,
                data=data,
                valid=False,
                errors=errors,
            )

        length, width, height = parse_dimensions(data.dimensions)
        weight_oz = parse_weight(data.weight)

        # Validate parsed values are reasonable
        if length <= 0 or width <= 0 or height <= 0:
            errors.append("Invalid dimensions: all values must be positive")
        if weight_oz <= 0:
            errors.append("Invalid weight: must be positive")

        # Basic validation rules
        if weight_oz > 150 * 16:  # 150 lbs max
            errors.append("Package exceeds 150 lbs limit")
        if not data.zip or len(data.zip) < 3:
            errors.append("Invalid postal code")
        if not data.street1:
            errors.append("Missing street address")
        if not data.country:
            errors.append("Missing country")

        return ValidationResultDTO(
            line=line_number,
            data=data,
            length=length,
            width=width,
            height=height,
            weight_oz=weight_oz,
            valid=len(errors) == 0,
            errors=errors,
        )
    except Exception as e:
        return ValidationResultDTO(
            line=line_number,
            valid=False,
            errors=[f"Parse error: {str(e)}"],
        )


def select_warehouse_address(
    data: ShipmentDataDTO,
) -> tuple[AddressDTO, str]:
    """
    Select warehouse address based on custom sender or auto-detection.

    Pure function - no I/O operations.
    Complexity: 4
    Returns: (address, warehouse_info_string)
    """
    # Priority 1: Custom sender address
    if data.sender_address and data.sender_address.get("name"):
        address_dict = data.sender_address
        warehouse_info = f"Custom sender: {address_dict.get('name')}"
        return AddressDTO(**address_dict), warehouse_info

    # Priority 2: Auto-select by category + state
    category = detect_product_category(data.contents)
    origin_state = data.origin_state or "California"
    warehouse_dict = get_warehouse_address(origin_state, category)

    warehouse_name = warehouse_dict.get("company") or warehouse_dict.get(
        "name", "Unknown"
    )
    warehouse_city = warehouse_dict.get("city", "Unknown")
    warehouse_info = f"{warehouse_name} ({warehouse_city}, {origin_state})"

    return AddressDTO(**warehouse_dict), warehouse_info


def build_to_address(data: ShipmentDataDTO) -> AddressDTO:
    """
    Build recipient address from shipment data.

    Pure function - no I/O operations.
    Complexity: 2
    """
    return AddressDTO(
        name=f"{data.recipient_name} {data.recipient_last_name}",
        street1=data.street1,
        street2=data.street2,
        city=data.city,
        state=data.state,
        zip=data.zip,
        country=data.country,
        phone=data.recipient_phone,
        email=data.recipient_email,
    )


def build_parcel(validation_result: ValidationResultDTO) -> ParcelDTO:
    """
    Build parcel DTO from validation result.

    Pure function - no I/O operations.
    Complexity: 1
    """
    if not validation_result.length or not validation_result.weight_oz:
        raise ValueError("Invalid validation result: missing dimensions or weight")

    return ParcelDTO(
        length=validation_result.length,
        width=validation_result.width or 0,
        height=validation_result.height or 0,
        weight=validation_result.weight_oz,
    )


def is_international_shipment(to_address: AddressDTO, from_address: AddressDTO) -> bool:
    """
    Check if shipment is international.

    Pure function - no I/O operations.
    Complexity: 1
    """
    return to_address.country != from_address.country


def build_shipment_request(
    to_address: AddressDTO,
    from_address: AddressDTO,
    parcel: ParcelDTO,
    customs_info: Any | None = None,
    carrier: str | None = None,
    reference: str | None = None,
) -> ShipmentRequestDTO:
    """
    Build complete shipment request DTO.

    Pure function - no I/O operations.
    Complexity: 2
    """
    return ShipmentRequestDTO(
        to_address=to_address,
        from_address=from_address,
        parcel=parcel,
        customs_info=customs_info,
        carrier=carrier,
        reference=reference,
    )


def parse_carrier_preference(preference: str | None) -> tuple[str | None, str | None]:
    """
    Parse carrier preference into carrier and optional service.

    Examples:
        "USPS- First Class Mail" -> ("USPS", "FIRST CLASS")
        "USPS" -> ("USPS", None)
        "FedEx- Priority" -> ("FEDEX", "PRIORITY")

    Returns: (carrier, service_keyword)
    """
    if not preference:
        return None, None

    # Split on dash if present
    if "-" in preference:
        parts = preference.split("-", 1)
        carrier = parts[0].strip().upper()
        service = parts[1].strip().upper()
        # Extract key service words
        if "FIRST" in service and "CLASS" in service:
            return carrier, "FIRSTCLASS"
        if "PRIORITY" in service:
            return carrier, "PRIORITY"
        if "EXPRESS" in service:
            return carrier, "EXPRESS"
        if "GROUND" in service:
            return carrier, "GROUND"
        if "ECONOMY" in service:
            return carrier, "ECONOMY"
        return carrier, service

    return preference.strip().upper(), None


def is_preferred_carrier(easypost_carrier: str, preferred: str) -> bool:
    """
    Check if EasyPost carrier matches preferred carrier.

    Pure function - no I/O operations.
    Complexity: 8
    """
    import logging

    logger = logging.getLogger(__name__)

    if not preferred:
        logger.debug(
            f"[DEBUG] is_preferred_carrier: No preferred carrier set for {easypost_carrier}"
        )
        return False
    easypost_upper = easypost_carrier.upper()
    preferred_upper = preferred.upper()

    logger.debug(
        f"[DEBUG] is_preferred_carrier: Comparing '{easypost_upper}' against '{preferred_upper}'"
    )

    # FedEx matching
    if "FEDEX" in preferred_upper and (
        "FEDEX" in easypost_upper or easypost_upper == "FEDEXDEFAULT"
    ):
        logger.debug("[DEBUG] ✅ MATCH: FedEx carrier matched")
        return True
    # UPS matching
    if "UPS" in preferred_upper and (
        "UPS" in easypost_upper or easypost_upper == "UPSDAP"
    ):
        logger.debug("[DEBUG] ✅ MATCH: UPS carrier matched")
        return True
    # USPS matching
    if "USPS" in preferred_upper and easypost_upper == "USPS":
        logger.debug("[DEBUG] ✅ MATCH: USPS carrier matched")
        return True
    # DHL matching
    if "DHL" in preferred_upper and (
        "DHL" in easypost_upper or "DHEXPRESS" in easypost_upper
    ):
        logger.debug("[DEBUG] ✅ MATCH: DHL carrier matched")
        return True
    # USA Export/Asendia matching
    usa_match = (
        "USA" in preferred_upper
        or "EXPORT" in preferred_upper
        or "ASENDIA" in preferred_upper
    )
    easypost_match = "USAEXPORT" in easypost_upper or "ASENDIA" in easypost_upper
    if usa_match and easypost_match:
        logger.debug("[DEBUG] ✅ MATCH: USA Export/Asendia carrier matched")
        return True

    logger.debug(
        f"[DEBUG] ❌ NO MATCH: '{easypost_upper}' does not match '{preferred_upper}'"
    )
    return False


def mark_preferred_rates(
    rates: list[dict[str, Any]], preferred_carrier: str | None
) -> list[dict[str, Any]]:
    """
    Mark preferred rates based on carrier AND service preference.

    Handles both:
    - "USPS- First Class Mail" -> matches carrier AND service
    - "USPS" -> matches carrier only (any service)

    Pure function - no I/O operations.
    Complexity: 4
    """
    import logging

    logger = logging.getLogger(__name__)

    if not preferred_carrier:
        logger.debug(
            "[DEBUG] mark_preferred_rates: No preferred carrier, returning all rates unmarked"
        )
        return rates

    # Parse carrier and optional service
    carrier_only, service_keyword = parse_carrier_preference(preferred_carrier)
    preferred_upper = preferred_carrier.upper()

    if service_keyword:
        logger.debug(
            f"[DEBUG] mark_preferred_rates: Marking rates for carrier "
            f"'{carrier_only}' + service '{service_keyword}'"
        )
    else:
        logger.debug(
            f"[DEBUG] mark_preferred_rates: Marking rates for preferred carrier '{carrier_only}'"
        )

    marked = []
    for rate in rates:
        carrier_match = is_preferred_carrier(
            rate.get("carrier", ""), carrier_only or preferred_upper
        )

        # If service specified, also check service name
        if carrier_match and service_keyword:
            service_name = rate.get("service", "").upper()
            service_match = service_keyword in service_name
            marked.append({**rate, "preferred": service_match})
            if service_match:
                logger.debug(
                    f"[DEBUG] ✅ MATCH (carrier + service): "
                    f"{rate.get('carrier')} - {rate.get('service')}"
                )
            else:
                logger.debug(
                    f"[DEBUG] ❌ NO MATCH (service): {rate.get('carrier')} - "
                    f"{rate.get('service')} (needs '{service_keyword}')"
                )
        else:
            marked.append({**rate, "preferred": carrier_match})

    preferred_count = sum(1 for r in marked if r.get("preferred"))
    logger.debug(
        f"[DEBUG] mark_preferred_rates: Marked {preferred_count}/{len(marked)} rates as preferred"
    )

    return marked


def select_best_rate(
    rates: list[dict[str, Any]],
    purchase_labels: bool,
    preferred_carrier: str | None = None,
) -> dict[str, Any] | None:
    """
    Select best rate based on carrier and optional service preference.

    Handles two modes:
    1. Specific service (e.g., "USPS- First Class Mail")
       -> Selects EXACT service if available
    2. Carrier only (e.g., "USPS")
       -> Selects CHEAPEST rate from that carrier

    Examples:
        "USPS- First Class Mail" -> Selects FirstClassPackageInternationalService only
        "USPS" -> Selects cheapest USPS rate (First Class if cheapest)
        "FedEx- Priority" -> Selects FedEx Priority service only
        None -> Selects cheapest overall rate

    Pure function - no I/O operations.
    Complexity: 6
    """
    import logging

    logger = logging.getLogger(__name__)

    logger.debug(
        f"[DEBUG] select_best_rate called: purchase_labels={purchase_labels}, "
        f"preferred_carrier={preferred_carrier}"
    )
    logger.debug(f"[DEBUG] Input rates count: {len(rates) if rates else 0}")

    if not rates:
        logger.debug("[DEBUG] No rates available, returning None")
        return None

    # Parse preference to check if specific service requested
    carrier_only, service_keyword = parse_carrier_preference(preferred_carrier)
    if service_keyword:
        logger.debug(
            f"[DEBUG] Specific service requested: {carrier_only} - {service_keyword}"
        )
    elif carrier_only:
        logger.debug(
            f"[DEBUG] Carrier-only preference: {carrier_only} (will select cheapest)"
        )

    # Log all input rates for visibility
    for i, rate in enumerate(rates):
        logger.debug(
            f"[DEBUG] Input rate {i + 1}: {rate.get('carrier')} - "
            f"{rate.get('service')} - ${rate.get('rate')}"
        )

    marked_rates = mark_preferred_rates(rates, preferred_carrier)

    # Log marked rates
    preferred_count = sum(1 for r in marked_rates if r.get("preferred"))
    logger.debug(
        f"[DEBUG] Marked {preferred_count}/{len(marked_rates)} rates as preferred"
    )
    for i, rate in enumerate(marked_rates):
        logger.debug(
            f"[DEBUG] Marked rate {i + 1}: {rate.get('carrier')} - {rate.get('service')} - "
            f"${rate.get('rate')} - preferred={rate.get('preferred', False)}"
        )

    # If purchasing, prefer marked rates, otherwise return cheapest
    if purchase_labels:
        logger.debug("[DEBUG] Purchase mode: selecting from preferred rates first")
        # Filter preferred rates
        preferred_rates = [r for r in marked_rates if r.get("preferred")]
        if preferred_rates:
            logger.debug(f"[DEBUG] Found {len(preferred_rates)} preferred rates")

            # If specific service requested and found, use it (should be only one match)
            if service_keyword and len(preferred_rates) == 1:
                selected = preferred_rates[0]
                logger.debug(
                    f"[DEBUG] ✅ SELECTED (exact service match): {selected.get('carrier')} - "
                    f"{selected.get('service')} - ${selected.get('rate')}"
                )
                return selected
            if service_keyword and len(preferred_rates) > 1:
                # Multiple matches for same service (shouldn't happen), pick cheapest
                logger.debug(
                    f"[DEBUG] Multiple matches for service '{service_keyword}', selecting cheapest"
                )
                selected = min(
                    preferred_rates, key=lambda r: float(r.get("rate", 0) or 0)
                )
                logger.debug(
                    f"[DEBUG] ✅ SELECTED (cheapest matching service): "
                    f"{selected.get('carrier')} - {selected.get('service')} - "
                    f"${selected.get('rate')}"
                )
                return selected

            # No specific service or carrier-only: Return CHEAPEST preferred rate
            selected = min(preferred_rates, key=lambda r: float(r.get("rate", 0) or 0))
            logger.debug(
                f"[DEBUG] ✅ SELECTED (cheapest preferred): {selected.get('carrier')} - "
                f"{selected.get('service')} - ${selected.get('rate')}"
            )
            return selected
        # Fall back to cheapest overall
        logger.debug("[DEBUG] No preferred rates found, selecting cheapest overall")
        selected = min(marked_rates, key=lambda r: float(r.get("rate", 0) or 0))
        logger.debug(
            f"[DEBUG] ✅ SELECTED (cheapest overall): {selected.get('carrier')} - "
            f"{selected.get('service')} - ${selected.get('rate')}"
        )
        return selected

    # Not purchasing - return cheapest
    logger.debug("[DEBUG] Not purchasing: selecting cheapest rate")
    selected = min(marked_rates, key=lambda r: float(r.get("rate", 0) or 0))
    logger.debug(
        f"[DEBUG] ✅ SELECTED (cheapest): {selected.get('carrier')} - "
        f"{selected.get('service')} - ${selected.get('rate')}"
    )
    return selected
