# Changelog - November 10, 2025

## Summary

Major improvements to international shipping, address preprocessing, and warehouse auto-detection.

## Changes

### International Shipping Fixes ✅

1. **Address Preprocessing for FedEx/UPS**
   - Removed state field for non-US addresses (carrier requirement)
   - Combined short street2 values into street1 (FedEx validation)
   - Handles 35-character street1 limit
   - Applied to both FedEx and UPS international shipments

2. **DDP/DDU Implementation**
   - FedEx shipments use DDP (Delivered Duty Paid)
   - UPS shipments use DDU (Delivered Duty Unpaid)
   - Proper `duty_payment` object handling

3. **Carrier-Specific Address Verification**
   - FedEx carrier verification before shipment creation
   - Address preprocessing before verification
   - Proper handling of verified address IDs

### Warehouse Auto-Detection ✅

**New York Warehouse Support**
- Added "New York" to state mapping in `bulk_creation_tools.py`
- Auto-detects NYC warehouse from spreadsheet column 1
- Improved error handling with warning logs

**Files Modified:**
- `backend/src/mcp_server/tools/bulk_creation_tools.py`
- `backend/src/services/easypost_service.py`

### Code Structure Improvements ✅

- Better documentation and comments
- Improved error handling with logging
- Consistent code organization
- Type hints throughout

## Production Shipments

**8 shipments purchased successfully:**
- Total cost: $570.68
- Countries: UK, Spain, France, Germany, Netherlands
- Carriers: FedEx (DDP), UPS (DDU)

## Files Changed

- `backend/src/mcp_server/tools/bulk_creation_tools.py`
- `backend/src/services/easypost_service.py`
- `backend/src/services/smart_customs.py`
- `backend/src/mcp_server/tools/bulk_tools.py`
- `.gitignore` - Added shipping-labels/

## Documentation

- All cleanup summaries moved to `docs/changelog/2025-11-10/`
- Improved function documentation
- Better code comments
