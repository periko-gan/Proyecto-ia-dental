from __future__ import annotations

import strawberry
from strawberry.types import Info

from src.api.context import AppContext
from src.api.types import Analysis, SystemStats, User, to_graphql_analysis, to_graphql_user
from src.domain.exceptions import AuthenticationError, AuthorizationError
from src.persistence.user_models import UserRole


def _require_user(info: Info[AppContext, None]) -> None:
    if info.context.current_user is None:
        raise AuthenticationError("Autenticacion requerida")


@strawberry.type
class Query:
    @strawberry.field(description="Obtiene un analisis por id validando pertenencia al usuario autenticado. Los administradores pueden consultar cualquier analisis.")
    async def get_analysis_by_id(self, info: Info[AppContext, None], analysis_id: str) -> Analysis | None:
        _require_user(info)
        assert info.context.current_user is not None

        if info.context.current_user.role == UserRole.ADMIN:
            record = await info.context.analysis_service.get_analysis_by_id(analysis_id)
        else:
            record = await info.context.analysis_service.get_analysis_by_id_for_user(
                analysis_id=analysis_id,
                user_id=info.context.current_user.user_id,
            )

        if record is None:
            return None
        return to_graphql_analysis(record)

    @strawberry.field(description="Lista global de analisis. Disponible solo para usuarios con rol ADMIN.")
    async def list_analyses(
        self,
        info: Info[AppContext, None],
        limit: int = 20,
        offset: int = 0,
    ) -> list[Analysis]:
        _require_user(info)
        assert info.context.current_user is not None
        if info.context.current_user.role != UserRole.ADMIN:
            raise AuthorizationError("Operacion reservada para administrador")

        records = await info.context.analysis_service.list_analyses(limit=limit, offset=offset)
        return [to_graphql_analysis(record) for record in records]

    @strawberry.field(description="Lista los analisis del usuario autenticado.")
    async def my_analyses(
        self,
        info: Info[AppContext, None],
        limit: int = 20,
        offset: int = 0,
    ) -> list[Analysis]:
        _require_user(info)
        assert info.context.current_user is not None
        records = await info.context.analysis_service.my_analyses(
            user_id=info.context.current_user.user_id,
            limit=limit,
            offset=offset,
        )
        return [to_graphql_analysis(record) for record in records]

    @strawberry.field(description="Devuelve el usuario autenticado en el contexto actual.")
    async def me(self, info: Info[AppContext, None]) -> User | None:
        user = info.context.current_user
        if user is None:
            return None
        return to_graphql_user(user)

    @strawberry.field(description="Estadisticas globales del sistema. Disponible solo para ADMIN.")
    async def get_system_stats(self, info: Info[AppContext, None]) -> SystemStats:
        _require_user(info)
        assert info.context.current_user is not None
        if info.context.current_user.role != UserRole.ADMIN:
            raise AuthorizationError("Operacion reservada para administrador")

        stats = await info.context.analysis_service.get_system_stats()
        return SystemStats(
            total_analyses=stats["total_analyses"],
            completed_analyses=stats["completed_analyses"],
            failed_analyses=stats["failed_analyses"],
        )
