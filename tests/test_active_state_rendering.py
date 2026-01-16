"""Test active state rendering in actual HTML output."""

import pytest
from django.test import RequestFactory
from flex_menu import MenuItem
from flex_menu.templatetags.flex_menu import render_menu


@pytest.mark.django_db
class TestActiveStateRendering:
    """Test that active state is properly rendered in HTML."""

    def test_active_class_appears_in_rendered_html(self, app_menu):
        """Verify active class is applied to menu items in rendered HTML."""
        rf = RequestFactory()

        # Create menu item
        MenuItem(
            name="current_page",
            view_name="dashboard",
            extra_context={"label": "Dashboard", "icon": "house"},
            parent=app_menu,
        )

        # Create request matching the menu item
        request = rf.get("/")
        request.resolver_match = type("obj", (object,), {"view_name": "dashboard", "url_name": "dashboard"})()

        # Render menu
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        print("\n=== Rendered HTML ===")
        print(output)
        print("=== End HTML ===\n")

        # Check for active class
        assert "Dashboard" in output, "Menu label should be in output"
        assert "active" in output, "Active class should be applied"
        assert (
            'class="nav-link active"' in output or "nav-link active" in output
        ), "Active class should be on nav-link element"

    def test_inactive_item_has_no_active_class(self, app_menu):
        """Verify inactive items don't have active class."""
        rf = RequestFactory()

        # Create menu item with URL (not view_name to avoid reverse resolution)
        MenuItem(
            name="other_page",
            url="/other/",
            extra_context={"label": "Other Page", "icon": "circle"},
            parent=app_menu,
        )

        # Create request for different page (dashboard)
        request = rf.get("/")
        request.resolver_match = type("obj", (object,), {"view_name": "dashboard", "url_name": "dashboard"})()

        # Render menu
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # The menu item should render since we're using URL not view_name
        assert "Other Page" in output, "Menu label should be in output"

        # Extract the HTML around "Other Page" and verify no active class nearby
        idx = output.find("Other Page")
        snippet = output[max(0, idx - 200) : idx + 100]

        # The nav-link before "Other Page" should not have active class
        # Look backwards from "Other Page" to find the nav-link
        link_start = snippet.rfind("<a", 0, len(snippet) - (len(output) - idx))
        if link_start != -1:
            link_html = snippet[link_start : len(snippet) - (len(output) - idx) + 50]
            # This specific link should not be active
            assert not ('class="nav-link active"' in link_html or "nav-link active" in link_html)
