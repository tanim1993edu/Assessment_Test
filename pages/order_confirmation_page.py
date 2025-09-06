"""
Page object representing the order confirmation page.

After a successful payment the user is presented with a confirmation
message and a link to download the invoice. This page object provides
methods to assert the presence of the success message and to trigger
the invoice download. The downloaded file path is returned so that
tests can verify its existence and file size.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional
from playwright.sync_api import Page, Download
from automation.pages.base_page import BasePage


class OrderConfirmationPage(BasePage):
    """Encapsulates interactions on the order confirmation page."""

    SUCCESS_MESSAGE_SELECTOR = "div#success_message, h2:has-text('Order Placed!')"
    DOWNLOAD_INVOICE_LINK = "a[href*='download_invoice']"

    def __init__(self, page: Page, logger: logging.Logger | None = None) -> None:
        super().__init__(page, logger)

    def get_success_message(self) -> str:
        """Return the success message text displayed on the page."""
        message = self.get_text(self.SUCCESS_MESSAGE_SELECTOR)
        self.logger.info(f"Order success message: {message}")
        return message

    def download_invoice(self) -> Path:
        """Click the download invoice link and return the path to the downloaded file."""
        self.logger.info("Downloading invoice from confirmation page")
        
        # Ensure download directory exists
        download_dir = Path("downloads").resolve()
        download_dir.mkdir(parents=True, exist_ok=True)
        
        # Wait for download to start and complete
        with self.page.expect_download() as download_info:
            self.click(self.DOWNLOAD_INVOICE_LINK)
        download = download_info.value
        
        # Save to downloads directory
        dest_path = download_dir / f"invoice_{download.suggested_filename}"
        download.save_as(dest_path)
        
        self.logger.info(f"Invoice downloaded to: {dest_path}")
        return dest_path
        
    def verify_invoice_file(self, file_path: Path) -> None:
        """Verify that the invoice file exists and is not empty.
        
        Args:
            file_path: Path to the invoice file to verify.
            
        Raises:
            AssertionError: If file doesn't exist or is empty.
        """
        self.logger.info(f"Verifying invoice file: {file_path}")
        assert file_path.exists(), f"Invoice file not found: {file_path}"
        assert file_path.stat().st_size > 0, f"Invoice file is empty: {file_path}"
        self.logger.info(f"Invoice file verified: {file_path} ({file_path.stat().st_size} bytes)")
