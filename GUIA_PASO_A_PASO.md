# 📖 GUÍA PASO A PASO - Ejecutar tu Proyecto en Local

## Paso 1: Preparación (5 minutos)

### 1.1 Verifica los requisitos
```bash
docker --version      # Debe estar instalado
docker compose version # Debe estar instalado (v2+)
```

**Resultado esperado:**
```
Docker version 20.10.x or higher
Docker Compose version v2.x or higher
```

### 1.2 Navega al directorio del proyecto
```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software
```

---

## Paso 2: Construir las Imágenes (10-15 minutos)

Ejecuta el siguiente comando para construir las imágenes Docker:

```bash
make build
```

> ⚠️ Si ves el error `make: docker-compose: No such file or directory`, tu sistema no tiene instalado `docker-compose` ni el `docker compose` plugin. A partir de ahora el `Makefile` detecta ambos formatos, pero si tienes problemas instala el plugin o añade un alias temporal:

```bash
# Instalar el plugin (Ubuntu/Debian con Docker Engine + repo oficial):
sudo apt-get update && sudo apt-get install -y docker-compose-plugin

# O crear un alias (temporal para la terminal actual):
alias docker-compose='docker compose'
```

Esto hará:
- ✅ Construir la imagen `auth-service` (Python 3.11 + FastAPI + boto3)
- ✅ Construir la imagen `users-service` (Python 3.11 + FastAPI + SQLModel + MySQL)

**Resultado esperado:**
```
🔨 Construyendo imágenes Docker...
[+] Building 45.2s (15/15) FINISHED
 => auth-service
 => users-service
```

---

## Paso 3: Iniciar los Servicios (5 minutos)

```bash
make up
```

Esto iniciará:

**Resultado esperado:**
```
🚀 Iniciando servicios...
✅ Servicios iniciados!

📝 URLs disponibles:
   - Auth Service:  http://localhost:8000/docs
   - Users Service: http://localhost:8001/docs
   - MySQL:         localhost:3306
   - LocalStack (DynamoDB): http://localhost:4566
```

  - LocalStack incluye DynamoDB y otros servicios AWS emulados localmente
  - Endpoint DynamoDB: `http://localhost:4566`
  - Health check: `http://localhost:4566/_localstack/health`

Los servicios necesitan tiempo para iniciarse. El script espera automáticamente.

---

## Paso 4: Verificar que Todo Funciona

### 4.1 Revisar estado de los contenedores
```bash
make ps
```

**Resultado esperado:**
```
NAME                  COMMAND                     SERVICE         STATUS
auth-service         uvicorn main:app ...        auth-service    Up
dynamodb-local       -jar DynamoDBLocal.jar ...  dynamodb-local  Up (healthy)
mysql-local          docker-entrypoint.sh ...    mysql           Up (healthy)
users-service        uvicorn app.main:app ...    users-service   Up
```

### 4.2 Acceder a Auth Service
Abre en tu navegador:
```
http://localhost:8000/docs
```

Deberías ver la interfaz Swagger de FastAPI del servicio de autenticación.

> ⚠️ Si no puedes abrir la URL, sigue estos pasos:

```bash
# 1) Verifica si el contenedor está publicado (puertos mapeados) y su estado:
make ps

# 2) Verifica qué puerto escucha el contenedor (si no aparece `0.0.0.0:8000->8000/tcp`):
docker ps --filter "name=auth-service" --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

# 3) Si `Ports` está vacío (no mapeado), fuerza su recreación para aplicar la configuración de puertos:
make recreate-auth

# 4) Si persiste el problema: recrea todo (reconstruye y recrea todos los servicios):
make recreate

# 5) Verifica logs para errores
make logs-auth
```

### 4.3 Acceder a Users Service
Abre en tu navegador:
```
http://localhost:8001/docs
```

Deberías ver la interfaz Swagger de FastAPI del servicio de usuarios.

### 4.4 Acceder a LocalStack DynamoDB
LocalStack proporciona un emulador completo de servicios AWS incluyendo DynamoDB.

**Tablas creadas automáticamente:**
Al ejecutar `make up`, LocalStack crea automáticamente las siguientes tablas:
- `auth_ms_usuario` - Usuarios del sistema (PK: e_mail)
- `auth_ms_jwt` - Tokens JWT (PK: token)
- `auth_ms_type_user` - Tipos de usuario (PK: type_user)

**Verificar tablas:**
```bash
# Comando rápido
make verify-dynamodb

# O manualmente
docker exec localstack awslocal dynamodb list-tables
```

**Gestionar DynamoDB:**
- **AWS CLI** apuntando a LocalStack:
```bash
aws dynamodb list-tables --endpoint-url http://localhost:4566
```

- **NoSQL Workbench** conectado a `http://localhost:4566`
- **Interfaz Web de LocalStack** en `http://localhost:4566/_localstack/health` para ver el estado

Verifica que LocalStack esté corriendo:
```bash
make ps
docker ps --filter "name=localstack" --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

📚 **Documentación completa**: Ver `TABLAS_DYNAMODB.md` para esquemas, ejemplos y comandos útiles.

### Herramientas GUI para DynamoDB
Si prefieres una interfaz gráfica dedicada:

- **NoSQL Workbench for Amazon DynamoDB** (aplicación oficial de AWS, desktop, gratuita)
  - Configura la conexión a: `http://localhost:4566`
- **Dynobase** (cliente GUI, con trial)
- **AWS CLI** para operaciones desde terminal:
```bash
# Listar tablas
aws dynamodb list-tables --endpoint-url http://localhost:4566

# Crear tabla de ejemplo
aws dynamodb create-table \
  --table-name test-table \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:4566
```

---

## Paso 5: Monitorizar y Depurar

### Ver logs de todos los servicios
```bash
make logs
```

Verás algo como:
```
auth-service      | INFO:     Application startup complete
users-service     | INFO:     Application startup complete
mysql-local       | [Server] /usr/sbin/mysqld: ready for connections
```

### Ver logs de un servicio específico
```bash
make logs-auth      # Solo auth
make logs-users     # Solo users
```

### Ejecutar comandos dentro de los contenedores
```bash
# Acceder a bash del auth service
docker compose exec auth-service bash

# Acceder a bash del users service
docker compose exec users-service bash

# Acceder a mysql
docker compose exec mysql bash
```

---

## Paso 6: Detener los Servicios

Cuando termines de trabajar:

```bash
# Detener sin perder datos
make down

# O limpiarlo todo (elimina base de datos)
make clean
```

---

## 🧪 Probar los Servicios

### Probar Auth Service
```bash
# En la interfaz Swagger o con curl:
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

### Probar Users Service
```bash
# Ver todos los usuarios
curl http://localhost:8001/

# En la interfaz Swagger o explorar endpoints
curl http://localhost:8001/docs
```

---

## 🔧 Solucionar Problemas

### Problema: Puerto 8000/8001/3306 ya en uso

```bash
# Ver qué proceso usa el puerto
lsof -i :8000
lsof -i :8001
lsof -i :3306

# Liberar el puerto (obtén el PID del comando anterior)
kill -9 <PID>
```

### Problema: Contenedor no inicia

```bash
# Ver logs detallados
docker compose logs auth-service
docker compose logs users-service

# Reconstruir imágenes
make rebuild

# Reiniciar todo
make down
make up
```

### Problema: MySQL no responde

```bash
# Esperar 15 segundos después de make up
sleep 15
make ps

# Si sigue sin responder, reiniciar MySQL
docker compose restart mysql
```

### Problema: DynamoDB Local no conecta

```bash
# Verificar que LocalStack esté corriendo y DynamoDB disponible
curl http://localhost:4566/_localstack/health

# Reiniciar LocalStack
docker compose restart localstack

# Ver logs de LocalStack
docker logs localstack --tail 100
```

---

## 📊 Resumen de Comandos Frecuentes

| Comando | Qué hace |
|---------|----------|
| `make up` | Inicia todos los servicios |
| `make down` | Detiene los servicios |
| `make logs` | Ve logs en tiempo real |
| `make ps` | Ver estado de contenedores |
| `make clean` | Limpia todo completamente |
| `make rebuild` | Reconstruye sin cache |
| `make restart` | Reinicia los servicios |

---

## ✅ Checklist de Confirmación

- [ ] Docker y Docker Compose instalados
- [ ] Estás en el directorio correcto: `/home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software`
- [ ] Ejecutaste `make build` sin errores
- [ ] Ejecutaste `make up` sin errores
- [ ] `make ps` muestra todos los contenedores "Up"
- [ ] Puedes acceder a http://localhost:8000/docs
- [ ] Puedes acceder a http://localhost:8001/docs
- [ ] Los logs no muestran errores críticos

---

## 🎉 ¡Éxito!

Si completaste todos estos pasos, tu proyecto está corriendo correctamente en local con Docker Compose.

Para más información:
- Ver `RESUMEN_EJECUTIVO.md`
- Ver `DOCKER_SETUP.md`
- Ver `ARQUITECTURA.md`
