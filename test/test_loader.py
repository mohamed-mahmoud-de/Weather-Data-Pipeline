"""
test/test_loader.py
Unit tests for src/load/postgres_loader.py
"""

import pytest
import pandas as pd
from unittest.mock import MagicMock, patch

from src.load.postgres_loader import (
    get_engine,
    upsert_locations,
    upsert_observations,
    load,
)


class TestGetEngine:
    @patch("src.load.postgres_loader.create_engine")
    def test_uses_env_vars(self, mock_create_engine, monkeypatch):
        monkeypatch.setenv("POSTGRES_DB",       "weather_db")
        monkeypatch.setenv("POSTGRES_USER",     "weather_user")
        monkeypatch.setenv("POSTGRES_PASSWORD", "weather_pass")
        get_engine()
        url = mock_create_engine.call_args[0][0]
        assert "weather_db"   in url
        assert "weather_user" in url

    @patch("src.load.postgres_loader.create_engine")
    def test_explicit_params_override_env(self, mock_create_engine, monkeypatch):
        monkeypatch.setenv("POSTGRES_DB", "other_db")
        get_engine(db="my_db", user="my_user", password="my_pass")
        url = mock_create_engine.call_args[0][0]
        assert "my_db"   in url
        assert "my_user" in url


class TestUpsertLocations:
    def test_returns_row_count(self, locations_df, mock_engine):
        engine, _ = mock_engine
        result = upsert_locations(engine, locations_df)
        assert result == len(locations_df)

    def test_calls_execute(self, locations_df, mock_engine):
        engine, _ = mock_engine
        upsert_locations(engine, locations_df)
        assert engine.begin.called

    def test_empty_dataframe_returns_zero(self, mock_engine):
        engine, _ = mock_engine
        result = upsert_locations(engine, pd.DataFrame())
        assert result == 0

    def test_empty_dataframe_skips_execute(self, mock_engine):
        engine, _ = mock_engine
        upsert_locations(engine, pd.DataFrame())
        engine.begin.assert_not_called()


class TestUpsertObservations:
    def test_returns_row_count(self, observations_df, mock_engine):
        engine, _ = mock_engine
        result = upsert_observations(engine, observations_df)
        assert result == len(observations_df)

    def test_calls_execute(self, observations_df, mock_engine):
        engine, _ = mock_engine
        upsert_observations(engine, observations_df)
        assert engine.begin.called

    def test_empty_dataframe_returns_zero(self, mock_engine):
        engine, _ = mock_engine
        result = upsert_observations(engine, pd.DataFrame())
        assert result == 0


class TestLoad:
    def test_returns_counts_dict(self, locations_df, observations_df, mock_engine):
        engine, _ = mock_engine
        result = load(locations_df, observations_df, engine=engine)
        assert result["locations"]    == len(locations_df)
        assert result["observations"] == len(observations_df)

    def test_creates_engine_when_none(self, locations_df, observations_df):
        with patch("src.load.postgres_loader.get_engine") as mock_get, \
             patch("src.load.postgres_loader.upsert_locations",    return_value=2), \
             patch("src.load.postgres_loader.upsert_observations", return_value=1):
            mock_get.return_value = MagicMock()
            result = load(locations_df, observations_df)
            mock_get.assert_called_once()
            assert result == {"locations": 2, "observations": 1}