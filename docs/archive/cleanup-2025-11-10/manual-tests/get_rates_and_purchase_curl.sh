#!/bin/bash
# Get rates and purchase shipments via curl

BASE_URL="http://localhost:8000"

echo "============================================================"
echo "Getting Rates and Purchasing Shipments via curl"
echo "============================================================"

# Shipment 1: Marie Lenaerts
echo ""
echo "[1] Creating Shipment 1: Marie Lenaerts"
SHIPMENT1_RESPONSE=$(curl -s -X POST "${BASE_URL}/bulk-shipments" \
  -H "Content-Type: application/json" \
  -d '{
    "shipments": [{
      "to_address": {
        "name": "Marie Lenaerts",
        "street1": "Recollettenstraat 39",
        "city": "Nieuwpoort",
        "state": "",
        "zip": "8620",
        "country": "BE",
        "phone": "+32488003329",
        "email": "marsiekke1@outlook.com"
      },
      "from_address": {
        "name": "Anderson Foy",
        "street1": "1542 Pitkin Ave",
        "city": "Brooklyn",
        "state": "NY",
        "zip": "11212",
        "country": "US"
      },
      "parcel": {
        "length": 13,
        "width": 13,
        "height": 7,
        "weight": 72
      },
      "carrier": "USPS",
      "customs_info": {
        "contents": [{
          "description": "Women'\''s cotton Sweater",
          "quantity": 2,
          "value": 34.0,
          "origin_country": "US"
        }],
        "customs_certify": true,
        "customs_signer": "Anderson Foy",
        "contents_type": "merchandise",
        "restriction_type": "none",
        "restriction_comments": "",
        "eel_pfc": "NOEEI 30.37(a)"
      }
    }]
  }')

echo "$SHIPMENT1_RESPONSE" | python3 -m json.tool

# Extract shipment ID and rates
SHIPMENT1_ID=$(echo "$SHIPMENT1_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('data', {}).get('results', [{}])[0].get('result', {}).get('id', ''))" 2>/dev/null)
SHIPMENT1_RATES=$(echo "$SHIPMENT1_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); rates=data.get('data', {}).get('results', [{}])[0].get('result', {}).get('rates', []); print(json.dumps(rates))" 2>/dev/null)

if [ -z "$SHIPMENT1_ID" ] || [ "$SHIPMENT1_ID" == "None" ]; then
  echo "ERROR: Failed to create shipment 1"
  exit 1
fi

echo ""
echo "✓ Shipment 1 created: $SHIPMENT1_ID"
echo "✓ Found rates"

# Find FedEx Economy DDP rate
FEDEX_RATE1=$(echo "$SHIPMENT1_RATES" | python3 -c "
import sys, json
rates = json.load(sys.stdin)
for r in rates:
    carrier = r.get('carrier', '').upper()
    service = r.get('service', '').upper()
    if 'FEDEX' in carrier and 'ECONOMY' in service:
        print(json.dumps(r))
        break
" 2>/dev/null)

if [ -z "$FEDEX_RATE1" ]; then
  echo "⚠ No FedEx Economy DDP rate found for shipment 1"
  echo "Available rates:"
  echo "$SHIPMENT1_RATES" | python3 -m json.tool | head -20
  exit 1
fi

RATE1_ID=$(echo "$FEDEX_RATE1" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
RATE1_COST=$(echo "$FEDEX_RATE1" | python3 -c "import sys, json; print(json.load(sys.stdin).get('rate', ''))" 2>/dev/null)

echo "✓ Found FedEx Economy DDP rate: \$$RATE1_COST (ID: $RATE1_ID)"

# Purchase shipment 1
echo ""
echo "Purchasing Shipment 1..."
BUY1_RESPONSE=$(curl -s -X POST "${BASE_URL}/shipments/${SHIPMENT1_ID}/buy?rate_id=${RATE1_ID}")
echo "$BUY1_RESPONSE" | python3 -m json.tool

TRACKING1=$(echo "$BUY1_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('data', {}).get('tracking_code', ''))" 2>/dev/null)
if [ -n "$TRACKING1" ] && [ "$TRACKING1" != "None" ]; then
  echo ""
  echo "✓✓✓ PURCHASED Shipment 1 ✓✓✓"
  echo "  Tracking: $TRACKING1"
  echo "  Label URL: $(echo "$BUY1_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('data', {}).get('postage_label_url', ''))" 2>/dev/null)"
else
  echo "✗ Purchase failed for shipment 1"
fi

# Wait to avoid rate limit
echo ""
echo "Waiting 5 seconds before shipment 2..."
sleep 5

# Shipment 2: Thibo Van Dyck
echo ""
echo "[2] Creating Shipment 2: Thibo Van Dyck"
SHIPMENT2_RESPONSE=$(curl -s -X POST "${BASE_URL}/bulk-shipments" \
  -H "Content-Type: application/json" \
  -d '{
    "shipments": [{
      "to_address": {
        "name": "Thibo Van Dyck",
        "street1": "Parijsstraat 12",
        "city": "Middelkerke",
        "state": "",
        "zip": "8430",
        "country": "BE",
        "phone": "+32478933888",
        "email": "oceanIn.5@outlook.com"
      },
      "from_address": {
        "name": "Xavier Parker",
        "street1": "246 E 116th St",
        "city": "New York",
        "state": "NY",
        "zip": "10029",
        "country": "US",
        "phone": "6466006012",
        "email": "Xavier@euromex.com"
      },
      "parcel": {
        "length": 13,
        "width": 13,
        "height": 13,
        "weight": 101
      },
      "carrier": "USPS",
      "customs_info": {
        "contents": [{
          "description": "Custom Soccer Cleats",
          "quantity": 2,
          "value": 55.0,
          "origin_country": "US"
        }],
        "customs_certify": true,
        "customs_signer": "Xavier Parker",
        "contents_type": "merchandise",
        "restriction_type": "none",
        "restriction_comments": "",
        "eel_pfc": "NOEEI 30.37(a)"
      }
    }]
  }')

echo "$SHIPMENT2_RESPONSE" | python3 -m json.tool

SHIPMENT2_ID=$(echo "$SHIPMENT2_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('data', {}).get('results', [{}])[0].get('result', {}).get('id', ''))" 2>/dev/null)
SHIPMENT2_RATES=$(echo "$SHIPMENT2_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); rates=data.get('data', {}).get('results', [{}])[0].get('result', {}).get('rates', []); print(json.dumps(rates))" 2>/dev/null)

if [ -z "$SHIPMENT2_ID" ] || [ "$SHIPMENT2_ID" == "None" ]; then
  echo "ERROR: Failed to create shipment 2"
  exit 1
fi

echo ""
echo "✓ Shipment 2 created: $SHIPMENT2_ID"
echo "✓ Found rates"

FEDEX_RATE2=$(echo "$SHIPMENT2_RATES" | python3 -c "
import sys, json
rates = json.load(sys.stdin)
for r in rates:
    carrier = r.get('carrier', '').upper()
    service = r.get('service', '').upper()
    if 'FEDEX' in carrier and 'ECONOMY' in service:
        print(json.dumps(r))
        break
" 2>/dev/null)

if [ -z "$FEDEX_RATE2" ]; then
  echo "⚠ No FedEx Economy DDP rate found for shipment 2"
  echo "Available rates:"
  echo "$SHIPMENT2_RATES" | python3 -m json.tool | head -20
  exit 1
fi

RATE2_ID=$(echo "$FEDEX_RATE2" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
RATE2_COST=$(echo "$FEDEX_RATE2" | python3 -c "import sys, json; print(json.load(sys.stdin).get('rate', ''))" 2>/dev/null)

echo "✓ Found FedEx Economy DDP rate: \$$RATE2_COST (ID: $RATE2_ID)"

# Purchase shipment 2
echo ""
echo "Purchasing Shipment 2..."
BUY2_RESPONSE=$(curl -s -X POST "${BASE_URL}/shipments/${SHIPMENT2_ID}/buy?rate_id=${RATE2_ID}")
echo "$BUY2_RESPONSE" | python3 -m json.tool

TRACKING2=$(echo "$BUY2_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('data', {}).get('tracking_code', ''))" 2>/dev/null)
if [ -n "$TRACKING2" ] && [ "$TRACKING2" != "None" ]; then
  echo ""
  echo "✓✓✓ PURCHASED Shipment 2 ✓✓✓"
  echo "  Tracking: $TRACKING2"
  echo "  Label URL: $(echo "$BUY2_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('data', {}).get('postage_label_url', ''))" 2>/dev/null)"
else
  echo "✗ Purchase failed for shipment 2"
fi

echo ""
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo "Shipment 1: $SHIPMENT1_ID - Tracking: ${TRACKING1:-N/A}"
echo "Shipment 2: $SHIPMENT2_ID - Tracking: ${TRACKING2:-N/A}"
