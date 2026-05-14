from __future__ import annotations

import base64
import logging
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from src.config.settings import Settings
from src.domain.exceptions import ValidationError
from src.events.image_events import create_image_uploaded_event
from src.events.publishers import EventPublisher
from src.services.event_emitter import EventEmitter

logger = logging.getLogger(__name__)


@dataclass
class StoredUpload:
    analysis_id: str
    file_name: str
    mime_type: str
    file_size_bytes: int
    file_path: Path


class UploadService(EventEmitter):
    def __init__(self, settings: Settings, event_publisher: EventPublisher | None = None) -> None:
        super().__init__(event_publisher=event_publisher, logger_name=__name__)
        self._settings = settings

    async def save_upload(self, file_base64: str, file_name: str, mime_type: str, user_id: str) -> StoredUpload:
        if mime_type not in self._settings.allowed_mime_types:
            raise ValidationError(f"Tipo de archivo no permitido: {mime_type}")

        try:
            content = base64.b64decode(file_base64)
        except Exception as exc:
            raise ValidationError("El archivo base64 no es valido") from exc
        file_size_bytes = len(content)

        if file_size_bytes == 0:
            raise ValidationError("El archivo esta vacio")

        if file_size_bytes > self._settings.max_file_size_bytes:
            raise ValidationError("El archivo excede el tamano maximo permitido")

        analysis_id = str(uuid4())
        safe_name = file_name.replace(" ", "_")
        file_path = self._settings.uploads_path / f"{analysis_id}_{safe_name}"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)

        stored = StoredUpload(
            analysis_id=analysis_id,
            file_name=file_name,
            mime_type=mime_type,
            file_size_bytes=file_size_bytes,
            file_path=file_path,
        )

        # Publicar evento de imagen subida
        await self._safe_publish_event(
            create_image_uploaded_event(
                analysis_id=analysis_id,
                user_id=user_id,
                file_name=file_name,
                mime_type=mime_type,
                file_size_bytes=file_size_bytes,
                file_path=str(file_path),
                correlation_id=analysis_id,
            )
        )
        await self.publish_system_log(
            message="Imagen subida correctamente",
            context={"analysis_id": analysis_id, "user_id": user_id, "file_name": file_name},
            source="UploadService",
        )

        return stored
