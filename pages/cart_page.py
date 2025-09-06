"""
Page object representing the shopping cart view.

This page enables verification of items in the cart and progression to
checkout. It also exposes a method to proceed directly to the checkout
screen.
"""

from __future__ import annotations

import logging
from playwright.sync_api import Page
from automation.pages.base_page import BasePage


class CartPage(BasePage):
    """Encapsulates interactions within the cart view."""

    PROCEED_TO_CHECKOUT_BUTTON = ".btn-default.check_out"
    CART_ITEM_ROWS = "#cart_info_table tbody tr"

    def __init__(self, page: Page, logger: logging.Logger | None = None) -> None:
        super().__init__(page, logger)

    def get_cart_items_count(self) -> int:
        """Return the number of line items currently in the cart."""
        count = self.page.locator(self.CART_ITEM_ROWS).count()
        self.logger.debug(f"Cart contains {count} items")
        return count

    def proceed_to_checkout(self) -> None:
        """Click the "Proceed To Checkout" button."""
        self.logger.info("Proceeding to checkout")
        self.click(self.PROCEED_TO_CHECKOUT_BUTTON)
