from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from src.config.settings import Settings
from src.events.analysis_events import (
    create_analysis_completed_event,
    create_analysis_failed_event,
    create_analysis_started_event,
    create_metrics_inference_event,
)
from src.inference.model_adapter import normalize_detections
from src.inference.model_loader import ModelLoader
from src.persistence.models import DetectionRecord
from src.services.event_emitter import EventEmitter

import logging
from src.events.publishers import EventPublisher

logger = logging.getLogger(__name__)


class InferenceService(EventEmitter):
    def __init__(self, settings: Settings, model_loader: ModelLoader, event_publisher: EventPublisher | None = None) -> None:
        super().__init__(event_publisher=event_publisher, logger_name=__name__)
        self._settings = settings
        self._model_loader = model_loader

    @property
    def model_version(self) -> str:
        return self._model_loader.model_version

    async def run_inference(self, image_path: Path) -> tuple[list[DetectionRecord], float]:
        started_at = time.perf_counter()
        results = await self._model_loader.predict(
            image_path=image_path,
            confidence=self._settings.model_confidence,
            iou=self._settings.model_iou,
        )
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        detections = normalize_detections(results)
        return detections, elapsed_ms

    async def process_requested_analysis(
        self,
        analysis_id: str,
        user_id: str,
        image_path: Path,
        correlation_id: str | None = None,
    ) -> tuple[list[DetectionRecord], float]:
        await self._safe_publish_event(
            create_analysis_started_event(
                analysis_id=analysis_id,
                user_id=user_id,
                correlation_id=correlation_id or analysis_id,
            )
        )

        try:
            detections, inference_time_ms = await self.run_inference(image_path)
        except Exception as exc:
            await self._safe_publish_event(
                create_analysis_failed_event(
                    analysis_id=analysis_id,
                    user_id=user_id,
                    status="FAILED",
                    error_message=str(exc),
                    model_version=self.model_version,
                    correlation_id=correlation_id or analysis_id,
                )
            )
            await self.publish_system_error(
                error_message="Error durante inferencia YOLO",
                error_type=type(exc).__name__,
                context={"analysis_id": analysis_id, "user_id": user_id},
                source="InferenceService",
            )
            raise

        await self._safe_publish_event(
            create_analysis_completed_event(
                analysis_id=analysis_id,
                user_id=user_id,
                status="COMPLETED",
                detections_count=len(detections),
                inference_time_ms=inference_time_ms,
                model_version=self.model_version,
                correlation_id=correlation_id or analysis_id,
            )
        )
        await self._safe_publish_event(
            create_metrics_inference_event(
                analysis_id=analysis_id,
                user_id=user_id,
                inference_time_ms=inference_time_ms,
                detections_count=len(detections),
                model_version=self.model_version,
                confidence=self._settings.model_confidence,
                iou=self._settings.model_iou,
                correlation_id=correlation_id or analysis_id,
            )
        )
        await self.publish_system_log(
            message="Inferencia completada",
            context={
                "analysis_id": analysis_id,
                "user_id": user_id,
                "detections_count": len(detections),
                "inference_time_ms": inference_time_ms,
            },
            source="InferenceService",
        )
        return detections, inference_time_ms

    async def consume_analysis_requested_payload(self, payload: dict[str, Any]) -> None:
        analysis_id = str(payload.get("analysis_id", "")).strip()
        user_id = str(payload.get("user_id", "")).strip()
        file_path_raw = str(payload.get("file_path", "")).strip()

        if not analysis_id or not user_id or not file_path_raw:
            await self.publish_system_error(
                error_message="Payload invalido para analysis.requested",
                error_type="ValidationError",
                context={"payload": payload},
                source="InferenceService",
            )
            return

        await self.process_requested_analysis(
            analysis_id=analysis_id,
            user_id=user_id,
            image_path=Path(file_path_raw),
            correlation_id=analysis_id,
        )
