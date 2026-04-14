from __future__ import annotations

from io import BytesIO
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import frontend.inference as inference_module
from PIL import Image

from frontend.inference import draw_detections, run_inference


class _FakeTensor:
    def __init__(self, values):
        self._values = values

    def tolist(self):
        return self._values


class _FakeBoxes:
    def __init__(self):
        self.xyxy = _FakeTensor([[10, 20, 100, 120]])
        self.conf = _FakeTensor([0.91])
        self.cls = _FakeTensor([0])


class _FakeResult:
    names = {0: "caries"}

    def __init__(self):
        self.boxes = _FakeBoxes()


class _FakeModel:
    def __init__(self):
        self.seen_devices = []

    def predict(self, **kwargs):
        self.seen_devices.append(kwargs.get("device"))
        assert "source" in kwargs
        return [_FakeResult()]


def test_run_inference_smoke():
    model = _FakeModel()
    img = Image.new("RGB", (64, 64), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")

    annotated, detections = run_inference(model, buf.getvalue(), device="cpu")

    assert annotated.size == (64, 64)
    assert len(detections) == 1
    assert detections[0]["class_name"] == "caries"
    assert model.seen_devices[-1] == "cpu"
    assert detections[0]["confidence"] == 91
    assert detections[0]["label"] == "caries 91"


def test_run_inference_uses_resolved_device(monkeypatch):
    model = _FakeModel()
    img = Image.new("RGB", (64, 64), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")

    monkeypatch.setattr(
        inference_module,
        "resolve_device",
        lambda device: type("_Resolved", (), {"resolved": "cpu"})(),
    )

    run_inference(model, buf.getvalue(), device="auto")

    assert model.seen_devices[-1] == "cpu"


def test_run_inference_uses_small_label_font(monkeypatch):
    model = _FakeModel()
    img = Image.new("RGB", (64, 64), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")

    seen = []

    original_put_text = inference_module.cv2.putText

    def capture_put_text(*args, **kwargs):
        seen.append({"text": args[1], "font_scale": args[4]})
        return original_put_text(*args, **kwargs)

    monkeypatch.setattr(inference_module.cv2, "putText", capture_put_text)

    run_inference(model, buf.getvalue(), device="cpu")

    assert seen
    assert seen[0]["text"] == "caries 91"
    assert seen[0]["font_scale"] <= 0.4


def test_draw_detections_can_render_only_selected_indices(monkeypatch):
    img = Image.new("RGB", (64, 64), color=(255, 255, 255))
    detections = [
        {"bbox_xyxy": [5, 5, 20, 20], "label": "caries 11"},
        {"bbox_xyxy": [25, 25, 40, 40], "label": "molar 88"},
    ]

    seen_labels = []
    original_put_text = inference_module.cv2.putText

    def capture_put_text(*args, **kwargs):
        seen_labels.append(args[1])
        return original_put_text(*args, **kwargs)

    monkeypatch.setattr(inference_module.cv2, "putText", capture_put_text)

    annotated = draw_detections(img, detections, selected_indices=[1])

    assert annotated.size == (64, 64)
    assert seen_labels == ["molar 88"]


