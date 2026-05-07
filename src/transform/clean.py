import logging

import pandas as pd

logger = logging.getLogger(__name__)

FLOAT_COLS = [
    "temperature_c",
    "humidity_pct",
    "wind_speed_kmh",
    "wind_direction_deg",
    "precipitation_mm",
    "surface_pressure_hpa",
]
INT_COLS = ["weather_code"]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean a normalized weather DataFrame.

    Steps:
    1. Parse observed_at as UTC-aware datetime.
    2. Drop exact duplicate rows.
    3. Cast numeric columns to correct types.
    4. Log and fill any nulls (mean for floats, 0 for weather_code).
    """
    df = df.copy()

    # 1. Parse timestamp and localize to UTC
    df["observed_at"] = pd.to_datetime(df["observed_at"], utc=True)

    # 2. Drop duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["observed_at"])
    dropped = before - len(df)
    if dropped:
        logger.warning("Dropped %d duplicate rows", dropped)

    # 3. Cast types
    for col in FLOAT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in INT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4. Handle nulls
    for col in FLOAT_COLS:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count:
                fill_val = df[col].mean()
                logger.warning("Column '%s' has %d nulls — filling with mean (%.2f)",
                               col, null_count, fill_val)
                df[col] = df[col].fillna(fill_val)

    for col in INT_COLS:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count:
                logger.warning("Column '%s' has %d nulls — filling with 0", col, null_count)
                df[col] = df[col].fillna(0)

    df[INT_COLS] = df[INT_COLS].astype(int)

    return df


if __name__ == "__main__":
    from pathlib import Path
    from normalize import normalize_weather_file

    logging.basicConfig(level=logging.INFO)

    files = sorted(Path("data/raw").glob("*.json"))
    if files:
        _, raw_df = normalize_weather_file(str(files[0]))
        cleaned = clean(raw_df)
        print(f"Rows: {len(cleaned)}")
        print(cleaned.dtypes)
        print(cleaned.head(3).to_string())