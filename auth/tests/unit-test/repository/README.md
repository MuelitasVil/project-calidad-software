# Unit Tests - Auth Repository

Este directorio contiene las pruebas unitarias para la capa de repositorio (`auth_repository.py`).

## 📋 Estructura de Pruebas

- `test_auth_repository.py`: Pruebas unitarias para todos los métodos del AuthRepository

## 🧪 Pruebas Implementadas

### Inicialización (1 prueba)
- ✅ `test_init_creates_tables_references`: Verificar creación de referencias a tablas DynamoDB

### Método: create_user(user)
**Total: 3 pruebas**

- ✅ `test_create_user_success`: Crear usuario exitosamente
- ✅ `test_create_user_with_admin_type`: Crear usuario tipo admin
- ✅ `test_create_user_with_inactive_state`: Crear usuario inactivo (state=False)

### Método: get_user_by_email(e_mail)
**Total: 3 pruebas**

- ✅ `test_get_user_by_email_found`: Usuario encontrado
- ✅ `test_get_user_by_email_not_found`: Usuario no existe (retorna None)
- ✅ `test_get_user_by_email_inactive_user`: Usuario inactivo

### Método: create_token(token)
**Total: 2 pruebas**

- ✅ `test_create_token_success`: Crear token exitosamente
- ✅ `test_create_token_with_datetime_serialization`: Verificar serialización de datetime a isoformat

### Método: get_token(token_value)
**Total: 2 pruebas**

- ✅ `test_get_token_found`: Token encontrado
- ✅ `test_get_token_not_found`: Token no existe (retorna None)

### Método: get_type_user(type_user)
**Total: 3 pruebas**

- ✅ `test_get_type_user_found`: Tipo de usuario encontrado
- ✅ `test_get_type_user_not_found`: Tipo no existe (retorna None)
- ✅ `test_get_type_user_admin`: Obtener tipo admin

### Método: create_type_user(type_user, e_mail)
**Total: 2 pruebas**

- ✅ `test_create_type_user_success`: Crear nuevo tipo de usuario
- ✅ `test_create_type_user_basic`: Crear tipo basic

### Método: add_email_to_type_user(type_user, e_mail)
**Total: 6 pruebas**

- ✅ `test_add_email_to_existing_type_user`: Agregar email a tipo existente
- ✅ `test_add_email_to_type_user_when_type_not_exists`: Crear tipo si no existe
- ✅ `test_add_duplicate_email_to_type_user`: No duplicar emails
- ✅ `test_add_multiple_emails_sequentially`: Agregar múltiples emails
- ✅ `test_add_email_to_admin_type`: Agregar email a tipo admin
- ✅ `test_add_email_with_empty_emails_list`: Agregar cuando lista está vacía

**Total de pruebas: 22 casos de prueba**

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

### Ejecutar Todas las Pruebas del Repository

```bash
# Activar el entorno virtual
source venv/bin/activate

# Ejecutar todas las pruebas del repository
pytest tests/unit-test/repository/test_auth_repository.py -v
```

### Ejecutar una Clase de Pruebas Específica

```bash
# Activar entorno virtual
source venv/bin/activate

# Solo pruebas de inicialización
pytest tests/unit-test/repository/test_auth_repository.py::TestAuthRepositoryInit -v

# Solo pruebas de create_user()
pytest tests/unit-test/repository/test_auth_repository.py::TestCreateUser -v

# Solo pruebas de get_user_by_email()
pytest tests/unit-test/repository/test_auth_repository.py::TestGetUserByEmail -v

# Solo pruebas de tokens (create_token y get_token)
pytest tests/unit-test/repository/test_auth_repository.py::TestCreateToken -v
pytest tests/unit-test/repository/test_auth_repository.py::TestGetToken -v

# Solo pruebas de tipos de usuario
pytest tests/unit-test/repository/test_auth_repository.py::TestGetTypeUser -v
pytest tests/unit-test/repository/test_auth_repository.py::TestCreateTypeUser -v
pytest tests/unit-test/repository/test_auth_repository.py::TestAddEmailToTypeUser -v
```

### Ejecutar una Prueba Individual

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejemplo: Solo test de crear usuario
pytest tests/unit-test/repository/test_auth_repository.py::TestCreateUser::test_create_user_success -v

# Ejemplo: Solo test de obtener usuario
pytest tests/unit-test/repository/test_auth_repository.py::TestGetUserByEmail::test_get_user_by_email_found -v

# Ejemplo: Solo test de agregar email
pytest tests/unit-test/repository/test_auth_repository.py::TestAddEmailToTypeUser::test_add_email_to_existing_type_user -v
```

### Ejecutar Todas las Pruebas Unitarias (Controller + Service + Repository)

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
pytest tests/unit-test/repository/test_auth_repository.py --cov=repository.auth_repository --cov-report=html

# Ver reporte en htmlcov/index.html
```

### Opciones Útiles de pytest

```bash
# Modo verbose con salida detallada
pytest tests/unit-test/repository/test_auth_repository.py -v

# Mostrar print statements
pytest tests/unit-test/repository/test_auth_repository.py -v -s

# Detener en el primer error
pytest tests/unit-test/repository/test_auth_repository.py -x

# Ejecutar solo tests que fallaron la última vez
pytest tests/unit-test/repository/test_auth_repository.py --lf

# Ver resumen de todas las pruebas
pytest tests/unit-test/repository/test_auth_repository.py -v --tb=short

# Buscar tests por nombre
pytest tests/unit-test/repository/ -k "create_user" -v
pytest tests/unit-test/repository/ -k "token" -v
pytest tests/unit-test/repository/ -k "type_user" -v
```

## 🔧 Tecnologías y Mocks Utilizadas

- **pytest**: Framework de testing
- **unittest.mock**: Mocking de dependencias DynamoDB
- **MagicMock**: Para simular objetos complejos de boto3

### Mocks Implementados

Las pruebas utilizan `MagicMock` para mockear las dependencias de AWS DynamoDB:

#### 1. DynamoDB Client (Mockeado)
- `dynamo_client.Table()`: Retorna tabla mockeada

#### 2. DynamoDB Tables (Mockeadas)
- `user_table.put_item()`: Simula guardado de usuario
- `user_table.get_item()`: Simula obtención de usuario
- `token_table.put_item()`: Simula guardado de token
- `token_table.get_item()`: Simula obtención de token
- `type_user_table.put_item()`: Simula guardado de tipo
- `type_user_table.get_item()`: Simula obtención de tipo
- `type_user_table.update_item()`: Simula actualización de emails

### SystemUser, Token (Objetos Reales)
- Se usan instancias reales de estos modelos para las aserciones

## 📊 Resultado Esperado

Al ejecutar todas las pruebas del repository, deberías ver:

```
tests/unit-test/repository/test_auth_repository.py::TestAuthRepositoryInit::test_init_creates_tables_references PASSED [ 4%]
tests/unit-test/repository/test_auth_repository.py::TestCreateUser::test_create_user_success PASSED                  [ 8%]
tests/unit-test/repository/test_auth_repository.py::TestCreateUser::test_create_user_with_admin_type PASSED         [12%]
tests/unit-test/repository/test_auth_repository.py::TestCreateUser::test_create_user_with_inactive_state PASSED     [16%]
tests/unit-test/repository/test_auth_repository.py::TestGetUserByEmail::test_get_user_by_email_found PASSED         [20%]
tests/unit-test/repository/test_auth_repository.py::TestGetUserByEmail::test_get_user_by_email_not_found PASSED     [25%]
tests/unit-test/repository/test_auth_repository.py::TestGetUserByEmail::test_get_user_by_email_inactive_user PASSED [29%]
tests/unit-test/repository/test_auth_repository.py::TestCreateToken::test_create_token_success PASSED               [33%]
tests/unit-test/repository/test_auth_repository.py::TestCreateToken::test_create_token_with_datetime_serialization PASSED [37%]
tests/unit-test/repository/test_auth_repository.py::TestGetToken::test_get_token_found PASSED                       [41%]
tests/unit-test/repository/test_auth_repository.py::TestGetToken::test_get_token_not_found PASSED                   [45%]
tests/unit-test/repository/test_auth_repository.py::TestGetTypeUser::test_get_type_user_found PASSED                [50%]
tests/unit-test/repository/test_auth_repository.py::TestGetTypeUser::test_get_type_user_not_found PASSED            [54%]
tests/unit-test/repository/test_auth_repository.py::TestGetTypeUser::test_get_type_user_admin PASSED                [58%]
tests/unit-test/repository/test_auth_repository.py::TestCreateTypeUser::test_create_type_user_success PASSED        [62%]
tests/unit-test/repository/test_auth_repository.py::TestCreateTypeUser::test_create_type_user_basic PASSED          [66%]
tests/unit-test/repository/test_auth_repository.py::TestAddEmailToTypeUser::test_add_email_to_existing_type_user PASSED [70%]
tests/unit-test/repository/test_auth_repository.py::TestAddEmailToTypeUser::test_add_email_to_type_user_when_type_not_exists PASSED [75%]
tests/unit-test/repository/test_auth_repository.py::TestAddEmailToTypeUser::test_add_duplicate_email_to_type_user PASSED [79%]
tests/unit-test/repository/test_auth_repository.py::TestAddEmailToTypeUser::test_add_multiple_emails_sequentially PASSED [83%]
tests/unit-test/repository/test_auth_repository.py::TestAddEmailToTypeUser::test_add_email_to_admin_type PASSED [87%]
tests/unit-test/repository/test_auth_repository.py::TestAddEmailToTypeUser::test_add_email_with_empty_emails_list PASSED [91%]

========================== 22 passed in X.XXs ==========================
```

## 🎯 Cobertura de Casos de Prueba

### AuthRepository.__init__()
- ✅ Inicialización correcta de tablas DynamoDB

### create_user()
- ✅ Crear usuario exitoso
- ✅ Diferentes tipos de usuario (basic, admin)
- ✅ Usuario con state=False

### get_user_by_email()
- ✅ Usuario encontrado
- ✅ Usuario no encontrado
- ✅ Usuario inactivo

### create_token() / get_token()
- ✅ Crear y obtener tokens
- ✅ Serialización de datetime
- ✅ Token no encontrado

### get_type_user()
- ✅ Tipo encontrado
- ✅ Tipo no encontrado
- ✅ Diferentes tipos (basic, admin)

### create_type_user()
- ✅ Crear nuevo tipo
- ✅ Primer email del tipo

### add_email_to_type_user()
- ✅ Agregar email a tipo existente
- ✅ Crear tipo si no existe
- ✅ No duplicar emails
- ✅ Agregar múltiples emails
- ✅ Lista vacía de emails

## 💡 Notas Importantes

1. **Mocks de DynamoDB**: Todas las operaciones de DynamoDB están mockeadas
2. **No se conecta a AWS**: Las pruebas son 100% unitarias y aisladas
3. **Verificación de Llamadas**: Se verifican los parámetros pasados a DynamoDB
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

### Las pruebas fallan con errores de boto3
```bash
# Verificar que boto3 esté instalado
pip list | grep boto3

# Si no está, instalarlo
pip install boto3
```

## 🔗 Documentación Relacionada

- Controller tests: `auth/tests/unit-test/controller/README.md`
- Service tests: `auth/tests/unit-test/service/README.md`
- Guía rápida: `auth/GUIA_RAPIDA_TESTS.md`
- Comandos pytest: `auth/COMANDOS_PYTEST.md`
