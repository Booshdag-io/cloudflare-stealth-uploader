import time
import logging
from typing import Optional

logger = logging.getLogger("stealth_uploader.cloudflare")

class CloudflareHandler:
    """Detects and resolves Cloudflare Turnstile, waiting rooms, and interstitial security checks."""
    
    CHALLENGE_SELECTORS = [
        "iframe[src*='challenges.cloudflare.com']",
        "#cf-turnstile-wrapper",
        "div.cf-turnstile",
        "div#turnstile-wrapper",
        "div#challenge-running",
        "div#challenge-stage"
    ]
    
    @classmethod
    def is_challenge_present(cls, page) -> bool:
        """Checks if any Cloudflare verification iframe or challenge stage is active on page."""
        for selector in cls.CHALLENGE_SELECTORS:
            try:
                el = page.query_selector(selector)
                if el and el.is_visible():
                    return True
            except Exception:
                pass
        # Check document title for Cloudflare interstitial
        try:
            title = page.title().lower()
            if "just a moment" in title or "attention required" in title:
                return True
        except Exception:
            pass
        return False

    @classmethod
    def wait_for_clearance(cls, page, timeout_sec: int = 60, human_fallback: bool = True) -> bool:
        """
        Polls until the challenge disappears.
        If challenge persists and human_fallback is enabled, prompts the operator on console.
        """
        if not cls.is_challenge_present(page):
            return True
            
        logger.warning("Cloudflare challenge detected! Initiating clearance protocol...")
        start_time = time.time()
        
        # Phase 1: Wait for automated stealth / JS challenge resolution
        while time.time() - start_time < 15:
            if not cls.is_challenge_present(page):
                logger.info("Cloudflare challenge automatically bypassed via stealth headers!")
                return True
            time.sleep(1.5)
            
        # Phase 2: Interactive Turnstile or human verification needed
        if human_fallback:
            logger.warning("=======================================================")
            logger.warning("HUMAN VERIFICATION REQUIRED: Please complete captcha on browser.")
            logger.warning("The script will automatically resume as soon as cleared.")
            logger.warning("=======================================================")
            
            while time.time() - start_time < timeout_sec:
                if not cls.is_challenge_present(page):
                    logger.info("Manual verification confirmed! Resuming automation queue...")
                    return True
                time.sleep(2)
                
        logger.error(f"Cloudflare clearance timed out after {timeout_sec}s.")
        return False
