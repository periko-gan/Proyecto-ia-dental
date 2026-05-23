# Memoria Técnica y Documentación de Infraestructura: Orquestación (Docker)

**Proyecto Final: Curso de Especialización en Inteligencia Artificial y Big Data (Formación Profesional)**

Este documento expone la arquitectura de infraestructura y orquestación de servicios periféricos del proyecto de Inteligencia Artificial Dental. Está redactado como una justificación técnica orientada a los estándares de la Ingeniería de Datos (Data Engineering), flujos de trabajo de streaming (Big Data) y despliegues robustos (MLOps).

---

## 1. Justificación de la Orquestación y Aislamiento (Docker Compose)

En un ecosistema moderno de IA y Big Data, la reproducibilidad del entorno es un requisito innegociable. La carpeta `docker/` y su manifiesto central `docker-compose.yml` garantizan que todos los servicios analíticos se levanten de forma determinista y predecible.

* **Aislamiento de Dependencias (DataOps)**: Al encapsular sistemas de bases de datos pesadas y brokers de mensajería en contenedores de Docker, se evita la "polución" del sistema operativo del desarrollador. Permite que el entorno de experimentación sea un reflejo idéntico del entorno productivo en servidores Linux.
* **Redes Virtuales Definidas por Software**: El despliegue genera automáticamente una red interna (Red Bridge `ia_dental_net`). Esto previene colisiones de puertos con servicios locales y blinda el clúster: el tráfico masivo interno (por ejemplo, la ingesta entre Logstash y Elasticsearch) viaja a través de un DNS interno resuelto por Docker y nunca se expone a la tarjeta de red pública del anfitrión.
* **Persistencia Inyectada (Bind Mounts)**: El directorio local `data/` actúa como puente de persistencia. Esto no solo salva el estado transaccional y los índices ante reinicios del orquestador, sino que facilita drásticamente la realización de copias de seguridad (Backups) regulares y la inyección en caliente de configuraciones analíticas.

---

## 2. Subsistema de Ingesta y Streaming (Apache Kafka)

Como núcleo del paradigma arquitectónico orientado a eventos (Event-Driven Architecture), el sistema prescinde de llamadas cruzadas síncronas entre los servicios de Inteligencia de Negocio y la API del servidor, optando por Apache Kafka como bus de mensajería asíncrona masiva.

* **Justificación de Elección (Big Data)**: A diferencia de los sistemas tradicionales como RabbitMQ, Kafka está diseñado fundamentalmente para ingestas a escala Big Data. Su modelo de *Append-Only Log* (registro secuencial) garantiza una altísima velocidad de escritura sostenida (Throughput) y permite que múltiples consumidores analíticos lean los mismos eventos clínicos simultáneamente sin consumir el mensaje original, permitiendo la reconstrucción de datos históricos (Replay) para el reentrenamiento de la red neuronal.
* **Zookeeper (Coordinador del Clúster)**: Ejerce el rol de gobernador distribuido. Se encarga de la gestión estricta de metadatos, control de liderazgo de particiones y sincronización ante fallos de nodos dentro de Kafka.
* **Recuperación Ante Desastres (`recover-kafka-zk.sh/ps1`)**: Los cortes bruscos de los contenedores locales pueden desincronizar los identificadores transaccionales entre Kafka y Zookeeper (`Invalid cluster.id`). Se han programado scripts Bash y PowerShell específicos para automatizar la purga y el restablecimiento del quórum. Esto asegura la resiliencia operativa en el desarrollo local sin obligar al desarrollador a depurar volúmenes corruptos a mano.
* **Kafka UI**: Consola de gestión incorporada para permitir a los ingenieros de datos auditar en tiempo real los tópicos (Topics), offsets de particiones y la correcta serialización de los eventos enviados.

---

## 3. Subsistema de Observabilidad y Analítica (Stack ELK)

La infraestructura despliega la triada ELK (Elasticsearch, Logstash, Kibana) para dominar el almacenamiento analítico columnar, la agregación de logs operacionales y la métrica del ecosistema clínico.

* **Logstash (Tuberías de Datos y ETL)**: Ejerce el rol de extractor y transformador de datos masivos. A través de las configuraciones montadas desde la carpeta persistente `data/logstash_pipeline/`, Logstash puede suscribirse a los tópicos de Kafka, aplicar filtros mutadores sobre las cadenas JSON (limpieza y enriquecimiento de datos clínicos) y empujar los eventos limpios hacia el repositorio final.
* **Elasticsearch (Búsqueda Analítica NoSQL)**: Actúa como el cerebro analítico distribuido. Su diseño subyacente basado en Apache Lucene le confiere una capacidad inigualable para búsquedas invertidas, indexación rápida y agregaciones estadísticas complejas. Es el repositorio ideal para cruzar miles de registros generados por YOLOv8 (coordenadas, patologías y probabilidades) e inferir conclusiones globales que serían demasiado costosas en bases de datos relacionales tradicionales.
* **Kibana (Visualización de Datos)**: Proporciona a los científicos de datos y analistas clínicos un entorno para crear de cuadros de mando interactivos (Dashboards). Permite la explotación de la métrica ingerida en Elasticsearch de forma puramente gráfica y dinámica.

---

## 4. Orquestación Auxiliar (Grafana y Node-RED)

Para complementar la solidez del MLOps de la inteligencia artificial predictiva, el ecosistema despliega herramientas modulares para alertas y telemetría de sistemas.

* **Grafana**: Posicionado como el visor maestro para el rendimiento de infraestructura y la salud técnica del modelo predictivo (Model Drift/Data Drift). Permite unificar fuentes heterogéneas, extrayendo métricas de la JVM de Kafka o tiempos de latencia del servidor backend, localizando cuellos de botella antes de que afecten al usuario final. Su almacén de reglas (normalmente SQLite) queda asegurado persistiendo en `data/grafana/`.
* **Node-RED**: Herramienta de programación visual basada en flujos de red. En contextos avanzados de Big Data y automatización o *Edge Computing*, se emplea como un "pegamento" ágil que facilita el levantamiento de APIs temporales de ingesta secundaria (por ejemplo, conectando sensores o bases de datos clínicas heredadas) para derivarlas velozmente hacia Kafka.

---

## 5. Balance de Cargas y Perfilado de Hardware

Al tratarse de un despliegue para desarrollo local dentro de un entorno de Formación Profesional, la orquestación en el manifiesto `docker-compose.yml` está diseñada siendo muy consciente de las limitaciones de hardware (caché, procesador y memoria RAM física):

* **Componentes Intensivos (Heavyweight)**: Los motores construidos sobre la Máquina Virtual de Java (JVM), como Elasticsearch, Logstash y Apache Kafka, representan el eslabón pesado de la infraestructura. Acaparan la mayor cuota de la caché en disco (Page Cache) requerida para lograr la ingestión masiva en escenarios reales.
* **Servicios Ligeros (Lightweight)**: Interfaces de control administrativo como Kafka UI, Kibana, Grafana o Node-RED mantienen perfiles de memoria contenidos. Esto garantiza que un ordenador convencional pueda sostener todo el clúster de Big Data de forma fluida junto a la pesada red neuronal de IA (que corre paralelamente en el backend) sin ahogar el sistema operativo anfitrión.
