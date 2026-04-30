from __future__ import annotations

from uuid import uuid4

from pymongo.errors import DuplicateKeyError

from src.domain.exceptions import (
    AuthenticationError,
    UserAlreadyExistsError,
    ValidationError,
)
from src.persistence.user_models import UserRecord
from src.persistence.user_repository import UserRepository
from src.services.password_service import PasswordService
from src.services.token_service import TokenService


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        token_service: TokenService,
    ) -> None:
        self._user_repository = user_repository
        self._password_service = password_service
        self._token_service = token_service

    async def register_user(self, email: str, password: str) -> UserRecord:
        if len(password) < 8:
            raise ValidationError("La contrasena debe tener al menos 8 caracteres")

        existing = await self._user_repository.get_by_email(email)
        if existing is not None:
            raise UserAlreadyExistsError("El usuario ya existe")

        user = UserRecord(
            user_id=str(uuid4()),
            email=email,
            password_hash=self._password_service.hash_password(password),
        )

        try:
            return await self._user_repository.create_user(user)
        except DuplicateKeyError as exc:
            raise UserAlreadyExistsError("El usuario ya existe") from exc

    async def login_user(self, email: str, password: str) -> tuple[UserRecord, str]:
        user = await self._user_repository.get_by_email(email)
        if user is None or not user.is_active:
            raise AuthenticationError("Credenciales invalidas")

        if not self._password_service.verify_password(password, user.password_hash):
            raise AuthenticationError("Credenciales invalidas")

        token = self._token_service.create_access_token(user)
        return user, token

    async def get_user_from_token(self, token: str) -> UserRecord:
        payload = self._token_service.decode_access_token(token)
        user_id = str(payload["sub"])
        user = await self._user_repository.get_by_user_id(user_id)
        if user is None or not user.is_active:
            raise AuthenticationError("Usuario no valido")
        return user