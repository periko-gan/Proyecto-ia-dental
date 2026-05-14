from __future__ import annotations

import logging
from typing import Any

from src.events.models import Event
from src.events.publishers import EventPublisher, NullEventPublisher
from src.events.system_events import create_system_error_event, create_system_log_event


class EventEmitter:
    """Base reusable para publicar eventos sin romper flujo de negocio."""

    def __init__(self, event_publisher: EventPublisher | None = None, logger_name: str | None = None) -> None:
        self._event_publisher = event_publisher or NullEventPublisher()
        self._logger = logging.getLogger(logger_name or self.__class__.__module__)

    async def _safe_publish_event(self, event: Event) -> None:
        try:
            await self._event_publisher.publish(event)
        except Exception:
            self._logger.exception("No se pudo publicar evento %s para event_id=%s", event.event_name, event.event_id)

    async def publish_system_log(
        self,
        message: str,
        level: str = "INFO",
        context: dict[str, Any] | None = None,
        source: str | None = None,
    ) -> None:
        await self._safe_publish_event(
            create_system_log_event(
                level=level,
                message=message,
                context=context,
                source=source or self.__class__.__name__,
            )
        )

    async def publish_system_error(
        self,
        error_message: str,
        error_type: str,
        traceback_str: str | None = None,
        context: dict[str, Any] | None = None,
        source: str | None = None,
    ) -> None:
        await self._safe_publish_event(
            create_system_error_event(
                error_message=error_message,
                error_type=error_type,
                traceback_str=traceback_str,
                context=context,
                source=source or self.__class__.__name__,
            )
        )