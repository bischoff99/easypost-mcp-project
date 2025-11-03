#!/usr/bin/env python3
"""Test all 19 shipments with live EasyPost API."""

import asyncio
import os
import sys

# Add backend root to path (we're in tests/integration/)
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_root)


async def test_all_shipments():
    """Test complete batch of 19 shipments."""

    # All 19 shipments
    full_batch = """California	FEDEX- Priority	Barra 	Odeamar	+639612109875	justinenganga@gmail.com	Blk 6 Lot 48 Camella Vera, Bignay		Valenzuela City	Metro Manila	1440	Philippines	TRUE	13 x 12 x 2	1.8 lbs	 1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)
California	FEDEX- Priority	Luis	Abdala	+639614337118	kingkonlouis@gmail.com	95 Feliza St, Parada		Valenzuela City	Metro Manila	1441	Philippines	FALSE	13 x 12 x 2	1.7 lbs	 1.5 lbs Dead Sea Mineral Bath Salts HTS Code: 3307.30.1000 ($27)
California	FEDEX- Priority	Ingebjørg  	Jacobsen	+31654760952	i.jacobsen@gmail.com	Lange Leidsedwarsstraat 27 	3H	Amsterdam 	Noord-Holland 	1017NG	Netherlands 	FALSE	22 x 18 x 4	8.1 lbs	(4) Heavyweight Carpenter-Style Hiking Jeans HTS Code: 6203.42.4011 ($22/each)
California	FEDEX- Priority	Marcin	Krzyzanowski	+48730714690	marcinkrzyzanowski99@wp.pl	Brzozowa 11a/270		Szeligi 	Mazowieckie	05-850	Poland	FALSE	14 x 12 x 6	4.3 lbs	(1) Gel-Infused Cooling Memory Foam Pillow HTS Code: 9404.90.1000 ($38 each)
California	UPS- Express	Bart	Dekker	+31687226229	bartdekker08@gmail.com	Kardinal de Jongplein 11		Tilburg	Noord Brabant	5046DE	Netherlands 	FALSE	12 x 12 x 4 	5.23 lbs	Original prints and engravings HTS Code: 4911.10.00 ($104)
California	FEDEX- Priority	Johannes 	Klaveren	+31688976134	johannesklaveren@gmail.com	Saturnusstraat 121		Emmeloord	Flevoland	8303cc	Netherlands 	FALSE	22 x 18 x 4	7 lbs 	(4) Heavyweight Carpenter-Style Hiking Jeans HTS Code: 6203.42.4011 ($22/each)
California	FEDEX- Priority	Wouter	Louwsma	+31684215487	wouterlouwsma@outlook.com	Prozastraat 168		Almere	Flevoland	1321dm	Netherland	FALSE	22 x 18 x 4	6.3 lbs 	(4) Heavyweight Carpenter-Style Hiking Jeans HTS Code: 6203.42.4011 ($22/each)
California	FEDEX- Priority	Hugo 	Vilares Pinto 	+34722725495	hvilares728@gmail.com	Calle E N4 	Bajo Derecha	Rioturbio 	Asturias 	33614	Spain 	FALSE	13 x 10 x 2	1.2 lbs	 1.5 lbs Organic Light Brown Sugar HTS Code: 1701.91.4800 ($27)
California	USPS- First Class International	Matthew	Whitwood	+447833775839	dhl.resend686@passfwd.com	15 Alfred King Close	Shavington	Crewe	Cheshire	CW2 5UW	United Kingdom	FALSE	12 x 12 x 4	4.6 lbs	Original prints and engravings HTS Code: 4911.10.00 ($104)
California	FEDEX	Paweł	Sikora	+48780068850	pawelsikora7878@gmal.com	Wandy Pawlik 2/2		Nysa	Opolskie	48-303	Poland 	FALSE	12 x 10 x 10	4 lbs	Original prints and engravings HTS Code: 4911.10.00 ($104)
California	UPS- Express	Bart	Dekker	+31687226229	bartdekker08@gmail.com	Kardinal de Jongplein 11		Tilburg	Noord Brabant	5046DE	Netherlands 	FALSE	10 x 10 x 6	7 lbs 	Mega Slot Car Race Track Set Electric Powered Super Loop Speedway with 5 Cars ($124.55)
California	FEDEX	Giorgio	Levi	+393357989478	cgmoon566@gmail.com	Largo XXI Aprile, 2, 00161 Roma RM		Roma	Lazio	00161	Italy	FALSE	12 x 12 x 4	6.8 lbs	Original prints and engravings HTS Code: 4911.10.00 ($104)
California	USPS- First Class International	Sophia	Michael	+447882750182	Sophmichaelss99@hotmail.com	26 Woodville Road		Barnet	London	EN5 5HA	United Kingdom	FALSE	12 x 12 x 4	3.9 lbs 	Original prints and engravings HTS Code: 4911.10.00 ($44)
California	UPS- Ground	Steven 	Barragan	7077998974	bmike290@gmail.com	293 Almond Way		Healdsburg	California	95485	USA		14 x 10 x 5	5 lbs	(3) Cordura® Reinforced Denim Hiking Jeans HTS Code: 6203.42.4011 ($22/each)
California	FEDEX	Tomas	Ruginus	+31610216754	tomasrugunis@gmail.com	Patrijsweg 16		Heusden 	Noord-Brabant 	5725AG	The Netherlands 	FALSE	22 x 18 x 4	7.6 lbs	(3) Cordura® Reinforced Denim Hiking Jeans HTS Code: 6203.42.4011 ($22/each)
Nevada	UPS	Osman	Kocakafa	+491635002688	hermanito040@protonmail.com	Memelerstrasse 16 		Hamburg	Hamburg 	22049	DE	TRUE	13 x 12 x 2	2.2 lbs	 1.5 lbs Organic Light Brown Sugar HTS Code: 1701.91.4800 ($27)
Nevada	FEDEX	Osman	Kocakafa	+491635002688	hermannso@proton.me	Memelerstrasse 16 		Hamburg	Hamburg	22049	DE	TRUE	13 x 11 x 2	1.4 lbs	 1.5 lbs Organic Light Brown Sugar HTS Code: 1701.91.4800 ($27)
Nevada	USPS- Express	Osman	Kocakafa	+491635002688	hermannso@proton.me	Memelerstrasse 16 		Hamburg	Hamburg 	22049	DE	FALSE	22 x 18 x 4	6.2 lbs	(4) Heavyweight Carpenter-Style Hiking Jeans HTS Code: 6203.42.4011 ($22/each)
Nevada	FEDEX	Pablo 	Alonso Iglesias 	+34675986659	soapfactor@yopmail.com	Calle Jose Uria Uria N2	Bajo R	Oviedo 	Asturias 	33011	Spain 	FALSE	22 x 18 x 4	5.7 lbs	(4) Heavyweight Carpenter-Style Hiking Jeans HTS Code: 6203.42.4011 ($22/each)
Nevada	USPS	Pau	Summers	+441339883481	mattmiller4404@gmail.com	9 clark hill place		Aberdeenshire	Scotland	Ab42 2BA	Uk	FALSE	12 x 12 x 4	3.74 lbs	Original Prints and Engravings HTS Code: 4911.10.00 ($104)"""

    print("🚀 TESTING ALL 19 SHIPMENTS WITH LIVE EASYPOST API")
    print("=" * 80)
    print("\nThis will take 2-5 minutes to get rates for all shipments...")
    print("⏳ Please wait...\n")

    from src.mcp import easypost_service
    from src.mcp.tools.bulk_tools import (
        STORE_ADDRESSES,
        parse_dimensions,
        parse_spreadsheet_line,
        parse_weight,
    )

    lines = [l.strip() for l in full_batch.split("\n") if l.strip()]
    print(f"📋 Total shipments: {len(lines)}\n")

    # Group by origin
    ca_lines = [l for l in lines if l.startswith("California")]
    nv_lines = [l for l in lines if l.startswith("Nevada")]

    print("📍 Origin breakdown:")
    print(f"  California (Los Angeles): {len(ca_lines)} shipments")
    print(f"  Nevada (Las Vegas): {len(nv_lines)} shipments\n")

    results = []

    for idx, line in enumerate(lines, 1):
        try:
            data = parse_spreadsheet_line(line)
            weight_oz = parse_weight(data["weight"])
            length, width, height = parse_dimensions(data["dimensions"])

            # Determine origin
            if data["origin_state"] == "California":
                from_addr = STORE_ADDRESSES["California"]["Los Angeles"]
                origin = "Los Angeles, CA"
            else:
                from_addr = STORE_ADDRESSES["Nevada"]["Las Vegas"]
                origin = "Las Vegas, NV"

            to_addr = {
                "name": f"{data['recipient_name']} {data['recipient_last_name']}",
                "street1": data["street1"],
                "street2": data["street2"],
                "city": data["city"],
                "state": data["state"],
                "zip": data["zip"],
                "country": data["country"],
                "phone": data["recipient_phone"],
                "email": data["recipient_email"],
            }

            parcel = {
                "length": length,
                "width": width,
                "height": height,
                "weight": weight_oz,
            }

            print(
                f"#{idx:2d} | {origin:18s} → {data['city']:20s}, {data['country']:15s} | {weight_oz:5.1f} oz | ",
                end="",
                flush=True,
            )

            # Get rates
            rates_result = await easypost_service.get_rates(to_addr, from_addr, parcel)

            if rates_result["status"] == "success":
                rates = rates_result.get("data", [])
                if rates:
                    cheapest = min(rates, key=lambda r: float(r.get("rate", 999)))
                    print(
                        f"✅ {len(rates):2d} rates | Cheapest: ${cheapest['rate']:7s} ({cheapest['carrier']})"
                    )
                    results.append(
                        {
                            "shipment": idx,
                            "recipient": to_addr["name"],
                            "destination": f"{data['city']}, {data['country']}",
                            "rates_count": len(rates),
                            "cheapest_rate": cheapest["rate"],
                            "cheapest_carrier": cheapest["carrier"],
                        }
                    )
                else:
                    print("⚠️  No rates available")
            else:
                print(f"❌ Error: {rates_result.get('message', 'Unknown error')[:40]}")

        except Exception as e:
            print(f"❌ Exception: {str(e)[:50]}")

    print("\n" + "=" * 80)
    print(f"✅ COMPLETED: {len(results)}/{len(lines)} shipments got rates\n")

    if results:
        print("💰 RATE SUMMARY:")
        total_cheapest = sum(float(r["cheapest_rate"]) for r in results)
        print(f"  Total (cheapest options): ${total_cheapest:.2f}")
        print(f"  Average per shipment: ${total_cheapest/len(results):.2f}")

        # Group by carrier
        carrier_counts = {}
        for r in results:
            carrier = r["cheapest_carrier"]
            carrier_counts[carrier] = carrier_counts.get(carrier, 0) + 1

        print("\n📊 Cheapest carrier breakdown:")
        for carrier, count in sorted(carrier_counts.items(), key=lambda x: -x[1]):
            print(f"  {carrier}: {count} shipments")


if __name__ == "__main__":
    asyncio.run(test_all_shipments())
