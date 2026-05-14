"""Eventos de análisis y métricas de inferencia."""

from src.events.models import Event, create_event


def create_analysis_requested_event(
    analysis_id: str,
    user_id: str,
    file_name: str,
    file_path: str,
    correlation_id: str | None = None,
) -> Event:
    """Crea evento de análisis solicitado."""
    return create_event(
        event_name="analysis.requested",
        payload={
            "analysis_id": analysis_id,
            "user_id": user_id,
            "file_name": file_name,
            "file_path": file_path,
        },
        source="AnalysisService",
        correlation_id=correlation_id or analysis_id,
    )


def create_analysis_started_event(
    analysis_id: str,
    user_id: str,
    correlation_id: str | None = None,
) -> Event:
    """Crea evento de análisis iniciado."""
    return create_event(
        event_name="analysis.started",
        payload={
            "analysis_id": analysis_id,
            "user_id": user_id,
        },
        source="InferenceService",
        correlation_id=correlation_id or analysis_id,
    )


def create_analysis_completed_event(
    analysis_id: str,
    user_id: str,
    status: str,
    detections_count: int,
    inference_time_ms: float,
    model_version: str,
    correlation_id: str | None = None,
) -> Event:
    """Crea evento de análisis completado."""
    return create_event(
        event_name="analysis.completed",
        payload={
            "analysis_id": analysis_id,
            "user_id": user_id,
            "status": status,
            "detections_count": detections_count,
            "inference_time_ms": inference_time_ms,
            "model_version": model_version,
        },
        source="InferenceService",
        correlation_id=correlation_id or analysis_id,
    )


def create_analysis_failed_event(
    analysis_id: str,
    user_id: str,
    status: str,
    error_message: str,
    model_version: str,
    correlation_id: str | None = None,
) -> Event:
    """Crea evento de análisis fallido."""
    return create_event(
        event_name="analysis.failed",
        payload={
            "analysis_id": analysis_id,
            "user_id": user_id,
            "status": status,
            "error_message": error_message,
            "model_version": model_version,
        },
        source="InferenceService",
        correlation_id=correlation_id or analysis_id,
    )


def create_metrics_inference_event(
    analysis_id: str,
    user_id: str,
    inference_time_ms: float,
    detections_count: int,
    model_version: str,
    confidence: float,
    iou: float,
    correlation_id: str | None = None,
) -> Event:
    """Crea evento de métricas de inferencia."""
    return create_event(
        event_name="metrics.inference",
        payload={
            "analysis_id": analysis_id,
            "user_id": user_id,
            "inference_time_ms": inference_time_ms,
            "detections_count": detections_count,
            "model_version": model_version,
            "confidence": confidence,
            "iou": iou,
        },
        source="InferenceService",
        correlation_id=correlation_id or analysis_id,
    )
