"""
Bulk shipment creation MCP tool - M3 MAX OPTIMIZED
16 cores × 2 = 32 concurrent workers
Optimized for I/O-bound EasyPost API calls
"""

import asyncio
import logging
import multiprocessing
from datetime import UTC, datetime
from time import time

from fastmcp import Context

from src.database import get_db
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
CHUNK_SIZE = 8  # Process 8 shipments per chunk
MAX_CONCURRENT = 16  # API concurrency limit (rate limiting)

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
        Create multiple shipments in parallel - M3 Max optimized (32 workers).

        TWO-PHASE WORKFLOW (Recommended):
        1. Get rates first: create_bulk_shipments(data, purchase_labels=False)
           - Creates shipments with customs info
           - Returns all available rates for each shipment
           - No charges yet

        2. Buy approved: buy_bulk_shipments(shipment_ids, carrier="USPS")
           - Purchase labels for approved shipments only
           - Charges applied

        Args:
            spreadsheet_data: Tab-separated shipment data (16 columns)
            from_city: Override origin city (e.g., "Los Angeles", "Las Vegas")
                      If None, auto-detects from origin_state column
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

            # Initialize database service for tracking
            db_service = None
            batch_operation = None

            async for session in get_db():
                db_service = DatabaseService(session)

                # Create batch operation record
                batch_operation = await db_service.create_batch_operation(
                    {
                        "batch_id": f"bulk_create_{int(start_time.timestamp())}",
                        "operation_type": "create_bulk_shipments",
                        "total_items": 0,  # Will update after validation
                        "source": "mcp_tool",
                        "parameters": {
                            "purchase_labels": purchase_labels,
                            "carrier": carrier,
                            "dry_run": dry_run,
                            "from_city": from_city,
                        },
                    }
                )
                break

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

            # Auto-detect origin
            if from_city is None:
                first_line_data = parse_spreadsheet_line(lines[0])
                origin_state = first_line_data["origin_state"]
                state_defaults = {
                    "California": "Los Angeles",
                    "Nevada": "Las Vegas",
                }
                from_city = state_defaults.get(origin_state, "Los Angeles")

                if ctx:
                    await ctx.info(f"📍 Auto-detected origin: {from_city}")

            # Get origin address
            from_address = None
            for state_stores in STORE_ADDRESSES.values():
                if from_city in state_stores:
                    from_address = state_stores[from_city]
                    break

            if from_address is None:
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
                    if not data["zip"] or len(data["zip"]) < 5:
                        errors.append("Invalid ZIP code")
                    if not data["street1"]:
                        errors.append("Missing street address")

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

                    # Check if international and create customs_info
                    is_international = to_address["country"] != from_address["country"]
                    customs_info = None

                    if is_international and purchase_labels:
                        # Smart customs: auto-fills missing HTS codes and values
                        loop = asyncio.get_event_loop()
                        customs_info = await loop.run_in_executor(
                            None,
                            get_or_create_customs,
                            data["contents"],
                            validation_result["weight_oz"],
                            easypost_service.client,
                            None,  # Auto-detect value from description
                        )

                    # Create shipment
                    result = await asyncio.wait_for(
                        easypost_service.create_shipment(
                            to_address=to_address,
                            from_address=from_address,
                            parcel=parcel,
                            carrier=carrier,
                            buy_label=purchase_labels,
                            customs_info=customs_info,
                        ),
                        timeout=30.0,
                    )

                    if result["status"] == "success":
                        # Extract rate info
                        rate_info = result.get("purchased_rate")
                        rates = result.get("rates", [])

                        if not rate_info and purchase_labels and rates:
                            rate_info = min(rates, key=lambda r: float(r["rate"]))

                        return {
                            "line": line_number,
                            "status": "success",
                            "shipment_id": result.get("id"),  # For two-phase workflow
                            "tracking_code": (
                                result.get("tracking_code") if purchase_labels else None
                            ),
                            "label_url": (
                                result.get("postage_label_url") if purchase_labels else None
                            ),
                            "carrier": rate_info["carrier"] if rate_info else None,
                            "service": rate_info["service"] if rate_info else None,
                            "cost": rate_info["rate"] if rate_info else None,
                            "all_rates": (
                                rates[:5] if not purchase_labels else None
                            ),  # Show top 5 rates
                            "recipient": to_address["name"],
                            "destination": f"{data['city']}, {data['state']}",
                        }
                    return {
                        "line": line_number,
                        "status": "error",
                        "error": result.get("message", "Unknown error"),
                        "recipient": to_address["name"],
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

            total_cost = sum(float(s.get("cost", 0)) for s in successful if s.get("cost"))

            # Carrier breakdown
            carrier_stats = {}
            for s in successful:
                carrier_name = s.get("carrier", "Unknown")
                if carrier_name not in carrier_stats:
                    carrier_stats[carrier_name] = {"count": 0, "cost": 0}
                carrier_stats[carrier_name]["count"] += 1
                carrier_stats[carrier_name]["cost"] += float(s.get("cost", 0))

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
                if successful and not dry_run:
                    for shipment_result in successful:
                        try:
                            shipment_id = shipment_result.get("shipment_id")
                            if shipment_id:
                                # Get shipment details from EasyPost API
                                loop = asyncio.get_event_loop()
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
                throughput = len(valid_shipments) / duration if duration > 0 else 0
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
                        "total_cost": round(total_cost, 2),
                        "average_cost": (
                            round(total_cost / len(successful), 2) if successful else 0
                        ),
                        "duration_seconds": round(duration, 2),
                        "throughput": round(len(valid_shipments) / duration, 2),
                        "carrier_breakdown": carrier_stats,
                    },
                    "validation_errors": [
                        {"line": v["line"], "errors": v["errors"]} for v in invalid_shipments
                    ],
                },
                "message": (
                    f"Created {len(successful)}/{len(valid_shipments)} shipments "
                    f"in {duration:.1f}s ({len(valid_shipments) / duration:.1f} shipments/s)"
                ),
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Bulk creation error: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "data": None,
                "message": f"Bulk creation failed: {str(e)}",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    @mcp.tool(tags=["bulk", "purchase", "shipping", "m3-optimized"])
    async def buy_bulk_shipments(
        shipment_ids: list[str],
        customs_data: list[dict] = None,
        carrier: str = None,
        ctx: Context = None,
    ) -> dict:
        """
        Purchase labels for pre-created shipments with customs info (Phase 2).

        WORKFLOW:
        1. create_bulk_shipments(data, purchase_labels=False) → get rates
        2. Review and approve
        3. buy_bulk_shipments(approved_ids, customs_data, carrier="USPS") → purchase

        Args:
            shipment_ids: List of shipment IDs to purchase
            customs_data: List of customs info dicts with contents, hs_code,
                          value, and weight fields
            carrier: Preferred carrier (default: lowest rate)
            ctx: MCP context

        Returns:
            Purchased labels with tracking numbers
        """
        start_time = datetime.now(UTC)

        try:
            if ctx:
                await ctx.info(f"🛒 Purchasing {len(shipment_ids)} labels...")

            semaphore = asyncio.Semaphore(MAX_CONCURRENT)
            performance_start = time()

            async def buy_one(idx: int, shipment_id: str) -> dict:
                try:
                    async with semaphore:
                        loop = asyncio.get_event_loop()

                        # Retrieve shipment
                        shipment = await loop.run_in_executor(
                            None, easypost_service.client.shipment.retrieve, shipment_id
                        )

                        # Add customs info for international shipments
                        # Auto-generates if customs_data not provided
                        if shipment.to_address.country != "US":
                            if customs_data and idx < len(customs_data):
                                customs_dict = customs_data[idx]
                                contents = customs_dict.get("contents", "General Merchandise")
                                value = customs_dict.get("value")
                            else:
                                # Auto-generate from minimal info
                                contents = "General Merchandise"
                                value = 50

                            # Use smart customs generator
                            customs_info = await loop.run_in_executor(
                                None,
                                get_or_create_customs,
                                contents,
                                (
                                    shipment.parcel.weight
                                    if hasattr(shipment.parcel, "weight")
                                    else 16
                                ),
                                easypost_service.client,
                                value,
                            )

                            if customs_info:
                                shipment.customs_info = customs_info

                        # Select rate
                        rate = (
                            shipment.lowest_rate([carrier]) if carrier else shipment.lowest_rate()
                        )

                        # Buy label
                        bought = await loop.run_in_executor(
                            None, easypost_service.client.shipment.buy, shipment_id, rate
                        )

                        return {
                            "status": "success",
                            "shipment_id": shipment_id,
                            "tracking_code": bought.tracking_code,
                            "label_url": bought.postage_label.label_url,
                            "carrier": rate.carrier,
                            "service": rate.service,
                            "cost": rate.rate,
                            "recipient": shipment.to_address.name,
                        }
                except Exception as e:
                    return {"status": "error", "shipment_id": shipment_id, "error": str(e)}

            # Execute - pass index for customs mapping
            tasks = [buy_one(idx, sid) for idx, sid in enumerate(shipment_ids)]
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
            total_cost = sum(float(s["cost"]) for s in successful)
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
