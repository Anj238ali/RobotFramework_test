"""
Cart Page Object
Contains locators and methods for shopping cart page
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging


class CartPage(BasePage):
    """Page Object for SauceDemo Shopping Cart Page"""
    
    # Locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[class*='cart_button']")
    
    # Checkout form locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    
    # Confirmation locators
    CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")
    CONFIRMATION_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    # Error locator
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    
    def __init__(self, driver, config):

        super().__init__(driver, config)
        self.logger = logging.getLogger(__name__)
    
    def is_cart_page_loaded(self):

        return (self.wait_for_url_contains("cart.html") and 
                self.get_text(self.PAGE_TITLE) == "Your Cart")
    
    def get_cart_items_count(self):
        if self.is_element_present(self.CART_ITEMS):
            return len(self.find_elements(self.CART_ITEMS))
        return 0
    
    def get_cart_item_names(self):
        items = self.find_elements(self.CART_ITEM_NAMES)
        return [item.text for item in items]
    
    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.logger.info("Clicked checkout button")
    
    def click_continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.logger.info("Clicked continue shopping")
    
    def fill_checkout_form(self, first_name, last_name, postal_code):

        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.POSTAL_CODE_INPUT, postal_code)
        self.logger.info("Filled checkout form")
    
    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)
        self.logger.info("Clicked continue on checkout form")
    
    def click_finish(self):
        self.click(self.FINISH_BUTTON)
        self.logger.info("Clicked finish to complete order")
    
    def is_order_complete(self):
        return self.is_element_visible(self.CONFIRMATION_HEADER)
    
    def get_confirmation_header(self):
        return self.get_text(self.CONFIRMATION_HEADER)
    
    def get_confirmation_message(self):
        return self.get_text(self.CONFIRMATION_TEXT)
    
    def click_back_home(self):
        self.click(self.BACK_HOME_BUTTON)
        self.logger.info("Clicked back to home")
    
    def complete_checkout(self, first_name, last_name, postal_code):

        self.click_checkout()
        self.fill_checkout_form(first_name, last_name, postal_code)
        self.click_continue()
        self.click_finish()
        return self.is_order_complete()
    
    def get_error_message(self):

        if self.is_element_visible(self.ERROR_MESSAGE, timeout=2):
            return self.get_text(self.ERROR_MESSAGE)
        return None
