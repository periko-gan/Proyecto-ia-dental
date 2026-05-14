"""Tests unitarios para módulos de eventos."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

import pytest

from src.events.analysis_events import (
    create_analysis_completed_event,
    create_analysis_requested_event,
)
from src.events.auth_events import create_user_register_event
from src.events.event_router import get_topic_for_event
from src.events.image_events import create_image_uploaded_event
from src.events.models import Event, create_event
from src.events.system_events import create_system_error_event
from src.events.topics import KafkaTopics


def test_create_event_generates_event_id() -> None:
    """Test que create_event genera event_id único."""
    event = create_event(
        event_name="test.event",
        payload={"key": "value"},
        source="TestSource",
    )

    assert isinstance(event.event_id, UUID)
    assert event.event_name == "test.event"
    assert event.source == "TestSource"
    assert event.version == 1


def test_event_timestamp_is_set() -> None:
    """Test que el timestamp se genera automáticamente."""
    before = datetime.now(timezone.utc)
    event = create_event(
        event_name="test.event",
        payload={},
        source="TestSource",
    )
    after = datetime.now(timezone.utc)

    assert before <= event.timestamp <= after


def test_create_image_uploaded_event() -> None:
    """Test creación de evento de imagen subida."""
    event = create_image_uploaded_event(
        analysis_id="analysis-1",
        user_id="user-1",
        file_name="test.jpg",
        mime_type="image/jpeg",
        file_size_bytes=1024,
        file_path="/uploads/test.jpg",
    )

    assert event.event_name == "image.uploaded"
    assert event.source == "UploadService"
    assert event.payload["analysis_id"] == "analysis-1"
    assert event.correlation_id == "analysis-1"


def test_create_analysis_requested_event() -> None:
    """Test creación de evento de análisis solicitado."""
    event = create_analysis_requested_event(
        analysis_id="analysis-1",
        user_id="user-1",
        file_name="test.jpg",
        file_path="/tmp/test.jpg",
    )

    assert event.event_name == "analysis.requested"
    assert event.source == "AnalysisService"
    assert event.payload["analysis_id"] == "analysis-1"
    assert event.payload["file_path"] == "/tmp/test.jpg"


def test_create_analysis_completed_event() -> None:
    """Test creación de evento de análisis completado."""
    event = create_analysis_completed_event(
        analysis_id="analysis-1",
        user_id="user-1",
        status="COMPLETED",
        detections_count=3,
        inference_time_ms=25.5,
        model_version="best.pt",
    )

    assert event.event_name == "analysis.completed"
    assert event.source == "InferenceService"
    assert event.payload["status"] == "COMPLETED"
    assert event.payload["detections_count"] == 3


def test_create_user_register_event() -> None:
    """Test creación de evento de registro de usuario."""
    event = create_user_register_event(user_id="user-1", email="test@example.com", name="Maria Perez")

    assert event.event_name == "auth.register"
    assert event.source == "AuthService"
    assert event.payload["email"] == "test@example.com"
    assert event.payload["name"] == "Maria Perez"
    assert event.correlation_id == "user-1"


def test_create_system_error_event() -> None:
    """Test creación de evento de error del sistema."""
    event = create_system_error_event(
        error_message="Test error",
        error_type="ValueError",
        traceback_str="Traceback...",
    )

    assert event.event_name == "system.error"
    assert event.payload["error_message"] == "Test error"
    assert event.payload["error_type"] == "ValueError"


def test_event_to_dict_serialization() -> None:
    """Test que Event se serializa correctamente a dict."""
    event = create_event(
        event_name="test.event",
        payload={"key": "value"},
        source="TestSource",
    )

    data = event.to_dict()

    assert isinstance(data["event_id"], str)  # UUID convertido a string
    assert isinstance(data["timestamp"], str)  # datetime convertido a ISO string
    assert data["event_name"] == "test.event"
    assert data["payload"] == {"key": "value"}


def test_event_router_maps_image_uploaded() -> None:
    """Test que event router mapea image.uploaded correctamente."""
    event = create_image_uploaded_event(
        analysis_id="a1",
        user_id="u1",
        file_name="test.jpg",
        mime_type="image/jpeg",
        file_size_bytes=1024,
        file_path="/tmp/test.jpg",
    )

    topic = get_topic_for_event(event)
    assert topic == KafkaTopics.IMAGE_UPLOADED


def test_event_router_maps_analysis_completed() -> None:
    """Test que event router mapea analysis.completed correctamente."""
    event = create_analysis_completed_event(
        analysis_id="a1",
        user_id="u1",
        status="COMPLETED",
        detections_count=5,
        inference_time_ms=20.0,
        model_version="v1",
    )

    topic = get_topic_for_event(event)
    assert topic == KafkaTopics.ANALYSIS_COMPLETED


def test_event_router_maps_auth_events() -> None:
    """Test que event router mapea auth events al topic correcto."""
    event = create_user_register_event(user_id="u1", email="test@example.com", name="User Test")

    topic = get_topic_for_event(event)
    assert topic == KafkaTopics.AUTH_EVENTS


def test_event_router_unmapped_event_goes_to_dead_letter() -> None:
    """Test que evento sin mapeo va a dead letter."""
    event = create_event(
        event_name="unmapped.event",
        payload={},
        source="TestSource",
    )

    topic = get_topic_for_event(event)
    assert topic == KafkaTopics.DEAD_LETTER
