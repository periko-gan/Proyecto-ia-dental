# Documentación de la aplicación backend - Servidor de IA Dental

Este documento proporciona una descripción técnica, funcional y de arquitectura del servidor backend correspondiente al sistema de análisis radiográfico dental mediante inteligencia artificial. El servidor está diseñado con una arquitectura limpia (Clean Architecture) orientada al dominio, garantizando la escalabilidad, la mantenibilidad y un acoplamiento débil entre la lógica de negocio y la infraestructura de red o bases de datos.

---

## 1. Stack tecnológico y justificación

La selección de tecnologías del backend responde a necesidades de alto rendimiento, asincronía y facilidad para integrar modelos de inteligencia artificial (Deep Learning):

* **Python 3.11+**: Lenguaje base seleccionado por su absoluto dominio en el ecosistema de Machine Learning y facilidad para la escritura de servidores rápidos.
* **FastAPI**: Framework web moderno, ultrarrápido y asíncrono para construir la API.
* **Strawberry GraphQL**: Biblioteca para la construcción de esquemas GraphQL tipados estáticamente mediante Type Hints nativos de Python. Se integra directamente con FastAPI.
* **Motor (MongoDB)**: Driver asíncrono oficial para conectar con la base de datos documental MongoDB, permitiendo I/O no bloqueante.
* **Ultralytics (YOLOv8)**: Framework líder en visión artificial para la carga, inferencia y decodificación de modelos de detección de objetos.
* **Pydantic**: Herramienta de validación de datos y configuración mediante anotaciones de tipos.
* **AIOKafka**: Cliente asíncrono de Kafka para la emisión de eventos del sistema en la arquitectura de mensajería (Fase 2).

---

## 2. Arquitectura de capas y estructura de directorios

El código de la aplicación se encuentra organizado de forma modular bajo la carpeta principal [src](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/backend/src). Sigue un patrón de separación de responsabilidades estricto:

* **main.py**: Archivo ubicado en la raíz que actúa como el punto de entrada ASGI.
* **src/app.py**: Configuración principal de la aplicación FastAPI, inicialización de eventos de ciclo de vida (startup/shutdown) e inyección de dependencias como middlewares y el enrutador GraphQL.
* **src/api/**: Capa de Exposición y Transporte.
  * Define el contrato GraphQL expuesto al frontend.
  * **schema.py**: Agrupación de todas las operaciones (Root Query y Root Mutation).
  * **queries.py** y **mutations.py**: Definición de los endpoints de lectura y escritura.
  * **types.py**: Tipos de datos devueltos por la API (ej. `Analysis`, `Detection`, `UploadResponse`).
* **src/services/**: Capa de Lógica de Aplicación (Casos de uso).
  * Orquesta el flujo de información sin acoplarse a GraphQL ni a la Base de Datos.
  * **analysis_service.py**: Servicio central que coordina la recepción de una radiografía, su paso por el modelo de IA y la persistencia de los resultados.
  * **upload_service.py**: Encargado de la validación de archivos, tipos MIME y guardado en el sistema de archivos local temporal.
  * **inference_service.py**: Fachada para solicitar predicciones al modelo subyacente de Inteligencia Artificial.
* **src/inference/**: Capa de Inteligencia Artificial y Visión Computacional.
  * **model_loader.py**: Patrón Singleton con carga diferida (*lazy-loading*) del archivo `.pt` de YOLO, garantizando que el arranque del servidor no se retrase por la carga en RAM/VRAM de los tensores matemáticos.
  * **model_adapter.py**: Traductor que convierte la salida cruda matemática de YOLOv8 (coordenadas de cajas, clases, tensores) en objetos de dominio Python convencionales.
  * **device_resolver.py**: Lógica matemática para auto-detectar el hardware óptimo (CUDA para Nvidia, MPS de Apple, o CPU estándar) para la inferencia.
* **src/persistence/**: Capa de Acceso a Datos.
  * **repository.py**: Abstracción del acceso a MongoDB (operaciones de guardado y lectura) para la colección de análisis diagnósticos.
  * **models.py**: Definición estructurada de los documentos almacenados en base de datos.
* **src/config/**: Gestión de Infraestructura.
  * **settings.py**: Clase centralizada que lee y valida todas las variables de entorno (`.env`) usando Pydantic Settings.
  * **mongodb.py**: Inicialización y gestión de la conexión asíncrona con el motor de base de datos.
* **src/events/**: Capa de Mensajería.
  * **publishers.py**: Implementa el patrón publicador para enviar telemetría o eventos del sistema (ej. radiografía procesada, error crítico) hacia Apache Kafka de manera asíncrona.
* **src/domain/**: Lógica de Dominio y Contratos Centrales.
  * **exceptions.py**: Definición de errores tipificados específicos del negocio clínico o técnico (ej. `ModelNotLoadedError`, `InvalidFileFormatError`).
* **src/utils/**: Herramientas Genéricas.
  * Módulos auxiliares, validadores sin estado y formateadores compartidos en todo el entorno.

---

## 3. Flujo principal de análisis radiográfico

El caso de uso core del servidor backend es la ingesta de una imagen y su correspondiente predicción diagnóstica. Este proceso respeta una cadena lógica que fluye a través de las capas antes descritas:

1. **Recepción (api)**: El cliente realiza la mutación GraphQL `uploadRadiography` adjuntando un binario (Multipart Form Data).
2. **Validación y Almacenamiento temporal (services)**: El `upload_service` evalúa la imagen clínica, valida su formato criptográfico, y la almacena de manera unívoca utilizando UUIDs en la carpeta local segura `storage/uploads/`.
3. **Inferencia de IA (inference)**: El `analysis_service` cede el control a la capa de Visión Computacional pasándole la ubicación física del archivo. La red convolucional YOLOv8 analiza la imagen y calcula las métricas de probabilidad (Confidence Scores) de las patologías detectadas.
4. **Adaptación Polimórfica**: El adaptador convierte el output matemático de Ultralytics retornando una estructura estandarizada de objetos `Detection`.
5. **Persistencia (persistence)**: Se inserta un documento consolidado de base de datos con el identificador del paciente/análisis, las coordenadas de cada hallazgo y el estado general.
6. **Respuesta (api)**: La capa GraphQL empaca y estructura todo el informe en un único nodo JSON, despachándolo de vuelta al frontend para su renderizado inminente.

---

## 4. Diseño de la API GraphQL (Strawberry)

El backend expone su funcionalidad a través de un esquema único y fuertemente tipado utilizando GraphQL, eliminando los problemas de falta de datos (under-fetching) o exceso de datos (over-fetching) clásicos de las APIs REST.

* **Tipado Estricto (Code-First)**: El esquema no se define en archivos `.graphql` de texto plano, sino que se auto-genera a partir de clases de Python puras (`@strawberry.type`). Esto permite que los validadores estáticos detecten errores en tiempo de desarrollo.
* **Resolvers**: Las funciones en `queries.py` (lecturas) y `mutations.py` (escrituras) actúan como controladores. Su única responsabilidad es recibir la solicitud del frontend, inyectar el contexto de la aplicación, y delegar el esfuerzo computacional a la capa `services/`.
* **Transporte Multipart (Subida de Archivos)**: Dado que GraphQL tradicionalmente solo transmite JSON, se integró un soporte que respeta la especificación *GraphQL Multipart Request*, permitiendo la transmisión asíncrona de las radiografías (tipo `Upload`) en la misma mutación sin necesidad de APIs REST paralelas.

---

## 5. Motor de Base de Datos Documental (MongoDB)

Toda la persistencia clínica del sistema se consolida en una base de datos NoSQL MongoDB, aprovechando su agilidad documental para lidiar con el esquema fluido de detecciones de la Inteligencia Artificial.

* **Colecciones (Collections)**: El esquema está centrado en la colección `analyses`, la cual almacena cada procesamiento de radiografía junto a su estado, métricas de inferencia de YOLO, y un arreglo incrustado de todas las patologías detectadas en dicha placa, evitando cruces relacionales costosos (JOINs).
* **Driver Asíncrono (I/O no bloqueante)**: En lugar de un driver síncrono, se implementó la librería `Motor`. Dado que FastAPI corre sobre un Event Loop de concurrencia ASGI, cualquier escritura o lectura hacia MongoDB liberará el hilo principal para servir otras peticiones web concurrentes de forma simultánea.
* **Mapeo Pydantic**: El acceso a base de datos se encapsula dentro del `repository.py`, transformando de forma transparente los documentos nativos (BSON/diccionarios) en entidades inmutables de Pydantic para el resto de la aplicación, garantizando seguridad estricta de tipos.

---

## 6. Configuración del Entorno de Ejecución

El servidor requiere la definición de un mapa de variables en el archivo `.env` local o en las variables inyectadas de su contenedor Docker.

* **Configuración del Modelo Predictivo**: Rutas locales hacia el archivo pre-entrenado de pesos de YOLO (`DENTAL_AI_MODEL_PATH`) y establecimiento de los umbrales de probabilidad (`DENTAL_AI_CONFIDENCE_THRESHOLD`) mínimos aceptables.
* **Base de Datos Documental**: URI de conexión hacia el clúster MongoDB (`DENTAL_AI_MONGO_URI`).
* **Mensajería Event-Driven (Kafka)**: Interuptores booleanos e IP para la habilitación de envío de logs estructurados hacia el clúster Apache Kafka (`DENTAL_AI_KAFKA_ENABLED`, `DENTAL_AI_KAFKA_BOOTSTRAP_SERVERS`).

La lectura de este entorno se somete a validación estricta al ejecutarse el servidor (`FastAPI startup`). El fallo o la ausencia de una variable crítica resultará en un aborto temprano de la aplicación ("Fail Fast"), garantizando la seguridad en el despliegue.

---

## 7. Eventos y Mensajería Híbrida (Kafka/Logs)

Para soportar un crecimiento horizontal e ingesta analítica en el sistema Big Data (ELK / Logstash / Grafana), el backend incorpora un emisor de notificaciones asíncronas estructurado.

* **Estrategia Fallback**: La arquitectura está programada para ser tolerante a fallos de red. Si el clúster local de Kafka no está disponible, el módulo de `publishers.py` conmuta de manera inmediata la emisión de mensajería hacia el stdout/logs tradicionales, asegurando que la API no se interrumpa.
* **Tópicos de Emisión**:
  * `dental.image.uploaded`
  * `dental.analysis.requested`
  * `dental.analysis.completed`
  * `dental.analysis.failed`

---

## 8. Operativa y Comandos Locales

El fichero global `pyproject.toml` especifica el comportamiento estándar y las versiones de dependencias del ecosistema Python necesarias.

### Ejecución de la API en Modo Desarrollo
El arranque convencional con recarga en caliente (Hot-Reload) ante modificaciones de código se ejecuta con el servidor Uvicorn:

```sh
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Interfaces de Depuración Interactivas
Cuando el motor web está activo, habilita endpoints visuales automatizados para el desarrollador:

* **Consola GraphQL (GraphiQL)**: `http://localhost:8000/graphql` - Un IDE web integrado que lista dinámicamente las operaciones de lectura (Query) y escritura (Mutation) disponibles en base a los esquemas tipeados, permitiendo pruebas granulares inmediatas.
* **Controles de Salud (Health Checks)**: `http://localhost:8000/health` - Endpoint base para orquestadores (Node-RED o Swarm) que confirma de inmediato la estabilidad y reactividad del hilo del framework web.
