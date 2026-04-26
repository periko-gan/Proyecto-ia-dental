#!/usr/bin/env bash
set -euo pipefail

NO_BACKUP=false
DRY_RUN=false

usage() {
  cat <<'EOF'
Uso: recover-kafka-zk.sh [--no-backup] [--dry-run]

Opciones:
  --no-backup   Omite copia de seguridad antes de limpiar datos.
  --dry-run     Muestra los comandos sin ejecutarlos.
  -h, --help    Muestra esta ayuda.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-backup)
      NO_BACKUP=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Argumento no reconocido: $1" >&2
      usage
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
DATA_DIR="$SCRIPT_DIR/data"
KAFKA_DATA_DIR="$DATA_DIR/kafka"
ZOOKEEPER_DATA_DIR="$DATA_DIR/zookeeper"
BACKUP_ROOT="$DATA_DIR/backups"

step() {
  echo "==> $1"
}

run_cmd() {
  if $DRY_RUN; then
    echo "[dry-run] $*"
    return 0
  fi

  "$@"
}

run_compose() {
  run_cmd docker compose -f "$COMPOSE_FILE" "$@"
}

remove_dir_if_exists() {
  local path="$1"
  if [[ -d "$path" ]]; then
    run_cmd rm -rf "$path"
  fi
}

ensure_dir() {
  run_cmd mkdir -p "$1"
}

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "No se encontro docker-compose.yml en: $COMPOSE_FILE" >&2
  exit 1
fi

step "Parando y eliminando contenedores de Kafka, Kafka UI y Zookeeper"
run_compose stop kafka kafka-ui zookeeper
run_compose rm -f kafka kafka-ui zookeeper

if [[ "$NO_BACKUP" == "false" ]]; then
  step "Creando copia de seguridad de datos actuales"
  ensure_dir "$BACKUP_ROOT"

  TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
  BACKUP_DIR="$BACKUP_ROOT/kafka-zk-$TIMESTAMP"
  ensure_dir "$BACKUP_DIR"

  if [[ -d "$KAFKA_DATA_DIR" ]]; then
    run_cmd cp -a "$KAFKA_DATA_DIR" "$BACKUP_DIR/kafka"
  fi

  if [[ -d "$ZOOKEEPER_DATA_DIR" ]]; then
    run_cmd cp -a "$ZOOKEEPER_DATA_DIR" "$BACKUP_DIR/zookeeper"
  fi

  echo "Backup generado en: $BACKUP_DIR"
fi

step "Limpiando directorios de datos de Kafka y Zookeeper"
remove_dir_if_exists "$KAFKA_DATA_DIR"
remove_dir_if_exists "$ZOOKEEPER_DATA_DIR"
ensure_dir "$KAFKA_DATA_DIR"
ensure_dir "$ZOOKEEPER_DATA_DIR"

step "Levantando Zookeeper, Kafka y Kafka UI"
run_compose up -d zookeeper kafka kafka-ui

step "Estado de servicios"
run_compose ps

step "Ultimos logs de Kafka"
run_compose logs kafka --tail=80

step "Ultimos logs de Kafka UI"
run_compose logs kafka-ui --tail=80

echo "Recuperacion finalizada. Kafka UI: http://localhost:8085"

