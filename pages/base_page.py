"""
Base Page Class
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging


class BasePage:

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.timeout = config.get('explicit_wait', 20)
        self.logger = logging.getLogger(__name__)
    
    def find_element(self, locator, timeout=None):
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator, timeout=None):
        timeout = timeout or self.timeout
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            raise
    
    def click(self, locator, timeout=None):
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            raise
    
    def send_keys(self, locator, text, timeout=None):
        timeout = timeout or self.timeout
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Entered text in element: {locator}")
    
    def get_text(self, locator, timeout=None):

        element = self.find_element(locator, timeout)
        return element.text
    
    def is_element_visible(self, locator, timeout=None):
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):

        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_url_contains(self, url_fragment, timeout=None):

        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(url_fragment)
            )
            return True
        except TimeoutException:
            self.logger.error(f"URL does not contain: {url_fragment}")
            return False
    
    def get_current_url(self):
        return self.driver.current_url
    
    def get_page_title(self):
        return self.driver.title
    
    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def get_attribute(self, locator, attribute_name, timeout=None):
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute_name)
