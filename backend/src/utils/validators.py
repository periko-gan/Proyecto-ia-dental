from __future__ import annotations

from pathlib import Path

from src.domain.exceptions import ValidationError


def validate_image_extension(file_name: str) -> None:
    extension = Path(file_name).suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png"}:
        raise ValidationError("Extension de imagen no soportada")
