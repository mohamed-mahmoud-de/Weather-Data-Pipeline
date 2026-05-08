"""
test/conftest.py
Shared pytest fixtures for all test files.
"""

import pytest
import pandas as pd
from unittest.mock import MagicMock


@pytest.fixture
def locations_df():
    return pd.DataFrame([
        {
            "city": "Cairo",
            "country_code": "EG",
            "latitude": 30.06,
            "longitude": 31.25,
            "timezone": "Africa/Cairo",
            "elevation_m": 23.0,
        },
        {
            "city": "Alexandria",
            "country_code": "EG",
            "latitude": 31.20,
            "longitude": 29.92,
            "timezone": "Africa/Cairo",
            "elevation_m": 32.0,
        },
    ])


@pytest.fixture
def observations_df():
    return pd.DataFrame([
        {
            "location_id": 1,
            "observed_at": "2026-05-08T00:00:00+00:00",
            "temperature_c": 28.5,
            "humidity_pct": 45.0,
            "wind_speed_kmh": 12.0,
            "wind_direction_deg": 270.0,
            "precipitation_mm": 0.0,
            "surface_pressure_hpa": 1013.0,
            "weather_code": 0,
        }
    ])


@pytest.fixture
def mock_engine():
    engine = MagicMock()
    conn = MagicMock()
    engine.begin.return_value.enter = MagicMock(return_value=conn)
    engine.begin.return_value.exit = MagicMock(return_value=False)
    engine.begin.return_value.execute = conn.execute
    return engine, conn