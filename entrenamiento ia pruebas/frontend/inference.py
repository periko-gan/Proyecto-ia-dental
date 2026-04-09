#!/usr/bin/env python3
"""Utilidades de inferencia YOLO para el frontend de radiografias dentales."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Tuple

import cv2
import numpy as np
from PIL import Image

from tools.device_resolver import resolve_device


def project_root() -> Path:
    """Devuelve la raiz del proyecto (`entrenamiento ia`)."""
    return Path(__file__).resolve().parents[1]


def default_model_path() -> Path:
    """Modelo por defecto solicitado por el usuario."""
    return project_root() / "best.pt"


def load_yolo_model(model_path: str):
    """Carga YOLO con import diferido para fallar rapido si falta la dependencia."""
    from ultralytics import YOLO

    model_file = Path(model_path).expanduser().resolve()
    if not model_file.exists():
        raise FileNotFoundError(f"No se encontro el modelo: {model_file}")
    return YOLO(str(model_file))


def _draw_detections(canvas: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
    """Dibuja cajas y etiquetas con fuente pequena sobre una imagen RGB."""
    output = canvas.copy()
    box_color = (0, 255, 0)
    text_color = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.4
    thickness = 1

    for detection in detections:
        x1, y1, x2, y2 = [int(round(value)) for value in detection["bbox_xyxy"]]
        label = detection["label"]

        cv2.rectangle(output, (x1, y1), (x2, y2), box_color, 2)

        (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
        label_x = max(x1, 0)
        label_y = max(y1 - 6, text_height + baseline + 4)
        top_left = (label_x, max(label_y - text_height - baseline - 4, 0))
        bottom_right = (label_x + text_width + 6, label_y)

        cv2.rectangle(output, top_left, bottom_right, box_color, -1)
        cv2.putText(
            output,
            label,
            (label_x + 3, label_y - baseline - 2),
            font,
            font_scale,
            text_color,
            thickness,
            lineType=cv2.LINE_AA,
        )

    return output


def draw_detections(
    image: Image.Image | np.ndarray | bytes,
    detections: List[Dict[str, Any]],
    selected_indices: List[int] | None = None,
) -> Image.Image:
    """Dibuja todas las detecciones o solo un subconjunto seleccionado por indice."""
    if isinstance(image, bytes):
        canvas = np.array(Image.open(BytesIO(image)).convert("RGB"))
    elif isinstance(image, Image.Image):
        canvas = np.array(image.convert("RGB"))
    else:
        canvas = np.array(image)

    if selected_indices is None:
        selected_detections = detections
    else:
        selected_detections = [
            detections[index]
            for index in selected_indices
            if 0 <= index < len(detections)
        ]

    plotted = _draw_detections(canvas, selected_detections)
    return Image.fromarray(plotted)


def run_inference(
    model: Any,
    image_bytes: bytes,
    conf: float = 0.25,
    iou: float = 0.7,
    imgsz: int = 640,
    device: str = "auto",
) -> Tuple[Image.Image, List[Dict[str, Any]]]:
    """Ejecuta inferencia sobre una imagen y devuelve imagen anotada + detecciones."""
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    device_resolution = resolve_device(device)

    # YOLO acepta arrays numpy HWC en RGB para prediccion directa.
    results = model.predict(
        source=np.array(image),
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        device=device_resolution.resolved,
        verbose=False,
    )

    if not results:
        return image, []

    result = results[0]
    names = result.names if isinstance(result.names, dict) else {}
    detections: List[Dict[str, Any]] = []

    boxes = getattr(result, "boxes", None)
    if boxes is not None:
        xyxy = boxes.xyxy.tolist()
        confs = boxes.conf.tolist()
        classes = boxes.cls.tolist()

        for box, score, cls_id in zip(xyxy, confs, classes):
            x1, y1, x2, y2 = [float(v) for v in box]
            class_index = int(cls_id)
            score_pct = int(round(float(score) * 100))
            detections.append(
                {
                    "class_id": class_index,
                    "class_name": str(names.get(class_index, class_index)),
                    "confidence": score_pct,
                    "bbox_xyxy": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)],
                    "label": f"{str(names.get(class_index, class_index))} {score_pct}",
                }
            )

    annotated = draw_detections(image, detections)
    return annotated, detections

