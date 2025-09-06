"""
Pytest fixtures for browser and test setup.

This module defines fixtures that spin up Playwright browsers with a
configured downloads directory, manage the event loop for synchronous
tests and expose the ``page`` object used across tests. It also
includes a fixture for loading and storing user credentials.

Fixtures:

* ``browser_name`` – parameterised over the list of browsers defined
  in ``settings.browsers``. This enables cross‑browser execution
  automatically in pytest.
* ``browser`` – yields the Playwright browser instance for the given
  browser name.
* ``context`` – provides a new browser context with a custom
  downloads directory.
* ``page`` – yields a new page for each test case.
* ``credentials_file`` – yields the path to the user credentials JSON
  and ensures it's available before tests that rely on it.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Generator, Any
from datetime import datetime

import pytest
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from automation.utils.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(settings.log_dir / 'test_run.log'),
        logging.StreamHandler()
    ]
)

def pytest_configure(config: Any) -> None:
    """Configure HTML reporting and ensure directories exist."""
    # Create necessary directories
    settings.report_dir.mkdir(parents=True, exist_ok=True)
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure HTML report
    config.option.htmlpath = str(settings.report_dir / f"report_{datetime.now():%Y%m%d_%H%M%S}.html")
    config.option.self_contained_html = True


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo[None]) -> Generator[None, Any, None]:
    """Capture screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            # Try to get the page object from fixtures
            page = None
            for name, value in item.funcargs.items():
                if isinstance(value, Page):
                    page = value
                    break
            
            if page:
                # Take screenshot
                screenshot_dir = settings.report_dir / "screenshots"
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = screenshot_dir / f"failure_{item.name}_{timestamp}.png"
                page.screenshot(path=str(screenshot_path))
                
                # Add to report
                if hasattr(item.config, "_html"):
                    html = f'<div><img src="{screenshot_path}" style="width:600px"></div>'
                    item.config._html.append(html)
                    
                logging.error(f"Test failed. Screenshot saved: {screenshot_path}")
        
        except Exception as e:
            logging.error(f"Failed to capture screenshot: {e}")


@pytest.fixture(scope="session")
def browser_name() -> list[str]:
    """Provide list of browsers for parametrisation.

    The Playwright pytest plugin automatically discovers this fixture and
    uses it to parameterise the built‑in ``browser_name`` fixture. We
    replicate this behaviour manually here because we are not using the
    plugin but rather creating our own browsers via Playwright API.
    """
    return settings.browsers


@pytest.fixture(scope="session")
def playwright_instance():
    """Start a Playwright instance for the entire session."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance, request) -> Generator[Browser, None, None]:
    """Launch a browser for the current parameterised browser name."""
    browser_name_param = getattr(request, "param", settings.browsers[0])
    
    # Browser-specific launch options
    launch_options = {
        "headless": settings.headless,
        "slow_mo": settings.slow_mo
    }
    
    # Add Firefox-specific options
    if browser_name_param == "firefox":
        launch_options.update({
            "firefox_user_prefs": {
                "browser.download.dir": str(settings.download_dir),
                "browser.download.folderList": 2,
                "browser.download.manager.showWhenStarting": False,
                "browser.helperApps.neverAsk.saveToDisk": "application/pdf,application/x-pdf"
            }
        })
    
    browser = getattr(playwright_instance, browser_name_param).launch(**launch_options)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Create a new context for each test.

    The context is configured with its own downloads directory and
    default timeout. This ensures isolation between tests and allows
    retrieval of downloaded files.
    """
    download_dir = settings.download_dir / f"run_{os.getpid()}"
    download_dir.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(accept_downloads=True)
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Yield a new page for the current test."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(autouse=True)
def _setup_reporting_dirs():
    """Ensure reporting directories exist."""
    for dir_path in [settings.report_dir, settings.log_dir, settings.download_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo[None]) -> Generator[None, Any, None]:
    """Capture screenshot and page source on test failure."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            # Try to get the page object from fixtures
            page = None
            for name, value in item.funcargs.items():
                if isinstance(value, Page):
                    page = value
                    break
            
            if page:
                # Take screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_dir = settings.report_dir / "screenshots"
                screenshot_dir.mkdir(exist_ok=True)
                
                screenshot_path = screenshot_dir / f"failure_{item.name}_{timestamp}.png"
                page.screenshot(path=str(screenshot_path))
                
                # Save page source
                source_dir = settings.report_dir / "page_source"
                source_dir.mkdir(exist_ok=True)
                source_path = source_dir / f"source_{item.name}_{timestamp}.html"
                source_path.write_text(page.content())
                
                # Add to HTML report
                if hasattr(item.config, "_html"):
                    extra = getattr(report, "extra", [])
                    extra.append(item.config._html.extras.image(str(screenshot_path)))
                    extra.append(item.config._html.extras.html(f"<a href='{source_path}'>Page Source</a>"))
                    report.extra = extra
                    
                logging.error(f"Test failed. Screenshot saved: {screenshot_path}")
                logging.error(f"Page source saved: {source_path}")
        
        except Exception as e:
            logging.error(f"Failed to capture failure artifacts: {e}")

@pytest.fixture(scope="session")
def credentials_file() -> Path:
    """Return the path to the JSON file storing user credentials."""
    file_path = Path("user_credentials.json").resolve()
    # Ensure file exists; if not, create an empty stub
    if not file_path.exists():
        file_path.write_text(json.dumps({"email": "", "password": ""}))
    return file_path
