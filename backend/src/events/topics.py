"""Definición centralizada de topics de Kafka para la aplicación de IA Dental."""

from enum import Enum


class KafkaTopics(str, Enum):
    """Topics de Kafka disponibles en la arquitectura de eventos."""

    # Image events
    IMAGE_UPLOADED = "dental.image.uploaded"

    # Analysis events
    ANALYSIS_REQUESTED = "dental.analysis.requested"
    ANALYSIS_STARTED = "dental.analysis.started"
    ANALYSIS_COMPLETED = "dental.analysis.completed"
    ANALYSIS_FAILED = "dental.analysis.failed"

    # Result events
    RESULT_SAVED = "dental.result.saved"

    # Metrics
    METRICS_INFERENCE = "dental.metrics.inference"

    # Auth events
    AUTH_EVENTS = "dental.auth.events"

    # System events
    SYSTEM_LOGS = "dental.system.logs"
    SYSTEM_ERRORS = "dental.system.errors"

    # Dead letter
    DEAD_LETTER = "dental.dead-letter"


# Mapa de event_name → topic Kafka para routing
EVENT_NAME_TO_TOPIC = {
    "image.uploaded": KafkaTopics.IMAGE_UPLOADED,
    "analysis.requested": KafkaTopics.ANALYSIS_REQUESTED,
    "analysis.started": KafkaTopics.ANALYSIS_STARTED,
    "analysis.completed": KafkaTopics.ANALYSIS_COMPLETED,
    "analysis.failed": KafkaTopics.ANALYSIS_FAILED,
    "result.saved": KafkaTopics.RESULT_SAVED,
    "metrics.inference": KafkaTopics.METRICS_INFERENCE,
    "auth.login_success": KafkaTopics.AUTH_EVENTS,
    "auth.login_failed": KafkaTopics.AUTH_EVENTS,
    "auth.register": KafkaTopics.AUTH_EVENTS,
    "auth.logout": KafkaTopics.AUTH_EVENTS,
    "auth.token_refresh": KafkaTopics.AUTH_EVENTS,
    "system.log": KafkaTopics.SYSTEM_LOGS,
    "system.error": KafkaTopics.SYSTEM_ERRORS,
}

# Metadatos de topics (para scripts de inicialización futuros)
TOPIC_METADATA = {
    KafkaTopics.IMAGE_UPLOADED: {"partitions": 1, "replication_factor": 1, "retention_ms": 7 * 24 * 60 * 60 * 1000},
    KafkaTopics.ANALYSIS_REQUESTED: {"partitions": 1, "replication_factor": 1, "retention_ms": 7 * 24 * 60 * 60 * 1000},
    KafkaTopics.ANALYSIS_STARTED: {"partitions": 1, "replication_factor": 1, "retention_ms": 7 * 24 * 60 * 60 * 1000},
    KafkaTopics.ANALYSIS_COMPLETED: {"partitions": 1, "replication_factor": 1, "retention_ms": 7 * 24 * 60 * 60 * 1000},
    KafkaTopics.ANALYSIS_FAILED: {"partitions": 1, "replication_factor": 1, "retention_ms": 7 * 24 * 60 * 60 * 1000},
    KafkaTopics.RESULT_SAVED: {"partitions": 1, "replication_factor": 1, "retention_ms": 7 * 24 * 60 * 60 * 1000},
    KafkaTopics.METRICS_INFERENCE: {"partitions": 1, "replication_factor": 1, "retention_ms": 24 * 60 * 60 * 1000},
    KafkaTopics.AUTH_EVENTS: {"partitions": 1, "replication_factor": 1, "retention_ms": 30 * 24 * 60 * 60 * 1000},
    KafkaTopics.SYSTEM_LOGS: {"partitions": 1, "replication_factor": 1, "retention_ms": 7 * 24 * 60 * 60 * 1000},
    KafkaTopics.SYSTEM_ERRORS: {"partitions": 1, "replication_factor": 1, "retention_ms": 30 * 24 * 60 * 60 * 1000},
    KafkaTopics.DEAD_LETTER: {"partitions": 1, "replication_factor": 1, "retention_ms": 90 * 24 * 60 * 60 * 1000},
}


def get_topic_for_event(event_name: str) -> str:
    """Retorna el topic Kafka para un nombre de evento dado."""
    topic = EVENT_NAME_TO_TOPIC.get(event_name)
    if topic is None:
        # Fallback a DEAD_LETTER si el evento no tiene mapeo definido
        return KafkaTopics.DEAD_LETTER
    return topic
