## 📊 Arquitectura Docker Compose Local

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Compose Network                        │
│                                                                   │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │   Auth Service   │         │  Users Service   │              │
│  │  (FastAPI)       │         │   (FastAPI)      │              │
│  │  Puerto: 8000    │         │   Puerto: 8001   │              │
│  │                  │         │                  │              │
│  └────────┬─────────┘         └────────┬─────────┘              │
│           │                            │                        │
│           │ Consulta                   │ Consulta               │
│           ▼                            ▼                        │
│  ┌──────────────────────┐   ┌──────────────────────┐           │
│  │ DynamoDB Local       │   │ MySQL                │           │
│  │ Puerto: 8000         │   │ Puerto: 3306         │           │
│  │ DB: dned (local)     │   │ DB: dned (local)     │           │
│  └──────────────────────┘   └──────────────────────┘           │
│           ▲                            ▲                        │
│           │ Volumen: dynamodb_data     │ Volumen: mysql_data   │
│           │ (Persistencia)             │ (Persistencia)        │
│           └────────────────────────────┘                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
        │              │              │              │
        ▼              ▼              ▼              ▼
    localhost      localhost      localhost    Docker Network
    :8000/docs     :8001/docs     :3306      app-network
    (Swagger)      (Swagger)      (MySQL)
```

## 📁 Archivos Modificados/Creados

### Archivos Nuevos:
```
✅ docker-compose.yml          - Configuración para desarrollo local
✅ docker-compose-prod.yml     - Configuración para producción
✅ .env.local                  - Variables de entorno (local)
✅ .dockerignore               - Archivos a ignorar en builds
✅ setup-local.sh              - Script de setup automático
✅ DOCKER_SETUP.md             - Guía de configuración detallada
```

### Archivos Modificados:
```
✏️  Makefile                   - Nuevos comandos para desarrollo local
✏️  README.md                  - Documentación de inicio rápido
✏️  auth/Dockerfile            - Simplificado para desarrollo local
✏️  users/Dockerfile           - Eliminado RDS bundle, simplificado
```

## 🚀 Pasos para Ejecutar Localmente

### Paso 1: Preparar el proyecto
```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software
```

### Paso 2: Ejecutar setup automático
```bash
./setup-local.sh
```

O manualmente:
```bash
make build
make up
```

### Paso 3: Verificar que todo está corriendo
```bash
make ps
```

Deberías ver:
```
NAME                  COMMAND                  SERVICE        STATUS
mysql-local          docker-entrypoint.sh...  mysql          Up (healthy)
dynamodb-local       -jar DynamoDBLocal.jar  dynamodb-local  Up (healthy)
auth-service         uvicorn main:app...     auth-service    Up
users-service        uvicorn app.main:app    users-service   Up
```

### Paso 4: Acceder a los servicios
- **Swagger Auth**: http://localhost:8000/docs
- **Swagger Users**: http://localhost:8001/docs

### Paso 5: Para detener
```bash
make down
```

## ⚙️ Configuración Importante en tu Código

### Para Auth Service (auth/configuration/database.py)

Necesitas modificar para soportar DynamoDB Local:

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_dynamo_client():
    session = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT_URL")  # Agrega esta línea
    )
    return session
```

### Para Users Service (usuarios/app/configuration/database.py)

Tu configuración ya está lista ✅

## 🔍 Monitoreo y Debugging

```bash
# Ver logs en tiempo real
make logs

# Ver logs de un servicio específico
make logs-auth
make logs-users

# Ver estado de contenedores
make ps

# Ejecutar comandos dentro de un contenedor
docker-compose exec auth-service bash
docker-compose exec users-service bash
docker-compose exec mysql bash

# Ver volúmenes
docker volume ls

# Inspeccionar red
docker network ls
```

## 🧹 Limpiar todo

```bash
# Solo detener (datos persisten)
make down

# Eliminar todo incluyendo datos
make clean
```

## ⚠️ Puntos Críticos

1. **DynamoDB Endpoint**: Asegúrate de que tu código auth lea `DYNAMODB_ENDPOINT_URL`
2. **MySQL Host**: En docker-compose es `mysql`, no `localhost`
3. **Health Checks**: Los servicios esperan a que MySQL y DynamoDB estén listos
4. **Puertos**: Si tienes servicios en estos puertos, libéralos primero
5. **Variables de Entorno**: Cargan desde `.env.local` automáticamente

