from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi import Request
from strawberry.fastapi import GraphQLRouter

from src.api.context import AppContext
from src.api.schema import schema
from src.config.mongodb import mongo_manager
from src.config.settings import get_settings
from src.events.publishers import LogEventPublisher, NullEventPublisher
from src.persistence.repository import AnalysisRepository
from src.persistence.user_repository import UserRepository
from src.services.analysis_service import AnalysisService
from src.services.auth_service import AuthService
from src.services.inference_service import InferenceService
from src.services.password_service import PasswordService
from src.services.token_service import TokenService
from src.services.upload_service import UploadService
from src.inference.model_loader import ModelLoader
from src.utils.logger import configure_logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title="Dental IA Backend",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    async def get_context(request: Request) -> AppContext:
        current_user = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
            if token:
                current_user = await app.state.auth_service.get_user_from_token(token)

        return AppContext(
            analysis_service=app.state.analysis_service,
            auth_service=app.state.auth_service,
            current_user=current_user,
        )

    graphql_app = GraphQLRouter(schema, context_getter=get_context)
    app.include_router(graphql_app, prefix="/graphql")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.on_event("startup")
    async def startup_event() -> None:
        logger.info("Inicializando backend")

        uploads_dir = settings.resolved_uploads_dir
        uploads_dir.mkdir(parents=True, exist_ok=True)

        await mongo_manager.connect(settings.mongo_uri, settings.mongo_db_name)
        repository = AnalysisRepository(
            mongo_manager.database,
            collection_name=settings.mongo_analyses_collection,
        )
        await repository.ensure_indexes()

        user_repository = UserRepository(
            mongo_manager.database,
            collection_name=settings.mongo_users_collection,
        )
        await user_repository.ensure_indexes()

        model_loader = ModelLoader(settings)
        if settings.model_warmup_on_startup:
            await model_loader.load_model()

        upload_service = UploadService(settings)
        inference_service = InferenceService(settings, model_loader)

        if not settings.events_enabled:
            event_publisher = NullEventPublisher()
        elif settings.events_transport.lower() == "log":
            event_publisher = LogEventPublisher()
        else:
            logger.warning(
                "Transporte de eventos no soportado en esta fase: %s. Se deshabilitan eventos.",
                settings.events_transport,
            )
            event_publisher = NullEventPublisher()

        analysis_service = AnalysisService(
            settings,
            upload_service,
            inference_service,
            repository,
            event_publisher=event_publisher,
        )
        password_service = PasswordService()
        token_service = TokenService(settings)
        auth_service = AuthService(user_repository, password_service, token_service)

        app.state.analysis_service = analysis_service
        app.state.auth_service = auth_service
        logger.info("Backend inicializado correctamente")

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        logger.info("Cerrando backend")
        await mongo_manager.close()

    return app
