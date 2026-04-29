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
