"""
Unit tests for login form functionality
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.unit
class TestGuestLoginForm:
    """Test login form elements and basic interactions for guest users"""
    
    def test_login_form_exists(self, driver, base_url, wait):
        """Test that login form is present on the page"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "loginForm")))
        
        login_form = driver.find_element(By.ID, "loginForm")
        assert login_form is not None
    
    def test_login_form_has_username_field(self, driver, base_url, wait):
        """Test that username input field exists"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "username")))
        
        username_field = driver.find_element(By.ID, "username")
        assert username_field is not None
        assert username_field.get_attribute("type") == "text"
    
    def test_login_form_has_password_field(self, driver, base_url, wait):
        """Test that password input field exists"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "password")))
        
        password_field = driver.find_element(By.ID, "password")
        assert password_field is not None
        assert password_field.get_attribute("type") == "password"
    
    def test_login_form_has_submit_button(self, driver, base_url, wait):
        """Test that submit button exists"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "SignIn")))
        
        submit_button = driver.find_element(By.ID, "SignIn")
        assert submit_button is not None
        assert submit_button.tag_name == "button"
    
    def test_can_fill_login_form(self, driver, base_url, wait):
        """Test that we can fill in the login form fields"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "username")))
        
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        
        username_field.send_keys("test@example.com")
        password_field.send_keys("testpassword")
        
        assert username_field.get_attribute("value") == "test@example.com"
        assert password_field.get_attribute("value") == "testpassword"

