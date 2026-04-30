from __future__ import annotations

import time
from pathlib import Path

from src.config.settings import Settings
from src.inference.model_adapter import normalize_detections
from src.inference.model_loader import ModelLoader
from src.persistence.models import DetectionRecord


class InferenceService:
    def __init__(self, settings: Settings, model_loader: ModelLoader) -> None:
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
