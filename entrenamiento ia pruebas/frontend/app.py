#!/usr/bin/env python3
"""Frontend Streamlit para inferencia dental con YOLOv8."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from .inference import default_model_path, draw_detections, load_yolo_model, run_inference
except ImportError:
    # Soporta ejecucion con `streamlit run frontend/app.py`.
    from inference import default_model_path, draw_detections, load_yolo_model, run_inference


st.set_page_config(page_title="Detector Dental YOLO", layout="wide")
st.title("Detección dental en radiografías (YOLOv8)")
st.caption("Sube una radiografia y obtendràs detecciones + imagen anotada con recuadros.")


@st.cache_resource
def get_model(model_path: str):
    return load_yolo_model(model_path)


default_model = str(default_model_path())
model_path = st.text_input("Ruta del modelo YOLO (.pt)", value=default_model) or default_model
col_left, col_right = st.columns(2)

with col_left:
    conf = st.slider("Confianza mínima", min_value=0.05, max_value=0.95, value=0.25, step=0.05)
    imgsz = st.select_slider("Tamaño de imagen", options=[320, 480, 640, 768, 896, 1024], value=640)

with col_right:
    iou = st.slider("IOU NMS", min_value=0.10, max_value=0.90, value=0.70, step=0.05)
    device = st.selectbox("Dispositivo", options=["auto", "cpu", "0"], index=0)

uploaded_file = st.file_uploader("Radiografia dental", type=["png", "jpg", "jpeg", "bmp", "webp"])

if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    st.image(image_bytes, caption="Radiografia original", use_container_width=True)

    if st.button("Analizar radiografia", type="primary"):
        with st.spinner("Ejecutando inferencia con YOLO..."):
            model = get_model(model_path)
            annotated_image, detections = run_inference(
                model=model,
                image_bytes=image_bytes,
                conf=conf,
                iou=iou,
                imgsz=imgsz,
                device=device,
            )

        st.session_state["frontend_analysis"] = {
            "image_bytes": image_bytes,
            "detections": detections,
            "signature": f"{uploaded_file.name}:{len(image_bytes)}:{len(detections)}",
        }
        st.session_state["frontend_analysis_signature"] = st.session_state["frontend_analysis"]["signature"]

    analysis = st.session_state.get("frontend_analysis")
    if analysis:
        detections = analysis["detections"]

        st.subheader("Resultados")
        st.write(f"Detecciones encontradas: {len(detections)}")
        if detections:
            table_rows = pd.DataFrame(
                [
                    {
                        "mostrar": True,
                        "recuadro": f"#{index + 1} {detection['label']}",
                        "clase": detection["class_name"],
                        "fiabilidad": str(detection["confidence"]),
                        "bbox": str(detection["bbox_xyxy"]),
                    }
                    for index, detection in enumerate(detections)
                ]
            )

            editor_key = f"frontend_detection_table_{analysis['signature']}"
            edited_table = st.data_editor(
                table_rows,
                hide_index=True,
                use_container_width=True,
                num_rows="fixed",
                key=editor_key,
                disabled=["recuadro", "clase", "fiabilidad", "bbox"],
                column_config={
                    "mostrar": st.column_config.CheckboxColumn("Mostrar"),
                    "recuadro": st.column_config.TextColumn("Recuadro"),
                    "clase": st.column_config.TextColumn("Clase"),
                    "fiabilidad": st.column_config.TextColumn("Fiabilidad"),
                    "bbox": st.column_config.TextColumn("BBox"),
                },
            )

            selected_indices = [
                index
                for index, visible in enumerate(edited_table["mostrar"].tolist())
                if bool(visible)
            ]
            st.info(f"Mostrando {len(selected_indices)} de {len(detections)} recuadros.")

            col_select_all, col_deselect_all = st.columns(2)
            with col_select_all:
                if st.button("✓ Seleccionar todos", use_container_width=True):
                    edited_table["mostrar"] = True
                    st.rerun()
            with col_deselect_all:
                if st.button("✗ Deseleccionar todos", use_container_width=True):
                    edited_table["mostrar"] = False
                    st.rerun()

            annotated_to_show = draw_detections(
                analysis["image_bytes"],
                detections,
                selected_indices=selected_indices,
            )
        else:
            st.info("No se detectaron objetos con los parámetros actuales.")
            annotated_to_show = None

        st.subheader("Radiografia con recuadros")
        if annotated_to_show is not None:
            st.image(annotated_to_show, use_container_width=True)

        out_name = f"annotated_{Path(uploaded_file.name).stem}.jpg"
        if annotated_to_show is not None:
            with st.expander("Descargar imagen anotada"):
                from io import BytesIO

                buffer = BytesIO()
                annotated_to_show.save(buffer, format="JPEG", quality=95)
                st.download_button(
                    label="Descargar JPG",
                    data=buffer.getvalue(),
                    file_name=out_name,
                    mime="image/jpeg",
                )
else:
    st.info("Sube una imagen para empezar.")

