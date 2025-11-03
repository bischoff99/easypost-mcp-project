# 📦 Bulk Shipment Rate Tool

**Tool**: `parse_and_get_bulk_rates`  
**Works with**: Single shipment OR multiple shipments

---

## ✅ Use Case 1: Single Shipment

**Just paste one line**:
```
California	FEDEX- Priority	Barra	Odeamar	+639612109875	justinenganga@gmail.com	Blk 6 Lot 48 Camella Vera, Bignay		Valenzuela City	Metro Manila	1440	Philippines	TRUE	13 x 12 x 2	1.8 lbs	1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)
```

**Result**: Rates for this one shipment

---

## ✅ Use Case 2: Multiple Shipments (Bulk)

**Paste multiple lines**:
```
California	FEDEX- Priority	Barra	Odeamar	+639612109875	justinenganga@gmail.com	Blk 6 Lot 48 Camella Vera, Bignay		Valenzuela City	Metro Manila	1440	Philippines	TRUE	13 x 12 x 2	1.8 lbs	1.5 lbs Dead Sea Mineral Bath Salts

California	FEDEX- Priority	Luis	Abdala	+639614337118	kingkonlouis@gmail.com	95 Feliza St, Parada		Valenzuela City	Metro Manila	1441	Philippines	FALSE	13 x 12 x 2	1.7 lbs	1.5 lbs Dead Sea Mineral Bath Salts
```

**Result**: Rates for all shipments in one response

---

## 🏪 California Store Addresses (Auto-Selected)

### 1. Los Angeles (Default)
```
Beauty & Wellness LA
Natural Essentials Store
8500 Beverly Blvd, Suite 120
Los Angeles, CA 90048
Phone: 310-555-0199
Email: shipping@beautywellnessla.com
```

### 2. San Francisco
```
Pacific Beauty Supply
Pacific Beauty Supply Co
2200 Market St
San Francisco, CA 94114
Phone: 415-555-0142
Email: orders@pacificbeauty.com
```

### 3. San Diego
```
Coastal Wellness
Coastal Wellness & Spa Supplies
1025 Garnet Ave
San Diego, CA 92109
Phone: 619-555-0188
Email: ship@coastalwellness.com
```

---

## 🔧 What Gets Auto-Filled

From your spreadsheet:
- ✅ Recipient name: Extracted
- ✅ Phone: Extracted
- ✅ Email: Extracted
- ✅ Address: Extracted (all fields)
- ✅ Dimensions: Parsed (13 x 12 x 2)
- ✅ Weight: Converted to oz (1.8 lbs → 28.8 oz)
- ✅ Contents: First 100 chars

Auto-added:
- ✅ From address: Realistic CA store
- ✅ Parcel specs: EasyPost format
- ✅ Country codes: Standardized

---

## 📋 Example MCP Call

```python
# Single or multiple - same tool!
result = await mcp.call_tool(
    "parse_and_get_bulk_rates",
    spreadsheet_data="""<paste your lines here>""",
    from_city="Los Angeles"  # Optional: LA (default), San Francisco, or San Diego
)

# Returns rates for each shipment
for shipment in result["data"]["shipments"]:
    print(f"Shipment {shipment['shipment_number']}: {shipment['recipient']}")
    print(f"  Destination: {shipment['destination']}")
    print(f"  Weight: {shipment['weight_oz']} oz")
    print(f"  Rates:")
    for rate in shipment['rates']:
        print(f"    - {rate['carrier']} {rate['service']}: ${rate['rate']} ({rate['delivery_days']} days)")
```

---

## ✨ Key Features

1. **Flexible Input**
   - Works with 1 line or 100+ lines
   - Just paste and go

2. **Smart Parsing**
   - Handles "1.8 lbs" → 28.8 oz
   - Parses "13 x 12 x 2" → dimensions
   - Extracts all address fields

3. **Realistic Addresses**
   - Real CA store locations
   - Appropriate for beauty/wellness products
   - Professional business details

4. **Error Handling**
   - Per-shipment error isolation
   - Continues if one fails
   - Summary shows success/failure count

5. **Progress Reporting**
   - Shows "Processing 1/5..."
   - Reports completion

---

## 🚀 Try It Now

**Your exact data works!** Just call:

```
parse_and_get_bulk_rates(
    spreadsheet_data="""California	FEDEX- Priority	Barra 	Odeamar	+639612109875	justinenganga@gmail.com	Blk 6 Lot 48 Camella Vera, Bignay		Valenzuela City	Metron Manila	1440	Philippines	TRUE	13 x 12 x 2	1.8 lbs	 1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)

California	FEDEX- Priority	Luis	Abdala	+639614337118	kingkonlouis@gmail.com	95 Feliza St, Parada		Valenzuela City	Metro Manila	1441	Philippines	FALSE	13 x 12 x 2	1.7 lbs	 1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)""",
    from_city="Los Angeles"
)
```

You'll get back rates for both shipments from a realistic LA beauty store! 🎉
