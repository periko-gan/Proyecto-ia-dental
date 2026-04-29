from __future__ import annotations

from datetime import datetime, timezone
import logging

from strawberry.file_uploads import Upload

from src.config.settings import Settings
from src.domain.exceptions import InferenceError
from src.events.publishers import EventPublisher, NullEventPublisher
from src.persistence.models import AnalysisRecord, AnalysisStatus
from src.persistence.repository import AnalysisRepository
from src.services.inference_service import InferenceService
from src.services.upload_service import UploadService


logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(
        self,
        settings: Settings,
        upload_service: UploadService,
        inference_service: InferenceService,
        repository: AnalysisRepository,
        event_publisher: EventPublisher | None = None,
    ) -> None:
        self._settings = settings
        self._upload_service = upload_service
        self._inference_service = inference_service
        self._repository = repository
        self._event_publisher = event_publisher or NullEventPublisher()

    async def _safe_publish(self, event_name: str, payload: dict[str, object]) -> None:
        try:
            await self._event_publisher.publish(event_name, payload)
        except Exception:
            logger.exception("No se pudo publicar evento %s", event_name)

    async def upload_and_analyze(self, upload: Upload, user_id: str) -> AnalysisRecord:
        stored_file = await self._upload_service.save_upload(upload)
        await self._safe_publish(
            "analysis.uploaded",
            {
                "analysis_id": stored_file.analysis_id,
                "user_id": user_id,
                "file_name": stored_file.file_name,
                "mime_type": stored_file.mime_type,
                "file_size_bytes": stored_file.file_size_bytes,
            },
        )

        try:
            detections, inference_time_ms = await self._inference_service.run_inference(stored_file.file_path)
            record = AnalysisRecord(
                analysis_id=stored_file.analysis_id,
                user_id=user_id,
                file_name=stored_file.file_name,
                file_path=str(stored_file.file_path),
                mime_type=stored_file.mime_type,
                file_size_bytes=stored_file.file_size_bytes,
                status=AnalysisStatus.COMPLETED,
                detections=detections,
                inference_time_ms=inference_time_ms,
                model_version=self._inference_service.model_version,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            persisted_record = await self._repository.create_analysis(record)
            await self._safe_publish(
                "analysis.completed",
                {
                    "analysis_id": persisted_record.analysis_id,
                    "user_id": persisted_record.user_id,
                    "status": persisted_record.status.value,
                    "detections_count": len(persisted_record.detections),
                    "inference_time_ms": persisted_record.inference_time_ms,
                    "model_version": persisted_record.model_version,
                },
            )
            return persisted_record
        except Exception as exc:
            record = AnalysisRecord(
                analysis_id=stored_file.analysis_id,
                user_id=user_id,
                file_name=stored_file.file_name,
                file_path=str(stored_file.file_path),
                mime_type=stored_file.mime_type,
                file_size_bytes=stored_file.file_size_bytes,
                status=AnalysisStatus.FAILED,
                detections=[],
                inference_time_ms=0.0,
                model_version=self._settings.model_version,
                error_message=str(exc),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            persisted_record = await self._repository.create_analysis(record)
            await self._safe_publish(
                "analysis.failed",
                {
                    "analysis_id": persisted_record.analysis_id,
                    "user_id": persisted_record.user_id,
                    "status": persisted_record.status.value,
                    "error_message": persisted_record.error_message,
                    "model_version": persisted_record.model_version,
                },
            )
            raise InferenceError(str(exc)) from exc

    async def get_analysis_by_id(self, analysis_id: str) -> AnalysisRecord | None:
        return await self._repository.get_by_analysis_id(analysis_id)

    async def get_analysis_by_id_for_user(self, analysis_id: str, user_id: str) -> AnalysisRecord | None:
        return await self._repository.get_by_analysis_id_for_user(analysis_id, user_id)

    async def list_analyses(self, limit: int, offset: int) -> list[AnalysisRecord]:
        return await self._repository.list_analyses(limit=limit, offset=offset)

    async def my_analyses(self, user_id: str, limit: int, offset: int) -> list[AnalysisRecord]:
        return await self._repository.list_analyses_by_user(user_id=user_id, limit=limit, offset=offset)

    async def get_system_stats(self) -> dict[str, int]:
        total = await self._repository.count_all()
        completed = await self._repository.count_by_status(AnalysisStatus.COMPLETED.value)
        failed = await self._repository.count_by_status(AnalysisStatus.FAILED.value)
        return {
            "total_analyses": total,
            "completed_analyses": completed,
            "failed_analyses": failed,
        }
