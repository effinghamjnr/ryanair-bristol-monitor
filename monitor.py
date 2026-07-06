import os
import json
import requests
from ryanair_data import get_bristol_routes

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")


def send_discord(message):
    if not WEBHOOK_URL:
        print("Missing DISCORD_WEBHOOK")
        return

    requests.post(WEBHOOK_URL, json={"content": message})


def load_snapshot():
    try:
        with open("snapshot.json", "r") as f:
            return json.load(f)
    except:
        return {}


def save_snapshot(data):
    with open("snapshot.json", "w") as f:
        json.dump(data, f, indent=2)


def compare(old, new):
    changes = []

    # new routes
    for route in new:
        if route not in old:
            changes.append(f"🆕 New route: {route}")

    # removed routes
    for route in old:
        if route not in new:
            changes.append(f"❌ Removed route: {route}")

    # frequency changes
    for route in new:
        if route in old:
            if old[route].get("freq") != new[route].get("freq"):
                changes.append(
                    f"📊 {route}: {old[route]['freq']} → {new[route]['freq']}"
                )

    return list(dict.fromkeys(changes))


def main():
    print("Running Ryanair Bristol monitor...")

    old = load_snapshot()
    new = get_bristol_routes()

    if not new:
        print("No data returned from API (skipping run to save quota)")
        return

    changes = compare(old, new)

    if changes:
        message = "🚨 Ryanair Bristol Update\n\n" + "\n".join(changes)
        send_discord(message)
    else:
        print("No changes detected")

    save_snapshot(new)


if __name__ == "__main__":
    main()
