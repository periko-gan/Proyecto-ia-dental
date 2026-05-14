# Contexto del proyecto backend

Estamos desarrollando el backend de una aplicación de apoyo a la identificación de anomalías dentales en radiografías mediante Inteligencia Artificial.

## Objetivo general del backend

Construir un backend robusto, modular y mantenible capaz de:

1. recibir radiografías dentales desde el frontend,
2. procesarlas usando un modelo de IA ya entrenado,
3. devolver al frontend los resultados de inferencia,
4. persistir imágenes, resultados y metadatos en base de datos,
5. exponer toda la funcionalidad mediante una API GraphQL,
6. registrar eventos, logs y métricas técnicas,
7. dejar preparada una arquitectura escalable y desacoplada.

## Meta funcional real

El flujo mínimo que debe funcionar de punta a punta es este:

- el usuario sube una radiografía desde el frontend,
- el backend recibe la imagen,
- el backend carga el modelo entrenado,
- el backend ejecuta la inferencia,
- el backend interpreta y estructura el resultado,
- el backend guarda el análisis en MongoDB,
- el backend devuelve al frontend el resultado del análisis.

Ese flujo es la prioridad absoluta. Todo lo demás es secundario hasta que esto funcione bien.

---

# Tecnologías del backend y papel de cada una

## 1. Python
Python será el lenguaje principal del backend.

### Se utilizará para:
- lógica de negocio,
- integración con el modelo de IA,
- procesamiento de imágenes,
- ejecución de inferencia,
- acceso a base de datos,
- implementación de la API GraphQL,
- orquestación de servicios internos.

### Requisitos
El código debe estar organizado en módulos claros, con separación entre:
- capa de API,
- capa de servicios,
- capa de inferencia,
- capa de persistencia,
- capa de eventos,
- utilidades y configuración.

---

## 2. Modelo de IA: YOLO con Ultralytics
El modelo ya entrenado es el núcleo de detección de anomalías dentales en radiografías.

### Responsabilidad del backend respecto al modelo
El backend NO debe entrenar el modelo en producción.
El backend solo debe:
- cargar el modelo ya entrenado desde disco o ruta configurada,
- recibir una imagen,
- ejecutarle inferencia,
- transformar el resultado a un formato útil para la aplicación,
- devolver clases detectadas, probabilidades, coordenadas y metadatos.

### Consideraciones importantes
- La carga del modelo debe estar desacoplada del resto del sistema.
- El modelo debe inicializarse una sola vez al arrancar el servicio, si es posible.
- Debe existir manejo de errores por si el modelo no carga o la inferencia falla.
- Debe haber una capa adaptadora que convierta la salida nativa de Ultralytics a un formato interno estable.

### Resultado esperado de la inferencia
La salida normalizada debe incluir como mínimo:
- nombre o id de la imagen,
- estado del análisis,
- lista de detecciones,
- clase detectada,
- confianza,
- bounding box,
- timestamp de ejecución,
- tiempo de procesamiento,
- versión del modelo.

---

## 3. GraphQL
La comunicación entre frontend y backend debe realizarse mediante GraphQL.

### Objetivo
Definir una capa de acceso limpia y estable para que el frontend consuma los datos del sistema sin depender de detalles internos.

### GraphQL debe permitir como mínimo:
- subir una radiografía para análisis,
- consultar un análisis por id,
- consultar listado de análisis,
- consultar detalle de detecciones,
- consultar estadísticas básicas del sistema.

### Principios de diseño
- El schema debe ser claro, coherente y estable.
- Los nombres de tipos, campos y mutations deben estar bien definidos desde el principio.
- El frontend debe depender del contrato GraphQL, no de implementaciones internas del backend.

### Posibles tipos a modelar
- `Analysis`
- `Detection`
- `UploadResponse`
- `AnalysisStatus`
- `SystemStats`

### Posibles operaciones
#### Mutations
- `uploadRadiography(...)`
- `analyzeRadiography(...)` si se separa subida de análisis

#### Queries
- `getAnalysisById(id)`
- `listAnalyses(...)`
- `getSystemStats()`

### Importante
Antes de implementar muchas pantallas o lógica adicional, debe quedar cerrado el contrato GraphQL.

---

## 4. MongoDB
MongoDB será la base de datos principal del backend.

### Qué debe almacenar
- imágenes procesadas o referencias a su ubicación,
- resultados de inferencia,
- clases detectadas,
- probabilidades,
- coordenadas,
- metadatos del análisis,
- estado del procesamiento,
- logs funcionales básicos si procede.

### Colecciones sugeridas
- `analyses`
- `detections`
- `uploads`
- `system_events` o similar si se desea separar eventos funcionales

### Cada análisis debería guardar como mínimo
- id del análisis,
- nombre del archivo,
- ruta o referencia de almacenamiento,
- fecha de subida,
- fecha de análisis,
- estado,
- resultado normalizado,
- versión del modelo,
- errores si los hubo,
- tiempo de inferencia.

### Principios
- Diseñar documentos útiles para consulta desde frontend.
- Evitar guardar estructuras ambiguas.
- Mantener trazabilidad de cada análisis.
- Preparar índices básicos para búsquedas por fecha, id o estado.

---

## 5. Kafka + Zookeeper
Kafka debe actuar como sistema de mensajería/eventos para desacoplar operaciones internas.

### Uso recomendado en este proyecto
Kafka no debe bloquear la primera versión funcional.
Debe integrarse después de tener el flujo principal funcionando.

### Eventos posibles
- imagen subida,
- análisis solicitado,
- análisis completado,
- análisis fallido,
- registro técnico de ejecución.

### Objetivo arquitectónico
Desacoplar ciertos procesos internos del flujo principal para facilitar:
- trazabilidad,
- extensibilidad,
- integración con otros componentes,
- analítica de eventos.

### Zookeeper
Se usará como componente de soporte del ecosistema Kafka, si la versión/stack elegida lo requiere.

### Importante
Kafka no debe complicar el MVP.
La primera versión puede funcionar de forma síncrona y más adelante publicar eventos.

---

## 6. Node-RED
Node-RED se utilizará como herramienta auxiliar de orquestación y automatización.

### Uso previsto
- pruebas de integración,
- canalización de eventos,
- automatización de algunos flujos,
- experimentación con procesos internos.

### Rol
Node-RED no es el núcleo del backend.
Es una capa de apoyo, no la lógica principal del sistema.

### Recomendación
Implementarlo después del flujo principal y después de tener eventos claros.

---

## 7. Logstash + Elasticsearch + Kibana
Esta parte se utilizará para observabilidad y análisis técnico.

## Logstash
Responsable de recoger y transformar logs y eventos.

## Elasticsearch
Responsable de indexar logs y eventos para consulta.

## Kibana
Responsable de visualización técnica:
- errores,
- actividad del sistema,
- tiempos de procesamiento,
- eventos de análisis.

### Qué logs interesan
- inicio del servicio,
- carga del modelo,
- subida de imagen,
- inicio de inferencia,
- resultado de inferencia,
- errores,
- tiempos de respuesta,
- estado de conexión a MongoDB,
- publicación de eventos.

### Importante
Esto también es secundario respecto al flujo principal.
Primero funcionalidad, luego observabilidad avanzada.

---

## 8. Docker
Toda la arquitectura debe ser desplegable con Docker.

### Objetivo
Tener un entorno reproducible, homogéneo y fácil de levantar para:
- desarrollo,
- pruebas,
- demo final.

### Deben estar dockerizados, idealmente:
- backend Python,
- MongoDB,
- GraphQL service si va separado,
- Kafka,
- Zookeeper,
- Node-RED,
- Elasticsearch,
- Kibana.

### Requisito
Debe existir una configuración clara basada en `docker-compose.yml` o estructura equivalente.

### Prioridad
No empezar por Docker complejo si aún no existe backend funcional.
Primero que el backend corra localmente.
Luego se dockeriza bien.

---

# Arquitectura lógica del backend

El backend debe diseñarse por capas, evitando mezclar responsabilidades.

## Estructura conceptual recomendada

### 1. API layer
Responsable de:
- exponer GraphQL,
- validar entradas,
- devolver respuestas consistentes.

### 2. Service layer
Responsable de:
- coordinar subida,
- lanzar inferencia,
- persistir resultados,
- gestionar casos de uso.

### 3. Inference layer
Responsable de:
- cargar modelo,
- procesar imagen,
- ejecutar YOLO,
- normalizar resultados.

### 4. Repository / data access layer
Responsable de:
- guardar y consultar MongoDB.

### 5. Event layer
Responsable de:
- publicar eventos en Kafka cuando corresponda.

### 6. Logging / monitoring layer
Responsable de:
- registrar actividad técnica y errores.

### 7. Config layer
Responsable de:
- variables de entorno,
- rutas,
- conexiones,
- toggles de features.

---

# Objetivos técnicos detallados del backend

## Objetivo 1: recepción de archivos
Implementar la lógica para recibir radiografías desde frontend.

### Debe permitir:
- validar tipo de archivo,
- validar tamaño máximo,
- generar identificador del análisis,
- almacenar temporalmente o persistir la imagen,
- devolver un estado inicial controlado.

## Objetivo 2: inferencia
Ejecutar el modelo entrenado sobre la imagen.

### Debe permitir:
- cargar modelo,
- ejecutar inferencia,
- capturar errores,
- medir tiempo de procesamiento,
- normalizar salida del modelo.

## Objetivo 3: persistencia
Guardar el análisis completo en MongoDB.

### Debe incluir:
- información del archivo,
- resultado estructurado,
- estado,
- tiempos,
- versión del modelo,
- posibles errores.

## Objetivo 4: exposición por GraphQL
Definir y exponer el contrato de acceso a datos.

### Debe incluir:
- mutation de subida/análisis,
- query de detalle,
- query de listado,
- query de estadísticas.

## Objetivo 5: trazabilidad
Preparar el backend para registrar de forma clara lo que ocurre.

### Debe registrar:
- inicio/fin de proceso,
- errores,
- tiempos,
- eventos relevantes.

## Objetivo 6: escalabilidad técnica
Dejar el código preparado para crecer sin rehacer todo.

### Esto implica:
- código modular,
- separación de responsabilidades,
- configuración desacoplada,
- servicios extensibles.

---

# Orden recomendado de implementación

## Fase 1. Base del proyecto
Implementar:
- estructura de carpetas,
- configuración,
- variables de entorno,
- arranque del backend,
- conexión a MongoDB,
- esqueleto GraphQL.

## Fase 2. Capa de inferencia
Implementar:
- servicio de carga del modelo,
- servicio de inferencia,
- normalizador de resultados,
- manejo de errores.

## Fase 3. Caso de uso principal
Implementar:
- recepción de imagen,
- análisis,
- persistencia,
- respuesta GraphQL.

## Fase 4. Consultas
Implementar:
- consulta por id,
- listado de análisis,
- filtros básicos,
- detalle completo.

## Fase 5. Endurecimiento del sistema
Implementar:
- validaciones,
- manejo de errores consistente,
- logs,
- pruebas,
- tiempos de ejecución.

## Fase 6. Infraestructura auxiliar
Implementar después:
- Kafka,
- Node-RED,
- ELK,
- Kibana,
- dockerización completa.

---

# Reglas de implementación importantes

## 1. No mezclar entrenamiento con inferencia
El backend de producción no entrena el modelo.
Solo lo carga y lo usa.

## 2. El contrato GraphQL manda
El frontend debe integrarse contra un schema estable.
No cambiar nombres de campos constantemente.

## 3. El flujo principal es prioritario
Antes de añadir Kafka, Kibana o automatizaciones, debe funcionar:
- subir imagen,
- analizar,
- guardar,
- devolver resultado.

## 4. Pensar en errores desde el principio
Casos a contemplar:
- archivo inválido,
- imagen corrupta,
- fallo al cargar modelo,
- fallo de inferencia,
- error de base de datos,
- timeout,
- respuesta incompleta.

## 5. Mantener salida interna normalizada
No exponer directamente al frontend estructuras crudas del modelo YOLO.
Crear un formato propio y estable.

## 6. Preparar todo para Docker
Aunque el arranque inicial sea local, el diseño debe facilitar la contenerización posterior.

---

# Qué debe poder hacer el backend al terminar la primera versión útil

La primera versión útil del backend debe poder:

- arrancar correctamente,
- conectarse a MongoDB,
- cargar el modelo entrenado,
- recibir una radiografía,
- ejecutar inferencia,
- normalizar el resultado,
- guardar el análisis,
- exponerlo por GraphQL,
- permitir consultar análisis previos.

Si eso funciona, el backend ya cumple el objetivo principal.

---

# Qué no debe hacerse al principio

No empezar por:
- Kafka complejo,
- Node-RED avanzado,
- dashboards,
- observabilidad excesiva,
- optimizaciones prematuras,
- refactors grandes sin flujo funcional ya hecho.

Primero funcionalidad core. Luego extras.

---

# Resultado esperado final del backend

Se espera un backend modular, claro y mantenible que actúe como núcleo de procesamiento del proyecto, integrando IA, persistencia y comunicación con frontend, y que además deje preparada la base para incorporar mensajería, observabilidad e infraestructura reproducible.

La meta no es solo "hacer que funcione", sino dejar una base técnica defendible, ordenada y coherente para un proyecto final.

---

# Instrucción para Copilot

Ayúdame a construir este backend paso a paso respetando estas reglas:

1. priorizar primero el flujo completo funcional de subida -> inferencia -> guardado -> respuesta,
2. mantener una arquitectura limpia por capas,
3. usar Python como núcleo del backend,
4. integrar el modelo YOLO ya entrenado mediante Ultralytics,
5. exponer la funcionalidad mediante GraphQL,
6. persistir resultados en MongoDB,
7. dejar preparado el sistema para eventos, logs y despliegue con Docker,
8. no introducir complejidad secundaria antes de tener el flujo principal funcionando,
9. generar código completo, no pseudocódigo,
10. proponer estructura de carpetas, archivos, clases y funciones de forma coherente.

Quiero que cualquier propuesta de implementación siga esta visión técnica y este orden de prioridades.