from __future__ import annotations

from datetime import datetime, timezone

from strawberry.file_uploads import Upload

from src.config.settings import Settings
from src.domain.exceptions import InferenceError
from src.persistence.models import AnalysisRecord, AnalysisStatus
from src.persistence.repository import AnalysisRepository
from src.services.inference_service import InferenceService
from src.services.upload_service import UploadService


class AnalysisService:
    def __init__(
        self,
        settings: Settings,
        upload_service: UploadService,
        inference_service: InferenceService,
        repository: AnalysisRepository,
    ) -> None:
        self._settings = settings
        self._upload_service = upload_service
        self._inference_service = inference_service
        self._repository = repository

    async def upload_and_analyze(self, upload: Upload, user_id: str) -> AnalysisRecord:
        stored_file = await self._upload_service.save_upload(upload)

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
            raise InferenceError(str(exc)) from exc

        return await self._repository.create_analysis(record)

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
