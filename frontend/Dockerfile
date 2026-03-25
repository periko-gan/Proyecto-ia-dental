# ==========================================
# Etapa 1: Construcción (Build)
# ==========================================
FROM node:20-alpine AS build-stage

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Habilitar corepack para usar pnpm sin necesidad de instalarlo manualmente
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copiar los archivos de definición de dependencias
COPY package.json pnpm-lock.yaml ./

# Instalar las dependencias de forma exacta usando el archivo lock
RUN pnpm install --frozen-lockfile

# Copiar el resto del código fuente del proyecto
COPY . .

# Compilar la aplicación para producción (esto generará la carpeta /dist)
RUN pnpm run build

# ==========================================
# Etapa 2: Servidor (Producción)
# ==========================================
FROM nginx:alpine AS production-stage

# Copiar los archivos compilados de la Etapa 1 al directorio público de Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Exponer el puerto en el que Nginx escuchará las peticiones
EXPOSE 80

# Iniciar Nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]
