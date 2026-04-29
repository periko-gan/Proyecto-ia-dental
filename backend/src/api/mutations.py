from __future__ import annotations

import strawberry
from strawberry.file_uploads import Upload
from strawberry.types import Info

from src.api.context import AppContext
from src.api.types import AuthPayload, UploadResponse, User, to_graphql_analysis, to_graphql_user
from src.domain.exceptions import AuthenticationError, BackendError


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Registra un nuevo usuario con email y contrasena.")
    async def register_user(self, info: Info[AppContext, None], email: str, password: str) -> User:
        user = await info.context.auth_service.register_user(email=email, password=password)
        return to_graphql_user(user)

    @strawberry.mutation(description="Inicia sesion y devuelve un access token JWT para autenticacion Bearer.")
    async def login_user(self, info: Info[AppContext, None], email: str, password: str) -> AuthPayload:
        user, token = await info.context.auth_service.login_user(email=email, password=password)
        return AuthPayload(access_token=token, token_type="Bearer", user=to_graphql_user(user))

    @strawberry.mutation(description="Sube una radiografia, ejecuta inferencia y guarda el analisis asociado al usuario autenticado.")
    async def upload_radiography(self, info: Info[AppContext, None], file: Upload) -> UploadResponse:
        if info.context.current_user is None:
            raise AuthenticationError("Autenticacion requerida")

        try:
            record = await info.context.analysis_service.upload_and_analyze(
                upload=file,
                user_id=info.context.current_user.user_id,
            )
            return UploadResponse(
                success=True,
                message="Analisis completado",
                analysis=to_graphql_analysis(record),
            )
        except BackendError as exc:
            return UploadResponse(success=False, message=str(exc), analysis=None)
        except Exception:
            return UploadResponse(success=False, message="Error interno durante el analisis", analysis=None)
