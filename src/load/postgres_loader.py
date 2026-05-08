"""
src/load/postgres_loader.py
Handles PostgreSQL connection and upsert logic using SQLAlchemy.
"""

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

def get_engine(db: str = None, user: str = None,
               password: str = None, host: str = "localhost",
               port: int = 5432) -> Engine:
    """
    Create and return a SQLAlchemy engine using env vars or explicit params.
    """
    db       = db       or os.getenv("POSTGRES_DB",       "weather_db")
    user     = user     or os.getenv("POSTGRES_USER",     "weather_user")
    password = password or os.getenv("POSTGRES_PASSWORD", "weather_pass")
    host     = os.getenv("POSTGRES_HOST", host)
    port     = int(os.getenv("POSTGRES_PORT", port))

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(url, pool_pre_ping=True)
    logger.info("Engine created for database '%s' on %s:%s", db, host, port)
    return engine


# ---------------------------------------------------------------------------
# Upsert helpers
# ---------------------------------------------------------------------------

def upsert_locations(engine: Engine, df: pd.DataFrame) -> int:
    """
    Upsert rows into the locations table.
    Conflict key: (city, country_code)
    Returns number of rows processed.
    """
    if df.empty:
        logger.warning("upsert_locations received empty DataFrame – skipping.")
        return 0

    sql = text("""
        INSERT INTO locations
            (city, country_code, latitude, longitude, timezone, elevation_m)
        VALUES
            (:city, :country_code, :latitude, :longitude, :timezone, :elevation_m)
        ON CONFLICT (city, country_code)
        DO UPDATE SET
            latitude    = EXCLUDED.latitude,
            longitude   = EXCLUDED.longitude,
            timezone    = EXCLUDED.timezone,
            elevation_m = EXCLUDED.elevation_m
    """)

    rows = df.to_dict(orient="records")
    with engine.begin() as conn:
        conn.execute(sql, rows)

    logger.info("upsert_locations: processed %d rows.", len(rows))
    return len(rows)


def upsert_observations(engine: Engine, df: pd.DataFrame) -> int:
    """
    Upsert rows into the weather_observations table.
    Conflict key: (location_id, observed_at)  — matches the UNIQUE constraint.
    Returns number of rows processed.
    """
    if df.empty:
        logger.warning("upsert_observations received empty DataFrame – skipping.")
        return 0

    sql = text("""
        INSERT INTO weather_observations
            (location_id, observed_at, temperature_c, humidity_pct,
             wind_speed_kmh, wind_direction_deg, precipitation_mm,
             surface_pressure_hpa, weather_code)
        VALUES
            (:location_id, :observed_at, :temperature_c, :humidity_pct,
             :wind_speed_kmh, :wind_direction_deg, :precipitation_mm,
             :surface_pressure_hpa, :weather_code)
        ON CONFLICT ON CONSTRAINT unique_location_observation
        DO UPDATE SET
            temperature_c        = EXCLUDED.temperature_c,
            humidity_pct         = EXCLUDED.humidity_pct,
            wind_speed_kmh       = EXCLUDED.wind_speed_kmh,
            wind_direction_deg   = EXCLUDED.wind_direction_deg,
            precipitation_mm     = EXCLUDED.precipitation_mm,
            surface_pressure_hpa = EXCLUDED.surface_pressure_hpa,
            weather_code         = EXCLUDED.weather_code
    """)

    rows = df.to_dict(orient="records")
    with engine.begin() as conn:
        conn.execute(sql, rows)

    logger.info("upsert_observations: processed %d rows.", len(rows))
    return len(rows)
# ---------------------------------------------------------------------------
# Convenience: load both tables in one call
# ---------------------------------------------------------------------------

def load(locations_df: pd.DataFrame,
         observations_df: pd.DataFrame,
         engine: Engine = None) -> dict:
    """
    Load locations then observations into PostgreSQL.
    Returns a dict with row counts for both tables.
    """
    if engine is None:
        engine = get_engine()

    loc_count = upsert_locations(engine, locations_df)
    obs_count = upsert_observations(engine, observations_df)

    return {"locations": loc_count, "observations": obs_count}