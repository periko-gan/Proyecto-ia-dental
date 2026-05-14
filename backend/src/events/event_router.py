"""Routing de eventos a topics de Kafka."""

from src.events.models import Event
from src.events.topics import EVENT_NAME_TO_TOPIC, KafkaTopics


def get_topic_for_event(event: Event) -> str:
    """Obtiene el topic Kafka correspondiente a un evento."""
    topic = EVENT_NAME_TO_TOPIC.get(event.event_name)
    if topic is None:
        # Si no hay mapeo, ir a dead-letter
        return KafkaTopics.DEAD_LETTER
    return topic
