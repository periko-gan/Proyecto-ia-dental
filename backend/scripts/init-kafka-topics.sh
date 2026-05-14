#!/bin/bash
# Script para inicializar Kafka topics definitivos para el proyecto Dental IA
# Uso: bash scripts/init-kafka-topics.sh [--dry-run]

set -euo pipefail

DRY_RUN=false

usage() {
  cat <<'EOF'
Uso: init-kafka-topics.sh [--dry-run]

Opciones:
  --dry-run   Muestra los comandos sin ejecutarlos
  -h, --help  Muestra esta ayuda
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
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

# Topics a crear con particiones y replication factor
TOPICS=(
  "dental.image.uploaded:1:1"
  "dental.analysis.requested:1:1"
  "dental.analysis.started:1:1"
  "dental.analysis.completed:1:1"
  "dental.analysis.failed:1:1"
  "dental.result.saved:1:1"
  "dental.metrics.inference:1:1"
  "dental.auth.events:1:1"
  "dental.system.logs:1:1"
  "dental.system.errors:1:1"
  "dental.dead-letter:1:1"
)

BOOTSTRAP_SERVERS="${KAFKA_BOOTSTRAP_SERVERS:-localhost:9092}"

run_cmd() {
  if $DRY_RUN; then
    echo "[dry-run] $*"
    return 0
  fi
  "$@"
}

step() {
  echo "==> $1"
}

step "Inicializando Kafka topics para Dental IA"
step "Bootstrap servers: $BOOTSTRAP_SERVERS"

for topic_config in "${TOPICS[@]}"; do
  IFS=':' read -r topic partitions replication_factor <<< "$topic_config"
  
  # Verificar si el topic ya existe
  existing=$(run_cmd kafka-topics --bootstrap-server "$BOOTSTRAP_SERVERS" --list 2>/dev/null | grep "^${topic}$" || true)
  
  if [ -n "$existing" ]; then
    echo "✓ Topic ya existe: $topic"
  else
    echo "✗ Creando topic: $topic (partitions=$partitions, replication_factor=$replication_factor)"
    run_cmd kafka-topics --bootstrap-server "$BOOTSTRAP_SERVERS" \
      --create \
      --topic "$topic" \
      --partitions "$partitions" \
      --replication-factor "$replication_factor" \
      --if-not-exists
  fi
done

step "Verificando topics creados"
run_cmd kafka-topics --bootstrap-server "$BOOTSTRAP_SERVERS" --list | grep "dental\."

step "Inicialización completada"
