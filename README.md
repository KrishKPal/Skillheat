
# SkillHeat 🌍⚡

**Track the global pulse of technology — in real time.**

SkillHeat is a live tech intelligence platform that maps breaking technology news onto an interactive 3D globe. Explore what’s trending across countries, monitor regional innovation hotspots, and watch the global tech ecosystem evolve minute by minute.

Built by **Krish Kumar Pal**

<img width="1470" height="801" alt="Screenshot 2026-05-09 at 12 22 22 AM" src="https://github.com/user-attachments/assets/8099b37e-a0c8-4373-856a-cc73bd1dd54d" />
---

# 🚀 Features

## 🌐 Interactive 3D Tech Globe

- Rotate, zoom, and explore the world in real time
- Heat indicators visualize global tech activity
- Click any country to instantly filter regional news

## 📰 Real-Time News Aggregation

- Pulls live updates from 100+ tech sources worldwide
- Auto-refreshing feed with breaking-news ticker
- Tracks emerging trends across regions

## ⚡ Live Intelligence Dashboard

- Country-wise tech momentum visualization
- Fast, responsive UI with smooth animations
- Dark command-center inspired design

## 🔄 Continuous Updates

- Background polling system refreshes news every minute
- Dynamic feed updates without page reloads

---

# 🧠 Why SkillHeat?

Most news platforms show headlines.

SkillHeat shows **where innovation is happening**.

Instead of scrolling endless feeds, you can visually explore:

- Which countries are dominating AI discussions
- Where startup ecosystems are heating up
- Which regions are driving cybersecurity, robotics, chip manufacturing, or climate-tech conversations

It turns global tech news into a spatial, real-time experience.

---

# 🛠 Tech Stack

## Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy

## Frontend

- Next.js
- TypeScript
- three.js
- react-globe.gl
- SWR

## Infrastructure

- Docker Compose
- Local PostgreSQL containerized setup

---

# ⚙️ Getting Started

## Prerequisites

- Docker Desktop
- Python 3.12+
- Node.js 18+
- Git

---

# 1️⃣ Clone the Repository

```bash
git clone https://github.com/KrishKPal/skillheat.git
cd skillheat
```

---

# 2️⃣ Start PostgreSQL

```bash
docker compose up -d
```

---

# 3️⃣ Backend Setup

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

Backend runs on:

```bash
http://localhost:8000
```

---

# 4️⃣ Frontend Setup

Open a new terminal:

```bash
cd frontend

npm install

cp .env.example .env.local

npm run dev
```

Frontend runs on:

```bash
http://localhost:3000
```

---

# 📂 Project Structure

```bash
skillheat/
├── backend/                # FastAPI backend
│   ├── app/
│   └── scripts/
│
├── frontend/               # Next.js frontend
│   ├── components/
│   ├── pages/
│   └── lib/
│
├── docker-compose.yml
└── README.md
```

---

# ✅ Current Progress

- [x] Real-time news aggregation pipeline
- [x] Interactive 3D globe visualization
- [x] Country-based filtering system
- [x] Live polling architecture
- [x] Breaking news ticker
- [x] Responsive dark UI

### It will be deployed soon

---


# 📸 Preview

> “See the world of technology move in real time.”

SkillHeat combines data visualization, real-time systems, and immersive UI into a single global dashboard experience.

---

# 📜 License

All rights reserved.

---

# ⭐ Note
SkillHeat started as an experiment in combining:

- real-time systems
- data aggregation
- spatial visualization
- interactive frontend engineering

