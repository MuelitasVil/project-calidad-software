# ⚡ Guía Rápida - Ejecutar Pruebas Unitarias

## Setup Inicial (Solo la primera vez)

```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth

# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Instalar paquete en modo editable
pip install -e .
```

## Ejecutar Pruebas

```bash
# Activar entorno virtual (siempre que abras una nueva terminal)
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth
source venv/bin/activate

# Ejecutar TODAS las pruebas unitarias (controller + service + repository)
pytest tests/unit-test/ -v

# Ejecutar solo pruebas del controller
pytest tests/unit-test/controller/test_auth_controller.py -v

# Ejecutar solo pruebas del service
pytest tests/unit-test/service/test_auth_service.py -v

# Ejecutar solo pruebas del repository
pytest tests/unit-test/repository/test_auth_repository.py -v

# Ejecutar con más detalle
pytest tests/unit-test/ -v -s

# Solo una clase específica
pytest tests/unit-test/service/test_auth_service.py::TestRegisterMethod -v

# Solo una prueba específica
pytest tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_success -v
```

## Resultado Esperado

✅ **60 passed** - Todas las pruebas pasaron exitosamente

### Controller Tests (15 pruebas)
```
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_success PASSED           [  2%]
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_user_already_exists PASSED [  5%]
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_invalid_email PASSED      [  7%]
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_short_password PASSED     [ 10%]
tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_with_admin_type PASSED    [ 13%]
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_success PASSED                  [ 15%]
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_invalid_credentials PASSED      [ 18%]
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_nonexistent_user PASSED         [ 21%]
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_invalid_email_format PASSED     [ 23%]
tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_missing_password PASSED         [ 26%]
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_valid PASSED   [ 28%]
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_expired PASSED [ 31%]
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_invalid PASSED [ 34%]
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_missing_parameter PASSED [ 36%]
tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_empty_string PASSED [ 39%]
```

### Service Tests (23 pruebas)
```
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_success_new_user PASSED          [ 42%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_user_already_exists PASSED       [ 44%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_with_admin_type PASSED           [ 47%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_password_hashing PASSED          [ 50%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_default_type_user PASSED         [ 52%]
tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_user_state_is_true PASSED        [ 55%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_success_valid_credentials PASSED       [ 57%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_user_not_found PASSED                  [ 60%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_user_inactive PASSED                   [ 63%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_wrong_password PASSED                  [ 65%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_jwt_token_expiration PASSED            [ 68%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_jwt_contains_user_info PASSED          [ 71%]
tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_saves_token_to_database PASSED         [ 73%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_valid PASSED              [ 76%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_expired PASSED            [ 78%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_invalid_signature PASSED  [ 81%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_malformed PASSED          [ 84%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_empty_string PASSED       [ 86%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_none PASSED               [ 89%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_with_different_algorithm PASSED [ 92%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_missing_required_claims PASSED [ 94%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_recently_expired PASSED   [ 97%]
tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_about_to_expire PASSED    [ 62%]
```

### Repository Tests (22 pruebas)
```
tests/unit-test/repository/test_auth_repository.py::TestAuthRepositoryInit::test_init_creates_tables_references PASSED [ 64%]
tests/unit-test/repository/test_auth_repository.py::TestCreateUser::test_create_user_success PASSED                   [ 67%]
tests/unit-test/repository/test_auth_repository.py::TestCreateUser::test_create_user_with_admin_type PASSED          [ 69%]
tests/unit-test/repository/test_auth_repository.py::TestCreateUser::test_create_user_with_inactive_state PASSED      [ 72%]
tests/unit-test/repository/test_auth_repository.py::TestGetUserByEmail::test_get_user_by_email_found PASSED          [ 75%]
tests/unit-test/repository/test_auth_repository.py::TestGetUserByEmail::test_get_user_by_email_not_found PASSED      [ 77%]
tests/unit-test/repository/test_auth_repository.py::TestGetUserByEmail::test_get_user_by_email_inactive_user PASSED  [ 80%]
tests/unit-test/repository/test_auth_repository.py::TestCreateToken::test_create_token_success PASSED                [ 82%]
tests/unit-test/repository/test_auth_repository.py::TestCreateToken::test_create_token_with_datetime_serialization PASSED [ 85%]
tests/unit-test/repository/test_auth_repository.py::TestGetToken::test_get_token_found PASSED                        [ 87%]
tests/unit-test/repository/test_auth_repository.py::TestGetToken::test_get_token_not_found PASSED                    [ 90%]
tests/unit-test/repository/test_auth_repository.py::TestGetTypeUser::test_get_type_user_found PASSED                 [ 92%]
tests/unit-test/repository/test_auth_repository.py::TestGetTypeUser::test_get_type_user_not_found PASSED             [ 95%]
tests/unit-test/repository/test_auth_repository.py::TestGetTypeUser::test_get_type_user_admin PASSED                 [ 97%]
tests/unit-test/repository/test_auth_repository.py::TestCreateTypeUser::test_create_type_user_success PASSED         [100%]
[... 7 pruebas más ...]

======================================== 60 passed in 1.41s ========================================
```

## 📝 Notas Importantes

- **Entorno Virtual**: Tu sistema Python está protegido (`externally-managed-environment`), por eso DEBES usar `venv`
- **Modo Editable**: El `pip install -e .` es necesario para que pytest encuentre los módulos de la aplicación
- **Activación**: Siempre activa el venv antes de ejecutar pruebas: `source venv/bin/activate`
- **Mocks**: Las pruebas usan mocks de `AuthService` (controller), `AuthRepository` (service) y DynamoDB client (repository)
- **Cobertura**: 60 pruebas unitarias totales (15 controller + 23 service + 22 repository)

## 📊 Resumen de Pruebas

### Controller (auth_controller.py) - 15 pruebas
- **POST /auth/register**: 5 pruebas (éxito, usuario existe, validaciones)
- **POST /auth/login**: 5 pruebas (éxito, credenciales inválidas, usuario inactivo)
- **GET /auth/validate-token**: 5 pruebas (válido, expirado, inválido)

### Service (auth_service.py) - 23 pruebas
- **register()**: 6 pruebas (registro, usuario existe, hasheo, tipos)
- **login()**: 7 pruebas (login exitoso, errores, JWT, guardado)
- **verify_token()**: 10 pruebas (válido, expirado, inválido, casos límite)

### Repository (auth_repository.py) - 22 pruebas
- **create_user()**: 3 pruebas (éxito, tipo admin, usuario inactivo)
- **get_user_by_email()**: 3 pruebas (encontrado, no existe, inactivo)
- **create_token()**: 2 pruebas (éxito, serialización datetime)
- **get_token()**: 2 pruebas (encontrado, no existe)
- **get_type_user()**: 3 pruebas (encontrado, no existe, admin)
- **create_type_user()**: 2 pruebas (éxito, tipo basic)
- **add_email_to_type_user()**: 6 pruebas (tipo existente, crear tipo, duplicados, múltiples emails, tipo admin, lista vacía)
- **__init__()**: 1 prueba (inicialización tablas)

## 🔗 Documentación Completa

- Controller: `auth/tests/unit-test/controller/README.md`
- Service: `auth/tests/unit-test/service/README.md`
- Repository: `auth/tests/unit-test/repository/README.md`
