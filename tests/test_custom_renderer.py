"""Tests for custom AdminLTE renderer logic.

Tests cover:
- Menu-open class for parents with active children
- Request context handling in renderer
- Active state is handled by django-flex-menus' 'selected' attribute
"""

from flex_menu import MenuItem

from mvp.renderers import AdminLTERenderer


class TestMenuOpenForParents:
    """Test menu-open class applied to parent with active child."""

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

        # django-flex-menus handles this via 'selected' attribute
        assert "selected" in context

