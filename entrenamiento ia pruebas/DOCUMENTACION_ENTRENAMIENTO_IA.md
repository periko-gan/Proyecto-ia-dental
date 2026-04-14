# Documentación técnica de `entrenamiento ia pruebas`

Este documento describe qué contiene `entrenamiento ia pruebas`, para qué sirve cada carpeta/archivo principal, qué hace cada función de los scripts de automatización y cómo se ejecutan entrenamiento, test (predicción) y validación.

> Alcance: solo `entrenamiento ia pruebas`.
> Nota: no se listan imágenes una por una; se documenta la estructura y el flujo.

## 1. Mapa del directorio

Raíz: `entrenamiento ia pruebas/`

- `.venv/`
  - Entorno virtual local de Python.
- `dataset/`
  - Dataset operativo para YOLOv8 (`images/`, `labels/`, `data.yaml`, reportes).
- `tools/`
  - Scripts CLI de conversión, entrenamiento, evaluación y pipeline.
- `tests/`
  - Pruebas de humo/unitarias para validar scripts y funciones.
- `frontend/`
  - Interfaz Streamlit e inferencia para visualización de detecciones.
- `runs/`
  - Salidas de entrenamiento/evaluación/predicción (y pipeline cuando se usa).
- `README.md`
  - Guía operativa de uso diario (instalación, comandos y limpieza).
- `requirements.txt`
  - Dependencias del proyecto (sin fijar `torch` para evitar conflictos CPU/CUDA).
- `yolov8n.pt`
  - Peso base preentrenado recomendado para iniciar entrenamiento.
- `best.pt`, `last.pt`
  - Checkpoints disponibles en la raíz (si se han copiado o dejado ahí).
- `data.yaml`, `conversion_report.json`
  - Copias de configuración/reporte en la raíz del proyecto.
- `radiografia-de-implantes.jpg`, `Radiografia-dental.png`, `radiografías-dentales1-1024x730.jpg`
  - Imágenes de ejemplo para pruebas de inferencia.

## 2. Contenido por directorio relevante

## `dataset/`

- `dataset/images/train`, `dataset/images/val`, `dataset/images/test`
  - Imágenes por split.
- `dataset/labels/train`, `dataset/labels/val`, `dataset/labels/test`
  - Etiquetas YOLO (`.txt`) y CSV origen (`_annotations.csv`).
- `dataset/data.yaml`
  - Manifiesto del dataset usado por Ultralytics.
- `dataset/conversion_report.json`
  - Resumen de calidad de la conversión CSV -> YOLO.

## `tools/`

- `tools/csv_to_yolo.py`
  - Convierte CSV a etiquetas YOLO y genera `data.yaml`.
- `tools/device_resolver.py`
  - Resuelve `--device` con fallback seguro (`auto`/`cpu`/GPU).
- `tools/train_yolov8.py`
  - Entrena YOLOv8 y fuerza que los `runs` queden dentro del proyecto.
- `tools/eval_predict_yolov8.py`
  - Ejecuta `val`, `predict` o `both`, exportando reportes.
- `tools/run_train_eval_predict_yolov8.py`
  - Pipeline de extremo a extremo: `train -> eval/predict`.

## `frontend/`

- `frontend/inference.py`
  - Carga modelo YOLO, ejecuta inferencia y dibuja recuadros.
- `frontend/app.py`
  - UI en Streamlit para cargar imagen, ajustar parámetros y descargar resultados.
- `frontend/README.md`
  - Instrucciones específicas del frontend.

## `tests/`

- `tests/test_csv_to_yolo_smoke.py`
  - Conversión básica CSV -> YOLO.
- `tests/test_train_yolov8_smoke.py`
  - Smoke test de `train_yolov8.py --dry-run`.
- `tests/test_eval_predict_yolov8_smoke.py`
  - Smoke test de `eval_predict_yolov8.py --dry-run`.
- `tests/test_eval_predict_yolov8_extract_metrics.py`
  - Valida normalización y extracción de métricas.
- `tests/test_run_train_eval_predict_yolov8_smoke.py`
  - Smoke test del pipeline completo en seco.
- `tests/test_frontend_inference_smoke.py`
  - Validación rápida de flujo de inferencia del frontend.

## `runs/`

- `runs/train/`
  - Artefactos de entrenamiento (`weights/best.pt`, `weights/last.pt`, gráficas).
- `runs/eval_predict/`
  - Salidas de validación/predicción (`val_metrics.*`, `run_report.json`, imágenes).
- `runs/pipeline/` (si se ejecuta el orquestador)
  - `pipeline_report.json` de corridas end-to-end.

## 3. Qué hace cada archivo de `tools/` y sus funciones

## `tools/device_resolver.py`

Objetivo: convertir el `--device` solicitado en un valor válido para Torch/Ultralytics.

- `DeviceResolution`
  - Dataclass inmutable con `requested`, `resolved` y `warning`.
- `_safe_torch_info()`
  - Intenta leer `torch.cuda.is_available()` y `torch.cuda.device_count()` con manejo defensivo.
- `resolve_device(requested_device)`
  - Reglas clave:
    - `auto` -> `0` si CUDA está disponible, si no `cpu`.
    - `cpu` -> CPU forzada.
    - `0`, `0,1`, etc. -> valida índices y cae a CPU si no hay CUDA.

## `tools/csv_to_yolo.py`

Objetivo: convertir anotaciones CSV por split al formato YOLOv8 y generar manifiestos.

- `parse_args()`
  - Define argumentos CLI de rutas y nombres de archivos.
- `collect_classes(dataset_root, csv_name)`
  - Recorre CSV y crea el vocabulario de clases.
- `list_images(images_dir)`
  - Lista imágenes válidas por extensión.
- `row_to_box(row, class_to_id)`
  - Convierte una fila CSV en caja YOLO normalizada.
- `write_label_file(path, boxes)`
  - Escribe `.txt` YOLO por imagen.
- `convert_split(...)`
  - Convierte un split completo y acumula estadísticas de calidad.
- `write_data_yaml(dataset_root, data_yaml_name, class_names)`
  - Genera `data.yaml` para Ultralytics.
- `write_report(dataset_root, report)`
  - Guarda `conversion_report.json`.
- `main()`
  - Orquesta todo el proceso y muestra rutas de salida.

## `tools/train_yolov8.py`

Objetivo: entrenar YOLOv8 desde CLI, con salidas dentro de `runs/` del proyecto.

- `_resolve_project_dir(project_arg)`
  - Resuelve rutas de proyecto; si son relativas, las ancla en `entrenamiento ia pruebas`.
- `parse_args()`
  - Define parámetros de entrenamiento (`data`, `model`, `epochs`, `imgsz`, `batch`, etc.).
- `build_train_kwargs(args)`
  - Construye kwargs para `model.train()`.
- `main()`
  - Valida `data.yaml`.
  - Resuelve dispositivo con `resolve_device`.
  - Configura `ultralytics.settings.runs_dir` a `entrenamiento ia pruebas/runs`.
  - Ejecuta entrenamiento y muestra `ultralytics_save_dir`.

## `tools/eval_predict_yolov8.py`

Objetivo: ejecutar validación y/o predicción con exportación de métricas y reporte.

- `_resolve_project_dir(project_arg)`
  - Fija rutas relativas dentro del proyecto.
- `parse_args()`
  - CLI para `--task val|predict|both`.
- `build_val_kwargs(args)`
  - Argumentos para `model.val()`.
- `build_predict_kwargs(args)`
  - Argumentos para `model.predict()`.
- `_normalize_metric_value(value)`
  - Convierte tensores/listas/arrays a tipos serializables.
- `extract_metrics(metrics_obj)`
  - Extrae métricas principales (`fitness`, `speed`, `box_map`, etc.).
- `write_metrics_files(metrics, output_dir)`
  - Guarda métricas en `val_metrics.json` y `val_metrics.csv`.
- `write_run_report(...)`
  - Escribe `run_report.json` con contexto de ejecución.
- `_validate_inputs(args)`
  - Valida existencia de `data` y `source` cuando corresponda.
- `_predict_count(results)`
  - Cuenta elementos procesados en predicción.
- `_extract_save_dir(value)`
  - Obtiene `save_dir` real devuelto por Ultralytics.
- `main()`
  - Ejecuta tareas, escribe reportes y muestra ruta final.

## `tools/run_train_eval_predict_yolov8.py`

Objetivo: orquestar `train -> eval/predict` con nombres versionados por timestamp UTC.

- `_resolve_project_dir(project_arg)`
  - Normaliza proyectos de salida (`train`, `eval_predict`, `pipeline`).
- `parse_args()`
  - CLI global del pipeline.
- `utc_stamp()`
  - Genera sello temporal UTC.
- `_run_step(command, label)`
  - Ejecuta scripts hijos y propaga errores.
- `_resolve_trained_model(train_project, train_name, fallback_model)`
  - Prioriza `best.pt`, luego `last.pt`, luego fallback.
- `main()`
  - Valida entradas, ejecuta train/eval según flags y guarda `pipeline_report.json`.

## 4. Qué hace cada archivo de `frontend/` y sus funciones

## `frontend/inference.py`

Objetivo: encapsular inferencia YOLO y dibujo de detecciones para la UI.

- `project_root()`
  - Devuelve la raíz del proyecto.
- `default_model_path()`
  - Devuelve `best.pt` como modelo por defecto.
- `load_yolo_model(model_path)`
  - Carga YOLO y valida que el modelo exista.
- `_draw_detections(canvas, detections)`
  - Dibuja recuadros y etiqueta sobre la imagen.
- `draw_detections(image, detections, selected_indices=None)`
  - Dibuja todas o solo detecciones seleccionadas.
- `run_inference(model, image_bytes, conf, iou, imgsz, device)`
  - Ejecuta predicción y devuelve imagen anotada + lista de detecciones.

## `frontend/app.py`

Objetivo: ofrecer una interfaz Streamlit para análisis visual de radiografías.

- `get_model(model_path)`
  - Cachea el modelo en memoria para no recargarlo en cada acción.
- Flujo principal de la app:
  - Lee imagen subida.
  - Ejecuta `run_inference` con parámetros de UI.
  - Muestra tabla editable para activar/desactivar recuadros.
  - Renderiza imagen final y permite descarga en JPG.

## 5. Flujo de entrenamiento, test y validación

## Entrenamiento

1. Preparar datos en `dataset/` y verificar `dataset/data.yaml`.
2. Ejecutar `tools/train_yolov8.py`.
3. El script resuelve dispositivo (`auto`, `cpu`, `0`, etc.).
4. Se guardan artefactos en `runs/train/<run>/`.
5. Pesos clave: `runs/train/<run>/weights/best.pt` y `last.pt`.

## Test (predicción)

1. Usar un modelo (`best.pt` recomendado).
2. Ejecutar `tools/eval_predict_yolov8.py --task predict ...`.
3. Revisar imágenes de salida en `runs/eval_predict/<run>/`.
4. Consultar `run_report.json` para trazabilidad.

## Validación (`val`)

1. Ejecutar `tools/eval_predict_yolov8.py --task val ...`.
2. Revisar métricas en:
   - `runs/eval_predict/<run>/val_metrics.json`
   - `runs/eval_predict/<run>/val_metrics.csv`
3. Revisar `run_report.json` para parámetros y rutas.

## 6. Cómo usar los datos resultantes

- Inferencia en nuevos datos: usar `weights/best.pt`.
- Comparación de experimentos: contrastar `val_metrics.*` y `run_report.json` entre corridas.
- Reentrenamiento/fine-tuning: partir de `last.pt` o `best.pt`.
- Despliegue mínimo: conservar `best.pt`, `dataset/data.yaml`, métricas y reportes.

## 7. Resumen rápido

- Conversión: `tools/csv_to_yolo.py`
- Entrenamiento: `tools/train_yolov8.py`
- Evaluación/test: `tools/eval_predict_yolov8.py`
- Pipeline: `tools/run_train_eval_predict_yolov8.py`
- Frontend: `frontend/app.py` + `frontend/inference.py`
- Pruebas: `tests/`
- Artefactos: `runs/`
