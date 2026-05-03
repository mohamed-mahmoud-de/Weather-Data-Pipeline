"""
Milestone 1 — fetch raw weather data from Open-Meteo for a list of cities.
Saves one JSON file per city per run into data/raw/.

"""

import json
import time
from datetime import datetime
from pathlib import Path

import requests

# ---- Config ----
CITIES = [
    {"name": "Cairo",       "lat": 30.0444, "lon": 31.2357, "country": "EG"},
    {"name": "Alexandria",  "lat": 31.2001, "lon": 29.9187, "country": "EG"},
    {"name": "London",      "lat": 51.5074, "lon":  -0.1278, "country": "GB"},
    {"name": "Tokyo",       "lat": 35.6762, "lon": 139.6503, "country": "JP"},
    {"name": "New York",    "lat": 40.7128, "lon": -74.0060, "country": "US"},
    {"name": "Sydney",      "lat": -33.8688,"lon": 151.2093, "country": "AU"},
    {"name": "Reykjavik",   "lat": 64.1466, "lon": -21.9426, "country": "IS"},
    {"name": "Mumbai",      "lat": 19.0760, "lon":  72.8777, "country": "IN"},
    {"name": "Sao Paulo",   "lat": -23.5505,"lon": -46.6333, "country": "BR"},
    {"name": "Cape Town",   "lat": -33.9249,"lon":  18.4241, "country": "ZA"},
]

VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "wind_direction_10m",
    "pressure_msl",
    "weather_code",
]

API_URL = "https://api.open-meteo.com/v1/forecast"
OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_city(city):
    """Fetch weather data for a single city. Returns the parsed JSON dict."""
    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "hourly": ",".join(VARIABLES),
        "timezone": "UTC",
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()  # crash loudly if the API errored
    return response.json()


def save_json(data, city, run_timestamp):
    """Save the raw JSON to disk with a filename that records city + run time."""
    safe_name = city["name"].lower().replace(" ", "_")
    filename = f"{safe_name}_{run_timestamp}.json"
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath


def main():
    run_timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    print(f"Starting fetch run: {run_timestamp}")
    print(f"Fetching {len(CITIES)} cities...\n")

    successes, failures = 0, 0
    for city in CITIES:
        try:
            data = fetch_city(city)
            filepath = save_json(data, city, run_timestamp)
            print(f"  ✓ {city['name']:<12} -> {filepath}")
            successes += 1
        except Exception as e:
            print(f"  ✗ {city['name']:<12} FAILED: {e}")
            failures += 1
        time.sleep(0.5)  # polite delay between requests

    print(f"\nDone. {successes} succeeded, {failures} failed.")


if __name__ == "__main__":
    main()