"""
Page object representing the "Signup / Login" page on Automation Exercise.

This page contains both the login form for existing users and the sign‑up
form for new users. In our end‑to‑end purchase flow we only need the
login form since account creation is performed via the API. The locators
used here are resilient to small UI changes by targeting visible labels
rather than brittle CSS classes.
"""

from __future__ import annotations

import logging
from playwright.sync_api import Page
from automation.pages.base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates interactions with the login portion of the login page."""

    # Locators for login form fields and buttons. These are defined as class
    # attributes for easy reuse and to avoid string duplication throughout
    # methods. Should the UI change, you only need to update these here.
    EMAIL_INPUT = "input[data-qa='login-email']"
    PASSWORD_INPUT = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"

    def __init__(self, page: Page, logger: logging.Logger | None = None) -> None:
        super().__init__(page, logger)

    def login(self, email: str, password: str) -> None:
        """Authenticate using the login form.

        Args:
            email: The user's registered email address.
            password: The user's plaintext password.
        """
        self.logger.info(f"Attempting login with email: {email}")
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
