"""
Pytest configuration for Playwright tests
"""

import pytest
from playwright.sync_api import Playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    """Playwright instance"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    """Browser instance"""
    browser = playwright.chromium.launch(headless=False)  # Set to True for CI
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser) -> BrowserContext:
    """Browser context"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="en-US"
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    """Page instance"""
    page = context.new_page()
    yield page
    page.close()

