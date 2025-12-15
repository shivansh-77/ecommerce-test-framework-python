"""
test_products.py - Test cases for Products/Inventory page
Covers product display, sorting, and add to cart
"""

import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config_reader import config


@pytest.mark.products
class TestProducts:
    """Test class for Products functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Login before each test"""
        login_page = LoginPage(driver)
        self.products_page = login_page.login(
            config.valid_username,
            config.valid_password
        )
    
    @pytest.mark.smoke
    def test_products_page_display(self, driver):
        """Verify products page displays correctly after login"""
        assert self.products_page.is_products_page_displayed(), \
            "Products page should be displayed after login"
        assert self.products_page.get_page_title_text() == "Products", \
            "Page title should be 'Products'"
    
    @pytest.mark.smoke
    def test_products_are_displayed(self, driver):
        """Verify products are displayed on the page"""
        product_count = self.products_page.get_product_count()
        
        assert product_count > 0, \
            "At least one product should be displayed"
        assert product_count == 6, \
            "SauceDemo should display 6 products"
    
    @pytest.mark.smoke
    def test_add_single_product_to_cart(self, driver):
        """Verify adding single product to cart"""
        self.products_page.add_first_product_to_cart()
        
        assert self.products_page.is_cart_badge_displayed(), \
            "Cart badge should appear after adding product"
        assert self.products_page.get_cart_badge_count() == 1, \
            "Cart badge should show count of 1"
    
    @pytest.mark.regression
    def test_add_multiple_products_to_cart(self, driver):
        """Verify adding multiple products to cart"""
        self.products_page.add_multiple_products_to_cart(3)
        
        assert self.products_page.get_cart_badge_count() == 3, \
            "Cart badge should show count of 3 after adding 3 products"
    
    @pytest.mark.regression
    def test_add_product_by_name(self, driver):
        """Verify adding product by name"""
        self.products_page.add_product_to_cart_by_name("sauce-labs-backpack")
        
        assert self.products_page.get_cart_badge_count() == 1, \
            "Cart should have 1 item after adding Sauce Labs Backpack"
    
    @pytest.mark.regression
    def test_remove_product_from_products_page(self, driver):
        """Verify removing product from cart on products page"""
        product_name = "sauce-labs-backpack"
        
        # Add product
        self.products_page.add_product_to_cart_by_name(product_name)
        assert self.products_page.get_cart_badge_count() == 1
        
        # Remove product
        self.products_page.remove_product_from_cart_by_name(product_name)
        assert not self.products_page.is_cart_badge_displayed(), \
            "Cart badge should not be displayed after removing product"
    
    @pytest.mark.regression
    def test_sort_by_name_a_to_z(self, driver):
        """Verify sorting products by name A to Z"""
        self.products_page.sort_by_name_a_to_z()
        first_product = self.products_page.get_first_product_name()
        
        assert first_product == "Sauce Labs Backpack", \
            "Products should be sorted A to Z"
    
    @pytest.mark.regression
    def test_sort_by_name_z_to_a(self, driver):
        """Verify sorting products by name Z to A"""
        self.products_page.sort_by_name_z_to_a()
        first_product = self.products_page.get_first_product_name()
        
        assert "Test.allTheThings" in first_product, \
            "Products should be sorted Z to A"
    
    @pytest.mark.regression
    def test_sort_by_price_low_to_high(self, driver):
        """Verify sorting products by price low to high"""
        self.products_page.sort_by_price_low_to_high()
        first_price = self.products_page.get_first_product_price()
        
        assert first_price == "$7.99", \
            "Lowest priced item ($7.99) should be first"
    
    @pytest.mark.regression
    def test_sort_by_price_high_to_low(self, driver):
        """Verify sorting products by price high to low"""
        self.products_page.sort_by_price_high_to_low()
        first_price = self.products_page.get_first_product_price()
        
        assert first_price == "$49.99", \
            "Highest priced item ($49.99) should be first"
    
    @pytest.mark.regression
    def test_logout(self, driver):
        """Verify user can logout successfully"""
        self.products_page.logout()
        
        login_page = LoginPage(driver)
        assert login_page.is_login_page_displayed(), \
            "User should be redirected to login page after logout"
