from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.config.settings import Settings
from src.domain.exceptions import AuthenticationError
from src.persistence.user_models import UserRecord


class TokenService:
    def __init__(self, settings: Settings) -> None:
        self._secret = settings.auth_jwt_secret
        self._algorithm = settings.auth_jwt_algorithm
        self._ttl_minutes = settings.auth_access_token_expire_minutes

    def create_access_token(self, user: UserRecord) -> str:
        now = datetime.now(timezone.utc)
        payload: dict[str, Any] = {
            "sub": user.user_id,
            "email": user.email,
            "role": user.role.value,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._ttl_minutes)).timestamp()),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
        except jwt.InvalidTokenError as exc:
            raise AuthenticationError("Token invalido o expirado") from exc

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Token sin sujeto")
        return payload