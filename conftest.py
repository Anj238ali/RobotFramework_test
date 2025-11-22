"""
Pytest Configuration and Fixtures
"""

import pytest
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.webdriver_manager import WebDriverManager
from utils.screenshot_helper import ScreenshotHelper


def load_config():
    config_path = Path(__file__).parent / 'config' / 'config.json'
    with open(config_path, 'r') as f:
        return json.load(f)


@pytest.fixture(scope='session')
def config():
    return load_config()


@pytest.fixture(scope='function')
def driver(config):
    # Initialize WebDriver
    driver_manager = WebDriverManager(config)
    driver = driver_manager.get_driver()
    
    # Maximize window
    driver.maximize_window()
    
    # Navigate to base URL
    driver.get(config['base_url'])
    
    yield driver
    
    # Teardown - quit driver
    driver.quit()


@pytest.fixture(scope='function')
def screenshot_helper(driver, config):
    return ScreenshotHelper(driver, config)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' and report.failed:
        # Get the driver fixture
        driver = item.funcargs.get('driver')
        if driver:
            # Create screenshots directory if it doesn't exist
            screenshot_dir = Path(__file__).parent / 'reports' / 'screenshots'
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate screenshot filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = screenshot_dir / screenshot_name
            
            # Capture screenshot
            try:
                driver.save_screenshot(str(screenshot_path))
                print(f"\nScreenshot saved: {screenshot_path}")
                
                # Attach screenshot to HTML report
                if hasattr(report, 'extra'):
                    report.extra.append(pytest.html.extras.image(str(screenshot_path)))
            except Exception as e:
                print(f"\n Failed to capture screenshot: {e}")


def pytest_configure(config):
    config._metadata = {
        'Project': 'SauceDemo Automation',
        'Framework': 'Selenium + Pytest',
        'Browser': 'Chrome',
        'Platform': os.name
    }
