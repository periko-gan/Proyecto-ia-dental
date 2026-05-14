from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from src.events.event_router import get_topic_for_event
from src.events.models import Event

if TYPE_CHECKING:
    from src.events.dead_letter import DeadLetterRepository

logger = logging.getLogger(__name__)


class EventPublisher:
    """Contrato base para publicar eventos del dominio con Event objects."""

    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None

    async def publish(self, event: Event) -> None:
        raise NotImplementedError


class NullEventPublisher(EventPublisher):
    """No-op publisher para entornos sin eventos habilitados."""

    async def publish(self, event: Event) -> None:
        _ = event
        return None


class LogEventPublisher(EventPublisher):
    """Publica eventos como logs estructurados."""

    async def publish(self, event: Event) -> None:
        logger.info("event=%s version=%s source=%s payload=%s", event.event_name, event.version, event.source, event.payload)


class KafkaEventPublisher(EventPublisher):
    """Publica eventos en Kafka con retry y fallback a DLQ."""

    def __init__(
        self,
        bootstrap_servers: str,
        dead_letter_repository: DeadLetterRepository | None = None,
        max_retries: int = 3,
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._dead_letter_repository = dead_letter_repository
        self._max_retries = max_retries
        self._producer: Any | None = None

    async def start(self) -> None:
        try:
            from aiokafka import AIOKafkaProducer
        except Exception as exc:
            raise RuntimeError("Dependencia aiokafka no disponible") from exc

        self._producer = AIOKafkaProducer(bootstrap_servers=self._bootstrap_servers)
        await self._producer.start()
        logger.info("KafkaEventPublisher iniciado en %s", self._bootstrap_servers)

    async def stop(self) -> None:
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None
        logger.info("KafkaEventPublisher detenido")

    async def publish(self, event: Event) -> None:
        """Publica evento en Kafka. Si falla, intenta guardar en DLQ."""
        if self._producer is None:
            raise RuntimeError("KafkaEventPublisher no inicializado")

        topic = get_topic_for_event(event)
        body = json.dumps(event.to_dict(), ensure_ascii=True).encode("utf-8")
        logger.info(
            "Publicando evento Kafka event_id=%s event_name=%s topic=%s",
            event.event_id,
            event.event_name,
            topic,
        )

        # Retry logic
        last_error = None
        for attempt in range(self._max_retries):
            try:
                await self._producer.send_and_wait(topic, body)
                logger.info(
                    "Evento publicado: event_id=%s event_name=%s topic=%s",
                    event.event_id,
                    event.event_name,
                    topic,
                )
                return
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "Intento %d/%d fallido para event_id=%s topic=%s: %s",
                    attempt + 1,
                    self._max_retries,
                    event.event_id,
                    topic,
                    str(exc),
                )

        # Si todos los reintentos fallaron, intentar guardar en DLQ
        logger.error(
            "Evento no publicado después de %d intentos: event_id=%s event_name=%s topic=%s",
            self._max_retries,
            event.event_id,
            event.event_name,
            topic,
        )
        if self._dead_letter_repository is not None:
            try:
                await self._dead_letter_repository.save_dead_letter(event, last_error or Exception("Unknown error"))
                logger.info("Evento guardado en DLQ: event_id=%s", event.event_id)
            except Exception as dlq_error:
                logger.exception("Error guardando en DLQ: event_id=%s", event.event_id)
                raise
        else:
            raise last_error or RuntimeError("No se pudo publicar evento y no hay DLQ disponible")


class CompositeEventPublisher(EventPublisher):
    """Publisher que distribuye eventos a múltiples publishers en paralelo."""

    def __init__(self, publishers: list[EventPublisher]) -> None:
        self._publishers = publishers

    async def start(self) -> None:
        for publisher in self._publishers:
            try:
                await publisher.start()
            except Exception:
                logger.exception("Error iniciando publisher %s", type(publisher).__name__)
                raise

    async def stop(self) -> None:
        for publisher in self._publishers:
            try:
                await publisher.stop()
            except Exception:
                logger.exception("Error deteniendo publisher %s", type(publisher).__name__)

    async def publish(self, event: Event) -> None:
        """Publica en todos los publishers. El fallo en uno no bloquea otros."""
        errors = []
        for publisher in self._publishers:
            try:
                await publisher.publish(event)
            except Exception as exc:
                logger.warning("Error en publisher %s: %s", type(publisher).__name__, str(exc))
                errors.append(exc)

        # Si todos fallaron, relanzar el primer error
        if errors and len(errors) == len(self._publishers):
            raise errors[0]
