"""
Page object for handling product listing and actions on Automation Exercise.

This page provides methods to interact with the product grid, add items to
the cart and navigate to product detail pages. It assumes that the
products listing page is already open when methods are invoked. The
selectors intentionally rely on the visible text of buttons and headings
to reduce coupling to CSS classes.
"""

from __future__ import annotations

import logging
from playwright.sync_api import Page
from automation.pages.base_page import BasePage


class ProductPage(BasePage):
    """Encapsulates operations on the products listing page."""

    # Selector for product cards; used for indexing into the product list
    PRODUCT_CARDS = ".product-image-wrapper"
    ADD_TO_CART_BUTTON = "a[href*='add_to_cart']"  # generic anchor used to add to cart
    CONTINUE_SHOPPING_BUTTON = "button[data-dismiss='modal']"
    VIEW_CART_BUTTON = "p.text-center a[href='/view_cart']"  # More specific selector for View Cart in modal

    def __init__(self, page: Page, logger: logging.Logger | None = None) -> None:
        super().__init__(page, logger)

    def add_product_to_cart_by_index(self, index: int) -> None:
        """Add a product to the cart based on its zero‑based index on the page.

        After clicking the Add to cart link a modal is displayed; this method
        clicks "Continue Shopping" to return to the product grid.

        Args:
            index: Zero‑based index of the product card to add.
        """
        self.logger.info(f"Adding product at index {index} to the cart")
        cards = self.page.locator(self.PRODUCT_CARDS)
        target = cards.nth(index)
        # Hover to reveal the Add to cart button if necessary
        target.hover()
        # Click the first Add to cart link within the card
        target.locator("text=Add to cart").first.click()
        # Wait for modal and click Continue Shopping
        self.logger.debug("Waiting for confirmation modal and clicking Continue Shopping")
        self.page.locator(self.CONTINUE_SHOPPING_BUTTON).click()

    def go_to_cart_via_popup(self) -> None:
        """When a product is added to the cart, click the "View Cart" link in the modal."""
        # Wait for modal to be visible and click View Cart
        self.page.wait_for_selector(self.VIEW_CART_BUTTON, state="visible")
        self.page.locator(self.VIEW_CART_BUTTON).first.click()
