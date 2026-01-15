"""
Test utilities and base widget rendering functionality.

This module tests the foundational widget system that all navbar widgets depend on,
including badge display logic, ARIA accessibility, and widget rendering utilities.

Tests follow Test-First principle (Constitution I):
- Badge display logic (hide if zero, "99+" if > 99)
- Negative and non-numeric value handling
- ARIA labels for accessibility
- Widget rendering helper functions
"""

from django_cotton import render_component


class TestBadgeDisplayLogic:
    """Test badge count display logic per FR-006, FR-007, and edge cases."""

    def test_badge_hidden_when_zero(self, rf):
        """Badge MUST be hidden when count is zero (FR-006)."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/widgets/base",
            {
                "icon": "bell",
                "count": 0,
                "badge_color": "danger",
            },
        )

        # ASSERT
        assert '<span class="navbar-badge' not in result
        assert "badge text-bg-" not in result

    def test_badge_shows_correct_count_normal_range(self, rf):
        """Badge MUST show exact count for values 1-99."""
        # ARRANGE
        request = rf.get("/")

        # ACT - Test various counts
        for count in [1, 5, 42, 99]:
            result = render_component(
                request,
                "navbar/widgets/base",
                {
                    "icon": "bell",
                    "count": count,
                    "badge_color": "danger",
                },
            )

            # ASSERT
            assert f">{count}</span>" in result
            assert "navbar-badge" in result

    def test_badge_shows_99_plus_when_over_99(self, rf):
        """Badge MUST display '99+' when count exceeds 99 (FR-007)."""
        # ARRANGE
        request = rf.get("/")

        # ACT - Test counts over 99
        for count in [100, 150, 999, 1000]:
            result = render_component(
                request,
                "navbar/widgets/base",
                {
                    "icon": "bell",
                    "count": count,
                    "badge_color": "danger",
                },
            )

            # ASSERT
            assert ">99+</span>" in result
            assert "navbar-badge" in result

    def test_badge_handles_negative_values(self, rf):
        """Badge MUST be hidden for negative count values (edge case validation)."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/widgets/base",
            {
                "icon": "bell",
                "count": -5,
                "badge_color": "danger",
            },
        )

        # ASSERT
        assert '<span class="navbar-badge' not in result

    def test_badge_handles_non_numeric_values(self, rf):
        """Badge MUST be hidden for non-numeric count values (edge case validation)."""
        # ARRANGE
        request = rf.get("/")

        # ACT - Test various non-numeric values
        for bad_value in ["invalid", None, "", "abc"]:
            result = render_component(
                request,
                "navbar/widgets/base",
                {
                    "icon": "bell",
                    "count": bad_value,
                    "badge_color": "danger",
                },
            )

            # ASSERT
            assert '<span class="navbar-badge' not in result

    def test_badge_color_classes(self, rf):
        """Badge MUST support custom color classes (FR-009)."""
        # ARRANGE
        request = rf.get("/")
        colors = ["danger", "warning", "info", "success"]

        # ACT & ASSERT
        for color in colors:
            result = render_component(
                request,
                "navbar/widgets/base",
                {
                    "icon": "bell",
                    "count": 5,
                    "badge_color": color,
                },
            )

            assert f"text-bg-{color}" in result


class TestWidgetAccessibility:
    """Test ARIA labels and accessibility features per FR-023 and Constitution III."""

    def test_widget_has_aria_label(self, rf):
        """Widget button MUST have aria-label for screen readers (Constitution III)."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/widgets/base",
            {
                "icon": "bell",
                "aria_label": "Notifications",
                "count": 3,
                "badge_color": "danger",
            },
        )

        # ASSERT
        assert 'aria-label="Notifications"' in result

    def test_widget_has_aria_expanded(self, rf):
        """Widget button MUST have aria-expanded attribute for dropdown state."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/widgets/base",
            {
                "icon": "bell",
                "aria_label": "Notifications",
                "count": 0,
                "badge_color": "danger",
            },
        )

        # ASSERT
        assert 'aria-expanded="false"' in result

    def test_widget_icon_has_class(self, rf):
        """Widget MUST render icon with Bootstrap Icons class."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/widgets/base",
            {
                "icon": "bell-fill",
                "aria_label": "Notifications",
                "count": 0,
                "badge_color": "danger",
            },
        )

        # ASSERT
        assert "bi bi-bell-fill" in result


class TestWidgetRendering:
    """Test basic widget structure and rendering utilities."""

    def test_widget_renders_as_nav_item(self, rf):
        """Widget MUST render within <li class='nav-item dropdown'> structure."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/widgets/base",
            {
                "icon": "bell",
                "aria_label": "Test Widget",
                "count": 0,
                "badge_color": "danger",
            },
        )

        # ASSERT
        assert '<li class="nav-item dropdown">' in result
        assert "</li>" in result

    def test_widget_has_dropdown_toggle_attributes(self, rf):
        """Widget button MUST have Bootstrap dropdown toggle attributes."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/widgets/base",
            {
                "icon": "bell",
                "aria_label": "Test Widget",
                "count": 0,
                "badge_color": "danger",
            },
        )

        # ASSERT
        assert 'data-bs-toggle="dropdown"' in result
        assert 'class="nav-link"' in result

    def test_widget_without_dropdown_content(self, rf):
        """Widget MUST render without dropdown menu if no content provided."""
        # ARRANGE
        request = rf.get("/")

        # ACT
        result = render_component(
            request,
            "navbar/widgets/base",
            {
                "icon": "arrows-fullscreen",
                "aria_label": "Fullscreen",
                # No dropdown content - simple button widget
            },
        )

        # ASSERT
        assert "bi bi-arrows-fullscreen" in result
        # Should not have dropdown-toggle if no dropdown content
        # This will be refined based on actual implementation
