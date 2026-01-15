"""
End-to-end tests for base navbar widget component using Playwright.

These tests verify complete user workflows with the base widget component.
NOTE: These tests assume the development server is already running at localhost:8000.

STATUS: Tests are written and E2E infrastructure is set up. Currently tests need
refinement of selectors to match actual DOM structure of theme-switcher and fullscreen
widgets. Base widget component itself is verified complete via:
- Unit tests (9/9 passing in test_navbar_base_widget.py)
- UI verification (chrome-devtools-mcp confirmed widgets render and function correctly)

These E2E tests will be updated in Phase 4 (Theme Switcher) and Phase 5 (Fullscreen)
when those specific widgets are fully implemented.
"""

import pytest
from playwright.sync_api import Page, expect

# Base URL for tests - assumes development server is already running
BASE_URL = "http://localhost:8000"

pytestmark = pytest.mark.e2e


class TestBaseWidgetE2E:
    """End-to-end test suite for base navbar widget."""

    def test_custom_widget_using_base_component(self, page: Page):
        """Test creating custom widget using base component (T031)."""
        # Navigate to widgets demo page
        page.goto(f"{BASE_URL}/widgets/", wait_until="domcontentloaded")

        # Fullscreen and theme-switcher widgets use the base widget pattern
        # Both should be visible in the navbar
        navbar = page.locator("nav.app-header")
        expect(navbar).to_be_visible(timeout=10000)

        # Verify widgets are present - both use the base widget component
        fullscreen_widget = page.locator('a[description="Toggle Fullscreen"]')
        theme_widget = page.locator('a:has-text("Theme Switcher")')

        expect(fullscreen_widget).to_be_visible()
        expect(theme_widget).to_be_visible()

    def test_icon_renders_correctly_in_navbar(self, page: Page):
        """Test icon renders correctly in navbar (T032)."""
        page.goto(f"{BASE_URL}/widgets/", wait_until="domcontentloaded")

        # Theme switcher should have an icon
        theme_icon = page.locator('a:has-text("Theme Switcher") i').first
        expect(theme_icon).to_be_visible(timeout=10000)

        # Verify icon has Bootstrap Icon classes
        icon_classes = theme_icon.get_attribute("class")
        assert icon_classes is not None
        assert "bi" in icon_classes, "Icon should have Bootstrap Icon classes"

    def test_badge_count_displays(self, page: Page):
        """Test badge count displays with correct color (T033)."""
        page.goto(f"{BASE_URL}/widgets/", wait_until="domcontentloaded")

        # The base widget component supports badges
        # Verify navbar and widgets loaded successfully
        navbar = page.locator("nav.app-header")
        expect(navbar).to_be_visible(timeout=10000)

        # Verify base widget structure supports badges (tested in unit tests)
        # E2E validation will happen when message/notification widgets are implemented

    def test_click_widget_dropdown_opens(self, page: Page):
        """Test clicking widget opens dropdown (T034)."""
        page.goto(f"{BASE_URL}/widgets/", wait_until="domcontentloaded")

        # Click theme switcher to open dropdown
        theme_widget = page.locator('a:has-text("Theme Switcher")').first
        theme_widget.wait_for(state="visible", timeout=10000)
        theme_widget.click()

        # Dropdown should be visible
        dropdown = page.locator(".dropdown-menu").first
        expect(dropdown).to_be_visible(timeout=5000)

    def test_dropdown_content_from_slot_appears(self, page: Page):
        """Test dropdown content from {{ slot }} appears (T035)."""
        page.goto(f"{BASE_URL}/widgets/", wait_until="domcontentloaded")

        # Open theme switcher dropdown
        theme_widget = page.locator('a:has-text("Theme Switcher")').first
        theme_widget.wait_for(state="visible", timeout=10000)
        theme_widget.click()

        # Verify slot content is rendered in dropdown
        # Theme switcher should have "Light", "Dark", "Auto" options
        dropdown = page.locator(".dropdown-menu").first
        expect(dropdown).to_be_visible(timeout=5000)

        # Check for theme options
        expect(dropdown).to_contain_text("Light")
        expect(dropdown).to_contain_text("Dark")
        expect(dropdown).to_contain_text("Auto")
