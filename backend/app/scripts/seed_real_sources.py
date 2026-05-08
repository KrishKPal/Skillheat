"""
Load real RSS sources into the news_sources table.

Run after init_db:
    python3 -m app.scripts.seed_real_sources

Idempotent — re-running updates rows by slug rather than failing.
"""
import logging
from sqlalchemy import select
from app.database import SessionLocal
from app.models.news_source import NewsSource
from app.data.news_sources import SOURCES

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


def main() -> None:
    db = SessionLocal()
    try:
        log.info(f"Upserting {len(SOURCES)} sources...")
        for slug, name, feed_url, homepage, country_code, category in SOURCES:
            existing = db.execute(
                select(NewsSource).where(NewsSource.slug == slug)
            ).scalar_one_or_none()

            if existing:
                existing.name = name
                existing.feed_url = feed_url
                existing.homepage_url = homepage
                existing.default_country_code = country_code
                existing.category = category
                existing.is_active = True
            else:
                db.add(NewsSource(
                    slug=slug,
                    name=name,
                    feed_url=feed_url,
                    homepage_url=homepage,
                    default_country_code=country_code,
                    category=category,
                    is_active=True,
                ))
        db.commit()
        log.info("Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
