import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from transform.validate import validate


def make_df(**overrides):
    """Return a minimal clean DataFrame with optional column overrides."""
    base = {
        "observed_at":          pd.to_datetime(["2026-05-03T00:00", "2026-05-03T01:00"], utc=True),
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


# ── valid data passes through unchanged ──────────────────────────────────────

def test_valid_data_unchanged():
    df = make_df()
    result = validate(df)
    assert len(result) == len(df)

def test_returns_dataframe():
    result = validate(make_df())
    assert isinstance(result, pd.DataFrame)


# ── temperature ──────────────────────────────────────────────────────────────

def test_temperature_too_low_dropped():
    df = make_df(temperature_c=[-99.0, 18.2])
    result = validate(df)
    assert len(result) == 1
    assert result["temperature_c"].iloc[0] == 18.2

def test_temperature_too_high_dropped():
    df = make_df(temperature_c=[18.5, 99.0])
    result = validate(df)
    assert len(result) == 1


# ── humidity ─────────────────────────────────────────────────────────────────

def test_humidity_above_100_dropped():
    df = make_df(humidity_pct=[101.0, 86.0])
    result = validate(df)
    assert len(result) == 1

def test_humidity_negative_dropped():
    df = make_df(humidity_pct=[-1.0, 86.0])
    result = validate(df)
    assert len(result) == 1


# ── wind ─────────────────────────────────────────────────────────────────────

def test_wind_speed_negative_dropped():
    df = make_df(wind_speed_kmh=[-5.0, 5.0])
    result = validate(df)
    assert len(result) == 1

def test_wind_direction_above_360_dropped():
    df = make_df(wind_direction_deg=[361.0, 21.0])
    result = validate(df)
    assert len(result) == 1


# ── pressure ─────────────────────────────────────────────────────────────────

def test_pressure_too_low_dropped():
    df = make_df(surface_pressure_hpa=[500.0, 1007.8])
    result = validate(df)
    assert len(result) == 1

def test_pressure_too_high_dropped():
    df = make_df(surface_pressure_hpa=[1008.2, 1200.0])
    result = validate(df)
    assert len(result) == 1


# ── weather code ─────────────────────────────────────────────────────────────

def test_weather_code_above_99_dropped():
    df = make_df(weather_code=[2, 100])
    result = validate(df)
    assert len(result) == 1

def test_weather_code_negative_dropped():
    df = make_df(weather_code=[-1, 2])
    result = validate(df)
    assert len(result) == 1


# ── precipitation (no upper bound) ───────────────────────────────────────────

def test_precipitation_negative_dropped():
    df = make_df(precipitation_mm=[-0.1, 0.1])
    result = validate(df)
    assert len(result) == 1

def test_precipitation_large_value_kept():
    df = make_df(precipitation_mm=[500.0, 0.1])
    result = validate(df)
    assert len(result) == 2


# ── index is reset after dropping ────────────────────────────────────────────

def test_index_reset_after_drop():
    df = make_df(temperature_c=[-99.0, 18.2])
    result = validate(df)
    assert list(result.index) == [0]
