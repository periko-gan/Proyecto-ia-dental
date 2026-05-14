"""Eventos de carga de imágenes."""

from src.events.models import Event, create_event


def create_image_uploaded_event(
    analysis_id: str,
    user_id: str,
    file_name: str,
    mime_type: str,
    file_size_bytes: int,
    file_path: str,
    correlation_id: str | None = None,
) -> Event:
    """Crea evento de imagen subida."""
    return create_event(
        event_name="image.uploaded",
        payload={
            "analysis_id": analysis_id,
            "user_id": user_id,
            "file_name": file_name,
            "mime_type": mime_type,
            "file_size_bytes": file_size_bytes,
            "file_path": file_path,
        },
        source="UploadService",
        correlation_id=correlation_id or analysis_id,
    )
