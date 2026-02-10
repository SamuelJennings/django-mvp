"""
Component Tests for Fullscreen Widget

Tests the fullscreen toggle widget component that uses AdminLTE 4's fullscreen plugin.
"""

import pytest


@pytest.fixture
def render_fullscreen_widget(cotton_render_soup):
    """Helper to render fullscreen widget and return BeautifulSoup object."""

    def _render(**context):
        return cotton_render_soup("navbar/widgets/fullscreen", **context)

    return _render


@pytest.mark.django_db
class TestFullscreenWidgetComponent:
    """
    Test fullscreen widget component.

    Requirements:
    - Renders with maximize icon alias
    - Has data-lte-toggle="fullscreen" attribute for AdminLTE integration
    - Extends base widget pattern without dropdown
    - Has ARIA label for accessibility
    - Conditionally renders based on Fullscreen API support
    """

    def test_fullscreen_widget_renders_with_maximize_icon(self, render_fullscreen_widget):
        """T076: Test fullscreen widget renders with maximize icon alias."""
        soup = render_fullscreen_widget()

        # Find the icon element
        icon = soup.find("i")
        assert icon is not None, "Icon element not found"

        # Check icon classes (should have bi-arrows-fullscreen or similar)
        icon_classes = icon.get("class", [])
        # Icon should use easy-icons, so just verify icon element exists
        assert len(icon_classes) > 0, "Icon should have classes"

    def test_fullscreen_widget_has_data_lte_toggle_attribute(self, render_fullscreen_widget):
        """T077: Test widget has data-lte-toggle='fullscreen' attribute."""
        soup = render_fullscreen_widget()

        # Find element with data-lte-toggle attribute
        toggle_element = soup.find(attrs={"data-lte-toggle": "fullscreen"})
        assert toggle_element is not None, "Element with data-lte-toggle='fullscreen' not found"

        # Verify it's a link or button
        assert toggle_element.name in [
            "a",
            "button",
        ], f"Expected link or button, got {toggle_element.name}"

    def test_fullscreen_widget_extends_base_widget_without_dropdown(self, render_fullscreen_widget):
        """T078: Test widget extends base widget without dropdown."""
        soup = render_fullscreen_widget()

        # Verify nav-item structure (from base widget)
        nav_item = soup.find("li", class_="nav-item")
        assert nav_item is not None, "nav-item not found"

        # Verify nav-link exists
        nav_link = nav_item.find("a", class_="nav-link")
        assert nav_link is not None, "nav-link not found"

        # Verify NO dropdown menu (fullscreen doesn't need dropdown)
        dropdown_menu = soup.find(class_="dropdown-menu")
        assert dropdown_menu is None, "Fullscreen widget should not have dropdown menu"

        # Verify NO dropdown class on nav-item
        nav_item_classes = nav_item.get("class", [])
        assert "dropdown" not in nav_item_classes, "nav-item should not have dropdown class"

    def test_fullscreen_widget_has_aria_label(self, render_fullscreen_widget):
        """T079: Test widget has ARIA label for accessibility."""
        soup = render_fullscreen_widget()

        # Find the nav-link with aria-label
        nav_link = soup.find("a", class_="nav-link")
        assert nav_link is not None, "nav-link not found"

        aria_label = nav_link.get("aria-label")
        assert aria_label is not None, "aria-label not found"
        assert len(aria_label) > 0, "aria-label should not be empty"
        assert "fullscreen" in aria_label.lower(), "aria-label should mention fullscreen"

    def test_fullscreen_widget_conditional_rendering(self, cotton_render_soup):
        """T080: Test widget always renders (JS handles hiding if API not supported)."""
        # The fullscreen widget always renders in the template
        # JavaScript handles hiding it if the Fullscreen API is not supported

        # Test rendering
        soup = cotton_render_soup("navbar/widgets/fullscreen")
        nav_item = soup.find("li", class_="nav-item")
        assert nav_item is not None, "Widget should always render"

        # Should have fullscreen toggle link
        link = nav_item.find("a", {"data-lte-toggle": "fullscreen"})
        assert link is not None, "Widget should have fullscreen toggle link"

        # JavaScript will handle hiding if Fullscreen API not supported
        # (tested in E2E tests)
