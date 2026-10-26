# Cloudflare-Resilient Video Upload Automation 🛡️📹

[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Cloudflare Evasion](https://img.shields.io/badge/Cloudflare-Turnstile%20Resilient-orange.svg)](https://cloudflare.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust Python browser automation framework engineered with **Playwright**, **stealth fingerprint spoofing**, **persistent cookie sessions**, and **human-in-the-loop fallback** to ensure uninterrupted video upload workflows across Cloudflare-protected web portals.

---

## ⚡ Key Highlights

- 🛡️ **Cloudflare Challenge Interception**: Automatically detects Turnstile iframes, waiting rooms, and interstitial security verifications.
- 🍪 **Persistent Session State**: Stores browser context, local storage, and authentication cookies in a persistent profile directory, reducing repeated security checkpoints.
- 🔁 **Human-in-the-Loop Auto-Resume**: When an interactive challenge requires human verification, execution pauses safely without crashing, waits for resolution, and resumes upload queues immediately.
- 📈 **Resilient Retry Handlers**: Implements exponential backoff, checksum tracking, and upload checkpointing to prevent corrupt or duplicate uploads.

---

## 🏗️ Architecture Flow

```
┌─────────────────────────┐
│     Video Upload Job    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Persistent Browser     │  ◄── Loads saved cookies & local storage
│  (Stealth Fingerprints) │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Cloudflare Challenge?   │
└──────┬───────────┬──────┘
       │ NO        │ YES
       │           ▼
       │     ┌───────────────────────────────────┐
       │     │ Wait for clearance / Prompt human │
       │     └─────────────────┬─────────────────┘
       │                       │ Cleared
       ▼ ◄─────────────────────┘
┌─────────────────────────┐
│   Attach & Upload Video │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Save State & Checkpoint │
└─────────────────────────┘
```

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/Booshdag-io/cloudflare-stealth-uploader.git
cd cloudflare-stealth-uploader
pip install -r requirements.txt
playwright install chromium
```

### 2. Usage
```python
from stealth_uploader.uploader import VideoUploadPipeline

pipeline = VideoUploadPipeline(
    target_url="https://target-portal.com/upload",
    session_dir="./my_browser_session",
    headless=False  # Headless=False enables visual verification if Cloudflare challenges
)

success = pipeline.execute_upload(
    video_file_path="my_video.mp4",
    title="Automated Upload",
    description="Automated with Cloudflare resilience"
)
```

---

## 📄 License

MIT © [Booshdag-io](https://github.com/Booshdag-io)
