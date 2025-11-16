"""
Bulk shipment creation MCP tool - Personal use configuration

PERSONAL USE CONFIGURATION:
- Fixed 4 workers for I/O-bound operations (not CPU-based)
- Concurrent API limit: 2 (prevents EasyPost rate limiting)
- Chunk processing: 4 shipments per chunk
- Performance: ~1-2 shipments/second (adequate for personal use)
"""

import asyncio
import logging
import multiprocessing
from datetime import UTC, datetime
from time import time
from typing import Any

from fastmcp import Context, FastMCP

from src.services.easypost_service import EasyPostService
from src.utils.constants import BULK_OPERATION_TIMEOUT

from .bulk_tools import parse_spreadsheet_line

logger = logging.getLogger(__name__)

# Personal use: simplified worker configuration
CPU_COUNT = multiprocessing.cpu_count()  # 16 cores on M3 Max
MAX_WORKERS = 4  # Fixed 4 workers for personal use (matches easypost_service.py)
CHUNK_SIZE = 4  # Process 4 shipments per chunk for personal use
MAX_CONCURRENT = 2  # API concurrency limit - reduced to avoid rate limiting

# Note: Customs caching handled by smart_customs module
# Use get_or_create_customs from src.services.smart_customs for customs info


def register_shipment_creation_tools(
    mcp: FastMCP, easypost_service: EasyPostService | None = None
) -> None:
    """Register shipment creation tools with MCP server."""

    @mcp.tool(
        tags=["shipment", "create", "shipping", "m3-optimized"],
        # Creates shipment resources but doesn't purchase - no destructiveHint annotation
    )
    async def create_shipment(
        spreadsheet_data: str,
        _from_city: str | None = None,
        dry_run: bool = False,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Create shipments and get rates - Phase 1 of two-phase workflow.

        Handles both single shipments (1 line) and bulk operations (multiple lines).
        Uses spreadsheet format: tab-separated columns (paste from spreadsheet).

        TWO-PHASE WORKFLOW (Required):
        1. create_shipment(data) → Creates shipments, returns ALL rates with rate IDs
           - Creates EasyPost shipment objects
           - Returns all available carriers and services
           - No charges applied
           - Each rate includes: id, carrier, service, rate, delivery_days

        2. buy_shipment_label(shipment_ids, rate_ids) → Purchase selected rates
           - Use specific rate IDs from step 1
           - Purchase only approved shipments
           - Charges applied

        This tool NEVER purchases labels - only creates shipments and returns rates.
        Always returns ALL available carriers to allow comparison and selection.

        Args:
            spreadsheet_data: Tab-separated shipment data (1+ lines, 16+ columns)
            from_city: Override origin city (e.g., "Los Angeles", "Las Vegas")
                      If None, auto-detects from origin_state column or uses sender address
            dry_run: If True, validates data without creating shipments
            ctx: MCP context for progress reporting

        Returns:
            Dictionary with:
            - shipments: List of created shipments with all available rates
            - Each shipment includes: shipment_id, recipient, destination, all_rates
            - Each rate includes: id, carrier, service, rate, delivery_days
            - Use rate IDs in buy_shipment_label() to purchase specific services
        """
        from src.utils.config import settings

        start_time = datetime.now(UTC)

        # Environment warning
        if settings.ENVIRONMENT == "production" and not dry_run:
            logger.warning(
                "⚠️  PRODUCTION MODE: Creating real shipments with actual charges!"
            )
        elif dry_run:
            logger.info("✓ Dry run mode: No shipments will be created")

        try:
            if ctx:
                await ctx.info(
                    "🚀 Starting bulk shipment creation (16 parallel workers)..."
                )

            # Auto-detect format: tab-separated spreadsheet or natural text
            # If first line has no tabs, assume natural text format
            from src.mcp_server.tools.bulk_tools import convert_natural_to_spreadsheet

            first_line = spreadsheet_data.split("\n")[0] if spreadsheet_data else ""
            is_natural_format = "\t" not in first_line

            if is_natural_format:
                if ctx:
                    await ctx.info(
                        "📝 Detected natural text format - converting to spreadsheet format..."
                    )

                # Convert natural text to tab-separated format
                converted_line = convert_natural_to_spreadsheet(spreadsheet_data)
                if not converted_line:
                    return {
                        "status": "error",
                        "data": None,
                        "message": (
                            "Failed to parse natural text format. "
                            "Ensure sender and recipient addresses are clearly separated "
                            "by blank lines."
                        ),
                        "timestamp": datetime.now(UTC).isoformat(),
                    }
                lines = [converted_line]
                if ctx:
                    await ctx.info(
                        "✅ Successfully converted natural text to spreadsheet format"
                    )
            else:
                # Parse lines (standard tab-separated format)
                lines = [
                    line.strip()
                    for line in spreadsheet_data.split("\n")
                    if line.strip()
                ]

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
                    [
                        f"Line {v['line']}: {', '.join(v['errors'])}"
                        for v in invalid_shipments
                    ]
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
                            {"line": v["line"], "errors": v["errors"]}
                            for v in invalid_shipments
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

            # Phase 2: Create shipments with limited concurrency (personal use)
            if ctx:
                await ctx.info(
                    f"🚀 Creating {len(valid_shipments)} shipments "
                    f"({MAX_WORKERS} workers, {MAX_CONCURRENT} concurrent)..."
                )

            # Semaphore to limit concurrent API calls (prevents rate limiting)
            semaphore = asyncio.Semaphore(MAX_CONCURRENT)
            performance_start = time()

            async def create_one_shipment(
                validation_result: dict[str, Any],
            ) -> dict[str, Any]:
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
                    from_address, warehouse_info = select_warehouse_address(
                        shipment_data
                    )

                    # Progress reporting
                    if ctx and line_number % max(1, total_lines // 10) == 0:
                        await ctx.info(f"📍 Shipment #{line_number}: {warehouse_info}")

                    # Build addresses and parcel using helpers
                    to_address = build_to_address(shipment_data)
                    parcel = build_parcel(ValidationResultDTO(**validation_result))

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

                    # Build shipment request (no carrier filter - get all rates)
                    shipment_request = build_shipment_request(
                        to_address=to_address,
                        from_address=from_address,
                        parcel=parcel,
                        customs_info=customs_info,
                        carrier=None,  # Get rates from ALL carriers
                        reference=f"bulk_line_{line_number}",
                    )

                    # Validate address before creating
                    if not to_address.street1 or not to_address.street1.strip():
                        error_msg = (
                            f"Invalid address: street1 is empty for {to_address.name}"
                        )
                        logger.error(error_msg)
                        return {
                            "line": line_number,
                            "status": "error",
                            "error": error_msg,
                            "recipient": to_address.name,
                            "destination": f"{shipment_data.city}, {shipment_data.state}",
                        }

                    # Create shipment via helper (Phase 1: get rates only)
                    shipment_result = await asyncio.wait_for(
                        create_shipment_with_rates(
                            shipment_request,
                            easypost_service,
                            ctx,
                        ),
                        timeout=BULK_OPERATION_TIMEOUT,
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

                    # Return ALL rates - no filtering or selection (Phase 1 only)
                    # User will select specific rate IDs in Phase 2 (buy_shipment_label)
                    return {
                        "line": line_number,
                        "status": "success",
                        "shipment_id": shipment_result.shipment_id,
                        "all_rates": shipment_result.rates,  # Return ALL rates unfiltered
                        "recipient": to_address.name,
                        "destination": f"{shipment_data.city}, {shipment_data.state}",
                        "warehouse_info": warehouse_info,
                    }

                except TimeoutError:
                    return {
                        "line": validation_result["line"],
                        "status": "error",
                        "error": f"Timeout ({BULK_OPERATION_TIMEOUT}s exceeded)",
                    }
                except Exception as e:
                    logger.error(
                        f"Error creating shipment line {validation_result['line']}: {e}",
                        exc_info=True,
                    )
                    return {
                        "line": validation_result["line"],
                        "status": "error",
                        "error": str(e),
                    }

            # Chunked processing with semaphore control (personal use)
            async def create_with_semaphore(
                validation_result: dict[str, Any],
            ) -> dict[str, Any]:
                """Wrapper to limit concurrent API calls."""
                async with semaphore:
                    return await create_one_shipment(validation_result)

            # Create all tasks
            tasks = [create_with_semaphore(v) for v in valid_shipments]

            # Execute with progress reporting
            results = []
            completed = 0
            total = len(valid_shipments)
            progress_interval = max(1, total // 20)  # Report every 5%

            # Process in small chunks (4 items per chunk for personal use)
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
                            eta = (
                                (total - completed) / throughput
                                if throughput > 0
                                else 0
                            )
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

            # Note: Database storage removed for personal use (YAGNI principle)
            # All shipment data is retrieved directly from EasyPost API

            if ctx:
                throughput = len(valid_shipments) / duration if duration > 0 else 0.0
                await ctx.info(
                    f"✅ Complete! {len(successful)}/{len(valid_shipments)} successful"
                )
                await ctx.info(f"⏱️ Total time: {duration:.1f}s")
                await ctx.info(f"⚡ Throughput: {throughput:.2f} shipments/second")

            return {
                "status": "success",
                "data": {
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
                            round(len(valid_shipments) / duration, 2)
                            if duration > 0
                            else 0.0
                        ),
                        "carrier_breakdown": carrier_stats,
                    },
                    "validation_errors": [
                        {"line": v["line"], "errors": v["errors"]}
                        for v in invalid_shipments
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

            return {
                "status": "error",
                "data": None,
                "message": f"Bulk creation failed: {error_msg}",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    @mcp.tool(
        tags=["shipment", "purchase", "shipping", "m3-optimized"],
        annotations={
            "destructiveHint": True,  # Purchases labels with actual charges
        },
    )
    async def buy_shipment_label(
        shipment_ids: list[str],
        rate_ids: list[str],
        _customs_data: list[dict[str, Any]] | None = None,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Purchase labels for pre-created shipments using selected rates (Phase 2).

        WORKFLOW:
        1. create_shipment(data, purchase_labels=False) → get rates
        2. Review and select rates for each shipment
        3. buy_shipment_label(shipment_ids, rate_ids) → purchase with selected rates

        Args:
            shipment_ids: List of shipment IDs to purchase (must match rate_ids length)
            rate_ids: List of rate IDs to use for each shipment (must match shipment_ids length)
            customs_data: List of customs info dicts with contents, hs_code,
                          value, and weight fields
            ctx: MCP context

        Returns:
            Purchased labels with tracking numbers
        """
        from src.utils.config import settings

        start_time = datetime.now(UTC)

        # Environment warning - purchasing labels incurs charges!
        if settings.ENVIRONMENT == "production":
            logger.warning(
                "⚠️  PRODUCTION MODE: Purchasing real shipping labels with actual charges!"
            )
        else:
            logger.info(f"✓ {settings.ENVIRONMENT.upper()} mode: Purchasing labels")

        try:
            if ctx:
                await ctx.info(
                    f"🛒 Purchasing {len(shipment_ids)} labels with selected rates..."
                )

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

            async def buy_one(
                _idx: int, shipment_id: str, rate_id: str
            ) -> dict[str, Any]:
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
                        buy_result = await easypost_service.buy_shipment(
                            shipment_id, rate_id
                        )

                        if buy_result.get("status") != "success":
                            error_msg = buy_result.get("message", "Unknown error")
                            error_details = buy_result.get("error_details", {})
                            logger.error(
                                f"Purchase failed for {shipment_id}: {error_msg}"
                            )
                            logger.error(f"Error details: {error_details}")
                            # Include error_details in error message for visibility
                            full_error = error_msg
                            if error_details.get("errors"):
                                full_error = (
                                    f"{error_msg} | Details: {error_details['errors']}"
                                )
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
                        error_details = (
                            f"{error_details} | HTTP Status: {e.http_status}"
                        )
                    if hasattr(e, "json_body"):
                        error_details = f"{error_details} | JSON: {e.json_body}"
                    logger.error(f"Purchase error for {shipment_id}: {error_details}")
                    return {
                        "status": "error",
                        "shipment_id": shipment_id,
                        "error": error_details,
                    }

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
            total_cost = sum(
                float(s["cost"]) for s in successful if s.get("cost") is not None
            )
            duration = (datetime.now(UTC) - start_time).total_seconds()

            if ctx:
                await ctx.info(
                    f"✅ Purchased {len(successful)}/{total} labels - ${total_cost:.2f}"
                )

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
            logger.error(f"Bulk purchase error: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }
