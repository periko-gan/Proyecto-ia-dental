#!/bin/bash

# Guardamos la ruta base para referencias absolutas
BASE_DIR=$(pwd)

# Función que se ejecutará al presionar Ctrl+C
cleanup() {
    echo -e "\n\e[36mDeteniendo contenedor de Docker y el frontend...\e[0m"
    
    # Detener MongoDB (asegurando estar en la carpeta backend)
    cd "$BASE_DIR/backend" && docker compose -f docker-compose.mongo.yml stop
    
    # Detener el proceso del frontend si está guardado
    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    echo -e "\e[32mBackend, Frontend y Docker detenidos.\e[0m"
    exit 0
}

# Configurar el "trap" para interceptar la señal SIGINT (Ctrl+C) y SIGTERM
trap cleanup SIGINT SIGTERM

echo -e "\e[32mIniciando entorno de desarrollo de IA Dental...\e[0m"

# 1. Iniciar el frontend en segundo plano (desde la raíz)
echo -e "\e[36mIniciando el frontend...\e[0m"
pnpm run dev &
FRONTEND_PID=$!

# Cambiar a la carpeta del backend
cd "$BASE_DIR/backend" || { echo "No se pudo entrar a la carpeta backend"; exit 1; }

# 2. Levantar el contenedor de Docker de MongoDB
echo -e "\e[36mLevantando el contenedor de MongoDB...\e[0m"
docker compose -f docker-compose.mongo.yml up -d

# 3. Activar el entorno virtual
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo -e "\e[36mEntorno virtual activado.\e[0m"
else
    echo -e "\e[33mAdvertencia: No se encontró el entorno virtual en backend/.venv\e[0m"
fi

# 4. Iniciar uvicorn (Este comando bloquea la terminal hasta que presiones Ctrl+C)
echo -e "\e[32mIniciando uvicorn (Presiona Ctrl+C para detener todo)...\e[0m"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
