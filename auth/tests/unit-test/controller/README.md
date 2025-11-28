# Unit Tests - Auth Controller

Este directorio contiene las pruebas unitarias para el controlador de autenticación (`auth_controller.py`).

## 📋 Estructura de Pruebas

- `test_auth_controller.py`: Pruebas unitarias para los endpoints de autenticación

## 🧪 Pruebas Implementadas

### Endpoint: POST /auth/register
- ✅ `test_register_success`: Registro exitoso de nuevo usuario
- ✅ `test_register_user_already_exists`: Usuario ya existe (error 400)
- ✅ `test_register_invalid_email`: Email con formato inválido (error 422)
- ✅ `test_register_short_password`: Contraseña muy corta (error 422)
- ✅ `test_register_with_admin_type`: Registro de usuario tipo admin

### Endpoint: POST /auth/login
- ✅ `test_login_success`: Login exitoso con credenciales válidas
- ✅ `test_login_invalid_credentials`: Credenciales inválidas (error 401)
- ✅ `test_login_nonexistent_user`: Usuario no existe (error 401)
- ✅ `test_login_invalid_email_format`: Email inválido (error 422)
- ✅ `test_login_missing_password`: Password faltante (error 422)

### Endpoint: GET /auth/validate-token
- ✅ `test_validate_token_valid`: Token válido (retorna True)
- ✅ `test_validate_token_expired`: Token expirado (retorna False)
- ✅ `test_validate_token_invalid`: Token inválido (retorna False)
- ✅ `test_validate_token_missing_parameter`: Token faltante (error 422)
- ✅ `test_validate_token_empty_string`: Token vacío (retorna False)

## 🚀 Cómo Ejecutar las Pruebas

### Requisitos Previos

1. **Crear entorno virtual** (tu sistema Python está protegido):

```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth
python3 -m venv venv
source venv/bin/activate
```

2. **Instalar dependencias**:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Instalar el paquete en modo editable** (necesario para que pytest encuentre los módulos):

```bash
pip install -e .
```

### Ejecutar Todas las Pruebas del Controller

```bash
# Activar el entorno virtual (si no está activo)
source venv/bin/activate

# Ejecutar las pruebas
pytest tests/unit-test/controller/test_auth_controller.py -v
```

### Ejecutar una Clase de Pruebas Específica

```bash
# Activar entorno virtual
source venv/bin/activate

# Solo pruebas de registro
pytest tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint -v

# Solo pruebas de login
pytest tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint -v

# Solo pruebas de validación de token
pytest tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint -v
```

### Ejecutar una Prueba Individual

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejemplo: Solo test de registro exitoso
pytest tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_success -v

# Ejemplo: Solo test de login inválido
pytest tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_invalid_credentials -v
```

### Ver Cobertura de Código

```bash
# Instalar coverage si no lo tienes
pip install pytest-cov

# Ejecutar con reporte de cobertura
pytest tests/unit-test/controller/test_auth_controller.py --cov=controller --cov-report=html

# Ver reporte en htmlcov/index.html
```

### Opciones Útiles de pytest

```bash
# Modo verbose con salida detallada
pytest tests/unit-test/controller/test_auth_controller.py -v

# Mostrar print statements
pytest tests/unit-test/controller/test_auth_controller.py -s

# Detener en el primer error
pytest tests/unit-test/controller/test_auth_controller.py -x

# Ejecutar solo tests que fallaron la última vez
pytest tests/unit-test/controller/test_auth_controller.py --lf

# Ver resumen de todas las pruebas
pytest tests/unit-test/controller/test_auth_controller.py -v --tb=short
```

## 🔧 Tecnologías Utilizadas

- **pytest**: Framework de testing
- **unittest.mock**: Mocking de AuthService
- **FastAPI TestClient**: Cliente HTTP para testing de endpoints
- **Pydantic**: Validación de DTOs (RegisterInput, LoginInput)

## 📝 Mocks Implementados

Las pruebas utilizan `@patch` para mockear los métodos del `AuthService`:

- `AuthService.register()`: Retorna `SystemUser` o `None`
- `AuthService.login()`: Retorna token JWT (string) o `None`
- `AuthService.verify_token()`: Retorna `True` o `False`

Esto permite probar el controlador de forma aislada sin depender de DynamoDB ni otros servicios externos.

## 📊 Resultado Esperado

Al ejecutar las pruebas, deberías ver:

```
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_success PASSED
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_user_already_exists PASSED
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_invalid_email PASSED
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_short_password PASSED
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_with_admin_type PASSED
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_success PASSED
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_invalid_credentials PASSED
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_nonexistent_user PASSED
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_invalid_email_format PASSED
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_missing_password PASSED
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_valid PASSED
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_expired PASSED
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_invalid PASSED
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_missing_parameter PASSED
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_empty_string PASSED

========================= 15 passed in 0.XX seconds =========================
```

## 🎯 Arquitectura de las Pruebas

```
auth/
├── controller/
│   └── auth_controller.py          # Código bajo prueba
├── service/
│   └── crud/
│       └── auth_service.py         # Mock en las pruebas
└── tests/
    └── unit-test/
        └── controller/
            ├── __init__.py
            ├── test_auth_controller.py   # 15 pruebas unitarias
            └── README.md                 # Este archivo
```

## 💡 Notas Importantes

1. **Mocks**: Todos los métodos de `AuthService` están mockeados, no se conecta a DynamoDB
2. **Validaciones**: Las pruebas verifican tanto casos exitosos como errores (422, 400, 401)
3. **TestClient**: Simula requests HTTP sin levantar servidor
4. **Independencia**: Cada prueba es independiente y puede ejecutarse por separado

## 🐛 Troubleshooting

Si encuentras errores al ejecutar las pruebas:

### Error: externally-managed-environment
```bash
# Tu sistema Python está protegido. SOLUCIÓN: Usar entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Error: ModuleNotFoundError: No module named 'controller'
```bash
# Instalar el paquete en modo editable
source venv/bin/activate
pip install -e .
```

### Error: Import "pytest" could not be resolved
```bash
# Instalar dependencias dentro del entorno virtual
source venv/bin/activate
pip install -r requirements.txt
```

### Las pruebas no se ejecutan
```bash
# Verificar que estás en el directorio correcto y el venv está activo
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth
source venv/bin/activate
pytest tests/unit-test/controller/test_auth_controller.py -v
```
