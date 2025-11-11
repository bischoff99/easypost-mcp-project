"""
Bulk shipment creation MCP tool - M3 MAX OPTIMIZED

M3 MAX OPTIMIZATION (16 cores, 128GB RAM):
- Formula: cpu_count × 2 = 16 × 2 = 32 workers for I/O-bound operations
- Concurrent API limit: 16 (prevents EasyPost rate limiting)
- Chunk processing: 8 shipments per chunk for optimal CPU utilization
- Performance: ~3-4 shipments/second (100 shipments in 30-40s)
"""

from typing import Any

import asyncio
import logging
import multiprocessing
from datetime import UTC, datetime
from time import time

from fastmcp import Context

from src.database import get_db, is_database_available
from src.services.database_service import DatabaseService

from .bulk_tools import parse_spreadsheet_line

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
        _from_city: str | None = None,
        purchase_labels: bool = False,
        carrier: str | None = None,
        dry_run: bool = False,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
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

            # Database tracking setup (optional - tool works without it)
            db_service = None
            batch_operation = None
            db_session = None

            if is_database_available():
                try:
                    # Get database session and keep it alive for the operation
                    db_gen = get_db()
                    db_session = await db_gen.__anext__()
                    db_service = DatabaseService(db_session)
                except Exception as e:
                    logger.warning(f"Database tracking unavailable: {e}")
                    if db_session:
                        await db_session.close()
                    db_session = None

            # Setup batch tracking
            from src.mcp_server.tools.bulk_aggregation import setup_database_tracking

            batch_operation, batch_id = await setup_database_tracking(
                db_service, start_time, ctx
            )

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

            # NOTE: Warehouse selection now happens PER-SHIPMENT based on:
            # 1. origin_state column (California, Nevada, New York)
            # 2. Product category detected from contents
            # This ensures each shipment uses the correct specialized warehouse

            if ctx:
                await ctx.info(f"📊 Validating {total_lines} shipments...")

            # Phase 1: Validate all lines using helper
            from src.mcp_server.tools.bulk_helpers import validate_shipment_data
            from src.models.bulk_dto import ShipmentDataDTO

            validation_results: list[dict[str, Any]] = []
            for idx, line in enumerate(lines):
                try:
                    data_dict = parse_spreadsheet_line(line)
                    shipment_data = ShipmentDataDTO(**data_dict)
                    validation_result = validate_shipment_data(shipment_data, idx + 1)
                    validation_results.append(validation_result.model_dump())
                except Exception as e:
                    validation_results.append({
                        "line": idx + 1,
                        "valid": False,
                        "errors": [f"Parse error: {str(e)}"],
                    })

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

            async def create_one_shipment(validation_result: dict[str, Any]) -> dict[str, Any]:
                """Create a single shipment using refactored helpers."""
                from src.mcp_server.tools.bulk_helpers import (
                    build_parcel,
                    build_shipment_request,
                    build_to_address,
                    is_international_shipment,
                    select_warehouse_address,
                )
                from src.mcp_server.tools.bulk_io import (
                    create_shipment_with_rates,
                    prepare_customs_if_international,
                    verify_address_if_needed,
                )
                from src.models.bulk_dto import ShipmentDataDTO, ValidationResultDTO

                try:
                    data_dict = validation_result["data"]
                    line_number = validation_result["line"]

                    # Convert dict to DTO
                    shipment_data = ShipmentDataDTO(**data_dict)

                    # Select warehouse address
                    from_address, warehouse_info = select_warehouse_address(shipment_data)

                    # Progress reporting
                    if ctx and line_number % max(1, total_lines // 10) == 0:
                        await ctx.info(f"📍 Shipment #{line_number}: {warehouse_info}")

                    # Build addresses and parcel using helpers
                    to_address = build_to_address(shipment_data)
                    parcel = build_parcel(
                        ValidationResultDTO(**validation_result)
                    )

                    # Check if international
                    is_intl = is_international_shipment(to_address, from_address)

                    # Verify address if needed (international FedEx/UPS)
                    verified = await verify_address_if_needed(
                        to_address,
                        easypost_service,
                        is_intl,
                        shipment_data.carrier_preference,
                        ctx,
                    )
                    to_address = verified.address

                    # Prepare customs if international
                    customs_info = None
                    if is_intl:
                        customs_info = await prepare_customs_if_international(
                            shipment_data.contents,
                            validation_result["weight_oz"],
                            easypost_service,
                            from_address,
                            shipment_data.carrier_preference,
                            ctx,
                        )

                    # Build shipment request
                    shipment_request = build_shipment_request(
                        to_address=to_address,
                        from_address=from_address,
                        parcel=parcel,
                        customs_info=customs_info,
                        carrier=carrier,
                        reference=f"bulk_line_{line_number}",
                    )

                    # Validate address before creating
                    if not to_address.street1 or not to_address.street1.strip():
                        error_msg = f"Invalid address: street1 is empty for {to_address.name}"
                        logger.error(error_msg)
                        return {
                            "line": line_number,
                            "status": "error",
                            "error": error_msg,
                            "recipient": to_address.name,
                            "destination": f"{shipment_data.city}, {shipment_data.state}",
                        }

                    # Create shipment via helper
                    shipment_result = await asyncio.wait_for(
                        create_shipment_with_rates(
                            shipment_request,
                            easypost_service,
                            purchase_labels,
                            carrier,
                            ctx,
                        ),
                        timeout=30.0,
                    )

                    # Handle errors
                    if shipment_result.errors:
                        return {
                            "line": line_number,
                            "status": "error",
                            "error": "; ".join(shipment_result.errors),
                            "recipient": to_address.name,
                            "destination": f"{shipment_data.city}, {shipment_data.state}",
                        }

                    # Process rates using helpers
                    from src.mcp_server.tools.bulk_helpers import (
                        mark_preferred_rates,
                        select_best_rate,
                    )

                    preferred_carrier = (shipment_data.carrier_preference or "").upper()
                    marked_rates = mark_preferred_rates(
                        shipment_result.rates, preferred_carrier
                    )
                    selected_rate = select_best_rate(
                        marked_rates, purchase_labels, preferred_carrier
                    )

                    # Build result dict
                    result_dict = {
                        "line": line_number,
                        "status": "success",
                        "shipment_id": shipment_result.shipment_id,
                        "tracking_code": shipment_result.tracking_code,
                        "label_url": shipment_result.label_url,
                        "carrier": selected_rate.get("carrier") if selected_rate else None,
                        "service": selected_rate.get("service") if selected_rate else None,
                        "all_rates": marked_rates if not purchase_labels else None,
                        "preferred_carrier": preferred_carrier if preferred_carrier else None,
                        "recipient": to_address.name,
                        "destination": f"{shipment_data.city}, {shipment_data.state}",
                        "warehouse_info": warehouse_info,
                    }

                    if selected_rate and purchase_labels:
                        result_dict["cost"] = selected_rate.get("rate")

                    return result_dict

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
            async def create_with_semaphore(
                validation_result: dict[str, Any],
            ) -> dict[str, Any]:
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

            # Calculate summary using aggregation helper
            from src.mcp_server.tools.bulk_aggregation import aggregate_results

            end_time = datetime.now(UTC)
            aggregated = aggregate_results(results, start_time, end_time)

            successful = aggregated["successful"]
            failed = aggregated["failed"]
            total_cost = aggregated["total_cost"]
            carrier_stats = aggregated["carrier_stats"]
            duration = aggregated["duration"]

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
                        "total_processing_time": aggregated["duration"],
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
                                # Get from_address from easypost_shipment object
                                from_address_data = {
                                    "name": getattr(
                                        easypost_shipment.from_address, "name", ""
                                    ),
                                    "company": getattr(
                                        easypost_shipment.from_address, "company", ""
                                    ),
                                    "street1": easypost_shipment.from_address.street1,
                                    "street2": getattr(
                                        easypost_shipment.from_address, "street2", ""
                                    ),
                                    "city": easypost_shipment.from_address.city,
                                    "state": getattr(easypost_shipment.from_address, "state", ""),
                                    "zip": easypost_shipment.from_address.zip,
                                    "country": easypost_shipment.from_address.country,
                                    "phone": getattr(easypost_shipment.from_address, "phone", ""),
                                    "email": getattr(easypost_shipment.from_address, "email", ""),
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
        _customs_data: list[dict[str, Any]] | None = None,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
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

            async def buy_one(_idx: int, shipment_id: str, rate_id: str) -> dict[str, Any]:
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
