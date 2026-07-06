import requests

def get_bristol_routes():
    """
    Fetch real Ryanair routes from a public dataset
    (Cirium-style open route data mirror via aviation API source)
    """

    url = "https://raw.githubusercontent.com/nelsonic/airports/master/routes.json"

    try:
        data = requests.get(url, timeout=10).json()
    except:
        return {}

    brs_routes = {}

    for route in data:
        # Route format varies, we filter Bristol (BRS)
        if route.get("source") == "BRS" and route.get("airline") == "FR":
            dest = route.get("destination")
            freq = route.get("weekly_flights", 1)

            if dest:
                key = f"BRS-{dest}"
                brs_routes[key] = {
                    "days": [],   # dataset doesn't always include days
                    "freq": freq
                }

    return brs_routes
