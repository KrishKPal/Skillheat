"""
Country model.

Each country is a node on the 3D globe. We use ISO 3166-1 alpha-2 codes
(e.g. 'US', 'IN', 'GB') as the canonical identifier — globe.gl uses these too,
so the frontend can look up a country by code without any translation layer.

`heat_score` is computed periodically and cached here so the globe loads fast.
We don't compute it on read — the dashboard can't afford that latency.
"""
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Country(Base):
    __tablename__ = "countries"

    # ISO 3166-1 alpha-2 code, e.g. "US", "IN". Primary key for simplicity.
    code = Column(String(2), primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    # Geographic centroid — used to place pulse markers on the globe.
    # Pre-populated from a static dataset; we don't compute these.
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # 0-100. Higher = more tech activity. Recomputed by the news fetcher.
    # Default 0 so newly-seeded countries don't appear "lit" until we have data.
    heat_score = Column(Float, default=0.0, nullable=False)

    # Number of articles tagged to this country in the last 24h.
    # Cached here for the globe's pulse intensity.
    article_count_24h = Column(Integer, default=0, nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    articles = relationship("NewsArticle", back_populates="country")

    def __repr__(self) -> str:
        return f"<Country {self.code} {self.name} heat={self.heat_score}>"
