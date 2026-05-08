"""
Health check.

`GET /api/health` — used by Docker healthchecks, uptime monitors, and as a
sanity check from the frontend on first load.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health(db: Session = Depends(get_db)) -> dict:
    """Return ok if the API is up and the DB is reachable."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}
    except Exception as e:
        return {"status": "ok", "database": f"error: {type(e).__name__}"}
