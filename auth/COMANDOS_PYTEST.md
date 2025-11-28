# 📝 Comandos pytest - Guía Completa

## 🎯 Comandos Básicos

### Ejecutar Todas las Pruebas Unitarias
```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/auth
source venv/bin/activate
pytest tests/unit-test/ -v
```

### Ejecutar Pruebas del Controller
```bash
pytest tests/unit-test/controller/test_auth_controller.py -v
```

### Ejecutar Pruebas del Service
```bash
pytest tests/unit-test/service/test_auth_service.py -v
```

## 🔍 Comandos por Clase de Pruebas

### Controller - Por Endpoint

#### Pruebas de Register
```bash
pytest tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint -v
```

#### Pruebas de Login
```bash
pytest tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint -v
```

#### Pruebas de ValidateToken
```bash
pytest tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint -v
```

### Service - Por Método

#### Pruebas de register()
```bash
pytest tests/unit-test/service/test_auth_service.py::TestRegisterMethod -v
```

#### Pruebas de login()
```bash
pytest tests/unit-test/service/test_auth_service.py::TestLoginMethod -v
```

#### Pruebas de verify_token()
```bash
pytest tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod -v
```

## 🎯 Comandos para Pruebas Individuales

### Controller - Pruebas Específicas

```bash
# Register exitoso
pytest tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_success -v

# Usuario ya existe
pytest tests/unit-test/controller/test_auth_controller.py::TestRegisterEndpoint::test_register_user_already_exists -v

# Login exitoso
pytest tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_success -v

# Credenciales inválidas
pytest tests/unit-test/controller/test_auth_controller.py::TestLoginEndpoint::test_login_invalid_credentials -v

# Token válido
pytest tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_valid -v

# Token expirado
pytest tests/unit-test/controller/test_auth_controller.py::TestValidateTokenEndpoint::test_validate_token_expired -v
```

### Service - Pruebas Específicas

```bash
# Register exitoso
pytest tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_success_new_user -v

# Usuario ya existe
pytest tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_user_already_exists -v

# Hasheo de password
pytest tests/unit-test/service/test_auth_service.py::TestRegisterMethod::test_register_password_hashing -v

# Login exitoso
pytest tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_success_valid_credentials -v

# Password incorrecta
pytest tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_wrong_password -v

# Usuario inactivo
pytest tests/unit-test/service/test_auth_service.py::TestLoginMethod::test_login_user_inactive -v

# Token válido
pytest tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_valid -v

# Token expirado
pytest tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_expired -v

# Firma inválida
pytest tests/unit-test/service/test_auth_service.py::TestVerifyTokenMethod::test_verify_token_invalid_signature -v
```

## 📊 Comandos con Opciones Avanzadas

### Verbose (Salida Detallada)
```bash
pytest tests/unit-test/ -v
```

### Mostrar Print Statements
```bash
pytest tests/unit-test/ -v -s
```

### Detener en Primer Error
```bash
pytest tests/unit-test/ -x
```

### Ejecutar Solo Tests que Fallaron
```bash
pytest tests/unit-test/ --lf
```

### Ver Traceback Completo
```bash
pytest tests/unit-test/ -v --tb=long
```

### Traceback Corto
```bash
pytest tests/unit-test/ -v --tb=short
```

### Sin Traceback
```bash
pytest tests/unit-test/ -v --tb=no
```

### Ejecutar Tests en Paralelo (requiere pytest-xdist)
```bash
pip install pytest-xdist
pytest tests/unit-test/ -n auto
```

## 📈 Comandos de Cobertura

### Cobertura Básica
```bash
pip install pytest-cov
pytest tests/unit-test/ --cov
```

### Cobertura del Controller
```bash
pytest tests/unit-test/controller/ --cov=controller --cov-report=term-missing
```

### Cobertura del Service
```bash
pytest tests/unit-test/service/ --cov=service.crud.auth_service --cov-report=term-missing
```

### Cobertura Completa con Reporte HTML
```bash
pytest tests/unit-test/ --cov=controller --cov=service --cov-report=html
```

### Ver Reporte HTML
```bash
# Después de ejecutar con --cov-report=html
xdg-open htmlcov/index.html  # Linux
# open htmlcov/index.html     # MacOS
# start htmlcov/index.html    # Windows
```

### Cobertura Solo de Líneas Faltantes
```bash
pytest tests/unit-test/ --cov=controller --cov=service --cov-report=term-missing
```

### Cobertura con Porcentaje Mínimo
```bash
pytest tests/unit-test/ --cov=controller --cov=service --cov-fail-under=80
```

## 🔎 Comandos de Búsqueda y Filtrado

### Buscar Tests por Nombre
```bash
# Buscar tests que contengan "register"
pytest tests/unit-test/ -k "register" -v

# Buscar tests que contengan "login"
pytest tests/unit-test/ -k "login" -v

# Buscar tests que contengan "token"
pytest tests/unit-test/ -k "token" -v

# Buscar tests que NO contengan "expired"
pytest tests/unit-test/ -k "not expired" -v

# Combinar condiciones (login Y success)
pytest tests/unit-test/ -k "login and success" -v

# Condición OR (register O login)
pytest tests/unit-test/ -k "register or login" -v
```

### Listar Tests Sin Ejecutar
```bash
pytest tests/unit-test/ --collect-only
```

### Contar Tests
```bash
pytest tests/unit-test/ --collect-only -q
```

## 🧪 Comandos de Debugging

### Ejecutar con PDB (Debugger)
```bash
pytest tests/unit-test/ --pdb
```

### PDB Solo en Fallas
```bash
pytest tests/unit-test/ --pdb --maxfail=1
```

### Ejecutar con Warnings Como Errores
```bash
pytest tests/unit-test/ -W error
```

### Mostrar Warnings
```bash
pytest tests/unit-test/ -v -W default
```

### Ignorar Warnings
```bash
pytest tests/unit-test/ -v --disable-warnings
```

## 📝 Comandos de Reporte

### Reporte Resumido
```bash
pytest tests/unit-test/ -q
```

### Reporte con Duración de Tests
```bash
pytest tests/unit-test/ -v --durations=10
```

### Reporte con Duración de Todos los Tests
```bash
pytest tests/unit-test/ -v --durations=0
```

### Reporte JUnit XML
```bash
pytest tests/unit-test/ --junit-xml=report.xml
```

### Reporte JSON (requiere pytest-json-report)
```bash
pip install pytest-json-report
pytest tests/unit-test/ --json-report --json-report-file=report.json
```

## 🎨 Comandos de Visualización

### Colores Deshabilitados
```bash
pytest tests/unit-test/ --color=no
```

### Forzar Colores
```bash
pytest tests/unit-test/ --color=yes
```

### Formato de Salida Personalizado
```bash
pytest tests/unit-test/ -v --tb=short --no-header
```

## 🔧 Comandos de Configuración

### Ver Configuración de pytest
```bash
pytest --version
```

### Ver Plugins Instalados
```bash
pytest --version --verbose
```

### Ver Variables de Configuración
```bash
pytest --markers
```

### Ver Fixtures Disponibles
```bash
pytest --fixtures
```

### Ver Fixtures de Un Archivo Específico
```bash
pytest tests/unit-test/controller/test_auth_controller.py --fixtures
```

## 🚀 Comandos Combinados Útiles

### Verbose + Sin Warnings + Traceback Corto
```bash
pytest tests/unit-test/ -v --disable-warnings --tb=short
```

### Detener en Primer Error + PDB
```bash
pytest tests/unit-test/ -x --pdb
```

### Cobertura + HTML + Solo Líneas Faltantes
```bash
pytest tests/unit-test/ --cov=controller --cov=service --cov-report=html --cov-report=term-missing
```

### Paralelo + Cobertura + Verbose
```bash
pytest tests/unit-test/ -n auto --cov --cov-report=term -v
```

### Solo Tests de Register (Service y Controller)
```bash
pytest tests/unit-test/ -k "register" -v --tb=short
```

## 💡 Alias Útiles (Agregar a ~/.bashrc o ~/.zshrc)

```bash
# Agregar estos alias a tu shell
alias ptest='pytest tests/unit-test/ -v'
alias ptest-controller='pytest tests/unit-test/controller/ -v'
alias ptest-service='pytest tests/unit-test/service/ -v'
alias ptest-cov='pytest tests/unit-test/ --cov=controller --cov=service --cov-report=html'
alias ptest-fast='pytest tests/unit-test/ -x --tb=short'
alias ptest-debug='pytest tests/unit-test/ -v -s --pdb'
```

## 📚 Recursos Adicionales

- Documentación pytest: https://docs.pytest.org/
- pytest-cov: https://pytest-cov.readthedocs.io/
- pytest-xdist: https://pytest-xdist.readthedocs.io/

## 🎯 Comandos Recomendados para Este Proyecto

### Desarrollo Diario
```bash
# Ejecutar todas las pruebas con salida limpia
pytest tests/unit-test/ -v --tb=short

# Ejecutar con cobertura
pytest tests/unit-test/ --cov --cov-report=term-missing
```

### Pre-Commit
```bash
# Ejecutar todas las pruebas sin warnings
pytest tests/unit-test/ -v --disable-warnings --tb=short

# Con cobertura mínima del 80%
pytest tests/unit-test/ --cov --cov-fail-under=80
```

### CI/CD
```bash
# Generar reporte JUnit + Cobertura HTML
pytest tests/unit-test/ -v --junit-xml=junit.xml --cov --cov-report=html --cov-report=xml
```

### Debugging
```bash
# Con prints y PDB
pytest tests/unit-test/ -v -s --pdb -x
```
