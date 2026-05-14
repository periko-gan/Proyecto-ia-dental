"""Modelos de eventos para la arquitectura event-driven."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Event:
    """Evento de dominio con formato completo para auditoría y trazabilidad."""

    event_id: UUID
    event_name: str
    version: int
    timestamp: datetime
    source: str
    payload: dict[str, Any]
    correlation_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serializa el evento a dict."""
        data = asdict(self)
        # Convertir UUID a string para JSON serialización
        data["event_id"] = str(self.event_id)
        # Convertir datetime a ISO string
        data["timestamp"] = self.timestamp.isoformat()
        return data


def create_event(
    event_name: str,
    payload: dict[str, Any],
    source: str,
    version: int = 1,
    correlation_id: str | None = None,
) -> Event:
    """Helper para crear eventos con values automáticos."""
    return Event(
        event_id=uuid4(),
        event_name=event_name,
        version=version,
        timestamp=datetime.now(timezone.utc),
        source=source,
        payload=payload,
        correlation_id=correlation_id,
    )
