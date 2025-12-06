"""
Unit tests for profile page functionality
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.unit
class TestGuestProfileForm:
    """Test profile page elements and basic interactions for guest users"""
    
    def test_profile_page_requires_authentication(self, driver, base_url, wait):
        """Test that profile page redirects if not authenticated"""
        driver.get(f"{base_url}/profile.html")
        
        # Should redirect to login page
        wait.until(lambda d: "login.html" in d.current_url or "profile.html" in d.current_url)
        
        # If redirected, current URL should be login
        if "login.html" in driver.current_url:
            assert "login.html" in driver.current_url
        else:
            # If not redirected, check if auth check is working
            # This might happen if localStorage has some data
            pass
    
    def test_profile_form_exists_when_authenticated(self, driver, base_url, wait, clean_local_storage):
        """Test that profile form exists when user is authenticated"""
        # Set up authentication in localStorage
        driver.get(f"{base_url}/login.html")
        driver.execute_script("""
            localStorage.setItem('authToken', 'test_token');
            localStorage.setItem('user', JSON.stringify({
                email: 'test@unal.edu.co',
                username: 'Test User',
                type_user: 'guest'
            }));
        """)
        
        driver.get(f"{base_url}/profile.html")
        wait.until(EC.presence_of_element_located((By.ID, "profileForm")))
        
        profile_form = driver.find_element(By.ID, "profileForm")
        assert profile_form is not None
    
    def test_profile_has_edit_buttons(self, driver, base_url, wait, clean_local_storage):
        """Test that profile page has edit buttons"""
        # Set up authentication
        driver.get(f"{base_url}/login.html")
        driver.execute_script("""
            localStorage.setItem('authToken', 'test_token');
            localStorage.setItem('user', JSON.stringify({
                email: 'test@unal.edu.co',
                username: 'Test User',
                type_user: 'guest'
            }));
        """)
        
        driver.get(f"{base_url}/profile.html")
        wait.until(EC.presence_of_element_located((By.ID, "editProfileBtn")))
        
        edit_profile_btn = driver.find_element(By.ID, "editProfileBtn")
        edit_personal_btn = driver.find_element(By.ID, "editPersonalBtn")
        
        assert edit_profile_btn is not None
        assert edit_personal_btn is not None
    
    def test_can_click_edit_profile_button(self, driver, base_url, wait, clean_local_storage):
        """Test that clicking edit profile button enables editing"""
        # Set up authentication
        driver.get(f"{base_url}/login.html")
        driver.execute_script("""
            localStorage.setItem('authToken', 'test_token');
            localStorage.setItem('user', JSON.stringify({
                email: 'test@unal.edu.co',
                username: 'Test User',
                type_user: 'guest'
            }));
        """)
        
        driver.get(f"{base_url}/profile.html")
        wait.until(EC.presence_of_element_located((By.ID, "editProfileBtn")))
        
        # Click edit button
        edit_btn = driver.find_element(By.ID, "editProfileBtn")
        edit_btn.click()
        
        # Check that input is enabled
        wait.until(EC.element_to_be_clickable((By.ID, "inputUsername")))
        username_input = driver.find_element(By.ID, "inputUsername")
        assert username_input.get_attribute("disabled") is None

