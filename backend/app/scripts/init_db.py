"""
Database initialization.

Creates all tables defined by the ORM models. Idempotent — running twice
is harmless.

Run:
    python -m app.scripts.init_db

For schema migrations later, swap this for Alembic. We don't need it yet.
"""
from app.database import Base, engine

# Import models so SQLAlchemy registers them on Base.metadata
from app import models  # noqa: F401


def main() -> None:
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done. Tables in DB:")
    for table_name in sorted(Base.metadata.tables.keys()):
        print(f"  - {table_name}")


if __name__ == "__main__":
    main()
