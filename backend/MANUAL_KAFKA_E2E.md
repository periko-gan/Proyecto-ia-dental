# Prueba Manual E2E Kafka (sin reemplazar flujo sincronico)

Objetivo de esta prueba:
1. Confirmar publicacion de `dental.analysis.requested`.
2. Confirmar que el consumer opcional recibe ese evento.
3. Confirmar que `InferenceService` puede procesarlo.
4. Confirmar publicacion de `dental.analysis.started` y `dental.analysis.completed` (o `dental.analysis.failed`).
5. Confirmar que el flujo sincronico GraphQL actual sigue funcionando.

## Precondiciones
- Docker stack de mensajeria levantado en `docker/docker-compose.yml`.
- MongoDB levantado para backend.
- Topics creados (si hace falta):
  - `bash scripts/init-kafka-topics.sh`
- Consumer opcional permanece deshabilitado por defecto en `.env`:
  - `DENTAL_AI_KAFKA_INFERENCE_CONSUMER_ENABLED=false`

## Terminales recomendadas

### Terminal A: backend normal (flujo sincronico intacto)
Desde `backend/`:

```powershell
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal B: observar eventos `analysis.requested`

```powershell
docker exec -it kafka_proyecto kafka-console-consumer --bootstrap-server localhost:9092 --topic dental.analysis.requested --from-beginning
```

### Terminal C: observar eventos de proceso (`started/completed/failed`)

```powershell
docker exec -it kafka_proyecto kafka-console-consumer --bootstrap-server localhost:9092 --topic dental.analysis.started --from-beginning
```

Abre otra terminal para completed:

```powershell
docker exec -it kafka_proyecto kafka-console-consumer --bootstrap-server localhost:9092 --topic dental.analysis.completed --from-beginning
```

Opcional para errores:

```powershell
docker exec -it kafka_proyecto kafka-console-consumer --bootstrap-server localhost:9092 --topic dental.analysis.failed --from-beginning
```

## Paso 1 - Validar que no se rompe el flujo sincronico actual
Ejecuta una mutacion GraphQL normal (`uploadRadiography`) contra `http://localhost:8000/graphql` con usuario autenticado.

Esperado:
- Respuesta GraphQL correcta como antes.
- Evento en `dental.analysis.requested`.
- Eventos `dental.analysis.started` y `dental.analysis.completed` (o `failed`) publicados.

Guarda estos datos de la respuesta para el paso 3:
- `analysis.analysisId`
- `analysis.userId`
- `analysis.fileName`
- `analysis.filePath`

## Paso 2 - Levantar una segunda instancia temporal con consumer habilitado
Sin tocar `.env`, abre otra terminal en `backend/`:

```powershell
.\scripts\run-backend-consumer-e2e.ps1 -Port 8001
```

Esperado en logs:
- `Consumidor opcional de analysis.requested habilitado`
- `AnalysisRequestedConsumer iniciado topic=dental.analysis.requested`

## Paso 3 - Publicar `analysis.requested` manual para que lo procese el consumer
En otra terminal, publica un nuevo evento apuntando a una imagen existente (usa `filePath` real del Paso 1):

```powershell
..\.venv\Scripts\python.exe .\scripts\publish_analysis_requested_e2e.py --analysis-id manual-e2e-001 --user-id <USER_ID> --file-name <FILE_NAME> --file-path <FILE_PATH_REAL>
```

Ejemplo:

```powershell
..\.venv\Scripts\python.exe .\scripts\publish_analysis_requested_e2e.py --analysis-id manual-e2e-001 --user-id 123 --file-name rx.png --file-path C:\Users\hufer\Desktop\personal symfony\Proyecto-ia-dental\backend\storage\uploads\<archivo>.png
```

## Paso 4 - Evidencia esperada por objetivo

### Objetivo 1: `dental.analysis.requested` se publica
- Confirmado en Terminal B.

### Objetivo 2: consumer recibe evento
- Confirmado en logs de la instancia `:8001` (Terminal del script PowerShell).

### Objetivo 3: `InferenceService` procesa evento
- Confirmado en logs de la instancia `:8001` con mensaje de inferencia completada o error de inferencia.

### Objetivo 4: eventos de proceso se publican
- Confirmado en consumidores de topics:
  - `dental.analysis.started`
  - `dental.analysis.completed` o `dental.analysis.failed`

### Objetivo 5: no se rompe flujo actual
- Repite `uploadRadiography` contra `http://localhost:8000/graphql` mientras la instancia `:8001` esta activa.
- Debe seguir respondiendo correctamente.

## Limpieza
- Deten la instancia temporal `:8001` con `Ctrl+C`.
- No se requiere cambiar `.env` porque el consumer se habilito solo por variables de entorno de proceso.
