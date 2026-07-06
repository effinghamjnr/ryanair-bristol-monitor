import os
import json
import requests
from datetime import datetime

# Get Discord webhook from GitHub Secrets (we'll set this in Step 5)
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

def send_discord(message):
    if not WEBHOOK_URL:
        print("No webhook found")
        return

    data = {
        "content": message
    }

    requests.post(WEBHOOK_URL, json=data)

def load_snapshot():
    try:
        with open("snapshot.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_snapshot(data):
    with open("snapshot.json", "w") as f:
        json.dump(data, f, indent=2)

def fake_check_for_changes():
    """
    This is temporary.
    Later we replace this with real Ryanair data.
    """
    return {
        "change_detected": True,
        "message": "Test: Bristol → Alicante frequency increased"
    }

def main():
    print("Running monitor...")

    previous = load_snapshot()
    result = fake_check_for_changes()

    if result["change_detected"]:
        send_discord("🚨 Ryanair Bristol Update\n\n" + result["message"])

    save_snapshot(result)

    print("Done.")

if __name__ == "__main__":
    main()
