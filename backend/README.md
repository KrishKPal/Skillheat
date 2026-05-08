# SkillHeat Backend

FastAPI + PostgreSQL backend for SkillHeat.

## Quick start

Make sure Postgres is running (via the `docker-compose.yml` at the repo root):

```bash
# from the repo root
docker compose up -d
```

Then from this `backend/` directory:

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env if your DATABASE_URL differs. Defaults match docker-compose.yml.

# 4. Initialize the database
python -m app.scripts.init_db

# 5. Seed mock data (so the frontend has something to render)
python -m app.scripts.seed_mock_data

# 6. Run the API
uvicorn app.main:app --reload --port 8000
```

Visit:
- http://localhost:8000/ — API metadata
- http://localhost:8000/docs — interactive API docs
- http://localhost:8000/api/health — health check
- http://localhost:8000/api/globe — globe state (countries + heat)
- http://localhost:8000/api/news — latest headlines
- http://localhost:8000/api/news?country=US — filtered to US

## Project layout

```
app/
├── main.py              FastAPI entry point
├── config.py            Settings loaded from .env
├── database.py          SQLAlchemy engine + session factory
├── schemas.py           Pydantic response shapes
├── models/              ORM models (Country, NewsSource, NewsArticle)
├── routes/              HTTP endpoints (one file per resource)
├── services/            Business logic (added next step — RSS pipeline)
├── scripts/             Standalone scripts (init_db, seed_mock_data)
└── data/                Static seed data (countries, news source list)
```

## Re-seeding

`seed_mock_data.py` is idempotent for countries and sources. For articles it
clears all mock articles (`url LIKE 'mock://%'`) and reinserts. Real articles
ingested by the RSS pipeline are untouched.

## Resetting the database

```bash
docker compose down -v   # nukes the postgres volume
docker compose up -d
python -m app.scripts.init_db
python -m app.scripts.seed_mock_data
```
