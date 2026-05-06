# Schema Design — Weather Data Pipeline

## Overview
The database has two main tables: `locations` (one row per city) and `weather_observations` (one row per city per hour).

---

## Table 1: `locations`

Stores static information about each city. One row per city — this is the dimension table.

| Column | Data Type | Description |
|---|---|---|
| location_id | SERIAL PRIMARY KEY | Auto-generated unique ID |
| city | VARCHAR(100) | City name (e.g. Cairo) |
| country_code | CHAR(2) | ISO 3166-1 alpha-2 country code (e.g. EG, GB) — sourced from `fetch_data.py` config |
| latitude | FLOAT | API-returned geographic latitude (snapped to grid — see data_exploration.md §7) |
| longitude | FLOAT | API-returned geographic longitude |
| timezone | VARCHAR(50) | Timezone string (always GMT/UTC in our pipeline) |
| elevation_m | FLOAT | Elevation in metres above sea level at the API grid point |

---

## Table 2: `weather_observations`

Stores hourly weather readings. Each row = one city at one hour. This is the fact table.

| Column | Data Type | Description |
|---|---|---|
| observation_id | SERIAL PRIMARY KEY | Auto-generated unique ID |
| location_id | INT (FK → locations) | Which city this reading belongs to |
| observed_at | TIMESTAMPTZ | Timestamp of the reading (UTC) — parsed from ISO 8601 string |
| temperature_c | FLOAT | Air temperature at 2 m above ground, in Celsius |
| humidity_pct | FLOAT | Relative humidity at 2 m above ground (0–100) |
| wind_speed_kmh | FLOAT | Wind speed at 10 m above ground, in km/h |
| wind_direction_deg | FLOAT | Wind direction at 10 m above ground, degrees (0–360) |
| precipitation_mm | FLOAT | Precipitation in millimetres (0 = no precipitation) |
| surface_pressure_hpa | FLOAT | Mean sea-level atmospheric pressure in hPa |
| weather_code | INT | WMO weather condition code (table 4677) — see §WMO Reference |

---

## Constraints

- `UNIQUE(location_id, observed_at)` on `weather_observations` — prevents duplicate rows if the pipeline runs more than once for the same time window
- `observed_at` uses `TIMESTAMPTZ` (not plain `TIMESTAMP`) to ensure timezone safety across pipeline runs
- `location_id` in `weather_observations` is a foreign key referencing `locations.location_id`
- `weather_code` is validated against WMO table 4677 (valid values: 0–3, 45, 48, 51–55, 61–65, 71–77, 80–82, 85–86, 95, 96, 99)

---

## WMO Weather Code Reference (table 4677)

| Code | Description |
|------|-------------|
| 0 | Clear sky |
| 1 | Mainly clear |
| 2 | Partly cloudy |
| 3 | Overcast |
| 45 | Fog |
| 48 | Depositing rime fog |
| 51 | Light drizzle |
| 53 | Moderate drizzle |
| 55 | Dense drizzle |
| 61 | Slight rain |
| 63 | Moderate rain |
| 65 | Heavy rain |
| 71 | Slight snowfall |
| 73 | Moderate snowfall |
| 75 | Heavy snowfall |
| 77 | Snow grains |
| 80 | Slight rain showers |
| 81 | Moderate rain showers |
| 82 | Violent rain showers |
| 85 | Slight snow showers |
| 86 | Heavy snow showers |
| 95 | Thunderstorm (slight or moderate) |
| 96 | Thunderstorm with slight hail |
| 99 | Thunderstorm with heavy hail |

---

## Column Name Mapping (API → Schema)

| API field | Schema column | Table |
|-----------|--------------|-------|
| `latitude` (API-returned) | `latitude` | locations |
| `longitude` (API-returned) | `longitude` | locations |
| `elevation` | `elevation_m` | locations |
| `timezone` | `timezone` | locations |
| country code from config | `country_code` | locations |
| `time` | `observed_at` | weather_observations |
| `temperature_2m` | `temperature_c` | weather_observations |
| `relative_humidity_2m` | `humidity_pct` | weather_observations |
| `precipitation` | `precipitation_mm` | weather_observations |
| `wind_speed_10m` | `wind_speed_kmh` | weather_observations |
| `wind_direction_10m` | `wind_direction_deg` | weather_observations |
| `pressure_msl` | `surface_pressure_hpa` | weather_observations |
| `weather_code` | `weather_code` | weather_observations |