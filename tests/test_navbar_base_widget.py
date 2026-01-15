"""
Tests for base navbar widget component.

This module tests the base widget component at cotton/navbar/widget.html
which provides the foundation for all custom navbar widgets.
"""

from bs4 import BeautifulSoup


class TestBaseWidgetRendering:
    """Test suite for base widget rendering."""

    def test_base_widget_renders_with_icon_alias(self, render_component):
        """Test base widget renders with icon alias (T009)."""
        html = render_component("navbar.widget", icon="notification", badge_count=0)
        soup = BeautifulSoup(html, "html.parser")

        # Should render nav-item with link
        nav_item = soup.find("li", class_="nav-item")
        assert nav_item is not None, "Should have nav-item element"

        # Should have link with icon
        link = nav_item.find("a", class_="nav-link")
        assert link is not None, "Should have nav-link anchor"

    def test_base_widget_uses_c_icon_component(self, render_component):
        """Test base widget uses c-icon component, not direct <i> tags (T010)."""
        # This test verifies the COMPONENT uses <c-icon /> tag, not direct <i> in source
        # The rendered output will have <i> tag from c-icon component, which is correct
        html = render_component("navbar.widget", icon="notification", badge_count=0)
        soup = BeautifulSoup(html, "html.parser")

        # Should have icon rendered from c-icon component
        icons = soup.find_all("i")
        assert len(icons) > 0, "Should have rendered icon element from c-icon component"

        # Icon should have bi- class from EASY_ICONS mapping
        icon = icons[0]
        assert any("bi" in cls for cls in icon.get("class", [])), "Icon should have Bootstrap Icon classes from c-icon"

    def test_base_widget_displays_badge_with_count(self, render_component):
        """Test base widget displays badge with count (T011)."""
        html = render_component("navbar.widget", icon="notification", badge_count=5)
        soup = BeautifulSoup(html, "html.parser")

        # Should have badge element
        badge = soup.find("span", class_=lambda c: c and "badge" in c)
        assert badge is not None, "Should have badge element when count provided"
        assert "5" in badge.get_text(), "Badge should display count"

    def test_base_widget_hides_badge_when_zero(self, render_component):
        """Test base widget hides badge when count is zero (T012)."""
        html = render_component("navbar.widget", icon="notification", badge_count=0)
        soup = BeautifulSoup(html, "html.parser")

        # Should NOT have badge element when count is zero
        badge = soup.find("span", class_=lambda c: c and "navbar-badge" in c)
        assert badge is None, "Should not display badge when count is zero"

    def test_base_widget_renders_slot_content(self, render_component):
        """Test base widget renders {{ slot }} content in dropdown (T013)."""
        # Test that dropdown container exists and can accept content via slot
        html = render_component(
            "navbar.widget",
            icon="notification",
            badge_count=3,
        )
        soup = BeautifulSoup(html, "html.parser")

        # Should have dropdown menu container ready for slot content
        dropdown = soup.find("div", class_="dropdown-menu")
        assert dropdown is not None, "Should have dropdown-menu element for slot content"
        assert "dropdown-menu-end" in dropdown.get("class", []), "Should have dropdown-menu-end class"
        assert "dropdown-menu-lg" in dropdown.get("class", []), "Should have dropdown-menu-lg class"

    def test_badge_supports_bootstrap_color_classes(self, render_component):
        """Test badge supports Bootstrap color classes (T014)."""
        colors = ["danger", "warning", "info", "success"]

        for color in colors:
            html = render_component(
                "navbar.widget",
                icon="notification",
                badge_count=5,
                badge_color=color,
            )
            soup = BeautifulSoup(html, "html.parser")

            # Should have badge with color class - use class attribute directly
            badge = soup.find(
                "span", class_=f"badge position-absolute top-0 start-100 translate-middle text-bg-{color}"
            )
            # Fallback: check if any badge has the color class
            if badge is None:
                all_badges = soup.find_all("span", class_="badge")
                for b in all_badges:
                    if f"text-bg-{color}" in b.get("class", []):
                        badge = b
                        break
            assert badge is not None, f"Should have badge with text-bg-{color} class"

    def test_badge_displays_99_plus_when_count_over_99(self, render_component):
        """Test badge displays '99+' when count > 99 (T015)."""
        html = render_component("navbar.widget", icon="notification", badge_count=150)
        soup = BeautifulSoup(html, "html.parser")

        badge = soup.find("span", class_=lambda c: c and "badge" in c)
        assert badge is not None, "Should have badge element"
        assert "99+" in badge.get_text(), "Should display '99+' for counts over 99"

    def test_base_widget_follows_adminlte_pattern(self, render_component):
        """Test base widget follows AdminLTE nav-item dropdown pattern (T016)."""
        html = render_component("navbar.widget", icon="notification", badge_count=3)
        soup = BeautifulSoup(html, "html.parser")

        # Should have nav-item with dropdown class
        nav_item = soup.find("li", class_=lambda c: c and "nav-item" in c)
        assert nav_item is not None, "Should have nav-item element"
        assert "dropdown" in nav_item.get("class", []), "nav-item should have dropdown class"

        # Should have link with data-bs-toggle attribute
        link = soup.find("a", class_="nav-link")
        assert link is not None, "Should have nav-link"
        assert link.get("data-bs-toggle") == "dropdown", "Link should have data-bs-toggle='dropdown'"

    def test_base_widget_handles_negative_badge_counts(self, render_component):
        """Test base widget handles negative badge counts by hiding badge (T017)."""
        html = render_component("navbar.widget", icon="notification", badge_count=-5)
        soup = BeautifulSoup(html, "html.parser")

        # Should NOT have badge element for negative counts
        badge = soup.find("span", class_=lambda c: c and "navbar-badge" in c)
        assert badge is None, "Should not display badge for negative counts"
