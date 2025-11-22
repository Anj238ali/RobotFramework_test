"""
Test cases for login functionality
"""

import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
import logging


class TestLogin:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        self.login_page = LoginPage(driver, config)
        self.products_page = ProductsPage(driver, config)
        self.logger = logging.getLogger(__name__)
    
    @pytest.mark.login
    def test_successful_login(self):
        self.logger.info("Starting test: test_successful_login")
        
        assert self.login_page.is_login_page_loaded(), "Login page should be loaded"
        
        credentials = self.config['users']['standard_user']
        self.login_page.login(credentials['username'], credentials['password'])
        
        assert self.products_page.is_products_page_loaded(), "Products page should be loaded after successful login"
        
        assert self.products_page.get_page_title() == "Products", "Page title should be 'Products'"
        
        product_count = self.products_page.get_product_count()
        assert product_count > 0, f"Should display products, found {product_count}"
        
        self.logger.info("Test passed: test_successful_login")
    
    @pytest.mark.login
    def test_login_failed(self):

        self.logger.info("Starting test: test_login_failed")
        
        credentials = self.config['users']['locked_out_user']
        self.login_page.login(credentials['username'], credentials['password'])
        
        assert self.login_page.is_error_message_displayed(), "Error message should be displayed for locked user"
        
        error_text = self.login_page.get_error_message_text()
        assert "locked out" in error_text.lower(), f"Error message should mention locked out user: {error_text}"
        
        assert "inventory.html" not in self.driver.current_url, "User should remain on login page"
        
        self.logger.info("Test passed: test_login_failed")
    
    @pytest.mark.login
    def test_login_with_empty_credentials(self):
        self.logger.info("Starting test: test_login_with_empty_credentials")
        
        self.login_page.click_login_button()
        
        assert self.login_page.is_error_message_displayed(), "Error message should be displayed for empty credentials"
        
        # Verify error message content
        error_text = self.login_page.get_error_message_text()
        assert "username is required" in error_text.lower(), f"Error message should mention username required: {error_text}"
        
        self.logger.info("Test passed: test_login_with_empty_credentials")
