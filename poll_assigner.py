import os
import time
import requests

# Configurable Constants
BASE_URL = "https://augustacwa.evidence.com"
CLIENT_ID = os.getenv("AXON_CLIENT_ID")
CLIENT_SECRET = os.getenv("AXON_CLIENT_SECRET")
AGENCY_ID = os.getenv("AXON_AGENCY_ID")  # e.g., "760E3682-839A-494B-854A-C0C8ED48DF8A"
POLL_INTERVAL = 60 * 15  # 15 minutes

def get_access_token():
    """Authenticate with Axon API and get a bearer token."""
    url = f"{BASE_URL}/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        token = response.json().get("access_token")
        print("✅ Access token acquired")
        return token
    except requests.exceptions.RequestException as e:
        print("❌ Failed to retrieve access token:", e)
        return None

def get_cases(token):
    """Fetch cases from Axon."""
    url = f"{BASE_URL}/api/v1/agencies/{AGENCY_ID}/cases?pageSize=10"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("📦 Cases retrieved successfully")
        return response.json().get("data", [])
    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch cases:", e)
        return []

def main_loop():
    while True:
        print(f"🔁 Polling at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        token = get_access_token()
        if not token:
            print("⚠️ Skipping polling due to auth error.")
            time.sleep(POLL_INTERVAL)
            continue

        cases = get_cases(token)
        for case in cases:
            print(f"🧾 Case: {case.get('title')} | ID: {case.get('id')}")

        print(f"⏱ Waiting {POLL_INTERVAL // 60} minutes...\n")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main_loop()
