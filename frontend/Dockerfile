
# Etapa 1: construir la aplicación Flutter Web
FROM ghcr.io/cirruslabs/flutter:3.47.9 AS build

WORKDIR /app

# Copiar el proyecto Flutter
COPY . .

# Descargar dependencias
RUN flutter pub get

# Construir la aplicación para producción
ARG API_BASE_URL=https://idapi.zona52.lat

RUN flutter build web --release \
    --dart-define=API_BASE_URL=${API_BASE_URL}

# Etapa 2: servir la aplicación con Nginx
FROM nginx:alpine

# Copiar los archivos web generados
COPY --from=build /app/build/web /usr/share/nginx/html

# Configuración de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

