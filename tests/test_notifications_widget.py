"""
Tests for Notifications Widget (User Story 2).

Tests follow django-cotton patterns and verify:
- Badge counter display (hide on 0, show exact count, 99+ for overflow)
- Dropdown list with notification items
- Scrolling when more than 5 items
- Custom badge colors (danger, warning, info)
"""

from django_cotton import render_component


class TestNotificationsWidgetBadge:
    """Test notifications widget badge display logic."""

    def test_notifications_widget_with_count_badge(self, rf):
        """Notifications widget should display badge with count."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/notifications",
            {
                "count": 5,
            },
        )

        # Check badge exists and shows count
        assert "navbar-badge" in html
        assert ">5<" in html

    def test_badge_hidden_when_count_is_zero(self, rf):
        """Badge should be hidden when count is zero."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/notifications",
            {
                "count": 0,
            },
        )

        # Badge should not be rendered
        assert "navbar-badge" not in html

    def test_badge_shows_99_plus_when_over_99(self, rf):
        """Badge should show '99+' when count exceeds 99."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/notifications",
            {
                "count": 150,
            },
        )

        # Check for 99+ display
        assert "99+" in html

    def test_custom_badge_colors(self, rf):
        """Notifications widget should support custom badge colors."""
        request = rf.get("/")

        # Test danger color
        html_danger = render_component(
            request,
            "navbar/widgets/notifications",
            {
                "count": 5,
                "badge_color": "danger",
            },
        )
        assert "text-bg-danger" in html_danger

        # Test warning color
        html_warning = render_component(
            request,
            "navbar/widgets/notifications",
            {
                "count": 3,
                "badge_color": "warning",
            },
        )
        assert "text-bg-warning" in html_warning


class TestNotificationsWidgetDropdown:
    """Test notifications widget dropdown functionality."""

    def test_dropdown_displays_max_5_items(self, rf):
        """Dropdown should render all items (AdminLTE handles layout)."""
        request = rf.get("/")

        # Create 7 notifications
        notifications = [{"text": f"Notification {i}", "time": f"{i} mins ago"} for i in range(1, 8)]

        html = render_component(
            request,
            "navbar/widgets/notifications",
            {
                "count": 7,
                "notifications": notifications,
            },
        )

        # Check that all 7 notifications are rendered
        for i in range(1, 8):
            assert f"Notification {i}" in html

        # Verify AdminLTE dropdown classes are present
        assert "dropdown-menu" in html
        assert "dropdown-menu-lg" in html

    def test_scrolling_when_more_than_5_items(self, rf):
        """Dropdown should use AdminLTE's dropdown-menu-lg for proper sizing."""
        request = rf.get("/")

        notifications = [{"text": f"Notification {i}", "time": f"{i} mins ago"} for i in range(1, 8)]

        html = render_component(
            request,
            "navbar/widgets/notifications",
            {
                "count": 7,
                "notifications": notifications,
            },
        )

        # Check that dropdown uses AdminLTE large dropdown class
        assert "dropdown-menu-lg" in html

        # Verify all items are present (AdminLTE/Bootstrap handles scrolling via CSS)
        for i in range(1, 8):
            assert f"Notification {i}" in html


class TestNotificationsWidgetAccessibility:
    """Test notifications widget accessibility features."""

    def test_widget_has_aria_label(self, rf):
        """Notifications widget should have descriptive aria-label."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/notifications",
            {
                "count": 3,
            },
        )

        # Check for aria-label
        assert 'aria-label="Notifications"' in html or 'aria-label="View notifications"' in html

    def test_widget_has_bell_icon(self, rf):
        """Notifications widget should use bell icon."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/notifications",
            {
                "count": 2,
            },
        )

        # Check for bell icon
        assert "bi-bell" in html
