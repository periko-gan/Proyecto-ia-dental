"""Persistencia y manejo de eventos fallidos (Dead Letter Queue)."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from uuid import UUID

from src.events.models import Event

logger = logging.getLogger(__name__)


@dataclass
class DeadLetterRecord:
    """Registro de un evento que falló al publicarse."""

    event_id: str
    original_event: dict
    error_message: str
    error_type: str
    created_at: datetime
    resolved: bool = False
    resolution_notes: str | None = None


class DeadLetterRepository:
    """Persistencia en MongoDB para dead letter events."""

    def __init__(self, database, collection_name: str = "dead_letter_events") -> None:
        self._db = database
        self._collection_name = collection_name

    @property
    def _collection(self):
        return self._db[self._collection_name]

    async def ensure_indexes(self) -> None:
        """Crea índices necesarios en la colección."""
        await self._collection.create_index("event_id", unique=True)
        await self._collection.create_index("created_at")
        await self._collection.create_index("resolved")

    async def save_dead_letter(self, event: Event, error: Exception) -> DeadLetterRecord:
        """Persiste un evento fallido en MongoDB."""
        record = DeadLetterRecord(
            event_id=str(event.event_id),
            original_event=event.to_dict(),
            error_message=str(error),
            error_type=type(error).__name__,
            created_at=datetime.now(timezone.utc),
        )

        try:
            await self._collection.insert_one(asdict(record))
            logger.warning("Dead letter guardado: event_id=%s error=%s", record.event_id, record.error_message)
        except Exception as exc:
            logger.exception("Error guardando dead letter para event_id=%s", record.event_id)
            raise

        return record

    async def get_by_event_id(self, event_id: str) -> DeadLetterRecord | None:
        """Obtiene un dead letter por event_id."""
        doc = await self._collection.find_one({"event_id": event_id})
        if doc is None:
            return None
        doc.pop("_id", None)
        return DeadLetterRecord(**doc)

    async def list_unresolved(self, limit: int = 100, offset: int = 0) -> list[DeadLetterRecord]:
        """Lista dead letters sin resolver."""
        cursor = self._collection.find({"resolved": False}).skip(offset).limit(limit)
        records = []
        async for doc in cursor:
            doc.pop("_id", None)
            records.append(DeadLetterRecord(**doc))
        return records

    async def mark_resolved(self, event_id: str, resolution_notes: str | None = None) -> bool:
        """Marca un dead letter como resuelto."""
        result = await self._collection.update_one(
            {"event_id": event_id},
            {"$set": {"resolved": True, "resolution_notes": resolution_notes}},
        )
        return result.modified_count > 0

    async def count_unresolved(self) -> int:
        """Cuenta dead letters sin resolver."""
        return await self._collection.count_documents({"resolved": False})
