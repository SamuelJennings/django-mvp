"""Tests for Custom Widget component."""

from django_cotton import render_component


class TestCustomWidgetWithBadge:
    """Test custom widget with icon and badge."""

    def test_custom_widget_renders_icon(self, rf):
        """Custom widget should render the provided icon."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/custom_widget",
            {
                "icon": "bi-tasks",
                "dropdown_id": "tasks-dropdown",
            },
        )
        assert 'class="bi bi-tasks"' in html

    def test_custom_widget_renders_badge(self, rf):
        """Custom widget should render badge when count provided."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/custom_widget",
            {
                "icon": "bi-tasks",
                "badge_count": 5,
                "dropdown_id": "tasks-dropdown",
            },
        )
        assert 'class="navbar-badge badge text-bg-danger"' in html
        assert "5" in html
        assert "navbar-badge" in html

    def test_custom_widget_badge_over_99(self, rf):
        """Custom widget should display 99+ when count exceeds 99."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/custom_widget",
            {
                "icon": "bi-tasks",
                "badge_count": 150,
                "dropdown_id": "tasks-dropdown",
            },
        )
        assert "99+" in html
        assert "150" not in html  # Should show 99+ not actual count


class TestCustomWidgetDropdown:
    """Test custom widget dropdown slot functionality."""

    def test_custom_widget_dropdown_slot(self, rf):
        """Custom widget should render dropdown content from children."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/custom_widget",
            {
                "icon": "bi-tasks",
                "dropdown_id": "tasks-dropdown",
                "children": "<span>Task 1</span><span>Task 2</span>",
            },
        )
        assert "<span>Task 1</span>" in html
        assert "<span>Task 2</span>" in html
        assert 'id="tasks-dropdown"' in html

    def test_custom_widget_dropdown_classes(self, rf):
        """Custom widget should apply dropdown classes correctly."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/custom_widget",
            {
                "icon": "bi-tasks",
                "dropdown_id": "tasks-dropdown",
            },
        )
        assert 'class="dropdown-menu dropdown-menu-lg dropdown-menu-end"' in html


class TestCustomWidgetBadgeColors:
    """Test badge color customization."""

    def test_custom_widget_default_badge_color(self, rf):
        """Custom widget should use danger (red) badge by default."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/custom_widget",
            {
                "icon": "bi-tasks",
                "badge_count": 3,
                "dropdown_id": "tasks-dropdown",
            },
        )
        assert "text-bg-danger" in html

    def test_custom_widget_custom_badge_color(self, rf):
        """Custom widget should accept custom badge color."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/custom_widget",
            {
                "icon": "bi-tasks",
                "badge_count": 3,
                "badge_color": "warning",
                "dropdown_id": "tasks-dropdown",
            },
        )
        assert "text-bg-warning" in html
        assert "text-bg-danger" not in html


class TestCustomWidgetWithoutBadge:
    """Test custom widget without badge."""

    def test_custom_widget_no_badge_when_count_zero(self, rf):
        """Custom widget should not render badge when count is 0."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/custom_widget",
            {
                "icon": "bi-tasks",
                "badge_count": 0,
                "dropdown_id": "tasks-dropdown",
            },
        )
        assert "navbar-badge" not in html

    def test_custom_widget_no_badge_when_not_provided(self, rf):
        """Custom widget should not render badge when count not provided."""
        request = rf.get("/")
        html = render_component(
            request,
            "navbar/widgets/custom_widget",
            {
                "icon": "bi-tasks",
                "dropdown_id": "tasks-dropdown",
            },
        )
        assert "navbar-badge" not in html
