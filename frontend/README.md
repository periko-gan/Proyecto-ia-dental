# Frontend

Aplicacion frontend construida con **Vue 3 + Vite**.

## Stack principal

- Vue 3
- Vite
- Pinia
- Vue Router
- Apollo Client + GraphQL
- Tailwind CSS v4 + daisyUI

## Requisitos

- **Node.js**: `^20.19.0 || >=22.12.0`
- **pnpm**: recomendado (definido en `packageManager`: `pnpm@10.17.1`)

## Instalacion

Desde la carpeta `frontend`:

```sh
pnpm install
```

## Scripts disponibles

```sh
pnpm dev
pnpm build
pnpm preview
pnpm format
```

- `pnpm dev`: inicia el servidor de desarrollo
- `pnpm build`: genera el build de produccion
- `pnpm preview`: sirve localmente el build generado
- `pnpm format`: formatea `src/` con `oxfmt`

## Estructura basica

```text
frontend/
  src/
    App.vue
    main.js
    style.css
    components/
      AnalysisResults.vue
      UploadRadiography.vue
    graphql/
      mutations.js
    router/
      index.js
    stores/
```

## Tailwind CSS v4 + daisyUI

La configuracion activa usa el plugin oficial de Vite para Tailwind v4:

- `vite.config.js` con `@tailwindcss/vite`
- `src/style.css` con:
  - `@import 'tailwindcss';`
  - `@plugin "daisyui";`
- `src/main.js` importa `./style.css`

En Tailwind v4 no es necesario `tailwindcss init -p`.

## Uso desde la raiz del repositorio

Con `pnpm-workspace.yaml` y `package.json` en la raiz (`codigo proyecto final`), puedes ejecutar:

```sh
pnpm install
pnpm dev
pnpm build
pnpm preview
pnpm format
```

Los scripts de la raiz delegan al paquete `frontend`.

## Docker (solo carpeta frontend)

El `Dockerfile` de `frontend` publica Nginx en el puerto `80`. Para lanzarlo con Compose:

```sh
cd frontend
docker compose up --build -d
```

Abrir en navegador:

```text
http://localhost:80
```

Comandos utiles:

```sh
cd frontend
docker compose ps
docker compose logs -f
docker compose down
```

Si el puerto `80` ya esta ocupado en tu maquina, cambia temporalmente el mapeo en `docker-compose.yml` a `8080:80` y abre `http://localhost:8080`.

## Problemas comunes

### 1) Error de dependencias con `npm` (`ERESOLVE`)

Este proyecto esta preparado para **pnpm**. Evita mezclar gestores.

```sh
# recomendado
pnpm install
```

### 2) `ERR_PNPM_UNEXPECTED_VIRTUAL_STORE`

Suele ocurrir si cambiaste de ruta/proyecto o instalaste antes desde otra ubicacion.

Pasos recomendados (en la raiz del frontend):

```sh
pnpm install
```

Si persiste, limpia instalaciones previas y reinstala:

```sh
Remove-Item -Recurse -Force node_modules
Remove-Item -Force pnpm-lock.yaml
pnpm install
```

## Notas

- Usa **solo pnpm** para evitar conflictos de lockfile y peers.
- Si vas a trabajar varios paquetes desde la raiz, considera mantener un `pnpm-workspace.yaml` en la raiz del repo.
