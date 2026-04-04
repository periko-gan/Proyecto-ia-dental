# Documentacion tecnica del directorio `entrenamiento ia`

Este documento explica **que hay** en `entrenamiento ia`, **que hace cada archivo importante**, **que hace cada funcion de los scripts**, y el flujo completo de **entrenamiento**, **test (predict)** y **validacion (val)**.

> Alcance: solo la carpeta `entrenamiento ia`.
> Nota: hay miles de imagenes, por eso se documenta la estructura y el rol de cada grupo de archivos, no una lista imagen por imagen.

## 1) Estructura general del directorio

Ruta base: `entrenamiento ia/`

- `.pytest_cache/`
  - Cache local de `pytest` (no forma parte del modelo ni del dataset).
- `.venv/`
  - Entorno virtual Python con dependencias instaladas.
- `archive/`
  - Dataset original/historico en formato de origen (`train/`, `valid/`, `test/` con imagenes y CSV de anotaciones).
- `archive.zip`
  - Comprimido del dataset original.
- `best.pt`
  - Checkpoint de modelo YOLO entrenado (si existe en raiz, suele ser una copia/exportacion manual).
- `last.pt`
  - Ultimo checkpoint de entrenamiento (si existe en raiz, suele ser una copia/exportacion manual).
- `dataset/`
  - Dataset operativo para YOLOv8 (imagenes, etiquetas YOLO, `data.yaml`, reportes de conversion).
- `README.md`
  - Guia operativa del proyecto (instalacion, comandos y rutas de salida).
- `requirements.txt`
  - Dependencias Python del proyecto (sin fijar `torch` para permitir elegir wheel CUDA/CPU).
- `runs/`
  - Salidas generadas por ejecuciones: entrenamiento, evaluacion/prediccion, pipeline.
- `tests/`
  - Tests de humo y unitarios de los scripts.
- `tools/`
  - Scripts principales del flujo de datos, entrenamiento y evaluacion.
- `yolo26n.pt`, `yolov8n.pt`
  - Pesos base/preentrenados para arrancar entrenamiento o pruebas.

## 2) Directorio `dataset/` (datos de trabajo)

Contenido observado:

- `dataset/images/`
  - Imagenes separadas por split (`train/`, `val/`, `test/`).
- `dataset/labels/`
  - Etiquetas YOLO por split (`.txt`) y CSV de origen (`_annotations.csv`) segun el flujo usado.
- `dataset/data.yaml`
  - Manifiesto que usa Ultralytics:
    - `path`: raiz del dataset.
    - `train`, `val`, `test`: rutas relativas a imagenes.
    - `nc`: numero de clases.
    - `names`: mapping id -> nombre de clase.
- `dataset/conversion_report.json`
  - Reporte de conversion CSV->YOLO (filas validas, invalidas, imagenes faltantes, etc.).

## 3) Directorio `tools/`: archivos y funciones

## `tools/device_resolver.py`
Utilidad para decidir CPU/GPU antes de llamar a Ultralytics.

Funciones:

- `DeviceResolution` (dataclass)
  - Estructura inmutable con:
    - `requested`: dispositivo pedido por CLI.
    - `resolved`: dispositivo final aplicado.
    - `warning`: advertencia opcional.
- `_safe_torch_info()`
  - Intenta importar `torch` y devolver `(cuda_available, cuda_count)`.
  - Si falla, devuelve `None`.
- `resolve_device(requested_device)`
  - Reglas:
    - `auto` -> `0` si hay CUDA; si no, `cpu`.
    - `cpu` -> fuerza `cpu`.
    - `0`, `0,1`, etc. -> valida indices GPU y hace fallback a `cpu` si no hay CUDA.

## `tools/csv_to_yolo.py`
Convierte anotaciones CSV a etiquetas YOLOv8 y genera `data.yaml`.

Constantes/estructuras:

- `REQUIRED_COLUMNS`: columnas obligatorias del CSV.
- `IMAGE_EXTENSIONS`: extensiones de imagen validas.
- `SPLITS`: `train`, `val`, `test`.
- `Box` (dataclass): caja normalizada YOLO (`class_id`, `x_center`, `y_center`, `width`, `height`).
- `SplitSummary` (dataclass): metricas de calidad por split.

Funciones:

- `parse_args()`
  - Lee parametros CLI (`dataset-root`, `csv-name`, `output-labels-dir`, `data-yaml`).
- `collect_classes(dataset_root, csv_name)`
  - Recorre CSV de los splits y detecta clases unicas.
- `list_images(images_dir)`
  - Lista archivos de imagen validos en disco.
- `row_to_box(row, class_to_id)`
  - Convierte una fila CSV a `Box` YOLO, valida y normaliza coordenadas.
- `write_label_file(path, boxes)`
  - Escribe etiquetas `.txt` YOLO por imagen.
- `convert_split(dataset_root, split, csv_name, class_to_id, output_labels_root)`
  - Procesa un split completo: valida, agrupa cajas y escribe labels.
- `write_data_yaml(dataset_root, data_yaml_name, class_names)`
  - Crea `data.yaml` con rutas y clases.
- `write_report(dataset_root, report)`
  - Guarda `conversion_report.json`.
- `main()`
  - Orquesta todo: clases -> conversion por split -> `data.yaml` -> reporte.

## `tools/train_yolov8.py`
Lanza entrenamiento YOLOv8 a partir de `data.yaml`.

Funciones:

- `_resolve_project_dir(project_arg)`
  - Resuelve rutas de salida y mantiene rutas relativas dentro de `entrenamiento ia`.
- `parse_args()`
  - CLI de entrenamiento (`data`, `model`, `epochs`, `imgsz`, `batch`, `device`, etc.).
- `build_train_kwargs(args)`
  - Traduce CLI al diccionario esperado por `model.train()`.
- `main()`
  - Valida entradas.
  - Resuelve dispositivo (`auto`/`cpu`/GPU).
  - Configura `ultralytics.settings.runs_dir` para guardar en `entrenamiento ia/runs`.
  - Ejecuta `YOLO(args.model).train(...)`.
  - Imprime `ultralytics_save_dir` y finaliza.

## `tools/eval_predict_yolov8.py`
Ejecuta validacion (`val`), prediccion (`predict`) o ambos, y genera reportes.

Funciones:

- `_resolve_project_dir(project_arg)`
  - Mismo objetivo: mantener salidas dentro de `entrenamiento ia` si la ruta es relativa.
- `parse_args()`
  - CLI de evaluacion/prediccion (`task`, `data`, `model`, `source`, `conf`, `iou`, etc.).
- `build_val_kwargs(args)`
  - Arma argumentos para `model.val()`.
- `build_predict_kwargs(args)`
  - Arma argumentos para `model.predict()`.
- `_normalize_metric_value(value)`
  - Convierte tensores/arrays/escalares a formato serializable JSON.
- `extract_metrics(metrics_obj)`
  - Extrae metricas estables (`fitness`, `speed`, `box_map`, etc.).
- `write_metrics_files(metrics, output_dir)`
  - Guarda `val_metrics.json` y `val_metrics.csv`.
- `write_run_report(output_dir, args, val_metrics, prediction_count, ultralytics_save_dir)`
  - Guarda `run_report.json` con contexto de ejecucion.
- `_validate_inputs(args)`
  - Verifica existencia de `data.yaml` y `source` cuando aplica.
- `_predict_count(results)`
  - Cuenta items procesados en prediccion.
- `_extract_save_dir(value)`
  - Intenta obtener ruta real de salida desde objetos de Ultralytics.
- `main()`
  - Resuelve dispositivo, ejecuta val/predict segun `--task`, guarda metricas/reporte.

## `tools/run_train_eval_predict_yolov8.py`
Pipeline end-to-end: entrena y luego evalua/predice con versionado por timestamp.

Funciones:

- `_resolve_project_dir(project_arg)`
  - Normaliza rutas de proyectos (`train`, `eval`, `pipeline`).
- `parse_args()`
  - CLI de pipeline completo.
- `utc_stamp()`
  - Genera marca temporal UTC para nombres unicos.
- `_run_step(command, label)`
  - Ejecuta subproceso (`train` o `eval_predict`) y propaga errores.
- `_resolve_trained_model(train_project, train_name, fallback_model)`
  - Busca `best.pt` o `last.pt` para usar en evaluacion.
- `main()`
  - Valida entradas.
  - Ejecuta entrenamiento (opcional si no `--skip-train`).
  - Ejecuta evaluacion/prediccion.
  - Guarda `pipeline_report.json`.

## 4) Directorio `tests/`: que valida cada archivo

- `tests/test_csv_to_yolo_smoke.py`
  - Test de humo de conversion CSV->YOLO:
    - crea dataset temporal,
    - ejecuta script,
    - verifica labels, `data.yaml` y `conversion_report.json`.
- `tests/test_train_yolov8_smoke.py`
  - Verifica que `train_yolov8.py --dry-run` funciona y reporta dispositivo.
- `tests/test_eval_predict_yolov8_smoke.py`
  - Verifica que `eval_predict_yolov8.py --dry-run` funciona y valida rutas.
- `tests/test_eval_predict_yolov8_extract_metrics.py`
  - Test unitario de `extract_metrics()` para valores escalares y array-like.
- `tests/test_run_train_eval_predict_yolov8_smoke.py`
  - Verifica pipeline en `--dry-run` y que se crea `pipeline_report.json`.

## 5) Directorio `runs/`: que guarda cada subdirectorio

- `runs/train/`
  - Corridas de entrenamiento:
    - pesos (`weights/best.pt`, `weights/last.pt`),
    - graficas y artefactos de entrenamiento.
- `runs/eval_predict/`
  - Corridas de validacion/prediccion:
    - imagenes de prediccion,
    - `val_metrics.json`, `val_metrics.csv` (si hay val),
    - `run_report.json`.
- `runs/pipeline/`
  - Reportes globales del pipeline (`pipeline_report.json`) para trazabilidad.

## 6) Que sucede cuando se entrena una IA en este proyecto

Flujo real:

1. Se prepara `dataset/data.yaml` apuntando a `images/train`, `images/val`, `images/test`.
2. `train_yolov8.py` resuelve dispositivo (GPU/CPU).
3. Se carga un modelo base (`yolov8n.pt`, por ejemplo).
4. Ultralytics entrena por epocas con los hiperparametros definidos.
5. Se guardan pesos y artefactos en `runs/train/<nombre_run>/`.
6. El script imprime `ultralytics_save_dir` con la ruta final real de la corrida.

Resultado clave del entrenamiento:

- `weights/best.pt`: mejor checkpoint segun metricas.
- `weights/last.pt`: ultimo estado entrenado.

## 7) Como se hace el test (prediccion)

En este proyecto, "test" normalmente se refiere a inferencia sobre imagenes de `dataset/images/test`.

Flujo:

1. Cargas un modelo (`best.pt` recomendado).
2. Ejecutas `eval_predict_yolov8.py --task predict`.
3. El script corre inferencia, dibuja cajas y guarda resultados en `runs/eval_predict/<run>/`.
4. Registra metadatos en `run_report.json`.

## 8) Como se valida (val)

Validar = medir rendimiento contra etiquetas conocidas (normalmente split `val`).

Flujo:

1. Cargas modelo.
2. Ejecutas `eval_predict_yolov8.py --task val`.
3. Ultralytics calcula precision/recall/mAP.
4. El script exporta metricas en:
   - `val_metrics.json`
   - `val_metrics.csv`
   - y contexto en `run_report.json`.

## 9) Como usar los datos resultantes del entrenamiento

## A) Para inferencia en nuevas imagenes

- Usa `weights/best.pt` como modelo de entrada en `predict`.
- Revisa imagenes generadas para inspeccion visual de detecciones.

## B) Para comparar experimentos

- Compara `val_metrics.json`/`val_metrics.csv` entre corridas.
- Usa `run_report.json` y `pipeline_report.json` para saber:
  - que modelo se uso,
  - con que parametros,
  - donde quedo guardada cada salida.

## C) Para reentrenar o afinar

- Usa `last.pt` para retomar entrenamiento (si se desea continuidad).
- Ajusta hiperparametros (`epochs`, `imgsz`, `batch`, `model`) y ejecuta otra corrida.

## D) Para despliegue

- Empaqueta `best.pt` junto con:
  - `data.yaml` (referencia de clases),
  - un ejemplo de `run_report.json` (trazabilidad),
  - version de dependencias (`requirements.txt` + wheel torch utilizado).

## 10) Resumen operativo rapido

- Conversion de datos: `tools/csv_to_yolo.py`
- Entrenamiento: `tools/train_yolov8.py`
- Evaluacion / prediccion: `tools/eval_predict_yolov8.py`
- Pipeline completo: `tools/run_train_eval_predict_yolov8.py`
- Tests: `tests/*.py`
- Artefactos: `runs/`

