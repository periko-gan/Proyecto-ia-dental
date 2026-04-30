from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any

from src.config.settings import Settings
from src.domain.exceptions import InferenceError, ModelLoadError
from src.inference.device_resolver import resolve_device

logger = logging.getLogger(__name__)


class ModelLoader:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model: Any | None = None
        self._device = resolve_device()
        self._lock = asyncio.Lock()

    @property
    def model_version(self) -> str:
        return self._settings.model_version

    async def load_model(self) -> Any:
        if self._model is not None:
            return self._model

        async with self._lock:
            if self._model is not None:
                return self._model

            model_path = self._settings.model_path_resolved
            if not model_path.exists():
                raise ModelLoadError(f"No se encontro el modelo en: {model_path}")

            try:
                from ultralytics import YOLO

                logger.info("Cargando modelo YOLO desde %s", model_path)
                self._model = await asyncio.to_thread(YOLO, str(model_path))
                logger.info("Modelo YOLO cargado en dispositivo %s", self._device)
                return self._model
            except Exception as exc:
                raise ModelLoadError("No se pudo cargar el modelo YOLO") from exc

    async def predict(self, image_path: Path, confidence: float, iou: float) -> list[Any]:
        model = await self.load_model()
        try:
            return await asyncio.to_thread(
                model.predict,
                str(image_path),
                conf=confidence,
                iou=iou,
                device=self._device,
                verbose=False,
            )
        except Exception as exc:
            raise InferenceError("Fallo la inferencia del modelo") from exc
