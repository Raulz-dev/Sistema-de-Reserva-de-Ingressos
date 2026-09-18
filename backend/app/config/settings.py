from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sistema de reservas de ingressos - cinema"
    app_env: Literal["development", "production"] = "development"
    debug: bool = False
    database_url: str
    sql_echo: bool = False
    jwt_secret: str
    token_expiration_minutes: int
    algorithm: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
