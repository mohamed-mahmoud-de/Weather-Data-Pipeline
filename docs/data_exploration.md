# Milestone 1 — Data Exploration Summary

## API
- **Source:** Open-Meteo Forecast API (https://api.open-meteo.com/v1/forecast)
- **Authentication:** None required (free tier)
- **Rate limit:** ~10,000 requests/day
- **Data freshness:** Updated hourly by Open-Meteo

## Cities ingested
10 cities across 6 continents — see `src/fetch_data.py` for the list.

## Variables captured
temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m,
wind_direction_10m, pressure_msl, weather_code

## JSON structure
Top-level: latitude, longitude, timezone, elevation, hourly_units, hourly
The `hourly` block is column-oriented — each variable is a parallel array
indexed by `time[]`. Length is 168 (7 days × 24 hours).

## Units
- temperature_2m: °C
- relative_humidity_2m: %
- precipitation: mm
- wind_speed_10m: km/h
- pressure_msl: hPa

## Data quality findings
1. **Coordinate snapping** — the API returns slightly different lat/lon than
   requested (deltas up to ~0.05°). We will store the API-returned coords.
2. **Nulls in precipitation** — expected; nulls indicate no measurement.
3. **Time arrays are consistent** — all cities returned 168 rows.
4. **Timezone handling** — we requested `timezone=UTC` so all timestamps are
   UTC. The schema must store as `TIMESTAMPTZ`.

## Implications for Milestone 2
- Transform must "melt" the column-oriented `hourly` block into rows.
- Schema needs a `locations` table keyed by API-returned (lat, lon).
- Fact table primary key: (location_id, observed_at).
- Use `INSERT ... ON CONFLICT DO UPDATE` to handle pipeline retries.
- All time columns must use TIMESTAMPTZ (not TIMESTAMP) to preserve UTC context.
- All weather columns can be NOT NULL since zero nulls were found across all 10 cities.

### locations table columns
- id (SERIAL PRIMARY KEY)
- city_name (TEXT NOT NULL)
- latitude (FLOAT NOT NULL)
- longitude (FLOAT NOT NULL)
- country (TEXT NOT NULL)
- elevation (FLOAT)
- timezone (TEXT NOT NULL)

### weather_observations table columns
- id (SERIAL PRIMARY KEY)
- location_id (INTEGER REFERENCES locations(id))
- observed_at (TIMESTAMPTZ NOT NULL)
- temperature_c (FLOAT NOT NULL)
- relative_humidity_pct (INTEGER NOT NULL)
- precipitation_mm (FLOAT NOT NULL)
- wind_speed_kmh (FLOAT NOT NULL)
- wind_direction_deg (INTEGER NOT NULL)
- pressure_hpa (FLOAT NOT NULL)
- weather_code (INTEGER NOT NULL)
- UNIQUE(location_id, observed_at)

# Milestone 1 — Data Exploration & Quality Summary

## 1. Data Quality Findings
- **Null Counts**: Confirmed zero missing values across all weather features (Temperature, Humidity, Wind Speed).
- **Value Ranges**: Verified that temperature (-3.1 to 36.5°C) and humidity (15 to 100%) are within expected meteorological ranges for the selected global cities.
- **Coordinate Snapping**: Grouped data by city and confirmed that each city has a 1:1 mapping for latitude and longitude.
- **Time Coverage**: Validated that all 10 cities have a complete record of 168 hours (7 days), covering the period from 2026-05-04 to 2026-05-10.

## 2. Conclusion
The dataset is clean and meets all data quality requirements for the next phase of the pipeline. No immediate quality issues were found that require data cleaning or imputation.
