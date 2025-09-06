"""
Reusable navigation component for common header actions.

This component encapsulates all header navigation related actions that are
shared across multiple pages, improving maintainability and reducing code
duplication.
"""

from __future__ import annotations

import logging
from typing import Optional

from playwright.sync_api import Page
from pages.base_page import BasePage


class NavigationComponent(BasePage):
    """Component for interacting with the site's main navigation."""

    def __init__(self, page: Page, logger: Optional[logging.Logger] = None) -> None:
        super().__init__(page, logger)
        # Header navigation locators
        self._home_link = page.locator("a[href='/']")
        self._products_link = page.locator("a[href='/products']")
        self._cart_link = page.locator("a[href='/view_cart']")
        self._login_link = page.locator("a[href='/login']")
        self._logout_link = page.locator("a[href='/logout']")
        self._delete_account_link = page.locator("a[href='/delete_account']")

    def go_to_home(self) -> None:
        """Navigate to the home page."""
        self.click(self._home_link)

    def go_to_products(self) -> None:
        """Navigate to the products page."""
        self.click(self._products_link)

    def go_to_cart(self) -> None:
        """Navigate to the shopping cart."""
        self.click(self._cart_link)

    def go_to_login(self) -> None:
        """Navigate to the login/signup page."""
        self.click(self._login_link)

    def logout(self) -> None:
        """Click the logout link."""
        self.click(self._logout_link)

    def delete_account(self) -> None:
        """Click the delete account link."""
        self.click(self._delete_account_link)