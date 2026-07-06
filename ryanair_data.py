import requests
import datetime

def get_bristol_routes():
    """
    Real-ish Ryanair route inference using flight search patterns.
    This checks multiple destination candidates and infers availability.
    """

    base_url = "https://www.ryanair.com/api/farfnd/3/oneWayFares"

    # Known Ryanair destinations from Bristol region (expandable list)
    destinations = [
        "ALC",  # Alicante
        "AGP",  # Malaga
        "PMI",  # Palma
        "DUB",  # Dublin
        "KRK",  # Krakow
        "FAO",  # Faro
        "TSF",  # Venice (Treviso)
        "BGY",  # Milan Bergamo
        "BCN",  # Barcelona
        "OPO"   # Porto
    ]

    today = datetime.date.today()
    routes = {}

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for dest in destinations:
        try:
            params = {
                "departureAirportIataCode": "BRS",
                "arrivalAirportIataCode": dest,
                "from": today.isoformat(),
                "to": (today + datetime.timedelta(days=30)).isoformat()
            }

            r = requests.get(base_url, params=params, headers=headers, timeout=10)

            if r.status_code != 200:
                continue

            data = r.json()

            fares = data.get("fares", [])

            # If Ryanair returns flights → route exists
            if len(fares) > 0:
                routes[f"BRS-{dest}"] = {
                    "freq": len(fares)  # proxy for availability strength
                }

        except:
            continue

    return routes
