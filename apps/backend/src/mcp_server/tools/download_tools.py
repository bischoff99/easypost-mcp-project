"""
MCP tool for downloading shipment labels and customs documents.

Intelligently detects user intent from natural language input.
"""

import asyncio
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import easypost
import requests  # type: ignore[import-untyped]
from fastmcp import Context

logger = logging.getLogger(__name__)

# Default download directory
DOWNLOAD_DIR = Path(__file__).parent.parent.parent.parent.parent / "data" / "shipping-labels"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def detect_download_intent(request: str) -> dict[str, bool]:
    """
    Detect what user wants to download from natural language input.

    Args:
        request: User's request string (e.g., "download label", "get customs", "both")

    Returns:
        Dictionary with flags: {"label": bool, "customs": bool, "invoice": bool}
    """
    request_lower = request.lower().strip()

    # Keywords for each type
    label_keywords = ["label", "shipping label", "postage", "postage label"]
    customs_keywords = [
        "customs",
        "customs form",
        "customs invoice",
        "commercial invoice",
        "cn22",
        "cn23",
        "customs document",
    ]
    invoice_keywords = ["invoice", "commercial invoice", "commercial"]
    both_keywords = ["both", "all", "everything", "labels and customs", "label and customs"]

    # Check for explicit "both" or "all" first
    if any(keyword in request_lower for keyword in both_keywords):
        return {"label": True, "customs": True, "invoice": True}

    # Check for specific types
    wants_label = any(keyword in request_lower for keyword in label_keywords)
    wants_customs = any(keyword in request_lower for keyword in customs_keywords)
    wants_invoice = any(keyword in request_lower for keyword in invoice_keywords)

    # If nothing specified, default to both label and customs
    if not wants_label and not wants_customs and not wants_invoice:
        return {"label": True, "customs": True, "invoice": True}

    return {
        "label": wants_label or wants_invoice,  # Invoice often includes label
        "customs": wants_customs or wants_invoice,
        "invoice": wants_invoice,
    }


def download_file(url: str, filepath: Path) -> bool:
    """
    Download a file from URL to local path.

    Args:
        url: URL to download from
        filepath: Local path to save file

    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_bytes(response.content)

        logger.info(f"Downloaded {filepath.name} ({len(response.content)} bytes)")
        return True
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return False


def register_download_tools(mcp, easypost_service=None):
    """Register download tools with MCP server."""

    @mcp.tool(tags=["download", "labels", "customs", "shipping"])
    async def download_shipment_documents(
        shipment_ids: list[str] | str,
        request: str = "both",
        download_path: str | None = None,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Download labels and/or customs documents for shipments.

        Intelligently detects what to download from natural language request:
        - "label" or "shipping label" → downloads postage label only
        - "customs" or "customs form" → downloads customs forms only
        - "invoice" or "commercial invoice" → downloads commercial invoice
        - "both" or "all" → downloads both label and customs (default)
        - Empty string → downloads both label and customs

        Args:
            shipment_ids: Single shipment ID or list of shipment IDs
                         (e.g., "shp_xxx" or ["shp_xxx", "shp_yyy"])
            request: What to download (default: "both")
                   Examples: "label", "customs", "invoice", "both", "all",
                            "label and customs"
            download_path: Optional custom download directory (default: data/shipping-labels/)
            ctx: MCP context for progress reporting

        Returns:
            Dictionary with download results for each shipment:
            {
                "status": "success",
                "data": {
                    "shipment_id": {
                        "label": {"downloaded": bool, "path": str, "url": str},
                        "customs": [
                            {
                                "form_type": str,
                                "downloaded": bool,
                                "path": str,
                                "url": str,
                            },
                            ...,
                        ],
                        "invoice": {"downloaded": bool, "path": str, "url": str} | None,
                    },
                    ...
                },
                "summary": {
                    "total": int,
                    "labels_downloaded": int,
                    "customs_downloaded": int,
                    "invoices_downloaded": int
                }
            }
        """
        start_time = datetime.now(UTC)

        try:
            # Get service from closure parameter (stdio mode) or context (HTTP mode)
            service = easypost_service
            if service is None and ctx:
                lifespan_ctx = ctx.request_context.lifespan_context
                service = (
                    lifespan_ctx.get("easypost_service")
                    if isinstance(lifespan_ctx, dict)
                    else lifespan_ctx.easypost_service
                )

            if not service:
                return {
                    "status": "error",
                    "data": None,
                    "message": "EasyPost service not initialized",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            # Normalize shipment_ids to list
            if isinstance(shipment_ids, str):
                shipment_ids = [shipment_ids]

            if not shipment_ids:
                return {
                    "status": "error",
                    "data": None,
                    "message": "No shipment IDs provided",
                    "timestamp": datetime.now(UTC).isoformat(),
                }

            # Detect download intent
            download_intent = detect_download_intent(request)
            wants_label = download_intent["label"]
            wants_customs = download_intent["customs"]
            wants_invoice = download_intent["invoice"]

            if ctx:
                intent_desc = []
                if wants_label:
                    intent_desc.append("labels")
                if wants_customs:
                    intent_desc.append("customs forms")
                if wants_invoice:
                    intent_desc.append("invoices")
                await ctx.info(f"📥 Downloading: {', '.join(intent_desc) or 'nothing'}")

            # Set download directory
            if download_path:
                download_dir = Path(download_path).absolute()
            else:
                download_dir = DOWNLOAD_DIR.absolute()

            # Ensure directory exists
            download_dir.mkdir(parents=True, exist_ok=True)

            # Process each shipment
            results: dict[str, Any] = {}
            summary = {
                "total": len(shipment_ids),
                "labels_downloaded": 0,
                "customs_downloaded": 0,
                "invoices_downloaded": 0,
            }

            for shipment_id in shipment_ids:
                shipment_id = shipment_id.strip()
                if not shipment_id:
                    continue

                if ctx:
                    await ctx.info(f"📦 Processing shipment: {shipment_id}")

                # Retrieve shipment
                shipment_result = await service.retrieve_shipment(shipment_id)
                if shipment_result.get("status") != "success":
                    results[shipment_id] = {
                        "error": shipment_result.get("message", "Failed to retrieve shipment"),
                    }
                    continue

                shipment_data = shipment_result.get("data", {})
                tracking_code = shipment_data.get("tracking_number", "")
                label_url = shipment_data.get("label_url")

                # Get actual shipment object to access forms
                # Use thread pool executor to avoid blocking event loop
                loop = asyncio.get_running_loop()
                easypost_api_key = os.environ.get("EASYPOST_API_KEY")

                if not easypost_api_key:
                    results[shipment_id] = {
                        "error": "EASYPOST_API_KEY not found in environment",
                    }
                    continue

                # Type assertion: we've checked it's not None above
                assert easypost_api_key is not None
                api_key_str: str = easypost_api_key

                # Capture API key in closure with default parameter
                def retrieve_shipment_sync(
                    shipment_id: str, api_key: str = api_key_str
                ) -> Any:
                    """Synchronous shipment retrieval."""
                    easypost.api_key = api_key  # type: ignore[attr-defined]
                    client = easypost.EasyPostClient(api_key=api_key)
                    return client.shipment.retrieve(shipment_id)

                try:
                    shipment = await loop.run_in_executor(None, retrieve_shipment_sync, shipment_id)
                except Exception as e:
                    results[shipment_id] = {
                        "error": f"Failed to retrieve shipment object: {str(e)}",
                    }
                    continue

                shipment_result_data: dict[str, Any] = {
                    "label": None,
                    "customs": [],
                    "invoice": None,
                }

                # Download label if requested
                if wants_label and label_url:
                    filename = f"{tracking_code or shipment_id}_label.png"
                    filepath = download_dir / filename

                    if download_file(label_url, filepath):
                        shipment_result_data["label"] = {
                            "downloaded": True,
                            "path": str(filepath),
                            "url": label_url,
                        }
                        summary["labels_downloaded"] += 1
                    else:
                        shipment_result_data["label"] = {
                            "downloaded": False,
                            "url": label_url,
                            "error": "Download failed",
                        }

                # Download customs forms if requested
                if wants_customs or wants_invoice:
                    forms = getattr(shipment, "forms", []) or []

                    # Try to generate commercial invoice if not present
                    if wants_invoice and not any(
                        getattr(f, "form_type", "").lower() == "commercial_invoice" for f in forms
                    ):
                        try:
                            if ctx:
                                await ctx.info(
                                    f"📄 Generating commercial invoice for {shipment_id}..."
                                )

                            # Capture API key in closure with default parameter
                            def generate_form_sync(
                                shipment_id: str,
                                form_type: str,
                                api_key: str = api_key_str,
                            ) -> Any:
                                """Synchronous form generation."""
                                easypost.api_key = api_key  # type: ignore[attr-defined]
                                client = easypost.EasyPostClient(api_key=api_key)
                                return client.shipment.generate_form(
                                    shipment_id, form_type=form_type
                                )

                            form = await loop.run_in_executor(
                                None, generate_form_sync, shipment_id, "commercial_invoice"
                            )
                            forms.append(form)
                        except Exception as e:
                            logger.warning(f"Failed to generate commercial invoice: {e}")

                    for form in forms:
                        form_type = getattr(form, "form_type", "unknown")
                        form_url = getattr(form, "form_url", None)

                        if not form_url:
                            continue

                        # Determine if this is an invoice
                        is_invoice = (
                            "invoice" in form_type.lower()
                            or "commercial" in form_type.lower()
                        )

                        # Download if it matches request
                        if (wants_customs and not is_invoice) or (wants_invoice and is_invoice):
                            # Determine file extension
                            ext = ".pdf" if "pdf" in form_url.lower() else ".pdf"
                            filename = f"{tracking_code or shipment_id}_{form_type}{ext}"
                            filepath = download_dir / filename

                            if download_file(form_url, filepath):
                                form_data = {
                                    "form_type": form_type,
                                    "downloaded": True,
                                    "path": str(filepath),
                                    "url": form_url,
                                }

                                if is_invoice:
                                    shipment_result_data["invoice"] = form_data
                                    summary["invoices_downloaded"] += 1
                                else:
                                    shipment_result_data["customs"].append(form_data)
                                    summary["customs_downloaded"] += 1
                            else:
                                form_data = {
                                    "form_type": form_type,
                                    "downloaded": False,
                                    "url": form_url,
                                    "error": "Download failed",
                                }
                                if is_invoice:
                                    shipment_result_data["invoice"] = form_data
                                else:
                                    shipment_result_data["customs"].append(form_data)

                results[shipment_id] = shipment_result_data

            duration = (datetime.now(UTC) - start_time).total_seconds()

            return {
                "status": "success",
                "data": results,
                "summary": summary,
                "download_directory": str(download_dir),
                "duration_seconds": duration,
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            logger.error(f"Error downloading shipment documents: {e}", exc_info=True)
            return {
                "status": "error",
                "data": None,
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }
