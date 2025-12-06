"""
Shared test configuration and fixtures for frontend tests
"""
import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the frontend application"""
    # If running in Docker on app-network, use service name
    # Otherwise use host.docker.internal or localhost
    if os.getenv("DOCKER_ENV") == "true":
        # Check if we can use service name (when on same network)
        docker_base_url = os.getenv("BASE_URL")
        if docker_base_url and "frontend" in docker_base_url:
            return docker_base_url
        return "http://host.docker.internal:3000"
    return os.getenv("BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="function")
def driver():
    """Create and configure Chrome/Chromium WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for CI/CD
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    # Check if running in Docker (Chromium is installed in /usr/bin/chromium)
    if os.path.exists("/usr/bin/chromium"):
        # Use Chromium in Docker
        chrome_options.binary_location = "/usr/bin/chromium"
        # Use system chromedriver
        service = Service("/usr/bin/chromedriver")
    elif os.path.exists("/usr/bin/google-chrome"):
        # Fallback: Chrome if available
        chrome_options.binary_location = "/usr/bin/google-chrome"
        service = Service(ChromeDriverManager().install())
    else:
        # Running locally, use webdriver-manager to download Chrome/Chromium
        service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="function")
def wait(driver):
    """WebDriverWait instance with default timeout"""
    return WebDriverWait(driver, 20)  # Increased timeout for more reliability


@pytest.fixture(scope="function")
def clean_local_storage(driver):
    """Clean localStorage before each test"""
    # Only clear localStorage if we're on a valid page (not data: URL)
    try:
        current_url = driver.current_url
        if current_url and not current_url.startswith("data:"):
            driver.execute_script("window.localStorage.clear();")
    except Exception:
        # If we can't access localStorage, that's okay - we'll clear it after navigating
        pass
    yield
    # Clean up after test
    try:
        current_url = driver.current_url
        if current_url and not current_url.startswith("data:"):
            driver.execute_script("window.localStorage.clear();")
    except Exception:
        # Ignore errors when cleaning up
        pass


@pytest.fixture
def unique_email():
    """Generate a unique email for testing"""
    import random
    import string
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@unal.edu.co"


@pytest.fixture
def test_password():
    """Standard test password"""
    return "testpass123"


def wait_for_page_load(driver, timeout=10):
    """Wait for page to fully load"""
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    time.sleep(0.5)  # Small delay for dynamic content
