#!/usr/bin/env python3
"""Orquesta train -> eval/predict de YOLOv8 con versionado por timestamp."""

# Como leer este archivo:
# 1) `parse_args()` define flags comunes para train y eval/predict.
# 2) `_run_step()` ejecuta scripts hijos y propaga errores.
# 3) `_resolve_trained_model()` busca `best.pt`/`last.pt` tras entrenar.
# 4) `main()` coordina todo y guarda `pipeline_report.json`.
#
# Ejemplo minimo de uso:
# python .\tools\run_train_eval_predict_yolov8.py --data .\dataset\data.yaml --source .\dataset\images\test --model yolov8n.pt --epochs 100 --imgsz 640 --batch 16 --device cpu --task both

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def parse_args() -> argparse.Namespace:
    # Define un CLI unico para encadenar train -> eval/predict.
    # El objetivo es ejecutar el flujo completo con un solo comando reproducible.
    parser = argparse.ArgumentParser(
        description="Ejecuta entrenamiento y luego evaluacion/prediccion YOLOv8 en secuencia."
    )
    parser.add_argument("--data", default="dataset/data.yaml", help="Ruta al data.yaml")
    parser.add_argument(
        "--source",
        default="dataset/images/test",
        help="Ruta para prediccion (carpeta, imagen o video)",
    )
    parser.add_argument("--model", default="yolov8n.pt", help="Modelo base para entrenamiento")
    parser.add_argument("--task", choices=("val", "predict", "both"), default="both")
    parser.add_argument("--epochs", type=int, default=100, help="Epocas de entrenamiento")
    parser.add_argument("--imgsz", type=int, default=640, help="Tamano de imagen")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument(
        "--device",
        default="auto",
        help="Dispositivo: auto, cpu, 0, 0,1...",
    )
    parser.add_argument("--project-train", default="runs/train", help="Proyecto para train")
    parser.add_argument("--project-eval", default="runs/eval_predict", help="Proyecto para eval/predict")
    parser.add_argument("--project-pipeline", default="runs/pipeline", help="Proyecto para reporte de pipeline")
    parser.add_argument(
        "--name-prefix",
        default="dental_pipeline",
        help="Prefijo base para nombres versionados",
    )
    parser.add_argument(
        "--skip-train",
        action="store_true",
        help="Omite entrenamiento y usa --model directo para eval/predict",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida el flujo sin entrenar ni evaluar realmente",
    )
    return parser.parse_args()


def utc_stamp() -> str:
    # Genera un identificador temporal estable para versionar salidas.
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _run_step(command: List[str], label: str) -> None:
    # Ejecuta un subproceso, reenvia su salida y falla si el paso devuelve error.
    # Asi mantenemos logs completos de cada fase del pipeline en la misma consola.
    printable = " ".join(command)
    print(f"[{label}] Ejecutando: {printable}")
    result = subprocess.run(command, capture_output=True, text=True, check=False)

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Fallo en {label} (exit={result.returncode})")


def _resolve_trained_model(train_project: Path, train_name: str, fallback_model: str) -> str:
    # Prioriza best.pt, luego last.pt, y usa fallback si no hay pesos entrenados.
    # Esto permite continuar flujo de evaluacion aun si no se genero best.pt por alguna razon.
    run_dir = train_project / train_name / "weights"
    best = run_dir / "best.pt"
    last = run_dir / "last.pt"
    if best.exists():
        return str(best.resolve())
    if last.exists():
        return str(last.resolve())
    return fallback_model


def main() -> int:
    # 1) Lee argumentos y valida recursos de entrada.
    args = parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"No se encontro data.yaml: {data_path}")

    # Solo validamos source si realmente habra etapa de prediccion.
    if args.task in ("predict", "both"):
        source_path = Path(args.source)
        if not source_path.exists():
            raise FileNotFoundError(f"No se encontro source para prediccion: {source_path}")

    # 2) Construye nombres versionados y localiza scripts hijos.
    stamp = utc_stamp()
    train_name = f"{args.name_prefix}_{stamp}_train"
    eval_name = f"{args.name_prefix}_{stamp}_evalpredict"
    pipeline_name = f"{args.name_prefix}_{stamp}_pipeline"

    # Resolver desde __file__ evita depender del directorio actual de ejecucion.
    tools_dir = Path(__file__).resolve().parent
    train_script = tools_dir / "train_yolov8.py"
    eval_script = tools_dir / "eval_predict_yolov8.py"

    if not args.skip_train:
        # 3) Ejecuta entrenamiento con el nombre versionado de esta corrida.
        train_cmd = [
            sys.executable,
            str(train_script),
            "--data",
            str(data_path),
            "--model",
            args.model,
            "--epochs",
            str(args.epochs),
            "--imgsz",
            str(args.imgsz),
            "--batch",
            str(args.batch),
            "--device",
            args.device,
            "--project",
            args.project_train,
            "--name",
            train_name,
        ]
        # En modo seco delegamos tambien en dry-run del script hijo para coherencia.
        if args.dry_run:
            train_cmd.append("--dry-run")
        _run_step(train_cmd, "train")

    # Modelo inicial para evaluar; puede sustituirse por best.pt tras entrenar.
    eval_model = args.model
    if not args.skip_train and not args.dry_run:
        # Si hubo train real, intenta evaluar con los mejores pesos generados.
        eval_model = _resolve_trained_model(Path(args.project_train), train_name, args.model)

    # 4) Ejecuta evaluacion/prediccion con el modelo seleccionado.
    eval_cmd = [
        sys.executable,
        str(eval_script),
        "--task",
        args.task,
        "--data",
        str(data_path),
        "--source",
        str(Path(args.source)),
        "--model",
        eval_model,
        "--imgsz",
        str(args.imgsz),
        "--batch",
        str(args.batch),
        "--device",
        args.device,
        "--project",
        args.project_eval,
        "--name",
        eval_name,
    ]
    if args.dry_run:
        eval_cmd.append("--dry-run")
    _run_step(eval_cmd, "eval_predict")

    # 5) Guarda un reporte consolidado del pipeline para trazabilidad.
    pipeline_dir = Path(args.project_pipeline) / pipeline_name
    pipeline_dir.mkdir(parents=True, exist_ok=True)
    report: Dict[str, str] = {
        "timestamp_utc": stamp,
        "train_name": train_name,
        "eval_name": eval_name,
        "pipeline_name": pipeline_name,
        "model_for_eval": eval_model,
        "train_project": str(Path(args.project_train).resolve()),
        "eval_project": str(Path(args.project_eval).resolve()),
        "task": args.task,
        "dry_run": str(args.dry_run),
    }

    # Archivo "indice" de la corrida: enlaza nombres, proyectos y modo de ejecucion.
    report_path = pipeline_dir / "pipeline_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Pipeline completado. Reporte: {report_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

