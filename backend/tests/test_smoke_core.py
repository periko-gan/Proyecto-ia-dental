import pytest
from src.persistence.models import AnalysisRecord, AnalysisStatus, DetectionRecord
from src.config.settings import get_settings


def test_settings_loads():
    """Valida que la configuracion se carga."""
    settings = get_settings()
    assert settings is not None
    assert settings.env == "development"
    assert settings.port == 8000


def test_analysis_record_creation():
    """Valida que se puede crear un documento de analisis."""
    record = AnalysisRecord(
        analysis_id="test-123",
        user_id="user-1",
        file_name="test.jpg",
        file_path="/tmp/test.jpg",
        mime_type="image/jpeg",
        file_size_bytes=1024,
        status=AnalysisStatus.COMPLETED,
        model_version="best.pt",
    )
    assert record.analysis_id == "test-123"
    assert record.user_id == "user-1"
    assert record.status == AnalysisStatus.COMPLETED


def test_detection_record_creation():
    """Valida que se puede crear un registro de deteccion."""
    detection = DetectionRecord(
        class_id=0,
        class_name="caries",
        confidence=0.95,
        bbox_xyxy=[10.0, 20.0, 100.0, 200.0],
        label="caries 95",
    )
    assert detection.class_name == "caries"
    assert detection.confidence == 0.95


def test_analysis_record_to_mongo():
    """Valida que un registro se convierte correctamente para MongoDB."""
    record = AnalysisRecord(
        analysis_id="test-123",
        user_id="user-1",
        file_name="test.jpg",
        file_path="/tmp/test.jpg",
        mime_type="image/jpeg",
        file_size_bytes=1024,
        status=AnalysisStatus.COMPLETED,
        model_version="best.pt",
    )
    mongo_doc = record.to_mongo()
    assert mongo_doc["analysis_id"] == "test-123"
    assert mongo_doc["user_id"] == "user-1"
    assert mongo_doc["status"] == "COMPLETED"
    assert "_id" not in mongo_doc or mongo_doc.get("_id") is None
