"""Tests for custom AdminLTE renderer logic.

Tests cover:
- Active state detection based on URL comparison
- Menu-open class for parents with active children
- Request context handling in renderer
"""

from django.urls import resolve
from flex_menu import MenuItem

from mvp.renderers import AdminLTERenderer


class TestActiveStateDetection:
    """Test active state detection compares request URL with view_name."""

    def test_active_state_detection_matches_view_name(self, app_menu, rf):
        """T040: Active state should match when request URL equals item view_name resolution."""
        from django.urls import resolve

        # Create a MenuItem with a view_name that can be reversed
        item = MenuItem(
            name="dashboard",
            view_name="dashboard",
            extra_context={"label": "Dashboard"},
            parent=app_menu,
        )

        # Create request matching the dashboard URL
        request = rf.get("/")  # dashboard URL from example/urls.py
        request.resolver_match = resolve("/")

        renderer = AdminLTERenderer()
        context = renderer.get_context_data(item, request=request)

        # Should detect this as active
        assert context.get("is_active") is True

    def test_inactive_state_when_urls_dont_match(self, app_menu, rf):
        """T040: Should not be active when request URL differs from view_name."""
        item = MenuItem(
            name="profile",
            view_name="profile",
            extra_context={"label": "Profile"},
            parent=app_menu,
        )

        # Create request for different URL
        request = rf.get("/")  # Different from profile URL
        request.resolver_match = resolve("/")

        renderer = AdminLTERenderer()
        context = renderer.get_context_data(item, request=request)

        # Should not be active
        assert context.get("is_active") is False

    def test_active_state_with_url_attribute(self, app_menu, rf):
        """T040: Active state should work with URL attribute when view_name is not available."""
        item = MenuItem(
            name="external",
            url="/external/",
            extra_context={"label": "External"},
            parent=app_menu,
        )

        # Create request matching the URL
        request = rf.get("/external/")

        renderer = AdminLTERenderer()
        context = renderer.get_context_data(item, request=request)

        # Should detect this as active
        assert context.get("is_active") is True


class TestActiveClassApplication:
    """Test active class applied to current menu item."""

    def test_active_class_applied_to_single_item(self, app_menu):
        """T041: Active menu item should have 'active' class applied."""
        item = MenuItem(
            name="current",
            url="/current/",
            extra_context={"label": "Current Page"},
            parent=app_menu,
        )

        renderer = AdminLTERenderer()
        # Mock request context for current page
        mock_request = type("MockRequest", (), {"path": "/current/"})()

        context = renderer.get_context_data(item, request=mock_request)

        # Should include active in CSS classes
        item_classes = context.get("item_classes", "")
        assert "active" in item_classes or context.get("is_active")

    def test_no_active_class_for_inactive_item(self, app_menu):
        """T041: Non-active menu items should not have 'active' class."""
        item = MenuItem(
            name="other",
            url="/other/",
            extra_context={"label": "Other Page"},
            parent=app_menu,
        )

        renderer = AdminLTERenderer()
        # Mock request for different page
        mock_request = type("MockRequest", (), {"path": "/current/"})()

        context = renderer.get_context_data(item, request=mock_request)

        # Should not have active class
        item_classes = context.get("item_classes", "")
        assert "active" not in item_classes
        assert not context.get("is_active")


class TestMenuOpenForParents:
    """Test menu-open class applied to parent with active child."""

    def test_parent_with_active_child_gets_menu_open(self, app_menu, rf):
        """T042: Parent item should have 'menu-open' class when child is active."""
        # Create parent item
        parent_item = MenuItem(
            name="admin",
            extra_context={"label": "Administration"},
            parent=app_menu,
        )

        # Create child item that will be active
        MenuItem(
            name="users",
            url="/admin/users/",
            extra_context={"label": "Users"},
            parent=parent_item,
        )

        # Mock request for child URL
        request = rf.get("/admin/users/")

        renderer = AdminLTERenderer()
        context = renderer.get_context_data(parent_item, request=request)

        # Parent should be marked as having active descendant
        assert context.get("is_open") is True or context.get("has_active_child")

    def test_parent_without_active_child_no_menu_open(self, app_menu, rf):
        """T042: Parent without active children should not have 'menu-open' class."""
        # Create parent item
        parent_item = MenuItem(
            name="tools",
            extra_context={"label": "Tools"},
            parent=app_menu,
        )

        # Create child items that won't be active
        MenuItem(
            name="import",
            url="/tools/import/",
            extra_context={"label": "Import"},
            parent=parent_item,
        )

        MenuItem(
            name="export",
            url="/tools/export/",
            extra_context={"label": "Export"},
            parent=parent_item,
        )

        # Mock request for different URL
        request = rf.get("/dashboard/")

        renderer = AdminLTERenderer()
        context = renderer.get_context_data(parent_item, request=request)

        # Parent should not be marked as open
        assert not context.get("is_open")
        assert not context.get("has_active_child")

    def test_nested_active_detection(self, app_menu, rf):
        """T042: Should detect active descendants at any depth."""
        # Create nested structure: Admin > Users > Roles
        admin_item = MenuItem(
            name="admin",
            extra_context={"label": "Administration"},
            parent=app_menu,
        )

        users_item = MenuItem(
            name="users",
            extra_context={"label": "Users"},
            parent=admin_item,
        )

        MenuItem(
            name="roles",
            url="/admin/users/roles/",
            extra_context={"label": "Roles"},
            parent=users_item,
        )

        # Request for deeply nested URL
        request = rf.get("/admin/users/roles/")

        renderer = AdminLTERenderer()

        # Both parent levels should detect active descendant
        admin_context = renderer.get_context_data(admin_item, request=request)
        users_context = renderer.get_context_data(users_item, request=request)

        assert admin_context.get("is_open") is True or admin_context.get("has_active_child")
        assert users_context.get("is_open") is True or users_context.get("has_active_child")
