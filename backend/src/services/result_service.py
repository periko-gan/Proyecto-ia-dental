from __future__ import annotations

from src.events.result_events import create_result_saved_event
from src.events.publishers import EventPublisher
from src.persistence.models import AnalysisRecord
from src.services.event_emitter import EventEmitter


class ResultService(EventEmitter):
    """Publica eventos relacionados a resultados persistidos."""

    def __init__(self, event_publisher: EventPublisher | None = None) -> None:
        super().__init__(event_publisher=event_publisher, logger_name=__name__)

    async def publish_result_saved(self, analysis: AnalysisRecord) -> None:
        await self._safe_publish_event(
            create_result_saved_event(
                analysis_id=analysis.analysis_id,
                user_id=analysis.user_id,
                detections_count=len(analysis.detections),
                model_version=analysis.model_version,
                correlation_id=analysis.analysis_id,
            )
        )
        await self.publish_system_log(
            message="Resultado de analisis persistido",
            context={"analysis_id": analysis.analysis_id, "user_id": analysis.user_id},
            source="ResultService",
        )