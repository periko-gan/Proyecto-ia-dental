param(
    [int]$Port = 8001,
    [string]$BindHost = "0.0.0.0"
)

$ErrorActionPreference = "Stop"

$env:DENTAL_AI_EVENTS_ENABLED = "true"
$env:DENTAL_AI_EVENTS_TRANSPORT = "kafka"
$env:DENTAL_AI_KAFKA_ENABLED = "true"
$env:DENTAL_AI_KAFKA_INFERENCE_CONSUMER_ENABLED = "true"
$env:DENTAL_AI_KAFKA_INFERENCE_CONSUMER_GROUP_ID = "dental-inference-consumer-e2e"
$env:DENTAL_AI_KAFKA_INFERENCE_CONSUMER_OFFSET_RESET = "latest"

Write-Host "[E2E] Iniciando backend con consumer opcional habilitado (temporal para esta terminal)..."
Write-Host "[E2E] Host=$BindHost Port=$Port"

..\.venv\Scripts\python.exe -m uvicorn main:app --reload --host $BindHost --port $Port
