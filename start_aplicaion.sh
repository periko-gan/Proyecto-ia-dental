#!/bin/bash

# start_aplicaion.sh
# Equivalente en Linux al start_aplicacion.ps1

LEVANTAR_DOCKER() {
    echo -e "\e[36mLevantando el contenedor de MongoDB...\e[0m"
    if [ -d "backend" ]; then
        cd backend
        docker compose -f docker-compose.mongo.yml up -d
        cd ..
        echo -e "\e[32mDocker levantado.\e[0m"
    else
        echo -e "\e[33mNo se encontró la carpeta backend.\e[0m"
    fi
}

LEVANTAR_DOCKER_CARPETA() {
    echo -e "\e[36mLevantando los contenedores de la carpeta docker...\e[0m"
    if [ -d "docker" ]; then
        cd docker
        docker compose -f docker-compose.yml up -d
        cd ..
        echo -e "\e[32mContenedores de la carpeta docker levantados.\e[0m"
    else
        echo -e "\e[33mNo se encontró la carpeta docker.\e[0m"
    fi
}

LEVANTAR_FRONTEND() {
    echo -e "\e[36mIniciando el frontend...\e[0m"
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal --title="Frontend IA Dental" -- bash -c "pnpm run dev; exec bash"
    elif command -v x-terminal-emulator &> /dev/null; then
        x-terminal-emulator -T "Frontend IA Dental" -e bash -c "pnpm run dev; exec bash" &
    else
        echo -e "\e[33mNo se encontró un emulador de terminal (gnome-terminal/xterm). Ejecutando en background...\e[0m"
        nohup pnpm run dev > frontend.log 2>&1 &
    fi
    echo -e "\e[32mFrontend iniciado.\e[0m"
}

LEVANTAR_BACKEND() {
    echo -e "\e[36mIniciando el backend (uvicorn)...\e[0m"

    local CMD=""
    if [ -f "backend/.venv/bin/activate" ]; then
        CMD="cd backend && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000; exec bash"
    else
        echo -e "\e[33mAdvertencia: No se encontró el entorno virtual en backend/.venv\e[0m"
        CMD="cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000; exec bash"
    fi

    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal --title="Backend IA Dental" -- bash -c "$CMD"
    elif command -v x-terminal-emulator &> /dev/null; then
        x-terminal-emulator -T "Backend IA Dental" -e bash -c "$CMD" &
    else
        echo -e "\e[33mNo se encontró un emulador de terminal. Ejecutando en background...\e[0m"
        nohup bash -c "${CMD/exec bash/}" > backend.log 2>&1 &
    fi

    echo -e "\e[32mBackend iniciado.\e[0m"
}

LEVANTAR_TODO() {
    LEVANTAR_DOCKER
    LEVANTAR_DOCKER_CARPETA
    sleep 2
    LEVANTAR_BACKEND
    LEVANTAR_FRONTEND
}

CERRAR_DOCKER() {
    if [ -f "backend/docker-compose.mongo.yml" ]; then
        cd backend
        echo -e "\e[36mDeteniendo contenedor de MongoDB...\e[0m"
        docker compose -f docker-compose.mongo.yml stop
        cd ..
    else
        echo -e "\e[33mNo se encontró el archivo docker-compose.mongo.yml en backend.\e[0m"
    fi
}

CERRAR_DOCKER_CARPETA() {
    if [ -f "docker/docker-compose.yml" ]; then
        cd docker
        echo -e "\e[36mDeteniendo contenedores de la carpeta docker...\e[0m"
        docker compose -f docker-compose.yml stop
        cd ..
    else
        echo -e "\e[33mNo se encontró el archivo docker-compose.yml en la carpeta docker.\e[0m"
    fi
}

CERRAR_FRONTEND() {
    echo -e "\e[36mDeteniendo procesos del frontend...\e[0m"
    pkill -f "vite"
    pkill -f "pnpm"
    echo -e "\e[32mFrontend detenido.\e[0m"
}

CERRAR_BACKEND() {
    echo -e "\e[36mDeteniendo procesos del backend...\e[0m"
    pkill -f "uvicorn"
    echo -e "\e[32mBackend detenido.\e[0m"
}

CERRAR_TODO() {
    echo -e "\e[32mCerrando la aplicación de IA Dental...\e[0m"
    CERRAR_DOCKER
    CERRAR_DOCKER_CARPETA
    CERRAR_BACKEND
    CERRAR_FRONTEND
    echo -e "\e[32mAplicación detenida completamente.\e[0m"
}

while true; do
    echo ""
    echo -e "\e[36m=========================================\e[0m"
    echo -e "\e[36m   Gestión de la Aplicación IA Dental    \e[0m"
    echo -e "\e[36m=========================================\e[0m"
    echo " --- Opciones para Levantar ---"
    echo " 1. Levantar Docker (MongoDB - Backend)"
    echo " 2. Levantar Docker (Carpeta 'docker')"
    echo " 3. Levantar Backend (Uvicorn)"
    echo " 4. Levantar Frontend (Vite)"
    echo " 5. Levantar TODO"
    echo " --- Opciones para Cerrar ---"
    echo " 6. Cerrar Docker (MongoDB - Backend)"
    echo " 7. Cerrar Docker (Carpeta 'docker')"
    echo " 8. Cerrar Backend (Uvicorn)"
    echo " 9. Cerrar Frontend (Vite)"
    echo " 10. Cerrar TODO"
    echo " ----------------------------"
    echo " 11. Salir"
    echo -e "\e[36m=========================================\e[0m"
    read -p "Elige una opción (1-11): " opcion

    case $opcion in
        1) LEVANTAR_DOCKER ;;
        2) LEVANTAR_DOCKER_CARPETA ;;
        3) LEVANTAR_BACKEND ;;
        4) LEVANTAR_FRONTEND ;;
        5) LEVANTAR_TODO ;;
        6) CERRAR_DOCKER ;;
        7) CERRAR_DOCKER_CARPETA ;;
        8) CERRAR_BACKEND ;;
        9) CERRAR_FRONTEND ;;
        10) CERRAR_TODO ;;
        11) echo -e "\e[32mSaliendo...\e[0m"; exit 0 ;;
        *) echo -e "\e[31mOpción no válida. Por favor, elige una opción entre 1 y 11.\e[0m" ;;
    esac
done