"""
NewsSource model.

A news source is one RSS feed we poll periodically. Each source has a
`default_country_code` because the simplest country-tagging strategy is
"trust the source's home country" — TechCrunch articles default to US,
YourStory defaults to IN, etc.

This is a deliberate v1 simplification. v2 will run NER on headlines
to override the default when articles mention specific countries.
"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class NewsSource(Base):
    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True)

    # Display name shown in the UI ("TechCrunch", "Hacker News")
    name = Column(String(100), nullable=False, unique=True)

    # Slug for stable URLs and CSS hooks ("techcrunch", "hacker-news")
    slug = Column(String(100), nullable=False, unique=True, index=True)

    # The RSS feed URL we poll
    feed_url = Column(String(500), nullable=False)

    # Optional homepage URL for "view source" links
    homepage_url = Column(String(500), nullable=True)

    # Default country to tag articles with (FK to countries.code).
    # Nullable because some sources are global (e.g. Hacker News).
    default_country_code = Column(
        String(2),
        ForeignKey("countries.code", ondelete="SET NULL"),
        nullable=True,
    )

    # Free-form category label ("ai", "general-tech", "web-dev").
    # Used for filter chips in the UI.
    category = Column(String(50), nullable=True)

    # Whether to actively poll this source
    is_active = Column(Boolean, default=True, nullable=False)

    last_fetched_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    articles = relationship("NewsArticle", back_populates="source")

    def __repr__(self) -> str:
        return f"<NewsSource {self.slug}>"
