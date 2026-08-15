"""Application settings.

Values are read from environment variables (see docker-compose.yml) and fall
back to sensible local defaults. We use pydantic-settings so configuration is
typed and validated at startup, mirroring the `core/config.py` convention used
across the main codebase.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # postgresql+psycopg2 -> synchronous driver. We keep the boilerplate sync on
    # purpose: it is simpler to read and a Celery worker can reuse the exact same
    # Session, with no async/event-loop juggling.
    database_url: str = "postgresql+psycopg2://app:app@db:5432/app"

    # Used both as Celery broker and result backend.
    redis_url: str = "redis://redis:6379/0"

    # Where generated files (e.g. PDF thumbnails) are written. This directory is
    # a Docker volume shared between the `api` and `worker` containers so that a
    # file produced by the worker can be served by the api.
    media_dir: str = "/app/media"


settings = Settings()
