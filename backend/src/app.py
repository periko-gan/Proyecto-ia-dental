from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi import Request
# Añadido para CORS
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from src.api.context import AppContext
from src.api.schema import schema
from src.config.mongodb import mongo_manager
from src.config.settings import get_settings
from src.events.analysis_requested_consumer import AnalysisRequestedConsumer
from src.events.dead_letter import DeadLetterRepository
from src.events.publishers import EventPublisher, KafkaEventPublisher, LogEventPublisher, NullEventPublisher
from src.persistence.repository import AnalysisRepository
from src.persistence.user_repository import UserRepository
from src.services.analysis_service import AnalysisService
from src.services.auth_service import AuthService
from src.services.inference_service import InferenceService
from src.services.password_service import PasswordService
from src.services.result_service import ResultService
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

    # Habilitar CORS para permitir todas las solicitudes desde cualquier origen.
    # Esto es intencionado para entornos de desarrollo; en producción restringir los orígenes.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
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

    graphql_app = GraphQLRouter(
        schema, 
        context_getter=get_context,
    )
    app.include_router(graphql_app, prefix="/graphql")
    
    # Servir las imágenes subidas como archivos estáticos
    from fastapi.staticfiles import StaticFiles
    app.mount("/uploads", StaticFiles(directory=settings.resolved_uploads_dir), name="uploads")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.on_event("startup")
    async def startup_event() -> None:
        logger.info("Inicializando backend")

        uploads_dir = settings.resolved_uploads_dir
        uploads_dir.mkdir(parents=True, exist_ok=True)

        await mongo_manager.connect(settings.mongo_uri, settings.mongo_db_name)
        # Inicializar DeadLetterRepository
        dead_letter_repository = DeadLetterRepository(
            mongo_manager.database,
            collection_name=settings.mongo_dead_letter_collection,
        )
        await dead_letter_repository.ensure_indexes()

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

        # Evento publisher será inyectado después
        event_publisher: EventPublisher | None = None

        if not settings.events_enabled:
            event_publisher = NullEventPublisher()
        elif settings.events_transport.lower() == "log":
            event_publisher = LogEventPublisher()
        elif settings.events_transport.lower() == "kafka" and settings.kafka_enabled:
            try:
                # Pasar DeadLetterRepository a KafkaEventPublisher
                event_publisher = KafkaEventPublisher(
                    bootstrap_servers=settings.kafka_bootstrap_servers,
                    dead_letter_repository=dead_letter_repository,
                )
                await event_publisher.start()
                logger.info("Eventos Kafka habilitados con soporte a DLQ")
            except Exception:
                logger.exception("No se pudo inicializar Kafka. Se usa transporte log como fallback.")
                event_publisher = LogEventPublisher()
        else:
            logger.warning(
                "Transporte de eventos no soportado: %s. Se deshabilitan eventos.",
                settings.events_transport,
            )
            event_publisher = NullEventPublisher()

        # Inyectar event_publisher en servicios
        upload_service = UploadService(settings, event_publisher=event_publisher)
        inference_service = InferenceService(settings, model_loader, event_publisher=event_publisher)
        result_service = ResultService(event_publisher=event_publisher)

        analysis_service = AnalysisService(
            settings,
            upload_service,
            inference_service,
            result_service,
            repository,
            event_publisher=event_publisher,
        )
        password_service = PasswordService()
        token_service = TokenService(settings)
        auth_service = AuthService(user_repository, password_service, token_service, event_publisher=event_publisher)

        inference_consumer = None
        if (
            settings.events_enabled
            and settings.events_transport.lower() == "kafka"
            and settings.kafka_enabled
            and settings.kafka_inference_consumer_enabled
        ):
            try:
                inference_consumer = AnalysisRequestedConsumer(settings, inference_service)
                await inference_consumer.start()
                logger.info("Consumidor opcional de analysis.requested habilitado")
            except Exception:
                logger.exception("No se pudo iniciar AnalysisRequestedConsumer")
                inference_consumer = None

        app.state.analysis_service = analysis_service
        app.state.auth_service = auth_service
        app.state.event_publisher = event_publisher
        app.state.dead_letter_repository = dead_letter_repository
        app.state.inference_consumer = inference_consumer
        logger.info("Backend inicializado correctamente")

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        logger.info("Cerrando backend")
        event_publisher = getattr(app.state, "event_publisher", None)
        inference_consumer = getattr(app.state, "inference_consumer", None)
        if inference_consumer is not None:
            try:
                await inference_consumer.stop()
            except Exception:
                logger.exception("No se pudo cerrar AnalysisRequestedConsumer")
        if event_publisher is not None:
            try:
                await event_publisher.stop()
            except Exception:
                logger.exception("No se pudo cerrar el publisher de eventos")
        await mongo_manager.close()

    return app
