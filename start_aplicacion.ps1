$ErrorActionPreference = "Stop"

Write-Host "Iniciando el backend de IA Dental..." -ForegroundColor Green

# Cambiar al directorio del backend
cd backend

# Iniciar contenedor Docker de MongoDB
Write-Host "Levantando el contenedor de MongoDB..." -ForegroundColor Cyan
docker compose -f docker-compose.mongo.yml up -d

# Activar el entorno virtual
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . ".\.venv\Scripts\Activate.ps1"
    Write-Host "Entorno virtual activado." -ForegroundColor Cyan
} else {
    Write-Host "Advertencia: No se encontró el entorno virtual en backend\.venv" -ForegroundColor Yellow
}

# Ejecutar el frontend en una nueva ventana (desde la carpeta raíz)
Write-Host "Iniciando el frontend..." -ForegroundColor Cyan
Start-Process "cmd.exe" -ArgumentList "/c pnpm run dev" -WorkingDirectory "..\"

# Ejecutar el servidor con uvicorn
try {
    Write-Host "Iniciando uvicorn (Presiona Ctrl+C para detener)..." -ForegroundColor Green
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}
finally {
    Write-Host "Deteniendo contenedor de Docker..." -ForegroundColor Cyan
    docker compose -f docker-compose.mongo.yml stop
    Write-Host "Backend y Docker detenidos." -ForegroundColor Green
    cd ..
}
