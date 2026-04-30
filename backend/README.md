# Backend - Proyecto IA Dental

Primera entrega minima del backend con arquitectura por capas para flujo:
subida -> inferencia -> guardado -> respuesta por GraphQL.

## Requisitos
- Python 3.11+
- MongoDB en ejecucion
- (Opcional) Kafka + Zookeeper para transporte de eventos

## Dependencias principales

| Paquete | Version minima | Proposito |
|---|---|---|
| fastapi | 0.115.0 | Framework HTTP/REST |
| strawberry-graphql | 0.275.0 | API GraphQL |
| uvicorn | 0.30.0 | Servidor ASGI |
| motor | 3.6.0 | Driver MongoDB async |
| pydantic-settings | 2.6.0 | Configuracion por entorno |
| passlib + bcrypt | 1.7.4 / 4.0.1 | Hash de contrasenas |
| PyJWT | 2.9.0 | Tokens JWT |
| ultralytics | 8.4.32 | Inferencia YOLOv8 |
| pillow | 10.4.0 | Procesamiento de imagenes |
| aiokafka | 0.11.0 | Productor Kafka async (opcional) |
| pytest + pytest-asyncio | 8.3.0 / 0.24.0 | Tests |

Ver [requirements.txt](requirements.txt) para la lista completa.

## Configuracion
1. Copia `.env.example` a `.env` y ajusta valores.
2. Instala dependencias:
   - `pip install -e .` (recomendado, usa pyproject.toml)
   - O bien: `pip install -r requirements.txt`

## MongoDB con Docker (mini)
- Levantar Mongo:
   - `docker compose -f docker-compose.mongo.yml up -d`
- Ver estado:
   - `docker compose -f docker-compose.mongo.yml ps`
- Ver logs:
   - `docker compose -f docker-compose.mongo.yml logs -f mongo`
- Parar y eliminar contenedor:
   - `docker compose -f docker-compose.mongo.yml down`

La configuracion por defecto de `.env` ya apunta a `mongodb://localhost:27017` y base `dental_ai`.

## Ejecutar
- `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

## Endpoints
- `GET /health`
- `POST /graphql` (GraphQL)

## Eventos (inicio Fase 2)
- El flujo de analisis publica eventos de dominio:
   - `analysis.uploaded`
   - `analysis.completed`
   - `analysis.failed`
- Por defecto se emiten como logs estructurados (`DENTAL_AI_EVENTS_TRANSPORT=log`).
- Puedes desactivarlos con `DENTAL_AI_EVENTS_ENABLED=false`.
- Puedes activar Kafka con:
   - `DENTAL_AI_EVENTS_TRANSPORT=kafka`
   - `DENTAL_AI_KAFKA_ENABLED=true`
   - `DENTAL_AI_KAFKA_BOOTSTRAP_SERVERS=localhost:9092`
   - `DENTAL_AI_KAFKA_TOPIC_ANALYSIS_EVENTS=analysis-events`
- Si Kafka no inicia o falla, el backend hace fallback seguro a transporte `log`.
