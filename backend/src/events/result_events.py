"""Eventos de resultado y persistencia."""

from src.events.models import Event, create_event


def create_result_saved_event(
    analysis_id: str,
    user_id: str,
    detections_count: int,
    model_version: str,
    correlation_id: str | None = None,
) -> Event:
    """Crea evento de resultado guardado en persistencia."""
    return create_event(
        event_name="result.saved",
        payload={
            "analysis_id": analysis_id,
            "user_id": user_id,
            "detections_count": detections_count,
            "model_version": model_version,
        },
        source="ResultService",
        correlation_id=correlation_id or analysis_id,
    )
