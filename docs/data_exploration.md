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