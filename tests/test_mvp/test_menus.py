"""Tests for mvp-specific menu functionality.

This module tests mvp's custom menu features, NOT django-flex-menus core functionality.

Tests cover:
- MenuGroup subclass behavior (component_type injection, url="#")
- MenuCollapse subclass behavior (component_type injection, url="#")
- Badge rendering in AdminLTE renderer (mvp-specific feature)

Note: We do NOT test:
- flex-menus Menu/MenuItem creation (library's responsibility)
- flex-menus render_menu templatetag (library's responsibility)
- flex-menus parent/child relationships (library's responsibility)
- URL resolution (Django + flex-menus responsibility)
"""

import pytest
from flex_menu import MenuItem


@pytest.mark.django_db
class TestMenuGroupSubclass:
    """Test mvp.menus.MenuGroup subclass behavior."""

    def test_menu_group_injects_component_type(self, app_menu):
        """MenuGroup should inject component_type='menu.group' into extra_context."""
        from mvp.menus import MenuGroup

        group = MenuGroup(
            name="admin_section",
            extra_context={"label": "ADMINISTRATION"},
            parent=app_menu,
        )

        assert group.extra_context["component_type"] == "menu.group"
        assert group.extra_context["label"] == "ADMINISTRATION"

    def test_menu_group_sets_url_to_hash(self, app_menu):
        """MenuGroup should set url='#' to prevent navigation."""
        from mvp.menus import MenuGroup

        group = MenuGroup(
            name="section_header",
            extra_context={"label": "SECTION"},
            parent=app_menu,
        )

        assert group.extra_context.get("url") == "#"


@pytest.mark.django_db
class TestMenuCollapseSubclass:
    """Test mvp.menus.MenuCollapse subclass behavior."""

    def test_menu_collapse_injects_component_type(self, app_menu):
        """MenuCollapse should inject component_type='menu.collapse' into extra_context."""
        from mvp.menus import MenuCollapse

        collapse = MenuCollapse(
            name="reports",
            extra_context={"label": "Reports", "icon": "chart-bar"},
            parent=app_menu,
        )

        assert collapse.extra_context["component_type"] == "menu.collapse"
        assert collapse.extra_context["label"] == "Reports"
        assert collapse.extra_context["icon"] == "chart-bar"

    def test_menu_collapse_sets_url_to_hash(self, app_menu):
        """MenuCollapse should set url='#' to prevent navigation."""
        from mvp.menus import MenuCollapse

        collapse = MenuCollapse(
            name="dropdown",
            extra_context={"label": "Dropdown"},
            parent=app_menu,
        )

        assert collapse.extra_context.get("url") == "#"


@pytest.mark.django_db
class TestAdminLTEBadgeRendering:
    """Test AdminLTE renderer badge support (mvp-specific feature)."""

    def test_badge_renders_with_custom_classes(self, app_menu, rf):
        """Badge should render when specified in extra_context with custom classes."""
        from flex_menu.templatetags.flex_menu import render_menu

        MenuItem(
            name="notifications",
            url="/notifications/",
            extra_context={
                "label": "Notifications",
                "badge": "5",
                "badge_classes": "text-bg-danger",
            },
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Should contain badge content
        assert "5" in output
        # Should apply badge classes
        assert "text-bg-danger" in output or "badge" in output

    def test_badge_renders_with_text_content(self, app_menu, rf):
        """Badge should support text content with Bootstrap 5 classes."""
        from flex_menu.templatetags.flex_menu import render_menu

        MenuItem(
            name="messages",
            url="/messages/",
            extra_context={
                "label": "Messages",
                "badge": "New",
                "badge_classes": "text-bg-success nav-badge",
            },
            parent=app_menu,
        )

        request = rf.get("/")
        output = render_menu({"request": request}, "AppMenu", renderer="adminlte")

        # Should contain badge text
        assert "New" in output
        # Should apply custom classes
        assert "text-bg-success" in output or "nav-badge" in output
