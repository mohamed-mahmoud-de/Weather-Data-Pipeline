# Schema Design — Weather Data Pipeline

## Overview
The database has two main tables: `locations` (one row per city) and `weather_observations` (one row per city per hour).

---

## Table 1: `locations`

Stores static information about each city.

| Column | Data Type | Description |
|---|---|---|
| location_id | SERIAL PRIMARY KEY | Auto-generated unique ID |
| city | VARCHAR(100) | City name (e.g. Cairo) |
| country | VARCHAR(100) | Country name |
| latitude | FLOAT | Geographic latitude |
| longitude | FLOAT | Geographic longitude |
| timezone | VARCHAR(50) | Timezone string (e.g. Africa/Cairo) |
| elevation | FLOAT | Elevation in metres above sea level |

---

## Table 2: `weather_observations`

Stores hourly weather readings. Each row = one city at one hour.

| Column | Data Type | Description |
|---|---|---|
| observation_id | SERIAL PRIMARY KEY | Auto-generated unique ID |
| location_id | INT (FK → locations) | Which city this reading belongs to |
| observed_at | TIMESTAMPTZ | Timestamp of the reading (UTC) |
| temperature_c | FLOAT | Temperature in Celsius |
| humidity_pct | FLOAT | Relative humidity (0–100) |
| wind_speed_kmh | FLOAT | Wind speed in km/h |
| wind_direction_deg | FLOAT | Wind direction in degrees (0–360) |
| precipitation_mm | FLOAT | Precipitation in millimetres |
| surface_pressure_hpa | FLOAT | Atmospheric pressure in hPa |

---

## Constraints

- `UNIQUE(location_id, observed_at)` on `weather_observations` — prevents duplicate entries if the pipeline runs twice
- `observed_at` uses `TIMESTAMPTZ` not `TIMESTAMP` to ensure timezone safety
- `location_id` in `weather_observations` is a foreign key referencing `locations.location_id`