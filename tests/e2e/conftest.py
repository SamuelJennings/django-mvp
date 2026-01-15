"""
E2E test fixtures for Playwright.

Provides fixtures for browser automation and live server integration.
"""

import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context with sensible defaults for testing.
    """
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        },
        "ignore_https_errors": True,
    }
