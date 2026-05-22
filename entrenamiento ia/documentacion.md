# Proyecto de fin de ciclo: Especialización en IA y Big Data
## Detección automatizada de patologías y estructuras dentales mediante visión artificial (YOLOv8)

---

*   **Entidad académica:** Ciclo de Especialización en Inteligencia Artificial y Big Data
*   **Módulo:** Sistemas de Aprendizaje Automático / MLOps y Big Data
*   **Proyecto:** Sistema de soporte clínico diagnóstico basado en redes neuronales convolucionales
*   **Área de trabajo:** Visión artificial (Object Detection) aplicada a la Odontología
*   **Autor:** Estudiante de IA y Big Data
*   **Fecha de presentación:** Mayo 2026

---

> [!NOTE]
> Esta documentación unifica los fundamentos teóricos, la arquitectura de código, las guías de instalación y despliegue, la bitácora experimental y los resultados clínicos del proyecto. Sirve como memoria técnica y material de soporte para la defensa ante el tribunal.

---

## 1. Introducción y objetivos del proyecto

El objetivo principal de este proyecto es la optimización de modelos de detección de objetos YOLOv8 para identificar y localizar de forma automática cuatro clases clínicas clave en radiografías dentales:
1.  **Caries (Cavity)**: Lesiones activas de descalcificación en el esmalte o dentina.
2.  **Empastes (Fillings)**: Obturaciones previas de amalgama o composite.
3.  **Implantes (Implant)**: Tornillos de titanio intraóseos y prótesis sobre implante.
4.  **Dientes impactados (Impacted Tooth)**: Piezas que no han erupcionado completamente y quedan retenidas en el hueso maxilar.

### Desafío del dataset (Big Data a escala médica)
Trabajamos bajo restricciones comunes en el ámbito clínico:
*   **Volumen de datos:** Un dataset cerrado de **1075 imágenes de entrenamiento** y **121 de validación**.
*   **Clases minoritarias / Complejidad geométrica:** Las caries representan el objeto de menor tamaño y con bordes menos definidos, lo que contrasta con el alto contraste metálico de los implantes.
*   **Objetivo técnico:** Maximizar el rendimiento global (mAP50) y el *Recall* (Sensibilidad) sin añadir datos externos, utilizando únicamente **Transfer Learning**, **Fine-Tuning avanzado** e **Hyperparameter Tuning genético**.

---

## 2. Tipo de entrenamiento y conceptos de Machine Learning utilizados

Para defender este proyecto como especialistas de IA y Big Data, definimos las bases metodológicas del entrenamiento:

1.  **Redes neuronales convolucionales (CNN) y Deep Learning**: El modelo YOLOv8 (*You Only Look Once*) implementa una red neuronal convolucional profunda para extraer mapas de características de forma jerárquica (bordes -> texturas -> morfología dental).
2.  **Detección de objetos (Object Detection)**: A diferencia de la clasificación simple, la red predice coordenadas exactas de las cajas delimitadoras (*bounding boxes*) y clasifica simultáneamente el objeto detectado.
3.  **Aprendizaje supervisado (Supervised Learning)**: La red aprende mediante el cálculo continuo de funciones de pérdida (Loss Functions) que penalizan el error entre las predicciones del modelo y las anotaciones reales etiquetadas por expertos.
4.  **Aprendizaje transferido y Fine-Tuning (Transfer Learning)**: Partimos de pesos preentrenados (`yolov8n.pt` o `yolo26m.pt`) del dataset generalista COCO. Durante el *fine-tuning*, re-especializamos los filtros superiores y medios de la red hacia las densidades radiológicas del tejido dental.

---

## 3. Mapa y arquitectura del directorio `entrenamiento ia`

La arquitectura del proyecto está estructurada bajo buenas prácticas de MLOps para facilitar la reproducibilidad de los experimentos:

*   [entrenamiento ia/](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia) (Directorio Raíz)
    *   [.venv/](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/.venv): Entorno virtual de Python aislado para el control estricto de dependencias.
    *   [dataset/](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/dataset): Almacén estructurado de datos.
        *   `images/`: Splits de imágenes en subcarpetas (`train/`, `val/`, `test/`).
        *   `labels/`: Archivos `.txt` en formato YOLO y reportes de conversión.
        *   `data.yaml`: Manifiesto de dataset configurado para Ultralytics.
    *   [tools/](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/tools): Scripts CLI de automatización.
        *   [csv_to_yolo.py](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/tools/csv_to_yolo.py): ETL de conversión.
        *   [device_resolver.py](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/tools/device_resolver.py): Selección inteligente de CPU/GPU.
        *   [train_yolov8.py](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/tools/train_yolov8.py): Script de entrenamiento y afinamiento.
        *   [eval_predict_yolov8.py](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/tools/eval_predict_yolov8.py): Evaluación en validación e inferencia visual.
        *   [run_train_eval_predict_yolov8.py](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/tools/run_train_eval_predict_yolov8.py): Pipeline secuencial integrado.
    *   [tests/](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/tests): Pruebas automatizadas (smoke tests) para asegurar que ningún cambio de código rompa la ejecución.
    *   [runs/](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs): Artefactos resultantes de los entrenamientos.
        *   `train/`: Pesos (`best.pt`, `last.pt`), gráficas de resultados (`results.png`), curvas F1 y matrices de confusión.
        *   `eval_predict/`: Reportes de métricas normalizadas en JSON/CSV.
    *   [requirements.txt](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/requirements.txt): Dependencias básicas del sistema.

---

## 4. Instalación del entorno y verificación de la GPU (CUDA)

Para garantizar un rendimiento de entrenamiento óptimo, es crucial habilitar el soporte de aceleración gráfica por hardware (NVIDIA CUDA).

### 4.1 Instalación de dependencias
Ejecutar en la consola desde la raíz de `entrenamiento ia/`:

**Windows (PowerShell):**
```powershell
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

**Linux (Bash):**
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r ./requirements.txt
```

### 4.2 Configuración limpia de PyTorch con CUDA
Para evitar fallos de ejecución debido a desajustes en las compilaciones del driver gráfico, se recomienda instalar las versiones correspondientes de CUDA:

**Windows (GPU NVIDIA - CUDA 13.0 / 12.8):**
```powershell
python -m pip uninstall -y torch torchvision torchaudio
python -m pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
# Alternativa para GPUs más antiguas (CUDA 12.8):
python -m pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

**Linux (GPU NVIDIA - CUDA 13.0):**
```bash
python3 -m pip uninstall -y torch torchvision torchaudio
python3 -m pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
```

### 4.3 Verificación de estado y diagnóstico de CUDA
Para comprobar que PyTorch se comunica correctamente con el hardware y los drivers gráficos, ejecutar el siguiente diagnóstico extendido:

```powershell
python -c "import torch; print('torch', torch.__version__); print('cuda', torch.version.cuda); print('avail', torch.cuda.is_available()); print('count', torch.cuda.device_count()); print('name0', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'); x=torch.randn(512,512,device='cuda:0') if torch.cuda.is_available() else None; print('kernel_ok', x is not None)"
```

> [!WARNING]
> Si aparece el mensaje `CUDA error: no kernel image is available for execution on the device`, indica que la versión instalada de PyTorch no compila con la microarquitectura de tu tarjeta gráfica. Se debe reinstalar una variante previa de CUDA (como `cu128` o `cu124`).

---

## 5. ETL y preprocesamiento de datos: `csv_to_yolo.py`

Las anotaciones originales vienen dadas en archivos CSV estructurados con columnas tabulares: `filename, width, height, class, xmin, ymin, xmax, ymax`.

### 5.1 Conversión y normalización matemática
El script `csv_to_yolo.py` procesa recursivamente los splits del dataset. Transforma las coordenadas absolutas de píxeles a ratios relativos al centro del objeto, normales en el intervalo $[0, 1]$, tal como exige la arquitectura de entrada de YOLO:

```python
width = (xmax - xmin) / img_w
height = (ymax - ymin) / img_h
x_center = ((xmin + xmax) / 2.0) / img_w
y_center = ((ymin + ymax) / 2.0) / img_h
```

### 5.2 Control de calidad y clipping defensivo
Para proteger el entrenamiento de datos ruidosos o fallos de anotación humana, el script implementa controles de calidad automáticos en la función `row_to_box()`:
*   **Limpieza de extremos (Clipping):** Si alguna coordenada de caja delimitadora excede los bordes físicos de la imagen (por ejemplo, un valor menor a 0 o mayor que el ancho/alto en píxeles), el script limita el valor al intervalo válido mediante funciones `min()` y `max()`.
*   **Filtrado de cajas inválidas:** Descarta anotaciones con áreas nulas o invertidas ($x_{min} \ge x_{max}$ o $y_{min} \ge y_{max}$).
*   **Reporte automatizado:** Genera [dataset/conversion_report.json](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/dataset/conversion_report.json), que audita el total de imágenes procesadas, clases encontradas y cajas corregidas.

---

## 6. Arquitectura detallada de scripts y funciones de `tools/`

La automatización de procesos en el proyecto está encapsulada en cinco componentes clave:

### 6.1 `device_resolver.py`
Proporciona lógica resiliente para mapear las peticiones del hardware.
*   **`DeviceResolution`**: Dataclass que encapsula el dispositivo solicitado, el resuelto y posibles advertencias.
*   **`resolve_device(requested_device)`**: Traduce `--device auto` a la GPU `0` si está disponible, o cae en `cpu` con una advertencia si se solicita CUDA pero no hay aceleración física activa.

### 6.2 `csv_to_yolo.py`
Orquesta la transformación del dataset.
*   **`collect_classes(dataset_root, csv_name)`**: Escanea dinámicamente los splits para listar clases sin hardcodearlas.
*   **`convert_split(...)`**: Ejecuta la conversión por split, verificando la presencia física del archivo de imagen antes de crear su etiqueta homónima `.txt`.
*   **`write_data_yaml(...)`**: Genera el manifiesto que vincula los directorios de imágenes de validación/entrenamiento y los nombres de las clases.

### 6.3 `train_yolov8.py`
Configura y arranca las fases de entrenamiento.
*   **`build_train_kwargs(args)`**: Mapea los argumentos CLI del usuario al formato clave-valor aceptado por Ultralytics.
*   **`main()`**: Reconfigura dinámicamente los directorios base de salida de Ultralytics hacia `entrenamiento ia/runs` para evitar desorganización en el disco.
*   **Inyección de hiperparámetros y filtrado de colisiones:** Permite alimentar el entrenamiento con una receta externa (`best_hyperparameters.yaml` o `--cfg`). El script implementa un filtro que descarta del archivo de entrada parámetros que colisionen con las variables CLI obligatorias del usuario (como `device`, `epochs` y `batch`).

### 6.4 `eval_predict_yolov8.py`
Extrae las métricas finales y genera predicciones en test.
*   **`extract_metrics(metrics_obj)`**: Convierte tensores de Ultralytics (que provocan errores de serialización JSON) a escalares nativos de Python.
*   **`write_metrics_files(...)`**: Exporta los resultados tanto en un archivo JSON legible para automatizaciones como en un CSV para análisis en Excel/Python.
*   **`write_run_report(...)`**: Genera una bitácora técnica (`run_report.json`) con las rutas físicas de los pesos evaluados y los parámetros utilizados.

### 6.5 `run_train_eval_predict_yolov8.py`
Pipeline de extremo a extremo que automatiza el ciclo completo:
1.  Recibe la configuración inicial.
2.  Lanza el entrenamiento (`train_yolov8.py`) y genera una carpeta única identificada por marca de tiempo UTC.
3.  Localiza dinámicamente el mejor peso entrenado (`best.pt`).
4.  Ejecuta la validación (`eval_predict_yolov8.py`) sobre ese peso.
5.  Consolida un reporte único en `runs/pipeline/pipeline_report.json`.

---

## 7. Evolución del fine-tuning e hiperparámetros

Encontrar el mejor modelo clínico requirió avanzar de manera metódica a través de cinco etapas diferenciadas:

```
[dental_yolov8] (Base/Default) -> Sobreajuste a la época 52 (71.8% mAP50)
        │
        ▼ (Aplicar Transfer Learning y Congelación)
[dental_yolo26n_laptop] (Freeze 10) -> Aprendizaje estable, muy conservador (69.3% mAP50)
        │
        ▼ (Ajuste del volumen de congelación)
[dental_yolo26n_laptop_freeze5] (Freeze 5) -> Equilibrio de Precisión/Recall (72.2% mAP50)
        │
        ▼ (Búsqueda de optimización sin congelación)
[dental_nofreeze_suave] (Nano, LR 0.0005) -> Ganador en categoría ligera (75.5% mAP50)
        │
        ▼ (Escalar la arquitectura del modelo)
[dental_nofreeze_suave_yolo26m] (Medium, 1024px) -> Salto monumental (82.19% mAP50)
        │
        ▼ (Tuning Genético de 10 iteraciones y entrenamiento final)
[dental_definitivo_optimizado_medium] (Best LR/Augmentation) -> Modelo de Producción (83.08% mAP50)
```

### El éxito del tuning genético de hiperparámetros

Para la fase definitiva del proyecto, se implementó una estrategia avanzada de optimización de hiperparámetros utilizando la funcionalidad de tuning genético (`--tune`) sobre la arquitectura YOLOv8 Medium. En lugar de aplicar técnicas de búsqueda tradicionales y costosas como la búsqueda en cuadrícula (grid search) o la búsqueda aleatoria pura, se empleó un algoritmo evolutivo basado en mutaciones para descubrir el equilibrio de aumentos de datos e hiperparámetros de entrenamiento más adecuado para el dominio específico de la radiología dental.

#### Mecánica de la búsqueda evolutiva
La búsqueda constó de un proceso iterativo detallado a continuación:
* **Estrategia y duración**: Se configuró un ciclo de 10 iteraciones de entrenamiento. Cada iteración consistió en un entrenamiento de prueba corto y controlado de 15 épocas sobre el modelo base.
* **Proceso de mutación**: En la primera iteración, el algoritmo parte de los hiperparámetros predeterminados de YOLOv8. En las iteraciones subsecuentes, el optimizador genético analiza los resultados históricos y muta (aplica pequeñas variaciones aleatorias guiadas) parámetros críticos, incluyendo la tasa de aprendizaje, el momento, el decaimiento de pesos y las probabilidades de técnicas de aumento de datos (como la mezcla y el mosaico).
* **Métrica de selección (Fitness)**: El algoritmo evalúa el éxito de cada configuración a través de una función de aptitud o fitness que combina de manera ponderada mAP50 y mAP50-95. Aquellas combinaciones con mayor puntuación guían la dirección de las mutaciones de la siguiente generación.

#### Descubrimiento en épocas cortas e iteración ganadora
La búsqueda genética arrojó sus mejores frutos de forma temprana:
* **El punto óptimo (iteración 2)**: Durante la iteración 2 del proceso (cuyos resultados se almacenaron en la carpeta [train5](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/train5)), el algoritmo evolutivo descubrió una combinación excepcional que alcanzó un **fitness de 0.55753** (mAP50-95) y un **mAP50 de 0.803** (80.34%) en tan solo 15 épocas.
* **Eficiencia del proceso**: Este hallazgo preliminar demostró que no era necesario entrenar cientos de épocas por cada combinación para predecir qué hiperparámetros tendrían un rendimiento superior en el entrenamiento definitivo de larga duración.

#### Parámetros mutados y justificación clínica de la receta
La configuración óptima obtenida a través de la evolución biológica simulada difiere sustancialmente de la configuración por defecto de YOLOv8. Cada uno de estos cambios tiene una justificación técnica y clínica directa:
* **Tasa de aprendizaje inicial moderada (`lr0: 0.00403`)**: El valor estándar de YOLOv8 (0.01) suele ser demasiado agresivo para imágenes médicas en escala de grises. Una tasa de aprendizaje reducida a 0.00403 evita las oscilaciones bruscas del gradiente en el espacio de características de baja variación cromática de las radiografías dentales, permitiendo una convergencia más fina y estable.
* **Momento elevado (`momentum: 0.98`)**: Se incrementó respecto al valor estándar (0.937). Al tener un learning rate inicial más bajo y controlado, un momento alto actúa como un acelerador de la dirección del gradiente, permitiendo que el optimizador continúe avanzando firmemente a través de valles planos en la superficie de pérdida, reduciendo el riesgo de estancamiento.
* **Decaimiento de peso nulo (`weight_decay: 0.0`)**: La regularización por decaimiento de peso penaliza los pesos de gran magnitud para evitar sobreajuste. Sin embargo, en radiografías dentales, las patologías como caries incipientes, reabsorciones óseas y microfisuras se representan como variaciones sutiles y diminutas de textura que ocupan unos pocos píxeles. Poner este parámetro a 0.0 evita que la red atenúe o suprima filtros de extracción de características finas y sutiles en las primeras capas.
* **Calentamiento de épocas prolongado (`warmup_epochs: 3.01`)**: Ofrece una transición más progresiva al inicio del entrenamiento, permitiendo que los pesos se estabilicen antes de aplicar la tasa de aprendizaje completa seleccionada.
* **Desactivación del mosaico al final (`close_mosaic: 10`)**: La técnica de Data Augmentation de mosaico combina cuatro imágenes de entrenamiento en una sola cuadrícula. Aunque esto ayuda a detectar objetos a distintas escalas en conjuntos de datos genéricos, introduce bordes e intersecciones artificiales que pueden confundir al modelo al evaluar contornos óseos continuos y morfología dental real. Desactivar el mosaico durante las últimas 10 épocas permite que el modelo refine sus predicciones sobre la geometría natural y anatómica de las radiografías clínicas sin interferencias artificiales de límites rectangulares.

#### Aplicación práctica en el modelo definitivo
Para trasladar el conocimiento extraído por el algoritmo evolutivo al entrenamiento final de producción, se procedió de la siguiente manera técnica:
1. **Exportación de la receta**: Al completarse las 10 iteraciones de búsqueda, Ultralytics guardó los hiperparámetros ganadores en un archivo de configuración estructurado en formato YAML, denominado [best_hyperparameters.yaml](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_tuning_medium_hiperparametros/best_hyperparameters.yaml).
2. **Inyección en el comando de entrenamiento**: En lugar de configurar manualmente las tasas de aprendizaje o los aumentos de datos por línea de comandos, se utilizó el argumento `--cfg` en la llamada a la herramienta de entrenamiento para apuntar directamente a dicho archivo de configuración optimizado.
3. **Comando ejecutado**:
   ```powershell
   python .\tools\train_yolov8.py --data .\dataset\data.yaml --model yolo26m.pt --epochs 150 --imgsz 1024 --batch 7 --cfg .\runs\train\dental_tuning_medium_hiperparametros\best_hyperparameters.yaml --name "dental_definitivo_optimizado_medium"
   ```
4. **Beneficios clínicos y operativos del método**: Esta integración automatizada no solo eliminó el error humano de transcribir parámetros mutados decimales complejos, sino que garantizó que el modelo heredara los incrementos de aumentos de datos específicos y el decaimiento de peso nulo exacto determinados evolutivamente. Esto permitió extender con total fidelidad el comportamiento de alta precisión del experimento de 15 épocas a lo largo del entrenamiento extendido de 150 épocas.

#### Impacto cuantitativo en el modelo final
La verdadera validación del tuning genético se observó al aplicar esta receta en el entrenamiento de producción a gran escala:
* **El experimento definitivo**: Se entrenó el modelo final [dental_definitivo_optimizado_medium](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_definitivo_optimizado_medium) durante 150 épocas utilizando los hiperparámetros mutados y una resolución de 1024px, alcanzando su mejor punto de convergencia en la época 86.
* **Comparativa del mAP50**:
  * **+11.3%** de incremento sobre el modelo base de control YOLOv8 Nano (`dental_yolov8`, que obtuvo un 71.79% mAP50).
  * **+1.0%** de incremento sobre el modelo YOLOv8 Medium equivalente que no utilizó la optimización por tuning genético (`dental_nofreeze_suave_yolo26m`, que obtuvo un 82.19% mAP50).
* **Robustez general**: El modelo definitivo alcanzó un **mAP50 final de 0.8308** (83.08%) y un mAP50-95 de 0.5398 (53.98%), logrando un equilibrio excelente entre precisión clínica (76.51%) y sensibilidad/recall (79.21%), minimizando los falsos negativos en diagnósticos sensibles.


---

## 8. Resultados y comparativa de los últimos entrenamientos

A continuación, se detalla la tabla comparativa oficial de todas las ejecuciones realizadas en el servidor del proyecto, ordenadas rigurosamente de mayor a menor precisión de detección global (mAP50):

| Pos | Experimento | Arquitectura Base | Resolución | Épocas (Realizadas/Max) | Batch | Capas Congeladas | LR Inicial | Best Epoch | mAP50 (Best) | mAP50-95 (Best) | Precisión (Best) | Recall (Best) |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **[dental_definitivo_optimizado_medium](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_definitivo_optimizado_medium)** | `yolo26m.pt` (Medium) | **1024px** | **89 / 150** | **7** | **Ninguna** | **0.00403** | **86** | **0.8308** | **0.5398** | **0.7651** | **0.7921** |
| 2 | [dental_nofreeze_suave_yolo26m](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_nofreeze_suave_yolo26m) | `yolo26m.pt` (Medium) | 1024px | 63 / 150 | 4 | Ninguna | 0.00050 | 39 | **0.8219** | 0.5464 | 0.8534 | 0.7287 |
| 3 | [train6 (Tuning Iteración 2)](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/train6) | `yolo26m.pt` (Medium) | 640px | 15 / 15 | 14 | Ninguna | 0.00603 | 13 | **0.7994** | 0.5368 | 0.8162 | 0.7560 |
| 4 | [train4 (Tuning Iteración 0)](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/train4) | `yolo26m.pt` (Medium) | 640px | 15 / 15 | 14 | Ninguna | 0.01000 | 15 | **0.7991** | 0.5508 | 0.7680 | 0.7901 |
| 5 | [dental_nofreeze_suave](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_nofreeze_suave) | `yolo26n.pt` (Nano) | 800px | 97 / 150 | 8 | Ninguna | 0.00050 | 79 | **0.7551** | 0.4914 | 0.8043 | 0.7137 |
| 6 | [dental_alta_resolucion](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_alta_resolucion) | `yolo26n.pt` (Nano) | 1024px | 97 / 150 | 4 | 5 | 0.00100 | 50 | **0.7413** | 0.4842 | 0.7256 | 0.7153 |
| 7 | [dental_regularizado](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_regularizado) | `yolo26n.pt` (Nano) | 800px | 99 / 150 | 8 | 5 | 0.00100 | 40 | **0.7375** | 0.4771 | 0.8002 | 0.6506 |
| 8 | [dental_yolo26n_laptop_freeze5](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_yolo26n_laptop_freeze5) | `yolo26n.pt` (Nano) | 800px | 95 / 150 | 8 | 5 | 0.00100 | 66 | **0.7342** | 0.4752 | 0.6819 | 0.7619 |
| 9 | [dental_definitivo](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_definitivo) | `yolo26n.pt` (Nano) | 1024px | 80 / 150 | 16 | Ninguna | 0.00050 | 49 | **0.7208** | 0.4727 | 0.7582 | 0.6612 |
| 10 | [dental_yolov8 (Modelo Control)](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_yolov8) | `yolo26n.pt` (Nano) | 640px | 52 / 100 | 16 | Ninguna | 0.01000 | 44 | **0.7179** | 0.4686 | 0.6805 | 0.6835 |
| 11 | [dental_yolo26n_laptop](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_yolo26n_laptop) | `yolo26n.pt` (Nano) | 800px | 119 / 150 | 8 | 10 | 0.00100 | 80 | **0.6935** | 0.4664 | 0.6590 | 0.6867 |
| 12 | [train2](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/train2) | `yolo26n.pt` (Nano) | 640px | 15 / 15 | 16 | Ninguna | 0.00386 | 15 | **0.6255** | 0.4194 | 0.6123 | 0.5863 |
| 13 | [train](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/train) | `yolo26n.pt` (Nano) | 640px | 4 / 15 | 16 | Ninguna | 0.00124 | 4 | **0.4849** | 0.3123 | 0.7269 | 0.4516 |

### Análisis de variables clave en los resultados

1.  **Escala del modelo (YOLO Nano vs Medium):** El salto de capacidad representacional de Nano (`yolo26n.pt`) a Medium (`yolo26m.pt`) generó el incremento de precisión más drástico, superando la barrera del 80% de mAP50. La complejidad estructural de las ortopantomografías requiere la capacidad matemática superior de un modelo más profundo.
2.  **Resolución de imagen (640px vs 800px vs 1024px):** Subir la resolución a 1024px permite que el modelo distinga caries incipientes (que a 640px ocupaban menos de $3\times3$ píxeles, perdiéndose en las capas de reducción espacial). El modelo definitivo a 1024px lidera la clasificación.
3.  **Congelación de capas (`freeze`):** En dominios altamente especializados (como radiografía médica en escala de grises), la congelación severa limita la adaptación. El entrenamiento completo de la red (`freeze: None`) con un learning rate refinado y suave demostró ser sustancialmente superior.

---

## 9. Interpretación de los artefactos gráficos clínicos

Durante el examen ante el tribunal, es vital demostrar que sabemos interpretar las gráficas de entrenamiento generadas en la carpeta de resultados (como las de `dental_nofreeze_suave_yolo26m`):

### 9.1 Diagnóstico de aprendizaje (`results.png`)
*   Muestra las curvas de pérdida (*loss*) en entrenamiento y validación.
*   **Box Loss / Class Loss**: Observamos que ambas líneas descienden de manera suave y paralela.
*   **Verificación de overfitting**: Dado que el *validation loss* nunca rebota hacia arriba mientras el *training loss* sigue bajando, se demuestra que el modelo ha aprendido patrones generalizables y no ha memorizado el dataset.

### 9.2 Curva precision-recall (`PR_curve.png`)
*   Representa la tasa de acierto frente a la exhaustividad del modelo.
*   Cuanto más cercana esté la curva a la esquina superior derecha, mayor es la calidad clínica. Las curvas de **Implantes** y **Dientes impactados** muestran áreas bajo la curva (AUC) de casi el **90%**, confirmando detecciones extremadamente fiables.

### 9.3 Matriz de confusión (`confusion_matrix.png`)
*   Cruza el diagnóstico real con la predicción del modelo.
*   **Diagonal principal**: Concentra los aciertos. Los implantes e impactos destacan por encima del 85%.
*   **Confusiones clínicas**: Las caries registran un ligero cruce con falsos positivos en el "Background" (ruido radiológico o sombras anatómicas). Es un comportamiento esperado en diagnóstico odontológico, donde las caries pequeñas pueden confundirse visualmente con la superposición de estructuras óseas.

### 9.4 Visualización de inferencia (`val_batch0_labels.jpg` vs `val_batch0_pred.jpg`)
*   Permite auditar el comportamiento del modelo de forma cualitativa.
*   El archivo `labels` contiene el diagnóstico humano de control.
*   El archivo `pred` dibuja las cajas predichas por la red neuronal con su porcentaje de confianza. Nos permite certificar visualmente la capacidad de la IA para aislar patologías en condiciones reales.

---

## 10. Guía de operación y despliegue en producción

### 10.1 Comandos de ejecución diaria

**Paso 1: Convertir etiquetas y preparar dataset:**
```powershell
python .\tools\csv_to_yolo.py --dataset-root .\dataset
```

**Paso 2: Entrenar el modelo con la mejor receta de hiperparámetros:**
```powershell
python .\tools\train_yolov8.py --data .\dataset\data.yaml --model yolo26m.pt --epochs 150 --imgsz 1024 --batch 7 --cfg .\runs\train\dental_tuning_medium_hiperparametros\best_hyperparameters.yaml --name "dental_definitivo_optimizado_medium"
```

**Paso 3: Validar y predecir en un solo comando:**
```powershell
python .\tools\eval_predict_yolov8.py --task both --data .\dataset\data.yaml --source .\dataset\images\test --model .\runs\train\dental_definitivo_optimizado_medium\weights\best.pt --device auto
```

### 10.2 Presets para evitar errores de memoria (VRAM OOM)
Si el hardware de ejecución tiene restricciones térmicas o de memoria VRAM, utiliza los siguientes perfiles de comando:

*   **Preset `GPU segura` (Portátiles de desarrollo / Menos de 6GB VRAM):**
    ```powershell
    python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --model yolo26n.pt --epochs 120 --imgsz 640 --batch 4 --device 0 --task both
    ```
*   **Preset `GPU agresiva` (Estación de trabajo / Más de 12GB VRAM):**
    ```powershell
    python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --model yolo26m.pt --epochs 200 --imgsz 1024 --batch 8 --device 0 --task both
    ```

### 10.3 Ejecución de baterías de tests
Para verificar que el sistema es robusto y que ninguna modificación del código interrumpe el pipeline MLOps, corre los tests unitarios con `pytest`:
```powershell
python -m pytest .\tests\test_csv_to_yolo_smoke.py
python -m pytest .\tests\test_train_yolov8_smoke.py
python -m pytest .\tests\test_eval_predict_yolov8_smoke.py
python -m pytest .\tests\test_run_train_eval_predict_yolov8_smoke.py
```

### 10.4 Despliegue clínico optimizado (ONNX)
Para integrar el modelo en una aplicación de interfaz de usuario clínica (por ejemplo, construida en Vue/Electron o Django) sin arrastrar la pesada dependencia de PyTorch, exportamos los pesos a formato **ONNX**:

```python
from ultralytics import YOLO

# Cargar el modelo final entrenado
model = YOLO("runs/train/dental_definitivo_optimizado_medium/weights/best.pt")

# Exportar con optimización de CPU/GPU
model.export(format="onnx", imgsz=1024, half=False)
```

*   **Inferencia real-time**: El archivo `best.onnx` resultante permite realizar inferencias en milisegundos directamente en el navegador o backend liviano.
*   **Test-time augmentation (TTA)**: Se aconseja habilitar TTA en inferencia de producción para aumentar la sensibilidad sobre caries diminutas sin alterar la velocidad del pipeline principal.

---

## 11. Documentación de pruebas y entregables del proyecto

Para la defensa del proyecto final y como parte del ciclo de vida de MLOps, se ha consolidado un conjunto de entregables técnicos y de presentación en la carpeta [Documentación de pruebas](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/Documentaci%C3%B3n%20de%20pruebas). Estos archivos estructuran la evidencia empírica del rendimiento de los modelos y facilitan la comunicación de los hallazgos ante el tribunal y personal clínico.

### 11.1 Catálogo de entregables clínicos y académicos

Los archivos contenidos en este directorio se dividen en tres categorías fundamentales según su propósito:

#### A. Soporte para la defensa y presentación visual
*   [Precision_Dental_AI.pptx](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/Documentaci%C3%B3n%20de%20pruebas/Precision_Dental_AI.pptx): Presentación formal de diapositivas diseñada para la exposición oral. Sintetiza los objetivos del proyecto, la arquitectura del pipeline de datos, la metodología de entrenamiento, la comparativa de modelos (Nano vs. Medium), el impacto de la resolución de imagen y las conclusiones del despliegue.

#### B. Informes técnicos de rendimiento y comparativa
*   [comparacion_resultados.docx](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/Documentaci%C3%B3n%20de%20pruebas/comparacion_resultados.docx): Memoria escrita formal en formato Microsoft Word. Detalla todo el proceso experimental, el análisis de métricas clínicas y la justificación de las decisiones de diseño del modelo.
*   [runs_comparison_report.pdf](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/Documentaci%C3%B3n%20de%20pruebas/runs_comparison_report.pdf): Versión portátil y de lectura fija del informe de comparación de entrenamientos, ideal para distribución digital oficial.
*   [runs_comparison_report.md](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/Documentaci%C3%B3n%20de%20pruebas/runs_comparison_report.md): Versión en formato Markdown del mismo informe, optimizada para visualización rápida en repositorios de código e integración directa en la documentación del proyecto.

#### C. Datos estructurados de los experimentos
*   [Comparativa de experimentos de entrenamiento YOLO para radiografías dentales - Table 1.csv](file:///c:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/Documentaci%C3%B3n%20de%20pruebas/Comparativa%20de%20Experimentos%20de%20Entrenamiento%20YOLO%20para%20Radiograf%C3%ADas%20Dentales%20-%20Table%201.csv): Matriz de datos consolidada con las métricas clave de las 10 pruebas más importantes. Facilita la carga de datos en entornos de análisis (como cuadernos Jupyter con Pandas o tableros de visualización de BI).

---

### 11.2 Estructura y métricas oficiales de validación (CSV)

La siguiente tabla sintetiza la información oficial extraída del archivo CSV de resultados, la cual representa la base empírica de nuestra comparativa de modelos:

| Modelo de entrenamiento | Arquitectura de red | Configuración (freeze/LR/imgsz) | mAP50 | mAP50-95 | Precisión | Recall | Época óptima | Estado de entrenamiento |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **dental_definitivo_optimizado_medium** | `yolo26m.pt` | Freeze: None / LR: 0.00403 / Imgsz: 1024 | **0.831** | **0.540** | 0.765 | 0.792 | 86 | Entrenamiento completo (Optimizado) |
| **dental_nofreeze_suave_yolo26m** | `yolo26m.pt` | Freeze: None / LR: 0.0005 / Imgsz: 1024 | **0.822** | **0.546** | 0.853 | 0.729 | 39 | Entrenamiento completo (Early Stopping) |
| **dental_tuning_medium_hiperparámetros** | `yolo26m.pt` | Freeze: None / LR: Variable / Imgsz: 640 | **0.803** | **0.558** | 0.740 | 0.804 | 15 | Búsqueda de hiperparámetros (Tuning) |
| **dental_nofreeze_suave** | `yolo26n.pt` | Freeze: None / LR: 0.0005 / Imgsz: 800 | **0.755** | **0.491** | 0.804 | 0.714 | 79 | Entrenamiento completo (Early Stopping) |
| **dental_alta_resolucion** | `yolo26n.pt` | Freeze: 5 / LR: 0.001 / Imgsz: 1024 | **0.741** | **0.484** | 0.726 | 0.715 | 50 | Entrenamiento completo (Early Stopping) |
| **dental_regularizado** | `yolo26n.pt` | Freeze: 5 / LR: 0.001 / Imgsz: 800 | **0.738** | **0.477** | 0.800 | 0.651 | 40 | Entrenamiento completo (Early Stopping) |
| **dental_yolo26n_laptop_freeze5** | `yolo26n.pt` | Freeze: 5 / LR: 0.001 / Imgsz: 800 | **0.734** | **0.475** | 0.682 | 0.762 | 66 | Entrenamiento completo (Early Stopping) |
| **dental_definitivo** | `yolo26n.pt` | Freeze: None / LR: 0.0005 / Imgsz: 1024 | **0.721** | **0.473** | 0.758 | 0.661 | 49 | Entrenamiento completo (Early Stopping) |
| **dental_yolov8** | `yolo26n.pt` | Freeze: None / LR: 0.01 / Imgsz: 640 | **0.718** | **0.469** | 0.681 | 0.684 | 44 | Entrenamiento completo (Original) |
| **dental_yolo26n_laptop** | `yolo26n.pt` | Freeze: 10 / LR: 0.001 / Imgsz: 800 | **0.694** | **0.466** | 0.659 | 0.687 | 80 | Entrenamiento completo (Early Stopping) |

---

### 11.3 Hallazgos clínico-técnicos clave del informe comparativo

Del análisis de la documentación de pruebas se extraen tres directrices metodológicas fundamentales para el desarrollo de sistemas de visión artificial en odontología:

1.  **Impacto del escalamiento de capacidad (Nano vs. Medium)**: Los modelos que emplean la arquitectura Medium (`yolo26m.pt`) superan sistemáticamente la barrera del **80% de mAP50**. Esto confirma que la escala "Medium" proporciona el balance óptimo entre parámetros y poder de representación para mapear las sutiles texturas óseas y dentales de las ortopantomografías.
2.  **Influencia de la resolución espacial**: Aumentar la resolución de entrada a **1024px** es crítico. Dado que las lesiones de caries representan objetos clínicamente muy pequeños, la alta resolución espacial evita que estas características se difuminen en las capas profundas de la red convolucional.
3.  **Filosofía de fine-tuning completo**: Desactivar la congelación de capas (`Freeze: None`) en combinación con tasas de aprendizaje suaves (`lr0: 0.00403` o `0.0005`) produce mejores resultados que congelar capas del backbone (`Freeze: 5` o `10`). Esto se debe a que las características del preentrenamiento genérico (COCO dataset) difieren sustancialmente de la radiología dental, requiriendo una adaptación completa de los extractores de características de la red.
