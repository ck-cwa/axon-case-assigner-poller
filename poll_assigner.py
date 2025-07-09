import time
import requests
import os
import re
from datetime import datetime

# Config
AXON_API_KEY = os.environ.get("AXON_API_KEY")
AXON_AGENCY_ID = os.environ.get("AXON_AGENCY_ID")
AXON_BASE_URL = "https://api.evidence.com/api/v1"
POLL_INTERVAL = 60  # in seconds

def get_headers():
    return {
        "Authorization": f"Token {AXON_API_KEY}",
        "Content-Type": "application/json"
    }

def get_recent_cases():
    url = f"{AXON_BASE_URL}/agencies/{AXON_AGENCY_ID}/cases"
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"❌ Failed to fetch cases: {e}")
        return []

def extract_internal_number(title):
    match = re.match(r"(\d{2})–(\d{5})", title)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def find_max_iterator(cases, current_year):
    max_iter = 0
    for case in cases:
        title = case["attributes"].get("title", "")
        year, number = extract_internal_number(title)
        if year == current_year and number is not None:
            max_iter = max(max_iter, number)
    return max_iter

def is_number_assigned(title, current_year):
    year, number = extract_internal_number(title)
    return year == current_year and number is not None

def assign_internal_number(case, number):
    case_id = case["id"]
    internal_number = f"{datetime.now().year % 100:02d}–{number:05d}"
    patch_url = f"{AXON_BASE_URL}/agencies/{AXON_AGENCY_ID}/cases/{case_id}"
    patch_payload = {
        "data": {
            "type": "case",
            "id": case_id,
            "attributes": {
                "title": internal_number
            }
        }
    }

    try:
        patch_response = requests.patch(patch_url, json=patch_payload, headers=get_headers())
        patch_response.raise_for_status()
        print(f"✅ Assigned internal number {internal_number} to case {case_id}")
    except Exception as e:
        print(f"❌ Failed to assign number to case {case_id}: {e}")

def main_loop():
    while True:
        print(f"🔁 Polling at {datetime.now().isoformat()}")
        cases = get_recent_cases()
        current_year = datetime.now().year % 100
        max_iter = find_max_iterator(cases, current_year)
        print(f"📈 Current max internal number for year {current_year}: {max_iter:05d}")

        for case in cases:
            title = case["attributes"].get("title", "")
            if not is_number_assigned(title, current_year):
                max_iter += 1
                assign_internal_number(case, max_iter)

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main_loop()