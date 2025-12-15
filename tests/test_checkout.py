"""
test_checkout.py - Test cases for complete Checkout flow
Covers form validation, order completion, and E2E scenarios
"""

import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.config_reader import config


@pytest.mark.checkout
class TestCheckout:
    """Test class for Checkout functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Login and add product before each test"""
        login_page = LoginPage(driver)
        self.products_page = login_page.login(
            config.valid_username,
            config.valid_password
        )
        # Add a product for checkout tests
        self.products_page.add_product_to_cart_by_name("sauce-labs-backpack")
    
    @pytest.mark.smoke
    def test_checkout_page_display(self, driver):
        """Verify checkout page displays correctly"""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        
        assert checkout_page.is_checkout_step_one_displayed(), \
            "Checkout Step One page should be displayed"
    
    @pytest.mark.smoke
    def test_valid_checkout_info(self, driver):
        """Verify checkout with valid information"""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        
        checkout_page.proceed_to_overview("Shivansh", "Bajpai", "208001")
        
        assert checkout_page.is_checkout_step_two_displayed(), \
            "User should proceed to checkout overview"
    
    @pytest.mark.regression
    def test_checkout_empty_first_name(self, driver):
        """Verify checkout fails with empty first name"""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        
        checkout_page.fill_checkout_info("", "Bajpai", "208001")
        checkout_page.click_continue()
        
        assert checkout_page.is_error_displayed(), \
            "Error should be displayed for empty first name"
        assert "First Name is required" in checkout_page.get_error_message_text(), \
            "Error message should indicate first name is required"
    
    @pytest.mark.regression
    def test_checkout_empty_last_name(self, driver):
        """Verify checkout fails with empty last name"""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        
        checkout_page.fill_checkout_info("Shivansh", "", "208001")
        checkout_page.click_continue()
        
        assert checkout_page.is_error_displayed(), \
            "Error should be displayed for empty last name"
        assert "Last Name is required" in checkout_page.get_error_message_text(), \
            "Error message should indicate last name is required"
    
    @pytest.mark.regression
    def test_checkout_empty_postal_code(self, driver):
        """Verify checkout fails with empty postal code"""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        
        checkout_page.fill_checkout_info("Shivansh", "Bajpai", "")
        checkout_page.click_continue()
        
        assert checkout_page.is_error_displayed(), \
            "Error should be displayed for empty postal code"
        assert "Postal Code is required" in checkout_page.get_error_message_text(), \
            "Error message should indicate postal code is required"
    
    @pytest.mark.regression
    def test_checkout_overview_summary(self, driver):
        """Verify checkout overview displays order summary"""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.proceed_to_overview("Shivansh", "Bajpai", "208001")
        
        subtotal = checkout_page.get_subtotal()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()
        
        assert "$" in subtotal, "Subtotal should display price"
        assert "$" in tax, "Tax should display amount"
        assert "$" in total, "Total should display final amount"
    
    @pytest.mark.smoke
    def test_complete_order_flow(self, driver):
        """Verify complete order flow - End to End"""
        # Navigate through checkout
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.proceed_to_overview("Shivansh", "Bajpai", "208001")
        checkout_page.click_finish()
        
        # Verify order completion
        assert checkout_page.is_checkout_complete_displayed(), \
            "Checkout complete page should be displayed"
        assert checkout_page.is_order_successful(), \
            "Order should be successful with thank you message"
        assert "Thank you" in checkout_page.get_complete_header(), \
            "Complete header should contain 'Thank you'"
    
    @pytest.mark.regression
    def test_back_home_after_order(self, driver):
        """Verify Back Home button after order completion"""
        # Complete order
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.proceed_to_overview("Shivansh", "Bajpai", "208001")
        checkout_page.click_finish()
        
        # Go back home
        returned_page = checkout_page.click_back_home()
        
        assert returned_page.is_products_page_displayed(), \
            "User should be redirected to Products page"
        assert not returned_page.is_cart_badge_displayed(), \
            "Cart should be empty after completing order"
    
    @pytest.mark.regression
    def test_cancel_checkout(self, driver):
        """Verify cancel button returns to cart"""
        cart_page = self.products_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        
        checkout_page.click_cancel()
        
        returned_cart = CartPage(driver)
        assert returned_cart.is_cart_page_displayed(), \
            "Cancel should return user to cart page"
        assert returned_cart.get_cart_item_count() == 1, \
            "Cart should still have the product"
    
    @pytest.mark.smoke
    def test_full_e2e_flow(self, driver):
        """Full E2E: Login -> Add Products -> Checkout -> Complete"""
        # Add more products (one already added in setup)
        self.products_page.add_product_to_cart_by_name("sauce-labs-bike-light")
        self.products_page.add_product_to_cart_by_name("sauce-labs-bolt-t-shirt")
        
        assert self.products_page.get_cart_badge_count() == 3, \
            "Cart should have 3 items"
        
        # Go to cart
        cart_page = self.products_page.go_to_cart()
        assert cart_page.get_cart_item_count() == 3
        
        # Checkout
        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.proceed_to_overview("Shivansh", "Bajpai", "208001")
        
        # Verify total includes all items
        total = checkout_page.get_total()
        assert "$" in total, "Total should show combined price"
        
        # Complete order
        checkout_page.click_finish()
        assert checkout_page.is_order_successful(), \
            "Order should complete successfully"
        
        # Return home and verify cart is empty
        final_page = checkout_page.click_back_home()
        assert not final_page.is_cart_badge_displayed(), \
            "Cart should be empty after order"
