import os
import time
import logging
from .browser import ResilientBrowser
from .cloudflare_handler import CloudflareHandler

logger = logging.getLogger("stealth_uploader.uploader")

class VideoUploadPipeline:
    """High-reliability automated upload pipeline with automatic retry and Cloudflare recovery."""
    
    def __init__(self, target_url: str, session_dir: str = "./browser_session", headless: bool = False):
        self.target_url = target_url
        self.browser_manager = ResilientBrowser(user_data_dir=session_dir, headless=headless)
        
    def execute_upload(self, video_file_path: str, title: str, description: str, max_retries: int = 3) -> bool:
        if not os.path.exists(video_file_path):
            raise FileNotFoundError(f"Video file not found at: {video_file_path}")
            
        file_size_mb = round(os.path.getsize(video_file_path) / (1024 * 1024), 2)
        logger.info(f"Initiating upload for '{video_file_path}' ({file_size_mb} MB) -> {self.target_url}")
        
        page = self.browser_manager.start()
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"[Attempt {attempt}/{max_retries}] Navigating to portal...")
                page.goto(self.target_url, wait_until="domcontentloaded", timeout=45000)
                
                # Check for Cloudflare challenge
                if not CloudflareHandler.wait_for_clearance(page, timeout_sec=90, human_fallback=True):
                    raise TimeoutError("Cloudflare verification could not be cleared.")
                    
                logger.info("Portal reached successfully. Handling file input...")
                # Note: File input selection handles standard HTML5 input[type=file]
                file_input = page.wait_for_selector("input[type=file]", timeout=15000)
                file_input.set_input_files(video_file_path)
                logger.info("File payload attached to upload buffer.")
                
                # Save session cookies after successful interaction
                self.browser_manager.save_storage_state()
                logger.info("Upload sequence successfully triggered!")
                return True
                
            except Exception as e:
                logger.error(f"Error on attempt {attempt}: {e}")
                if attempt < max_retries:
                    wait_time = attempt * 5
                    logger.info(f"Retrying in {wait_time}s with exponential backoff...")
                    time.sleep(wait_time)
                else:
                    logger.critical("Max upload retries exceeded.")
            finally:
                self.browser_manager.close()
                
        return False
