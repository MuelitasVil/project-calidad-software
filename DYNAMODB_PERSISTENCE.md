# Gestión de Persistencia de DynamoDB (LocalStack)

## ⚠️ Limitación de LocalStack Community Edition

LocalStack Community Edition (versión gratuita) **NO soporta persistencia automática** de DynamoDB. Los datos se pierden cuando:
- Se reinicia el servicio de LocalStack
- Se apaga el computador
- Se ejecuta `docker compose down`

## ✅ Solución Implementada: Scripts de Backup y Restore

Hemos implementado scripts para hacer backup manual y restaurar los datos de DynamoDB.

### Comandos Disponibles

```bash
# Crear usuario admin (si no existe)
make seed-admin

# Hacer backup de todas las tablas DynamoDB
make backup-db

# Restaurar datos desde el último backup
make restore-db
```

### 📋 Flujo de Trabajo Recomendado

#### 1. Antes de apagar el sistema o bajar los servicios:

```bash
make backup-db
```

Esto guardará todas las tablas en `/tmp/dynamodb-backup/`:
- `auth_ms_usuario.json`
- `auth_ms_jwt.json`
- `auth_ms_type_user.json`

#### 2. Después de iniciar los servicios:

```bash
make up
sleep 10  # Esperar a que LocalStack esté listo
make restore-db
```

Esto restaurará todos los datos desde el backup.

#### 3. Para crear el usuario admin inicial:

```bash
make seed-admin
```

Esto creará el usuario:
- **Email:** `mhoyos@example.com`
- **Password:** `qwerty123`
- **Rol:** `admin`

### 🔄 Workflow Completo

```bash
# Inicio de desarrollo
make up
make restore-db  # Restaurar datos previos (si existen)

# ... trabajar ...

# Antes de cerrar
make backup-db   # Guardar datos
make down
```

### 📦 Ubicación de Backups

Los backups se guardan en `/tmp/dynamodb-backup/` en formato JSON. 

**Nota:** Este directorio se limpia al reiniciar el sistema operativo. Para persistencia permanente, puedes cambiar la ubicación a un directorio en tu home:

```bash
# Editar localstack-init/backup-dynamodb.sh
BACKUP_DIR="$HOME/dynamodb-backups"
```

### 🔧 Scripts Disponibles

- **`seed-admin.sh`**: Crea el usuario admin si no existe
- **`backup-dynamodb.sh`**: Exporta todas las tablas a JSON
- **`restore-dynamodb.sh`**: Importa datos desde archivos JSON

### 📝 Alternativas para Persistencia Completa

Si necesitas persistencia automática, considera:

1. **LocalStack Pro** ($$$): Soporta persistencia nativa con `PERSISTENCE=1`
2. **DynamoDB Local**: Alternativa de AWS que soporta persistencia
3. **Base de datos tradicional**: Usar PostgreSQL/MySQL en lugar de DynamoDB para desarrollo local

### 🐛 Troubleshooting

#### Error: "Admin user already exists"
El usuario admin ya está registrado. Si necesitas cambiarlo:

```bash
# Eliminar el usuario actual
aws dynamodb delete-item \
    --table-name auth_ms_usuario \
    --key '{"e_mail":{"S":"mhoyos@example.com"}}' \
    --endpoint-url http://localhost:4566 \
    --region us-east-1

# Crear nuevo admin
make seed-admin
```

#### Los datos no se restauran
Asegúrate de:
1. Haber hecho backup antes: `make backup-db`
2. Que las tablas existan: `make verify-dynamodb`
3. Que LocalStack esté listo (espera ~10 segundos después de `make up`)

#### No hay backups
Si no hay backups previos, crea el usuario admin desde cero:

```bash
make seed-admin
make backup-db  # Crear primer backup
```

### 📚 Comandos Útiles

```bash
# Ver tablas
aws dynamodb list-tables \
    --endpoint-url http://localhost:4566 \
    --region us-east-1

# Ver usuarios
aws dynamodb scan \
    --table-name auth_ms_usuario \
    --endpoint-url http://localhost:4566 \
    --region us-east-1

# Ver tipos de usuario
aws dynamodb scan \
    --table-name auth_ms_type_user \
    --endpoint-url http://localhost:4566 \
    --region us-east-1
```

### 🎯 Estado Actual del Sistema

- ✅ Usuario admin único: `mhoyos@example.com` (password: `qwerty123`)
- ✅ Scripts de backup/restore funcionando
- ✅ Validación de un solo admin implementada
- ✅ Frontend con badge de rol verde
- ✅ Componentes reutilizables (navbar/footer)

---

**Última actualización:** Diciembre 2, 2024
