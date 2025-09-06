"""
Global configuration used across the automation framework.

Values are read from environment variables when available, falling back
to sensible defaults. Keeping configuration in a separate module
decouples tests from hardcoded values and enables easy overrides via
CI/CD pipelines or command line options.
"""

import os
from pathlib import Path
from typing import Dict, Any


class Settings:
    """Configuration object for retrieving runtime settings."""

    def __init__(self) -> None:
        # Base URL and API endpoints
        self.base_url: str = os.getenv("BASE_URL", "https://automationexercise.com")
        self.api_base_url: str = f"{self.base_url}/api"
        
        # File paths and directories
        self.download_dir: Path = Path(os.getenv("DOWNLOAD_DIR", "downloads")).resolve()
        self.log_dir: Path = Path(os.getenv("LOG_DIR", "logs")).resolve()
        self.report_dir: Path = Path(os.getenv("REPORT_DIR", "reports")).resolve()
        self.credentials_file: Path = Path("user_credentials.json").resolve()
        
        # Browser configuration
        self.browsers: list[str] = os.getenv("BROWSERS", "chromium,firefox").split(",")
        self.headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
        self.slow_mo: int = int(os.getenv("SLOW_MO", "0"))
        
        # Test execution settings
        self.retry_count: int = int(os.getenv("RETRY_COUNT", "2"))
        self.parallel_workers: int = int(os.getenv("PARALLEL_WORKERS", "2"))
        self.video_recording: bool = os.getenv("VIDEO_RECORDING", "false").lower() == "true"
        
        # Timeouts
        self.default_timeout: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
        self.navigation_timeout: int = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
        
        # API Settings
        self.api_timeout: int = int(os.getenv("API_TIMEOUT", "30000"))
        self.api_retry_count: int = int(os.getenv("API_RETRY_COUNT", "3"))

    def ensure_directories(self) -> None:
        """Create directories for downloads and logs if they don't exist."""
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
