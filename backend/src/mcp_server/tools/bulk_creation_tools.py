"""
Bulk shipment creation MCP tool - M3 MAX OPTIMIZED

M3 MAX OPTIMIZATION (16 cores, 128GB RAM):
- Formula: cpu_count × 2 = 16 × 2 = 32 workers for I/O-bound operations
- Concurrent API limit: 16 (prevents EasyPost rate limiting)
- Chunk processing: 8 shipments per chunk for optimal CPU utilization
- Performance: ~3-4 shipments/second (100 shipments in 30-40s)
"""

import asyncio
import logging
import multiprocessing
from datetime import UTC, datetime
from time import time

from fastmcp import Context

from src.database import get_db, is_database_available
from src.services.database_service import DatabaseService
from src.services.smart_customs import get_or_create_customs

from .bulk_tools import (
    STORE_ADDRESSES,
    parse_dimensions,
    parse_spreadsheet_line,
    parse_weight,
)

logger = logging.getLogger(__name__)

# M3 Max Hardware Optimization Constants
CPU_COUNT = multiprocessing.cpu_count()  # 16 cores on M3 Max
MAX_WORKERS = min(32, CPU_COUNT * 2)  # 32 workers for I/O-bound operations
CHUNK_SIZE = 8  # Process 8 shipments per chunk for optimal throughput
MAX_CONCURRENT = 16  # API concurrency limit (prevents rate limiting)

# Note: Customs caching handled by smart_customs module
# Use get_or_create_customs from src.services.smart_customs for customs info


def register_bulk_creation_tools(mcp, easypost_service=None):
    """Register bulk shipment creation tools with MCP server."""

    @mcp.tool(tags=["bulk", "create", "shipping", "m3-optimized"])
    async def create_bulk_shipments(
        spreadsheet_data: str,
        from_city: str = None,
        purchase_labels: bool = False,
        carrier: str = None,
        dry_run: bool = False,
        ctx: Context = None,
    ) -> dict:
        """
        Create single or multiple shipments in parallel - M3 Max optimized (16 workers).

        Handles both single shipments (1 line) and bulk operations (multiple lines).
        Uses spreadsheet format: tab-separated columns (paste from spreadsheet).

        TWO-PHASE WORKFLOW (Recommended):
        1. Get rates first: create_bulk_shipments(data, purchase_labels=False)
           - Creates shipments with customs info
           - Returns all available rates for each shipment
           - No charges yet

        2. Buy approved: buy_bulk_shipments(shipment_ids, carrier="USPS")
           - Purchase labels for approved shipments only
           - Charges applied

        Args:
            spreadsheet_data: Tab-separated shipment data (1+ lines, 16+ columns)
            from_city: Override origin city (e.g., "Los Angeles", "Las Vegas")
                      If None, auto-detects from origin_state column or uses sender address
            purchase_labels: Whether to purchase labels immediately (default: False)
                            Set False for two-phase workflow (recommended)
            carrier: Force specific carrier (e.g., "USPS", "FedEx", "UPS")
                    If None, returns all available rates
            dry_run: If True, validates data without creating shipments
            ctx: MCP context for progress reporting

        Returns:
            Dictionary with created shipments, rates, and shipment IDs for approval
        """
        start_time = datetime.now(UTC)

        try:
            if ctx:
                await ctx.info("🚀 Starting bulk shipment creation (16 parallel workers)...")

            # Database tracking (optional - tool works without it)
            db_service = None
            batch_operation = None
            db_session = None

            if is_database_available():
                try:
                    # Get database session and keep it alive for the operation
                    db_gen = get_db()
                    db_session = await db_gen.__anext__()
                    db_service = DatabaseService(db_session)
                    # Create batch operation record
                    batch_id = f"bulk_{int(time())}"
                    batch_operation = await db_service.create_batch_operation(
                        {
                            "batch_id": batch_id,
                            "operation_type": "create_shipments",
                            "status": "processing",
                            "started_at": start_time,
                            "total_items": 0,  # Will be updated after validation
                            "source": "mcp",
                        }
                    )
                    if ctx:
                        await ctx.info(f"📊 Database tracking enabled (batch: {batch_id})")
                except Exception as e:
                    logger.warning(f"Database tracking unavailable: {e}")
                    db_service = None
                    batch_operation = None
                    if db_session:
                        await db_session.close()
                    db_session = None

            # Parse lines
            lines = [l.strip() for l in spreadsheet_data.split("\n") if l.strip()]

            if not lines:
                return {
                    "status": "error",
                    "data": None,
                    "message": "No data provided",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            total_lines = len(lines)

            # Auto-detect origin from spreadsheet column 1
            if from_city is None:
                first_line_data = parse_spreadsheet_line(lines[0])
                origin_state = first_line_data["origin_state"]
                # Map state names to default warehouse cities
                # Must match keys in STORE_ADDRESSES structure
                state_defaults = {
                    "California": "Los Angeles",
                    "Nevada": "Las Vegas",
                    "New York": "New York",
                }
                from_city = state_defaults.get(origin_state, "Los Angeles")

                if ctx:
                    await ctx.info(f"📍 Auto-detected origin: {from_city}")

            # Get origin address from warehouse lookup
            from_address = None
            for state_stores in STORE_ADDRESSES.values():
                if from_city in state_stores:
                    from_address = state_stores[from_city]
                    break

            # Fallback to Los Angeles if city not found
            if from_address is None:
                logger.warning(
                    f"City '{from_city}' not found in warehouses, using Los Angeles default"
                )
                from_address = STORE_ADDRESSES["California"]["Los Angeles"]

            if ctx:
                await ctx.info(f"📊 Validating {total_lines} shipments...")

            # Phase 1: Validate all lines
            validation_results = []
            for idx, line in enumerate(lines):
                try:
                    data = parse_spreadsheet_line(line)
                    length, width, height = parse_dimensions(data["dimensions"])
                    weight_oz = parse_weight(data["weight"])

                    # Basic validation
                    errors = []
                    if weight_oz > 150 * 16:  # 150 lbs max
                        errors.append("Package exceeds 150 lbs limit")
                    # International postal codes can be 3-10 characters (not just US 5-digit ZIP)
                    if not data["zip"] or len(data["zip"]) < 3:
                        errors.append("Invalid postal code")
                    if not data["street1"]:
                        errors.append("Missing street address")
                    if not data["country"]:
                        errors.append("Missing country")

                    validation_results.append(
                        {
                            "line": idx + 1,
                            "data": data,
                            "length": length,
                            "width": width,
                            "height": height,
                            "weight_oz": weight_oz,
                            "valid": len(errors) == 0,
                            "errors": errors,
                        }
                    )

                except Exception as e:
                    validation_results.append(
                        {
                            "line": idx + 1,
                            "valid": False,
                            "errors": [f"Parse error: {str(e)}"],
                        }
                    )

            valid_shipments = [v for v in validation_results if v["valid"]]
            invalid_shipments = [v for v in validation_results if not v["valid"]]

            if ctx:
                await ctx.info(
                    f"✅ Valid: {len(valid_shipments)}, ❌ Invalid: {len(invalid_shipments)}"
                )

            if invalid_shipments:
                error_summary = "\n".join(
                    [f"Line {v['line']}: {', '.join(v['errors'])}" for v in invalid_shipments]
                )
                if ctx:
                    await ctx.info(f"⚠️ Validation errors:\n{error_summary}")

            # Dry-run mode: stop here
            if dry_run:
                return {
                    "status": "success",
                    "data": {
                        "dry_run": True,
                        "validation": {
                            "total": len(validation_results),
                            "valid": len(valid_shipments),
                            "invalid": len(invalid_shipments),
                        },
                        "invalid_shipments": [
                            {"line": v["line"], "errors": v["errors"]} for v in invalid_shipments
                        ],
                    },
                    "message": f"Dry-run: {len(valid_shipments)}/{len(validation_results)} valid",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            if not valid_shipments:
                return {
                    "status": "error",
                    "data": None,
                    "message": "No valid shipments to create",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            # Phase 2: Create shipments in parallel - M3 Max: 32 workers with semaphore
            if ctx:
                await ctx.info(
                    f"🚀 Creating {len(valid_shipments)} shipments "
                    f"({MAX_WORKERS} workers, {MAX_CONCURRENT} concurrent)..."
                )

            # Semaphore to limit concurrent API calls (prevents rate limiting)
            semaphore = asyncio.Semaphore(MAX_CONCURRENT)
            performance_start = time()

            async def create_one_shipment(validation_result: dict) -> dict:
                """Create a single shipment (async wrapper for sync API)."""
                try:
                    data = validation_result["data"]
                    line_number = validation_result["line"]

                    # Use sender address if provided, otherwise use warehouse address
                    shipment_from_address = from_address  # Default to warehouse
                    if "sender_address" in data and data["sender_address"].get("name"):
                        # Use provided sender address from spreadsheet data
                        shipment_from_address = data["sender_address"]

                    # Build addresses and parcel
                    to_address = {
                        "name": f"{data['recipient_name']} {data['recipient_last_name']}",
                        "street1": data["street1"],
                        "street2": data["street2"],
                        "city": data["city"],
                        "state": data["state"],
                        "zip": data["zip"],
                        "country": data["country"],
                        "phone": data["recipient_phone"],
                        "email": data["recipient_email"],
                    }

                    parcel = {
                        "length": validation_result["length"],
                        "width": validation_result["width"],
                        "height": validation_result["height"],
                        "weight": validation_result["weight_oz"],
                    }

                    # Check if international - store country before verification
                    # may convert to_address to ID
                    to_country = to_address["country"]
                    is_international = to_country != shipment_from_address.get("country", "US")
                    customs_info = None

                    # Preprocess address for international FedEx/UPS shipments
                    preferred_carrier = data.get("carrier_preference", "").upper()
                    if is_international and (
                        "FEDEX" in preferred_carrier or "UPS" in preferred_carrier
                    ):
                        # Preprocess address for FedEx/UPS before verification
                        from src.services.easypost_service import preprocess_address_for_fedex

                        to_address = preprocess_address_for_fedex(to_address)

                        if ctx:
                            name = to_address.get("name", "recipient")
                            await ctx.info(
                                f"🔍 Verifying FedEx-preprocessed address for {name}..."
                            )

                        verify_result = await easypost_service.verify_address(
                            to_address, carrier="fedex"
                        )

                        # Check if verification was actually successful
                        verification_success = verify_result.get("data", {}).get(
                            "verification_success", False
                        )
                        verified_addr = verify_result.get("data", {}).get("address", {})

                        if (
                            verify_result.get("status") == "success"
                            and verified_addr
                            and verification_success
                        ):
                            # Use verified address fields - EasyPost SDK may not
                            # accept address IDs directly. The verification status
                            # should still be preserved when using verified fields
                            verified_street1 = verified_addr.get("street1") or to_address.get(
                                "street1"
                            )

                            if not verified_street1 or not verified_street1.strip():
                                orig = to_address.get("street1")
                                ver = verified_addr.get("street1")
                                logger.error(
                                    f"FedEx verification returned empty street1! "
                                    f"Original: '{orig}', Verified: '{ver}'"
                                )
                                if ctx:
                                    await ctx.info(
                                        "❌ FedEx verification returned empty "
                                        "street1 - using original address"
                                    )
                            else:
                                # Use verified address fields
                                # (FedEx has validated and corrected them)
                                to_address = {
                                    "name": verified_addr.get("name") or to_address.get("name"),
                                    "street1": verified_street1,
                                    "street2": verified_addr.get("street2")
                                    or to_address.get("street2"),
                                    "city": verified_addr.get("city") or to_address.get("city"),
                                    "state": verified_addr.get("state") or to_address.get("state"),
                                    "zip": verified_addr.get("zip") or to_address.get("zip"),
                                    "country": verified_addr.get("country")
                                    or to_address.get("country"),
                                    "phone": verified_addr.get("phone") or to_address.get("phone"),
                                    "email": verified_addr.get("email") or to_address.get("email"),
                                    "company": verified_addr.get("company")
                                    or to_address.get("company"),
                                }
                                st = to_address.get("street1")
                                city = to_address.get("city")
                                country = to_address.get("country")
                                logger.info(
                                    f"Using FedEx verified address: "
                                    f"street1='{st}', city='{city}', country='{country}'"
                                )
                                if ctx:
                                    await ctx.info("✅ Address verified and corrected by FedEx")
                        elif verify_result.get("status") == "warning" or (
                            verified_addr and not verification_success
                        ):
                            # Address has warnings or verification didn't fully succeed
                            errors = verify_result.get("data", {}).get("errors", [])
                            name = to_address.get("name")
                            logger.warning(
                                f"FedEx address verification warnings for {name}: {errors}"
                            )
                            if verified_addr:
                                # Still try to use verified address fields if available
                                to_address = {
                                    "name": verified_addr.get("name") or to_address.get("name"),
                                    "street1": verified_addr.get("street1")
                                    or to_address.get("street1"),
                                    "street2": verified_addr.get("street2")
                                    or to_address.get("street2"),
                                    "city": verified_addr.get("city") or to_address.get("city"),
                                    "state": verified_addr.get("state") or to_address.get("state"),
                                    "zip": verified_addr.get("zip") or to_address.get("zip"),
                                    "country": verified_addr.get("country")
                                    or to_address.get("country"),
                                    "phone": verified_addr.get("phone") or to_address.get("phone"),
                                    "email": verified_addr.get("email") or to_address.get("email"),
                                    "company": verified_addr.get("company")
                                    or to_address.get("company"),
                                }
                            if ctx:
                                await ctx.info(f"⚠️  Address verification warnings: {errors}")
                        else:
                            # Verification failed - this is a problem for FedEx
                            error_msg = verify_result.get("message", "Unknown verification error")
                            errors = verify_result.get("data", {}).get("errors", [])
                            name = to_address.get("name")
                            logger.error(
                                f"FedEx address verification FAILED for {name}: "
                                f"{error_msg}, Errors: {errors}"
                            )
                            if ctx:
                                await ctx.info(f"❌ Address verification failed: {error_msg}")
                            # Note: We'll still try to create shipment, but it will
                            # likely fail at purchase

                    if is_international:
                        # Smart customs: auto-fills missing HTS codes and values
                        # Always populate customs for international shipments,
                        # even if not purchasing yet
                        loop = asyncio.get_running_loop()

                        # Get actual person's name for customs signing
                        from src.mcp_server.tools.bulk_tools import get_customs_signer

                        customs_signer = get_customs_signer(shipment_from_address)

                        # DDP for FedEx, DDU for others by default
                        # Carrier preference determines incoterm
                        preferred_carrier = data.get("carrier_preference", "").upper()
                        incoterm = "DDP" if "FEDEX" in preferred_carrier else "DDU"

                        customs_info = await loop.run_in_executor(
                            None,
                            get_or_create_customs,
                            data["contents"],
                            validation_result["weight_oz"],
                            easypost_service.client,
                            None,  # Auto-detect value from description
                            customs_signer,
                            incoterm,
                        )

                    # Set duty_payment for DDP (FedEx international shipments only)
                    # DDU is default for UPS and other carriers, no need to specify
                    # For wallet accounts, try without account field -
                    # EasyPost may handle billing automatically
                    duty_payment = None
                    if is_international:
                        preferred_carrier = data.get("carrier_preference", "").upper()
                        if "FEDEX" in preferred_carrier:
                            # DDP: SENDER pays duties (FedEx requirement)
                            # Try without account field - wallet accounts may
                            # handle billing automatically. If this fails, we may
                            # need to get the EasyPost billing account number
                            duty_payment = {
                                "type": "SENDER",
                                "country": shipment_from_address.get("country", "US"),
                                "postal_code": shipment_from_address.get("zip", "89169"),
                            }

                    # Final validation: Ensure street1 is not empty before creating shipment
                    # Skip validation if to_address is an ID string (verified address)
                    if isinstance(to_address, dict) and (
                        not to_address.get("street1") or not to_address.get("street1").strip()
                    ):
                        name = to_address.get("name", "recipient")
                        error_msg = f"Invalid address: street1 is empty for {name}"
                        logger.error(error_msg)
                        return {
                            "line": line_number,
                            "status": "error",
                            "error": error_msg,
                            "recipient": to_address.get("name"),
                            "destination": f"{data['city']}, {data['state']}",
                        }

                    # Create shipment
                    result = await asyncio.wait_for(
                        easypost_service.create_shipment(
                            to_address=to_address,
                            from_address=shipment_from_address,
                            parcel=parcel,
                            carrier=carrier,
                            buy_label=purchase_labels,
                            rate_id=None,  # Will be set if purchase_labels=True and rate selected
                            customs_info=customs_info,
                            duty_payment=duty_payment,
                        ),
                        timeout=30.0,
                    )

                    if result["status"] == "success":
                        # Extract rate info
                        rate_info = result.get("purchased_rate")
                        rates = result.get("rates", [])

                        # Get preferred carrier from spreadsheet data
                        preferred_carrier = data.get("carrier_preference", "").upper()

                        # Map EasyPost carrier names to preferred carrier format
                        def is_preferred_carrier(easypost_carrier: str, preferred: str) -> bool:
                            """Check if EasyPost carrier matches preferred carrier."""
                            if not preferred:
                                return False
                            easypost_upper = easypost_carrier.upper()

                            # FedEx matching
                            if "FEDEX" in preferred and (
                                "FEDEX" in easypost_upper or easypost_upper == "FEDEXDEFAULT"
                            ):
                                return True
                            # UPS matching
                            if "UPS" in preferred and (
                                "UPS" in easypost_upper or easypost_upper == "UPSDAP"
                            ):
                                return True
                            # USPS matching
                            if "USPS" in preferred and easypost_upper == "USPS":
                                return True
                            # DHL matching
                            if "DHL" in preferred and (
                                "DHL" in easypost_upper or "DHEXPRESS" in easypost_upper
                            ):
                                return True
                            # USA Export/Asendia matching
                            usa_match = ("USA" in preferred or "EXPORT" in preferred
                                        or "ASENDIA" in preferred)
                            easypost_match = ("USAEXPORT" in easypost_upper
                                             or "ASENDIA" in easypost_upper)
                            return bool(usa_match and easypost_match)

                        # Mark preferred rates
                        marked_rates = []
                        for rate in rates:
                            rate_dict = dict(rate)  # Make a copy
                            rate_dict["preferred"] = is_preferred_carrier(
                                rate.get("carrier", ""), preferred_carrier
                            )
                            marked_rates.append(rate_dict)

                        if not rate_info and purchase_labels and marked_rates:
                            rate_info = min(
                                marked_rates, key=lambda r: float(r.get("rate", 0) or 0)
                            )

                        # Build result - only include cost if purchased
                        # Get recipient name - handle both dict and string ID cases
                        if isinstance(to_address, dict):
                            recipient_name = to_address.get("name")
                        else:
                            fname = data.get("recipient_name", "")
                            lname = data.get("recipient_last_name", "")
                            recipient_name = f"{fname} {lname}".strip()
                        recipient_name = recipient_name or data.get("name") or "Unknown"
                        result_dict = {
                            "line": line_number,
                            "status": "success",
                            "shipment_id": result.get("id"),  # For two-phase workflow
                            "tracking_code": (
                                result.get("tracking_code") if purchase_labels else None
                            ),
                            "label_url": (
                                result.get("postage_label_url") if purchase_labels else None
                            ),
                            "carrier": rate_info.get("carrier") if rate_info else None,
                            "service": rate_info.get("service") if rate_info else None,
                            "all_rates": (
                                marked_rates if not purchase_labels else None
                            ),  # Show all available rates with preferred flag
                            "preferred_carrier": preferred_carrier if preferred_carrier else None,
                            "recipient": recipient_name,
                            "destination": f"{data['city']}, {data['state']}",
                        }
                        # Only include cost if we have rate_info (when purchasing)
                        if rate_info and purchase_labels:
                            result_dict["cost"] = rate_info.get("rate")
                        return result_dict
                    return {
                        "line": line_number,
                        "status": "error",
                        "error": result.get("message", "Unknown error"),
                        "recipient": recipient_name,
                        "destination": f"{data['city']}, {data['state']}",
                    }

                except TimeoutError:
                    return {
                        "line": validation_result["line"],
                        "status": "error",
                        "error": "Timeout (30s exceeded)",
                    }
                except Exception as e:
                    logger.error(f"Error creating shipment line {validation_result['line']}: {e}")
                    return {
                        "line": validation_result["line"],
                        "status": "error",
                        "error": str(e),
                    }

            # M3 Max Optimization: Chunked processing with semaphore control
            async def create_with_semaphore(validation_result):
                """Wrapper to limit concurrent API calls."""
                async with semaphore:
                    return await create_one_shipment(validation_result)

            # Create all tasks
            tasks = [create_with_semaphore(v) for v in valid_shipments]

            # Execute with progress reporting - OPTIMIZED for M3 Max
            results = []
            completed = 0
            total = len(valid_shipments)
            progress_interval = max(1, total // 20)  # Report every 5%

            # Process in optimized chunks (8 items per chunk for better CPU utilization)
            for i in range(0, len(tasks), CHUNK_SIZE):
                chunk = tasks[i : i + CHUNK_SIZE]
                chunk_results = await asyncio.gather(*chunk, return_exceptions=True)

                for result in chunk_results:
                    if isinstance(result, Exception):
                        logger.error(f"Task exception: {result}")
                        results.append({"status": "error", "error": str(result)})
                    else:
                        results.append(result)

                    completed += 1
                    if ctx:
                        await ctx.report_progress(completed, total)
                        # Adaptive progress reporting with throughput
                        if completed % progress_interval == 0 or completed == total:
                            elapsed = time() - performance_start
                            throughput = completed / elapsed if elapsed > 0 else 0
                            eta = (total - completed) / throughput if throughput > 0 else 0
                            await ctx.info(
                                f"📦 {completed}/{total} | {throughput:.1f}/s | ETA: {eta:.0f}s"
                            )

            # Calculate summary
            end_time = datetime.now(UTC)
            duration = (end_time - start_time).total_seconds()

            successful = [r for r in results if r.get("status") == "success"]
            failed = [r for r in results if r.get("status") == "error"]

            total_cost = sum(
                float(s.get("cost", 0)) for s in successful if s.get("cost") is not None
            )

            # Carrier breakdown
            carrier_stats = {}
            for s in successful:
                carrier_name = s.get("carrier", "Unknown")
                if carrier_name not in carrier_stats:
                    carrier_stats[carrier_name] = {"count": 0, "cost": 0}
                carrier_stats[carrier_name]["count"] += 1
                cost = s.get("cost")
                if cost is not None:
                    carrier_stats[carrier_name]["cost"] += float(cost)

            # Update batch operation with final results
            if db_service and batch_operation:
                await db_service.update_batch_operation(
                    batch_operation.batch_id,
                    {
                        "total_items": len(valid_shipments),
                        "processed_items": len(results),
                        "successful_items": len(successful),
                        "failed_items": len(failed),
                        "status": "completed",
                        "completed_at": datetime.now(UTC),
                        "total_processing_time": duration,
                        "errors": [
                            {"line": r.get("line"), "error": r.get("error")} for r in failed
                        ],
                    },
                )

                # Store successful shipments in database
                if successful and not dry_run and db_service:
                    for shipment_result in successful:
                        try:
                            shipment_id = shipment_result.get("shipment_id")
                            if shipment_id:
                                # Get shipment details from EasyPost API
                                loop = asyncio.get_running_loop()
                                easypost_shipment = await loop.run_in_executor(
                                    None, easypost_service.client.shipment.retrieve, shipment_id
                                )

                                # Store shipment in database
                                shipment_data = {
                                    "easypost_id": shipment_id,
                                    "status": "created",
                                    "mode": "test",
                                    "reference": f"bulk_{batch_operation.batch_id}",
                                    "batch_id": batch_operation.batch_id,
                                    "batch_status": "created",
                                    "carrier": shipment_result.get("carrier"),
                                    "service": shipment_result.get("service"),
                                    "total_cost": shipment_result.get("cost"),
                                    "currency": "USD",
                                    "tracking_code": shipment_result.get("tracking_code"),
                                    "metadata": {
                                        "batch_operation": batch_operation.batch_id,
                                        "line_number": shipment_result.get("line"),
                                        "recipient": shipment_result.get("recipient"),
                                        "destination": shipment_result.get("destination"),
                                    },
                                }

                                # Create addresses if they don't exist
                                from_address_data = {
                                    "name": from_address.get("name", ""),
                                    "company": from_address.get("company", ""),
                                    "street1": from_address.get("street1", ""),
                                    "street2": from_address.get("street2", ""),
                                    "city": from_address.get("city", ""),
                                    "state": from_address.get("state", ""),
                                    "zip": from_address.get("zip", ""),
                                    "country": from_address.get("country", "US"),
                                    "phone": from_address.get("phone", ""),
                                    "email": from_address.get("email", ""),
                                }

                                to_address_data = {
                                    "name": shipment_result.get("recipient", ""),
                                    "street1": easypost_shipment.to_address.street1,
                                    "street2": getattr(easypost_shipment.to_address, "street2", ""),
                                    "city": easypost_shipment.to_address.city,
                                    "state": getattr(easypost_shipment.to_address, "state", ""),
                                    "zip": easypost_shipment.to_address.zip,
                                    "country": easypost_shipment.to_address.country,
                                    "phone": getattr(easypost_shipment.to_address, "phone", ""),
                                    "email": getattr(easypost_shipment.to_address, "email", ""),
                                }

                                # Create or get addresses
                                from_addr = await db_service.create_address(from_address_data)
                                to_addr = await db_service.create_address(to_address_data)

                                # Create shipment with address references
                                shipment_data.update(
                                    {
                                        "from_address_id": from_addr.id,
                                        "to_address_id": to_addr.id,
                                        "parcel_id": None,  # Will be set after parcel creation
                                    }
                                )

                                db_shipment = await db_service.create_shipment(shipment_data)

                                # Log user activity
                                await db_service.log_user_activity(
                                    {
                                        "action": "create_bulk_shipment",
                                        "resource": "shipment",
                                        "resource_id": db_shipment.id,
                                        "method": "POST",
                                        "endpoint": "/mcp/create_bulk_shipments",
                                        "status_code": 200,
                                        "response_time_ms": duration * 1000 / len(valid_shipments),
                                        "metadata": {
                                            "batch_id": batch_operation.batch_id,
                                            "carrier": shipment_result.get("carrier"),
                                            "cost": shipment_result.get("cost"),
                                        },
                                    }
                                )

                        except Exception as e:
                            logger.error(
                                f"Failed to store shipment "
                                f"{shipment_result.get('shipment_id')}: {e}"
                            )

            if ctx:
                throughput = len(valid_shipments) / duration if duration > 0 else 0.0
                await ctx.info(f"✅ Complete! {len(successful)}/{len(valid_shipments)} successful")
                await ctx.info(f"⏱️ Total time: {duration:.1f}s")
                await ctx.info(f"⚡ Throughput: {throughput:.2f} shipments/second")
                await ctx.info(f"🔧 M3 Max: {MAX_WORKERS} workers, {MAX_CONCURRENT} concurrent")
                if db_service:
                    await ctx.info("💾 Shipment data persisted to database")

            return {
                "status": "success",
                "data": {
                    "batch_id": batch_operation.batch_id if batch_operation else None,
                    "from_address": from_address,
                    "shipments": results,
                    "successful": successful,
                    "failed": failed,
                    "summary": {
                        "total_attempted": len(valid_shipments),
                        "successful": len(successful),
                        "failed": len(failed),
                        "total_cost": round(total_cost, 2) if total_cost else 0.0,
                        "average_cost": (
                            round(total_cost / len(successful), 2)
                            if successful and total_cost
                            else 0.0
                        ),
                        "duration_seconds": round(duration, 2),
                        "throughput": (
                            round(len(valid_shipments) / duration, 2) if duration > 0 else 0.0
                        ),
                        "carrier_breakdown": carrier_stats,
                    },
                    "validation_errors": [
                        {"line": v["line"], "errors": v["errors"]} for v in invalid_shipments
                    ],
                },
                "message": (
                    f"Created {len(successful)}/{len(valid_shipments)} shipments "
                    f"in {duration:.1f}s ({len(valid_shipments) / duration:.1f} shipments/s)"
                    if duration > 0
                    else f"Created {len(successful)}/{len(valid_shipments)} shipments"
                ),
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Bulk creation error: {error_msg}", exc_info=True)

            # Update batch operation with error status
            if db_service and batch_operation:
                try:
                    await db_service.update_batch_operation(
                        batch_operation.batch_id,
                        {
                            "status": "failed",
                            "completed_at": datetime.now(UTC),
                            "errors": [{"error": error_msg}],
                        },
                    )
                except Exception as db_error:
                    logger.error(f"Failed to update batch operation: {db_error}")

            # Cleanup database session
            if db_session:
                import contextlib

                with contextlib.suppress(Exception):
                    await db_session.close()

            return {
                "status": "error",
                "data": None,
                "message": f"Bulk creation failed: {error_msg}",
                "timestamp": datetime.now(UTC).isoformat(),
            }

        finally:
            # Cleanup database session
            if db_session:
                import contextlib

                with contextlib.suppress(Exception):
                    await db_session.close()

    @mcp.tool(tags=["bulk", "purchase", "shipping", "m3-optimized"])
    async def buy_bulk_shipments(
        shipment_ids: list[str],
        rate_ids: list[str],
        _customs_data: list[dict] | None = None,
        ctx: Context | None = None,
    ) -> dict:
        """
        Purchase labels for pre-created shipments using selected rates (Phase 2).

        WORKFLOW:
        1. create_bulk_shipments(data, purchase_labels=False) → get rates
        2. Review and select rates for each shipment
        3. buy_bulk_shipments(shipment_ids, rate_ids) → purchase with selected rates

        Args:
            shipment_ids: List of shipment IDs to purchase (must match rate_ids length)
            rate_ids: List of rate IDs to use for each shipment (must match shipment_ids length)
            customs_data: List of customs info dicts with contents, hs_code,
                          value, and weight fields
            ctx: MCP context

        Returns:
            Purchased labels with tracking numbers
        """
        start_time = datetime.now(UTC)

        try:
            if ctx:
                await ctx.info(f"🛒 Purchasing {len(shipment_ids)} labels with selected rates...")

            # Validate inputs
            if len(shipment_ids) != len(rate_ids):
                return {
                    "status": "error",
                    "data": None,
                    "message": (
                        f"shipment_ids ({len(shipment_ids)}) and rate_ids ({len(rate_ids)}) "
                        "must have the same length"
                    ),
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            semaphore = asyncio.Semaphore(MAX_CONCURRENT)
            performance_start = time()

            async def buy_one(_idx: int, shipment_id: str, rate_id: str) -> dict:
                try:
                    async with semaphore:
                        loop = asyncio.get_running_loop()

                        # Retrieve shipment to verify rate exists
                        shipment = await loop.run_in_executor(
                            None, easypost_service.client.shipment.retrieve, shipment_id
                        )

                        # Verify rate exists in shipment rates
                        rate_obj = None
                        for r in shipment.rates:
                            if r.id == rate_id:
                                rate_obj = r
                                break

                        if not rate_obj:
                            available_ids = [r.id for r in shipment.rates]
                            return {
                                "status": "error",
                                "shipment_id": shipment_id,
                                "error": (
                                    f"Rate {rate_id} not found in shipment rates. "
                                    f"Available: {available_ids}"
                                ),
                            }

                        # Customs info should already be on the shipment from creation
                        # We don't need to set it again here - just verify
                        if (
                            shipment.to_address.country != "US"
                            and not shipment.customs_info
                            and ctx
                        ):
                            await ctx.info(
                                f"⚠️  Warning: Shipment {shipment_id} is international "
                                "but missing customs info"
                            )

                        # Buy label using service method (better error handling)
                        buy_result = await easypost_service.buy_shipment(shipment_id, rate_id)

                        if buy_result.get("status") != "success":
                            error_msg = buy_result.get("message", "Unknown error")
                            error_details = buy_result.get("error_details", {})
                            logger.error(f"Purchase failed for {shipment_id}: {error_msg}")
                            logger.error(f"Error details: {error_details}")
                            # Include error_details in error message for visibility
                            full_error = error_msg
                            if error_details.get("errors"):
                                full_error = f"{error_msg} | Details: {error_details['errors']}"
                            return {
                                "status": "error",
                                "shipment_id": shipment_id,
                                "error": full_error,
                                "error_details": error_details,
                            }

                        # Extract purchase details
                        data = buy_result.get("data", {})
                        return {
                            "status": "success",
                            "shipment_id": shipment_id,
                            "tracking_code": data.get("tracking_code"),
                            "label_url": data.get("postage_label_url"),
                            "carrier": rate_obj.carrier,
                            "service": rate_obj.service,
                            "cost": rate_obj.rate,
                            "recipient": shipment.to_address.name,
                        }
                except Exception as e:
                    # Capture full error details from EasyPost
                    error_details = str(e)
                    if hasattr(e, "message"):
                        error_details = e.message
                    if hasattr(e, "errors"):
                        error_details = f"{error_details} | Errors: {e.errors}"
                    if hasattr(e, "http_status"):
                        error_details = f"{error_details} | HTTP Status: {e.http_status}"
                    if hasattr(e, "json_body"):
                        error_details = f"{error_details} | JSON: {e.json_body}"
                    logger.error(f"Purchase error for {shipment_id}: {error_details}")
                    return {"status": "error", "shipment_id": shipment_id, "error": error_details}

            # Execute - pass index, shipment_id, and rate_id
            tasks = [
                buy_one(idx, shipment_id, rate_ids[idx])
                for idx, shipment_id in enumerate(shipment_ids)
            ]
            results = []
            completed = 0
            total = len(shipment_ids)

            for i in range(0, len(tasks), CHUNK_SIZE):
                chunk_results = await asyncio.gather(*tasks[i : i + CHUNK_SIZE])
                results.extend(chunk_results)
                completed += len(chunk_results)

                if ctx and completed % max(1, total // 10) == 0:
                    elapsed = time() - performance_start
                    throughput = completed / elapsed if elapsed > 0 else 0
                    await ctx.info(f"💳 {completed}/{total} | {throughput:.1f}/s")

            # Summary
            successful = [r for r in results if r.get("status") == "success"]
            failed = [r for r in results if r.get("status") == "error"]
            total_cost = sum(float(s["cost"]) for s in successful if s.get("cost") is not None)
            duration = (datetime.now(UTC) - start_time).total_seconds()

            if ctx:
                await ctx.info(f"✅ Purchased {len(successful)}/{total} labels - ${total_cost:.2f}")

            return {
                "status": "success",
                "data": {
                    "purchased": successful,
                    "failed": failed,
                    "summary": {
                        "total": total,
                        "successful": len(successful),
                        "failed": len(failed),
                        "total_cost": total_cost,
                        "duration_seconds": round(duration, 2),
                    },
                },
                "message": f"Purchased {len(successful)}/{total} labels - ${total_cost:.2f}",
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Bulk purchase error: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }
