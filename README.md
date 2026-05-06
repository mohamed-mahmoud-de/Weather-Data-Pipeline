# Weather Data Pipeline

**DEPI Capstone Project** — End-to-end batch data engineering pipeline that extracts hourly weather data from the Open-Meteo API, transforms and validates it with Python, and loads it into a PostgreSQL database.

## Tech Stack

| Layer | Tool |
|-------|------|
| Data source | Open-Meteo API (free, no auth) |
| Language | Python 3.10+ |
| Database | PostgreSQL 16 |
| Containerization | Docker & Docker Compose |
| Scheduling | Apache Airflow (M4) |
| Version control | Git & GitHub |

## Project Milestones

| # | Milestone | Status |
|---|-----------|--------|
| M1 | Data Collection & Exploration | ✅ Done |
| M2 | System Development & Transformation | 🔄 In Progress |
| M3 | Deployment (Batch Processing) | ⬜ Not Started |
| M4 | Automation, Monitoring, Reliability | ⬜ Not Started |
| M5 | Documentation, Demo, Presentation | ⬜ Not Started |

## Quick Start

### Prerequisites

- Python 3.10+
- Docker Desktop
- Git

### 1. Clone & set up environment

```bash
git clone https://github.com/mohamed-mahmoud-de/Weather-Data-Pipeline.git
cd Weather-Data-Pipeline
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
copy .env.example .env         # Windows
# Edit .env if you changed the defaults
```

### 3. Start PostgreSQL

```bash
docker compose up -d
```

### 4. Fetch raw data

```bash
python src/fetch_data.py
```

### 5. Run the ETL pipeline

```bash
python src/run_etl.py
```

## Repository Structure

```
Weather-Data-Pipeline/
├── data/
│   ├── raw/            # Raw JSON from Open-Meteo (gitignored)
│   └── processed/      # Intermediate transformed files (gitignored)
├── docs/
│   ├── data_exploration.md
│   └── schema_design.md
├── notebooks/
│   ├── 01_explore_structure.ipynb
│   └── 02_data_quality.ipynb
├── sql/
│   ├── 01_create_schema.sql
│   └── 02_analytical_queries.sql
├── src/
│   ├── fetch_data.py
│   ├── run_etl.py
│   ├── transform/
│   │   ├── normalize.py
│   │   ├── clean.py
│   │   └── validate.py
│   └── load/
│       └── postgres_loader.py
├── test/
│   ├── test_normalize.py
│   ├── test_clean.py
│   ├── test_validate.py
│   └── test_loader.py
├── .env.example
├── docker-compose.yml
├── requirements.txt
└── TEAM_GUIDE.md
```

## Team

| Name | Role |
|------|------|
| Mohamed Mahmoud | Team Lead |
| Alaa Elfaramawy | Data Engineer |
| Belquese Sahm | Data Engineer |
| Habeba AbdEldayem | Data Engineer |
| Mohamed Rifaat | Data Engineer |
| Yahya Galal | Data Engineer |

See [TEAM_GUIDE.md](TEAM_GUIDE.md) for task assignments, setup instructions, and the Git workflow.
