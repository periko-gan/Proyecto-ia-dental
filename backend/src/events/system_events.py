"""Eventos del sistema (logs y errores)."""

from typing import Any

from src.events.models import Event, create_event


def create_system_log_event(
    level: str,
    message: str,
    context: dict[str, Any] | None = None,
    source: str = "SystemLogger",
) -> Event:
    """Crea evento de log del sistema."""
    return create_event(
        event_name="system.log",
        payload={
            "level": level,
            "message": message,
            "context": context or {},
        },
        source=source,
    )


def create_system_error_event(
    error_message: str,
    error_type: str,
    traceback_str: str | None = None,
    context: dict[str, Any] | None = None,
    source: str = "ErrorHandler",
) -> Event:
    """Crea evento de error del sistema."""
    return create_event(
        event_name="system.error",
        payload={
            "error_message": error_message,
            "error_type": error_type,
            "traceback": traceback_str,
            "context": context or {},
        },
        source=source,
    )
