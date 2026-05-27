# Resumen del despliegue en Dokploy

## Checklist
- [x] Se creó un `docker-compose.yml` en la raíz del proyecto.
- [x] Se añadieron servicios para `mongo`, `zookeeper`, `kafka`, `kafka-ui`, `backend` y `frontend`.
- [x] Se creó `backend/Dockerfile` para ejecutar el backend Python con FastAPI.
- [x] Se añadió `frontend/nginx.conf` para servir la SPA y hacer proxy al backend.
- [x] Se ajustó `frontend/Dockerfile` para usar `VITE_GRAPHQL_ENDPOINT=/graphql`.
- [x] Se creó una `.dockerignore` para reducir el peso del build.
- [x] Se validó la configuración con `docker compose config`.

## Qué se hizo
Se preparó una configuración de contenedores pensada para Dokploy con el objetivo de levantar todo el proyecto de forma unificada:

- **Frontend**: aplicación Vue compilada con Vite y servida con Nginx.
- **Backend**: API en FastAPI con GraphQL, MongoDB y carga del modelo de IA.
- **Base de datos**: MongoDB con volumen persistente.
- **Mensajería**: Kafka y Zookeeper para los eventos del sistema.
- **UI de Kafka**: incluida para observar tópicos y estado del broker.

## Archivos creados o modificados
- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `frontend/nginx.conf`
- `.dockerignore`

## Validación realizada
Se ejecutó la validación de Docker Compose y la configuración resultó correcta.

```powershell
docker compose -f docker-compose.yml config
```

## Detalles relevantes
- El backend apunta al modelo:
  `entrenamiento ia/runs/train/dental_definitivo_optimizado_medium/weights/best.pt`
- Mongo queda accesible internamente como:
  `mongodb://mongo:27017`
- El frontend usa el proxy de Nginx para resolver:
  - `/graphql`
  - `/uploads`
  - `/health`
  - `/docs`
  - `/redoc`

## Puertos principales
- **Frontend**: `8080`
- **Backend**: `8000`
- **MongoDB**: `27017`
- **Kafka UI**: `8085`

## Nota importante
Antes de pasar a producción, conviene reemplazar el secreto JWT por uno seguro:

- `DENTAL_AI_AUTH_JWT_SECRET`

## Siguiente paso recomendado
Si se quiere una versión más ligera para Dokploy, se puede simplificar el stack y dejar solo:
- `frontend`
- `backend`
- `mongo`

sin Kafka ni Kafka UI.

