from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class to retrieve environment variables.
    """

    DATABASE_URL: str
    SECRET_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JTI_EXPIRY: int
    ACCESS_TOKEN_EXPIRY: int
    REFRESH_TOKEN_EXPIRY: int
    # REDIS_HOST: str
    # REDIS_PORT: int
    # REDIS_PASSWORD: Optional[str] = None
    DOMAIN: str  # localhost or production domain

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


Config = Settings()
