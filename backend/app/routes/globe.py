"""
Globe endpoint.

`GET /api/globe` returns everything needed to render the globe on first paint:
all country markers with their heat scores. Frontend hits this once on mount,
then polls /api/news for fresh headlines on its own schedule.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Country, NewsArticle
from app.schemas import CountryOut, GlobeStateOut

router = APIRouter(prefix="/api", tags=["globe"])


@router.get("/globe", response_model=GlobeStateOut)
def get_globe_state(db: Session = Depends(get_db)) -> GlobeStateOut:
    """Return all country markers + dashboard metadata."""
    countries = db.query(Country).order_by(Country.heat_score.desc()).all()

    total_articles_24h = (
        db.query(func.coalesce(func.sum(Country.article_count_24h), 0)).scalar() or 0
    )

    return GlobeStateOut(
        countries=[CountryOut.model_validate(c) for c in countries],
        total_articles_24h=int(total_articles_24h),
        last_updated=datetime.now(timezone.utc),
    )
