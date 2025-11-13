# EasyPost Customs Guide Compliance Implementation

**Date:** 2025-11-13
**Commit:** 4fa9f7d
**Reference:** https://docs.easypost.com/guides/customs-guide

## Summary

Implemented full compliance with EasyPost's [official customs guide](https://docs.easypost.com/guides/customs-guide), adding critical validation and carrier-specific limits that were missing from the original implementation.

## Changes

### 1. EEL/PFC Validation (Critical)

**Per EasyPost Guide:**
- Shipments < $2,500: Use `"NOEEI 30.37(a)"` (automatic)
- Shipments ≥ $2,500: Require AES ITN from https://aesdirect.census.gov

**Implementation:**
```python
# Auto-set for low-value shipments
if eel_pfc is None:
    if total_value >= 2500:
        raise ValueError(
            f"Shipment value ${total_value:.2f} ≥ $2,500 requires AES ITN. "
            "Get ITN from https://aesdirect.census.gov and pass as eel_pfc parameter. "
            "Example: 'AES X20120502123456'"
        )
    eel_pfc = "NOEEI 30.37(a)"
```

**Result:** Clear error message with actionable steps for high-value shipments.

### 2. UPS 100-Item Limit

**Per EasyPost Guide:**
> "The maximum number of items that can be included in customs info with UPS is 100."

**Implementation:**
```python
# Enforce UPS 100-item limit
if len(customs_items) > 100:
    logger.warning(
        f"UPS limits customs to 100 items, got {len(customs_items)}. Truncating."
    )
    customs_items = customs_items[:100]
```

**Result:** Prevents API errors for bulk shipments exceeding UPS limits.

### 3. Optional Fields Support

Added support for edge-case fields required by customs regulations:

- `contents_explanation`: Required when `contents_type='other'`
- `restriction_comments`: Required when `restriction_type != 'none'`

Both fields always included (even if empty) for API consistency.

### 4. `.cursorignore` Optimization

Reduced embedding noise from 373 → ~150 files by excluding:

- Test files (`tests/`, `**/*.test.js`)
- CI/CD workflows (`.github/workflows/`)
- Review docs (`docs/reviews/`)
- Migrations (`alembic/versions/`)
- Data directories (`data/`, `shipping-labels/`)

**Result:** Cursor AI context now focuses on actual source code.

## Test Coverage

Created comprehensive test suite (`test_smart_customs_eel_pfc.py`):

**17 tests, 100% pass rate:**

### EEL/PFC Requirements (8 tests)
- ✅ Low-value automatic NOEEI
- ✅ High-value AES ITN requirement
- ✅ Multi-item value aggregation
- ✅ Custom EEL/PFC override
- ✅ Threshold boundary ($2,499 vs $2,500)

### UPS Item Limit (4 tests)
- ✅ Single item (no truncation)
- ✅ Under 100 items (no truncation)
- ✅ Exactly 100 items (allowed)
- ✅ Over 100 items (truncated with warning)

### Optional Fields (3 tests)
- ✅ contents_explanation passed through
- ✅ restriction_comments passed through
- ✅ Fields default to empty string

### Integration (2 tests)
- ✅ T-shirt to UK (EasyPost guide example)
- ✅ High-value electronics validation

## Impact

**Before:**
- ❌ Hardcoded `eel_pfc = "NOEEI 30.37(a)"` for all shipments
- ❌ No validation for $2,500+ shipments (would fail at EasyPost API)
- ❌ No UPS 100-item enforcement (would fail at carrier)
- ❌ Missing optional fields support

**After:**
- ✅ Automatic EEL/PFC determination based on value
- ✅ Clear error messages with ITN instructions
- ✅ UPS limits enforced proactively
- ✅ Full customs guide compliance

## Files Changed

1. **`apps/backend/src/services/smart_customs.py`** (+77 lines)
   - Added EEL/PFC validation logic
   - Added UPS 100-item limit enforcement
   - Added optional fields support
   - Improved error handling (don't catch ValueError for validation)

2. **`apps/backend/tests/unit/test_smart_customs_eel_pfc.py`** (new file, 358 lines)
   - Comprehensive test coverage for new features
   - Mock EasyPost client for isolation
   - Edge case testing (thresholds, limits, overrides)

3. **`.cursorignore`** (+24 lines)
   - Excluded test files and CI/CD from embeddings
   - Reduced context noise for better AI assistance

## Backwards Compatibility

✅ **Fully backwards compatible** - new parameters have defaults:

```python
def extract_customs_smart(
    contents: str,
    weight_oz: float,
    easypost_client,
    default_value: float | None = None,
    customs_signer: str = "Sender",
    _incoterm: str = "DDP",
    eel_pfc: str | None = None,          # ← New (optional)
    contents_explanation: str = "",       # ← New (optional)
    restriction_comments: str = "",       # ← New (optional)
) -> Any | None:
```

Existing callers continue working without changes.

## Usage Example

**Low-value shipment (< $2,500):**
```python
customs = extract_customs_smart(
    contents="(2) Jeans HTS: 6203.42.4011 ($50 each)",
    weight_oz=32.0,
    easypost_client=client,
)
# Result: eel_pfc = "NOEEI 30.37(a)" (automatic)
```

**High-value shipment (≥ $2,500):**
```python
# Without ITN - raises ValueError with instructions
customs = extract_customs_smart(
    contents="(1) Professional Equipment ($5000)",
    weight_oz=80.0,
    easypost_client=client,
)
# ValueError: Shipment value $5000.00 ≥ $2,500 requires AES ITN...

# With ITN - succeeds
customs = extract_customs_smart(
    contents="(1) Professional Equipment ($5000)",
    weight_oz=80.0,
    easypost_client=client,
    eel_pfc="AES X20120502123456",  # From aesdirect.census.gov
)
# Success!
```

## References

- [EasyPost Customs Guide](https://docs.easypost.com/guides/customs-guide)
- [AES Direct (ITN Portal)](https://aesdirect.census.gov)
- [Commit 4fa9f7d](https://github.com/user/repo/commit/4fa9f7d)

## Next Steps

Consider documenting high-value shipment workflow in user-facing docs:

1. How to obtain AES ITN for $2,500+ shipments
2. When to use `contents_explanation` (contents_type='other')
3. When to use `restriction_comments` (quarantine, special handling)

---

**Status:** ✅ Complete - Production-ready
**Coverage:** 17/17 tests passing (100%)
**Compliance:** Full EasyPost customs guide alignment

---

## Update: Defense-in-Depth Validation (2025-11-13)

**Commit:** f2e759b

### Additional Fix Applied

Added EEL/PFC validation to `easypost_service.py` to close a latent validation gap.

### Problem Identified

While `smart_customs.py` correctly validates EEL/PFC requirements, the `create_shipment()` method in `easypost_service.py` had a hardcoded fallback:

```python
# BEFORE (risky)
eel_pfc=customs_info.get("eel_pfc", "NOEEI 30.37(a)")  # Always defaulted
```

**Risk:** Future code calling `create_shipment()` directly with high-value customs (≥$2,500) would bypass validation and use incorrect `"NOEEI 30.37(a)"`.

### Solution Implemented

Added the same validation logic to `easypost_service.py`:

```python
# AFTER (validated)
# Calculate total value
total_value = 0.0
for item in customs_info.get("customs_items", []):
    quantity = item.get("quantity", 1)
    value = item.get("value", 50.0)
    total_value += quantity * value

# Validate EEL/PFC requirement
eel_pfc = customs_info.get("eel_pfc")
if eel_pfc is None:
    if total_value >= 2500:
        raise ValueError(
            f"Shipment value ${total_value:.2f} ≥ $2,500 requires AES ITN. "
            "Get ITN from https://aesdirect.census.gov or use "
            "smart_customs.extract_customs_smart() for automatic validation."
        )
    eel_pfc = "NOEEI 30.37(a)"
```

### Defense-in-Depth Strategy

**Two Validation Layers:**

1. **Primary:** `smart_customs.py` - Used by all MCP tools and bulk operations
2. **Secondary:** `easypost_service.py` - Catches direct API calls that bypass smart_customs

**Result:** No code path can create high-value international shipments without proper EEL/PFC validation.

### Test Results

✅ **17/17 customs tests pass** (test_smart_customs_eel_pfc.py)  
✅ **11/11 service tests pass** (test_easypost_service.py)  
✅ **No breaking changes** to existing functionality  

### Production Impact

- ✅ **Zero risk to current production** - all existing code paths validated
- ✅ **Future-proof** - prevents accidental high-value shipment errors
- ✅ **Better error messages** - guides users to correct solution
- ✅ **EasyPost guide compliant** - both layers enforce same rules

---

**Final Status:** ✅ **Complete & Production-Ready**

Both `smart_customs.py` and `easypost_service.py` now enforce EasyPost customs guide requirements at every entry point.
