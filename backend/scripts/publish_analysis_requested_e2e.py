from __future__ import annotations

import argparse
import asyncio
import json

from src.config.settings import Settings
from src.events.analysis_events import create_analysis_requested_event
from src.events.publishers import KafkaEventPublisher


async def main() -> None:
    parser = argparse.ArgumentParser(description="Publica un evento analysis.requested para prueba manual E2E")
    parser.add_argument("--analysis-id", required=True)
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--file-name", required=True)
    parser.add_argument("--file-path", required=True)
    args = parser.parse_args()

    settings = Settings()
    event = create_analysis_requested_event(
        analysis_id=args.analysis_id,
        user_id=args.user_id,
        file_name=args.file_name,
        file_path=args.file_path,
        correlation_id=args.analysis_id,
    )

    publisher = KafkaEventPublisher(bootstrap_servers=settings.kafka_bootstrap_servers)
    await publisher.start()
    try:
        await publisher.publish(event)
    finally:
        await publisher.stop()

    print(json.dumps({
        "published": True,
        "topic": "dental.analysis.requested",
        "event_id": str(event.event_id),
        "analysis_id": args.analysis_id,
        "user_id": args.user_id,
        "file_path": args.file_path,
    }, ensure_ascii=True))


if __name__ == "__main__":
    asyncio.run(main())
