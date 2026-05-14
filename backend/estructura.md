# Estructura base backend - Primera entrega minima

Esta estructura implementa la base funcional prioritaria:

subida de imagen -> inferencia -> normalizacion -> persistencia MongoDB -> respuesta GraphQL

## Arbol actual

backend/
├── .env.example
├── instrucciones.md
├── estructura.md
├── main.py
├── pyproject.toml
├── README.md
└── src/
	├── __init__.py
	├── app.py
	├── api/
	│   ├── __init__.py
	│   ├── context.py
	│   ├── mutations.py
	│   ├── queries.py
	│   ├── schema.py
	│   └── types.py
	├── config/
	│   ├── __init__.py
	│   ├── mongodb.py
	│   └── settings.py
	├── domain/
	│   ├── __init__.py
	│   └── exceptions.py
	├── events/
	│   ├── __init__.py
	│   └── publishers.py
	├── inference/
	│   ├── __init__.py
	│   ├── device_resolver.py
	│   ├── model_adapter.py
	│   └── model_loader.py
	├── persistence/
	│   ├── __init__.py
	│   ├── models.py
	│   └── repository.py
	├── services/
	│   ├── __init__.py
	│   ├── analysis_service.py
	│   ├── inference_service.py
	│   └── upload_service.py
	└── utils/
		├── __init__.py
		├── logger.py
		└── validators.py

## Rol de cada capa

- api: contrato GraphQL (queries, mutation, tipos y schema).
- services: casos de uso y orquestacion del flujo funcional.
- inference: carga de modelo YOLO y adaptacion de salida.
- persistence: modelo documental y acceso a MongoDB.
- config: variables de entorno y cliente de infraestructura.
- domain: errores de dominio y contratos internos.
- events: base preparada para integrar eventos en fases posteriores.
- utils: utilidades transversales (logging y validadores).

## Estado de esta entrega

Incluido en esta fase:

1. estructura base por capas,
2. arranque de backend en Python con FastAPI,
3. configuracion por variables de entorno,
4. conexion MongoDB con Motor,
5. base GraphQL minima,
6. servicios iniciales de inferencia y analisis.

No incluido en esta fase:

1. Kafka,
2. Node-RED,
3. ELK,
4. observabilidad avanzada,
5. extras no prioritarios.
