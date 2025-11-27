# 🚀 Inicio Rápido: LocalStack DynamoDB

## ✅ Cambio Completado
El servicio `dynamodb-admin` fue reemplazado por **LocalStack** para gestionar DynamoDB localmente.

## 📍 URLs Actualizadas

| Servicio | URL |
|----------|-----|
| Auth Service (Swagger) | http://localhost:8000/docs |
| Users Service (Swagger) | http://localhost:8001/docs |
| MySQL | localhost:3306 |
| **LocalStack DynamoDB** | **http://localhost:4566** |
| LocalStack Health | http://localhost:4566/_localstack/health |

## 🔧 Cómo Usar DynamoDB Ahora

### Opción 1: AWS CLI (Recomendada)

```bash
# Instalar AWS CLI si no la tienes
pip install awscli

# Listar tablas
aws dynamodb list-tables --endpoint-url http://localhost:4566

# Crear tabla
aws dynamodb create-table \
  --table-name mi-tabla \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:4566

# Probar todo con el script incluido
./test-localstack-dynamodb.sh
```

### Opción 2: NoSQL Workbench (GUI)

1. Descargar: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html
2. Abrir NoSQL Workbench
3. Crear nueva conexión:
   - **Type**: DynamoDB Local
   - **Endpoint**: `http://localhost:4566`
   - **Region**: `us-east-1`
4. Conectar y gestionar tablas visualmente

### Opción 3: Dynobase (GUI Comercial)

- Web: https://dynobase.dev/
- Conectar a: `http://localhost:4566`

## 🧪 Verificar que Funciona

```bash
# 1. Ver estado de servicios
docker ps

# 2. Health check de LocalStack
curl http://localhost:4566/_localstack/health

# 3. Verificar tablas DynamoDB creadas automáticamente
./verify-dynamodb-tables.sh

# 4. Ejecutar script de prueba completo
./test-localstack-dynamodb.sh

# 5. Ver logs si hay problemas
docker logs localstack
```

## 📊 Tablas DynamoDB Creadas Automáticamente

Al iniciar LocalStack, se crean **automáticamente** 3 tablas para el servicio de autenticación:

| Tabla | Primary Key | Descripción |
|-------|-------------|-------------|
| `auth_ms_usuario` | `e_mail` (String) | Usuarios del sistema (email, password, type_user, state) |
| `auth_ms_jwt` | `token` (String) | Tokens JWT emitidos (token, e_mail, created_at) |
| `auth_ms_type_user` | `type_user` (String) | Tipos de usuario y sus emails asociados |

**Verificar las tablas:**
```bash
# Ver tablas disponibles
docker exec localstack awslocal dynamodb list-tables

# Ver estructura de una tabla
docker exec localstack awslocal dynamodb describe-table --table-name auth_ms_usuario

# Script completo de verificación
./verify-dynamodb-tables.sh
```

## ⚡ Comandos Rápidos

```bash
# Reiniciar LocalStack
docker compose restart localstack

# Ver logs de LocalStack
docker logs -f localstack

# Recrear todo desde cero
make clean && make build && make up

# Ver todos los servicios
make ps
```

## 📦 Lo que Cambió

- ❌ **Eliminado**: `dynamodb-admin` (puerto 8003) - tenía problemas de binding
- ❌ **Deprecado**: `dynamodb-local` (puerto 8002) - reemplazado por LocalStack
- ✅ **Añadido**: `localstack` (puerto 4566) - solución robusta y completa
- 🔧 **Actualizado**: `auth-service` y `users-service` ahora apuntan a LocalStack

## 🎯 Próximos Pasos

1. **Probar el sistema**: `./test-localstack-dynamodb.sh`
2. **Instalar AWS CLI**: `pip install awscli`
3. **Descargar NoSQL Workbench** (opcional, para UI visual)
4. **Crear tus tablas** con los comandos de arriba
5. **Leer documentación completa**: Ver `CAMBIOS_LOCALSTACK.md`

## 💡 Tips

- LocalStack usa credenciales ficticias: `test` / `test` (no importa el valor)
- Todos los datos se persisten en el volumen `localstack_data`
- LocalStack puede emular otros servicios AWS si los necesitas en el futuro
- El endpoint es **siempre** `http://localhost:4566` (no 8002)

## ❓ Problemas Comunes

### "Connection refused" al puerto 4566
```bash
# Verificar que LocalStack está corriendo
docker ps | grep localstack

# Si no está, levantarlo
docker compose up -d localstack
```

### "Table already exists"
```bash
# Es normal si ejecutas el script de prueba varias veces
# Eliminar tabla:
aws dynamodb delete-table --table-name test-users --endpoint-url http://localhost:4566
```

### Ver tablas creadas
```bash
aws dynamodb list-tables --endpoint-url http://localhost:4566
```

---

**¡Todo listo!** LocalStack está funcionando y puedes gestionar DynamoDB con AWS CLI o herramientas GUI. 🎉
