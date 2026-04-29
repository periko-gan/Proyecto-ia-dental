# Backend - Proyecto IA Dental

Primera entrega minima del backend con arquitectura por capas para flujo:
subida -> inferencia -> guardado -> respuesta por GraphQL.

## Requisitos
- Python 3.11+
- MongoDB en ejecucion

## Configuracion
1. Copia `.env.example` a `.env` y ajusta valores.
2. Instala dependencias:
   - `pip install -e .`

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
