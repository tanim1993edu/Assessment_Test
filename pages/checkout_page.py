"""Page object for checkout summary and order placement."""

from __future__ import annotations

import logging
from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Encapsulates interactions on the checkout summary page."""

    COMMENT_TEXTAREA = "textarea[name='message']"
    PLACE_ORDER_BUTTON = "a[href*='payment']"

    def __init__(self, page: Page, logger: logging.Logger | None = None) -> None:
        super().__init__(page, logger)

    def add_order_comment(self, comment: str) -> None:
        """Type a comment into the comment textarea."""
        self.logger.debug(f"Adding order comment: {comment}")
        self.fill(self.COMMENT_TEXTAREA, comment)

    def place_order(self) -> None:
        """Click the Place Order button to navigate to payment form."""
        self.logger.info("Placing order and navigating to payment page")
        self.click(self.PLACE_ORDER_BUTTON)
