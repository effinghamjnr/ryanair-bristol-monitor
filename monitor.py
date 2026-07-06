import os
import json
import requests
from ryanair_data import get_bristol_routes

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")


def send_discord(message):
    if not WEBHOOK_URL:
        print("Missing webhook")
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

    for route in new:
        if route not in old:
            changes.append(f"🆕 New route: {route}")

    for route in old:
        if route not in new:
            changes.append(f"❌ Removed route: {route}")

    for route in new:
        if route in old:
            if old[route].get("freq") != new[route].get("freq"):
                changes.append(
                    f"📊 {route}: {old[route]['freq']} → {new[route]['freq']}"
                )

    # remove duplicates safely
    return list(dict.fromkeys(changes))


def main():
    print("Checking Ryanair Bristol routes...")

    old = load_snapshot()
    new = get_bristol_routes()

    changes = compare(old, new)

    if changes:
        msg = "🚨 Ryanair Bristol Update\n\n" + "\n".join(changes)
        send_discord(msg)
    else:
        print("No changes detected")

    save_snapshot(new)


if __name__ == "__main__":
    main()
