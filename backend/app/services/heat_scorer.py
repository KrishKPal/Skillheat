"""
Recompute country heat scores from recent article volume.

For v1, heat is normalized 24h-article-count per country. Simple and honest:
"this country produced more tech news in the last 24h."

Run after fetch_news so heat reflects fresh data.
"""
import logging
from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.country import Country
from app.models.news_article import NewsArticle


logger = logging.getLogger(__name__)

HEAT_WINDOW_HOURS = 24


def recompute_heat_scores(db: Session) -> dict[str, int]:
    """Compute heat (0-100) for every country. Returns {code: score}."""
    cutoff = datetime.utcnow() - timedelta(hours=HEAT_WINDOW_HOURS)

    counts_query = (
        select(NewsArticle.country_code, func.count(NewsArticle.id))
        .where(
            NewsArticle.published_at >= cutoff,
            NewsArticle.country_code.is_not(None),
        )
        .group_by(NewsArticle.country_code)
    )
    raw_counts = dict(db.execute(counts_query).all())

    if not raw_counts:
        logger.warning("No recent articles — heat scores unchanged")
        return {}

    # Normalize: max count = 100. Use sqrt to compress so US (likely dominant)
    # doesn't make every other country look cold.
    max_count = max(raw_counts.values())
    scores: dict[str, int] = {}
    for code, count in raw_counts.items():
        normalized = (count / max_count) ** 0.5
        scores[code] = int(normalized * 100)

    countries = db.execute(select(Country)).scalars().all()
    for country in countries:
        country.heat_score = scores.get(country.code, 0)
        country.article_count_24h = raw_counts.get(country.code, 0)

    db.commit()
    logger.info(f"Updated heat scores for {len(scores)} countries")
    return scores
