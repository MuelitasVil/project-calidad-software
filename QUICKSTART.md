# 🚀 Quick Start Guide

## Para Empezar en 30 Segundos

```bash
./start-dev.sh
```

Espera a que termine y luego:
- **Frontend**: http://localhost:3000
- **Login**: mhoyos@example.com / qwerty123

## Para Detener

```bash
./stop-dev.sh
```

## ¿Qué Hace Automáticamente?

### start-dev.sh
1. ✅ Inicia todos los servicios Docker
2. ✅ Espera a que estén listos
3. ✅ Restaura datos previos (si existen)
4. ✅ Si no hay datos, crea el usuario admin
5. ✅ Hace un backup inicial

### stop-dev.sh
1. ✅ Hace backup de todos los datos
2. ✅ Detiene los servicios
3. ✅ Datos guardados en `/tmp/dynamodb-backup/`

## Usuario Admin

- **Email:** mhoyos@example.com
- **Password:** qwerty123
- **Rol:** admin

⚠️ **Solo puede existir UN admin** (requisito RF1.4)

## Comandos Útiles

```bash
# Ver logs en tiempo real
make logs

# Ver estado de contenedores
make ps

# Hacer backup manual
make backup-db

# Restaurar datos manualmente
make restore-db

# Ver todos los comandos
make help
```

## Solución de Problemas

### No puedo hacer login
```bash
make logs-auth
```

### Los datos no están
```bash
make restore-db
```

### Quiero empezar desde cero
```bash
make down
rm -rf /tmp/dynamodb-backup
./start-dev.sh
```

## URLs del Sistema

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:3000 |
| Auth API | http://localhost:8000/docs |
| Users API | http://localhost:8001/docs |
| MySQL | localhost:3306 |
| LocalStack | http://localhost:4566 |

## Estructura del Proyecto

```
project-calidad-software/
├── start-dev.sh           ← Inicia todo (USAR ESTE)
├── stop-dev.sh            ← Detiene todo (USAR ESTE)
├── front/                 ← Frontend (Nginx + JavaScript)
├── auth/                  ← Auth Service (FastAPI + DynamoDB)
├── users/                 ← Users Service (FastAPI + MySQL)
└── localstack-init/       ← Scripts de persistencia
    ├── backup-dynamodb.sh
    ├── restore-dynamodb.sh
    └── seed-admin.sh
```

## Documentación Completa

- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - Resumen de todo lo implementado
- **[DYNAMODB_PERSISTENCE.md](./DYNAMODB_PERSISTENCE.md)** - Guía detallada de persistencia
- **[README.md](./README.md)** - Documentación completa del proyecto

## ⚠️ Importante

1. **Siempre usa `./stop-dev.sh`** para detener (hace backup automático)
2. Los backups se guardan en `/tmp/dynamodb-backup/`
3. `/tmp/` se limpia al reiniciar el computador (considera cambiar la ubicación)
4. Solo puede existir un usuario admin

## Tips

### Cambiar ubicación de backups (persistencia permanente)

Edita `localstack-init/backup-dynamodb.sh`:
```bash
# Cambia esta línea:
BACKUP_DIR="/tmp/dynamodb-backup"

# Por esta:
BACKUP_DIR="$HOME/Documents/dynamodb-backups"
```

### Ver datos en DynamoDB

```bash
# Usuarios
aws dynamodb scan \
  --table-name auth_ms_usuario \
  --endpoint-url http://localhost:4566 \
  --region us-east-1 \
  --no-cli-pager

# Tipos de usuario
aws dynamodb scan \
  --table-name auth_ms_type_user \
  --endpoint-url http://localhost:4566 \
  --region us-east-1 \
  --no-cli-pager
```

---

**¿Necesitas ayuda?** Lee la [documentación completa](./IMPLEMENTATION_SUMMARY.md)
