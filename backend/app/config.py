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

    # Background fetcher cadence
    news_fetch_interval_seconds: int = 300

    # Toggle real fetch vs mock data — useful in dev / tests / CI
    use_mock_data: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        # Don't error if extra env vars are present — Docker injects some
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


# Singleton — import this everywhere instead of constructing Settings repeatedly
settings = Settings()
