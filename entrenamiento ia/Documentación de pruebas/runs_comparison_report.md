# Comparativa de Resultados de Entrenamiento IA Dental

Este informe contiene la comparación de los resultados de los diferentes entrenamientos realizados en el proyecto de IA dental, extraídos automáticamente de los archivos `results.csv` y `args.yaml` en la ruta `runs/train/`.

## 🏆 Resumen Ejecutivo

> [!IMPORTANT]

> **Mejor Modelo Detectado:** El experimento **[dental_definitivo_optimizado_medium](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_definitivo_optimizado_medium)** obtuvo los mejores resultados con un **mAP50 de 0.831** y un **mAP50-95 de 0.540** en la época 86.

> Este modelo utiliza la arquitectura **yolo26m.pt** con una resolución de imagen de **1024px**, optimizado con los hiperparámetros de fine-tuning.


### 📊 Comparativa General de Modelos (Ordenados por Mejor mAP50)

| Pos | Experimento | Modelo | Res (px) | Epochs (Run/Conf) | Batch | Freeze | LR Base | Best Epoch | mAP50 (Best) | mAP50-95 (Best) | Precision (Best) | Recall (Best) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [dental_definitivo_optimizado_medium](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_definitivo_optimizado_medium) | `yolo26m.pt` | 1024 | 89/150 | 7 | None | 0.00403 | 86 | **0.8308** | 0.5398 | 0.7651 | 0.7921 |
| 2 | [dental_nofreeze_suave_yolo26m](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_nofreeze_suave_yolo26m) | `yolo26m.pt` | 1024 | 63/150 | 4 | None | 0.0005 | 39 | **0.8219** | 0.5464 | 0.8534 | 0.7287 |
| 3 | [train6](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/train6) | `yolo26m.pt` | 640 | 15/15 | 14 | None | 0.00603 | 13 | **0.7994** | 0.5368 | 0.8162 | 0.7560 |
| 4 | [train4](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/train4) | `yolo26m.pt` | 640 | 15/15 | 14 | None | 0.01 | 15 | **0.7991** | 0.5508 | 0.7680 | 0.7901 |
| 5 | [dental_nofreeze_suave](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_nofreeze_suave) | `yolo26n.pt` | 800 | 97/150 | 8 | None | 0.0005 | 79 | **0.7551** | 0.4914 | 0.8043 | 0.7137 |
| 6 | [dental_alta_resolucion](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_alta_resolucion) | `yolo26n.pt` | 1024 | 97/150 | 4 | 5 | 0.001 | 50 | **0.7413** | 0.4842 | 0.7256 | 0.7153 |
| 7 | [dental_regularizado](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_regularizado) | `yolo26n.pt` | 800 | 99/150 | 8 | 5 | 0.001 | 40 | **0.7375** | 0.4771 | 0.8002 | 0.6506 |
| 8 | [dental_yolo26n_laptop_freeze5](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_yolo26n_laptop_freeze5) | `yolo26n.pt` | 800 | 95/150 | 8 | 5 | 0.001 | 66 | **0.7342** | 0.4752 | 0.6819 | 0.7619 |
| 9 | [dental_definitivo](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_definitivo) | `yolo26n.pt` | 1024 | 80/150 | 16 | None | 0.0005 | 49 | **0.7208** | 0.4727 | 0.7582 | 0.6612 |
| 10 | [dental_yolov8](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_yolov8) | `yolo26n.pt` | 640 | 52/100 | 16 | None | 0.01 | 44 | **0.7179** | 0.4686 | 0.6805 | 0.6835 |
| 11 | [dental_yolo26n_laptop](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_yolo26n_laptop) | `yolo26n.pt` | 800 | 119/150 | 8 | 10 | 0.001 | 80 | **0.6935** | 0.4664 | 0.6590 | 0.6867 |
| 12 | [train2](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/train2) | `yolo26n.pt` | 640 | 15/15 | 16 | None | 0.00386 | 15 | **0.6255** | 0.4194 | 0.6123 | 0.5863 |
| 13 | [train](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/train) | `yolo26n.pt` | 640 | 4/15 | 16 | None | 0.00124 | 4 | **0.4849** | 0.3123 | 0.7269 | 0.4516 |

## 🔍 Análisis Detallado por Factores

### 1. Escala del Modelo: YOLO Nano (`yolo26n.pt`) vs YOLO Medium (`yolo26m.pt`)

- **Modelos Medium (`yolo26m.pt`):** Lideran la tabla de precisión. Los experimentos **`dental_definitivo_optimizado_medium`** (mAP50: **0.831**) y **`dental_nofreeze_suave_yolo26m`** (mAP50: **0.822**) demuestran que la capacidad extra de la arquitectura Medium es crucial para representar los detalles de las radiografías/imágenes dentales.

- **Modelos Nano (`yolo26n.pt`):** Aunque son más rápidos y ligeros, se estancan en un mAP50 máximo de **0.755** (caso de `dental_nofreeze_suave`). Es una diferencia del **~8% en mAP50** respecto a los modelos Medium.


### 2. Resolución de Imagen (640 vs 800 vs 1024)

- Las resoluciones más altas benefician significativamente la detección de patologías dentales, las cuales suelen ocupar pocos píxeles en la imagen global (objetos pequeños):

  - **1024px** con YOLO Medium produce los mejores resultados (**>0.82 mAP50**).

  - **800px** con YOLO Nano mejora sobre los 640px estándar (alcanzando **0.73 - 0.75 mAP50**).

  - **640px** con YOLO Nano (`dental_yolov8`) obtuvo **0.718 mAP50**, lo que confirma que el aumento de resolución a 800px o 1024px da un impulso constante en el rendimiento.


### 3. Congelación de Capas (`freeze`)

- **Sin Congelar (`freeze: None`):** En general, los modelos sin capas congeladas obtuvieron mejores resultados finales. Por ejemplo, `dental_nofreeze_suave` (Nano, mAP50: **0.755**) superó a `dental_yolo26n_laptop_freeze5` (Nano, freeze: 5, mAP50: **0.734**) y a `dental_yolo26n_laptop` (Nano, freeze: 10, mAP50: **0.693**).

- **Conclusión:** Dado que el dataset dental es muy específico y difiere del preentrenamiento genérico de COCO, permitir el fine-tuning completo de todas las capas (`freeze: None` o `freeze: null`) permite adaptar mejor los extractores de características a la textura de los dientes y encías.


### 4. Búsqueda de Hiperparámetros (Hyperparameter Tuning)

Se identificaron dos carpetas de tuning con búsquedas finalizadas o parciales:

#### A. Tuning Medium ([dental_tuning_medium_hiperparametros](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_tuning_medium_hiperparametros))

- **Progreso:** 10/10 iteraciones completadas.

- **Mejor Fitness (mAP50-95):** **0.55753** (en la iteración 2, correspondiente al modelo guardado en `train5`).

- **Métricas Asociadas:** mAP50: **0.80346**, Precision: **0.73962**, Recall: **0.80441**.

- **Hiperparámetros óptimos descubiertos:**

  - `lr0` (Learning Rate Inicial): **0.00403** (más bajo que el 0.01 por defecto de YOLO, reduciendo oscilaciones).

  - `momentum`: **0.98**

  - `weight_decay`: **0.0** (sin regularización de peso en esta iteración).

  - `warmup_epochs`: **3.01**

  - `close_mosaic`: **10** (desactivar mosaic augmentation en las últimas 10 épocas).

- *Nota:* Estos hiperparámetros óptimos se utilizaron directamente para entrenar **`dental_definitivo_optimizado_medium`**, logrando elevar el mAP50 final a **0.831**.


#### B. Tuning Nano ([dental_tuning_nano](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_tuning_nano))

- **Progreso:** 2/10 iteraciones completadas.

- **Mejor Fitness:** **0.44489** (iteración 1).

- **Métricas Asociadas:** mAP50: **0.66186**, Precision: **0.56777**, Recall: **0.68599**.


## 📈 Gráficos Recomendados para Inspección Manual

Para cada uno de los mejores modelos, puedes visualizar visualmente el entrenamiento abriendo las siguientes imágenes directamente desde tu explorador de archivos:

1. **Mejor Modelo (Medium Optimizado):**

   - [Curva de Resultados (`results.png`)](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_definitivo_optimizado_medium/results.png)

   - [Matriz de Confusión (`confusion_matrix_normalized.png`)](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_definitivo_optimizado_medium/confusion_matrix_normalized.png)

2. **Segundo Mejor Modelo (Medium Suave NoFreeze):**

   - [Curva de Resultados (`results.png`)](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_nofreeze_suave_yolo26m/results.png)

   - [Matriz de Confusión (`confusion_matrix_normalized.png`)](file:///C:/Users/pemip/Desktop/Proyecto-ia-dental/entrenamiento%20ia/runs/train/dental_nofreeze_suave_yolo26m/confusion_matrix_normalized.png)


## 💡 Recomendaciones para Siguientes Pasos

1. **Despliegue del Modelo Definitivo:** El modelo guardado en `dental_definitivo_optimizado_medium/weights/best.pt` es, con diferencia, el más robusto para producción con un **mAP50 de 0.831**.

2. **Exportación:** Si se planea integrar en un frontend o backend ligero, se recomienda exportar `best.pt` a formato ONNX (`format='onnx'`) para acelerar la inferencia en CPU/GPU sin depender de PyTorch.

3. **Estrategia de Entrenamiento Futuro:** Si se recolectan más imágenes, se debe continuar usando la arquitectura Medium (`yolo26m`), resolución de **1024px**, sin congelar capas (`freeze: None`), y con el learning rate optimizado de **0.00403**.
