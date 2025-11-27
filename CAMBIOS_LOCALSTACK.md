# Cambios Realizados: Migración de DynamoDB Admin a LocalStack

## 📋 Resumen
Se eliminó el servicio `dynamodb-admin` (que tenía problemas de conectividad/binding) y se reemplazó con **LocalStack**, una solución contenerizada robusta que emula servicios AWS incluyendo DynamoDB con soporte para gestión via AWS CLI y herramientas GUI.

## 🔄 Cambios en docker-compose.yml

### Eliminado
- ❌ Servicio `dynamodb-admin` (node:18-slim con instalación de npm package)
- ❌ Servicio `dynamodb-local` (comentado, puede eliminarse en el futuro)

### Añadido
- ✅ Servicio `localstack` (puerto 4566 para API, incluye DynamoDB)
- ✅ Volumen `localstack_data` para persistencia
- ✅ Healthcheck integrado en LocalStack

### Modificado
- 🔧 `auth-service`:
  - `DYNAMODB_ENDPOINT_URL`: `http://dynamodb-local:8000` → `http://localstack:4566`
  - `AWS_ACCESS_KEY_ID`: `local` → `test`
  - `AWS_SECRET_ACCESS_KEY`: `local` → `test`
  - `depends_on`: `dynamodb-local` → `localstack`

- 🔧 `users-service`:
  - `DYNAMODB_ENDPOINT_URL`: `http://dynamodb-local:8000` → `http://localstack:4566`
  - `AWS_ACCESS_KEY_ID`: `local` → `test`
  - `AWS_SECRET_ACCESS_KEY`: `test`

## 📝 Archivos Modificados

### 1. `docker-compose.yml`
- Reemplazado `dynamodb-admin` con `localstack`
- Comentado `dynamodb-local` (deprecado)
- Actualizado `auth-service` y `users-service` para usar LocalStack
- Añadido volumen `localstack_data`

### 2. `Makefile`
- Actualizado target `up` para mostrar URL de LocalStack
- Eliminado target `dynamodb-ui-host` (ya no necesario)

### 3. `GUIA_PASO_A_PASO.md`
- Sección 4.4: Reemplazada instrucciones de DynamoDB Admin con LocalStack
- Añadidas instrucciones para usar AWS CLI con LocalStack
- Actualizadas URLs de acceso
- Simplificado troubleshooting eliminando referencias a `dynamodb-admin`

### 4. `README.md`
- Actualizada sección "URLs de Acceso Local" con LocalStack
- Añadida sección "Gestionar DynamoDB Local" con instrucciones de AWS CLI
- Actualizada sección "Variables de Entorno" con credenciales `test`/`test`
- Actualizada descripción del servicio DynamoDB

### 5. Nuevo archivo: `test-localstack-dynamodb.sh`
- Script ejecutable para verificar funcionamiento de DynamoDB en LocalStack
- Incluye health check, creación de tabla de prueba, y listado de tablas
- Proporciona comandos de ejemplo para AWS CLI

## ✅ Ventajas de LocalStack

1. **Confiabilidad**: LocalStack es una solución madura y ampliamente adoptada
2. **Compatibilidad total**: Soporta AWS CLI, SDKs oficiales, y herramientas GUI
3. **Sin problemas de binding**: Healthcheck nativo, mapeo de puertos funciona correctamente
4. **Multiservicio**: Puede emular otros servicios AWS si se necesitan en el futuro
5. **Mejor documentación**: Comunidad activa y documentación oficial extensa

## 🧪 Verificación

### Servicios activos después del cambio:
```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Resultado esperado:
- ✅ `auth-service` en puerto 8000
- ✅ `users-service` en puerto 8001
- ✅ `localstack` en puerto 4566 (healthy)
- ✅ `mysql-local` en puerto 3306

### Health check de LocalStack:
```bash
curl http://localhost:4566/_localstack/health
```

### Prueba completa:
```bash
./test-localstack-dynamodb.sh
```

## 📌 Notas Importantes

1. **Puerto DynamoDB**: Ahora es `http://localhost:4566` (antes era 8002 para dynamodb-local)
2. **Credenciales AWS**: Usar `test`/`test` para desarrollo local (LocalStack no valida credenciales)
3. **AWS CLI**: Instalar con `pip install awscli` para gestionar DynamoDB desde terminal
4. **GUI Recomendadas**:
   - NoSQL Workbench (oficial AWS, gratuita)
   - Dynobase (comercial con trial)

## 🚀 Próximos Pasos Recomendados

1. Actualizar scripts de inicialización si crean tablas DynamoDB automáticamente
2. Considerar añadir scripts de seed para poblar datos de prueba en DynamoDB
3. Documentar schemas de tablas DynamoDB en el proyecto
4. Opcional: Eliminar completamente el servicio `dynamodb-local` comentado del docker-compose.yml

## 🔗 Enlaces Útiles

- LocalStack: https://localstack.cloud/
- AWS CLI: https://aws.amazon.com/cli/
- NoSQL Workbench: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html
- Dynobase: https://dynobase.dev/
