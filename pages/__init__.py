"""
Package initialization for pages module
"""

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

__all__ = ['BasePage', 'LoginPage', 'ProductsPage', 'CartPage']
