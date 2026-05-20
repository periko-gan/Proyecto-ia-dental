# 🦷 Proyecto IA Dental

![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-FF1493?style=for-the-badge&logo=yolo&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

## 📌 Descripción General

**Proyecto IA Dental** es una plataforma web integral impulsada por Inteligencia Artificial diseñada para asistir a odontólogos y especialistas en el análisis, diagnóstico y seguimiento de radiografías dentales.

A través de un modelo de visión artificial entrenado específicamente (basado en **YOLOv8**), la aplicación procesa radiografías subidas por el usuario, detectando automáticamente problemas y patologías dentales (como caries, sarro/cálculo, lesiones periapicales, etc.). 

El sistema proporciona una interfaz visual altamente interactiva para ver los resultados, incluyendo niveles de confianza de la IA, cajas delimitadoras (bounding boxes) sobre la imagen, un panel de estadísticas y un "Score" general de la salud dental del paciente.

---

## 🚀 Características Principales

* **Autenticación de Usuarios:** Sistema seguro de registro e inicio de sesión para que los especialistas guarden sus historiales médicos.
* **Diagnóstico Automatizado (IA):** Subida de radiografías en varios formatos e inferencia instantánea utilizando redes neuronales profundas (YOLOv8).
* **Visor Interactivo de Radiografías:** Visualización enriquecida con *bounding boxes* dinámicos que se pueden ocultar, mostrar o filtrar según el tipo de patología y el nivel de confianza de la IA.
* **Dashboard Analítico:** Panel de control (Dashboard) que resume los diagnósticos previos del usuario, muestra una puntuación de salud (Health Score) y gráficas de los tipos de problemas más frecuentes.
* **Historial Clínico:** Registro de todos los análisis realizados, permitiendo al usuario revisar diagnósticos anteriores, compararlos y mantener un control a lo largo del tiempo.

---

## 🏗️ Arquitectura del Sistema

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

## 🛠️ Requisitos Previos

Asegúrate de tener instalados en tu sistema local los siguientes programas:
* [Node.js](https://nodejs.org/) y [pnpm](https://pnpm.io/) (para el Frontend).
* [Python 3.10+](https://www.python.org/) y `pip` (para el Backend).
* [Docker](https://www.docker.com/) y Docker Compose (para bases de datos e infraestructura).

---

## ⚙️ Cómo iniciar la aplicación

El proyecto incluye scripts interactivos que automatizan el levantamiento y cierre de todos los componentes de la aplicación (Frontend, Backend, Bases de Datos).

### 🪟 En Windows (PowerShell)

Abre PowerShell en la raíz del proyecto y ejecuta:
```powershell
.\start_aplicacion.ps1
```
*Se desplegará un menú en la terminal donde podrás elegir la opción `5. Levantar TODO` para iniciar Docker, FastAPI y Vite de forma automática.*

### 🐧 En Linux / macOS (Bash)

Abre la terminal en la raíz del proyecto y ejecuta:
```bash
./start_aplicaion.sh
```
*Al igual que en Windows, se mostrará un menú interactivo. Selecciona `5` para desplegar todos los servicios.*

### ¿Qué ocurre al iniciar la aplicación?
1. Se levantan los contenedores de **Docker** (MongoDB).
2. Se inicia el servidor **Backend (Uvicorn/FastAPI)** en el puerto local (`localhost:8000`).
3. Se inicia el entorno de desarrollo del **Frontend (Vite)**, el cual suele ejecutarse en `localhost:5173` u `8080`. Se abrirá automáticamente o te mostrará el enlace en la consola.

---

## 📁 Estructura de Directorios

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

## 🤝 Soporte y Cierre Seguro

Para detener la aplicación, simplemente vuelve al menú interactivo del script (`start_aplicacion.ps1` o `start_aplicaion.sh`) y selecciona la opción **10. Cerrar TODO**. Esto detendrá de forma segura los servidores y apagará los contenedores Docker, evitando que queden procesos huérfanos consumiendo memoria.
