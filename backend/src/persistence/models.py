from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AnalysisStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DetectionRecord(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    bbox_xyxy: list[float]
    label: str


class AnalysisRecord(BaseModel):
    analysis_id: str
    user_id: str | None = None
    file_name: str
    file_path: str
    mime_type: str
    file_size_bytes: int
    status: AnalysisStatus
    detections: list[DetectionRecord] = Field(default_factory=list)
    inference_time_ms: float = 0.0
    model_version: str
    error_message: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_mongo(self) -> dict[str, Any]:
        payload = self.model_dump()
        payload["status"] = self.status.value
        return payload

    @classmethod
    def from_mongo(cls, data: dict[str, Any]) -> "AnalysisRecord":
        normalized = dict(data)
        normalized.pop("_id", None)
        return cls.model_validate(normalized)
