import logging

import pandas as pd

logger = logging.getLogger(__name__)

# Acceptable value ranges per column — based on meteorological standards.
# Rows outside these bounds are dropped and logged.
RULES = {
    "temperature_c":        (-50,  60),
    "humidity_pct":         (  0, 100),
    "wind_speed_kmh":       (  0, 200),
    "wind_direction_deg":   (  0, 360),
    "precipitation_mm":     (  0, None),   # no upper bound
    "surface_pressure_hpa": (870, 1084),
    "weather_code":         (  0,  99),
}


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows that fall outside acceptable meteorological ranges.

    Logs how many rows were dropped per column and overall.
    Returns the validated DataFrame.
    """
    df = df.copy()
    total_before = len(df)
    invalid_mask = pd.Series(False, index=df.index)

    for col, (low, high) in RULES.items():
        if col not in df.columns:
            continue

        col_mask = pd.Series(False, index=df.index)
        if low is not None:
            col_mask |= df[col] < low
        if high is not None:
            col_mask |= df[col] > high

        flagged = col_mask.sum()
        if flagged:
            logger.warning("Column '%s': %d row(s) out of range [%s, %s] — dropping",
                           col, flagged, low, high)
        invalid_mask |= col_mask

    df = df[~invalid_mask].reset_index(drop=True)
    total_dropped = total_before - len(df)

    if total_dropped:
        logger.warning("Validation dropped %d of %d rows total", total_dropped, total_before)
    else:
        logger.info("Validation passed — all %d rows are within range", len(df))

    return df


if __name__ == "__main__":
    from pathlib import Path
    from normalize import normalize_weather_file
    from clean import clean

    logging.basicConfig(level=logging.INFO)

    files = sorted(Path("data/raw").glob("*.json"))
    if files:
        _, raw_df = normalize_weather_file(str(files[0]))
        cleaned = clean(raw_df)
        validated = validate(cleaned)
        print(f"Rows before: {len(cleaned)}  |  after: {len(validated)}")
        print(validated.head(3).to_string())
