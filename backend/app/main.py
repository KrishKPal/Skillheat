"""
FastAPI app entry.

Run with:
    uvicorn app.main:app --reload --port 8000

Visit http://localhost:8000/docs for interactive API docs.

On startup (when settings.init_on_startup is True) the app:
  1. Creates tables from the ORM models (idempotent).
  2. Seeds countries and RSS sources (idempotent upserts).
  3. Starts a background thread that fetches RSS every
     settings.news_fetch_interval_seconds (0 disables it).

This consolidates what used to be separate manual scripts (init_db.py,
seed_*.py, fetch_news.py) so a managed host like Render — where you can't
easily run one-off shell commands against the DB — boots into a working
state on its own.
"""
import logging
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import globe, health, news

log = logging.getLogger("skillheat.startup")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Event used to stop the background loop cleanly on shutdown.
_stop_event = threading.Event()


def _init_database() -> None:
    """Create tables and seed reference data. Each step is isolated so one
    failure doesn't abort the rest of startup."""
    from app.database import Base, engine
    from app import models  # noqa: F401  (registers models on Base.metadata)

    try:
        log.info("Creating tables (if missing)...")
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        log.error(f"create_all failed: {type(e).__name__}: {e}")
        return  # No tables -> seeding will fail too; bail out of init.

    try:
        from app.scripts.seed_countries import main as seed_countries
        log.info("Seeding countries...")
        seed_countries()
    except Exception as e:
        log.error(f"seed_countries failed: {type(e).__name__}: {e}")

    try:
        from app.scripts.seed_real_sources import main as seed_real_sources
        log.info("Seeding sources...")
        seed_real_sources()
    except Exception as e:
        log.error(f"seed_real_sources failed: {type(e).__name__}: {e}")


def _run_one_fetch() -> None:
    """Run a single RSS fetch + heat recompute, swallowing all errors so the
    loop never dies."""
    from app.database import SessionLocal
    from app.services.rss_fetcher import fetch_all

    db = SessionLocal()
    try:
        stats = fetch_all(db)
        total = sum(n for n in stats.values() if n > 0)
        log.info(f"Fetch complete: +{total} new articles")

        # Heat scoring is optional — only run it if the module is present.
        try:
            from app.services.heat_scorer import recompute_heat_scores
            recompute_heat_scores(db)
            log.info("Heat scores recomputed")
        except ImportError:
            log.warning("heat_scorer not found; skipping heat recompute")
        except Exception as e:
            log.error(f"heat recompute failed: {type(e).__name__}: {e}")
    except Exception as e:
        log.error(f"fetch_all failed: {type(e).__name__}: {e}")
        db.rollback()
    finally:
        db.close()


def _fetch_loop() -> None:
    """Background worker: fetch immediately, then every N seconds until stop."""
    interval = settings.news_fetch_interval_seconds
    log.info(f"Background fetcher starting (every {interval}s)")
    while not _stop_event.is_set():
        _run_one_fetch()
        # Wait returns True if the event was set during the wait -> exit promptly.
        if _stop_event.wait(timeout=interval):
            break
    log.info("Background fetcher stopped")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown actions."""
    if settings.init_on_startup:
        _init_database()

    fetcher_thread = None
    if not settings.use_mock_data and settings.news_fetch_interval_seconds > 0:
        fetcher_thread = threading.Thread(target=_fetch_loop, daemon=True)
        fetcher_thread.start()
    else:
        log.info("Background fetcher disabled (mock data or interval=0)")

    yield

    # Shutdown: signal the loop and give it a moment to exit.
    _stop_event.set()
    if fetcher_thread is not None:
        fetcher_thread.join(timeout=5)


app = FastAPI(
    title="SkillHeat API",
    description="Tech signal engine + 3D globe news dashboard.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — necessary because the Next.js frontend runs on a different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET"],  # only GETs in v1; widen if/when we add writes
    allow_headers=["*"],
)

# Mount routers — keep this list short and scannable
app.include_router(health.router)
app.include_router(globe.router)
app.include_router(news.router)


@app.get("/")
def root() -> dict:
    """Friendly landing payload — no logic, just confirms the API is alive."""
    return {
        "name": "SkillHeat API",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": ["/api/health", "/api/globe", "/api/news"],
    }
