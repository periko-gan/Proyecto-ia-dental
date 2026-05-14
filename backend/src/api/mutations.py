from __future__ import annotations

import logging

import strawberry
from strawberry.types import Info

from src.api.context import AppContext
from src.api.types import AuthPayload, UploadResponse, User, to_graphql_analysis, to_graphql_user
from src.domain.exceptions import AuthenticationError, BackendError


logger = logging.getLogger(__name__)


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Registra un nuevo usuario con nombre, email y contrasena.")
    async def register_user(self, info: Info[AppContext, None], name: str, email: str, password: str) -> User:
        user = await info.context.auth_service.register_user(name=name, email=email, password=password)
        return to_graphql_user(user)

    @strawberry.mutation(description="Inicia sesion y devuelve un access token JWT para autenticacion Bearer.")
    async def login_user(self, info: Info[AppContext, None], email: str, password: str) -> AuthPayload:
        user, token = await info.context.auth_service.login_user(email=email, password=password)
        return AuthPayload(access_token=token, token_type="Bearer", user=to_graphql_user(user))

    @strawberry.mutation(description="Refresca un token JWT válido y devuelve uno nuevo.")
    async def refresh_token(self, info: Info[AppContext, None], token: str) -> str:
        return await info.context.auth_service.refresh_token(token)

    @strawberry.mutation(description="Publica evento de logout para un token válido.")
    async def logout_user(self, info: Info[AppContext, None], token: str) -> bool:
        return await info.context.auth_service.logout_user(token)

    @strawberry.mutation(description="Sube una radiografia en base64, ejecuta inferencia y guarda el analisis asociado al usuario autenticado.")
    async def upload_radiography(self, info: Info[AppContext, None], file_base64: str, file_name: str, mime_type: str) -> UploadResponse:
        if info.context.current_user is None:
            raise AuthenticationError("Autenticacion requerida")

        try:
            record = await info.context.analysis_service.upload_and_analyze(
                file_base64=file_base64,
                file_name=file_name,
                mime_type=mime_type,
                user_id=info.context.current_user.user_id,
            )
            return UploadResponse(
                success=True,
                message="Analisis completado",
                analysis=to_graphql_analysis(record),
            )
        except BackendError as exc:
            logger.warning("Fallo uploadRadiography: %s", exc)
            return UploadResponse(success=False, message=str(exc), analysis=None)
        except Exception as exc:
            logger.exception("Error interno inesperado en uploadRadiography")
            return UploadResponse(
                success=False,
                message=f"Error interno durante el analisis: {exc}",
                analysis=None,
            )
