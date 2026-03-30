#!/usr/bin/env python3
"""Entrenamiento YOLOv8 sobre un data.yaml existente."""

# Como leer este archivo:
# 1) `parse_args()` define flags de entrenamiento.
# 2) `build_train_kwargs()` traduce flags al formato de Ultralytics.
# 3) `main()` valida rutas, imprime configuracion y ejecuta `model.train()`.
#
# Ejemplo minimo de uso:
# python .\tools\train_yolov8.py --data .\dataset\data.yaml --model yolov8n.pt --epochs 100 --imgsz 640 --batch 16 --device cpu

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

from device_resolver import resolve_device


TOOLS_ROOT = Path(__file__).resolve().parents[1]


def _resolve_project_dir(project_arg: str) -> Path:
    # Fuerza rutas relativas a vivir dentro de `entrenamiento ia` para evitar salidas fuera.
    project_path = Path(project_arg)
    if project_path.is_absolute():
        return project_path
    return (TOOLS_ROOT / project_path).resolve()


def parse_args() -> argparse.Namespace:
    # Define todos los parametros de entrada del entrenamiento.
    # La idea es poder ejecutar el script tanto en pruebas rapidas como en corridas largas.
    parser = argparse.ArgumentParser(description="Entrena un detector YOLOv8 con Ultralytics.")
    parser.add_argument("--data", default="dataset/data.yaml", help="Ruta al data.yaml")
    parser.add_argument("--model", default="yolov8n.pt", help="Modelo base o checkpoint")
    parser.add_argument("--epochs", type=int, default=100, help="Numero de epocas")
    parser.add_argument("--imgsz", type=int, default=640, help="Tamano de imagen")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument(
        "--device",
        default="auto",
        help="Dispositivo: auto, cpu, 0, 0,1, ... (auto usa GPU si existe)",
    )
    parser.add_argument("--project", default="runs/train", help="Carpeta base de resultados")
    parser.add_argument("--name", default="dental_yolov8", help="Nombre del experimento")
    parser.add_argument("--workers", type=int, default=4, help="Workers del dataloader")
    parser.add_argument("--patience", type=int, default=30, help="Early stopping patience")
    parser.add_argument("--seed", type=int, default=42, help="Semilla reproducible")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo imprime configuracion, no ejecuta entrenamiento",
    )
    return parser.parse_args()


def build_train_kwargs(args: argparse.Namespace) -> Dict[str, Any]:
    # Adapta los argumentos CLI al formato esperado por model.train().
    # Separar esta funcion facilita pruebas unitarias y reutilizacion.
    return {
        "data": str(Path(args.data).resolve()),
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "device": args.device,
        "project": str(_resolve_project_dir(args.project)),
        "name": args.name,
        "workers": args.workers,
        "patience": args.patience,
        "seed": args.seed,
    }


def main() -> int:
    # 1) Lee argumentos y valida precondiciones minimas.
    args = parse_args()
    data_path = Path(args.data)

    # El entrenamiento debe fallar rapido si falta el manifiesto del dataset.
    if not data_path.exists():
        raise FileNotFoundError(f"No se encontro data.yaml: {data_path}")

    # 2) Prepara e imprime la configuracion final que se enviara a Ultralytics.
    device_resolution = resolve_device(args.device)
    args.device = device_resolution.resolved
    train_kwargs = build_train_kwargs(args)

    # Mostrar configuracion ayuda a reproducir la corrida exacta despues.
    print("Configuracion de entrenamiento:")
    print(f"  model: {args.model}")
    print(f"  requested_device: {device_resolution.requested}")
    print(f"  resolved_device: {device_resolution.resolved}")
    if device_resolution.warning:
        print(f"  warning: {device_resolution.warning}")
    for key, value in train_kwargs.items():
        print(f"  {key}: {value}")

    # 3) Permite validar configuracion sin coste de entrenamiento.
    # Muy util para revisar rutas/flags antes de una corrida larga.
    if args.dry_run:
        print("Dry run activo: no se ejecuto entrenamiento.")
        return 0

    # Import diferido para permitir pruebas sin instalar ultralytics.
    from ultralytics import YOLO, settings

    # Mantiene todos los artefactos de Ultralytics bajo `entrenamiento ia/runs`.
    settings.update({"runs_dir": str((TOOLS_ROOT / "runs").resolve())})

    # 4) Carga pesos base y ejecuta el entrenamiento.
    # Si args.model es un .pt, usa pesos preentrenados; si es .yaml, inicializa arquitectura.
    model = YOLO(args.model)
    model.train(**train_kwargs)

    # `trainer.save_dir` refleja el directorio final (incluyendo sufijos incrementales).
    save_dir = getattr(getattr(model, "trainer", None), "save_dir", None)
    if save_dir is not None:
        print(f"ultralytics_save_dir: {Path(save_dir).resolve()}")

    print("Entrenamiento finalizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

