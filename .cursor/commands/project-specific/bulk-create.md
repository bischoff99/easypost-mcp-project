Create bulk shipments with EasyPost (M3 Max optimized - 16 parallel workers).

**Domain**: EasyPost shipping automation
**MCP Tool**: create_bulk_shipments (Phase 2)
**Performance**: 3-4 shipments/second (100 in 30-40s)

## Usage

```bash
# Create shipments from spreadsheet data
/bulk-create [spreadsheet data]

# With specific origin city
/bulk-create --from="Los Angeles" [data]

# Preview without purchasing labels
/bulk-create --no-labels [data]

# Dry-run to validate data
/bulk-create --dry-run [data]
```

## What It Does

**Parallel Bulk Shipment Creation:**
1. Parses tab-separated spreadsheet data (16 columns)
2. Auto-detects origin state and city
3. Validates all addresses and parcel data
4. Creates shipments in parallel (16 workers)
5. Purchases labels for each shipment
6. Returns tracking numbers and label URLs
7. Exports results as JSON/CSV

**Difference from `/bulk-ship`:**
- `/bulk-ship`: Gets RATES only (comparison shopping)
- `/bulk-create`: Creates ACTUAL shipments with labels

## MCP Integration

**Server**: easypost-shipping
**Tool**: `create_bulk_shipments` (new)

**Execution Chain:**
1. **Parse & Validate** (Desktop Commander):
   - Parse spreadsheet data
   - Validate 16 columns per row
   - Check address formats
   - Validate parcel dimensions/weight

2. **Batch Processing** (16 parallel workers):
   - Split into batches of 16
   - Create shipments concurrently
   - Purchase labels in parallel
   - Handle errors per shipment

3. **Progress Reporting** (Real-time):
   - ctx.info(): "Creating shipment 45/150..."
   - ctx.report_progress(45, 150)
   - Shows estimated time remaining

4. **Result Aggregation**:
   - Collect all tracking numbers
   - Aggregate label URLs
   - Calculate success/failure rates
   - Export to JSON/CSV

## Input Format

**Tab-separated with 16 columns:**
```
Origin_State	Carrier	First_Name	Last_Name	Phone	Email	Street1	Street2	City	State	ZIP	Country	Type	Dimensions	Weight	Contents
California	USPS	John	Doe	555-0100	john@example.com	123 Main St		Los Angeles	CA	90001	US	Package	12 x 9 x 6	1.5 lbs	Beauty products
Nevada	FedEx	Jane	Smith	555-0101	jane@example.com	456 Oak Ave	Apt 2	Las Vegas	NV	89101	US	Package	10 x 8 x 4	2.3 lbs	Wellness items
```

## Output Format

```
📦 Bulk Shipment Creation (M3 Max: 16 parallel workers)

📊 Validation:
- Total rows: 150
- Valid: 148
- Invalid: 2 (line 23: bad ZIP, line 67: parcel too large)
- Origin: Los Angeles, CA (auto-detected)

🚀 Creating shipments...
[████████████████████████-----] 128/148 (86%)
Estimated time: 12s remaining

✅ Creation Complete!

Success: 145/148 (97.9%)
Failed: 3/148 (2.1%)

Performance:
- Total time: 38.7s
- Throughput: 3.8 shipments/second
- Workers: 16
- Labels purchased: 145

Cost Summary:
- Total: $1,247.50
- Average: $8.60 per shipment
- Carrier breakdown:
  - USPS: 98 shipments ($782.40)
  - FedEx: 35 shipments ($327.50)
  - UPS: 12 shipments ($137.60)

Tracking Numbers:
📋 Exported to: bulk_shipments_20251103_143022.json

Failed Shipments:
- Line 23: Invalid ZIP code (90000)
- Line 67: Parcel exceeds 150 lbs limit
- Line 134: Insufficient address details

💾 Results:
- JSON: bulk_shipments_20251103_143022.json
- CSV: bulk_shipments_20251103_143022.csv
- Labels: /downloads/labels/ (145 PDF files)

Next steps:
1. Review failed shipments in CSV
2. Download labels from /downloads/labels/
3. Track all shipments: /track-batch [paste tracking numbers]
```

## Performance (M3 Max)

**Parallel Creation:**
- Workers: 16 simultaneous shipment creations
- Batch size: Processes in chunks of 16
- Memory: 4GB per worker (efficient)
- API calls: Managed with rate limiting

**Expected Times:**
- 10 shipments: 3-4s
- 50 shipments: 15-18s
- 100 shipments: 30-35s
- 150 shipments: 45-50s
- 500 shipments: 2.5-3 minutes

**Cost Tracking:**
- Real-time cost calculation
- Per-carrier breakdown
- Average cost per shipment
- Total spend summary

## Error Handling

**Graceful Per-Shipment:**
- Invalid address: Skip, report line number
- API error: Retry 3 times with backoff
- Rate limit: Queue and continue
- Parcel too large: Skip, report
- Network error: Retry, then mark failed

**Continues processing** even if some shipments fail.

**All errors logged** with line numbers for easy correction.

## Safety Features

- **Dry-run mode**: Validate without creating
- **Preview cost**: Shows total cost before purchasing
- **Confirm prompt**: For large batches (>50)
- **Rollback**: Can cancel mid-processing
- **Export**: Always saves results for audit

## Advanced Options

```bash
# Specific carrier for all
/bulk-create --carrier=USPS [data]

# Don't purchase labels (create only)
/bulk-create --no-labels [data]

# Custom batch size (for testing)
/bulk-create --batch-size=5 [data]

# Export format
/bulk-create --export=csv [data]
/bulk-create --export=json [data]
```

## Integration Points

**Uses existing tools:**
- `parse_spreadsheet_line()` from bulk_tools.py
- `parse_dimensions()`, `parse_weight()` helpers
- `STORE_ADDRESSES` for origin locations
- EasyPost service with 32-worker ThreadPoolExecutor

**New MCP tool:**
- `create_bulk_shipments()` in bulk_creation_tools.py
- Registered in mcp/__init__.py
- Tested in tests/integration/

## Use Cases

**1. Daily Fulfillment:**
- Export orders from e-commerce platform
- Paste into /bulk-create
- Get 100 labels in 30 seconds
- Download and print labels

**2. Bulk Mailing:**
- Prepare shipment list
- Run /bulk-create
- Track progress in real-time
- Get all tracking numbers instantly

**3. Multi-Store Shipping:**
- Different origins (LA, Vegas, SF)
- Process by origin city
- Optimize carrier per location

## Related Commands

```bash
/bulk-ship [data]      # Get rates first (comparison)
/bulk-create [data]    # Then create shipments
/track-batch [numbers] # Track all created shipments
/analytics-deep 7d     # Analyze shipping patterns
```

**The killer feature - bulk shipment creation in seconds!**

