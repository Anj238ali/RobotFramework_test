"""
Form Submission Tests
"""

import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.test_data_generator import TestDataGenerator
import logging


class TestFormSubmission:

    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.login_page = LoginPage(driver, config)
        self.products_page = ProductsPage(driver, config)
        self.cart_page = CartPage(driver, config)
        self.test_data = TestDataGenerator()
        self.logger = logging.getLogger(__name__)
        
        # Login before each test
        self.login_page.login_with_valid_credentials()
        assert self.products_page.is_products_page_loaded(), "Login should be successful"

    def test_product_add_and_checkout(self):
        self.logger.info("Starting test: test_product_add_and_checkout")
        
        # Add product to cart
        product_name = "Sauce Labs Backpack"
        self.products_page.add_product_to_cart_by_name(product_name)
        
        # Navigate to cart
        self.products_page.click_shopping_cart()
        assert self.cart_page.is_cart_page_loaded(), "Cart page should be loaded"
        
        # Generate test data using Faker
        checkout_data = self.test_data.generate_checkout_data()
        
        self.logger.info(f"Using test data: {checkout_data}")
        
        # Complete checkout
        is_complete = self.cart_page.complete_checkout(
            checkout_data['first_name'],
            checkout_data['last_name'],
            checkout_data['postal_code']
        )
        
        # Verify order is complete
        assert is_complete, "Checkout should be successful"
        
        # Verify confirmation message
        confirmation_header = self.cart_page.get_confirmation_header()
        assert "Thank you" in confirmation_header or "Complete" in confirmation_header, \
            f"Confirmation header should show success: {confirmation_header}"
        
        # Verify URL contains checkout-complete
        assert "checkout-complete" in self.driver.current_url, "URL should indicate checkout complete"
        
        self.logger.info("Test passed: test_product_add_and_checkout")

    def test_product_add_and_checkout_fail(self):
        self.logger.info("Starting test: test_product_add_and_checkout_fail")

        # Add product to cart
        product_name = "Sauce Labs INVALID ITEM"
        self.products_page.add_product_to_cart_by_name(product_name)

        # Navigate to cart
        self.products_page.click_shopping_cart()
        assert self.cart_page.is_cart_page_loaded(), "Cart page should be loaded"

        # Generate test data using Faker
        checkout_data = self.test_data.generate_checkout_data()

        self.logger.info(f"Using test data: {checkout_data}")

        # Complete checkout
        is_complete = self.cart_page.complete_checkout(
            checkout_data['first_name'],
            checkout_data['last_name'],
            checkout_data['postal_code']
        )

        # Verify order is complete
        assert is_complete, "Checkout should be successful"

        # Verify confirmation message
        confirmation_header = self.cart_page.get_confirmation_header()
        assert "Thank you" in confirmation_header or "Complete" in confirmation_header, \
            f"Confirmation header should show success: {confirmation_header}"

        # Verify URL contains checkout-complete
        assert "checkout-complete" in self.driver.current_url, "URL should indicate checkout complete"

        self.logger.info("Test passed: test_product_add_and_checkout_fail")
