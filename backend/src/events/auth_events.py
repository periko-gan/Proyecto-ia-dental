"""Eventos de autenticación."""

from src.events.models import Event, create_event


def create_user_register_event(user_id: str, email: str, name: str) -> Event:
    """Crea evento de registro de usuario."""
    return create_event(
        event_name="auth.register",
        payload={
            "user_id": user_id,
            "email": email,
            "name": name,
        },
        source="AuthService",
        correlation_id=user_id,
    )


def create_user_login_success_event(user_id: str, email: str, name: str) -> Event:
    """Crea evento de login exitoso."""
    return create_event(
        event_name="auth.login_success",
        payload={
            "user_id": user_id,
            "email": email,
            "name": name,
        },
        source="AuthService",
        correlation_id=user_id,
    )


def create_user_login_failed_event(email: str, reason: str) -> Event:
    """Crea evento de login fallido."""
    return create_event(
        event_name="auth.login_failed",
        payload={
            "email": email,
            "reason": reason,
        },
        source="AuthService",
    )


def create_user_logout_event(user_id: str, email: str, name: str) -> Event:
    """Crea evento de logout."""
    return create_event(
        event_name="auth.logout",
        payload={
            "user_id": user_id,
            "email": email,
            "name": name,
        },
        source="AuthService",
        correlation_id=user_id,
    )


def create_token_refresh_event(user_id: str) -> Event:
    """Crea evento de refresh de token."""
    return create_event(
        event_name="auth.token_refresh",
        payload={
            "user_id": user_id,
        },
        source="AuthService",
        correlation_id=user_id,
    )
