# Unit Tests - Auth Service

Este directorio contiene las pruebas unitarias para la capa de servicio (`auth_service.py`).

## 📋 Estructura de Pruebas

- `test_auth_service.py`: Pruebas unitarias para todos los métodos del AuthService

## 🧪 Pruebas Implementadas

### Método: register(e_mail, password, type_user)
**Total: 7 pruebas**

- ✅ `test_register_success_new_user`: Registro exitoso de usuario nuevo
- ✅ `test_register_user_already_exists`: Usuario ya existe (retorna None)
- ✅ `test_register_with_admin_type`: Registro con tipo admin
- ✅ `test_register_password_hashing`: Verificar hasheo de contraseña
- ✅ `test_register_default_type_user`: Tipo de usuario por defecto ('basic')
- ✅ `test_register_user_state_is_true`: Usuario creado con state=True
- ✅ Verifica llamadas a `AuthRepository`: `get_user_by_email()`, `create_user()`, `add_email_to_type_user()`

### Método: login(e_mail, password)
**Total: 7 pruebas**

- ✅ `test_login_success_valid_credentials`: Login exitoso con credenciales válidas
- ✅ `test_login_user_not_found`: Usuario no existe (retorna None)
- ✅ `test_login_user_inactive`: Usuario inactivo state=False (retorna None)
- ✅ `test_login_wrong_password`: Contraseña incorrecta (retorna None)
- ✅ `test_login_jwt_token_expiration`: Token tiene expiración correcta (30 min)
- ✅ `test_login_jwt_contains_user_info`: JWT contiene sub, type_user, exp
- ✅ `test_login_saves_token_to_database`: Token se guarda en DynamoDB
- ✅ Verifica llamadas a `AuthRepository`: `get_user_by_email()`, `create_token()`

### Método: verify_token(token)
**Total: 10 pruebas**

- ✅ `test_verify_token_valid`: Token válido (retorna True)
- ✅ `test_verify_token_expired`: Token expirado (retorna False)
- ✅ `test_verify_token_invalid_signature`: Firma inválida (retorna False)
- ✅ `test_verify_token_malformed`: Token mal formado (retorna False)
- ✅ `test_verify_token_empty_string`: String vacío (retorna False)
- ✅ `test_verify_token_none`: Token None (retorna False o excepción)
- ✅ `test_verify_token_with_different_algorithm`: Algoritmo incorrecto (retorna False)
- ✅ `test_verify_token_missing_required_claims`: Sin claim 'exp' (retorna False)
- ✅ `test_verify_token_recently_expired`: Expirado hace 1 segundo (retorna False)
- ✅ `test_verify_token_about_to_expire`: Expira en 1 segundo (retorna True)

**Total de pruebas: 24 casos de prueba**

## 🚀 Cómo Ejecutar las Pruebas

### Requisitos Previos

Si aún no has configurado el entorno virtual:

```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### Ejecutar Todas las Pruebas del Service

```bash
# Activar el entorno virtual
source venv/bin/activate

# Ejecutar todas las pruebas del service
pytest tests/unit-test/service/test_auth_service.py -v
```

### Ejecutar una Clase de Pruebas Específica

```bash
# Activar entorno virtual
source venv/bin/activate

# Solo pruebas del método register()
pytest tests/unit-test/service/test_auth_service.py::TestRegisterMethod -v

# Solo pruebas del método login()
pytest tests/unit-test/service/test_auth_service.py::TestLoginMethod -v

# Solo pruebas del método verify_token()
pytest tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod -v
```

### Ejecutar una Prueba Individual

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejemplo: Solo test de registro exitoso
pytest tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_success_new_user -v

# Ejemplo: Solo test de login inválido
pytest tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_wrong_password -v

# Ejemplo: Solo test de token expirado
pytest tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_expired -v
```

### Ejecutar Todas las Pruebas Unitarias (Controller + Service)

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar todas las pruebas unitarias
pytest tests/unit-test/ -v

# Con resumen de cobertura
pytest tests/unit-test/ -v --tb=short
```

### Ver Cobertura de Código

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar coverage si no lo tienes
pip install pytest-cov

# Ejecutar con reporte de cobertura
pytest tests/unit-test/service/test_auth_service.py --cov=service.crud.auth_service --cov-report=html

# Ver reporte en htmlcov/index.html
```

### Opciones Útiles de pytest

```bash
# Modo verbose con salida detallada
pytest tests/unit-test/service/test_auth_service.py -v

# Mostrar print statements
pytest tests/unit-test/service/test_auth_service.py -v -s

# Detener en el primer error
pytest tests/unit-test/service/test_auth_service.py -x

# Ejecutar solo tests que fallaron la última vez
pytest tests/unit-test/service/test_auth_service.py --lf

# Ver resumen de todas las pruebas
pytest tests/unit-test/service/test_auth_service.py -v --tb=short

# Ejecutar tests en paralelo (instalar: pip install pytest-xdist)
pytest tests/unit-test/service/test_auth_service.py -n auto
```

## 🔧 Tecnologías y Mocks Utilizadas

- **pytest**: Framework de testing
- **unittest.mock**: Mocking de dependencias
- **PyJWT**: Para crear y verificar tokens JWT en las pruebas
- **passlib**: Para verificar hasheo de contraseñas

### Mocks Implementados

Las pruebas utilizan `@patch` para mockear dependencias externas:

#### 1. AuthRepository (Mockeado)
- `get_user_by_email()`: Retorna `SystemUser` o `None`
- `create_user()`: Simula creación de usuario en DynamoDB
- `add_email_to_type_user()`: Simula asociación email-tipo en DynamoDB
- `create_token()`: Simula guardado de token en DynamoDB

#### 2. get_dynamo_client() (Mockeado)
- Mock del cliente de DynamoDB para evitar conexión real

#### 3. pwd_context (Mockeado cuando necesario)
- `hash()`: Simula hasheo de contraseñas
- `verify()`: Simula verificación de contraseñas

### SystemUser y Token (Objetos Reales)
- Se usan instancias reales de estos modelos para las aserciones

## 📊 Resultado Esperado

Al ejecutar todas las pruebas del service, deberías ver:

```
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_success_new_user PASSED              [  4%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_user_already_exists PASSED          [  8%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_with_admin_type PASSED              [ 12%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_password_hashing PASSED             [ 16%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_default_type_user PASSED            [ 20%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_user_state_is_true PASSED           [ 25%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_success_valid_credentials PASSED          [ 29%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_user_not_found PASSED                     [ 33%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_user_inactive PASSED                      [ 37%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_wrong_password PASSED                     [ 41%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_jwt_token_expiration PASSED               [ 45%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_jwt_contains_user_info PASSED             [ 50%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_saves_token_to_database PASSED            [ 54%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_valid PASSED                 [ 58%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_expired PASSED               [ 62%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_invalid_signature PASSED     [ 66%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_malformed PASSED             [ 70%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_empty_string PASSED          [ 75%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_none PASSED                  [ 79%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_with_different_algorithm PASSED [ 83%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_missing_required_claims PASSED [ 87%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_recently_expired PASSED      [ 91%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_about_to_expire PASSED       [ 95%]

========================== 24 passed in X.XXs ==========================
```

## 🎯 Cobertura de Casos de Prueba

### AuthService.register()
- ✅ Caso exitoso (usuario nuevo)
- ✅ Usuario ya existe
- ✅ Diferentes tipos de usuario (basic, admin)
- ✅ Hasheo de contraseña
- ✅ Estado del usuario
- ✅ Asociación email-tipo

### AuthService.login()
- ✅ Login exitoso
- ✅ Usuario no existe
- ✅ Usuario inactivo
- ✅ Contraseña incorrecta
- ✅ Generación de JWT
- ✅ Contenido del JWT
- ✅ Expiración del JWT
- ✅ Guardado del token en BD

### AuthService.verify_token()
- ✅ Token válido
- ✅ Token expirado
- ✅ Firma inválida
- ✅ Token mal formado
- ✅ String vacío
- ✅ None
- ✅ Algoritmo incorrecto
- ✅ Claims faltantes
- ✅ Casos límite de expiración

## 💡 Notas Importantes

1. **Mocks de AuthRepository**: Todas las llamadas a DynamoDB están mockeadas
2. **JWT Real**: Se generan y verifican tokens JWT reales para probar la lógica
3. **Passlib**: Se mockea cuando se necesita controlar el resultado del hash
4. **Independencia**: Cada prueba es independiente y puede ejecutarse por separado
5. **Cobertura Completa**: Se cubren casos exitosos, errores y casos límite

## 🐛 Troubleshooting

### Error: ModuleNotFoundError
```bash
# Asegúrate de tener el paquete instalado en modo editable
source venv/bin/activate
pip install -e .
```

### Error: Import "pytest" could not be resolved
```bash
# Instalar dependencias dentro del entorno virtual
source venv/bin/activate
pip install -r requirements.txt
```

### Las pruebas fallan con errores de JWT
```bash
# Verificar que PyJWT esté instalado
pip list | grep PyJWT

# Si no está, instalarlo
pip install PyJWT
```

## 🔗 Documentación Relacionada

- Controller tests: `auth/tests/unit-test/controller/README.md`
- Guía rápida: `auth/GUIA_RAPIDA_TESTS.md`
