# Shipment Warehouse Selection Bug Fix

**Date:** 2025-11-10  
**Status:** ✅ FIXED  
**Tools Used:** Desktop Commander + Sequential Thinking

## Problem

Shipments from California were incorrectly assigned Las Vegas (Nevada) warehouses instead of Los Angeles warehouses when using `create_bulk_shipments`.

### Root Cause

`bulk_creation_tools.py` (shipment creation/buying) and `bulk_tools.py` (rate quotes) used **different warehouse selection logic**:

#### bulk_tools.py (CORRECT) ✅
```python
# Per-shipment warehouse selection
category = detect_product_category(contents)  # bedding, art, sporting, etc.
origin_state = data['origin_state']  # California, Nevada, New York
warehouse = get_warehouse_address(origin_state, category)
```

**Result:** Each shipment gets correct specialized warehouse:
- California + Art → LA Arts District Warehouse
- Nevada + Bedding → Las Vegas Home Goods
- New York + Sporting → NYC Outdoor Gear Hub

#### bulk_creation_tools.py (BROKEN) ❌

```python
# Lines 137-164 (OLD CODE)
# Used FIRST LINE's origin_state for ALL shipments
first_line_data = parse_spreadsheet_line(lines[0])
origin_state = first_line_data["origin_state"]
from_city = state_defaults.get(origin_state, "Los Angeles")

# Looked up by city name only (no category)
from_address = STORE_ADDRESSES[state][city]
```

**Result:** If first shipment was Nevada, ALL shipments (including California ones) used Nevada warehouses.

## The Fix

### 1. Import Category Detection Functions

```python
from .bulk_tools import (
    detect_product_category,      # NEW
    get_warehouse_address,         # NEW
    parse_dimensions,
    parse_spreadsheet_line,
    parse_weight,
)
```

### 2. Remove Global Warehouse Lookup

**Removed** (lines 137-164):
```python
# OLD: Determined ONE warehouse for ALL shipments
from_city = state_defaults.get(origin_state, "Los Angeles")
from_address = STORE_ADDRESSES[state][city]
```

**Replaced with** (lines 137-140):
```python
# NEW: Note that warehouse selection happens PER-SHIPMENT
# based on origin_state + product category
```

### 3. Per-Shipment Warehouse Selection

**Inside `create_one_shipment` function** (lines 246-266):

```python
# PRIORITY 1: Custom sender address (columns 16-24)
if "sender_address" in data and data["sender_address"].get("name"):
    shipment_from_address = data["sender_address"]
    warehouse_info = f"Custom sender: {shipment_from_address.get('name')}"
else:
    # PRIORITY 2: Auto-select by category + state (PER SHIPMENT)
    category = detect_product_category(data["contents"])
    origin_state = data.get("origin_state", "California")
    
    # Get specialized warehouse for THIS shipment
    shipment_from_address = get_warehouse_address(origin_state, category)
    
    warehouse_name = shipment_from_address.get("company", "Unknown")
    warehouse_city = shipment_from_address.get("city", "Unknown")
    warehouse_info = f"{warehouse_name} ({warehouse_city}, {origin_state})"

# Log warehouse selection
if ctx and line_number % max(1, total_lines // 10) == 0:
    await ctx.info(f"📍 Shipment #{line_number}: {warehouse_info}")
```

## Verification

### buy_bulk_shipments Flow
**No changes needed** ✅

`buy_bulk_shipments` retrieves existing shipments by ID:
```python
shipment = await loop.run_in_executor(
    None, easypost_service.client.shipment.retrieve, shipment_id
)
```

Since `create_bulk_shipments` now sets correct warehouses, `buy_bulk_shipments` automatically inherits the correct sender addresses.

## Impact

### Before Fix ❌
```
Spreadsheet:
  Line 1: Nevada  + Art      → Las Vegas Arts Warehouse ✓
  Line 2: California + Bedding → Las Vegas Home Goods ✗ (WRONG!)
  Line 3: California + Apparel → Las Vegas Fashion ✗ (WRONG!)
```

### After Fix ✅
```
Spreadsheet:
  Line 1: Nevada + Art       → Las Vegas Arts Warehouse ✓
  Line 2: California + Bedding → LA Home Goods Warehouse ✓
  Line 3: California + Apparel → LA Fashion District Warehouse ✓
```

## Testing

### Test Case 1: Mixed States
```python
spreadsheet_data = """
Nevada	UPS	Siham	Focken	...	(4) Original Prints HTS: 4911.10.00
California	FEDEX	Sarah	Rani	...	(2) Cooling Pillow HTS: 9404.90.1000
"""

# Expected:
# Line 1: Nevada Fine Arts (Las Vegas)
# Line 2: Premium Bedding Distribution (Los Angeles)
```

### Test Case 2: Same State, Different Categories
```python
spreadsheet_data = """
California	UPS	...	(1) Baseball Glove HTS: 9506.51.40
California	FEDEX	...	(2) Canvas Print HTS: 4911.10.00
"""

# Expected:
# Line 1: California Outdoor Supply (sporting)
# Line 2: California Fine Arts (art)
```

## Files Changed

- `backend/src/mcp_server/tools/bulk_creation_tools.py`:
  - Lines 23-29: Added imports
  - Lines 137-140: Removed global warehouse lookup
  - Lines 246-266: Added per-shipment warehouse selection

## Related Files

- `backend/src/mcp_server/tools/bulk_tools.py`: Warehouse definitions and category detection (unchanged)
- `backend/src/mcp_server/tools/bulk_rates_example.md`: Rate quotes example (uses correct logic)

## Consistency Achieved

✅ `parse_and_get_bulk_rates` (quotes) and `create_bulk_shipments` (creation) now use **identical warehouse selection logic**:

1. Check for custom sender address (columns 16-24)
2. If not provided, detect product category from contents
3. Get warehouse using `get_warehouse_address(origin_state, category)`
4. Log warehouse selection for transparency

## Future Improvements

Consider adding:
- Warehouse selection summary in response (which warehouses were used)
- Validation warning if mixing states without custom sender addresses
- Unit tests for mixed-state shipment batches


