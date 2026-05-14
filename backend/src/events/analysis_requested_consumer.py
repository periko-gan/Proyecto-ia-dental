from __future__ import annotations

import asyncio
import contextlib
import json
import logging
from typing import Any

from src.config.settings import Settings
from src.events.topics import KafkaTopics
from src.services.inference_service import InferenceService

logger = logging.getLogger(__name__)


class AnalysisRequestedConsumer:
    """Consumidor opcional para dental.analysis.requested."""

    def __init__(self, settings: Settings, inference_service: InferenceService) -> None:
        self._settings = settings
        self._inference_service = inference_service
        self._consumer: Any | None = None
        self._task: asyncio.Task[Any] | None = None
        self._running = False

    async def start(self) -> None:
        try:
            from aiokafka import AIOKafkaConsumer
        except Exception as exc:
            raise RuntimeError("Dependencia aiokafka no disponible para consumer") from exc

        self._consumer = AIOKafkaConsumer(
            KafkaTopics.ANALYSIS_REQUESTED.value,
            bootstrap_servers=self._settings.kafka_bootstrap_servers,
            group_id=self._settings.kafka_inference_consumer_group_id,
            value_deserializer=lambda value: json.loads(value.decode("utf-8")),
            auto_offset_reset=self._settings.kafka_inference_consumer_offset_reset,
        )
        await self._consumer.start()
        self._running = True
        self._task = asyncio.create_task(self._consume_loop())
        logger.info(
            "AnalysisRequestedConsumer iniciado topic=%s group_id=%s",
            KafkaTopics.ANALYSIS_REQUESTED.value,
            self._settings.kafka_inference_consumer_group_id,
        )

    async def stop(self) -> None:
        self._running = False
        if self._task is not None:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None
        if self._consumer is not None:
            await self._consumer.stop()
            self._consumer = None
        logger.info("AnalysisRequestedConsumer detenido")

    async def _consume_loop(self) -> None:
        if self._consumer is None:
            return

        while self._running:
            try:
                message = await self._consumer.getone()
                event_data = message.value
                payload = event_data.get("payload", {}) if isinstance(event_data, dict) else {}
                await self._inference_service.consume_analysis_requested_payload(payload)
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Error consumiendo evento de analysis.requested")
