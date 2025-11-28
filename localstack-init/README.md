# LocalStack Init Scripts

Esta carpeta contiene scripts de inicialización que se ejecutan automáticamente cuando LocalStack arranca.

## 📁 Contenido

### `init-dynamodb-tables.sh`
Script que crea las 3 tablas DynamoDB necesarias para el servicio de autenticación:

- `auth_ms_usuario` - Usuarios del sistema (PK: e_mail)
- `auth_ms_jwt` - Tokens JWT (PK: token)
- `auth_ms_type_user` - Tipos de usuario (PK: type_user)

## 🚀 Cómo Funciona

1. Esta carpeta se monta en el contenedor LocalStack en `/etc/localstack/init/ready.d/`
2. LocalStack ejecuta automáticamente todos los scripts `.sh` en esa carpeta cuando está listo
3. Los scripts se ejecutan una vez al arrancar (o cuando se reinicia el contenedor)

## 📝 Configuración en docker-compose.yml

```yaml
localstack:
  volumes:
    - ./localstack-init:/etc/localstack/init/ready.d
```

## ✅ Verificación

Para verificar que los scripts se ejecutaron correctamente:

```bash
# Ver logs de LocalStack (buscar mensajes del script)
docker logs localstack | grep "Creando tabla"

# Verificar tablas creadas
make verify-dynamodb

# O manualmente
docker exec localstack awslocal dynamodb list-tables
```

## 🔧 Añadir Más Scripts

Para añadir más inicializaciones:

1. Crear un nuevo archivo `.sh` en esta carpeta
2. Hacerlo ejecutable: `chmod +x nombre-script.sh`
3. Reiniciar LocalStack: `docker compose restart localstack`

Los scripts se ejecutan en orden alfabético.

## 📚 Referencias

- LocalStack Init Hooks: https://docs.localstack.cloud/references/init-hooks/
- Documentación de tablas: Ver `TABLAS_DYNAMODB.md` en la raíz del proyecto
