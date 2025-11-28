# Pruebas de Integración - Auth Microservice

Este directorio contiene las **pruebas de integración** que validan el flujo completo de la aplicación desde el controlador hasta la base de datos real.

## 🎯 ¿Qué son las Pruebas de Integración?

Las pruebas de integración verifican que **múltiples componentes trabajen juntos correctamente**. A diferencia de las pruebas unitarias (que usan mocks), estas pruebas:

- ✅ Usan **recursos reales** (DynamoDB, HTTP)
- ✅ Validan el **flujo completo** de la aplicación
- ✅ **No usan mocks ni stubs**
- ✅ Detectan problemas de integración entre capas

### Flujo de las Pruebas de Integración

```
HTTP Request → FastAPI Controller → Service Layer → Repository → DynamoDB REAL
     ↓              ↓                    ↓              ↓             ↓
  TestClient   auth_controller    auth_service   auth_repository  AWS/Local
```

## 📋 Pruebas Implementadas

### `test_auth_integration.py` - Pruebas del endpoint POST /auth/register

#### **TestRegisterIntegration** (6 pruebas)

1. ✅ `test_register_new_user_creates_record_in_database`
   - Registra un usuario y verifica que existe en DynamoDB
   - Valida que la contraseña está hasheada con bcrypt
   - Verifica el campo `state=True`
   - Confirma la asociación con `auth_ms_type_user`

2. ✅ `test_register_duplicate_user_returns_error`
   - Intenta registrar un usuario duplicado
   - Verifica que retorna error 400
   - Confirma que no se crea un segundo registro

3. ✅ `test_register_with_admin_type_creates_admin_user`
   - Registra un usuario tipo 'admin'
   - Verifica que `type_user='admin'` en DynamoDB
   - Confirma asociación en tabla `auth_ms_type_user`

4. ✅ `test_register_invalid_email_returns_validation_error`
   - Envía un email con formato inválido
   - Verifica error 422 (Validation Error)

5. ✅ `test_register_and_verify_password_hashing`
   - Valida que la contraseña se hashea con bcrypt
   - Verifica el formato del hash (60 caracteres, $2b$)
   - Confirma que el hash es verificable
   - Valida que contraseñas incorrectas fallan

#### **TestRegisterIntegrationEdgeCases** (2 pruebas)

6. ✅ `test_register_multiple_users_same_type`
   - Registra 3 usuarios con el mismo `type_user`
   - Verifica que todos los emails están en `auth_ms_type_user`

7. ✅ `test_register_empty_password_returns_validation_error`
   - Intenta registrar con contraseña vacía
   - Verifica error de validación

**Total: 8 pruebas de integración**

## 🔧 Requisitos Previos

### 1. Base de Datos DynamoDB con LocalStack

Este proyecto usa **LocalStack** para simular servicios de AWS localmente, incluyendo DynamoDB.

#### Verificar que LocalStack está corriendo

```bash
# Ver si LocalStack está activo
docker ps | grep localstack

# Debería mostrar algo como:
# localstack/localstack:latest   "docker-entrypoint.sh"   Up X hours   0.0.0.0:4566->4566/tcp

# Si no está corriendo, iniciarlo (depende de tu configuración de docker-compose)
docker-compose up -d localstack
```

#### Verificar conexión a DynamoDB en LocalStack

```bash
# LocalStack usa el puerto 4566 para todos los servicios
curl http://localhost:4566

# O verificar específicamente DynamoDB
aws dynamodb list-tables --endpoint-url http://localhost:4566
```

### 2. Variables de Entorno

Crea o verifica tu archivo `.env` en la raíz del proyecto `auth/`:

```bash
# Para LocalStack (desarrollo local)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
DYNAMODB_ENDPOINT_URL=http://localhost:4566
```

**Nota**: LocalStack no requiere credenciales reales de AWS. Usa valores de prueba como `test`.

### 3. Crear las Tablas en DynamoDB (LocalStack)

Si usas **LocalStack**, necesitas crear las tablas manualmente:

```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth

# Activar entorno virtual
source venv/bin/activate

# Crear las tablas usando AWS CLI apuntando a LocalStack (puerto 4566)
aws dynamodb create-table \
    --table-name auth_ms_usuario \
    --attribute-definitions AttributeName=e_mail,AttributeType=S \
    --key-schema AttributeName=e_mail,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:4566

aws dynamodb create-table \
    --table-name auth_ms_jwt \
    --attribute-definitions AttributeName=token,AttributeType=S \
    --key-schema AttributeName=token,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:4566

aws dynamodb create-table \
    --table-name auth_ms_type_user \
    --attribute-definitions AttributeName=type_user,AttributeType=S \
    --key-schema AttributeName=type_user,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url http://localhost:4566
```

### 4. Verificar Tablas Creadas

```bash
# Listar tablas en LocalStack DynamoDB
aws dynamodb list-tables --endpoint-url http://localhost:4566

# Debería mostrar:
# {
#     "TableNames": [
#         "auth_ms_usuario",
#         "auth_ms_jwt",
#         "auth_ms_type_user"
#     ]
# }
```

## 🚀 Cómo Ejecutar las Pruebas

### Setup Inicial (Primera vez)

```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth

# Activar entorno virtual
source venv/bin/activate

# Verificar que todas las dependencias están instaladas
pip install -r requirements.txt
pip install -e .
```

### Ejecutar Todas las Pruebas de Integración

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar todas las pruebas de integración con output verbose
pytest tests/integration-test/ -v

# Con más detalle (muestra prints)
pytest tests/integration-test/ -v -s

# Con resumen corto
pytest tests/integration-test/ -v --tb=short
```

### Ejecutar Pruebas Específicas

```bash
# Solo la clase TestRegisterIntegration
pytest tests/integration-test/test_auth_integration.py::TestRegisterIntegration -v

# Solo casos límite
pytest tests/integration-test/test_auth_integration.py::TestRegisterIntegrationEdgeCases -v

# Solo una prueba específica
pytest tests/integration-test/test_auth_integration.py::TestRegisterIntegration::test_register_new_user_creates_record_in_database -v
```

### Ejecutar con Reportes de Cobertura

```bash
# Instalar coverage si no lo tienes
pip install pytest-cov

# Ejecutar con reporte de cobertura
pytest tests/integration-test/ --cov=controller --cov=service --cov=repository --cov-report=html

# Ver reporte en el navegador
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## 📊 Resultado Esperado

Al ejecutar las pruebas de integración, deberías ver algo como:

```
====================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.6.0
rootdir: /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth
configfile: pytest.ini
plugins: anyio-4.11.0, asyncio-0.25.2
collected 8 items

tests/integration-test/test_auth_integration.py::TestRegisterIntegration::test_register_new_user_creates_record_in_database PASSED [ 12%]
🧪 Testing integration with email: integration_test_a1b2c3d4@test.com
✅ Usuario encontrado en DynamoDB: {...}
✅ Tipo de usuario verificado: {...}
🧹 Cleanup: Usuario integration_test_a1b2c3d4@test.com eliminado de DynamoDB

tests/integration-test/test_auth_integration.py::TestRegisterIntegration::test_register_duplicate_user_returns_error PASSED [ 25%]
tests/integration-test/test_auth_integration.py::TestRegisterIntegration::test_register_with_admin_type_creates_admin_user PASSED [ 37%]
tests/integration-test/test_auth_integration.py::TestRegisterIntegration::test_register_invalid_email_returns_validation_error PASSED [ 50%]
tests/integration-test/test_auth_integration.py::TestRegisterIntegration::test_register_and_verify_password_hashing PASSED [ 62%]
tests/integration-test/test_auth_integration.py::TestRegisterIntegrationEdgeCases::test_register_multiple_users_same_type PASSED [ 75%]
tests/integration-test/test_auth_integration.py::TestRegisterIntegrationEdgeCases::test_register_empty_password_returns_validation_error PASSED [ 87%]

======================================== 8 passed in X.XXs ========================================
```

## 🔍 Diferencias: Pruebas Unitarias vs Pruebas de Integración

| Aspecto | Pruebas Unitarias | Pruebas de Integración |
|---------|-------------------|------------------------|
| **Scope** | Una función/método aislado | Múltiples componentes juntos |
| **Mocks** | ✅ Usa mocks extensivamente | ❌ No usa mocks (recursos reales) |
| **Velocidad** | ⚡ Muy rápidas (~1-2s para 60 pruebas) | 🐢 Más lentas (~5-10s para 8 pruebas) |
| **Base de Datos** | 🎭 Mockeada (MagicMock) | 🔥 Real (DynamoDB) |
| **HTTP** | 🎭 Mockeada (TestClient con mocks) | 🔥 Real (TestClient + FastAPI) |
| **Propósito** | Verificar lógica de negocio | Verificar integración completa |
| **Ejecutar en CI/CD** | ✅ Siempre | 🔶 Opcional (requiere infra) |
| **Detecta** | Bugs en lógica | Problemas de integración |

## 🧹 Limpieza Automática

Las pruebas de integración usan **fixtures de cleanup** que eliminan automáticamente los datos de prueba:

- `cleanup_test_user`: Elimina el usuario de prueba después de cada test
- `cleanup_test_tokens`: Elimina tokens de prueba después de cada test
- `test_email`: Genera emails únicos usando UUID para evitar conflictos

**No necesitas limpiar manualmente** después de ejecutar las pruebas.

## 🐛 Troubleshooting

### Error: "Unable to connect to DynamoDB"

```bash
# Verificar que LocalStack está corriendo
docker ps | grep localstack

# Si no está corriendo, iniciarlo
docker-compose up -d localstack

# Verificar que el puerto 4566 está accesible
curl http://localhost:4566
```

### Error: "ResourceNotFoundException: Requested resource not found"

Las tablas no existen en DynamoDB. Créalas siguiendo la sección **"3. Crear las Tablas en DynamoDB"**.

### Error: "ModuleNotFoundError"

```bash
# Instalar el paquete en modo editable
source venv/bin/activate
pip install -e .
```

### Las pruebas fallan con "User already exists"

Esto puede suceder si una ejecución anterior no limpió correctamente los datos. Soluciones:

```bash
# Opción 1: Reiniciar LocalStack (elimina todos los datos)
docker-compose restart localstack

# Opción 2: Eliminar manualmente el usuario de prueba
aws dynamodb delete-item \
    --table-name auth_ms_usuario \
    --key '{"e_mail": {"S": "email_del_test@test.com"}}' \
    --endpoint-url http://localhost:4566
```

### Ver datos en LocalStack DynamoDB

```bash
# Escanear tabla de usuarios
aws dynamodb scan \
    --table-name auth_ms_usuario \
    --endpoint-url http://localhost:4566

# Escanear tabla de tipos
aws dynamodb scan \
    --table-name auth_ms_type_user \
    --endpoint-url http://localhost:4566
```

## 💡 Mejores Prácticas

1. **Ejecutar con LocalStack en desarrollo**: Simula AWS sin costos y es más rápido
2. **Usar emails únicos**: Las fixtures generan emails con UUID automáticamente
3. **Verificar cleanup**: Las fixtures limpian automáticamente después de cada prueba
4. **No commitear .env**: El archivo `.env` debe estar en `.gitignore`
5. **Ejecutar antes de hacer merge**: Las pruebas de integración detectan problemas reales
6. **LocalStack persiste datos**: Reinicia LocalStack si necesitas limpiar completamente

## 🎯 Próximos Pasos

Para extender las pruebas de integración:

1. Agregar pruebas para `POST /auth/login`
2. Agregar pruebas para `GET /auth/validate-token`
3. Agregar pruebas de rendimiento (tiempo de respuesta)
4. Agregar pruebas de concurrencia (múltiples requests simultáneos)
5. Agregar pruebas de edge cases (límites de caracteres, SQL injection, etc.)

## 📚 Documentación Relacionada

- Pruebas Unitarias: `auth/tests/unit-test/`
- Guía Rápida de Tests: `auth/GUIA_RAPIDA_TESTS.md`
- Comandos pytest: `auth/COMANDOS_PYTEST.md`
- Resumen de Pruebas: `auth/RESUMEN_PRUEBAS_UNITARIAS.md`

## 📞 Soporte

Si tienes problemas ejecutando las pruebas de integración:

1. Verifica que DynamoDB está corriendo
2. Verifica las variables de entorno en `.env`
3. Verifica que las tablas existen
4. Revisa los logs de las pruebas con `-v -s`
5. Consulta la sección de Troubleshooting
