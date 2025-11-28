# 📊 Tablas DynamoDB - Configuración Automática

## ✅ Resumen

Las 3 tablas DynamoDB necesarias para el servicio de autenticación (`auth-service`) se crean **automáticamente** cuando LocalStack arranca.

## 🚀 Cómo Funciona

Al ejecutar `make up` o `docker compose up`, LocalStack:

1. Se inicia en el puerto **4566**
2. Ejecuta automáticamente el script `localstack-init/init-dynamodb-tables.sh`
3. Crea las 3 tablas necesarias
4. Los servicios `auth-service` y `users-service` se conectan y funcionan sin configuración adicional

## 📋 Tablas Creadas

### 1. auth_ms_usuario
**Almacena los usuarios del sistema**

- **Primary Key**: `e_mail` (String)
- **Atributos**:
  - `e_mail`: Email del usuario (PK)
  - `hashed_password`: Contraseña hasheada
  - `salt`: Salt (opcional, legado)
  - `type_user`: Tipo de usuario (ej: "basic", "admin")
  - `state`: Estado activo/inactivo (Boolean)

**Ejemplo de registro:**
```json
{
  "e_mail": "usuario@example.com",
  "hashed_password": "$2b$12$...",
  "type_user": "basic",
  "state": true
}
```

### 2. auth_ms_jwt
**Almacena tokens JWT emitidos**

- **Primary Key**: `token` (String)
- **Atributos**:
  - `token`: Token JWT (PK)
  - `e_mail`: Email del usuario asociado
  - `created_at`: Timestamp de creación (ISO 8601)

**Ejemplo de registro:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "e_mail": "usuario@example.com",
  "created_at": "2025-11-27T03:00:00.000Z"
}
```

### 3. auth_ms_type_user
**Mapea tipos de usuario con sus emails**

- **Primary Key**: `type_user` (String)
- **Atributos**:
  - `type_user`: Tipo de usuario (PK, ej: "admin", "basic")
  - `emails`: Lista de emails asociados a este tipo (List)

**Ejemplo de registro:**
```json
{
  "type_user": "admin",
  "emails": ["admin@example.com", "superuser@example.com"]
}
```

## 🔧 Comandos Útiles

### Verificar que las tablas existen
```bash
# Opción 1: Script completo de verificación
make verify-dynamodb

# Opción 2: Listar tablas manualmente
docker exec localstack awslocal dynamodb list-tables

# Opción 3: Desde el host con AWS CLI
aws dynamodb list-tables --endpoint-url http://localhost:4566
```

### Ver estructura de una tabla
```bash
docker exec localstack awslocal dynamodb describe-table --table-name auth_ms_usuario
```

### Insertar datos de prueba
```bash
# Crear un usuario de prueba
docker exec localstack awslocal dynamodb put-item \
  --table-name auth_ms_usuario \
  --item '{
    "e_mail": {"S": "test@example.com"},
    "hashed_password": {"S": "$2b$12$hashedpassword"},
    "type_user": {"S": "basic"},
    "state": {"BOOL": true}
  }'

# Verificar inserción
docker exec localstack awslocal dynamodb scan --table-name auth_ms_usuario
```

### Consultar datos
```bash
# Escanear toda la tabla
docker exec localstack awslocal dynamodb scan --table-name auth_ms_usuario

# Obtener un registro por clave primaria
docker exec localstack awslocal dynamodb get-item \
  --table-name auth_ms_usuario \
  --key '{"e_mail": {"S": "test@example.com"}}'
```

### Eliminar una tabla (para recrearla)
```bash
docker exec localstack awslocal dynamodb delete-table --table-name auth_ms_usuario

# Reiniciar LocalStack para recrear todas las tablas
docker compose restart localstack
```

## 📝 Script de Inicialización

El script que crea las tablas está en: `localstack-init/init-dynamodb-tables.sh`

```bash
#!/bin/bash
# Este script se ejecuta automáticamente cuando LocalStack arranca

# Espera a que LocalStack esté listo
until curl -s http://localhost:4566/_localstack/health | grep -q '"dynamodb": "available"'; do
  sleep 2
done

# Crea las 3 tablas con AWS CLI
aws dynamodb create-table --table-name auth_ms_usuario ...
aws dynamodb create-table --table-name auth_ms_jwt ...
aws dynamodb create-table --table-name auth_ms_type_user ...
```

El script se monta en el contenedor LocalStack via volumen:
```yaml
volumes:
  - ./localstack-init:/etc/localstack/init/ready.d
```

LocalStack ejecuta automáticamente todos los scripts en `/etc/localstack/init/ready.d/` cuando está listo.

## 🔄 Recrear las Tablas

Si necesitas recrear las tablas desde cero:

```bash
# Opción 1: Reiniciar LocalStack (tablas se vuelven a crear)
docker compose restart localstack
sleep 10
make verify-dynamodb

# Opción 2: Limpiar todo y empezar de nuevo
make clean
make build
make up
```

## 🧪 Probar el Auth Service

Una vez que las tablas están creadas, puedes probar el servicio de autenticación:

```bash
# 1. Verificar que el servicio esté corriendo
curl http://localhost:8000/docs

# 2. Registrar un usuario (si el endpoint existe)
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "e_mail": "test@example.com",
    "password": "password123",
    "type_user": "basic"
  }'

# 3. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "e_mail": "test@example.com",
    "password": "password123"
  }'
```

## ❓ Troubleshooting

### Las tablas no se crean
```bash
# Ver logs del script de inicialización
docker logs localstack | grep -A 20 "init-dynamodb-tables"

# Verificar que el script está montado
docker exec localstack ls -la /etc/localstack/init/ready.d/

# Ejecutar manualmente el script dentro del contenedor
docker exec localstack sh /etc/localstack/init/ready.d/init-dynamodb-tables.sh
```

### Error: "Table already exists"
Es normal si reinicias LocalStack varias veces. LocalStack persiste datos en el volumen `localstack_data`. Para empezar desde cero:
```bash
make clean  # Elimina volúmenes
make up     # Recrea todo
```

### No puedo conectarme a DynamoDB desde el auth-service
Verifica las variables de entorno en `docker-compose.yml`:
```yaml
environment:
  - DYNAMODB_ENDPOINT_URL=http://localstack:4566
  - AWS_ACCESS_KEY_ID=test
  - AWS_SECRET_ACCESS_KEY=test
  - AWS_REGION=us-east-1
```

## 📚 Referencias

- Repositorio AuthRepository: `auth/repository/auth_repository.py`
- Script de inicialización: `localstack-init/init-dynamodb-tables.sh`
- Script de verificación: `verify-dynamodb-tables.sh`
- Documentación LocalStack: https://docs.localstack.cloud/
- AWS CLI DynamoDB: https://docs.aws.amazon.com/cli/latest/reference/dynamodb/

---

✅ **Las tablas se crean automáticamente al iniciar el proyecto. No requiere configuración manual.**
