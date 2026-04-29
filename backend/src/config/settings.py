from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DENTAL_AI_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "dental_ai"
    mongo_analyses_collection: str = "analyses"
    mongo_users_collection: str = "users"

    model_path: str = "../entrenamiento ia pruebas/best.pt"
    model_version: str = "best.pt"
    model_device: str = "auto"
    model_warmup_on_startup: bool = True
    model_confidence: float = 0.25
    model_iou: float = 0.45

    uploads_dir: str = "./storage/uploads"
    max_file_size_bytes: int = 10 * 1024 * 1024
    allowed_mime_types: list[str] = Field(default_factory=lambda: ["image/jpeg", "image/png"])

    log_level: str = "INFO"

    events_enabled: bool = True
    events_transport: str = "log"
    kafka_enabled: bool = False
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic_analysis_events: str = "analysis-events"

    auth_jwt_secret: str = "change-this-secret-in-production"
    auth_jwt_algorithm: str = "HS256"
    auth_access_token_expire_minutes: int = 60 * 24

    @field_validator("allowed_mime_types", mode="before")
    @classmethod
    def parse_mime_types(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return ["image/jpeg", "image/png"]

    @property
    def backend_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def resolved_model_path(self) -> Path:
        candidate = Path(self.model_path)
        if candidate.is_absolute():
            return candidate
        return (self.backend_root / candidate).resolve()

    @property
    def model_path_resolved(self) -> Path:
        return self.resolved_model_path

    @property
    def resolved_uploads_dir(self) -> Path:
        candidate = Path(self.uploads_dir)
        if candidate.is_absolute():
            return candidate
        return (self.backend_root / candidate).resolve()

    @property
    def uploads_path(self) -> Path:
        return self.resolved_uploads_dir


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
