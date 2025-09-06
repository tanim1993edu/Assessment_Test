"""
Browser configuration utilities.

This module provides functions and types for configuring browser contexts
with consistent options across tests. It supports both headed and headless
modes, various viewport sizes, and handles download directory setup.
"""

from __future__ import annotations

from typing import Dict, Any
from pathlib import Path

from playwright.sync_api import BrowserContext
from utils.config import settings


def get_browser_context_args(
    download_dir: Path = settings.download_dir,
    headed: bool = False,
    slow_mo: int = 0
) -> Dict[str, Any]:
    """Get standardized browser context configuration.

    Args:
        download_dir: Directory where downloaded files will be saved.
        headed: Whether to run in headed mode.
        slow_mo: Milliseconds to wait between actions (for debugging).

    Returns:
        Dictionary of context options suitable for launching browsers.
    """
    return {
        "viewport": {"width": 1920, "height": 1080},
        "accept_downloads": True,
        "downloads_path": str(download_dir),
        "record_video_dir": str(settings.log_dir / "videos") if headed else None,
        "record_har_path": str(settings.log_dir / "network.har") if headed else None,
        "slow_mo": slow_mo
    }


def setup_browser_tracing(context: BrowserContext) -> None:
    """Configure browser tracing for debugging test failures.

    Args:
        context: The browser context to configure tracing for.
    """
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )