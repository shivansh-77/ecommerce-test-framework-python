"""
checkout_page.py - Page Object for Checkout process
Handles checkout step one, step two, and completion
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for Checkout Pages"""
    
    # =============== LOCATORS - Step One ===============
    PAGE_TITLE = (By.CLASS_NAME, "title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    # =============== LOCATORS - Step Two (Overview) ===============
    SUMMARY_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    
    # =============== LOCATORS - Complete ===============
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    # =============== STEP ONE ACTIONS ===============
    
    def enter_first_name(self, first_name: str) -> None:
        """Enter first name"""
        self.type_text(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name: str) -> None:
        """Enter last name"""
        self.type_text(self.LAST_NAME_INPUT, last_name)
    
    def enter_postal_code(self, postal_code: str) -> None:
        """Enter postal code"""
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
    
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill all checkout information fields"""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
    
    def click_continue(self) -> None:
        """Click Continue button"""
        self.click(self.CONTINUE_BUTTON)
    
    def click_cancel(self) -> None:
        """Click Cancel button"""
        self.click(self.CANCEL_BUTTON)
    
    def proceed_to_overview(self, first_name: str, last_name: str, postal_code: str) -> 'CheckoutPage':
        """Fill info and proceed to overview"""
        self.fill_checkout_info(first_name, last_name, postal_code)
        self.click_continue()
        return self
    
    # =============== STEP TWO ACTIONS ===============
    
    def get_subtotal(self) -> str:
        """Get subtotal amount"""
        return self.get_text(self.SUMMARY_SUBTOTAL)
    
    def get_tax(self) -> str:
        """Get tax amount"""
        return self.get_text(self.SUMMARY_TAX)
    
    def get_total(self) -> str:
        """Get total amount"""
        return self.get_text(self.SUMMARY_TOTAL)
    
    def click_finish(self) -> 'CheckoutPage':
        """Click Finish button"""
        self.click(self.FINISH_BUTTON)
        return self
    
    # =============== COMPLETE PAGE ACTIONS ===============
    
    def get_complete_header(self) -> str:
        """Get completion header text"""
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_complete_text(self) -> str:
        """Get completion message text"""
        return self.get_text(self.COMPLETE_TEXT)
    
    def click_back_home(self):
        """Click Back Home button"""
        self.click(self.BACK_HOME_BUTTON)
        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)
    
    # =============== VERIFICATIONS ===============
    
    def get_page_title_text(self) -> str:
        """Get page title text"""
        return self.get_text(self.PAGE_TITLE)
    
    def is_checkout_step_one_displayed(self) -> bool:
        """Check if checkout step one is displayed"""
        return "checkout-step-one" in self.get_current_url()
    
    def is_checkout_step_two_displayed(self) -> bool:
        """Check if checkout overview is displayed"""
        return "checkout-step-two" in self.get_current_url()
    
    def is_checkout_complete_displayed(self) -> bool:
        """Check if checkout complete page is displayed"""
        return "checkout-complete" in self.get_current_url()
    
    def is_order_successful(self) -> bool:
        """Check if order was successful"""
        return "Thank you for your order" in self.get_complete_header()
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_displayed(self.ERROR_MESSAGE)
    
    def get_error_message_text(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
