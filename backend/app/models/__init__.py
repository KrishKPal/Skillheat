"""
ORM models — exported for convenient single-import use.

    from app.models import Country, NewsArticle, NewsSource
"""
from app.models.country import Country
from app.models.news_article import NewsArticle
from app.models.news_source import NewsSource

__all__ = ["Country", "NewsArticle", "NewsSource"]
