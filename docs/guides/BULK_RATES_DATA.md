# Bulk Rates Data - Ready for Parser

## Formatted Tab-Separated Data:

```
New York		Marie	Lenaerts	+32488003329	marsiekke1@outlook.com	Recollettenstraat 39		Nieuwpoort		8620	Belgium		13x13x7	4.5 lbs	Women's cotton Sweater Quantity: 2 Total Price: $34
New York		Thibo	Van Dyck	+32478933888	oceanIn.5@outlook.com	Parijsstraat 12		Middelkerke		8430	Belgium		13x13x13	6lb 5oz	Custom Soccer Cleats Quantity: 2 Price: $55
```

## Shipment Details:

### Shipment 1: Magic Womens
- **From**: Anderson Foy, 1542 Pitkin Ave, Brooklyn, NY 11212, US
- **To**: Marie Lenaerts, Recollettenstraat 39, Nieuwpoort, 8620, Belgium
- **Email**: marsiekke1@outlook.com
- **Phone**: +32 488 00 33 29
- **Dimensions**: 13x13x7 inches
- **Weight**: 4.5 lbs (72 oz)
- **Contents**: Women's cotton Sweater, Quantity: 2, Price: $34

### Shipment 2: Euromex Soccer
- **From**: Xavier Parker, 246 E 116th St, New York, NY 10029, US
- **Email**: Xavier@euromex.com
- **Phone**: 6466006012
- **To**: Thibo Van Dyck, Parijsstraat 12, Middelkerke, 8430, Belgium
- **Email**: oceanIn.5@outlook.com
- **Phone**: +32 478 93 38 88
- **Dimensions**: 13x13x13 inches
- **Weight**: 6lb 5oz (101 oz)
- **Contents**: Custom Soccer Cleats, Quantity: 2, Price: $55

## To Use:

1. Start backend: `make prod` or `cd backend && ./venv/bin/python -m uvicorn src.server:app --port 8000`
2. Use the MCP tool `parse_and_get_bulk_rates` with the tab-separated data above
3. Or use the API endpoint `/api/v1/shipments/rates` with individual shipment JSON
