# Frontend - Dashboard de IA Dental

Aplicación frontend construida con **Vue 3 + Vite** para análisis radiográfico dental con inteligencia artificial.

## Stack principal

- **Vue 3** - Framework progresivo
- **Vite** - Build tool y dev server
- **Pinia** - State management
- **Vue Router** - Enrutamiento
- **Apollo Client + GraphQL** - Consultas y mutaciones API
- **Tailwind CSS v4 + daisyUI** - Styling y componentes UI

## Requisitos

- **Node.js**: `^20.19.0` o `>=22.12.0`
- **pnpm**: `10.17.1` (recomendado, evita mezclar gestores)

## Instalación

Desde la carpeta `frontend`:

```sh
pnpm install
```

## Scripts disponibles

```sh
pnpm dev       # Inicia servidor de desarrollo (hot reload)
pnpm build     # Genera build de producción
pnpm preview   # Sirve localmente el build generado
pnpm format    # Formatea src/ con oxfmt
```

## Estructura de carpetas

```text
frontend/
  src/
     main.js                    # Punto de entrada
     App.vue                    # Componente raíz
     style.css                  # Estilos globales con Tailwind
     components/
        AnalyzeView.vue        # Vista de análisis de radiografías
        DashboardView.vue      # Dashboard principal (responsive)
        RegisterView.vue       # Registro de usuarios
        LoginView.vue          # Login de usuarios
        parts/
            dashboard/
               HealthScoreHero.vue          # Puntuación de salud (hero)
               LatestDiagnosisSummary.vue   # Último diagnóstico
               ProblemTypesChart.vue        # Gráfico de tipos de problemas
            Formulario.vue                   # Componente reutilizable formulario
     composables/
        useHealthScoreHero.js  # Lógica de cálculo de puntuación de salud
        useAuth.js             # Lógica de autenticación
     config/
        graphql.js             # Configuración del endpoint GraphQL
     graphql/
        mutations.js           # Mutaciones GraphQL
        queries.js             # Consultas GraphQL
     router/
        index.js               # Configuración de rutas
     services/
        graphqlClient.js       # Cliente GraphQL (Apollo)
        authService.js         # Servicio de autenticación
     stores/
         auth.js                # Store de Pinia para autenticación
```

## Configuración de variables de entorno

Crear archivo `.env` en la raíz de `frontend`:

```env
VITE_GRAPHQL_ENDPOINT=http://localhost:8080/graphql
```

**Nota**: Las variables deben estar prefijadas con `VITE_` para ser inyectadas por Vite en tiempo de build.

- `VITE_GRAPHQL_ENDPOINT`: Endpoint GraphQL (por defecto: `http://localhost:8000/graphql`)

## Flujo de autenticación

### Registro

1. El usuario completa el formulario de registro (`RegisterView`)
2. Se ejecuta la mutación GraphQL `registerUser(email, password)`
3. El backend crea la cuenta y retorna `accessToken`
4. El token se guarda en `sessionStorage`
5. Se redirige a `/dashboard`

### Login

1. El usuario ingresa credenciales en `LoginView`
2. Se ejecuta la mutación GraphQL `loginUser(email, password)`
3. Retorna `accessToken` y datos de usuario
4. Se almacena en `sessionStorage`:
    - `accessToken` - para autorización GraphQL
    - `user` - JSON con `userId`, `email`, `isActive`, `role`

### Protección de rutas

Las rutas protegidas requieren `accessToken` válido en `sessionStorage`. Si no existe, se redirige a `/login`.

## Dashboard responsivo

El dashboard se adapta automáticamente a diferentes tamaños de pantalla:

- **Móvil** (< 768px): Stack vertical de componentes
- **Tablet** (768px - 1024px): Dos columnas
- **Desktop** (> 1024px): Tres columnas con proporciones ajustadas

### Componentes principales

1. **Health Score Hero**
    - Muestra puntuación de salud (promedio de confianza de todos los hallazgos)
    - Radiograma circular con indicador de porcentaje
    - Recuento de severidades (crítico, advertencia, éxito)

2. **Latest Diagnosis Summary**
    - Thumbnail de la radiografía más reciente
    - Resumen del hallazgo principal
    - Confianza promedio del análisis

3. **Problem Types Chart**
    - Visualiza distribución de problemas detectados
    - Categorías: Caries, Empastes, Implantes, Dientes impactados
    - Muestra conteos y porcentajes

## Tailwind CSS v4 + daisyUI

Configuración:

- `vite.config.js` - Usa plugin `@tailwindcss/vite`
- `src/style.css` - Importa Tailwind y plugin daisyUI:
  ```css
  @import 'tailwindcss';
  @plugin 'daisyui';
  ```
- `tailwind.config.js` - Configuración de temas y extensiones

**Nota**: En Tailwind v4 no es necesario ejecutar `tailwindcss init -p`.

## Uso desde raíz del repositorio

Con `pnpm-workspace.yaml` en la raíz, puedes ejecutar los scripts desde cualquier ubicación:

```sh
pnpm install  # Instala dependencias de todos los workspaces
pnpm dev      # Inicia dev de frontend (delegado por workspace)
pnpm build    # Build de frontend
```

## Docker

Lanzar frontend en contenedor:

```sh
cd frontend
docker compose up --build -d
```

Acceso:

- Si puerto `80` está disponible: `http://localhost:80`
- Si puerto `80` está ocupado: `http://localhost:8080` (cambiar mapeo en `docker-compose.yml` a `8080:80`)

Comandos útiles:

```sh
docker compose ps      # Ver estado del contenedor
docker compose logs -f # Ver logs en tiempo real
docker compose down    # Detener contenedor
```

## Problemas comunes

### 1) Error de dependencias con `npm` (`ERESOLVE`)

Este proyecto está preparado para **pnpm**. Evita mezclar gestores:

```sh
pnpm install  #  Correcto
npm install   #  Evitar
```

### 2) `ERR_PNPM_UNEXPECTED_VIRTUAL_STORE`

Ocurre si hay conflictos con instalaciones previas. Solución:

```sh
Remove-Item -Recurse -Force node_modules
Remove-Item -Force pnpm-lock.yaml
pnpm install
```

### 3) Variables de entorno no cargadas

Las variables de entorno se inyectan en tiempo de **build**. Si cambias `.env`:

```sh
# Reinicia el servidor de desarrollo
pnpm dev
```

Verifica que la variable exista en el bundle compilado:

```powershell
# En frontend/
pnpm build
Select-String -Path "dist\assets\*.js" -Pattern "8080/graphql"
```

### 4) CSS compilation error: `Invalid declaration: //`

En bloques `<style>` de Vue, usar solo comentarios en bloque:

```vue
<!--  Correcto -->
<style>
  /* Comentario válido */
</style>

<!--  Incorrecto -->
<style>
  // Esto causa error en Tailwind CSS v4
</style>
```

## Desarrollo local

### Flujo típico

1. Clonar repository y entrar en `frontend/`
2. Instalar dependencias: `pnpm install`
3. Crear `.env` con `VITE_GRAPHQL_ENDPOINT`
4. Asegurarse de que backend está corriendo en el endpoint especificado
5. Iniciar dev server: `pnpm dev`
6. Abrir navegador en `http://localhost:5173`

### Debugging

- **Inspeccionar requests GraphQL**: Abrir DevTools → Network tab → filtrar "graphql"
- **Verificar variables de entorno**: Abrir DevTools y revisar `import.meta.env` en la consola o con herramientas de depuración
- **Ver estado de Pinia**: Instalar [Pinia DevTools](https://devtools.vuejs.org/)

## Notas importantes

- Usa **solo pnpm** para evitar conflictos con lock files
- Las variables de entorno deben prefijarse con `VITE_` para ser accesibles
- Los composables (`src/composables/`) contienen lógica reutilizable
- Los stores de Pinia deben usarse para estado global (autenticación, datos usuario)
- El dashboard usa Flexbox (no CSS Grid) para mejor responsividad

## Contacto y recursos

- [Documentación Vue 3](https://vuejs.org/)
- [Documentación Vite](https://vitejs.dev/)
- [Documentación Tailwind CSS v4](https://tailwindcss.com/)
- [Documentación Apollo Client](https://www.apollographiql.com/docs/react/)
