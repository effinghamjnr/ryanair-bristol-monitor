# Temporary “real structure” data layer
# (We will replace the sample data with live Ryanair scraping next step)

def get_bristol_routes():
    """
    Returns simulated Ryanair Bristol routes.
    This is structured exactly like real data will be.
    """

    return {
        "BRS-ALC": {"days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "freq": 7},
        "BRS-PMI": {"days": ["Mon", "Wed", "Fri", "Sun"], "freq": 4},
        "BRS-KRK": {"days": ["Tue", "Thu", "Sat"], "freq": 3}
    }
