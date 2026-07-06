import requests
import datetime

def get_bristol_routes():
    """
    Real Ryanair availability probing.
    Only returns routes that appear bookable right now.
    """

    base_url = "https://www.ryanair.com/api/farfnd/3/oneWayFares"

    # realistic Ryanair Europe destinations from Bristol region
    candidates = [
        "ALC",  # Alicante
        "AGP",  # Malaga
        "PMI",  # Palma
        "FAO",  # Faro
        "DUB",  # Dublin
        "KRK",  # Krakow
        "BCN",  # Barcelona
        "OPO",  # Porto
        "BGY",  # Milan Bergamo
        "ROM",  # Rome (FCO region sometimes varies)
        "TFS",  # Tenerife South
        "LPA"   # Gran Canaria
    ]

    today = datetime.date.today()
    routes = {}

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for dest in candidates:
        try:
            params = {
                "departureAirportIataCode": "BRS",
                "arrivalAirportIataCode": dest,
                "from": today.isoformat(),
                "to": (today + datetime.timedelta(days=180)).isoformat()
            }

            r = requests.get(base_url, params=params, headers=headers, timeout=10)

            if r.status_code != 200:
                continue

            data = r.json()

            fares = data.get("fares", [])

            # ONLY keep real bookable routes
            if fares and len(fares) > 0:
                routes[f"BRS-{dest}"] = {
                    "freq": len(fares)
                }

        except:
            continue

    return routes
