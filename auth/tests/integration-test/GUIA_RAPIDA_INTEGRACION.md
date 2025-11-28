# ⚡ Guía Rápida - Pruebas de Integración

## 🎯 ¿Qué son las Pruebas de Integración?

Las pruebas de integración validan el **flujo completo de la aplicación** desde el controlador hasta la base de datos **sin usar mocks**:

```
HTTP Request → Controller → Service → Repository → DynamoDB REAL (LocalStack)
```

## ✅ Resultado: 7 pruebas de integración pasando

```bash
pytest tests/integration-test/ -v

# Resultado:
# 7 passed in 2.55s
```

## 🚀 Ejecutar Pruebas (Paso a Paso)

### 1. Verificar LocalStack

```bash
# LocalStack debe estar corriendo
docker ps | grep localstack

# Si no está corriendo, iniciarlo
docker-compose up -d localstack
```

### 2. Verificar Variables de Entorno

```bash
# El archivo .env debe existir en auth/
cat auth/.env

# Debe contener:
# AWS_REGION=us-east-1
# AWS_ACCESS_KEY_ID=test
# AWS_SECRET_ACCESS_KEY=test
# DYNAMODB_ENDPOINT_URL=http://localhost:4566
```

### 3. Verificar Tablas en DynamoDB

```bash
# Listar tablas
aws dynamodb list-tables --endpoint-url http://localhost:4566

# Debería mostrar:
# - auth_ms_usuario
# - auth_ms_jwt
# - auth_ms_type_user
```

### 4. Ejecutar Pruebas

```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth

# Activar entorno virtual
source venv/bin/activate

# Ejecutar todas las pruebas de integración
pytest tests/integration-test/ -v

# Con output detallado (muestra prints)
pytest tests/integration-test/ -v -s

# Solo una prueba específica
pytest tests/integration-test/test_auth_integration.py::TestRegisterIntegration::test_register_new_user_creates_record_in_database -v -s
```

## 📊 Pruebas Implementadas

### TestRegisterIntegration (5 pruebas)

1. ✅ **test_register_new_user_creates_record_in_database**
   - Registra usuario → Verifica en DynamoDB
   - Valida password hasheada con bcrypt
   - Verifica asociación con type_user

2. ✅ **test_register_duplicate_user_returns_error**
   - Intenta registrar usuario duplicado
   - Verifica error 400

3. ✅ **test_register_with_admin_type_creates_admin_user**
   - Registra usuario tipo 'admin'
   - Verifica en tabla auth_ms_type_user

4. ✅ **test_register_invalid_email_returns_validation_error**
   - Email inválido → Error 422

5. ✅ **test_register_and_verify_password_hashing**
   - Verifica formato bcrypt ($2b$)
   - Valida que el hash funciona

### TestRegisterIntegrationEdgeCases (2 pruebas)

6. ✅ **test_register_multiple_users_same_type**
   - Registra 3 usuarios del mismo tipo
   - Verifica todos en auth_ms_type_user

7. ✅ **test_register_empty_password_returns_validation_error**
   - Password vacío → Error de validación

## 🔥 Características Clave

- ✅ **Sin Mocks**: Todo es real (HTTP, DynamoDB)
- ✅ **LocalStack**: Simula AWS localmente
- ✅ **Cleanup Automático**: Elimina datos de prueba automáticamente
- ✅ **Emails Únicos**: Usa UUID para evitar conflictos
- ✅ **Verificación Directa en BD**: Lee datos reales de DynamoDB

## 🐛 Troubleshooting Rápido

### Error: "Unable to connect to DynamoDB"
```bash
# Verificar LocalStack
docker ps | grep localstack
curl http://localhost:4566
```

### Error: "ResourceNotFoundException"
```bash
# Crear las tablas (si no existen)
aws dynamodb list-tables --endpoint-url http://localhost:4566

# Si faltan tablas, crearlas (ver README.md completo)
```

### Error: "User already exists"
```bash
# Reiniciar LocalStack para limpiar datos
docker-compose restart localstack
```

## 📝 Verificar Datos en DynamoDB

```bash
# Ver todos los usuarios
aws dynamodb scan --table-name auth_ms_usuario --endpoint-url http://localhost:4566

# Ver tipos de usuario
aws dynamodb scan --table-name auth_ms_type_user --endpoint-url http://localhost:4566

# Ver tokens
aws dynamodb scan --table-name auth_ms_jwt --endpoint-url http://localhost:4566
```

## 🎯 Diferencias con Pruebas Unitarias

| Aspecto | Unit Tests | Integration Tests |
|---------|-----------|-------------------|
| **Mocks** | ✅ Sí | ❌ No |
| **Base de Datos** | 🎭 Mockeada | 🔥 Real (LocalStack) |
| **Velocidad** | ⚡ ~1.4s (60 tests) | 🐢 ~2.5s (7 tests) |
| **Scope** | Función individual | Flujo completo |
| **Detecta** | Bugs en lógica | Problemas de integración |

## 📚 Documentación Completa

- README completo: `tests/integration-test/README.md`
- Pruebas unitarias: `tests/unit-test/`
- Guía rápida tests: `GUIA_RAPIDA_TESTS.md`

## ✨ Comando Todo-en-Uno

```bash
cd auth && \
source venv/bin/activate && \
docker ps | grep localstack && \
pytest tests/integration-test/ -v
```

¡Listo! 🎉
