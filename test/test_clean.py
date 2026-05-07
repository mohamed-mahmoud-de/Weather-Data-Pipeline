import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from transform.clean import clean


def make_df(**overrides):
    """Return a minimal valid normalized DataFrame with optional column overrides."""
    base = {
        "observed_at":          ["2026-05-03T00:00", "2026-05-03T01:00"],
        "temperature_c":        [18.5, 18.2],
        "humidity_pct":         [82.0, 86.0],
        "wind_speed_kmh":       [6.6, 5.0],
        "wind_direction_deg":   [22.0, 21.0],
        "precipitation_mm":     [0.0, 0.1],
        "surface_pressure_hpa": [1008.2, 1007.8],
        "weather_code":         [2, 2],
    }
    base.update(overrides)
    return pd.DataFrame(base)


# ── observed_at parsing ──────────────────────────────────────────────────────

def test_observed_at_is_datetime():
    df = clean(make_df())
    assert pd.api.types.is_datetime64_any_dtype(df["observed_at"])

def test_observed_at_is_utc():
    df = clean(make_df())
    assert str(df["observed_at"].dt.tz) == "UTC"


# ── duplicate removal ────────────────────────────────────────────────────────

def test_duplicates_removed():
    raw = make_df(
        observed_at=["2026-05-03T00:00", "2026-05-03T00:00"],
        temperature_c=[18.5, 18.5],
    )
    df = clean(raw)
    assert len(df) == 1


# ── type coercion ────────────────────────────────────────────────────────────

def test_weather_code_is_int():
    df = clean(make_df())
    assert df["weather_code"].dtype == int

def test_float_columns_are_numeric():
    df = clean(make_df())
    for col in ["temperature_c", "humidity_pct", "wind_speed_kmh",
                "wind_direction_deg", "precipitation_mm", "surface_pressure_hpa"]:
        assert pd.api.types.is_numeric_dtype(df[col])


# ── null handling ────────────────────────────────────────────────────────────

def test_nulls_filled_in_float_column():
    raw = make_df(temperature_c=[None, 18.2])
    df = clean(raw)
    assert df["temperature_c"].isnull().sum() == 0

def test_nulls_filled_in_weather_code():
    raw = make_df(weather_code=[None, 2])
    df = clean(raw)
    assert df["weather_code"].isnull().sum() == 0


# ── output shape ─────────────────────────────────────────────────────────────

def test_output_row_count():
    df = clean(make_df())
    assert len(df) == 2

def test_all_columns_preserved():
    df = clean(make_df())
    expected = {"observed_at", "temperature_c", "humidity_pct", "wind_speed_kmh",
                "wind_direction_deg", "precipitation_mm", "surface_pressure_hpa",
                "weather_code"}
    assert expected.issubset(set(df.columns))
