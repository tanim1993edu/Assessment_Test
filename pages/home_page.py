"""
Page object representing the home page of Automation Exercise.

The home page exposes top navigation elements used to drive the purchase
flow, such as the link to the login page and product categories. The
locators defined here target the visible names of the menu items rather
than classes which may change over time.
"""

from __future__ import annotations

import logging
from playwright.sync_api import Page
from automation.pages.base_page import BasePage


class HomePage(BasePage):
    """Encapsulates interactions on the home page."""

    SIGNUP_LOGIN_LINK = "a[href='/login']"
    PRODUCTS_LINK = "a[href='/products']"
    CART_LINK = "a[href='/view_cart']" # Using the same locator as ProductPage

    def __init__(self, page: Page, logger: logging.Logger | None = None) -> None:
        super().__init__(page, logger)

    def go_to_login(self) -> None:
        """Click the Signup / Login link in the header."""
        self.click(self.SIGNUP_LOGIN_LINK)

    def go_to_products(self) -> None:
        """Click the Products link in the header to view all items."""
        self.click(self.PRODUCTS_LINK)

    def go_to_cart(self) -> None:
        """Navigate directly to the shopping cart."""
        self.click(self.CART_LINK)
