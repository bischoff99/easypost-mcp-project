# Legacy Tool File - Not Registered

**File**: `backend/src/mcp_server/tools/shipment_tools.py`
**Status**: Legacy code, intentionally not registered
**Date**: 2025-11-08

## Purpose

This file contains the legacy `create_shipment` tool that was replaced by bulk tools.

## Why Not Registered

The `create_bulk_shipments` tool handles both single and multiple shipments:
- Single shipment: 1 line in spreadsheet = 1 shipment
- Multiple shipments: N lines = N shipments

This makes the separate `create_shipment` tool redundant.

## Current Status

- ✅ Tool file exists but is **NOT** registered in `tools/__init__.py`
- ✅ Bulk tools handle all use cases
- ⚠️ File kept for reference but can be removed if desired

## Removal Decision

**Option 1**: Keep file for reference (current approach)
**Option 2**: Remove file entirely (cleaner codebase)

**Recommendation**: Remove if no longer needed for reference.

---

**Last Updated**: 2025-11-08
**Related**: `docs/architecture/MCP_TOOLS_INVENTORY.md`
