"""
login_page.py - Page Object for Login functionality
URL: https://www.saucedemo.com
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for Login Page"""
    
    # =============== LOCATORS ===============
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    # =============== PAGE ACTIONS ===============
    
    def enter_username(self, username: str) -> None:
        """Enter username in the username field"""
        self.type_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """Enter password in the password field"""
        self.type_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> None:
        """Click the login button"""
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str):
        """
        Complete login action - combines all steps
        Returns ProductsPage on success
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
        # Import here to avoid circular import
        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)
    
    def login_expecting_failure(self, username: str, password: str) -> 'LoginPage':
        """Login expecting failure (for negative tests)"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    # =============== VERIFICATIONS ===============
    
    def is_login_page_displayed(self) -> bool:
        """Check if login page is displayed"""
        return self.is_displayed(self.LOGIN_LOGO) and self.is_displayed(self.LOGIN_BUTTON)
    
    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_displayed(self.ERROR_MESSAGE)
    
    def get_error_message_text(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
