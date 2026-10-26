"""
Example script demonstrating Cloudflare-resilient video upload pipeline.
"""
import logging
from stealth_uploader.uploader import VideoUploadPipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    target_portal = "https://example-video-platform.com/upload"
    sample_clip = "sample_video.mp4"
    
    pipeline = VideoUploadPipeline(
        target_url=target_portal,
        session_dir="./saved_session",
        headless=False # Set False to allow interactive captcha resolution
    )
    
    # Run the upload pipeline with Cloudflare handling and auto-resume
    # pipeline.execute_upload(
    #     video_file_path=sample_clip,
    #     title="Automated Upload Test",
    #     description="Uploaded via Cloudflare-Resilient Python pipeline"
    # )
    print("Example pipeline configured and ready for production endpoints.")

if __name__ == "__main__":
    main()
