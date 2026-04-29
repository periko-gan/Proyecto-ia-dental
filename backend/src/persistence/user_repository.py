from __future__ import annotations

from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING

from src.persistence.user_models import UserRecord


class UserRepository:
    def __init__(self, database: AsyncIOMotorDatabase, collection_name: str = "users") -> None:
        self._collection = database[collection_name]

    async def ensure_indexes(self) -> None:
        await self._collection.create_index([("email", ASCENDING)], unique=True)
        await self._collection.create_index([("created_at", DESCENDING)])

    async def create_user(self, user: UserRecord) -> UserRecord:
        user.updated_at = datetime.now(timezone.utc)
        await self._collection.insert_one(user.to_mongo())
        return user

    async def get_by_email(self, email: str) -> UserRecord | None:
        document = await self._collection.find_one({"email": email.strip().lower()})
        if document is None:
            return None
        return UserRecord.from_mongo(document)

    async def get_by_user_id(self, user_id: str) -> UserRecord | None:
        document = await self._collection.find_one({"user_id": user_id})
        if document is None:
            return None
        return UserRecord.from_mongo(document)