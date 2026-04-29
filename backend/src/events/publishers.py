from __future__ import annotations

import logging
from typing import Any


logger = logging.getLogger(__name__)


class EventPublisher:
    """Contrato base para publicar eventos del dominio."""

    async def publish(self, event_name: str, payload: dict[str, Any]) -> None:
        raise NotImplementedError


class NullEventPublisher(EventPublisher):
    """No-op publisher para entornos sin eventos habilitados."""

    async def publish(self, event_name: str, payload: dict[str, Any]) -> None:
        _ = (event_name, payload)
        return None


class LogEventPublisher(EventPublisher):
    """Publica eventos como logs estructurados mientras se integra Kafka."""

    async def publish(self, event_name: str, payload: dict[str, Any]) -> None:
        logger.info("event=%s payload=%s", event_name, payload)
