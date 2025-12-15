"""
base_page.py - Parent class for all Page Objects
Contains common methods used across all pages
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple, List
from utils.wait_helper import WaitHelper


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitHelper(driver)
    
    def click(self, locator: Tuple[str, str]) -> None:
        """Click on element after waiting for it to be clickable"""
        self.wait.wait_for_element_clickable(locator).click()
    
    def type_text(self, locator: Tuple[str, str], text: str) -> None:
        """Clear field and type text"""
        element = self.wait.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Get text from element"""
        return self.wait.wait_for_element_visible(locator).text
    
    def is_displayed(self, locator: Tuple[str, str]) -> bool:
        """Check if element is displayed"""
        try:
            return self.wait.wait_for_element_visible(locator).is_displayed()
        except:
            return False
    
    def get_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Get list of elements"""
        return self.driver.find_elements(*locator)
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get page title"""
        return self.driver.title
    
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Check if element exists in DOM"""
        elements = self.driver.find_elements(*locator)
        return len(elements) > 0
