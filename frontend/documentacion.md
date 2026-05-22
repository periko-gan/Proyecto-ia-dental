# Documentación de la aplicación frontend - Portal de IA Dental

Este documento proporciona una descripción técnica, funcional y de arquitectura de la interfaz web (frontend) correspondiente al sistema de análisis radiográfico dental mediante inteligencia artificial. El portal está diseñado para el uso de clínicos y estudiantes, ofreciendo un flujo de diagnóstico rápido, seguro y adaptable.

---

## 1. Stack tecnológico y justificación

La selección de tecnologías del frontend responde a necesidades de agilidad, responsividad y modularidad necesarias para un entorno de análisis médico:

* **Vue 3 (Composition API)**: Framework principal para estructurar componentes interactivos y reactivos. La Composition API y el uso de composables permiten desacoplar la lógica de estado de los componentes visuales de presentación.
* **Vite**: Motor de compilación y servidor de desarrollo ágil que provee reemplazo de módulos en caliente (HMR), acelerando significativamente el desarrollo y optimizando el empaquetado para producción.
* **Pinia**: Biblioteca de gestión de estado global utilizada para centralizar la autenticación, datos del usuario activo e información de sesión.
* **Vue Router**: Motor de enrutamiento del lado del cliente (SPA) para mapear rutas públicas y protegidas mediante guards de navegación de seguridad.
* **Apollo Client + GraphQL**: Cliente de consultas de datos. Permite solicitar al backend únicamente la información requerida, estructurando operaciones mediante consultas y mutaciones autotipadas en escala.
* **Tailwind CSS v4 + daisyUI**: Framework de diseño y biblioteca de componentes CSS basado en utilidades que asegura una visualización moderna, consistente y responsiva con el mínimo tamaño de archivo CSS final.

---

## 2. Estructura de directorios y organización de código

El código de la aplicación se encuentra organizado bajo la carpeta [src](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src) según el siguiente mapa de directorios:

* **main.js**: Punto de entrada de la aplicación Vue. Registra los componentes globales, inicializa Pinia, el enrutador y levanta el renderizado de la interfaz.
* **App.vue**: Componente raíz contenedor que incluye las plantillas principales de visualización y el sistema de vistas dinámicas.
* **style.css**: Configuración central de estilos. Importa las directivas base de Tailwind CSS y el plugin de daisyUI.
* **components**: Contiene las vistas principales del portal y elementos de interfaz:
  * **LandingView.vue**: Página de presentación inicial del proyecto con descripción de capacidades.
  * **LoginView.vue**: Formulario de inicio de sesión clínica.
  * **RegisterView.vue**: Formulario de registro de nuevos especialistas clínicos.
  * **DashboardView.vue**: Panel principal que organiza y expone métricas agregadas del historial clínico del usuario.
  * **AnalyzeView.vue**: Panel interactivo para cargar radiografías y renderizar los diagnósticos devueltos por el backend.
  * **DiagnosticView.vue**: Vista en detalle de un informe clínico de diagnóstico específico.
  * **parts**: Componentes específicos divididos por funcionalidad:
    * **all_pages**: Estructuras globales reutilizables como la barra lateral de navegación (Aside.vue), cabeceras con menús de usuario (Header.vue) y pie de página (Footer.vue).
    * **dashboard**: Contenedores visuales para el panel principal, como el indicador de salud dental (HealthScoreHero.vue), tarjetas de últimas radiografías (LatestDiagnosisSummary.vue), gráficos de patologías (ProblemTypesChart.vue) y listado global paginado (AllDiagnostics.vue).
    * **diagnostic**: Bloques especializados de inspección como la lista de problemas detectados (DentalProblems.vue) y el lienzo dinámico con la radiografía superpuesta con las detecciones (ImageAnalyzed.vue).
    * **login_register**: Elemento del formulario de autenticación compartida (Formulario.vue).
    * **upload_images**: Caja interactiva de arrastre y carga de archivos (UploadImages.vue).
* **composables**: Capa lógica encargada de encapsular el estado reactivo, cálculo de variables y llamadas a servicios. Evita que la interfaz contenga lógica de negocio pesada.
* **config**: Contiene la configuración global de endpoints (graphql.js).
* **services**: Servicios de bajo nivel que manejan las llamadas a API GraphQL, base de datos local del navegador e IndexedDB.
* **utils**: Funciones auxiliares y formateadores globales (como problemTranslations.js).

---

## 3. Rutas y componentes asociados

El enrutamiento de la aplicación SPA se define en el archivo [router/index.js](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/router/index.js) y mapea las siguientes vistas principales:

### Ruta `/` (Pública) - Landing de inicio
* **Propósito**: Actúa como portal de presentación pública del proyecto clínico. Detalla la propuesta de valor del sistema, la precisión de la IA, el flujo de trabajo sugerido y testimonios profesionales, además de proveer los accesos directos hacia el flujo de inicio de sesión o registro.
* **Vista principal**: [LandingView.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/LandingView.vue)
* **Componentes que la integran**:
  * [Header.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Header.vue): Cabecera de navegación pública.
  * [Footer.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Footer.vue): Pie de página técnico básico con enlaces de interés.

### Ruta `/login` (Pública) - Inicio de sesión
* **Propósito**: Punto de acceso obligatorio para que los clínicos y estudiantes registrados puedan autenticarse con sus credenciales (correo electrónico y contraseña).
* **Vista principal**: [LoginView.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/LoginView.vue)
* **Componentes que la integran**:
  * [Header.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Header.vue): Cabecera global de navegación.
  * [Formulario.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/login_register/Formulario.vue): Configurado para el modo de inicio de sesión (propiedad page="login"). Gestiona la entrada de datos, realiza la validación de formato y efectúa la autenticación llamando a la API GraphQL.
  * [Footer.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Footer.vue): Pie de página de cierre.

### Ruta `/register` (Pública) - Registro de clínicos
* **Propósito**: Permite el auto-registro en el sistema para nuevos profesionales sanitarios.
* **Vista principal**: [RegisterView.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/RegisterView.vue)
* **Componentes que la integran**:
  * [Header.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Header.vue): Cabecera global de navegación.
  * [Formulario.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/login_register/Formulario.vue): Configurado en modo de registro (propiedad page="register"). Habilita campos adicionales de datos personales (nombre completo), valida la fortaleza de contraseña y ejecuta la mutación GraphQL para crear la cuenta e iniciar sesión automáticamente.
  * [Footer.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Footer.vue): Pie de página de cierre.

### Ruta `/dashboard` (Protegida) - Panel Principal de Gestión
* **Propósito**: Ofrece al especialista autenticado una vista consolidada de su actividad clínica, con métricas globales de salud de sus análisis y el listado de diagnósticos realizados.
* **Vista principal**: [DashboardView.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/DashboardView.vue)
* **Componentes de layout**:
  * [Aside.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Aside.vue): Barra lateral izquierda persistente para navegación entre las distintas secciones de la aplicación.
  * [Footer.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Footer.vue): Pie de página de cierre.
* **Componentes de contenido**:
  * [HealthScoreHero.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/dashboard/HealthScoreHero.vue): Widget con un indicador circular que calcula el promedio de salud dental del historial de radiografías.
  * [LatestDiagnosisSummary.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/dashboard/LatestDiagnosisSummary.vue): Tarjeta informativa que resume los hallazgos clínicos del último diagnóstico realizado.
  * [ProblemTypesChart.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/dashboard/ProblemTypesChart.vue): Gráfica de barras que muestra la distribución agregada por tipologías patológicas detectadas por la IA.
  * [AllDiagnostics.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/dashboard/AllDiagnostics.vue): Tabla del historial clínico con paginación interactiva, listando todos los análisis realizados por el usuario activo con acceso directo a sus informes.

### Ruta `/analyze` (Protegida) - Carga y análisis clínico
* **Propósito**: Espacio de carga de imágenes clínicas. El profesional sube los archivos y el sistema realiza las validaciones, enviándolos al motor de IA a través de GraphQL. Tras un procesamiento exitoso, el flujo redirige automáticamente al informe de diagnóstico resultante.
* **Vista principal**: [AnalyzeView.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/AnalyzeView.vue)
* **Componentes de layout**:
  * [Aside.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Aside.vue): Barra lateral izquierda persistente de navegación.
  * [Footer.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Footer.vue): Pie de página de cierre.
* **Componentes de contenido**:
  * [UploadImages.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/upload_images/UploadImages.vue): Zona de arrastre e interacción ("drag and drop") para encolar una imagen, realizar la lectura en Base64, ejecutar la mutación asíncrona de subida contra el backend y, una vez recibidos los datos del diagnóstico de la IA, guardar los datos en el estado global para transferir el control a la pantalla de informe.

### Ruta `/diagnostic` (Protegida) - Informe de diagnóstico detallado
* **Propósito**: Visualización a pantalla completa del informe de diagnóstico devuelto por la IA. Permite inspeccionar la radiografía con las cajas delimitadoras y consultar las patologías clasificadas.
* **Vista principal**: [DiagnosticView.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/DiagnosticView.vue)
* **Componentes de layout**:
  * [Aside.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Aside.vue): Barra lateral izquierda de navegación.
  * [Footer.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/all_pages/Footer.vue): Pie de página de cierre.
* **Componentes de contenido**:
  * [ImageAnalyzed.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/diagnostic/ImageAnalyzed.vue): Módulo visual interactivo que carga la placa dental y dibuja dinámicamente sobre ella las cajas delimitadoras (bounding boxes) con los colores asociados a su nivel de severidad.
  * [DentalProblems.vue](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/components/parts/diagnostic/DentalProblems.vue): Listado tabular estructurado de los problemas y hallazgos específicos del diagnóstico (caries, implantes, etc.), agrupándolos por niveles de riesgo clínicos (Crítico, Seguimiento y Óptimo).

---

## 4. Arquitectura basada en composables

Para cumplir con principios de responsabilidad única y alta mantenibilidad, cada componente de presentación delega su lógica en un archivo composable correspondiente en [composables](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/composables):

* **useAuthForm.js**: Controla la reactividad de los formularios de acceso y registro, validaciones de formato de email, longitud de contraseñas y llamadas a peticiones asíncronas de registro y login.
* **useAside.js**: Gestiona el comportamiento de colapso, navegación activa y despliegue del menú lateral del portal clínico.
* **useMyAnalyses.js**: Controla el estado asíncrono para cargar el historial de análisis radiológicos desde el backend utilizando paginación.
* **useLatestDiagnosisSummary.js**: Filtra y formatea los datos de la última radiografía completada por el paciente, calculando la confianza y seleccionando la miniatura de visualización.
* **useHealthScoreHero.js**: Calcula el promedio ponderado de confianza del total de diagnósticos del clínico y clasifica la severidad acumulada (Óptimo, Seguimiento, Crítico).
* **useProblemTypesChart.js**: Procesa las etiquetas de detección arrojadas por la IA para agruparlas por categorías patológicas (Caries, Empastes, Implantes, Dientes impactados) y estructurar gráficos de distribución porcentual.
* **useUploadImagesQueue.js**: Administra la cola de archivos seleccionados por el clínico para subir al backend. Procesa la conversión asíncrona a formato base64, llamadas secuenciales a la mutación de red y reintentos locales.
* **useDiagnosticAnalysis.js**: Recupera y distribuye los datos detallados de un análisis específico para renderizar la vista de informe.
* **useDentalProblems.js**: Formatea y ordena los problemas detectados en una radiografía para su listado tabular estructurado por severidad diagnóstica.
* **useImageAnalyzed.js**: Expone la lógica para calcular las posiciones proporcionales de las cajas delimitadoras de las patologías (bounding boxes) y dibujarlas dinámicamente en un canvas o contenedor superpuesto sobre la radiografía dental a diferentes resoluciones de pantalla.

---

## 5. Flujo de autenticación, seguridad y persistencia de sesión

La seguridad de las rutas clínicas se gestiona mediante tokens JWT y persistencia en el almacenamiento web del navegador web:

### Registro y login unificado
* Durante el registro, el sistema invoca la mutación `RegisterAndLogin` que genera el usuario en base de datos y automáticamente inicia sesión.
* En el login normal, el usuario ingresa sus credenciales en `LoginView` y se ejecuta la mutación `LoginUser` contra el endpoint GraphQL.
* Si el inicio de sesión es correcto y el usuario se encuentra activo, se ejecuta la persistencia mediante el servicio asíncrono [authService.js](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/services/authService.js).

### Persistencia granular en sessionStorage
Para evitar tener que parsear continuamente payloads complejos y asegurar que la sesión expire inmediatamente cuando el profesional cierra la pestaña o navegador por motivos de seguridad médica, se guardan los siguientes cinco campos planos en `sessionStorage`:

* **accessToken**: Token JWT Bearer enviado en la cabecera `Authorization` de todas las peticiones posteriores.
* **userId**: Identificador universal único de la base de datos del usuario.
* **name**: Nombre registrado del clínico.
* **email**: Dirección de correo electrónico del usuario.
* **isActive**: Booleano que define si el perfil clínico tiene permisos de operación activos.
* **role**: Nivel de rol del usuario (por ejemplo, USER o ADMIN).

### Guards de navegación del router
En el enrutador [router/index.js](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/router/index.js), se ejecuta un hook de control antes de cada transición de ruta (`router.beforeEach`):

* **Rutas que requieren autenticación**: `/dashboard`, `/analyze`, `/diagnostic`. Si no se detecta la existencia de un `accessToken` válido en el almacenamiento web, el sistema intercepta el flujo y redirige al usuario a `/login`.
* **Redirección de usuario autenticado**: Si un usuario con sesión activa intenta forzar la navegación hacia `/login` o `/register`, el enrutador lo redirige automáticamente hacia `/dashboard` para evitar redundancias de inicio de sesión.
* **Logout**: La función `logout()` remueve individualmente cada una de las claves de sesión en `sessionStorage`, restableciendo el estado de la aplicación antes de redirigir a la vista de aterrizaje.

---

## 6. Diseño adaptativo y responsivo

El panel clínico ha sido diseñado siguiendo un enfoque de priorización móvil y adaptabilidad en tres niveles soportado por utilidades nativas de Tailwind CSS:

* **Dispositivos móviles** (pantallas inferiores a 768px): La interfaz apila verticalmente todos los bloques de información y componentes de análisis para facilitar la interacción táctil en smartphones o tablets pequeñas.
* **Dispositivos tablet** (pantallas entre 768px y 1024px): Distribución optimizada en dos columnas de ancho similar, dividiendo la carga de archivos o listados de la visualización resumida.
* **Dispositivos desktop** (pantallas superiores a 1024px): Distribución espacial avanzada en tres columnas que optimiza la carga de información. Integra de manera simultánea la navegación lateral colapsable, el indicador de rendimiento y el feed dinámico de radiografías recientes.

---

## 7. Persistencia y almacenamiento local (IndexedDB)

La aplicación implementa dos bases de datos locales no relacionales en el navegador web del usuario a través de la API nativa de IndexedDB para asegurar un flujo de trabajo tolerante a desconexiones de red:

### Base de datos local de imágenes (DentalAI-Images)
Definida y expuesta a través del servicio [imageStorageService.js](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/services/imageStorageService.js). Cumple las siguientes especificaciones:
* **Almacén (Store)**: `radiographs`.
* **Propósitos**: Almacena las imágenes radiográficas junto con su representación base64 y metadatos completos asociados de forma local. Permite acelerar los tiempos de visualización de placas repetidas en la interfaz, auditar los archivos cargados y admitir la descarga directa de imágenes locales.
* **Estructura del registro**: Cada entrada contiene un ID auto-generado, `fileName`, `mimeType`, `fileSize`, `base64`, metadatos detallados y fechas de creación y actualización del archivo.

### Cola local de carga (dental-ai-upload-queue)
Gestionada mediante el módulo [uploadQueueDb.js](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/services/uploadQueueDb.js). Cumple con las siguientes especificaciones:
* **Almacén (Store)**: `files`.
* **Propósito**: Actúa como un búfer temporal local (upload queue) de archivos listos para enviar al backend. Si un usuario se queda sin conexión durante la subida, los archivos se mantienen en cola para reintentarse en cuanto se restablezca el enlace a la API GraphQL.
* **Operaciones**: Soporta la carga clasificada por fecha de encolado, reemplazo total y vaciado de registros mediante promesas asíncronas sobre transacciones de lectura/escritura.

---

## 8. Cliente de comunicaciones GraphQL y carga de archivos

La interacción cliente-servidor se consolida en una arquitectura ligera y centralizada de red asíncrona:

### Cliente unificado de operaciones (graphqlClient.js)
El servicio [graphqlClient.js](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/services/graphqlClient.js) implementa la función `postGraphQL` que realiza llamadas HTTP POST directas usando la API nativa `fetch` del navegador:
* **Inyección de token**: Recupera de manera automática el `accessToken` activo y, si existe, añade la cabecera `Authorization: Bearer <token>` a la petición.
* **Trazas y diagnóstico**: Escribe en la consola del desarrollador los detalles estructurados de la solicitud (Endpoint, Query enviada, variables) y de la respuesta (Código HTTP, latencia en milisegundos y formato de payload devuelto) para agilizar las tareas de auditoría de red.
* **Validación de errores**: Captura de forma jerárquica errores de red HTTP (códigos fuera de rango 2xx) y excepciones GraphQL internas (array de errores devuelto por la especificación GraphQL), traduciendo los fallos al hilo principal.

### Carga de placas a través de mutación GraphQL (uploadRadiographyService.js)
Dado que las radiografías dentales se procesan en base de datos como registros y archivos asociados, el portal implementa la mutación asíncrona `UploadRadiography`:
* **Carga por base64**: La imagen de la radiografía dental es leída localmente por el navegador como un Blob asíncrono y codificada a string Base64.
* **Mutación**: Envía el archivo cifrado en base64, el nombre original del archivo y su tipo MIME correspondiente a la mutación `uploadRadiography`.
* **Retorno**: Si el backend procesa con éxito la imagen mediante la IA, el frontend recibe un mensaje confirmatorio y un objeto estructurado del tipo `analysis` con todas las detecciones patológicas calculadas, coordenadas de caja y tiempos de inferencia técnica para su renderizado inmediato.

---

## 9. Normalización y traducción de patologías dentales

Para tender un puente comprensible entre los nombres de clases crudos devueltos por el modelo de IA de detección YOLOv8 (en inglés) y la visualización médica en español, se diseñó el módulo de traducción estructurado [problemTranslations.js](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/src/utils/problemTranslations.js):

### Mapeo de patologías y normalización
La función `translateProblem` realiza una normalización avanzada de la etiqueta de la IA (limpieza de espacios, minúsculas, eliminación de porcentajes de acierto numéricos y acentos problemáticos) para luego cruzarlo contra un mapa léxico:
* `cavity` es traducido a **Caries**.
* `filling` es traducido a **Empaste**.
* `implant` es traducido a **Implante**.
* `impacted` es traducido a **Diente impactado**.

### Niveles de severidad y clasificación por colores
El módulo asigna a cada tipo de problema una etiqueta de severidad de DaisyUI y colores hexadecimales precisos para el dibujado sobre el canvas:

* **Severidad crítica** (`critical` / Color DaisyUI: `error` / Hexadecimal: `#EF4444`): Asignada a caries (`cavity`), abscesos dentales (`abscess`), caries profundas (`decay`) y fracturas. Denota atención dental inmediata prioritaria.
* **Severidad de seguimiento** (`warning` / Color DaisyUI: `warning` o `primary` / Hexadecimal: `#F59E0B` o `#8B5CF6`): Asignada a empastes (`filling`), sarro (`tartar`), placa bacteriana (`plaque`), inflamaciones gingivales y dientes impactados (`impacted`). Denota monitoreo.
* **Severidad óptima** (`success` / Color oiled: `success` / Hexadecimal: `#12457EFF` o verde): Asignada a implantes (`implant`) o tejidos dentales sanos y normales (`normal`/`healthy`). Indica intervención terminada exitosamente o anatomía sana.

---

## 10. Guía de operación y desarrollo local

### Configuración del entorno de desarrollo
Para asegurar el correcto funcionamiento del portal en local, se requiere un archivo de configuración de variables de entorno `.env` en la raíz de la carpeta [frontend](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend):

```env
VITE_GRAPHQL_ENDPOINT=http://localhost:8080/graphql
```

### Comandos de consola del frontend

El desarrollo del portal cuenta con scripts automatizados detallados en el [package.json](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/package.json):

* **Instalación de dependencias**:
  Se recomienda usar exclusivamente pnpm para mantener la coherencia con el workspace del proyecto y evitar colisiones de dependencias:
  ```powershell
  pnpm install
  ```
* **Inicio del servidor de desarrollo**:
  Levanta el entorno en local con hot reload en el puerto por defecto de Vite (normalmente `http://localhost:5173`):
  ```powershell
  pnpm dev
  ```
* **Compilación de producción**:
  Genera los archivos compilados, optimizados y minificados listos para distribución estática dentro de la carpeta `dist`:
  ```powershell
  pnpm build
  ```
* **Formateo de código**:
  Aplica el formateador y corrector estático de estilos `oxfmt` sobre el directorio del código fuente:
  ```powershell
  pnpm format
  ```

---

## 11. Configuración para despliegues en contenedores (Docker)

El portal frontend puede ser empaquetado y servido de forma aislada en un contenedor Docker utilizando la configuración provista en el directorio:

### Archivo de configuración de contenedor (Dockerfile)
Contiene una receta de construcción en dos etapas (Multi-stage build) para mantener la ligereza del contenedor en producción:
1. **Etapa de construcción (Build Stage)**: Utiliza una imagen base ligera de Node.js, instala `pnpm`, copia el código de la aplicación, inyecta las variables de entorno de producción y compila los estáticos optimizados mediante `pnpm build`.
2. **Etapa de servidor (Production Stage)**: Copia únicamente el directorio final de salida compile (`dist`) sobre una imagen ultraligera del servidor web Nginx, exponiendo el puerto 80 para la lectura de la interfaz de forma nativa.

### Lanzamiento mediante Docker Compose
El archivo [docker-compose.yml](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/frontend/docker-compose.yml) permite orquestar de manera automática el levantamiento del contenedor:

```sh
# Construir y arrancar el frontend en segundo plano
docker compose up --build -d
```

Una vez en ejecución, el frontend estará disponible en `http://localhost:80` (o en el puerto alternativo configurado en las propiedades de docker-compose).
