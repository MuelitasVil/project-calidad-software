"""
Sistema de Pruebas de Autenticación - ORGSECURE
Prueba de Login de Usuario Administrador

Requisitos Funcionales Validados:
- RF1.1: El sistema debe permitir el inicio de sesión mediante una página de login
- RF1.2: El login debe permitir el acceso tanto a usuarios normales como al usuario administrador
- RF1.4: El administrador debe acceder con una única cuenta especial de administración

Caso de Prueba: Login exitoso de administrador y redirección a home
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración del navegador
options = Options()
# Descomentar las siguientes líneas si quieres ejecutar en modo headless (sin ventana)
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Maximizar ventana para mejor visualización
driver.maximize_window()

print("=" * 80)
print("INICIANDO PRUEBA DE AUTENTICACIÓN - ORGSECURE")
print("=" * 80)

try:
    # Paso 1: Navegar a la página de login
    print("\n[TEST] Paso 1: Navegando a http://localhost:3000/login.html")
    driver.get("http://localhost:3000/login.html")
    time.sleep(2)  # Esperar a que cargue la página
    
    print(f"✓ URL actual: {driver.current_url}")
    assert "login.html" in driver.current_url, "No se cargó la página de login correctamente"
    print("✓ Página de login cargada exitosamente")
    
    # Paso 2: Localizar campos de entrada
    print("\n[TEST] Paso 2: Localizando campos de formulario...")
    
    # Buscar el campo de username (ID puede ser 'username' o 'email')
    try:
        username_field = driver.find_element(By.ID, "username")
        print("✓ Campo de usuario encontrado (ID: username)")
    except:
        username_field = driver.find_element(By.NAME, "username")
        print("✓ Campo de usuario encontrado (NAME: username)")
    
    # Buscar el campo de password
    password_field = driver.find_element(By.ID, "password")
    print("✓ Campo de contraseña encontrado")
    
    # Buscar el botón de login
    try:
        login_button = driver.find_element(By.ID, "SignIn")
        print("✓ Botón de login encontrado (ID: SignIn)")
    except:
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        print("✓ Botón de login encontrado (CSS Selector)")
    
    # Paso 3: Ingresar credenciales del administrador
    print("\n[TEST] Paso 3: Ingresando credenciales de administrador...")
    username_field.clear()
    username_field.send_keys("admin@example.com")
    print("✓ Usuario ingresado: admin@example.com")
    
    password_field.clear()
    password_field.send_keys("qwerty123")
    print("✓ Contraseña ingresada: ********")
    
    time.sleep(1)  # Pausa para visualización
    
    # Paso 4: Click en el botón de login
    print("\n[TEST] Paso 4: Haciendo click en el botón de login...")
    login_button.click()
    print("✓ Click ejecutado")
    
    # Paso 5: Esperar redirección y validar
    print("\n[TEST] Paso 5: Esperando redirección a home.html...")
    
    # Esperar hasta 10 segundos a que la URL cambie
    WebDriverWait(driver, 10).until(
        EC.url_contains("home.html")
    )
    
    time.sleep(2)  # Pausa adicional para asegurar carga completa
    
    current_url = driver.current_url
    print(f"✓ URL actual después del login: {current_url}")
    
    # Validación 1: Verificar redirección a home.html
    assert "home.html" in current_url, f"ERROR: No se redirigió a home.html. URL actual: {current_url}"
    print("✓ VALIDACIÓN 1 EXITOSA: Redirección a home.html confirmada")
    
    # Paso 6: Validar elementos del home
    print("\n[TEST] Paso 6: Validando elementos de la página home...")
    
    # Esperar a que el body esté presente
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # Obtener el texto del body
    body_text = driver.find_element(By.TAG_NAME, "body").text
    
    # Validación 2: Verificar que se muestra contenido del home
    # Buscar elementos característicos del home de admin
    admin_indicators = [
        "Gestión de Usuarios",
        "Bienvenido",
        "ORGSECURE",
        "admin"
    ]
    
    found_indicator = False
    for indicator in admin_indicators:
        if indicator.lower() in body_text.lower():
            print(f"✓ Elemento encontrado en la página: '{indicator}'")
            found_indicator = True
            break
    
    assert found_indicator, "ERROR: No se encontraron elementos característicos del home"
    print("✓ VALIDACIÓN 2 EXITOSA: Contenido del home cargado correctamente")
    
    # Validación 3: Verificar que el título de la página es correcto
    page_title = driver.title
    print(f"\n✓ Título de la página: {page_title}")
    assert page_title != "", "ERROR: El título de la página está vacío"
    print("✓ VALIDACIÓN 3 EXITOSA: Título de página válido")
    
    # Validación 4: Verificar que existe el navbar o header
    try:
        navbar = driver.find_element(By.TAG_NAME, "nav")
        print("✓ VALIDACIÓN 4 EXITOSA: Navbar encontrado en la página")
    except:
        print("⚠ ADVERTENCIA: No se encontró elemento nav, pero la prueba continúa")
    
    # Captura de pantalla como evidencia
    screenshot_path = "/home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/login-system-tests/login_success_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"\n✓ Screenshot guardado en: {screenshot_path}")
    
    # RESULTADO FINAL
    print("\n" + "=" * 80)
    print("✓✓✓ TEST PASSED ✓✓✓")
    print("=" * 80)
    print("Requisitos Funcionales Validados:")
    print("  ✓ RF1.1: Inicio de sesión mediante página de login")
    print("  ✓ RF1.2: Acceso de usuario administrador")
    print("  ✓ RF1.4: Cuenta especial de administración funcional")
    print("\nValidaciones Exitosas:")
    print("  1. Login con credenciales de administrador")
    print("  2. Redirección correcta a home.html")
    print("  3. Carga de contenido del dashboard")
    print("  4. Título de página válido")
    print("=" * 80)

except AssertionError as e:
    print("\n" + "=" * 80)
    print("✗✗✗ TEST FAILED ✗✗✗")
    print("=" * 80)
    print(f"Error de validación: {e}")
    print(f"URL actual: {driver.current_url}")
    
    # Captura de pantalla del error
    error_screenshot = "/home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/login-system-tests/login_error_screenshot.png"
    driver.save_screenshot(error_screenshot)
    print(f"Screenshot del error guardado en: {error_screenshot}")
    print("=" * 80)

except Exception as e:
    print("\n" + "=" * 80)
    print("✗✗✗ TEST ERROR ✗✗✗")
    print("=" * 80)
    print(f"Error inesperado: {type(e).__name__}")
    print(f"Detalle: {e}")
    print(f"URL actual: {driver.current_url}")
    
    # Captura de pantalla del error
    error_screenshot = "/home/totallyti/Documents/academy/UNAL/Calidad_de_Software/project-calidad-software/login-system-tests/login_exception_screenshot.png"
    driver.save_screenshot(error_screenshot)
    print(f"Screenshot del error guardado en: {error_screenshot}")
    print("=" * 80)

finally:
    print("\n[TEST] Cerrando navegador...")
    time.sleep(3)  # Pausa para ver el resultado antes de cerrar
    driver.quit()
    print("✓ Navegador cerrado")
    print("\nFin de la prueba\n")
