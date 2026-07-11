from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        url = "postgresql://" + url.removeprefix("postgres://")
    if url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url.removeprefix("postgresql://")
    return url


def strip_wrapping_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    jwt_secret: str
    admin_username: str
    admin_password_hash: str
    cors_origins: str = "http://localhost:5173"
    jwt_expire_hours: int = 12

    def resolved_database_url(self) -> str:
        return normalize_database_url(self.database_url)

    def resolved_password_hash(self) -> str:
        return strip_wrapping_quotes(self.admin_password_hash)


@lru_cache
def get_settings() -> Settings:
    return Settings()
