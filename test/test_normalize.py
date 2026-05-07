import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from transform.normalize import normalize_weather_file, _city_key_from_filename


SAMPLE_JSON = {
    "latitude": 30.0625,
    "longitude": 31.25,
    "timezone": "UTC",
    "elevation": 23.0,
    "hourly": {
        "time":                 ["2026-05-03T00:00", "2026-05-03T01:00"],
        "temperature_2m":       [18.5, 18.2],
        "relative_humidity_2m": [82, 86],
        "precipitation":        [0.0, 0.1],
        "wind_speed_10m":       [6.6, 5.0],
        "wind_direction_10m":   [22, 21],
        "pressure_msl":         [1008.2, 1007.8],
        "weather_code":         [2, 2],
    }
}


@pytest.fixture
def sample_file(tmp_path):
    """Write a minimal JSON file that mimics a real Open-Meteo dump."""
    path = tmp_path / "cairo_20260503T004508Z.json"
    path.write_text(json.dumps(SAMPLE_JSON), encoding="utf-8")
    return str(path)


# ── _city_key_from_filename ──────────────────────────────────────────────────

def test_city_key_single_word():
    assert _city_key_from_filename("cairo_20260503T004508Z.json") == "cairo"

def test_city_key_two_words():
    assert _city_key_from_filename("new_york_20260503T004508Z.json") == "new_york"

def test_city_key_three_words():
    assert _city_key_from_filename("cape_town_20260503T004508Z.json") == "cape_town"


# ── normalize_weather_file — location dict ───────────────────────────────────

def test_location_dict_keys(sample_file):
    loc, _ = normalize_weather_file(sample_file)
    assert set(loc.keys()) == {"city", "country_code", "latitude", "longitude",
                               "timezone", "elevation_m"}

def test_location_city_name(sample_file):
    loc, _ = normalize_weather_file(sample_file)
    assert loc["city"] == "Cairo"

def test_location_country_code(sample_file):
    loc, _ = normalize_weather_file(sample_file)
    assert loc["country_code"] == "EG"

def test_location_coordinates(sample_file):
    loc, _ = normalize_weather_file(sample_file)
    assert loc["latitude"] == SAMPLE_JSON["latitude"]
    assert loc["longitude"] == SAMPLE_JSON["longitude"]


# ── normalize_weather_file — DataFrame ──────────────────────────────────────

def test_dataframe_row_count(sample_file):
    _, df = normalize_weather_file(sample_file)
    assert len(df) == 2

def test_dataframe_has_all_columns(sample_file):
    _, df = normalize_weather_file(sample_file)
    expected = {
        "observed_at", "temperature_c", "humidity_pct",
        "wind_speed_kmh", "wind_direction_deg",
        "precipitation_mm", "surface_pressure_hpa", "weather_code",
    }
    assert expected.issubset(set(df.columns))

def test_dataframe_values(sample_file):
    _, df = normalize_weather_file(sample_file)
    assert df["temperature_c"].iloc[0] == 18.5
    assert df["humidity_pct"].iloc[0] == 82
    assert df["precipitation_mm"].iloc[1] == 0.1
    assert df["wind_direction_deg"].iloc[0] == 22
    assert df["surface_pressure_hpa"].iloc[0] == 1008.2
    assert df["weather_code"].iloc[0] == 2

def test_observed_at_values(sample_file):
    _, df = normalize_weather_file(sample_file)
    assert df["observed_at"].iloc[0] == "2026-05-03T00:00"
