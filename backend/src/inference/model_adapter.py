from __future__ import annotations

from typing import Any

from src.persistence.models import DetectionRecord


def _resolve_class_name(names: Any, class_id: int) -> str:
    if isinstance(names, dict):
        return str(names.get(class_id, class_id))
    if isinstance(names, list) and 0 <= class_id < len(names):
        return str(names[class_id])
    return str(class_id)


def normalize_detections(results: list[Any]) -> list[DetectionRecord]:
    if not results:
        return []

    first_result = results[0]
    boxes = getattr(first_result, "boxes", None)
    names = getattr(first_result, "names", {})
    if boxes is None:
        return []

    detections: list[DetectionRecord] = []
    for box in boxes:
        class_id = int(box.cls[0].item())
        confidence = float(box.conf[0].item())
        bbox_xyxy = [float(value) for value in box.xyxy[0].tolist()]
        class_name = _resolve_class_name(names, class_id)
        label = f"{class_name} {round(confidence * 100)}"

        detections.append(
            DetectionRecord(
                class_id=class_id,
                class_name=class_name,
                confidence=confidence,
                bbox_xyxy=bbox_xyxy,
                label=label,
            )
        )

    return detections
