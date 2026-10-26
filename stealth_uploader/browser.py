import os
import json
import logging
from typing import Optional
from playwright.sync_api import sync_playwright, BrowserContext, Page

logger = logging.getLogger("stealth_uploader.browser")

STEALTH_EVASION_SCRIPTS = """
// Overwrite the 'navigator.webdriver' property to fool bot detection
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});

// Mock Chrome runtime object
window.chrome = {
    runtime: {},
    loadTimes: function() {},
    csi: function() {},
    app: {}
};

// Mock standard plugins array
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
});

// Mock standard language settings
Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en', 'es']
});
"""

class ResilientBrowser:
    """Manages persistent browser contexts, cookies, and stealth fingerprint spoofing."""
    
    def __init__(self, user_data_dir: str = "./browser_session", headless: bool = False):
        self.user_data_dir = os.path.abspath(user_data_dir)
        self.headless = headless
        self._playwright = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    def start(self):
        os.makedirs(self.user_data_dir, exist_ok=True)
        self._playwright = sync_playwright().start()
        
        # Launch persistent context to preserve cookies and login tokens across executions
        self.context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars"
            ]
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        # Inject anti-detection evasions into all frames before any scripts execute
        self.context.add_init_script(STEALTH_EVASION_SCRIPTS)
        logger.info(f"Browser launched with persistent session at: {self.user_data_dir}")
        return self.page
        
    def save_storage_state(self, state_path: str = "./browser_session/state.json"):
        if self.context:
            self.context.storage_state(path=state_path)
            logger.info(f"Session cookies & local storage persisted to {state_path}")
            
    def close(self):
        if self.context:
            self.context.close()
        if self._playwright:
            self._playwright.stop()
        logger.info("Browser session cleanly closed.")
