# Milestone 1 — Data Exploration Summary

**Project:** Weather Data Pipeline — DEPI Capstone  
**Data source:** Open-Meteo Forecast API  
**Cities:** 10 (Cairo, Alexandria, London, Tokyo, New York, Sydney, Reykjavik, Mumbai, Sao Paulo, Cape Town)  
**Total rows collected:** 1,680 (10 cities × 168 hours)

---

## 1. API Overview

| Property | Value |
|----------|-------|
| Endpoint | `https://api.open-meteo.com/v1/forecast` |
| Authentication | None (free tier) |
| Rate limit | ~10,000 requests/day |
| Data freshness | Updated hourly by Open-Meteo |
| Timezone requested | UTC (all timestamps are UTC) |
| Forecast window | 7 days (168 hourly records per city) |

---

## 2. JSON Structure

Each city response is a single JSON object. Top-level structure:

```
{
  "latitude": 30.0625,           ← API-snapped coordinate
  "longitude": 31.25,
  "generationtime_ms": 0.12,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 23.0,
  "hourly_units": { ... },       ← unit metadata for every variable
  "hourly": { ... }              ← actual time-series data (parallel arrays)
}
```

### `hourly_units` — unit metadata

```json
{
  "time": "iso8601",
  "temperature_2m": "°C",
  "relative_humidity_2m": "%",
  "precipitation": "mm",
  "wind_speed_10m": "km/h",
  "wind_direction_10m": "°",
  "pressure_msl": "hPa",
  "weather_code": "wmo code"
}
```

### `hourly` — column-oriented time-series

The `hourly` block is **column-oriented** (not row-oriented). Each variable is a separate array of 168 values, all index-aligned:

```
hourly["time"][0]            → "2026-05-03T00:00"
hourly["temperature_2m"][0]  → 18.5         ← same hour as time[0]
hourly["precipitation"][0]   → 0.0          ← same hour as time[0]
```

`pd.DataFrame(data["hourly"])` converts this into a row-per-hour table in one call — this is the core of the M2 transform.

---

## 3. Variables Captured

| API field | Unit | M2 schema column | Notes |
|-----------|------|-----------------|-------|
| `time` | ISO 8601 | `observed_at` (TIMESTAMPTZ) | UTC, 1-hour intervals |
| `temperature_2m` | °C | `temperature_c` | 2 m above ground |
| `relative_humidity_2m` | % | `humidity_pct` | 2 m above ground |
| `precipitation` | mm | `precipitation_mm` | 0 = no precipitation |
| `wind_speed_10m` | km/h | `wind_speed_kmh` | 10 m above ground |
| `wind_direction_10m` | ° | `wind_direction_deg` | 0–360 compass bearing |
| `pressure_msl` | hPa | `surface_pressure_hpa` | Mean sea-level |
| `weather_code` | WMO int | `weather_code` (INT) | WMO table 4677 |

---

## 4. Data Quality Findings

### 4.1 Null values

Zero null values across all 8 variables for all 10 cities (1,680 rows checked).  
No imputation required for this 7-day window. Null guards should still be added in M2 for future pipeline runs.

### 4.2 Value ranges

| Variable | Min | Max | Within expected range? |
|----------|-----|-----|------------------------|
| `temperature_2m` | −3.1 °C | 36.5 °C | ✅ (global bounds: −50 to +60) |
| `relative_humidity_2m` | 15 % | 100 % | ✅ (must be 0–100) |
| `precipitation` | 0.0 mm | 7.2 mm | ✅ (cannot be negative) |
| `wind_speed_10m` | 0.0 km/h | 44.0 km/h | ✅ (reasonable for these cities) |
| `wind_direction_10m` | 0 ° | 360 ° | ✅ (valid compass range) |
| `pressure_msl` | 994.9 hPa | 1030.6 hPa | ✅ (global bounds: 870–1084) |
| `weather_code` | 0 | 95 | ✅ (valid WMO 4677 values) |

No invalid records found. M2 range validation (`validate.py`) will enforce these bounds on every future run.

### 4.3 Coordinate snapping

Open-Meteo snaps requested coordinates to its ~0.25° resolution grid. All deltas are < 0.025° — expected behaviour, not a data error.

**Decision:** store the **API-returned** coordinates in the `locations` table, since the data corresponds to the snapped grid point.

| City | Requested lat | API lat | Δ |
|------|--------------|---------|---|
| Cairo | 30.0444 | 30.0625 | 0.0181 |
| Alexandria | 31.2001 | 31.1875 | 0.0126 |
| London | 51.5074 | 51.5115 | 0.0041 |
| (others all < 0.025°) | | | |

### 4.4 Time coverage

All 10 cities have exactly **168 hourly records** covering a full 7-day window. No gaps detected.

```
Every city: 168 rows, continuous from start_date 00:00 to end_date 23:00 UTC ✅
```

### 4.5 Weather code distribution

Codes observed across all cities (WMO table 4677):

| Code | Description | Count |
|------|-------------|-------|
| 0 | Clear sky | most frequent |
| 1–3 | Mainly clear / partly cloudy / overcast | frequent |
| 61, 63 | Slight / moderate rain | present |
| 80, 81 | Rain showers | present |
| 95 | Thunderstorm | present |

Full distribution available in `notebooks/01_explore_structure.ipynb` §8.

---

## 5. Preprocessing Requirements for M2

| Requirement | How to address in M2 |
|-------------|----------------------|
| Melt column-oriented `hourly` into rows | `pd.DataFrame(data["hourly"])` in `normalize.py` |
| Parse ISO 8601 time strings | `pd.to_datetime(df["time"])` + store as `TIMESTAMPTZ` |
| Rename columns to schema names | Column rename map in `normalize.py` |
| Validate value ranges | `validate.py` with bounds from §4.2 above |
| Handle nulls | `clean.py` — drop or flag rows with nulls in key columns |
| Store API-returned coordinates | Pass `data["latitude"]`, `data["longitude"]`, `data["elevation"]` to locations loader |
| Carry country code from config | Pass `city["country"]` from `CITIES` list in `fetch_data.py` |
| Prevent duplicate rows on retry | `INSERT ... ON CONFLICT DO UPDATE` on `UNIQUE(location_id, observed_at)` |

---

## 6. Conclusion

The dataset is **clean and complete** for this 7-day snapshot:

- Zero nulls across all variables
- All values within valid meteorological ranges
- All 10 cities have full 168-hour coverage
- Coordinate snapping is documented and handled
- `weather_code` is a WMO integer — documented and added to the schema

No blocking data quality issues exist. M2 can proceed directly to schema creation and ETL implementation.
