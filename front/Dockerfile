# Stage 1: Test environment (for running tests)
FROM python:3.12-slim as test

WORKDIR /app

# Install system dependencies and Chromium (simpler than Chrome)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install test dependencies
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

# Copy test files
COPY tests/ /app/tests/

# Set working directory to tests
WORKDIR /app/tests

# Stage 2: Production nginx server
FROM nginx:alpine

# Copiar archivos HTML y recursos estáticos
COPY *.html /usr/share/nginx/html/
COPY *.png /usr/share/nginx/html/
COPY *.jpeg /usr/share/nginx/html/
COPY *.jpg /usr/share/nginx/html/

# Copiar componentes JavaScript reutilizables
COPY components/ /usr/share/nginx/html/components/

# Copiar scripts JavaScript
COPY js/ /usr/share/nginx/html/js/

# Copiar documentación
COPY *.md /usr/share/nginx/html/docs/

# Copiar configuración personalizada de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto 80
EXPOSE 80

# Comando por defecto (nginx lo inicia automáticamente)
CMD ["nginx", "-g", "daemon off;"]
