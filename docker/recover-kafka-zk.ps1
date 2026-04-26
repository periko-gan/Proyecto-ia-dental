[CmdletBinding()]
param(
    [switch]$NoBackup,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$composeFile = Join-Path $scriptDir 'docker-compose.yml'
$dataDir = Join-Path $scriptDir 'data'
$kafkaDataDir = Join-Path $dataDir 'kafka'
$zookeeperDataDir = Join-Path $dataDir 'zookeeper'
$backupRoot = Join-Path $dataDir 'backups'

function Write-Step {
    param([string]$Message)
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Invoke-Compose {
    param([string[]]$ComposeArgs)

    $cmdPreview = "docker compose -f `"$composeFile`" $($ComposeArgs -join ' ')"
    if ($DryRun) {
        Write-Host "[dry-run] $cmdPreview" -ForegroundColor Yellow
        return
    }

    & docker compose -f "$composeFile" @ComposeArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo ejecutando: $cmdPreview"
    }
}

function Remove-DirectoryIfExists {
    param([string]$Path)

    if (Test-Path $Path) {
        if ($DryRun) {
            Write-Host "[dry-run] Remove-Item -Path `"$Path`" -Recurse -Force" -ForegroundColor Yellow
        }
        else {
            Remove-Item -Path $Path -Recurse -Force -ErrorAction Stop
        }
    }
}

function Ensure-Directory {
    param([string]$Path)

    if ($DryRun) {
        Write-Host "[dry-run] New-Item -ItemType Directory -Path `"$Path`" -Force" -ForegroundColor Yellow
        return
    }

    New-Item -ItemType Directory -Path $Path -Force | Out-Null
}

if (-not (Test-Path $composeFile)) {
    throw "No se encontro docker-compose.yml en: $composeFile"
}

Write-Step 'Parando y eliminando contenedores de Kafka, Kafka UI y Zookeeper'
Invoke-Compose @('stop', 'kafka', 'kafka-ui', 'zookeeper')
Invoke-Compose @('rm', '-f', 'kafka', 'kafka-ui', 'zookeeper')

if (-not $NoBackup) {
    Write-Step 'Creando copia de seguridad de datos actuales'
    Ensure-Directory -Path $backupRoot

    $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $backupDir = Join-Path $backupRoot "kafka-zk-$timestamp"
    Ensure-Directory -Path $backupDir

    if (Test-Path $kafkaDataDir) {
        $targetKafkaBackup = Join-Path $backupDir 'kafka'
        if ($DryRun) {
            Write-Host "[dry-run] Copy-Item -Path `"$kafkaDataDir`" -Destination `"$targetKafkaBackup`" -Recurse -Force" -ForegroundColor Yellow
        }
        else {
            Copy-Item -Path $kafkaDataDir -Destination $targetKafkaBackup -Recurse -Force
        }
    }

    if (Test-Path $zookeeperDataDir) {
        $targetZkBackup = Join-Path $backupDir 'zookeeper'
        if ($DryRun) {
            Write-Host "[dry-run] Copy-Item -Path `"$zookeeperDataDir`" -Destination `"$targetZkBackup`" -Recurse -Force" -ForegroundColor Yellow
        }
        else {
            Copy-Item -Path $zookeeperDataDir -Destination $targetZkBackup -Recurse -Force
        }
    }

    Write-Host "Backup generado en: $backupDir" -ForegroundColor Green
}

Write-Step 'Limpiando directorios de datos de Kafka y Zookeeper'
Remove-DirectoryIfExists -Path $kafkaDataDir
Remove-DirectoryIfExists -Path $zookeeperDataDir
Ensure-Directory -Path $kafkaDataDir
Ensure-Directory -Path $zookeeperDataDir

Write-Step 'Levantando Zookeeper, Kafka y Kafka UI'
Invoke-Compose @('up', '-d', 'zookeeper', 'kafka', 'kafka-ui')

Write-Step 'Estado de servicios'
Invoke-Compose @('ps')

Write-Step 'Ultimos logs de Kafka'
Invoke-Compose @('logs', 'kafka', '--tail=80')

Write-Step 'Ultimos logs de Kafka UI'
Invoke-Compose @('logs', 'kafka-ui', '--tail=80')

Write-Host 'Recuperacion finalizada. Kafka UI: http://localhost:8085/' -ForegroundColor Green

