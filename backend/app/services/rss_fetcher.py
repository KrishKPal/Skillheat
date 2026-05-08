"""
RSS fetcher.

Pulls every active source, parses each feed, upserts articles into the DB.
Designed to fail gracefully — one bad feed never kills the whole run.

Dedup: news_articles.url has a unique constraint, so re-runs don't duplicate.
We use Postgres ON CONFLICT DO NOTHING for fast bulk upsert.
"""
import logging
from datetime import datetime, timezone
from typing import Iterable

import feedparser
import httpx
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.news_source import NewsSource
from app.models.news_article import NewsArticle


logger = logging.getLogger(__name__)

# Cap summary length so DB rows stay small and the UI looks consistent
SUMMARY_MAX_CHARS = 500

# Per-feed timeout. Slow feeds shouldn't hold up the whole run.
FETCH_TIMEOUT = 15

# Cap articles per feed per run. Most feeds give 10-50; we take 50 max.
MAX_PER_SOURCE = 50


def fetch_all(db: Session) -> dict[str, int]:
    """
    Fetch every active source and write articles to the DB.
    Returns {source_name: count_inserted}, with -1 indicating a fetch failure.
    """
    sources = db.execute(
        select(NewsSource).where(NewsSource.is_active.is_(True))
    ).scalars().all()
    logger.info(f"Fetching {len(sources)} active sources")

    stats: dict[str, int] = {}
    for source in sources:
        try:
            n = _fetch_one(db, source)
            stats[source.name] = n
            source.last_fetched_at = datetime.now(timezone.utc)
            db.commit()
        except Exception as e:
            logger.error(f"  {source.name} FAILED: {type(e).__name__}: {e}")
            stats[source.name] = -1
            db.rollback()

    return stats


def _fetch_one(db: Session, source: NewsSource) -> int:
    """Fetch one feed, parse it, upsert articles. Returns count inserted."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,ja;q=0.7",
        "Connection": "keep-alive",
    }
    response = httpx.get(
        source.feed_url,
        headers=headers,
        timeout=FETCH_TIMEOUT,
        follow_redirects=True,
    )
    response.raise_for_status()

    feed = feedparser.parse(response.content)
    if feed.bozo and not feed.entries:
        raise RuntimeError(f"feed parse error: {feed.bozo_exception}")

    candidates = list(_extract(feed.entries[:MAX_PER_SOURCE], source))
    if not candidates:
        return 0

    # Bulk upsert with dedup on URL
    stmt = insert(NewsArticle).values(candidates).on_conflict_do_nothing(
        index_elements=["url"]
    )
    result = db.execute(stmt)
    n = result.rowcount or 0
    logger.info(f"  {source.name}: +{n} new")
    return n


def _extract(entries: Iterable, source: NewsSource) -> Iterable[dict]:
    """Convert feedparser entries to dicts ready for ORM insertion."""
    for entry in entries:
        url = (entry.get("link") or "").strip()
        title = (entry.get("title") or "").strip()
        if not url or not title:
            continue

        # Pubdate fallbacks — RSS is the wild west on date formats
        published = (
            _parse_date(entry.get("published") or entry.get("updated") or "")
            or datetime.now(timezone.utc).replace(tzinfo=None)
        )

        summary = _clean(entry.get("summary") or entry.get("description") or "")

        yield {
            "title": title[:500],
            "summary": summary,
            "url": url[:1000],
            "published_at": published,
            "source_id": source.id,
            "country_code": source.default_country_code,
        }


def _parse_date(raw: str):
    """Best-effort date parser. Returns naive UTC datetime or None."""
    if not raw:
        return None
    try:
        dt = date_parser.parse(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    except (ValueError, TypeError):
        return None


def _clean(html: str) -> str:
    """Strip HTML, collapse whitespace, truncate."""
    if not html:
        return ""
    text = BeautifulSoup(html, "html.parser").get_text(separator=" ")
    text = " ".join(text.split())
    if len(text) > SUMMARY_MAX_CHARS:
        return text[:SUMMARY_MAX_CHARS - 1].rstrip() + "…"
    return text
