"""
products_page.py - Page Object for Products/Inventory page
URL: https://www.saucedemo.com/inventory.html
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
from typing import List


class ProductsPage(BasePage):
    """Page Object for Products Page"""
    
    # =============== LOCATORS ===============
    PAGE_TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    # =============== PAGE ACTIONS ===============
    
    def get_page_title_text(self) -> str:
        """Get the page title text"""
        return self.get_text(self.PAGE_TITLE)
    
    def get_product_count(self) -> int:
        """Get total number of products displayed"""
        return len(self.get_elements(self.PRODUCT_ITEMS))
    
    def add_first_product_to_cart(self) -> None:
        """Add the first product to cart"""
        buttons = self.get_elements(self.ADD_TO_CART_BUTTONS)
        if buttons:
            buttons[0].click()
    
    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """Add product to cart by its name"""
        button_id = f"add-to-cart-{product_name.lower().replace(' ', '-')}"
        self.click((By.ID, button_id))
    
    def remove_product_from_cart_by_name(self, product_name: str) -> None:
        """Remove product from cart by its name"""
        button_id = f"remove-{product_name.lower().replace(' ', '-')}"
        self.click((By.ID, button_id))
    
    def add_multiple_products_to_cart(self, count: int) -> None:
        """Add specified number of products to cart"""
        for i in range(count):
            buttons = self.get_elements(self.ADD_TO_CART_BUTTONS)
            if i < len(buttons):
                buttons[0].click()  # Always click first available button
    
    def go_to_cart(self):
        """Navigate to cart page"""
        self.click(self.CART_LINK)
        from pages.cart_page import CartPage
        return CartPage(self.driver)
    
    def sort_by_option(self, option_value: str) -> None:
        """Sort products by dropdown option value"""
        dropdown = self.wait.wait_for_element_clickable(self.SORT_DROPDOWN)
        select = Select(dropdown)
        select.select_by_value(option_value)
    
    def sort_by_price_low_to_high(self) -> None:
        """Sort products by price: low to high"""
        self.sort_by_option("lohi")
    
    def sort_by_price_high_to_low(self) -> None:
        """Sort products by price: high to low"""
        self.sort_by_option("hilo")
    
    def sort_by_name_a_to_z(self) -> None:
        """Sort products by name: A to Z"""
        self.sort_by_option("az")
    
    def sort_by_name_z_to_a(self) -> None:
        """Sort products by name: Z to A"""
        self.sort_by_option("za")
    
    def logout(self) -> None:
        """Logout from the application"""
        self.click(self.BURGER_MENU_BUTTON)
        self.wait.wait_for_element_clickable(self.LOGOUT_LINK)
        self.click(self.LOGOUT_LINK)
    
    # =============== VERIFICATIONS ===============
    
    def is_products_page_displayed(self) -> bool:
        """Check if products page is displayed"""
        return "inventory" in self.get_current_url() and self.get_page_title_text() == "Products"
    
    def get_cart_badge_count(self) -> int:
        """Get the number shown on cart badge"""
        try:
            return int(self.get_text(self.CART_BADGE))
        except:
            return 0
    
    def is_cart_badge_displayed(self) -> bool:
        """Check if cart badge is displayed"""
        return self.is_element_present(self.CART_BADGE)
    
    def get_first_product_name(self) -> str:
        """Get the name of the first product"""
        names = self.get_elements(self.PRODUCT_NAMES)
        return names[0].text if names else ""
    
    def get_first_product_price(self) -> str:
        """Get the price of the first product"""
        prices = self.get_elements(self.PRODUCT_PRICES)
        return prices[0].text if prices else ""
    
    def get_all_product_names(self) -> List[str]:
        """Get all product names"""
        names = self.get_elements(self.PRODUCT_NAMES)
        return [name.text for name in names]
    
    def get_all_product_prices(self) -> List[str]:
        """Get all product prices"""
        prices = self.get_elements(self.PRODUCT_PRICES)
        return [price.text for price in prices]
