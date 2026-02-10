"""
Unit tests for theme switcher navbar widget component.

Tests the theme switcher component that extends the base widget
to provide light/dark/auto theme selection with localStorage persistence.
"""

import pytest


@pytest.mark.django_db
class TestThemeSwitcherComponent:
    """Test suite for theme switcher component rendering."""

    def test_theme_switcher_renders_with_light_dark_auto_options(self, cotton_render_soup):
        """Test theme switcher component renders with Light/Dark/Auto options (T036)."""
        soup = cotton_render_soup("navbar.widgets.theme-switcher")

        # Should have dropdown menu
        dropdown = soup.find("div", class_="dropdown-menu")
        assert dropdown is not None, "Theme switcher should have dropdown menu"

        # Should have Light, Dark, and Auto options
        dropdown_text = dropdown.get_text()
        assert "Light" in dropdown_text, "Should have Light theme option"
        assert "Dark" in dropdown_text, "Should have Dark theme option"
        assert "Auto" in dropdown_text, "Should have Auto theme option"

    def test_theme_switcher_uses_theme_light_icon_alias(self, cotton_render_soup):
        """Test theme switcher uses theme_light icon alias (T037)."""
        soup = cotton_render_soup("navbar.widgets.theme-switcher")

        # Should have icon rendered by c-icon component
        icon = soup.find("i")
        assert icon is not None, "Theme switcher should have icon"

        # Icon should have Bootstrap Icon classes (rendered by c-icon)
        icon_classes = icon.get("class", [])
        assert "bi" in icon_classes, "Icon should have Bootstrap Icon classes"

    def test_theme_switcher_extends_base_widget_correctly(self, cotton_render_soup):
        """Test theme switcher extends base widget correctly (T038)."""
        soup = cotton_render_soup("navbar.widgets.theme-switcher")

        # Should have nav-item dropdown structure from base widget
        nav_item = soup.find("li", class_="nav-item")
        assert nav_item is not None, "Should have nav-item from base widget"
        assert "dropdown" in nav_item.get("class", []), "Should have dropdown class from base widget"

        # Should have nav-link with data-bs-toggle
        nav_link = soup.find("a", class_="nav-link")
        assert nav_link is not None, "Should have nav-link from base widget"
        assert nav_link.get("data-bs-toggle") == "dropdown", "Should have dropdown toggle"

    def test_active_theme_indicator_displays_in_dropdown(self, cotton_render_soup):
        """Test theme switcher has check icons (hidden by default, shown by JS) (T039)."""
        soup = cotton_render_soup("navbar.widgets.theme-switcher")

        # All theme options should have check icons
        for theme_name in ["Light", "Dark", "Auto"]:
            found = False
            dropdown_items = soup.find_all("a", class_="dropdown-item")
            for item in dropdown_items:
                if theme_name in item.get_text():
                    found = True
                    # Should have check icon element
                    icon = item.find("i", class_="bi")
                    assert icon is not None, f"{theme_name} option should have check icon"
                    break
            assert found, f"Should find {theme_name} theme option"

        # No active class by default (added by JavaScript)
        dropdown_items = soup.find_all("a", {"data-theme": True})
        for item in dropdown_items:
            classes = item.get("class", [])
            assert "active" not in classes, "Should not have active class by default (JS adds it)"

    def test_theme_switcher_dropdown_has_data_attributes_for_js(self, cotton_render_soup):
        """Test theme switcher dropdown has correct data attributes for JS (T040)."""
        soup = cotton_render_soup("navbar.widgets.theme-switcher")

        # Widget should have data attribute for JS targeting
        nav_item = soup.find("li", class_="nav-item")
        assert nav_item is not None, "Should have nav-item"

        # Should have data-theme-switcher or similar attribute
        has_data_attr = (
            nav_item.get("data-theme-switcher") is not None
            or nav_item.get("id") == "theme-switcher"
            or soup.find(attrs={"data-theme-switcher": True}) is not None
        )
        assert has_data_attr, "Should have data attribute for JavaScript targeting"

        # Each theme option should have data-theme attribute
        dropdown_items = soup.find_all("a", class_="dropdown-item")
        for item in dropdown_items:
            item_text = item.get_text()
            if any(theme in item_text for theme in ["Light", "Dark", "Auto"]):
                data_theme = item.get("data-theme")
                assert data_theme is not None, f"Theme option '{item_text.strip()}' should have data-theme attribute"
                assert data_theme.lower() in [
                    "light",
                    "dark",
                    "auto",
                ], f"data-theme should be light/dark/auto, got {data_theme}"
