import json
import os
from pathlib import Path

import pandas as pd

# Maps city name (lowercase, spaces replaced with underscores) to country code.
# Needed because the JSON file has no country field — we derive it from the filename.
CITY_COUNTRY_MAP = {
    "cairo":      "EG",
    "alexandria": "EG",
    "london":     "GB",
    "tokyo":      "JP",
    "new_york":   "US",
    "sydney":     "AU",
    "reykjavik":  "IS",
    "mumbai":     "IN",
    "sao_paulo":  "BR",
    "cape_town":  "ZA",
}

# Maps city key (same as above) to the display name with correct casing/spacing.
CITY_NAME_MAP = {
    "cairo":      "Cairo",
    "alexandria": "Alexandria",
    "london":     "London",
    "tokyo":      "Tokyo",
    "new_york":   "New York",
    "sydney":     "Sydney",
    "reykjavik":  "Reykjavik",
    "mumbai":     "Mumbai",
    "sao_paulo":  "Sao Paulo",
    "cape_town":  "Cape Town",
}


def _city_key_from_filename(filename: str) -> str:
    """Extract the city key from a raw JSON filename.

    Filenames follow the pattern <city>_<timestamp>.json where city may be
    multiple words joined by underscores (e.g. new_york_20260503T004508Z.json).
    The timestamp segment always starts with an 8-digit date, so we drop
    everything from that segment onward.
    """
    stem = Path(filename).stem          # e.g. "new_york_20260503T004508Z"
    parts = stem.split("_")
    key_parts = []
    for part in parts:
        if part[:8].isdigit():          # first timestamp segment — stop here
            break
        key_parts.append(part)
    return "_".join(key_parts)          # e.g. "new_york"


def normalize_weather_file(file_path: str):
    """Load one raw JSON file and return (location_dict, observations_df).

    location_dict keys match the `locations` table columns:
        city, country_code, latitude, longitude, timezone, elevation_m

    observations_df columns match the `weather_observations` table:
        observed_at, temperature_c, humidity_pct, wind_speed_kmh,
        wind_direction_deg, precipitation_mm, surface_pressure_hpa, weather_code
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    city_key = _city_key_from_filename(file_path)
    city_name = CITY_NAME_MAP.get(city_key, city_key.replace("_", " ").title())
    country_code = CITY_COUNTRY_MAP.get(city_key, "??")

    location_data = {
        "city":         city_name,
        "country_code": country_code,
        "latitude":     data["latitude"],
        "longitude":    data["longitude"],
        "timezone":     data["timezone"],
        "elevation_m":  data.get("elevation", 0.0),
    }

    hourly = data.get("hourly", {})
    df = pd.DataFrame({
        "observed_at":          hourly.get("time", []),
        "temperature_c":        hourly.get("temperature_2m", []),
        "humidity_pct":         hourly.get("relative_humidity_2m", []),
        "wind_speed_kmh":       hourly.get("wind_speed_10m", []),
        "wind_direction_deg":   hourly.get("wind_direction_10m", []),
        "precipitation_mm":     hourly.get("precipitation", []),
        "surface_pressure_hpa": hourly.get("pressure_msl", []),
        "weather_code":         hourly.get("weather_code", []),
    })

    return location_data, df


if __name__ == "__main__":
    raw_dir = Path("data/raw")
    files = sorted(raw_dir.glob("*.json"))

    if not files:
        print("No JSON files found in data/raw/")
    else:
        loc, df = normalize_weather_file(str(files[0]))
        print(f"\nCity     : {loc['city']} ({loc['country_code']})")
        print(f"Timezone : {loc['timezone']}")
        print(f"Rows     : {len(df)}  |  Columns: {list(df.columns)}")
        print("\nFirst 3 rows:")
        print(df.head(3).to_string())
