from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserRecord(BaseModel):
    user_id: str
    email: str
    password_hash: str
    is_active: bool = True
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized or "@" not in normalized:
            raise ValueError("Email invalido")
        return normalized

    def to_mongo(self) -> dict[str, Any]:
        payload = self.model_dump()
        payload["role"] = self.role.value
        return payload

    @classmethod
    def from_mongo(cls, data: dict[str, Any]) -> "UserRecord":
        normalized = dict(data)
        normalized.pop("_id", None)
        return cls.model_validate(normalized)