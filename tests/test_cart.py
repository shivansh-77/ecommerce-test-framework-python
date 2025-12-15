"""
test_cart.py - Test cases for Shopping Cart functionality
Covers cart operations, item management, and navigation
"""

import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.config_reader import config


@pytest.mark.cart
class TestCart:
    """Test class for Cart functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Login before each test"""
        login_page = LoginPage(driver)
        self.products_page = login_page.login(
            config.valid_username,
            config.valid_password
        )
    
    @pytest.mark.smoke
    def test_empty_cart_display(self, driver):
        """Verify empty cart page display"""
        cart_page = self.products_page.go_to_cart()
        
        assert cart_page.is_cart_page_displayed(), \
            "Cart page should be displayed"
        assert cart_page.get_page_title_text() == "Your Cart", \
            "Page title should be 'Your Cart'"
        assert cart_page.is_cart_empty(), \
            "Cart should be empty initially"
    
    @pytest.mark.smoke
    def test_cart_with_products(self, driver):
        """Verify cart displays added products"""
        # Add products
        self.products_page.add_product_to_cart_by_name("sauce-labs-backpack")
        self.products_page.add_product_to_cart_by_name("sauce-labs-bike-light")
        
        # Go to cart
        cart_page = self.products_page.go_to_cart()
        
        assert cart_page.get_cart_item_count() == 2, \
            "Cart should have 2 items"
        assert cart_page.is_product_in_cart("Sauce Labs Backpack"), \
            "Sauce Labs Backpack should be in cart"
        assert cart_page.is_product_in_cart("Sauce Labs Bike Light"), \
            "Sauce Labs Bike Light should be in cart"
    
    @pytest.mark.regression
    def test_remove_item_from_cart(self, driver):
        """Verify removing item from cart"""
        # Add products
        self.products_page.add_product_to_cart_by_name("sauce-labs-backpack")
        self.products_page.add_product_to_cart_by_name("sauce-labs-bike-light")
        
        # Go to cart and remove one item
        cart_page = self.products_page.go_to_cart()
        cart_page.remove_item_by_name("sauce-labs-backpack")
        
        assert cart_page.get_cart_item_count() == 1, \
            "Cart should have 1 item after removal"
        assert not cart_page.is_product_in_cart("Sauce Labs Backpack"), \
            "Sauce Labs Backpack should be removed from cart"
        assert cart_page.is_product_in_cart("Sauce Labs Bike Light"), \
            "Sauce Labs Bike Light should still be in cart"
    
    @pytest.mark.regression
    def test_remove_all_items_from_cart(self, driver):
        """Verify removing all items from cart"""
        # Add products
        self.products_page.add_multiple_products_to_cart(3)
        
        # Go to cart and remove all
        cart_page = self.products_page.go_to_cart()
        cart_page.remove_all_items()
        
        assert cart_page.is_cart_empty(), \
            "Cart should be empty after removing all items"
    
    @pytest.mark.regression
    def test_continue_shopping_navigation(self, driver):
        """Verify Continue Shopping button navigates back"""
        self.products_page.add_first_product_to_cart()
        cart_page = self.products_page.go_to_cart()
        
        returned_products_page = cart_page.continue_shopping()
        
        assert returned_products_page.is_products_page_displayed(), \
            "User should be navigated back to Products page"
        assert returned_products_page.get_cart_badge_count() == 1, \
            "Cart should still have 1 item after returning"
    
    @pytest.mark.regression
    def test_cart_persistence(self, driver):
        """Verify cart persists items after navigation"""
        # Add product and go to cart
        self.products_page.add_product_to_cart_by_name("sauce-labs-backpack")
        cart_page = self.products_page.go_to_cart()
        
        # Navigate back and add more
        returned_page = cart_page.continue_shopping()
        returned_page.add_product_to_cart_by_name("sauce-labs-bike-light")
        
        # Go back to cart
        updated_cart = returned_page.go_to_cart()
        
        assert updated_cart.get_cart_item_count() == 2, \
            "Cart should persist items and have 2 total"
    
    @pytest.mark.regression
    def test_cart_icon_updates(self, driver):
        """Verify cart icon updates after adding products"""
        assert not self.products_page.is_cart_badge_displayed(), \
            "Cart badge should not be visible initially"
        
        self.products_page.add_first_product_to_cart()
        assert self.products_page.get_cart_badge_count() == 1
        
        self.products_page.add_multiple_products_to_cart(2)
        assert self.products_page.get_cart_badge_count() == 3, \
            "Cart badge should update to show 3 items"
