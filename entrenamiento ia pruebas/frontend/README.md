# Frontend de detección dental (YOLOv8)

Este frontend permite subir una radiografia dental, ejecutar inferencia con YOLO (`best.pt`) y ver:

- tabla de detecciones (clase, confianza y bbox)
- la misma imagen con recuadros
- seleccionar desde la tabla qué recuadros se muestran, con todos activos por defecto
- opcion de descarga de la imagen anotada

## Requisitos

- Dependencias del proyecto instaladas (`requirements.txt`)
- Modelo `best.pt` en la raiz de `entrenamiento ia`

## Ejecutar

Desde la raiz del proyecto (`entrenamiento ia`):

```powershell
python -m streamlit run .\frontend\app.py
```

Si el modelo no esta en la ruta por defecto, puedes cambiarlo en el campo `Ruta del modelo YOLO (.pt)`.

