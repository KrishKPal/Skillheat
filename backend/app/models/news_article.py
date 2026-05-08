"""
NewsArticle model.

The core entity. Every headline shown in the dashboard is one of these.

Design choices worth noting:
- `url` is unique to dedupe across feed re-polls without needing a separate
  hash column. RSS feeds re-publish the same items often.
- `country_code` is denormalized from `source.default_country_code` so the
  dashboard can filter by country with a single index lookup, no joins.
  When v2 NER overrides the default, we just update this field.
- `published_at` is what we sort by, NOT `created_at`. RSS feeds can have
  items from days ago appear in a fresh fetch.
"""
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True)

    # The article's canonical URL — uniqueness here gives us free dedup.
    url = Column(String(1000), nullable=False, unique=True, index=True)

    title = Column(String(500), nullable=False)

    # Short description / summary from the RSS feed. Optional.
    summary = Column(Text, nullable=True)

    # FK to the source that gave us this article
    source_id = Column(
        Integer,
        ForeignKey("news_sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Denormalized country code for fast filtering on the globe.
    # Nullable for global / unattributable articles.
    country_code = Column(
        String(2),
        ForeignKey("countries.code", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Optional space-separated keywords/tags ("ai claude llm").
    # We'll use this in v2 for tech-specific filtering.
    tags = Column(String(500), nullable=True)

    # When the article was published per the RSS feed, NOT when we ingested it.
    # Indexed because every list query sorts by this DESC.
    published_at = Column(DateTime(timezone=True), nullable=False, index=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    source = relationship("NewsSource", back_populates="articles")
    country = relationship("Country", back_populates="articles")

    # Composite index for the most common query pattern:
    # "latest articles for country X"
    __table_args__ = (
        Index(
            "ix_articles_country_published",
            "country_code",
            "published_at",
        ),
    )

    def __repr__(self) -> str:
        return f"<NewsArticle id={self.id} {self.title[:40]!r}>"
