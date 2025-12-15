"""
cart_page.py - Page Object for Shopping Cart
URL: https://www.saucedemo.com/cart.html
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from typing import List


class CartPage(BasePage):
    """Page Object for Cart Page"""
    
    # =============== LOCATORS ===============
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CART_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    # =============== PAGE ACTIONS ===============
    
    def get_page_title_text(self) -> str:
        """Get the page title text"""
        return self.get_text(self.PAGE_TITLE)
    
    def get_cart_item_count(self) -> int:
        """Get number of items in cart"""
        return len(self.get_elements(self.CART_ITEMS))
    
    def get_cart_item_names(self) -> List[str]:
        """Get names of all items in cart"""
        names = self.get_elements(self.CART_ITEM_NAMES)
        return [name.text for name in names]
    
    def remove_first_item(self) -> None:
        """Remove the first item from cart"""
        buttons = self.get_elements(self.REMOVE_BUTTONS)
        if buttons:
            buttons[0].click()
    
    def remove_item_by_name(self, product_name: str) -> None:
        """Remove specific item from cart by name"""
        button_id = f"remove-{product_name.lower().replace(' ', '-')}"
        self.click((By.ID, button_id))
    
    def remove_all_items(self) -> None:
        """Remove all items from cart"""
        buttons = self.get_elements(self.REMOVE_BUTTONS)
        while buttons:
            buttons[0].click()
            buttons = self.get_elements(self.REMOVE_BUTTONS)
    
    def continue_shopping(self):
        """Click Continue Shopping button"""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)
    
    def proceed_to_checkout(self):
        """Click Checkout button"""
        self.click(self.CHECKOUT_BUTTON)
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
    
    # =============== VERIFICATIONS ===============
    
    def is_cart_page_displayed(self) -> bool:
        """Check if cart page is displayed"""
        return "cart" in self.get_current_url() and self.get_page_title_text() == "Your Cart"
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty"""
        return self.get_cart_item_count() == 0
    
    def is_product_in_cart(self, product_name: str) -> bool:
        """Check if specific product is in cart"""
        return product_name in self.get_cart_item_names()
