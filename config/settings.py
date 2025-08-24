from __future__ import annotations
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SENKRON API"
    APP_VERSION: str = "0.2.0"
    TELEMETRY_DIR: str = "logs/telemetry"
    METRICS_DIR: str = "logs/metrics"
    OUTPUT_DIR: str = "data-pipelines/output"
    ENV: str = "dev"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache
def get_settings() -> Settings:
    return Settings()
