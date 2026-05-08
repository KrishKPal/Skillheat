"""
FastAPI app entry.

Run with:
    uvicorn app.main:app --reload --port 8000

Visit http://localhost:8000/docs for interactive API docs.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import globe, health, news


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Hook for startup/shutdown actions. We'll add the news fetcher here later."""
    # Startup: nothing yet — DB schema is created by `init_db.py`, not on app boot.
    # Adding it here would slow cold starts and complicate testing.
    yield
    # Shutdown: nothing yet.


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
