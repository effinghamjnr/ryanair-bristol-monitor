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

    # New routes
    for route in new:
        if route not in old:
            changes.append(f"🆕 New route: {route}")

    # Removed routes
    for route in old:
        if route not in new:
            changes.append(f"❌ Removed route: {route}")

    # Frequency changes
    for route in new:
        if route in old:
            old_freq = old[route].get("freq")
            new_freq = new[route].get("freq")

            if old_freq != new_freq:
                changes.append(
                    f"📊 {route}: {old_freq} → {new_freq} flights/week"
                )

    return changes


def main():
    print("Checking Ryanair Bristol routes...")

    old = load_snapshot()
    new = get_bristol_routes()

    changes = compare(old, new)

    if changes:
        message = "🚨 Ryanair Bristol Update\n\n" + "\n".join(changes)
        send_discord(message)
    else:
        print("No changes detected")

    save_snapshot(new)


if __name__ == "__main__":
    main()
