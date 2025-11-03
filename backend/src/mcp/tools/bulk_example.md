# Bulk Shipment Tool - Usage Example

## Input Format

Paste tab-separated data from your spreadsheet:

```
California	FEDEX- Priority	Barra	Odeamar	+639612109875	justinenganga@gmail.com	Blk 6 Lot 48 Camella Vera, Bignay		Valenzuela City	Metro Manila	1440	Philippines	TRUE	13 x 12 x 2	1.8 lbs	1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)

California	FEDEX- Priority	Luis	Abdala	+639614337118	kingkonlouis@gmail.com	95 Feliza St, Parada		Valenzuela City	Metro Manila	1441	Philippines	FALSE	13 x 12 x 2	1.7 lbs	1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)
```

## Tool Usage

```python
# Use the parse_and_get_bulk_rates tool
result = await parse_and_get_bulk_rates(
    spreadsheet_data="""<paste your data here>""",
    from_city="Los Angeles"  # Options: Los Angeles, San Francisco, San Diego
)
```

## Available From Addresses

### Los Angeles (Default)
- **Store**: Beauty & Wellness LA
- **Address**: 8500 Beverly Blvd, Suite 120, Los Angeles, CA 90048
- **Phone**: 310-555-0199
- **Best for**: Retail beauty/wellness products

### San Francisco
- **Store**: Pacific Beauty Supply Co
- **Address**: 2200 Market St, San Francisco, CA 94114
- **Phone**: 415-555-0142
- **Best for**: Wholesale beauty supplies

### San Diego
- **Store**: Coastal Wellness & Spa Supplies
- **Address**: 1025 Garnet Ave, San Diego, CA 92109
- **Phone**: 619-555-0188
- **Best for**: Spa and wellness products

## What the Tool Does

1. **Parses** your spreadsheet data
2. **Extracts** recipient info, dimensions, weight
3. **Converts** lbs to oz (1.8 lbs → 28.8 oz)
4. **Parses** dimensions (13 x 12 x 2 → length: 13, width: 12, height: 2)
5. **Adds** realistic CA retail store as origin
6. **Gets rates** from EasyPost for each shipment
7. **Returns** formatted results with best options

## Output Format

```json
{
  "status": "success",
  "data": {
    "from_address": {
      "name": "Beauty & Wellness LA",
      "street1": "8500 Beverly Blvd",
      "city": "Los Angeles",
      "state": "CA",
      "zip": "90048"
    },
    "shipments": [
      {
        "shipment_number": 1,
        "recipient": "Barra Odeamar",
        "destination": "Valenzuela City, Metro Manila, Philippines",
        "weight_oz": 28.8,
        "dimensions": "13 x 12 x 2 in",
        "contents": "1.5 lbs Dead Sea Mineral Bath Salts...",
        "rates": [
          {
            "carrier": "USPS",
            "service": "Priority Mail International",
            "rate": "45.50",
            "delivery_days": 6
          },
          {
            "carrier": "FedEx",
            "service": "International Priority",
            "rate": "89.25",
            "delivery_days": 3
          }
        ]
      },
      {
        "shipment_number": 2,
        "recipient": "Luis Abdala",
        ...
      }
    ],
    "summary": {
      "total": 2,
      "successful": 2,
      "failed": 0
    }
  },
  "message": "Processed 2 shipments (2 successful, 0 failed)"
}
```

## Usage in MCP

Simply paste your spreadsheet data into the tool and get instant rate quotes for all shipments!

