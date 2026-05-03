# 👥 Team Guide — Weather Data Pipeline

> **Read this first.** It tells you what's done, how to set up the project on your machine, your task for the current milestone, and what's coming next.

**Project:** DEPI Capstone — Weather Data Pipeline
**Repo:** https://github.com/mohamed-mahmoud-de/Weather-Data-Pipeline
**Last updated:** May 2026

---

## 👥 The Team

| Name | GitHub | Role |
|---|---|---|
| **Mohamed Mahmoud** | [@mohamed-mahmoud-de](https://github.com/mohamed-mahmoud-de) | Team Lead |
| Alaa Elfaramawy | [@alaaelstar](https://github.com/alaaelstar) | Data Engineer |
| Belquese Sahm | [@belquesekhaled-commits](https://github.com/belquesekhaled-commits) | Data Engineer |
| Habeba AbdEldayem | [@habebaabdeldayem311-hash](https://github.com/habebaabdeldayem311-hash) | Data Engineer |
| Mohamed Rifaat | [@Mohamed-Rifaat](https://github.com/Mohamed-Rifaat) | Data Engineer |
| Yahya Galal | [@Yahya7Galal](https://github.com/Yahya7Galal) | Data Engineer |

---

## 📊 Project Status

| Milestone | Status |
|---|---|
| **M1 — Data Collection & Exploration** | 🟡 In Progress |
| **M2 — System Development & Transformation** | ⚪ Not Started |
| **M3 — Deployment (Batch Processing)** | ⚪ Not Started |
| **M4 — Automation, Monitoring, Reliability** | ⚪ Not Started |
| **M5 — Documentation, Demo, Presentation** | ⚪ Not Started |

🟢 Done · 🟡 In Progress · ⚪ Not Started · 🔴 Blocked

---

## ✅ What's Already Done

Mohamed has set the foundation. **Don't redo any of this:**

- [x] GitHub repo created
- [x] Project folder structure (`src/`, `notebooks/`, `docs/`, `data/raw/`)
- [x] `requirements.txt` with milestone 1 dependencies pinned
- [x] `.gitignore` configured
- [x] `README.md` with project overview
- [x] Architecture diagram (`weather_pipeline.svg`)
- [x] **Fetch script** (`src/fetch_data.py`) — already coded, pulls weather for 10 cities from Open-Meteo
- [x] **Both notebook scaffolds** ready in `notebooks/`:
  - `01_explore_structure.ipynb`
  - `02_data_quality.ipynb`
- [x] `docs/data_exploration.md` template
- [x] All 6 collaborators added to the repo

This means you can clone the repo and start working immediately — no setup decisions needed.

---

## 🚀 First-Time Setup (do this once)

### Prerequisites

- **Python 3.10 or newer** — check with `python --version`
- **Git** — check with `git --version`
- **VS Code** (recommended) — with the Python and Jupyter extensions

If you don't have Python, get it from [python.org/downloads](https://www.python.org/downloads/). On Windows, **check "Add Python to PATH"** during install.

### Step 1 — Clone the repo

```bash
git clone https://github.com/mohamed-mahmoud-de/Weather-Data-Pipeline.git
cd Weather-Data-Pipeline
```

### Step 2 — Configure your Git identity

So your commits show up under your name on GitHub:

```bash
git config user.name "Your Name"
git config user.email "your-github-email@example.com"
```

Use the email registered on your GitHub account.

### Step 3 — Create a virtual environment

This isolates project packages from your system Python:

```bash
# Create
python -m venv venv

# Activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (cmd):
venv\Scripts\activate.bat
# Mac / Linux:
source venv/bin/activate
```

You'll know it worked when your terminal prompt starts with `(venv)`.

> **Reminder:** activate the venv every time you open a new terminal in this project.

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Run the fetch script

```bash
python src/fetch_data.py
```

You should see 10 success lines and now have 10 JSON files in `data/raw/`. **Do this first** — your notebooks will read from these files.

### Step 6 — Open the notebooks

In VS Code, open `notebooks/01_explore_structure.ipynb`. When prompted, select the **venv** kernel (Python 3.13.9 or whatever your venv shows). Run all cells with **Run All**.

If everything runs without errors, you're set up correctly.

---

## 🌿 Git Workflow (every contributor)

**Never push directly to `main`.** Use feature branches and pull requests.

### Starting a new task

```bash
git checkout main
git pull origin main             # always pull before starting
git checkout -b m1-explore-structure   # branch name describes your task
```

### While working

```bash
git add .
git commit -m "Clear message describing what changed"
git push -u origin m1-explore-structure
```

### When done

1. Open a Pull Request on GitHub from your branch into `main`
2. Tag Mohamed (or another teammate) for review
3. Once approved, merge it, then delete the branch

### Branch naming convention

- `m1-<task>` for milestone 1 work — e.g. `m1-explore-structure`, `m1-data-quality`
- `m2-<task>` for milestone 2 — e.g. `m2-transform-script`, `m2-schema-design`

---

## 📁 Project Structure

```
Weather-Data-Pipeline/
├── data/
│   └── raw/                    # 10 JSON dumps from Open-Meteo (gitignored)
├── docs/
│   └── data_exploration.md     # M1 deliverable: findings summary
├── notebooks/
│   ├── 01_explore_structure.ipynb
│   └── 02_data_quality.ipynb
├── src/
│   └── fetch_data.py           # Pulls weather data for 10 cities
├── venv/                       # Local virtual environment (gitignored)
├── .gitignore
├── README.md
├── requirements.txt
└── weather_pipeline.svg        # Architecture diagram
```

---

# 🗓️ Milestone 1 — Data Collection & Exploration

**Goal:** by the end of M1, the team understands exactly what data we're ingesting, what's wrong with it, and what the schema needs to look like in M2.

**Deliverables (from the project plan):** raw JSON samples, data exploration summary.

## Task assignments

| Person | Task | Output |
|---|---|---|
| **Mohamed Mahmoud** | Coordinate, review PRs, unblock the team | Code reviews, merge approvals |
| **Alaa Elfaramawy** | Run `fetch_data.py`, document any API errors or unusual responses | Comments on edge cases in `docs/data_exploration.md` |
| **Belquese Sahm** | Complete `01_explore_structure.ipynb`: walk through JSON structure, units, top-level keys, hourly array layout | Filled-in notebook with markdown explanations between cells |
| **Habeba AbdEldayem** | Complete `02_data_quality.ipynb`: null counts, value ranges, coordinate snapping check, time coverage | Filled-in notebook + a section in `docs/data_exploration.md` listing quality issues |
| **Mohamed Rifaat** | Consolidate findings into final `docs/data_exploration.md` (units, structure, issues, schema implications) | Polished markdown doc ready for M2 handoff |
| **Yahya Galal** | Sketch a preliminary schema (locations + observations tables) based on the exploration findings, ready for M2 | Draft `docs/schema_design.md` with table definitions |

## Definition of Done for M1

- [ ] All 6 teammates have cloned the repo, run `fetch_data.py` successfully, and pushed at least one commit
- [ ] Both notebooks are fully filled in and run end-to-end without errors
- [ ] `docs/data_exploration.md` is complete and reviewed
- [ ] `docs/schema_design.md` exists with first-draft table definitions
- [ ] All M1 PRs merged into `main`

---

# 🗓️ Milestone 2 — System Development & Data Transformation

**Goal:** clean, transform, and prepare weather data for database storage. Build the ETL scripts and the Postgres schema.

**Deliverables:** Python ETL scripts, PostgreSQL schema, transformed datasets.

## What this milestone actually means

Right now, our raw data is column-oriented JSON (Open-Meteo gives us `{time: [...], temp: [...]}` parallel arrays). We need to:

1. **Transform** it into row-oriented tabular data (one row per city per hour)
2. **Clean** it (handle nulls, validate ranges)
3. **Design** the Postgres schema (locations, weather_observations, forecasts)
4. **Load** it into Postgres and verify the data

## Step-by-step implementation

### Step 1 — Update dependencies

Add these to `requirements.txt`:

```
sqlalchemy==2.0.36
psycopg2-binary==2.9.10
```

Then everyone runs:
```bash
pip install -r requirements.txt
```

### Step 2 — Set up Postgres locally (temporary)

For M2, we just need Postgres running on your laptop. Easiest way:

```bash
# Pull and run a Postgres container (one command, no install)
docker run --name weather-pg \
  -e POSTGRES_USER=weather_user \
  -e POSTGRES_PASSWORD=weather_pass \
  -e POSTGRES_DB=weather_db \
  -p 5432:5432 \
  -d postgres:16
```

> If you don't have Docker, install it from [docker.com/get-started](https://www.docker.com/get-started). We'll use it heavily in M3 anyway.

Verify it's running:
```bash
docker ps
```

### Step 3 — Design the schema

Create `sql/01_create_schema.sql` with three tables:

- **`locations`** — dimension table: city, country, lat, lon, timezone, elevation
- **`weather_observations`** — fact table: location_id, observed_at, temperature, humidity, wind, pressure, etc.
- **`forecasts`** — same as observations + `forecast_made_at` to track forecast vs actual

Key constraints:
- `UNIQUE(location_id, observed_at)` on observations — prevents duplicates on retry
- Foreign key from observations → locations
- Use `TIMESTAMPTZ` (not `TIMESTAMP`) for all time columns

### Step 4 — Build the transform layer

Create `src/transform/`:

- `normalize.py` — flips column-oriented `hourly` JSON into rows. Each input file becomes a DataFrame with columns: `observed_at`, `temperature_c`, `humidity_pct`, etc.
- `clean.py` — handles nulls, applies type coercion, ensures timestamps are UTC
- `validate.py` — runs sanity checks (temp between -50 and 60, humidity 0–100, etc.). Drops or flags invalid rows.

### Step 5 — Build the load layer

Create `src/load/postgres_loader.py`:

- Connects to Postgres via SQLAlchemy
- Upserts cities into `locations` (insert if new, return location_id)
- Upserts observations into `weather_observations` using `INSERT ... ON CONFLICT DO UPDATE`

### Step 6 — Wire it all together

Create `src/run_etl.py` that does the full flow:

```
1. List JSON files in data/raw/
2. For each file: extract → transform → clean → validate → load
3. Log how many rows were inserted/updated
```

### Step 7 — Validate

Run analytical queries against the loaded data to make sure it makes sense:

```sql
-- How many rows per city?
SELECT l.city, COUNT(*) FROM weather_observations o
JOIN locations l USING(location_id)
GROUP BY l.city;

-- Latest observation per city
SELECT l.city, MAX(o.observed_at) FROM weather_observations o
JOIN locations l USING(location_id)
GROUP BY l.city;
```

If every city has the expected number of rows and recent timestamps, M2 is working.

## Task assignments for M2

| Person | Task | Output |
|---|---|---|
| **Mohamed Mahmoud** | Architecture decisions, code review, integrate everyone's PRs, write `src/run_etl.py` orchestrator | Working end-to-end ETL run |
| **Alaa Elfaramawy** | Build `src/transform/normalize.py` — flips column-oriented hourly JSON into row-based DataFrame | Transform module + unit tests |
| **Belquese Sahm** | Build `src/transform/clean.py` and `src/transform/validate.py` — null handling, type coercion, range checks | Clean & validate modules + tests |
| **Habeba AbdEldayem** | Write `sql/01_create_schema.sql` — three tables, constraints, indexes | SQL schema file + ER diagram in `docs/schema_design.md` |
| **Mohamed Rifaat** | Build `src/load/postgres_loader.py` — SQLAlchemy connection, upsert logic | Load module + tests |
| **Yahya Galal** | Write analytical SQL queries (`sql/02_analytical_queries.sql`) and validate the loaded data | Working query set + screenshots of results |

## Definition of Done for M2

- [ ] Postgres schema created and documented
- [ ] All transform modules pass tests
- [ ] Loader successfully populates all three tables
- [ ] `python src/run_etl.py` runs end-to-end with no errors
- [ ] At least 5 analytical queries written and verified
- [ ] `docs/schema_design.md` updated with final ERD
- [ ] All M2 PRs merged into `main`

---

## ⏭️ Looking Ahead

After M2, here's what's coming:

- **M3 — Dockerize everything.** Wrap the ETL in a Dockerfile. Use docker-compose to run Postgres + ETL together. Add Airflow as the scheduler.
- **M4 — Automate and monitor.** Hourly DAG runs. Logging at every step. Retries. Data freshness checks.
- **M5 — Demo and present.** Live pipeline run. SQL queries shown. Final slides.

---

## 🆘 Help & Communication

- **Stuck on something?** Open a draft PR early and tag Mohamed for help — better than struggling alone.
- **Found a bug in someone else's code?** Open a GitHub issue, don't fix it silently.
- **Disagreement on a design choice?** Discuss in PR comments or in the team chat — Mohamed makes the final call as team lead.

Let's build something great. 🌦️ 