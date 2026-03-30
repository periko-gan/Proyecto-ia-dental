# Conversor CSV -> YOLOv8

Este proyecto convierte anotaciones en CSV dentro de `dataset/labels/{train,val,test}/_annotations.csv`
al formato YOLO (`.txt` por imagen) y crea `dataset/data.yaml`.

## Estructura esperada

- `dataset/images/train`, `dataset/images/val`, `dataset/images/test`
- `dataset/labels/train/_annotations.csv`, `dataset/labels/val/_annotations.csv`, `dataset/labels/test/_annotations.csv`

Columnas requeridas en CSV:

`filename,width,height,class,xmin,ymin,xmax,ymax`

## Instalar dependencias

```powershell
python -m pip install -r .\requirements.txt
```

## Ejecutar conversión

```powershell
python .\tools\csv_to_yolo.py --dataset-root .\dataset
```

Salida:

- `dataset/labels/{train,val,test}/*.txt`
- `dataset/data.yaml`
- `dataset/conversion_report.json`

Si quieres conservar etiquetas separadas, puedes usar:

```powershell
python .\tools\csv_to_yolo.py --dataset-root .\dataset --output-labels-dir labels_yolo
```

## Entrenar YOLOv8

Ejemplo base (CPU):

```powershell
python .\tools\train_yolov8.py --data .\dataset\data.yaml --model yolov8n.pt --epochs 100 --imgsz 640 --batch 16 --device cpu
```

Ejemplo GPU (si tu equipo la detecta):

```powershell
python .\tools\train_yolov8.py --data .\dataset\data.yaml --model yolov8n.pt --epochs 100 --imgsz 640 --batch 16 --device 0
```

Validar configuración sin entrenar:

```powershell
python .\tools\train_yolov8.py --data .\dataset\data.yaml --dry-run
```

## Evaluar y predecir YOLOv8

Evaluar + predecir en un solo comando:

```powershell
python .\tools\eval_predict_yolov8.py --task both --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --device cpu
```

Solo evaluacion:

```powershell
python .\tools\eval_predict_yolov8.py --task val --data .\dataset\data.yaml --model yolov8n.pt --device cpu
```

Solo prediccion:

```powershell
python .\tools\eval_predict_yolov8.py --task predict --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --device cpu
```

Validar configuracion sin ejecutar Ultralytics:

```powershell
python .\tools\eval_predict_yolov8.py --task both --data .\dataset\data.yaml --source .\dataset\images\test --dry-run
```

Salida esperada en `runs/eval_predict/<name>`:

- `run_report.json`
- `val_metrics.json` y `val_metrics.csv` (si se ejecuta `val`)
- imagenes con predicciones guardadas por Ultralytics (si se ejecuta `predict`)

## Pipeline unico (train -> eval/predict)

Ejecuta todo en secuencia con nombres versionados por timestamp UTC:

```powershell
python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --epochs 100 --imgsz 640 --batch 16 --device cpu --task both
```

Preset `GPU segura` (prioriza estabilidad, menor riesgo de OOM):

```powershell
python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --epochs 120 --imgsz 640 --batch 4 --device 0 --task both
```

Preset `GPU agresiva` (prioriza calidad/rendimiento, requiere mas VRAM):

```powershell
python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8s.pt --epochs 200 --imgsz 896 --batch 8 --device 0 --task both
```

Si aparece `CUDA out of memory`, baja primero `--batch` (por ejemplo, `8 -> 4 -> 2`) y luego `--imgsz` (`896 -> 768 -> 640`).

Modo validacion rapida del pipeline (sin entrenar/evaluar realmente):

```powershell
python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --dry-run
```

Salida del pipeline:

- `runs/pipeline/<name_prefix>_<timestamp>_pipeline/pipeline_report.json`
- Entrenamiento en `runs/train/<name_prefix>_<timestamp>_train`
- Evaluacion/prediccion en `runs/eval_predict/<name_prefix>_<timestamp>_evalpredict`

## Ejecutar pruebas rápidas

```powershell
python -m pytest .\tests\test_csv_to_yolo_smoke.py
python -m pytest .\tests\test_train_yolov8_smoke.py
python -m pytest .\tests\test_eval_predict_yolov8_smoke.py
python -m pytest .\tests\test_run_train_eval_predict_yolov8_smoke.py
```
