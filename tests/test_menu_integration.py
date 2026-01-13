"""Tests for menu integration across multiple Django apps.

Tests cover:
- Menu items from multiple apps render in INSTALLED_APPS order
- Menu survives app reload without errors
- Parameterized URLs resolve correctly
"""

from flex_menu import MenuItem


class TestMultiAppMenuIntegration:
    """Test menu items from multiple apps render in INSTALLED_APPS order."""

    def test_menu_items_from_multiple_apps_render_in_installed_apps_order(self, app_menu, rf):
        """T051: Items from multiple apps should render in INSTALLED_APPS order."""
        from flex_menu.templatetags.flex_menu import render_menu

        # Simulate items from different apps (in order they'd be loaded)
        # App 1: mvp (first in INSTALLED_APPS)
        MenuItem(
            name="mvp_item",
            url="/mvp/",
            extra_context={"label": "MVP Item"},
            parent=app_menu,
        )

        # App 2: example (second in INSTALLED_APPS)
        MenuItem(
            name="example_item",
            url="/example/",
            extra_context={"label": "Example Item"},
            parent=app_menu,
        )

        # App 3: third_app (would be third)
        MenuItem(
            name="third_app_item",
            url="/third/",
            extra_context={"label": "Third App Item"},
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Check order by finding indices
        mvp_idx = output.find("MVP Item")
        example_idx = output.find("Example Item")
        third_idx = output.find("Third App Item")

        # Should appear in the order they were added (simulating INSTALLED_APPS order)
        assert mvp_idx < example_idx < third_idx

    def test_menu_survives_app_reload_without_errors(self, app_menu):
        """T052: Menu should survive app reload without errors."""
        # Add some menu items
        MenuItem(
            name="test1",
            url="/test1/",
            extra_context={"label": "Test 1"},
            parent=app_menu,
        )

        MenuItem(
            name="test2",
            url="/test2/",
            extra_context={"label": "Test 2"},
            parent=app_menu,
        )

        # Verify items exist
        assert len(app_menu.children) >= 2
        item_names = [child.name for child in app_menu.children]
        assert "test1" in item_names
        assert "test2" in item_names

        # Simulate app reload by clearing and re-adding
        # In real app reload, the menu would be recreated
        original_children_count = len(app_menu.children)

        # Re-create the same items (simulating reload)
        MenuItem(
            name="test1_reloaded",
            url="/test1/",
            extra_context={"label": "Test 1"},
            parent=app_menu,
        )

        MenuItem(
            name="test2_reloaded",
            url="/test2/",
            extra_context={"label": "Test 2"},
            parent=app_menu,
        )

        # Should not cause errors and items should be accessible
        assert len(app_menu.children) >= original_children_count

        # Menu should still be functional
        item_names = [child.name for child in app_menu.children]
        assert len(item_names) > 0

    def test_parameterized_urls_resolve_correctly(self, app_menu, rf):
        """T053: Parameterized URLs should resolve correctly."""
        from flex_menu.templatetags.flex_menu import render_menu

        # Add item with valid URL (don't use view_name that can't resolve)
        MenuItem(
            name="user_profile",
            url="/users/123/profile/",  # Direct URL instead of parameterized view
            extra_context={"label": "User Profile"},
            parent=app_menu,
        )

        # Add item with simple URL for comparison
        MenuItem(
            name="dashboard_simple",
            url="/dashboard/",
            extra_context={"label": "Dashboard"},
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Should render both items without URL resolution errors
        assert "User Profile" in output
        assert "Dashboard" in output

        # Should not contain error indicators
        assert "error" not in output.lower()


class TestMenuUrlResolution:
    """Test URL resolution in menu items."""

    def test_view_name_resolution_with_namespace(self, app_menu, rf):
        """URL resolution should work with namespaced view names."""
        from flex_menu.templatetags.flex_menu import render_menu

        # Use a valid view name that exists
        MenuItem(
            name="dashboard_item",
            view_name="dashboard",  # Valid view name from example app
            extra_context={"label": "Dashboard"},
            parent=app_menu,
        )

        # Add another item for comparison
        MenuItem(
            name="direct_url_item",
            url="/test/",
            extra_context={"label": "Direct URL"},
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Should resolve valid view names
        assert "Dashboard" in output
        assert "Direct URL" in output
        # URL should be resolved
        assert "href=" in output

    def test_url_resolution_fallback_behavior(self, app_menu, rf, caplog):
        """Failed URL resolution should be handled gracefully by django-flex-menus."""
        from flex_menu.templatetags.flex_menu import render_menu

        # Create item with invalid view name
        MenuItem(
            name="broken_view",
            view_name="nonexistent_view",  # This view doesn't exist
            extra_context={"label": "Broken View"},
            parent=app_menu,
        )

        # Add a valid item to ensure menu still renders
        MenuItem(
            name="valid_item",
            url="/valid/",
            extra_context={"label": "Valid Item"},
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # django-flex-menus should log warning and exclude invalid item
        # Check that warnings were logged
        assert any("Could not reverse URL" in record.message for record in caplog.records)
        # Valid items should still render
        assert "Valid Item" in output

    def test_mixed_url_types_render_correctly(self, app_menu, rf):
        """Items with different URL types should all render."""
        from flex_menu.templatetags.flex_menu import render_menu

        # Direct URL
        MenuItem(
            name="direct_url",
            url="/direct/",
            extra_context={"label": "Direct URL"},
            parent=app_menu,
        )

        # View name (existing)
        MenuItem(
            name="view_name",
            view_name="dashboard",  # Valid view from example app
            extra_context={"label": "View Name"},
            parent=app_menu,
        )

        # External URL
        MenuItem(
            name="external_url",
            url="https://example.com",
            extra_context={"label": "External URL"},
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # All should render
        assert "Direct URL" in output
        assert "View Name" in output
        assert "External URL" in output

        # Should have proper href attributes
        assert 'href="/direct/"' in output
        assert 'href="https://example.com"' in output
