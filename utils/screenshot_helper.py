"""
Screenshot Helper
"""

import os
from datetime import datetime
from pathlib import Path
from PIL import Image
import logging


class ScreenshotHelper:

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.screenshots_enabled = config.get('screenshots', {}).get('enabled', True)
        self.screenshots_path = config.get('screenshots', {}).get('path', 'reports/screenshots')
        self.logger = logging.getLogger(__name__)
        
        # Create screenshots directory if it doesn't exist
        self._create_screenshots_directory()
    
    def _create_screenshots_directory(self):
        if self.screenshots_enabled:
            Path(self.screenshots_path).mkdir(parents=True, exist_ok=True)
    
    def capture_screenshot(self, name=None):
        if not self.screenshots_enabled:
            self.logger.warning("Screenshots are disabled in config")
            return None
        
        try:
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if name:
                filename = f"{name}_{timestamp}.png"
            else:
                filename = f"screenshot_{timestamp}.png"
            
            filepath = os.path.join(self.screenshots_path, filename)
            
            # Capture screenshot
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            
            return filepath
        
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {e}")
            return None
    
    def capture_element_screenshot(self, element, name=None):
        if not self.screenshots_enabled:
            self.logger.warning("Screenshots are disabled in config")
            return None
        
        try:
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if name:
                filename = f"{name}_element_{timestamp}.png"
            else:
                filename = f"element_{timestamp}.png"
            
            filepath = os.path.join(self.screenshots_path, filename)
            
            # Capture element screenshot
            element.screenshot(filepath)
            self.logger.info(f"Element screenshot saved: {filepath}")
            
            return filepath
        
        except Exception as e:
            self.logger.error(f"Failed to capture element screenshot: {e}")
            return None
    
    def capture_full_page_screenshot(self, name=None):
        if not self.screenshots_enabled:
            self.logger.warning("Screenshots are disabled in config")
            return None
        
        try:
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if name:
                filename = f"{name}_fullpage_{timestamp}.png"
            else:
                filename = f"fullpage_{timestamp}.png"
            
            filepath = os.path.join(self.screenshots_path, filename)
            
            # Get page dimensions
            original_size = self.driver.get_window_size()
            required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
            required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
            
            # Resize window to capture full page
            self.driver.set_window_size(required_width, required_height)
            
            # Capture screenshot
            self.driver.save_screenshot(filepath)
            
            # Restore original window size
            self.driver.set_window_size(original_size['width'], original_size['height'])
            
            self.logger.info(f"Full page screenshot saved: {filepath}")
            
            return filepath
        
        except Exception as e:
            self.logger.error(f"Failed to capture full page screenshot: {e}")
            # Restore window size on error
            try:
                self.driver.set_window_size(original_size['width'], original_size['height'])
            except:
                pass
            return None
