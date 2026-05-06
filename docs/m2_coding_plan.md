# M2 Coding Plan — Who Codes What and When

**Milestone 2: System Development & Data Transformation**

Read this before writing a single line of code. It tells you exactly what to build, in what order, and what you are waiting for.

---

## Dependency Chain

This is why order matters. Each arrow means "must be done before":

```
sql/01_create_schema.sql ─────────────────────────────────┐
                                                           ↓
normalize.py ──→ clean.py ──→ validate.py ──→ postgres_loader.py ──→ run_etl.py ──→ 02_analytical_queries.sql
```

- **`run_etl.py`** is the last file coded — it wires everything together
- **`postgres_loader.py`** needs the schema SQL done first
- **`clean.py`** needs `normalize.py` done first (needs to know what columns come in)
- **`validate.py`** needs `clean.py` done first
- **`02_analytical_queries.sql`** is last — needs real data loaded to verify the queries actually work

---

## Wave 1 — Start Immediately (No Dependencies)

These two tasks have zero blockers. Both can be worked on **right now, at the same time**.

### Habeba AbdEldayem → `sql/01_create_schema.sql`

Create the two Postgres tables that the entire pipeline writes into.

**What to build:**

```sql
-- Table 1: locations
-- One row per city. Columns:
--   location_id    SERIAL PRIMARY KEY
--   city           VARCHAR(100)
--   country_code   CHAR(2)
--   latitude       FLOAT
--   longitude      FLOAT
--   timezone       VARCHAR(50)
--   elevation_m    FLOAT

-- Table 2: weather_observations
-- One row per city per hour. Columns:
--   observation_id        SERIAL PRIMARY KEY
--   location_id           INT (FK → locations)
--   observed_at           TIMESTAMPTZ
--   temperature_c         FLOAT
--   humidity_pct          FLOAT
--   wind_speed_kmh        FLOAT
--   wind_direction_deg    FLOAT
--   precipitation_mm      FLOAT
--   surface_pressure_hpa  FLOAT
--   weather_code          INT
```

**Key constraints to include:**
- `UNIQUE(location_id, observed_at)` on `weather_observations` — prevents duplicate rows if the pipeline runs twice
- Foreign key from `weather_observations.location_id` → `locations.location_id`
- `TIMESTAMPTZ` not `TIMESTAMP` for `observed_at`

**Reference:** `docs/schema_design.md` has the full column definitions, types, and WMO code reference.

**Output:** `sql/01_create_schema.sql` — complete and tested (run it against your local Docker Postgres to verify)

---

### Alaa Elfaramawy → `src/transform/normalize.py`

Flip the column-oriented Open-Meteo JSON into a row-per-hour DataFrame.

**What to build:**

A function `normalize(data: dict, city_name: str, country_code: str) -> pd.DataFrame` that:

1. Takes the raw JSON dict loaded from one city file
2. Calls `pd.DataFrame(data["hourly"])` to convert parallel arrays into rows
3. Renames all columns to their schema names:

| API field | Schema column |
|-----------|--------------|
| `time` | `observed_at` |
| `temperature_2m` | `temperature_c` |
| `relative_humidity_2m` | `humidity_pct` |
| `precipitation` | `precipitation_mm` |
| `wind_speed_10m` | `wind_speed_kmh` |
| `wind_direction_10m` | `wind_direction_deg` |
| `pressure_msl` | `surface_pressure_hpa` |
| `weather_code` | `weather_code` |

4. Adds location metadata columns from the JSON root:
   - `api_latitude` ← `data["latitude"]`
   - `api_longitude` ← `data["longitude"]`
   - `elevation_m` ← `data["elevation"]`
   - `city` ← passed in as argument
   - `country_code` ← passed in as argument

5. Returns the DataFrame (no filtering or validation — that's clean.py's job)

**Reference:** `notebooks/01_explore_structure.ipynb` §4 and §5 show exactly how this conversion works with real data.

**Output:** `src/transform/normalize.py` + `test/test_normalize.py`

---

## Wave 2 — Starts After Wave 1

Do not start these until the Wave 1 file you depend on is merged into `main`.

### Belquese Sahm → `src/transform/clean.py` then `src/transform/validate.py`

**Waits for:** `normalize.py` merged (needs to know the exact column names coming in)

**`clean.py`** — A function `clean(df: pd.DataFrame) -> pd.DataFrame` that:
- Parses `observed_at` from string to proper datetime with UTC timezone
- Converts all numeric columns to the correct types (`FLOAT`, `INT`)
- Fills or flags null values (log a warning, don't silently drop)
- Returns a clean DataFrame ready for validation

**`validate.py`** — A function `validate(df: pd.DataFrame) -> pd.DataFrame` that:
- Checks every numeric column against its acceptable range:

| Column | Min | Max |
|--------|-----|-----|
| `temperature_c` | -50 | 60 |
| `humidity_pct` | 0 | 100 |
| `precipitation_mm` | 0 | — |
| `wind_speed_kmh` | 0 | 200 |
| `wind_direction_deg` | 0 | 360 |
| `surface_pressure_hpa` | 870 | 1084 |
| `weather_code` | 0 | 99 |

- Drops rows that fail validation and logs how many were dropped
- Returns the validated DataFrame

**Output:** `src/transform/clean.py` + `src/transform/validate.py` + `test/test_clean.py` + `test/test_validate.py`

---

### Mohamed Rifaat → `src/load/postgres_loader.py`

**Waits for:** `sql/01_create_schema.sql` merged (must know the exact table and column names)

A module with two functions:

**`upsert_location(engine, city, country_code, latitude, longitude, timezone, elevation_m) -> int`**
- Inserts a new row into `locations` if the city doesn't exist yet
- If it does exist, updates it
- Returns the `location_id` for use in the observations insert

**`upsert_observations(engine, df: pd.DataFrame, location_id: int)`**
- Bulk inserts all rows from the DataFrame into `weather_observations`
- Uses `INSERT ... ON CONFLICT (location_id, observed_at) DO UPDATE` so re-running the pipeline never creates duplicates

**Connection:** read credentials from `.env` using `python-dotenv`. Do not hardcode any passwords.

**Output:** `src/load/postgres_loader.py` + `test/test_loader.py`

---

## Wave 3 — Final Assembly (Waits for Everything)

### Mohamed Mahmoud → `src/run_etl.py`

**Waits for:** all 4 modules above merged and tested

The orchestrator that runs the full pipeline end-to-end:

```
1. List all JSON files in data/raw/
2. Create SQLAlchemy engine from .env credentials
3. For each file:
     a. Load JSON
     b. normalize()  → raw DataFrame
     c. clean()      → clean DataFrame
     d. validate()   → validated DataFrame
     e. upsert_location() → get location_id
     f. upsert_observations() → load rows
     g. Log: city name, rows inserted/updated
4. Print summary: total cities, total rows
```

**Output:** `src/run_etl.py` — running `python src/run_etl.py` must complete with no errors

---

### Yahya Galal → `sql/02_analytical_queries.sql`

**Waits for:** `run_etl.py` working and data loaded into Postgres

Write at least 5 SQL queries that verify the loaded data makes sense. Include the expected output as a comment above each query.

Suggested queries:
1. Row count per city
2. Latest `observed_at` per city
3. City with the highest average temperature
4. Hours where `weather_code` ≥ 61 (rain or worse) per city
5. Min/max temperature per city for the full 7-day window

**Output:** `sql/02_analytical_queries.sql` + screenshots of results in `docs/schema_design.md`

---

## Tests — Write Alongside Your Module

Every module must have a test file. Write tests **as you code**, not after.

| Module | Test file | Who |
|--------|-----------|-----|
| `normalize.py` | `test/test_normalize.py` | Alaa |
| `clean.py` | `test/test_clean.py` | Belquese |
| `validate.py` | `test/test_validate.py` | Belquese |
| `postgres_loader.py` | `test/test_loader.py` | Mohamed Rifaat |

Run all tests with:
```bash
pytest test/
```

All tests must pass before opening a PR.

---

## Git Workflow Reminder

- Branch off `main` before starting: `git checkout -b m2-<your-task>`
- Open a PR when done, tag Mohamed for review
- Do **not** push directly to `main`
- Branch naming: `m2-schema`, `m2-normalize`, `m2-clean-validate`, `m2-loader`, `m2-etl`, `m2-queries`

---

## M2 Definition of Done

- [ ] `sql/01_create_schema.sql` runs without errors on a fresh Postgres container
- [ ] `normalize.py`, `clean.py`, `validate.py` all pass their tests
- [ ] `postgres_loader.py` passes its tests
- [ ] `python src/run_etl.py` runs end-to-end with no errors
- [ ] All 3 Postgres tables populated with correct data
- [ ] At least 5 analytical queries written and verified
- [ ] All M2 PRs merged into `main`
