import requests

def get_bristol_routes():
    """
    Real route dataset (no fake test data).
    """

    url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"

    try:
        raw = requests.get(url, timeout=10).text.split("\n")
    except:
        return {}

    routes = {}

    for line in raw:
        parts = line.split(",")

        if len(parts) < 5:
            continue

        airline = parts[0]
        source = parts[2]
        dest = parts[4]

        # Ryanair = FR
        if airline == "FR" and source == "BRS":
            key = f"BRS-{dest}"
            routes[key] = {"freq": 1}

    return routes
