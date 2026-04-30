from __future__ import annotations

from datetime import datetime, timezone

from pymongo import ASCENDING, DESCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.persistence.models import AnalysisRecord


class AnalysisRepository:
    def __init__(self, database: AsyncIOMotorDatabase, collection_name: str = "analyses") -> None:
        self._collection = database[collection_name]

    async def ensure_indexes(self) -> None:
        await self._collection.create_index([("analysis_id", ASCENDING)], unique=True)
        await self._collection.create_index([("status", ASCENDING)])
        await self._collection.create_index([("created_at", DESCENDING)])
        await self._collection.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])

    async def create_analysis(self, analysis: AnalysisRecord) -> AnalysisRecord:
        analysis.updated_at = datetime.now(timezone.utc)
        await self._collection.insert_one(analysis.to_mongo())
        return analysis

    async def get_by_analysis_id(self, analysis_id: str) -> AnalysisRecord | None:
        document = await self._collection.find_one({"analysis_id": analysis_id})
        if document is None:
            return None
        return AnalysisRecord.from_mongo(document)

    async def get_by_analysis_id_for_user(self, analysis_id: str, user_id: str) -> AnalysisRecord | None:
        document = await self._collection.find_one({"analysis_id": analysis_id, "user_id": user_id})
        if document is None:
            return None
        return AnalysisRecord.from_mongo(document)

    async def list_analyses(self, limit: int = 20, offset: int = 0) -> list[AnalysisRecord]:
        cursor = (
            self._collection.find({})
            .sort("created_at", DESCENDING)
            .skip(offset)
            .limit(limit)
        )
        documents = await cursor.to_list(length=limit)
        return [AnalysisRecord.from_mongo(item) for item in documents]

    async def list_analyses_by_user(self, user_id: str, limit: int = 20, offset: int = 0) -> list[AnalysisRecord]:
        cursor = (
            self._collection.find({"user_id": user_id})
            .sort("created_at", DESCENDING)
            .skip(offset)
            .limit(limit)
        )
        documents = await cursor.to_list(length=limit)
        return [AnalysisRecord.from_mongo(item) for item in documents]

    async def count_all(self) -> int:
        return await self._collection.count_documents({})

    async def count_by_status(self, status: str) -> int:
        return await self._collection.count_documents({"status": status})
