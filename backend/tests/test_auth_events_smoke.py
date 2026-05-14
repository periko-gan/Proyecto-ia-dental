"""Tests smoke para eventos de autenticación."""

from __future__ import annotations

from typing import Any

import pytest

from src.domain.exceptions import AuthenticationError, UserAlreadyExistsError
from src.events.publishers import EventPublisher
from src.persistence.user_models import UserRecord
from src.persistence.user_repository import UserRepository
from src.services.auth_service import AuthService
from src.services.password_service import PasswordService
from src.services.token_service import TokenService
from src.config.settings import Settings


class FakeUserRepository(UserRepository):
    def __init__(self):
        self._users: dict[str, UserRecord] = {}

    async def ensure_indexes(self) -> None:
        pass

    async def create_user(self, user: UserRecord) -> UserRecord:
        if user.email in self._users:
            raise Exception("Duplicate key")
        self._users[user.email] = user
        return user

    async def get_by_email(self, email: str) -> UserRecord | None:
        return self._users.get(email)

    async def get_by_user_id(self, user_id: str) -> UserRecord | None:
        for user in self._users.values():
            if user.user_id == user_id:
                return user
        return None


class FakeEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.calls: list[Any] = []

    async def publish(self, event) -> None:
        self.calls.append(event)


@pytest.mark.asyncio
async def test_auth_service_register_publishes_event() -> None:
    """Test que register_user publica evento de registro."""
    event_publisher = FakeEventPublisher()
    service = AuthService(
        user_repository=FakeUserRepository(),
        password_service=PasswordService(),
        token_service=TokenService(Settings()),
        event_publisher=event_publisher,
    )

    user = await service.register_user(name="Maria Perez", email="test@example.com", password="password123")

    assert user.email == "test@example.com"
    assert user.name == "Maria Perez"
    assert len(event_publisher.calls) == 2
    assert event_publisher.calls[0].event_name == "auth.register"
    assert event_publisher.calls[0].payload["email"] == "test@example.com"
    assert event_publisher.calls[0].payload["name"] == "Maria Perez"
    assert event_publisher.calls[1].event_name == "system.log"


@pytest.mark.asyncio
async def test_auth_service_login_success_publishes_event() -> None:
    """Test que login_user exitoso publica evento de login_success."""
    repo = FakeUserRepository()
    ps = PasswordService()
    event_publisher = FakeEventPublisher()
    service = AuthService(
        user_repository=repo,
        password_service=ps,
        token_service=TokenService(Settings()),
        event_publisher=event_publisher,
    )

    # Crear usuario primero
    await service.register_user(name="Maria Perez", email="test@example.com", password="password123")
    event_publisher.calls.clear()  # Limpiar evento de registro

    # Hacer login
    user, token = await service.login_user(email="test@example.com", password="password123")

    assert user.email == "test@example.com"
    assert token is not None
    assert len(event_publisher.calls) == 2
    assert event_publisher.calls[0].event_name == "auth.login_success"
    assert event_publisher.calls[0].payload["email"] == "test@example.com"
    assert event_publisher.calls[0].payload["name"] == "Maria Perez"
    assert event_publisher.calls[1].event_name == "system.log"


@pytest.mark.asyncio
async def test_auth_service_login_failed_publishes_event() -> None:
    """Test que login_user fallido publica evento de login_failed."""
    repo = FakeUserRepository()
    event_publisher = FakeEventPublisher()
    service = AuthService(
        user_repository=repo,
        password_service=PasswordService(),
        token_service=TokenService(Settings()),
        event_publisher=event_publisher,
    )

    with pytest.raises(AuthenticationError):
        await service.login_user(email="nonexistent@example.com", password="password123")

    assert len(event_publisher.calls) == 2
    assert event_publisher.calls[0].event_name == "auth.login_failed"
    assert event_publisher.calls[0].payload["email"] == "nonexistent@example.com"
    assert event_publisher.calls[1].event_name == "system.error"


@pytest.mark.asyncio
async def test_auth_service_refresh_token_publishes_event() -> None:
    repo = FakeUserRepository()
    event_publisher = FakeEventPublisher()
    service = AuthService(
        user_repository=repo,
        password_service=PasswordService(),
        token_service=TokenService(Settings()),
        event_publisher=event_publisher,
    )

    await service.register_user(name="Refresh User", email="refresh@example.com", password="password123")
    _, token = await service.login_user(email="refresh@example.com", password="password123")
    event_publisher.calls.clear()

    refreshed = await service.refresh_token(token)

    assert refreshed
    assert [event.event_name for event in event_publisher.calls] == ["auth.token_refresh", "system.log"]


@pytest.mark.asyncio
async def test_auth_service_logout_publishes_event() -> None:
    repo = FakeUserRepository()
    event_publisher = FakeEventPublisher()
    service = AuthService(
        user_repository=repo,
        password_service=PasswordService(),
        token_service=TokenService(Settings()),
        event_publisher=event_publisher,
    )

    await service.register_user(name="Logout User", email="logout@example.com", password="password123")
    _, token = await service.login_user(email="logout@example.com", password="password123")
    event_publisher.calls.clear()

    result = await service.logout_user(token)

    assert result is True
    assert [event.event_name for event in event_publisher.calls] == ["auth.logout", "system.log"]
