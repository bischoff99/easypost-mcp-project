# Code Changes Summary - November 10, 2025

## Fixed Issues

### 1. New York Warehouse Auto-Detection ✅
**File:** `backend/src/mcp_server/tools/bulk_creation_tools.py`
**Line:** 140-144

**Problem:** When "New York" was specified in column 1, system defaulted to Los Angeles warehouse.

**Fix:** Added "New York": "New York" to state_defaults mapping.

**Before:**
```python
state_defaults = {
    "California": "Los Angeles",
    "Nevada": "Las Vegas",
}
```

**After:**
```python
state_defaults = {
    "California": "Los Angeles",
    "Nevada": "Las Vegas",
    "New York": "New York",
}
```

**Result:** Shipments with "New York" in column 1 now automatically use NYC Distribution Center (246 E 116th St, New York, NY 10029) without requiring `from_city` parameter.

---

### 2. API Key Configuration ✅
**File:** `backend/.env`

**Changed:** Switched from production key (your_production_api_key_here...) to test key (EZTK...) for safe testing.

---

## Testing Status

- ✅ Code syntax validated (no linter errors)
- ✅ MCP server running with updated code (PID 48954)
- ⏳ Waiting for Cursor MCP reconnection to test

---

## Next Steps

1. Wait for Cursor to reconnect to MCP server (or restart Cursor)
2. Test with: `New York	FEDEX	...` (should auto-detect NYC warehouse)
3. Verify shipment creation uses correct origin address

---

## Files Modified

1. `backend/src/mcp_server/tools/bulk_creation_tools.py` - Added NY warehouse mapping
2. `backend/.env` - Switched to test API key
