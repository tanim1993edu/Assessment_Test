"""
Base page object for Playwright page interactions.

This module defines a ``BasePage`` class that all page objects in the
framework inherit from. It exposes a reference to the Playwright ``Page``
instance and provides a handful of convenience methods for interacting
with the UI. Encapsulating common behaviour here improves maintainability
and allows you to swap out the underlying implementation (e.g. switch to
another driver) without rewriting every page object.

Because Playwright has rich built‑in methods for waiting and action
assertions, this base class simply wraps a few of those methods to keep
page objects terse. It also accepts a logger so that all interactions
generate useful debug output which can be consumed by test reports.

Usage:

    from pages.base_page import BasePage
    from playwright.sync_api import Page

    class HomePage(BasePage):
        def __init__(self, page: Page, logger: logging.Logger):
            super().__init__(page, logger)
            ...

        def click_login(self) -> None:
            self.click("text=Signup / Login")

The above example shows how the base page can be used to define
interactions on derived page objects.
"""

from __future__ import annotations

import logging
from typing import Optional, Union

from playwright.sync_api import Page, Locator


class BasePage:
    """A generic page object base class for Playwright tests.

    This class wraps a Playwright ``Page`` instance and exposes helper
    methods for the most common interactions. All page objects in the
    framework should derive from this class to inherit these helpers and
    automatically log actions.
    """

    def __init__(self, page: Page, logger: Optional[logging.Logger] = None) -> None:
        self.page = page
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def navigate(self, url: str) -> None:
        """Navigate the browser to ``url`` and wait until network is idle."""
        self.logger.debug(f"Navigating to URL: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def click(self, selector: Union[str, Locator], *, force: bool = False) -> None:
        """Click an element specified by the CSS selector or Locator.

        Args:
            selector: CSS selector string or Playwright Locator to click on.
            force: If set to ``True``, Playwright will bypass actionability
                checks and attempt the click regardless of element state.
        """
        self.logger.debug(f"Clicking element: {selector}")
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        locator.click(force=force)

    def fill(self, selector: Union[str, Locator], text: str) -> None:
        """Fill an input element with the given text."""
        self.logger.debug(f"Filling element {selector} with text: {text}")
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        locator.fill(text)

    def get_text(self, selector: Union[str, Locator]) -> str:
        """Return the inner text of the element matched by ``selector``."""
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        text = locator.inner_text()
        self.logger.debug(f"Got text from {selector!r}: {text!r}")
        return text

    def wait_for_url(self, url_substring: str, timeout: int = 10000) -> None:
        """Wait until the current URL contains ``url_substring`` within ``timeout`` ms."""
        self.logger.debug(f"Waiting for URL to contain: {url_substring}")
        self.page.wait_for_url(f"**{url_substring}**", timeout=timeout)

    def expect_visible(self, selector: Union[str, Locator]) -> None:
        """Assert that the given element is visible."""
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        self.logger.debug(f"Asserting element {selector} is visible")
        locator.wait_for(state="visible")

    def expect_not_visible(self, selector: Union[str, Locator]) -> None:
        """Assert that the given element is not visible."""
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        self.logger.debug(f"Asserting element {selector} is not visible")
        locator.wait_for(state="hidden")

    def select_option(self, selector: Union[str, Locator], value: str) -> None:
        """Select an option from a dropdown by value."""
        self.logger.debug(f"Selecting option {value} from dropdown {selector}")
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        locator.select_option(value=value)

    def get_attribute(self, selector: Union[str, Locator], name: str) -> str:
        """Get the value of an attribute on the element."""
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        value = locator.get_attribute(name)
        self.logger.debug(f"Got attribute {name} from {selector}: {value}")
        return value or ""

    def wait_for_download(self) -> str:
        """Wait for a download to complete and return the file path."""
        with self.page.expect_download() as download_info:
            yield
        download = download_info.value
        path = download.path()
        self.logger.debug(f"Download completed: {path}")
        return str(path)

    def expect_enabled(self, selector: Union[str, Locator]) -> None:
        """Assert that the given element is enabled."""
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        self.logger.debug(f"Asserting element {selector} is enabled")
        locator.wait_for(state="visible")
        assert locator.is_enabled(), f"Element {selector} is not enabled"

    def scroll_into_view(self, selector: Union[str, Locator]) -> None:
        """Scroll the element into view."""
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        self.logger.debug(f"Scrolling element {selector} into view")
        locator.scroll_into_view_if_needed()

    def get_count(self, selector: Union[str, Locator]) -> int:
        """Get the number of elements matching the selector."""
        locator = selector if isinstance(selector, Locator) else self.page.locator(selector)
        count = locator.count()
        self.logger.debug(f"Found {count} elements matching {selector}")
        return count
