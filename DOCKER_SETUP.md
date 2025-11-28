# Configuración para Desarrollo Local

## Ajustes necesarios en los microservicios

### 1. Auth Service (auth/main.py)

Para soportar DynamoDB Local, asegúrate de que tu código pueda configurar el endpoint:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Variable para endpoint local (solo desarrollo)
DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL")
```

En tu configuration/database.py:
```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_dynamo_client():
    session = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION"),
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT_URL", None)  # None en producción
    )
    return session
```

### 2. Users Service (users/app/configuration/database.py)

Tu configuración ya soporta variables de entorno. Solo verifica:

```python
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")  # "mysql" en docker-compose
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
```

## Estructura de Volúmenes

- `mysql_data`: Almacena la base de datos MySQL
- `dynamodb_data`: Almacena datos de DynamoDB Local

## Health Checks

Todos los servicios tienen health checks configurados:
- MySQL: ping a través de mysqladmin
- DynamoDB: curl al endpoint
- App Services: Reintentos automáticos

## Networking

Los servicios se comunican usando nombres de servicio:
- MySQL: `mysql:3306`
- DynamoDB: `dynamodb-local:8000`
- Auth Service: `auth-service:8000`
- Users Service: `users-service:8001`

## Troubleshooting

### Puerto ya en uso
```bash
# Ver qué proceso usa el puerto
lsof -i :8000
lsof -i :8001
lsof -i :3306

# Liberar puerto (Linux/Mac)
kill -9 <PID>
```

### Contenedor no inicia
```bash
# Ver logs detallados
docker-compose logs auth-service
docker-compose logs users-service
docker-compose logs mysql
```

### MySQL no se conecta
- Espera 10-15 segundos después de `make up`
- Verifica que MySQL está sano: `docker-compose ps`
- Reinicia MySQL: `docker-compose restart mysql`

### Cambiar plugin de autenticación MySQL a `mysql_native_password`

Para evitar el error `Public Key Retrieval is not allowed` desde clientes JDBC (DBeaver, etc.) hemos configurado el usuario `admin` para que use `mysql_native_password`.

En el entorno local el script `users/db/00-change-auth-plugin.sql` se monta en `/docker-entrypoint-initdb.d/`; se aplica automáticamente cuando la base de datos es creada por primera vez.

Si la base de datos ya existe (volumen persistente), puedes aplicar el cambio sin perder datos ejecutando:

```bash
make mysql-native-auth
```

Esto ejecuta:

```sql
ALTER USER 'admin'@'%' IDENTIFIED WITH mysql_native_password BY 'teamb321**';
FLUSH PRIVILEGES;
```

En producción (RDS, CloudSQL), ejecuta la instrucción `ALTER USER` con las credenciales de administrador del servicio gestionado o mediante la consola de administración de tu proveedor.

### DynamoDB Local no responde
- Verifica: `curl http://localhost:8000`
- Reinicia: `docker-compose restart dynamodb-local`
