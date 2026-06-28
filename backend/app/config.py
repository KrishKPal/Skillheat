"""
App configuration.

Reads .env once at import time and exposes a typed `settings` object.
Using pydantic-settings means typos in env var names fail loudly at startup
rather than silently producing wrong behavior at runtime.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://skillheat:skillheat_dev_pw@localhost:5432/skillheat"

    # CORS — comma-separated string in env, parsed to list via property below
    allowed_origins: str = "http://localhost:3000"

    # External APIs (optional for MVP, all RSS-based by default)
    news_api_key: str = ""

    # Background fetcher cadence (seconds). 0 disables the in-process loop.
    news_fetch_interval_seconds: int = 900

    # Run schema create + seed on startup. True is correct for a fresh
    # managed DB (e.g. Render) where you can't run one-off shell commands.
    init_on_startup: bool = True

    # Toggle real fetch vs mock data — useful in dev / tests / CI.
    # Defaults False so production serves real RSS unless told otherwise.
    use_mock_data: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        # Don't error if extra env vars are present — Docker/Render inject some
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def sqlalchemy_url(self) -> str:
        """
        Normalize the connection string. Render (and Heroku) hand out URLs
        starting with 'postgres://', but SQLAlchemy 2.x requires the explicit
        'postgresql://' (or a driver-qualified scheme). Rewrite it here so the
        rest of the app never has to care.
        """
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url


# Singleton — import this everywhere instead of constructing Settings repeatedly
settings = Settings()
