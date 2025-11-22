"""
Login Page Object
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging


class LoginPage(BasePage):

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, "button.error-button")
    
    def __init__(self, driver, config):
        super().__init__(driver, config)
        self.logger = logging.getLogger(__name__)
    
    def enter_username(self, username):
        self.send_keys(self.USERNAME_INPUT, username)
        self.logger.info(f"Entered username: {username}")
    
    def enter_password(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)
        self.logger.info("Entered password")
    
    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)
        self.logger.info("Clicked login button")
    
    def login(self, username, password):

        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        self.logger.info(f"Login attempted with username: {username}")
    
    def login_with_valid_credentials(self):

        credentials = self.config['users']['standard_user']
        self.login(credentials['username'], credentials['password'])
    
    def is_error_message_displayed(self):

        return self.is_element_visible(self.ERROR_MESSAGE, timeout=5)
    
    def get_error_message_text(self):

        if self.is_error_message_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def is_login_page_loaded(self):

        return (self.is_element_visible(self.USERNAME_INPUT) and 
                self.is_element_visible(self.PASSWORD_INPUT) and 
                self.is_element_visible(self.LOGIN_BUTTON))
