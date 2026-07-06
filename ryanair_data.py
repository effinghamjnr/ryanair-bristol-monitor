import requests
import os

API_KEY = os.environ.get("AVIATIONSTACK_KEY")

def get_bristol_routes():
    """
    Pulls real Ryanair-operated routes from Aviationstack.
    Optimised for low API usage (1 call per day).
    """

    if not API_KEY:
        print("Missing AVIATIONSTACK_KEY")
        return {}

    url = "http://api.aviationstack.com/v1/routes"

    params = {
        "access_key": API_KEY,
        "dep_iata": "BRS"
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        data = response.json()
    except:
        return {}

    routes = {}

    for item in data.get("data", []):
        airline = item.get("airline", {}).get("iata_code")
        dest = item.get("arrival", {}).get("iata_code")

        # Only Ryanair
        if airline == "FR" and dest:
            key = f"BRS-{dest}"
            routes[key] = {
                "freq": 1
            }

    return routes
