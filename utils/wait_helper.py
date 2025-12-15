"""
wait_helper.py - Provides reusable explicit wait methods
Reduces flaky tests by properly waiting for elements
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple
from utils.config_reader import config


class WaitHelper:
    """Helper class for explicit waits"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.timeout = config.explicit_wait
        self.wait = WebDriverWait(driver, self.timeout)
    
    def wait_for_element_visible(self, locator: Tuple[str, str]) -> WebElement:
        """Wait for element to be visible and return it"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator: Tuple[str, str]) -> WebElement:
        """Wait for element to be clickable and return it"""
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_element_present(self, locator: Tuple[str, str]) -> WebElement:
        """Wait for element to be present in DOM"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_elements_visible(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Wait for all elements to be visible"""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))
    
    def wait_for_element_invisible(self, locator: Tuple[str, str]) -> bool:
        """Wait for element to become invisible"""
        return self.wait.until(EC.invisibility_of_element_located(locator))
    
    def wait_for_text_present(self, locator: Tuple[str, str], text: str) -> bool:
        """Wait for specific text to be present in element"""
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))
    
    def wait_for_url_contains(self, url_part: str) -> bool:
        """Wait for URL to contain specific text"""
        return self.wait.until(EC.url_contains(url_part))
    
    def wait_for_url_to_be(self, url: str) -> bool:
        """Wait for URL to be exactly as specified"""
        return self.wait.until(EC.url_to_be(url))
