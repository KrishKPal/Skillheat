"""
News endpoints.

`GET /api/news` — global feed (all countries)
`GET /api/news?country=US` — filtered to one country
`GET /api/news?since=2026-05-01T00:00:00Z` — only articles newer than X
                                              (used by the polling loop on FE)

We deliberately keep this small. No pagination yet — limit-based cutoff is fine
for an MVP that shows the latest 50 headlines. Add cursor pagination in v2.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import NewsArticle
from app.schemas import NewsArticleOut

router = APIRouter(prefix="/api", tags=["news"])


@router.get("/news", response_model=list[NewsArticleOut])
def list_news(
    country: Optional[str] = Query(
        None, min_length=2, max_length=2, description="ISO alpha-2 country code"
    ),
    limit: int = Query(50, ge=1, le=200),
    since: Optional[datetime] = Query(
        None, description="Only return articles published after this UTC timestamp"
    ),
    db: Session = Depends(get_db),
) -> list[NewsArticleOut]:
    """Latest headlines, optionally scoped to a country or to a freshness window."""
    q = db.query(NewsArticle).options(joinedload(NewsArticle.source))

    if country:
        q = q.filter(NewsArticle.country_code == country.upper())

    if since:
        q = q.filter(NewsArticle.published_at > since)

    articles = q.order_by(NewsArticle.published_at.desc()).limit(limit).all()

    return [NewsArticleOut.model_validate(a) for a in articles]


@router.get("/news/{article_id}", response_model=NewsArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)) -> NewsArticleOut:
    """Fetch one article by ID — used for the future article detail panel."""
    article = (
        db.query(NewsArticle)
        .options(joinedload(NewsArticle.source))
        .filter(NewsArticle.id == article_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return NewsArticleOut.model_validate(article)
