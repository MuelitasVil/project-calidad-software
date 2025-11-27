FROM python:3.11-slim

WORKDIR /code

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y curl && apt-get clean
RUN pip install --upgrade pip

# Copiar código
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade -r app/requirements.txt

EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]