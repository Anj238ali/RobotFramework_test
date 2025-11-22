"""
WebDriver Manager
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import logging


class WebDriverManager:

    def __init__(self, config):

        self.config = config
        self.browser = config.get('browser', 'chrome').lower()
        self.headless = config.get('headless', False)
        self.implicit_wait = config.get('implicit_wait', 10)
        self.logger = logging.getLogger(__name__)

    def get_chrome_options(self):

        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')

        # Additional options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--ignore-certificate-errors')

        # Disable password save popup and notifications
        options.add_argument('--disable-save-password-bubble')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        # Disable password leak/breach detection
        options.add_argument('--disable-features=PasswordLeakDetection')

        # Use incognito mode (no saved passwords)
        options.add_argument('--incognito')

        # Preferences
        prefs = {
            'credentials_enable_service': False,
            'profile.password_manager_enabled': False,
            'profile.default_content_setting_values.notifications': 2,
            'autofill.profile_enabled': False,
            'profile.default_content_settings.popups': 0,
            'profile.password_manager_leak_detection': False,
            'password_manager_leak_detection': False,
            'safebrowsing.enabled': False,  # Disables breach warnings
            'safebrowsing.enhanced': False,
        }
        options.add_experimental_option('prefs', prefs)

        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        return options

    def get_driver(self):

        driver = None
        driver_path = r'C:\chromedriver\chromedriver.exe'

        try:
            if self.browser == 'chrome':
                service = ChromeService(executable_path=driver_path)
                driver = webdriver.Chrome(service=service, options=self.get_chrome_options())
                self.logger.info("Chrome WebDriver initialized")
            
            else:
                raise ValueError(f"Unsupported browser: {self.browser}")
            
            driver.implicitly_wait(self.implicit_wait)
            
            return driver
        
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise
