# Proyecto IA Dental

## Tecnologías utilizadas

| Tecnología | Descripción |
| :--- | :--- |
| **Vue.js** | **Frontend**: Construcción de la interfaz de usuario interactiva y reactiva. |
| **FastAPI** | **Backend**: Servidor web principal que expone la API GraphQL. |
| **Python** | **Lenguaje principal**: Lógica de backend, procesamiento ETL de datos y ejecución del entrenamiento del modelo. |
| **YOLOv8** | **Inteligencia Artificial**: Red neuronal convolucional para la detección y localización de patologías dentales. |
| **MongoDB** | **Base de datos**: Almacenamiento no relacional y persistente para usuarios, diagnósticos e imágenes. |
| **Docker** | **Infraestructura**: Contenedorización para el levantamiento unificado de las bases de datos y microservicios. |
| **Tailwind CSS** | **Diseño**: Estilado moderno y responsivo de la interfaz de usuario. |

## Descripción general

**Proyecto IA Dental** es una plataforma web integral impulsada por Inteligencia Artificial diseñada para asistir a odontólogos y especialistas en el análisis, diagnóstico y seguimiento de radiografías dentales.

A través de un modelo de visión artificial entrenado específicamente (basado en **YOLOv8**), la aplicación procesa radiografías subidas por el usuario, detectando automáticamente problemas y patologías dentales (como caries, sarro/cálculo, lesiones periapicales, etc.). 

El sistema proporciona una interfaz visual altamente interactiva para ver los resultados, incluyendo niveles de confianza de la IA, cajas delimitadoras (bounding boxes) sobre la imagen, un panel de estadísticas y un "Score" general de la salud dental del paciente.

---

## Características principales

* **Autenticación de Usuarios:** Sistema seguro de registro e inicio de sesión para que los especialistas guarden sus historiales médicos.
* **Diagnóstico Automatizado (IA):** Subida de radiografías en varios formatos e inferencia instantánea utilizando redes neuronales profundas (YOLOv8).
* **Visor Interactivo de Radiografías:** Visualización enriquecida con *bounding boxes* dinámicos que se pueden ocultar, mostrar o filtrar según el tipo de patología y el nivel de confianza de la IA.
* **Dashboard Analítico:** Panel de control (Dashboard) que resume los diagnósticos previos del usuario, muestra una puntuación de salud (Health Score) y gráficas de los tipos de problemas más frecuentes.
* **Historial Clínico:** Registro de todos los análisis realizados, permitiendo al usuario revisar diagnósticos anteriores, compararlos y mantener un control a lo largo del tiempo.

---

## Arquitectura del sistema

El proyecto está dividido en varios microservicios y capas principales:

1. **Frontend (`/frontend`)**: 
   * Construido con **Vue 3** y **Vite**.
   * Estilizado con **Tailwind CSS**.
   * Se encarga de toda la interfaz de usuario, gestión del estado, peticiones GraphQL y renderizado de cajas delimitadoras (bounding boxes) sobre las imágenes usando coordenadas proporcionales.

2. **Backend (`/backend`)**:
   * Construido con **Python** y **FastAPI**.
   * Servidor **Uvicorn**.
   * Expone una API GraphQL (o REST) que gestiona la autenticación, recibe las imágenes en Base64, invoca al modelo de inteligencia artificial y guarda los resultados en la base de datos.

3. **Modelo de IA (`/entrenamiento ia`)**:
   * Utiliza modelos de detección de objetos **YOLOv8**.
   * Las imágenes enviadas se analizan en tiempo real para predecir las patologías dentales, devolviendo las coordenadas exactas y un índice de confianza.

4. **Base de Datos y Servicios (Docker)**:
   * **MongoDB**: Almacena de forma persistente los usuarios, las imágenes y el historial de diagnósticos (corriendo mediante Docker Compose).
   * Contenedores adicionales gestionados desde la carpeta `/docker` para un entorno escalable y aislado.

---

## Requisitos previos

Asegúrate de tener instalados en tu sistema local los siguientes programas:
* [Node.js](https://nodejs.org/) y [pnpm](https://pnpm.io/) (para el Frontend).
* [Python 3.10+](https://www.python.org/) y `pip` (para el Backend).
* [Docker](https://www.docker.com/) y Docker Compose (para bases de datos e infraestructura).

---

## Cómo iniciar la aplicación

El proyecto se puede iniciar de forma automática a través de scripts interactivos o de forma manual paso a paso.

### Inicio automático (Recomendado)

El proyecto incluye scripts interactivos que automatizan el levantamiento y cierre de todos los componentes de la aplicación (Frontend, Backend, Bases de Datos).

#### En Windows (PowerShell)

Abre PowerShell en la raíz del proyecto y ejecuta:
```powershell
.\start_aplicacion.ps1
```
*Se desplegará un menú en la terminal donde podrás elegir la opción `5. Levantar TODO` para iniciar Docker, FastAPI y Vite de forma automática.*

#### En Linux / macOS (Bash)

Abre la terminal en la raíz del proyecto y ejecuta:
```bash
./start_aplicaion.sh
```
*Al igual que en Windows, se mostrará un menú interactivo. Selecciona `5` para desplegar todos los servicios.*

### Inicio manual paso a paso

Si prefieres levantar cada servicio de forma individual y manual, abre diferentes terminales y sigue estos pasos:

#### 1. Base de Datos (MongoDB)
El backend requiere una instancia de MongoDB. Puedes levantar el contenedor Docker de las siguientes maneras:
- **MongoDB básico**:
  ```bash
  cd backend
  docker compose -f docker-compose.mongo.yml up -d
  ```
- **Contenedores completos (MongoDB, Kafka, Zookeeper)**:
  ```bash
  cd docker
  docker compose up -d
  ```

#### 2. Servidor Backend (FastAPI)
1. Ve al directorio del backend:
   ```bash
   cd backend
   ```
2. Crea y activa el entorno virtual de Python:
   - **En Windows**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **En Linux / macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Instala las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```
4. Copia el archivo `.env.example` a `.env` (si aún no lo has hecho) y arranca el servidor:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   *El backend estará escuchando en `http://localhost:8000`.*

#### 3. Aplicación Frontend (Vue 3 / Vite)
1. Ve al directorio del frontend:
   ```bash
   cd frontend
   ```
2. Crea el archivo de variables de entorno `.env` en `frontend/` apuntando al endpoint de GraphQL del backend:
   ```env
   VITE_GRAPHQL_ENDPOINT=http://localhost:8000/graphql
   ```
3. Instala las dependencias del proyecto usando `pnpm` (evita `npm` o `yarn` para prevenir conflictos de lockfile):
   ```bash
   pnpm install
   ```
4. Inicia el servidor de desarrollo:
   ```bash
   pnpm run dev
   ```
   *(Alternativamente, puedes ejecutar `pnpm install` y `pnpm dev` directamente desde la raíz del proyecto gracias a la configuración de workspaces de `pnpm`).*
   
   *El frontend estará disponible en `http://localhost:5173`.*


---

## Estructura de directorios

```text
Proyecto-ia-dental/
├── backend/                # Servidor FastAPI, lógica de negocio y ejecución modelo IA
├── frontend/               # Aplicación web en Vue.js + Vite + TailwindCSS
├── docker/                 # Archivos de configuración general para contenedores
├── entrenamiento ia/       # Scripts, datasets y pesos (weights) del modelo YOLOv8
├── capturas/               # Imágenes y demostraciones para la documentación
├── start_aplicacion.ps1    # Script lanzador interactivo para Windows
└── start_aplicaion.sh      # Script lanzador interactivo para Linux/macOS
```

---

## Soporte y cierre seguro

Para detener la aplicación, simplemente vuelve al menú interactivo del script (`start_aplicacion.ps1` o `start_aplicaion.sh`) y selecciona la opción **10. Cerrar TODO**. Esto detendrá de forma segura los servidores y apagará los contenedores Docker, evitando que queden procesos huérfanos consumiendo memoria.
