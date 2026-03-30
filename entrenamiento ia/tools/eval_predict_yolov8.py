#!/usr/bin/env python3
"""Evaluacion y prediccion YOLOv8 con reporte consolidado."""

# Como leer este archivo:
# 1) `parse_args()` define el modo (`val`, `predict` o `both`).
# 2) `build_val_kwargs()` y `build_predict_kwargs()` arman parametros de Ultralytics.
# 3) `extract_metrics()` normaliza metricas para exportarlas.
# 4) `main()` ejecuta tareas y genera `run_report.json`.
#
# Ejemplo minimo de uso:
# python .\tools\eval_predict_yolov8.py --task both --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --device cpu

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable

from device_resolver import resolve_device


def parse_args() -> argparse.Namespace:
    # Expone un CLI unico para validar, predecir o ejecutar ambos pasos.
    # Esto evita mantener dos scripts separados para tareas muy parecidas.
    parser = argparse.ArgumentParser(
        description="Evalua y/o genera predicciones con YOLOv8."
    )
    parser.add_argument("--task", choices=("val", "predict", "both"), default="both")
    parser.add_argument("--data", default="dataset/data.yaml", help="Ruta al data.yaml")
    parser.add_argument("--model", default="yolov8n.pt", help="Modelo base o checkpoint")
    parser.add_argument(
        "--source",
        default="dataset/images/test",
        help="Ruta de imagen, carpeta o video para prediccion",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Tamano de imagen")
    parser.add_argument("--batch", type=int, default=16, help="Batch size para validacion")
    parser.add_argument(
        "--device",
        default="auto",
        help="Dispositivo: auto, cpu, 0, 0,1, ... (auto usa GPU si existe)",
    )
    parser.add_argument("--conf", type=float, default=0.25, help="Confianza minima")
    parser.add_argument("--iou", type=float, default=0.7, help="IOU NMS para prediccion")
    parser.add_argument("--project", default="runs/eval_predict", help="Directorio base")
    parser.add_argument("--name", default="dental_eval_predict", help="Nombre del experimento")
    parser.add_argument(
        "--max-pred-images",
        type=int,
        default=100,
        help="Limite de imagenes a procesar en prediccion",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo imprime configuracion sin ejecutar ultralytics",
    )
    return parser.parse_args()


def build_val_kwargs(args: argparse.Namespace) -> Dict[str, Any]:
    # Construye los argumentos de model.val() a partir del CLI.
    return {
        "data": str(Path(args.data).resolve()),
        "imgsz": args.imgsz,
        "batch": args.batch,
        "device": args.device,
        "project": args.project,
        "name": args.name,
    }


def build_predict_kwargs(args: argparse.Namespace) -> Dict[str, Any]:
    # Construye los argumentos de model.predict() con guardado de resultados activado.
    # save=True asegura visualizar rapidamente resultados sin codigo adicional.
    return {
        "source": str(Path(args.source).resolve()),
        "imgsz": args.imgsz,
        "conf": args.conf,
        "iou": args.iou,
        "device": args.device,
        "project": args.project,
        "name": args.name,
        "save": True,
        "stream": False,
        "max_det": 300,
    }


def _normalize_metric_value(value: Any) -> Any:
    # Convierte valores de Ultralytics (incluyendo arrays/tensores) a tipos JSON-safe.
    if value is None:
        return None

    if isinstance(value, (bool, int, float, str)):
        return value

    if hasattr(value, "item"):
        try:
            return float(value.item())
        except Exception:
            pass

    if hasattr(value, "tolist"):
        try:
            return _normalize_metric_value(value.tolist())
        except Exception:
            pass

    if isinstance(value, dict):
        normalized: Dict[str, Any] = {}
        for k, v in value.items():
            normalized_v = _normalize_metric_value(v)
            if normalized_v is not None:
                normalized[str(k)] = normalized_v
        return normalized

    if isinstance(value, (list, tuple)):
        normalized_list = []
        for item in value:
            normalized_item = _normalize_metric_value(item)
            if normalized_item is not None:
                normalized_list.append(normalized_item)
        return normalized_list

    try:
        return float(value)
    except Exception:
        return str(value)


def extract_metrics(metrics_obj: Any) -> Dict[str, Any]:
    # Extrae metadatos estables para serializarlos en JSON/CSV.
    # Esta capa protege contra cambios menores en la estructura interna de Ultralytics.
    metrics: Dict[str, Any] = {}
    for key in ("fitness", "speed"):
        value = getattr(metrics_obj, key, None)
        normalized_value = _normalize_metric_value(value)
        if normalized_value is not None:
            metrics[key] = normalized_value

    box_obj = getattr(metrics_obj, "box", None)
    if box_obj is not None:
        for source_name in ("map", "map50", "map75", "maps"):
            value = getattr(box_obj, source_name, None)
            normalized_value = _normalize_metric_value(value)
            if normalized_value is not None:
                metrics[f"box_{source_name}"] = normalized_value

    # Fallback para objetos no estandar.
    # Si la API devuelve un diccionario de resultados, se conserva lo simple (int/float/str).
    results_dict = getattr(metrics_obj, "results_dict", None)
    if isinstance(results_dict, dict):
        for k, v in results_dict.items():
            normalized_value = _normalize_metric_value(v)
            if normalized_value is not None:
                metrics[str(k)] = normalized_value

    return metrics


def write_metrics_files(metrics: Dict[str, Any], output_dir: Path) -> None:
    # Escribe metricas en formatos legibles para humanos (CSV) y maquinas (JSON).
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "val_metrics.json"
    json_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    csv_path = output_dir / "val_metrics.csv"
    # El CSV en formato key/value facilita abrir metricas en Excel o Google Sheets.
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key in sorted(metrics.keys()):
            writer.writerow([key, metrics[key]])


def write_run_report(
    output_dir: Path,
    args: argparse.Namespace,
    val_metrics: Dict[str, Any] | None,
    prediction_count: int | None,
) -> Path:
    # Registra un resumen de ejecucion para trazabilidad del experimento.
    # Incluye configuracion y rutas para reconstruir la corrida mas adelante.
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "task": args.task,
        "model": args.model,
        "data": str(Path(args.data).resolve()),
        "source": str(Path(args.source).resolve()),
        "output_dir": str(output_dir.resolve()),
        "val_metrics": val_metrics,
        "prediction_items": prediction_count,
    }

    report_path = output_dir / "run_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path


def _validate_inputs(args: argparse.Namespace) -> None:
    # Verifica rutas criticas antes de cargar YOLO para fallar rapido.
    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"No se encontro data.yaml: {data_path}")

    # Solo exigimos source cuando se va a ejecutar inferencia.
    if args.task in ("predict", "both"):
        source_path = Path(args.source)
        if not source_path.exists():
            raise FileNotFoundError(f"No se encontro source para prediccion: {source_path}")


def _predict_count(results: Iterable[Any]) -> int:
    # Cuenta resultados iterables sin asumir estructura interna de Ultralytics.
    count = 0
    for _ in results:
        count += 1
    return count


def main() -> int:
    # 1) Prepara y valida configuracion de entrada.
    args = parse_args()
    _validate_inputs(args)

    device_resolution = resolve_device(args.device)
    args.device = device_resolution.resolved

    # 2) Compone parametros de val/predict y muestra configuracion final.
    val_kwargs = build_val_kwargs(args)
    predict_kwargs = build_predict_kwargs(args)
    # Carpeta canonica de salida para reportes y artefactos.
    output_dir = (Path(args.project) / args.name).resolve()

    print("Configuracion eval/predict:")
    print(f"  task: {args.task}")
    print(f"  model: {args.model}")
    print(f"  requested_device: {device_resolution.requested}")
    print(f"  resolved_device: {device_resolution.resolved}")
    if device_resolution.warning:
        print(f"  warning: {device_resolution.warning}")
    print(f"  data: {val_kwargs['data']}")
    print(f"  source: {predict_kwargs['source']}")
    print(f"  output_dir: {output_dir}")

    # 3) Permite revisar configuracion sin ejecutar inferencia real.
    # Es equivalente a un "lint" operacional de la corrida.
    if args.dry_run:
        print("Dry run activo: no se ejecuto evaluacion ni prediccion.")
        return 0

    # Import diferido para permitir pruebas smoke sin ultralytics.
    from ultralytics import YOLO

    # 4) Carga modelo y ejecuta tareas solicitadas.
    model = YOLO(args.model)

    val_metrics: Dict[str, Any] | None = None
    prediction_count: int | None = None

    if args.task in ("val", "both"):
        # Guarda metricas de validacion para analisis posterior.
        metrics_obj = model.val(**val_kwargs)
        val_metrics = extract_metrics(metrics_obj)
        write_metrics_files(val_metrics, output_dir)

    if args.task in ("predict", "both"):
        # Ejecuta prediccion y reporta cuantas muestras fueron procesadas.
        results = model.predict(**predict_kwargs)
        prediction_count = _predict_count(results)

    # 5) Escribe reporte global de ejecucion.
    report_path = write_run_report(
        output_dir=output_dir,
        args=args,
        val_metrics=val_metrics,
        prediction_count=prediction_count,
    )

    # Mensaje final con la ruta principal de salida.
    print(f"Proceso completado. Reporte: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

