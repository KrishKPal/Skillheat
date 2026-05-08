"""
Seed mock data.

Populates countries + news_sources from the static data files, then inserts
a batch of fake articles so the dashboard shows realistic-looking content
the moment you boot it up — before the real RSS fetcher runs.

Run:
    python -m app.scripts.seed_mock_data

Idempotent for countries and sources (uses upsert-ish logic).
For articles, it deletes anything with a `mock://` URL prefix and reinserts,
so re-running gives you a fresh batch without piling up duplicates.
"""
from datetime import datetime, timedelta, timezone
import random

from sqlalchemy.orm import Session

from app.data.countries import COUNTRIES
from app.data.news_sources import NEWS_SOURCES
from app.database import SessionLocal
from app.models import Country, NewsArticle, NewsSource


# Realistic-sounding mock headlines per country/topic.
# Spread across a few days so the "last 24h" filter has variety.
MOCK_HEADLINES = [
    # AI / LLM
    ("Anthropic announces Claude 4.7 with extended context window", "ai", "US"),
    ("OpenAI's Dev Day keynote highlights agentic SDK", "ai", "US"),
    ("Google DeepMind ships Gemini 3 with native tool use", "ai", "US"),
    ("Mistral releases new open-weights model under Apache 2.0", "ai", "FR"),
    ("Bharti AI raises $50M Series B to build India-focused LLM", "ai", "IN"),
    ("Baidu unveils Ernie 5 with multimodal reasoning", "ai", "CN"),
    ("Cohere announces enterprise RAG offering for Fortune 500", "ai", "CA"),
    # Dev tools / infrastructure
    ("Vercel ships v0 to general availability after beta", "dev-tools", "US"),
    ("GitHub adds Copilot Workspace to all paid tiers", "dev-tools", "US"),
    ("Bun 1.2 released with improved Node compatibility", "dev-tools", "US"),
    ("Deno raises $40M to push deeper into edge computing", "dev-tools", "US"),
    ("UK startup ships Kubernetes alternative for small teams", "dev-tools", "GB"),
    # Frameworks
    ("Next.js 16 introduces partial prerendering as default", "frameworks", "US"),
    ("Remix merges into React Router as v7 ships", "frameworks", "US"),
    ("Svelte 6 promises 30% smaller bundle sizes", "frameworks", "GB"),
    ("Astro adds streaming server components", "frameworks", "DE"),
    # Funding / startup
    ("Bengaluru-based fintech raises $25M Series A", "funding", "IN"),
    ("Berlin AI infra startup closes €18M seed round", "funding", "DE"),
    ("Singapore's Sea Group invests in regional AI labs", "funding", "SG"),
    ("São Paulo dev tools startup reaches Series B", "funding", "BR"),
    ("Lagos fintech secures $15M to expand across Africa", "funding", "NG"),
    # Hardware / chips
    ("NVIDIA ships RTX 50 series targeting on-device AI", "hardware", "US"),
    ("Apple unveils M5 chip with neural engine refresh", "hardware", "US"),
    ("TSMC's 2nm process enters volume production", "hardware", "JP"),  # near JP/TW
    ("Samsung announces HBM4 memory for AI accelerators", "hardware", "KR"),
    # Geopolitics-tech
    ("EU AI Act enforcement begins for foundation model providers", "policy", "DE"),
    ("India's Digital India Bill clears parliamentary committee", "policy", "IN"),
    ("UK regulator probes major cloud providers' market share", "policy", "GB"),
    # Global / dev community
    ("Hacker News thread on RAG vs fine-tuning hits 2k upvotes", "discussion", None),
    ("dev.to publishes 2026 developer survey results", "discussion", None),
    ("Stack Overflow traffic continues post-AI decline", "discussion", None),
]


def upsert_countries(db: Session) -> int:
    """Insert or update each seed country. Returns count of countries in DB."""
    for c in COUNTRIES:
        existing = db.query(Country).filter(Country.code == c["code"]).first()
        if existing:
            existing.name = c["name"]
            existing.latitude = c["latitude"]
            existing.longitude = c["longitude"]
        else:
            db.add(Country(**c))
    db.commit()
    return db.query(Country).count()


def upsert_sources(db: Session) -> int:
    """Insert or update each seed news source."""
    for s in NEWS_SOURCES:
        existing = db.query(NewsSource).filter(NewsSource.slug == s["slug"]).first()
        if existing:
            for key, val in s.items():
                setattr(existing, key, val)
        else:
            db.add(NewsSource(**s))
    db.commit()
    return db.query(NewsSource).count()


def reseed_mock_articles(db: Session) -> int:
    """Delete any prior mock articles and insert a fresh batch."""
    db.query(NewsArticle).filter(NewsArticle.url.like("mock://%")).delete(
        synchronize_session=False
    )
    db.commit()

    sources_by_country: dict[str | None, list[NewsSource]] = {}
    for src in db.query(NewsSource).all():
        sources_by_country.setdefault(src.default_country_code, []).append(src)

    now = datetime.now(timezone.utc)
    inserted = 0

    for i, (title, tag, country_code) in enumerate(MOCK_HEADLINES):
        # Pick a source whose default country matches; fall back to global sources
        candidates = sources_by_country.get(country_code) or sources_by_country.get(
            None
        )
        if not candidates:
            continue
        source = random.choice(candidates)

        # Spread across last ~36 hours so "last 24h" isn't all-or-nothing
        published_at = now - timedelta(
            hours=random.uniform(0, 36),
            minutes=random.uniform(0, 60),
        )

        article = NewsArticle(
            url=f"mock://article/{i}-{source.slug}",
            title=title,
            summary=f"[Mock article seeded for development. Tag: {tag}]",
            source_id=source.id,
            country_code=country_code,
            tags=tag,
            published_at=published_at,
        )
        db.add(article)
        inserted += 1

    db.commit()
    return inserted


def recompute_country_heat(db: Session) -> None:
    """
    Update each country's heat_score and article_count_24h based on current data.

    For mock data we use a simple proxy: 24h article count, normalized to 0-100
    by scaling against the country with the most articles.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    counts: dict[str, int] = {}
    for article in (
        db.query(NewsArticle).filter(NewsArticle.published_at >= cutoff).all()
    ):
        if article.country_code:
            counts[article.country_code] = counts.get(article.country_code, 0) + 1

    max_count = max(counts.values()) if counts else 1

    for country in db.query(Country).all():
        n = counts.get(country.code, 0)
        country.article_count_24h = n
        # Scale to 0-100, with a small floor so low-activity countries are dimly lit.
        country.heat_score = round((n / max_count) * 100, 1) if n else 0.0

    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        n_countries = upsert_countries(db)
        n_sources = upsert_sources(db)
        n_articles = reseed_mock_articles(db)
        recompute_country_heat(db)
        print(f"Seeded {n_countries} countries, {n_sources} sources, {n_articles} mock articles.")
        print("Country heat scores recomputed.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
