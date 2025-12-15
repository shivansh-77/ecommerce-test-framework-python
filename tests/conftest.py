"""
conftest.py - Pytest fixtures and configuration
Contains setup/teardown fixtures for all tests
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_reader import config
from pages.login_page import LoginPage


@pytest.fixture(scope="function")
def driver():
    """
    Fixture to initialize and quit WebDriver
    Runs before and after each test function
    """
    browser = config.browser
    headless = config.headless
    
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        # ============ DISABLE PASSWORD BREACH ALERTS ============
        options.add_argument("--disable-features=PasswordLeakDetection")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Disable password manager and save password prompts
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)
        # =========================================================
        
        # Fix for webdriver-manager issue - get correct executable path
        driver_path = ChromeDriverManager().install()
        # Ensure we get the actual chromedriver.exe, not THIRD_PARTY_NOTICES
        if "THIRD_PARTY" in driver_path:
            driver_path = driver_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe")
        
        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        driver.maximize_window()
    
    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
        driver.maximize_window()
    
    else:
        raise ValueError(f"Browser '{browser}' not supported!")
    
    # Set implicit wait
    driver.implicitly_wait(config.implicit_wait)
    
    # Navigate to base URL
    driver.get(config.base_url)
    
    yield driver
    
    # Teardown - quit browser
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Fixture that provides a logged-in driver
    Use this for tests that need to start from logged-in state
    """
    login_page = LoginPage(driver)
    login_page.login(config.valid_username, config.valid_password)
    return driver


@pytest.fixture(scope="function")
def login_page(driver):
    """Fixture to get LoginPage object"""
    return LoginPage(driver)


# ============ Pytest Hooks ============

def pytest_html_report_title(report):
    """Set custom title for HTML report"""
    report.title = "E-commerce Test Automation Report"


def pytest_configure(config):
    """Create reports directory if it doesn't exist"""
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)