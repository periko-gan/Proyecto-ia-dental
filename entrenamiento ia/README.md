# Conversor CSV -> YOLOv8

Este proyecto convierte anotaciones en CSV dentro de `dataset/labels/{train,val,test}/_annotations.csv`
al formato YOLO (`.txt` por imagen) y crea `dataset/data.yaml`.

## Estructura esperada

- `dataset/images/train`, `dataset/images/val`, `dataset/images/test`
- `dataset/labels/train/_annotations.csv`, `dataset/labels/val/_annotations.csv`, `dataset/labels/test/_annotations.csv`

Columnas requeridas en CSV:

`filename,width,height,class,xmin,ymin,xmax,ymax`

## Instalar dependencias

Actualiza `pip` e instala dependencias del proyecto:

```powershell
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

## Instalar PyTorch

CPU (recomendado si no tienes NVIDIA CUDA):

```powershell
python -m pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

GPU NVIDIA (instalación limpia recomendada):

```powershell
python -m pip uninstall -y torch torchvision torchaudio
python -m pip install --upgrade pip
python -m pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
```

Alternativa si `cu130` no está disponible en tu entorno:

```powershell
python -m pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

Verificar detección de CUDA:

```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.device_count())"
```

Verificación extendida (nombre de GPU y prueba de kernel CUDA):

```powershell
python -c "import torch; print('torch', torch.__version__); print('cuda', torch.version.cuda); print('avail', torch.cuda.is_available()); print('count', torch.cuda.device_count()); print('name0', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'); x=torch.randn(512,512,device='cuda:0') if torch.cuda.is_available() else None; print('kernel_ok', x is not None)"
```

Si aparece `CUDA error: no kernel image is available for execution on the device`, normalmente indica un wheel CUDA incompatible con tu GPU. Reinstala con `cu130` (o `cu128`) y verifica de nuevo.

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

Ejemplo recomendado (auto: usa GPU si existe; si no, CPU):

```powershell
python .\tools\train_yolov8.py --data .\dataset\data.yaml --model yolov8n.pt --epochs 100 --imgsz 640 --batch 16 --device auto
```

Ejemplo base (CPU forzado):

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

Dónde buscar el entrenamiento:

- Pesos del modelo entrenado: `runs/detect/runs/train/<nombre_run>/weights/best.pt` y `last.pt`
- Ejemplo real: `runs/detect/runs/train/dental_yolov84/weights/best.pt`

## Evaluar y predecir YOLOv8

Evaluar + predecir en un solo comando:

```powershell
python .\tools\eval_predict_yolov8.py --task both --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --device auto
```

Solo evaluación:

```powershell
python .\tools\eval_predict_yolov8.py --task val --data .\dataset\data.yaml --model yolov8n.pt --device auto
```

Solo predicción:

```powershell
python .\tools\eval_predict_yolov8.py --task predict --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --device auto
```

Validar configuración sin ejecutar Ultralytics:

```powershell
python .\tools\eval_predict_yolov8.py --task both --data .\dataset\data.yaml --source .\dataset\images\test --dry-run
```

Nota: `eval_predict_yolov8.py` ya normaliza métricas escalares y array-like de Ultralytics al exportar `val_metrics.json/csv`, evitando errores como `TypeError: only 0-dimensional arrays can be converted to Python scalars`.

Salida esperada en `runs/eval_predict/<name>`:

- `run_report.json`
- `val_metrics.json` y `val_metrics.csv` (si se ejecuta `val`)
- imágenes con predicciones guardadas por Ultralytics (si se ejecuta `predict`)

Dónde buscar test y evaluación:

- Test (predicción sobre `dataset/images/test`): imágenes resultantes en `runs/detect/runs/eval_predict/<nombre_run>/`
- Evaluación (`--task val`): métricas en `runs/eval_predict/<nombre_run>/val_metrics.json` y `val_metrics.csv`
- Reporte consolidado (val/predict): `runs/eval_predict/<nombre_run>/run_report.json`

Nota de rutas: Ultralytics puede guardar artefactos visuales bajo `runs/detect/...` según su `runs_dir`, mientras que este script guarda reportes/métricas en `runs/eval_predict/...`.

## Limpieza rápida (entrenamiento limpio)

Para empezar desde cero, vacía los directorios generados por entrenamiento, test (predicción) y evaluación.

Rutas que se limpian:

- `entrenamiento ia/runs/detect/runs/train`
- `entrenamiento ia/runs/eval_predict`
- `entrenamiento ia/runs/pipeline`
- `runs/detect/runs/train`
- `runs/detect/runs/eval_predict`

Ejecuta este comando desde `entrenamiento ia`:

```powershell
$repoRoot = Split-Path -Parent (Get-Location)
$targets = @(
  (Join-Path (Get-Location) "runs\detect\runs\train"),
  (Join-Path (Get-Location) "runs\eval_predict"),
  (Join-Path (Get-Location) "runs\pipeline"),
  (Join-Path $repoRoot "runs\detect\runs\train"),
  (Join-Path $repoRoot "runs\detect\runs\eval_predict")
)
foreach ($path in $targets) {
  if (Test-Path $path) {
	Get-ChildItem -Path $path -Force | Remove-Item -Recurse -Force
  }
}
```

Este comando no toca `dataset/` ni archivos de código.

## Pipeline único (train -> eval/predict)

Ejecuta todo en secuencia con nombres versionados por timestamp UTC:

```powershell
python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --epochs 100 --imgsz 640 --batch 16 --device auto --task both
```

Preset `GPU segura` (prioriza estabilidad, menor riesgo de OOM):

```powershell
python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --epochs 120 --imgsz 640 --batch 4 --device 0 --task both
```

Preset `GPU agresiva` (prioriza calidad/rendimiento, requiere más VRAM):

```powershell
python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8s.pt --epochs 200 --imgsz 896 --batch 8 --device 0 --task both
```

Si aparece `CUDA out of memory`, baja primero `--batch` (por ejemplo, `8 -> 4 -> 2`) y luego `--imgsz` (`896 -> 768 -> 640`).

Modo validación rápida del pipeline (sin entrenar/evaluar realmente):

```powershell
python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --dry-run
```

Salida del pipeline:

- `runs/pipeline/<name_prefix>_<timestamp>_pipeline/pipeline_report.json`
- Entrenamiento en `runs/train/<name_prefix>_<timestamp>_train`
- Evaluación/predicción en `runs/eval_predict/<name_prefix>_<timestamp>_evalpredict`

## Ejecutar pruebas rápidas

```powershell
python -m pytest .\tests\test_csv_to_yolo_smoke.py
python -m pytest .\tests\test_train_yolov8_smoke.py
python -m pytest .\tests\test_eval_predict_yolov8_smoke.py
python -m pytest .\tests\test_eval_predict_yolov8_extract_metrics.py
python -m pytest .\tests\test_run_train_eval_predict_yolov8_smoke.py
```
