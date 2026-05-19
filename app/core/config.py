from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/events_db",
        env="POSTGRES_CONNECTION_STRING",
    )

    POSTGRES_HOST: str = Field(default="", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(default=5432, env="POSTGRES_PORT")
    POSTGRES_USER: str = Field(default="", env="POSTGRES_USERNAME")
    POSTGRES_PASSWORD: str = Field(default="", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="", env="POSTGRES_DATABASE_NAME")

    # Events Provider API
    EVENTS_PROVIDER_BASE_URL: str = Field(
        default="https://events-provider.dev-2.python-labs.ru"
    )
    EVENTS_PROVIDER_INTERNAL_URL: str = Field(
        default="https://student-system-events-provider-web.student-system-events-provider.svc:8000"
    )
    EVENTS_PROVIDER_API_KEY: str = Field(default="")

    # Sync settings
    SYNC_INTERVAL_HOURS: int = Field(default=24)
    SYNC_INITIAL_DATE: str = Field(default="2000-01-01")

    # API settings
    CACHE_SEATS_TTL_SECONDS: int = Field(default=30)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
