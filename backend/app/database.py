"""
SQLAlchemy engine + session factory.

Pattern: one global engine, per-request sessions via `get_db()` dependency.
This is the FastAPI-recommended way and avoids connection leaks.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


# `pool_pre_ping=True` checks connections are alive before handing them out.
# Without it, you get cryptic errors when Postgres restarts mid-day in dev.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    # echo=True is useful for debugging SQL queries during dev.
    # Leave off by default — it's noisy in logs.
    echo=False,
)

# Session factory: each call to SessionLocal() gives a fresh session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class all ORM models inherit from
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a DB session and closes it after the request.

    Usage in routes:
        @router.get(...)
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
