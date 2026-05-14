"""Servicio de análisis de radiografías con soporte a eventos."""

from __future__ import annotations

from datetime import datetime, timezone
import logging
import tempfile
from contextlib import suppress
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from src.config.settings import Settings
from src.domain.exceptions import InferenceError
from src.events.analysis_events import create_analysis_requested_event
from src.events.publishers import EventPublisher
from src.persistence.models import AnalysisRecord, AnalysisStatus
from src.persistence.repository import AnalysisRepository
from src.services.event_emitter import EventEmitter
from src.services.inference_service import InferenceService
from src.services.result_service import ResultService
from src.services.upload_service import UploadService

logger = logging.getLogger(__name__)


def _prepare_image_for_inference(image_path: Path) -> Path:
    """Convierte la imagen a un PNG temporal estandarizado para inferencia."""
    try:
        with Image.open(image_path) as image:
            normalized = image.convert("RGB")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            temp_path = Path(temp_file.name)
            temp_file.close()
            normalized.save(temp_path, format="PNG")
            return temp_path
    except (UnidentifiedImageError, OSError):
        return image_path


class AnalysisService(EventEmitter):
    def __init__(
        self,
        settings: Settings,
        upload_service: UploadService,
        inference_service: InferenceService,
        result_service: ResultService,
        repository: AnalysisRepository,
        event_publisher: EventPublisher | None = None,
    ) -> None:
        super().__init__(event_publisher=event_publisher, logger_name=__name__)
        self._settings = settings
        self._upload_service = upload_service
        self._inference_service = inference_service
        self._result_service = result_service
        self._repository = repository

    async def upload_and_analyze(self, file_base64: str, file_name: str, mime_type: str, user_id: str) -> AnalysisRecord:
        stored_file = await self._upload_service.save_upload(file_base64, file_name, mime_type, user_id)

        # Publicar evento de análisis solicitado
        await self._safe_publish_event(
            create_analysis_requested_event(
                analysis_id=stored_file.analysis_id,
                user_id=user_id,
                file_name=stored_file.file_name,
                file_path=str(stored_file.file_path),
                correlation_id=stored_file.analysis_id,
            )
        )
        await self.publish_system_log(
            message="Analisis solicitado",
            context={"analysis_id": stored_file.analysis_id, "user_id": user_id},
            source="AnalysisService",
        )

        try:
            inference_path = _prepare_image_for_inference(stored_file.file_path)
            try:
                detections, inference_time_ms = await self._inference_service.process_requested_analysis(
                    analysis_id=stored_file.analysis_id,
                    user_id=user_id,
                    image_path=inference_path,
                    correlation_id=stored_file.analysis_id,
                )
            finally:
                if inference_path != stored_file.file_path:
                    with suppress(FileNotFoundError):
                        inference_path.unlink()

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

            await self._result_service.publish_result_saved(persisted_record)

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
            await self._repository.create_analysis(record)
            await self.publish_system_error(
                error_message="Fallo el analisis",
                error_type=type(exc).__name__,
                context={"analysis_id": stored_file.analysis_id, "user_id": user_id},
                source="AnalysisService",
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
