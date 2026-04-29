from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from strawberry.file_uploads import Upload

from src.config.settings import Settings
from src.domain.exceptions import ValidationError


@dataclass
class StoredUpload:
    analysis_id: str
    file_name: str
    mime_type: str
    file_size_bytes: int
    file_path: Path


class UploadService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def save_upload(self, upload: Upload) -> StoredUpload:
        file_name = upload.filename or "radiography"
        mime_type = upload.content_type or "application/octet-stream"

        if mime_type not in self._settings.allowed_mime_types:
            raise ValidationError(f"Tipo de archivo no permitido: {mime_type}")

        content = await upload.read()
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

        return StoredUpload(
            analysis_id=analysis_id,
            file_name=file_name,
            mime_type=mime_type,
            file_size_bytes=file_size_bytes,
            file_path=file_path,
        )
