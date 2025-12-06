"""
Unit tests for registration form functionality
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.unit
class TestGuestRegisterForm:
    """Test registration form elements and basic interactions for guest users"""
    
    def test_register_tab_exists(self, driver, base_url, wait):
        """Test that register tab button exists"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "tabRegister")))
        
        register_tab = driver.find_element(By.ID, "tabRegister")
        assert register_tab is not None
    
    def test_can_switch_to_register_tab(self, driver, base_url, wait):
        """Test that clicking register tab shows registration form"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "tabRegister")))
        
        register_tab = driver.find_element(By.ID, "tabRegister")
        register_tab.click()
        
        wait.until(EC.presence_of_element_located((By.ID, "registerForm")))
        register_form = driver.find_element(By.ID, "registerForm")
        assert register_form is not None
    
    def test_register_form_has_required_fields(self, driver, base_url, wait):
        """Test that registration form has all required fields"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "tabRegister")))
        
        # Switch to register tab
        driver.find_element(By.ID, "tabRegister").click()
        wait.until(EC.presence_of_element_located((By.ID, "registerForm")))
        
        # Check required fields
        email_field = driver.find_element(By.ID, "reg_email_unal")
        password_field = driver.find_element(By.ID, "reg_password")
        password_confirm_field = driver.find_element(By.ID, "reg_password_confirm")
        
        assert email_field is not None
        assert password_field is not None
        assert password_confirm_field is not None
        
        # Check they are required
        assert email_field.get_attribute("required") is not None
        assert password_field.get_attribute("required") is not None
        assert password_confirm_field.get_attribute("required") is not None
    
    def test_register_form_has_optional_fields(self, driver, base_url, wait):
        """Test that registration form has optional personal information fields"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "tabRegister")))
        
        # Switch to register tab
        driver.find_element(By.ID, "tabRegister").click()
        wait.until(EC.presence_of_element_located((By.ID, "registerForm")))
        
        # Check optional fields exist
        document_field = driver.find_element(By.ID, "reg_document")
        name_field = driver.find_element(By.ID, "reg_name")
        lastname_field = driver.find_element(By.ID, "reg_lastname")
        full_name_field = driver.find_element(By.ID, "reg_full_name")
        gender_field = driver.find_element(By.ID, "reg_gender")
        birth_date_field = driver.find_element(By.ID, "reg_birth_date")
        
        assert document_field is not None
        assert name_field is not None
        assert lastname_field is not None
        assert full_name_field is not None
        assert gender_field is not None
        assert birth_date_field is not None
    
    def test_can_fill_register_form(self, driver, base_url, wait):
        """Test that we can fill in the registration form fields"""
        driver.get(f"{base_url}/login.html")
        wait.until(EC.presence_of_element_located((By.ID, "tabRegister")))
        
        # Switch to register tab
        driver.find_element(By.ID, "tabRegister").click()
        wait.until(EC.presence_of_element_located((By.ID, "reg_email_unal")))
        
        # Fill form
        driver.find_element(By.ID, "reg_email_unal").send_keys("test@unal.edu.co")
        driver.find_element(By.ID, "reg_password").send_keys("testpass123")
        driver.find_element(By.ID, "reg_password_confirm").send_keys("testpass123")
        driver.find_element(By.ID, "reg_name").send_keys("Test")
        driver.find_element(By.ID, "reg_lastname").send_keys("User")
        
        # Verify values
        assert driver.find_element(By.ID, "reg_email_unal").get_attribute("value") == "test@unal.edu.co"
        assert driver.find_element(By.ID, "reg_name").get_attribute("value") == "Test"
        assert driver.find_element(By.ID, "reg_lastname").get_attribute("value") == "User"

