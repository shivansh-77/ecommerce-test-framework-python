"""
Pages package - Contains all Page Object classes
"""

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

__all__ = ['BasePage', 'LoginPage', 'ProductsPage', 'CartPage', 'CheckoutPage']
