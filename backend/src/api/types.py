from __future__ import annotations

from datetime import datetime
from enum import Enum

import strawberry

from src.persistence.models import AnalysisRecord, AnalysisStatus as AnalysisStatusModel
from src.persistence.user_models import UserRecord, UserRole


@strawberry.enum
class AnalysisStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@strawberry.type(description="Deteccion individual resultante de la inferencia YOLO.")
class Detection:
    class_id: int
    class_name: str
    confidence: float
    bbox_xyxy: list[float]
    label: str


@strawberry.type(description="Analisis completo de una radiografia dental.")
class Analysis:
    analysis_id: str
    user_id: str | None
    file_name: str
    file_path: str
    mime_type: str
    file_size_bytes: int
    status: AnalysisStatus
    detections: list[Detection]
    inference_time_ms: float
    model_version: str
    error_message: str | None
    created_at: datetime
    updated_at: datetime


@strawberry.type(description="Resultado de la mutacion de subida y analisis de radiografia.")
class UploadResponse:
    success: bool
    message: str
    analysis: Analysis | None


@strawberry.type(description="Metricas globales del sistema de analisis.")
class SystemStats:
    total_analyses: int
    completed_analyses: int
    failed_analyses: int


@strawberry.enum
class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"


@strawberry.type(description="Usuario del sistema de autenticacion.")
class User:
    user_id: str
    email: str
    role: Role
    is_active: bool
    created_at: datetime


@strawberry.type(description="Respuesta de login con token JWT y datos del usuario.")
class AuthPayload:
    access_token: str
    token_type: str
    user: User


def _to_graphql_status(value: AnalysisStatusModel) -> AnalysisStatus:
    return AnalysisStatus(value.value)


def to_graphql_analysis(record: AnalysisRecord) -> Analysis:
    return Analysis(
        analysis_id=record.analysis_id,
        user_id=record.user_id,
        file_name=record.file_name,
        file_path=record.file_path,
        mime_type=record.mime_type,
        file_size_bytes=record.file_size_bytes,
        status=_to_graphql_status(record.status),
        detections=[
            Detection(
                class_id=item.class_id,
                class_name=item.class_name,
                confidence=item.confidence,
                bbox_xyxy=item.bbox_xyxy,
                label=item.label,
            )
            for item in record.detections
        ],
        inference_time_ms=record.inference_time_ms,
        model_version=record.model_version,
        error_message=record.error_message,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


def to_graphql_role(value: UserRole) -> Role:
    return Role(value.value)


def to_graphql_user(record: UserRecord) -> User:
    return User(
        user_id=record.user_id,
        email=record.email,
        role=to_graphql_role(record.role),
        is_active=record.is_active,
        created_at=record.created_at,
    )
