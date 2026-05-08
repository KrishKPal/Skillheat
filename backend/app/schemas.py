"""
Pydantic response schemas.

These are NOT the ORM models — they're the JSON shapes the API emits.
Keeping them separate from ORM models lets the DB schema evolve without
breaking the API contract (and vice versa).
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CountryOut(BaseModel):
    """One country marker on the globe."""

    code: str
    name: str
    latitude: float
    longitude: float
    heat_score: float
    article_count_24h: int

    model_config = ConfigDict(from_attributes=True)


class NewsSourceOut(BaseModel):
    """Source attribution shown next to each headline."""

    slug: str
    name: str
    homepage_url: str | None = None
    category: str | None = None

    model_config = ConfigDict(from_attributes=True)


class NewsArticleOut(BaseModel):
    """One headline in the news stack."""

    id: int
    title: str
    summary: str | None = None
    url: str
    country_code: str | None = None
    published_at: datetime
    source: NewsSourceOut

    model_config = ConfigDict(from_attributes=True)


class GlobeStateOut(BaseModel):
    """
    Single payload for the homepage — gives the frontend everything it needs
    to render the globe + initial news stack in one round trip.
    """

    countries: list[CountryOut]
    total_articles_24h: int
    last_updated: datetime
