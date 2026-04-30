from __future__ import annotations

import json
import logging
from typing import Any


logger = logging.getLogger(__name__)


class EventPublisher:
    """Contrato base para publicar eventos del dominio."""

    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None

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


class KafkaEventPublisher(EventPublisher):
    """Publica eventos en Kafka. Si falla, la capa de servicio maneja el fallback."""

    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._producer: Any | None = None

    async def start(self) -> None:
        try:
            from aiokafka import AIOKafkaProducer
        except Exception as exc:
            raise RuntimeError("Dependencia aiokafka no disponible") from exc

        self._producer = AIOKafkaProducer(bootstrap_servers=self._bootstrap_servers)
        await self._producer.start()

    async def stop(self) -> None:
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None

    async def publish(self, event_name: str, payload: dict[str, Any]) -> None:
        if self._producer is None:
            raise RuntimeError("KafkaEventPublisher no inicializado")

        message = {
            "event_name": event_name,
            "payload": payload,
        }
        body = json.dumps(message, ensure_ascii=True).encode("utf-8")
        await self._producer.send_and_wait(self._topic, body)
