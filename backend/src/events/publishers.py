from __future__ import annotations


class EventPublisher:
    """Placeholder de publicador para futura integracion con Kafka."""

    async def publish(self, event_name: str, payload: dict) -> None:
        _ = (event_name, payload)
        return None
