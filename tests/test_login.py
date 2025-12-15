"""
test_login.py - Test cases for Login functionality
Covers positive, negative, and edge cases
"""

import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config_reader import config


@pytest.mark.login
class TestLogin:
    """Test class for Login functionality"""
    
    @pytest.mark.smoke
    def test_login_page_display(self, driver, login_page):
        """Verify login page is displayed correctly"""
        assert login_page.is_login_page_displayed(), \
            "Login page should be displayed with logo and login button"
    
    @pytest.mark.smoke
    def test_valid_login(self, driver, login_page):
        """Verify successful login with valid credentials"""
        products_page = login_page.login(
            config.valid_username, 
            config.valid_password
        )
        
        assert products_page.is_products_page_displayed(), \
            "User should be redirected to Products page after successful login"
        assert products_page.get_page_title_text() == "Products", \
            "Page title should be 'Products'"
    
    @pytest.mark.regression
    def test_invalid_username(self, driver, login_page):
        """Verify login fails with invalid username"""
        login_page.login_expecting_failure(
            config.invalid_username, 
            config.valid_password
        )
        
        assert login_page.is_error_message_displayed(), \
            "Error message should be displayed for invalid username"
        assert "Username and password do not match" in login_page.get_error_message_text(), \
            "Error message should indicate credentials mismatch"
    
    @pytest.mark.regression
    def test_invalid_password(self, driver, login_page):
        """Verify login fails with invalid password"""
        login_page.login_expecting_failure(
            config.valid_username, 
            config.invalid_password
        )
        
        assert login_page.is_error_message_displayed(), \
            "Error message should be displayed for invalid password"
    
    @pytest.mark.regression
    def test_empty_username(self, driver, login_page):
        """Verify login fails with empty username"""
        login_page.login_expecting_failure("", config.valid_password)
        
        assert login_page.is_error_message_displayed(), \
            "Error message should be displayed for empty username"
        assert "Username is required" in login_page.get_error_message_text(), \
            "Error message should indicate username is required"
    
    @pytest.mark.regression
    def test_empty_password(self, driver, login_page):
        """Verify login fails with empty password"""
        login_page.login_expecting_failure(config.valid_username, "")
        
        assert login_page.is_error_message_displayed(), \
            "Error message should be displayed for empty password"
        assert "Password is required" in login_page.get_error_message_text(), \
            "Error message should indicate password is required"
    
    @pytest.mark.regression
    def test_empty_credentials(self, driver, login_page):
        """Verify login fails with empty credentials"""
        login_page.login_expecting_failure("", "")
        
        assert login_page.is_error_message_displayed(), \
            "Error message should be displayed for empty credentials"
    
    @pytest.mark.regression
    def test_locked_user_login(self, driver, login_page):
        """Verify locked user cannot login"""
        login_page.login_expecting_failure(
            config.locked_username, 
            config.valid_password
        )
        
        assert login_page.is_error_message_displayed(), \
            "Error message should be displayed for locked user"
        assert "locked out" in login_page.get_error_message_text(), \
            "Error message should indicate user is locked out"
