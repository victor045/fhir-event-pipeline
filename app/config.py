import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Kafka
    kafka_bootstrap_servers: str = Field("localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic: str = Field("fhir-events", env="KAFKA_TOPIC")

    # App
    app_name: str = "FHIR Event Pipeline"
    environment: str = Field("development", env="ENVIRONMENT")

    # Logging / Observability
    sentry_dsn: str = Field("", env="SENTRY_DSN")

    # Database
    database_url: str = Field(..., env="DATABASE_URL")  # ⬅️ Agregado

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Cacheado para no cargar múltiples veces
@lru_cache()
def get_settings() -> Settings:
    return Settings()

