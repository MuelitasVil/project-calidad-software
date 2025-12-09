# Sistema de Pruebas de Autenticación - ORGSECURE

Pruebas funcionales automatizadas para validar el sistema de autenticación del proyecto.

## Requisitos Funcionales Validados

- **RF1.1**: El sistema debe permitir el inicio de sesión mediante una página de login
- **RF1.2**: El login debe permitir el acceso tanto a usuarios normales como al usuario administrador
- **RF1.4**: El administrador debe acceder con una única cuenta especial de administración

## Prerrequisitos

1. **Google Chrome instalado**
2. **Python 3.8+** instalado
3. **Servicios del proyecto ejecutándose**:
   - Frontend en `http://localhost:3000`
   - Auth service en `http://localhost:8000`
   - Users service en `http://localhost:8001`

## Instalación

### 1. Crear y activar entorno virtual

```bash
cd login-system-tests
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate  # En Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar la Prueba Manualmente

### Paso 1: Asegurarse que los servicios estén corriendo

Desde la raíz del proyecto:

```bash
cd /home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software
docker compose up -d
```

Verificar que todos los servicios estén levantados:

```bash
docker compose ps
```

Deberías ver:
- `frontend-service` en puerto 3000
- `auth-service` en puerto 8000
- `users-service` en puerto 8001

### Paso 2: Activar el entorno virtual (si no está activado)

```bash
cd login-system-tests
source venv/bin/activate
```

### Paso 3: Ejecutar la prueba

```bash
python test_login.py
```

## Salida Esperada

Si la prueba es **EXITOSA**, verás:

```
================================================================================
INICIANDO PRUEBA DE AUTENTICACIÓN - ORGSECURE
================================================================================

[TEST] Paso 1: Navegando a http://localhost:3000/login.html
✓ URL actual: http://localhost:3000/login.html
✓ Página de login cargada exitosamente

[TEST] Paso 2: Localizando campos de formulario...
✓ Campo de usuario encontrado (ID: username)
✓ Campo de contraseña encontrado
✓ Botón de login encontrado (ID: SignIn)

[TEST] Paso 3: Ingresando credenciales de administrador...
✓ Usuario ingresado: admin@example.com
✓ Contraseña ingresada: ********

[TEST] Paso 4: Haciendo click en el botón de login...
✓ Click ejecutado

[TEST] Paso 5: Esperando redirección a home.html...
✓ URL actual después del login: http://localhost:3000/home.html
✓ VALIDACIÓN 1 EXITOSA: Redirección a home.html confirmada

[TEST] Paso 6: Validando elementos de la página home...
✓ Elemento encontrado en la página: 'Gestión de Usuarios'
✓ VALIDACIÓN 2 EXITOSA: Contenido del home cargado correctamente

✓ Título de la página: ORGSECURE - Home
✓ VALIDACIÓN 3 EXITOSA: Título de página válido
✓ VALIDACIÓN 4 EXITOSA: Navbar encontrado en la página

✓ Screenshot guardado en: .../login_success_screenshot.png

================================================================================
✓✓✓ TEST PASSED ✓✓✓
================================================================================
Requisitos Funcionales Validados:
  ✓ RF1.1: Inicio de sesión mediante página de login
  ✓ RF1.2: Acceso de usuario administrador
  ✓ RF1.4: Cuenta especial de administración funcional

Validaciones Exitosas:
  1. Login con credenciales de administrador
  2. Redirección correcta a home.html
  3. Carga de contenido del dashboard
  4. Título de página válido
================================================================================

[TEST] Cerrando navegador...
✓ Navegador cerrado

Fin de la prueba
```

## Credenciales de Prueba

- **Usuario**: `admin@example.com`
- **Contraseña**: `qwert123`

## Evidencias

La prueba genera automáticamente un screenshot como evidencia:

- **Éxito**: `login_success_screenshot.png`
- **Error**: `login_error_screenshot.png` o `login_exception_screenshot.png`

## Modo Headless

Si quieres ejecutar la prueba sin abrir una ventana del navegador, edita `test_login.py` y descomenta estas líneas:

```python
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
```

## Solución de Problemas

### Error: "No se cargó la página de login"

**Causa**: Los servicios no están corriendo.

**Solución**:
```bash
cd ..
docker compose up -d
```

### Error: "No se redirigió a home.html"

**Causas posibles**:
1. Credenciales incorrectas
2. Error en el servicio de autenticación
3. Base de datos sin el usuario admin

**Solución**: Verificar logs de los servicios:
```bash
docker logs auth-service
docker logs users-service
```

### Error: "ChromeDriver no encontrado"

**Causa**: webdriver-manager no pudo descargar ChromeDriver.

**Solución**:
```bash
pip install --upgrade webdriver-manager
```

### Error: "selenium module not found"

**Causa**: El entorno virtual no está activado.

**Solución**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Desactivar Entorno Virtual

Cuando termines de ejecutar las pruebas:

```bash
deactivate
```

## Estructura de Archivos

```
login-system-tests/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias Python
├── test_login.py                     # Script de prueba principal
├── venv/                             # Entorno virtual (creado localmente)
├── login_success_screenshot.png      # Evidencia de éxito (generado)
└── login_error_screenshot.png        # Evidencia de error (generado)
```

## Notas Adicionales

- La prueba espera hasta 10 segundos para que se complete la redirección
- Se toman screenshots automáticos como evidencia
- La ventana del navegador permanece abierta 3 segundos después de la prueba para visualizar el resultado
- Los errores de lint en VSCode son normales antes de instalar las dependencias
