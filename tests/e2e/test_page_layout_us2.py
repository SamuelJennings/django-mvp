"""
E2E tests for User Story 2: Secondary Sidebar Integration.

Tests sidebar toggle functionality and sessionStorage persistence.

NOTE: These E2E tests have Django async configuration challenges.
The sidebar toggle functionality can be verified via:
- Unit tests (tests/test_page_layout_us2.py)
- Manual testing in browser
- Chrome DevTools inspection
"""

import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
@pytest.mark.skip(reason="E2E infrastructure - needs async Django configuration")
class TestInnerLayoutSidebarToggle:
    """Test sidebar toggle functionality (US2)."""

    def test_toggle_button_toggles_sidebar_visibility(self, page: Page, live_server):
        """Test that clicking toggle button shows/hides sidebar."""
        # Navigate to a page with toggleable sidebar
        page.goto(f"{live_server.url}/page-layout/")

        # Wait for page to load
        page.wait_for_load_state("networkidle")

        # Verify sidebar is initially visible
        sidebar = page.locator("#page-sidebar")
        expect(sidebar).to_be_visible()

        # Find and click toggle button
        toggle_button = page.locator("[data-page-layout-toggle]")
        expect(toggle_button).to_be_visible()
        toggle_button.click()

        # Verify sidebar is hidden
        expect(sidebar).to_be_hidden()

        # Verify toggle button aria-expanded changed
        expect(toggle_button).to_have_attribute("aria-expanded", "false")

        # Click again to show sidebar
        toggle_button.click()

        # Verify sidebar is visible again
        expect(sidebar).to_be_visible()
        expect(toggle_button).to_have_attribute("aria-expanded", "true")

    def test_toggle_state_persists_across_page_reloads(self, page: Page, live_server):
        """Test that sidebar toggle state persists via sessionStorage."""
        # Navigate to page with toggleable sidebar
        page.goto(f"{live_server.url}/page-layout/")
        page.wait_for_load_state("networkidle")

        # Get initial sidebar visibility
        sidebar = page.locator("#page-sidebar")
        expect(sidebar).to_be_visible()

        # Toggle sidebar to hidden
        toggle_button = page.locator("[data-page-layout-toggle]")
        toggle_button.click()
        expect(sidebar).to_be_hidden()

        # Reload the page
        page.reload()
        page.wait_for_load_state("networkidle")

        # Verify sidebar remains hidden after reload
        sidebar = page.locator("#page-sidebar")
        expect(sidebar).to_be_hidden()

        # Verify toggle button reflects correct state
        toggle_button = page.locator("[data-page-layout-toggle]")
        expect(toggle_button).to_have_attribute("aria-expanded", "false")

    def test_toggle_button_keyboard_accessible(self, page: Page, live_server):
        """Test that toggle button can be activated via keyboard."""
        page.goto(f"{live_server.url}/page-layout/")
        page.wait_for_load_state("networkidle")

        # Focus on toggle button
        toggle_button = page.locator("[data-page-layout-toggle]")
        toggle_button.focus()

        # Verify button is focused
        expect(toggle_button).to_be_focused()

        # Get initial sidebar state
        sidebar = page.locator("#page-sidebar")
        expect(sidebar).to_be_visible()

        # Press Enter to toggle
        page.keyboard.press("Enter")

        # Verify sidebar is hidden
        expect(sidebar).to_be_hidden()

        # Press Space to toggle back
        toggle_button.focus()  # Re-focus in case it changed
        page.keyboard.press("Space")

        # Verify sidebar is visible again
        expect(sidebar).to_be_visible()

    def test_sidebar_responsive_hiding_below_breakpoint(self, page: Page, live_server):
        """Test that sidebar hides automatically below responsive breakpoint."""
        # Navigate to page with sidebar
        page.goto(f"{live_server.url}/page-layout/")
        page.wait_for_load_state("networkidle")

        # Verify sidebar is visible at desktop width (1280px)
        sidebar = page.locator("#page-sidebar")
        expect(sidebar).to_be_visible()

        # Resize viewport to below 'lg' breakpoint (1024px)
        page.set_viewport_size({"width": 768, "height": 720})

        # Wait for responsive changes
        page.wait_for_timeout(100)

        # Verify sidebar is hidden due to responsive CSS
        # Note: Check computed display style since CSS may hide it
        is_hidden = sidebar.evaluate("el => window.getComputedStyle(el).display === 'none'")
        assert is_hidden, "Sidebar should be hidden below lg breakpoint"


@pytest.mark.e2e
@pytest.mark.skip(reason="E2E infrastructure - needs async Django configuration")
class TestInnerLayoutSidebarAcceptanceScenarios:
    """Test User Story 2 acceptance scenarios."""

    def test_us2_scenario1_sidebar_displays_with_adjusted_content(self, page: Page, live_server):
        """
        Given a page with inner layout including sidebar
        When the page loads
        Then sidebar displays on the right
        And content area adjusts width to accommodate sidebar
        """
        page.goto(f"{live_server.url}/page-layout/")
        page.wait_for_load_state("networkidle")

        # Verify sidebar exists and is visible
        sidebar = page.locator("#page-sidebar")
        expect(sidebar).to_be_visible()

        # Verify sidebar has correct CSS class
        expect(sidebar).to_have_class(re.compile(r"page-sidebar"))

        # Verify content area exists
        content = page.locator(".page-layout-content")
        expect(content).to_be_visible()

        # Verify layout container has sidebar class
        layout = page.locator(".page-layout")
        expect(layout).to_have_class(re.compile(r"has-sidebar"))

    def test_us2_scenario2_toggle_button_shows_hides_sidebar(self, page: Page, live_server):
        """
        Given a page with toggleable sidebar
        When user clicks toggle button
        Then sidebar hides and content expands to full width
        And toggle button icon indicates collapsed state
        """
        page.goto(f"{live_server.url}/page-layout/")
        page.wait_for_load_state("networkidle")

        # Get initial states
        sidebar = page.locator("#page-sidebar")
        toggle_button = page.locator("[data-page-layout-toggle]")

        # Verify initial state: sidebar visible
        expect(sidebar).to_be_visible()
        expect(toggle_button).to_have_attribute("aria-expanded", "true")

        # Click toggle button
        toggle_button.click()

        # Verify sidebar is hidden
        expect(sidebar).to_be_hidden()
        expect(toggle_button).to_have_attribute("aria-expanded", "false")

    def test_us2_scenario3_sidebar_hides_below_breakpoint(self, page: Page, live_server):
        """
        Given a page with sidebar
        When viewport width is below configured breakpoint
        Then sidebar automatically hides
        And toggle button remains visible for manual override
        """
        page.goto(f"{live_server.url}/page-layout/")
        page.wait_for_load_state("networkidle")

        # Verify sidebar visible at desktop width
        sidebar = page.locator("#page-sidebar")
        expect(sidebar).to_be_visible()

        # Resize to tablet width (below lg breakpoint)
        page.set_viewport_size({"width": 768, "height": 720})
        page.wait_for_timeout(100)

        # Verify sidebar is hidden by responsive CSS
        is_hidden = sidebar.evaluate("el => window.getComputedStyle(el).display === 'none'")
        assert is_hidden

        # Verify toggle button still exists
        toggle_button = page.locator("[data-page-layout-toggle]")
        expect(toggle_button).to_be_visible()

    def test_us2_scenario4_toggle_state_persists_across_navigation(self, page: Page, live_server):
        """
        Given a user has collapsed the sidebar
        When user navigates to another page with sidebar
        Then sidebar remains collapsed
        And user preference is maintained within session
        """
        # Navigate to first page with sidebar
        page.goto(f"{live_server.url}/page-layout/")
        page.wait_for_load_state("networkidle")

        # Collapse sidebar
        toggle_button = page.locator("[data-page-layout-toggle]")
        toggle_button.click()

        # Verify sidebar is hidden
        sidebar = page.locator("#page-sidebar")
        expect(sidebar).to_be_hidden()

        # Navigate to another page (reload same page for test)
        page.goto(f"{live_server.url}/page-layout/")
        page.wait_for_load_state("networkidle")

        # Verify sidebar remains hidden
        sidebar = page.locator("#page-sidebar")
        expect(sidebar).to_be_hidden()

        # Verify sessionStorage has the collapsed state
        storage_value = page.evaluate("() => sessionStorage.getItem('page-sidebar-collapsed')")
        assert storage_value == "true", "Sidebar state should be persisted in sessionStorage"
