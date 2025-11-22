"""
Products Page
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging


class ProductsPage(BasePage):
    
    # Locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    PRODUCT_SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
    # Dynamic locators
    ADD_TO_CART_BUTTON_TEMPLATE = "//div[text()='{}']/ancestor::div[@class='inventory_item']//button"
    REMOVE_BUTTON_TEMPLATE = "//div[text()='{}']/ancestor::div[@class='inventory_item']//button[text()='Remove']"
    PRODUCT_NAME_TEMPLATE = "//div[text()='{}']"
    PRODUCT_PRICE_TEMPLATE = "//div[text()='{}']/ancestor::div[@class='inventory_item']//div[@class='inventory_item_price']"
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.logger = logging.getLogger(__name__)
    
    def is_products_page_loaded(self):

        return (self.is_element_visible(self.INVENTORY_CONTAINER) and 
                self.get_text(self.PAGE_TITLE) == "Products")
    
    def get_page_title(self):

        return self.get_text(self.PAGE_TITLE)
    
    def get_all_products(self):

        return self.find_elements(self.INVENTORY_ITEMS)
    
    def get_product_count(self):

        return len(self.get_all_products())
    
    def add_product_to_cart_by_name(self, product_name):

        add_button_locator = (By.XPATH, self.ADD_TO_CART_BUTTON_TEMPLATE.format(product_name))
        self.click(add_button_locator)
        self.logger.info(f"Added product to cart: {product_name}")
    
    def remove_product_from_cart_by_name(self, product_name):

        remove_button_locator = (By.XPATH, self.REMOVE_BUTTON_TEMPLATE.format(product_name))
        self.click(remove_button_locator)
        self.logger.info(f"Removed product from cart: {product_name}")
    
    def get_cart_item_count(self):

        if self.is_element_visible(self.SHOPPING_CART_BADGE, timeout=2):
            return int(self.get_text(self.SHOPPING_CART_BADGE))
        return 0
    
    def click_shopping_cart(self):
        self.click(self.SHOPPING_CART_LINK)
        self.logger.info("Clicked shopping cart")
    
    def get_product_price(self, product_name):

        price_locator = (By.XPATH, self.PRODUCT_PRICE_TEMPLATE.format(product_name))
        return self.get_text(price_locator)
    
    def is_product_displayed(self, product_name):

        product_locator = (By.XPATH, self.PRODUCT_NAME_TEMPLATE.format(product_name))
        return self.is_element_visible(product_locator, timeout=5)
    
    def logout(self):
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)
        self.logger.info("Logged out")
