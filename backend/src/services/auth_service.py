"""Servicio de autenticación con soporte a eventos."""

from __future__ import annotations

import logging
from uuid import uuid4

from pymongo.errors import DuplicateKeyError

from src.domain.exceptions import (
    AuthenticationError,
    UserAlreadyExistsError,
    ValidationError,
)
from src.events.auth_events import (
    create_token_refresh_event,
    create_user_login_failed_event,
    create_user_login_success_event,
    create_user_logout_event,
    create_user_register_event,
)
from src.events.publishers import EventPublisher
from src.persistence.user_models import UserRecord
from src.persistence.user_repository import UserRepository
from src.services.event_emitter import EventEmitter
from src.services.password_service import PasswordService
from src.services.token_service import TokenService

logger = logging.getLogger(__name__)


class AuthService(EventEmitter):
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        token_service: TokenService,
        event_publisher: EventPublisher | None = None,
    ) -> None:
        super().__init__(event_publisher=event_publisher, logger_name=__name__)
        self._user_repository = user_repository
        self._password_service = password_service
        self._token_service = token_service

    async def register_user(self, name: str, email: str, password: str) -> UserRecord:
        if not name.strip():
            raise ValidationError("El nombre es obligatorio")

        if len(password) < 8:
            raise ValidationError("La contrasena debe tener al menos 8 caracteres")

        existing = await self._user_repository.get_by_email(email)
        if existing is not None:
            raise UserAlreadyExistsError("El usuario ya existe")

        user = UserRecord(
            user_id=str(uuid4()),
            email=email,
            name=name,
            password_hash=self._password_service.hash_password(password),
        )

        try:
            created_user = await self._user_repository.create_user(user)
            # Publicar evento de registro
            await self._safe_publish_event(
                create_user_register_event(user_id=created_user.user_id, email=created_user.email, name=created_user.name)
            )
            await self.publish_system_log(
                message="Usuario registrado",
                context={"user_id": created_user.user_id, "email": created_user.email, "name": created_user.name},
                source="AuthService",
            )
            return created_user
        except DuplicateKeyError as exc:
            raise UserAlreadyExistsError("El usuario ya existe") from exc

    async def login_user(self, email: str, password: str) -> tuple[UserRecord, str]:
        user = await self._user_repository.get_by_email(email)
        if user is None or not user.is_active:
            # Publicar evento de login fallido
            await self._safe_publish_event(create_user_login_failed_event(email=email, reason="Credenciales inválidas"))
            await self.publish_system_error(
                error_message="Login fallido por credenciales invalidas",
                error_type="AuthenticationError",
                context={"email": email},
                source="AuthService",
            )
            raise AuthenticationError("Credenciales invalidas")

        if not self._password_service.verify_password(password, user.password_hash):
            # Publicar evento de login fallido
            await self._safe_publish_event(create_user_login_failed_event(email=email, reason="Contraseña incorrecta"))
            await self.publish_system_error(
                error_message="Login fallido por password incorrecta",
                error_type="AuthenticationError",
                context={"email": email},
                source="AuthService",
            )
            raise AuthenticationError("Credenciales invalidas")

        token = self._token_service.create_access_token(user)

        # Publicar evento de login exitoso
        await self._safe_publish_event(
            create_user_login_success_event(user_id=user.user_id, email=user.email, name=user.name)
        )
        await self.publish_system_log(
            message="Login exitoso",
            context={"user_id": user.user_id, "email": user.email, "name": user.name},
            source="AuthService",
        )

        return user, token

    async def refresh_token(self, token: str) -> str:
        user = await self.get_user_from_token(token)
        new_token = self._token_service.create_access_token(user)
        await self._safe_publish_event(create_token_refresh_event(user_id=user.user_id))
        await self.publish_system_log(
            message="Token refrescado",
            context={"user_id": user.user_id, "email": user.email, "name": user.name},
            source="AuthService",
        )
        return new_token

    async def logout_user(self, token: str) -> bool:
        user = await self.get_user_from_token(token)
        await self._safe_publish_event(create_user_logout_event(user_id=user.user_id, email=user.email, name=user.name))
        await self.publish_system_log(
            message="Logout de usuario",
            context={"user_id": user.user_id, "email": user.email, "name": user.name},
            source="AuthService",
        )
        return True

    async def get_user_from_token(self, token: str) -> UserRecord:
        payload = self._token_service.decode_access_token(token)
        user_id = str(payload["sub"])
        user = await self._user_repository.get_by_user_id(user_id)
        if user is None or not user.is_active:
            raise AuthenticationError("Usuario no valido")
        return user
