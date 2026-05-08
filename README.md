# SkillHeat

A real-time tech news dashboard with a 3D interactive globe. Click any country to see what's happening in tech there, with live news from 100+ sources updating every minute.

![Status](https://img.shields.io/badge/status-MVP-blue) ![Backend](https://img.shields.io/badge/backend-FastAPI-009688) ![Frontend](https://img.shields.io/badge/frontend-Next.js-black)

---

## What it does

- Aggregates real-time tech news from major publications worldwide
- Renders an interactive 3D globe with heat indicators per country
- Click a country to filter news to that region
- Live-polling news feed with breaking-news ticker
- Dark command-center aesthetic

---

## Tech stack

**Backend** — Python, FastAPI, PostgreSQL, SQLAlchemy
**Frontend** — Next.js, TypeScript, react-globe.gl, three.js, SWR
**Infra** — Docker Compose for local Postgres

---

## Getting started

### Prerequisites

- Docker Desktop
- Python 3.12 (recommended via [python.org installer](https://www.python.org/downloads/macos/))
- Node.js 18+
- Git

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/skillheat.git
cd skillheat
docker compose up -d
```

**Backend:**

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

python3 -m app.scripts.init_db
python3 -m app.scripts.seed_countries
python3 -m app.scripts.seed_real_sources
python3 -m app.scripts.fetch_news

uvicorn app.main:app --reload --port 8000
```

**Frontend** (new terminal):

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open **http://localhost:3000**

---

## Project structure

```
skillheat/
├── docker-compose.yml
├── backend/        FastAPI + Postgres
└── frontend/       Next.js + TypeScript
```

---

## Roadmap

- [x] News aggregation pipeline
- [x] 3D interactive globe
- [x] Per-country news filtering
- [x] Live polling
- [ ] Tech trend verdicts (rising / stable / declining)
- [ ] Per-technology detail pages
- [ ] Search and filtering
- [ ] Public deployment

---

## License

All rights reserved.

---
