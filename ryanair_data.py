from playwright.sync_api import sync_playwright

def get_bristol_routes():
    """
    Live Ryanair scrape (simple extraction version).
    """

    routes = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://www.ryanair.com/gb/en")

        page.wait_for_timeout(5000)

        content = page.content().lower()

        # Known common Ryanair destinations from Bristol area
        candidates = [
            "alicante",
            "malaga",
            "palma",
            "dublin",
            "krakow",
            "faro",
            "turin",
            "barcelona",
            "rome"
        ]

        for city in candidates:
            if city in content:
                routes[f"BRS-{city.upper()}"] = {"freq": 1}

        browser.close()

    return routes
