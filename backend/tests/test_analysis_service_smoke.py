from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from src.config.settings import Settings
from src.domain.exceptions import InferenceError
from src.events.publishers import EventPublisher
from src.persistence.models import AnalysisRecord, AnalysisStatus, DetectionRecord
from src.services.analysis_service import AnalysisService


@dataclass
class FakeStoredUpload:
    analysis_id: str
    file_name: str
    mime_type: str
    file_size_bytes: int
    file_path: Path


class FakeUploadService:
    async def save_upload(self, _upload: object) -> FakeStoredUpload:
        return FakeStoredUpload(
            analysis_id="analysis-1",
            file_name="rx.png",
            mime_type="image/png",
            file_size_bytes=1024,
            file_path=Path("/tmp/rx.png"),
        )


class FakeInferenceService:
    model_version = "best.pt"

    async def run_inference(self, _image_path: Path) -> tuple[list[DetectionRecord], float]:
        return [
            DetectionRecord(
                class_id=0,
                class_name="caries",
                confidence=0.92,
                bbox_xyxy=[1.0, 2.0, 3.0, 4.0],
                label="caries 92",
            )
        ], 15.3


class FakeInferenceServiceFail:
    model_version = "best.pt"

    async def run_inference(self, _image_path: Path) -> tuple[list[DetectionRecord], float]:
        raise RuntimeError("inference boom")


class FakeEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def publish(self, event_name: str, payload: dict[str, Any]) -> None:
        self.calls.append((event_name, payload))


class FakeRepository:
    def __init__(self) -> None:
        self.created: AnalysisRecord | None = None

    async def create_analysis(self, analysis: AnalysisRecord) -> AnalysisRecord:
        self.created = analysis
        return analysis

    async def get_by_analysis_id(self, _analysis_id: str) -> AnalysisRecord | None:
        return self.created

    async def get_by_analysis_id_for_user(self, _analysis_id: str, user_id: str) -> AnalysisRecord | None:
        if self.created is None or self.created.user_id != user_id:
            return None
        return self.created

    async def list_analyses(self, limit: int, offset: int) -> list[AnalysisRecord]:
        if self.created is None:
            return []
        return [self.created][offset : offset + limit]

    async def list_analyses_by_user(self, user_id: str, limit: int, offset: int) -> list[AnalysisRecord]:
        if self.created is None or self.created.user_id != user_id:
            return []
        return [self.created][offset : offset + limit]

    async def count_all(self) -> int:
        return 1 if self.created else 0

    async def count_by_status(self, status: str) -> int:
        if self.created is None:
            return 0
        return 1 if self.created.status.value == status else 0


@pytest.mark.asyncio
async def test_analysis_service_upload_and_analyze_smoke() -> None:
    settings = Settings()
    repository = FakeRepository()
    event_publisher = FakeEventPublisher()
    service = AnalysisService(
        settings=settings,
        upload_service=FakeUploadService(),
        inference_service=FakeInferenceService(),
        repository=repository,
        event_publisher=event_publisher,
    )

    result = await service.upload_and_analyze(upload=object(), user_id="user-1")

    assert result.analysis_id == "analysis-1"
    assert result.user_id == "user-1"
    assert result.status == AnalysisStatus.COMPLETED
    assert result.model_version == "best.pt"
    assert len(result.detections) == 1
    assert [name for name, _ in event_publisher.calls] == ["analysis.uploaded", "analysis.completed"]


@pytest.mark.asyncio
async def test_analysis_service_upload_and_analyze_publishes_failed_event() -> None:
    settings = Settings()
    repository = FakeRepository()
    event_publisher = FakeEventPublisher()
    service = AnalysisService(
        settings=settings,
        upload_service=FakeUploadService(),
        inference_service=FakeInferenceServiceFail(),
        repository=repository,
        event_publisher=event_publisher,
    )

    with pytest.raises(InferenceError):
        await service.upload_and_analyze(upload=object(), user_id="user-1")

    assert repository.created is not None
    assert repository.created.status == AnalysisStatus.FAILED
    assert [name for name, _ in event_publisher.calls] == ["analysis.uploaded", "analysis.failed"]
