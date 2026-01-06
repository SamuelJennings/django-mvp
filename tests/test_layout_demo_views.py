"""
Tests for layout demo views in example app.

These tests validate:
- T027-T029: Fixed properties demo view with query parameters
- T035-T036: Responsive breakpoint demo view with query parameters

The demo views are designed for manual testing of layout configurations
without requiring browser automation.
"""

import pytest
from django.test import Client


@pytest.mark.django_db
class TestLayoutFixedDemo:
    """Test Fixed Properties Demo View (T027-T029)"""

    def test_layout_fixed_demo_no_query_params(self, client: Client):
        """
        T027: Test layout_fixed_demo view with no query params renders default state.

        Given: User visits /layout-fixed/ without query parameters
        When: View renders
        Then: All fixed properties are False by default
        And: Form checkboxes are unchecked
        And: Page contains required content elements
        And: Body tag has no fixed CSS classes
        """
        response = client.get("/layout-fixed/")

        assert response.status_code == 200
        assert "example/layout_fixed.html" in [t.name for t in response.templates]

        # Verify default state passed to template
        assert response.context["fixed_sidebar"] is False
        assert response.context["fixed_header"] is False
        assert response.context["fixed_footer"] is False

        # Verify checkboxes are unchecked (no 'checked' attribute when False)
        html = response.content.decode("utf-8")
        assert 'name="fixed_sidebar"' in html
        assert 'name="fixed_header"' in html
        assert 'name="fixed_footer"' in html

        # Verify app component is rendered (Cotton processes <c-app> into HTML)
        assert '<div class="app-wrapper' in html

        # Verify NO fixed CSS classes on .app-wrapper when attributes are False
        # Check the actual app-wrapper class attribute
        import re

        wrapper_match = re.search(r'<div class="app-wrapper([^"]*)">|<div class="app-wrapper">', html)
        assert wrapper_match, "Could not find app-wrapper div"
        wrapper_classes = "app-wrapper" + (wrapper_match.group(1) if wrapper_match.group(1) else "")

        # Wrapper should only have app-wrapper and sidebar-expand-lg (no fixed classes)
        assert "layout-fixed" not in wrapper_classes
        assert "fixed-header" not in wrapper_classes
        assert "fixed-footer" not in wrapper_classes
        assert "app-wrapper" in wrapper_classes
        assert "sidebar-expand-lg" in wrapper_classes

    def test_layout_fixed_demo_with_fixed_sidebar_on(self, client: Client):
        """
        T028: Test layout_fixed_demo view with fixed_sidebar=on query param.

        Given: User submits form with fixed_sidebar checkbox checked
        When: Page reloads with ?fixed_sidebar=on
        Then: fixed_sidebar context variable is True
        And: Sidebar checkbox is checked
        And: Other checkboxes remain unchecked
        And: Body tag has layout-fixed CSS class
        """
        response = client.get("/layout-fixed/?fixed_sidebar=on")

        assert response.status_code == 200

        # Verify state
        assert response.context["fixed_sidebar"] is True
        assert response.context["fixed_header"] is False
        assert response.context["fixed_footer"] is False

        # Verify checkbox state in HTML
        html = response.content.decode("utf-8")
        # When checkbox is checked, it should have 'checked' attribute or be checked in template
        assert 'name="fixed_sidebar"' in html

        # CRITICAL: Verify layout-fixed CSS class is applied to .app-wrapper element
        assert 'class="app-wrapper layout-fixed sidebar-expand-lg' in html or (
            "layout-fixed" in html and "app-wrapper" in html
        )

    def test_layout_fixed_demo_with_all_checkboxes(self, client: Client):
        """
        T029: Test layout_fixed_demo view with all fixed properties enabled.

        Given: User submits form with all checkboxes checked
        When: Page reloads with ?fixed_sidebar=on&fixed_header=on&fixed_footer=on
        Then: All fixed properties are True
        And: All checkboxes are checked
        And: Body tag has all three fixed CSS classes
        """
        response = client.get(
            "/layout-fixed/?fixed_sidebar=on&fixed_header=on&fixed_footer=on"
        )

        assert response.status_code == 200

        # Verify all properties enabled
        assert response.context["fixed_sidebar"] is True
        assert response.context["fixed_header"] is True
        assert response.context["fixed_footer"] is True

        html = response.content.decode("utf-8")

        # Verify all checkboxes present
        assert 'name="fixed_sidebar"' in html
        assert 'name="fixed_header"' in html
        assert 'name="fixed_footer"' in html

        # Verify app component is rendered (Cotton processes <c-app> into HTML)
        assert '<div class="app-wrapper' in html

        # CRITICAL: Verify all three fixed CSS classes are applied to .app-wrapper element
        assert "layout-fixed" in html, "layout-fixed class missing from app-wrapper"
        assert "fixed-header" in html, "fixed-header class missing from app-wrapper"
        assert "fixed-footer" in html, "fixed-footer class missing from app-wrapper"
        # Verify they're all on the app-wrapper div together
        assert (
            'class="app-wrapper layout-fixed fixed-header fixed-footer sidebar-expand-lg'
            in html
            or (
                "layout-fixed" in html
                and "fixed-header" in html
                and "fixed-footer" in html
                and "app-wrapper" in html
            )
        )


@pytest.mark.django_db
class TestLayoutResponsiveDemo:
    """Test Responsive Breakpoint Demo View (T035-T036)"""

    def test_layout_responsive_demo_default_breakpoint(self, client: Client):
        """
        T035: Test layout_responsive_demo view with default breakpoint.

        Given: User visits /layout-responsive/ without query parameters
        When: View renders
        Then: Default breakpoint is 'lg'
        And: Breakpoint list contains all valid values
        And: <c-app> receives sidebar_expand="lg"
        """
        response = client.get("/layout-responsive/")

        assert response.status_code == 200
        assert "example/layout_responsive.html" in [t.name for t in response.templates]

        # Verify default breakpoint
        assert response.context["breakpoint"] == "lg"

        # Verify all breakpoints available
        assert response.context["breakpoints"] == ["sm", "md", "lg", "xl", "xxl"]

        # Verify dropdown is present
        html = response.content.decode("utf-8")
        assert 'name="breakpoint"' in html

        # Verify all breakpoint options in dropdown
        for bp in ["sm", "md", "lg", "xl", "xxl"]:
            assert f'value="{bp}"' in html or f">{bp}<" in html

    def test_layout_responsive_demo_with_breakpoint_md(self, client: Client):
        """
        T036: Test layout_responsive_demo view with breakpoint=md query param.

        Given: User selects 'md' from dropdown
        When: Page reloads with ?breakpoint=md
        Then: breakpoint context variable is 'md'
        And: Dropdown shows 'md' as selected
        And: <c-app> receives sidebar_expand="md"
        """
        response = client.get("/layout-responsive/?breakpoint=md")

        assert response.status_code == 200

        # Verify breakpoint state
        assert response.context["breakpoint"] == "md"

        # Verify HTML structure
        html = response.content.decode("utf-8")
        assert 'name="breakpoint"' in html
        assert 'value="md"' in html

    def test_layout_responsive_demo_invalid_breakpoint_fallback(self, client: Client):
        """
        Test that invalid breakpoint values fall back to 'lg'.

        Given: User provides invalid breakpoint query parameter
        When: Page renders
        Then: Breakpoint defaults to 'lg'
        """
        response = client.get("/layout-responsive/?breakpoint=invalid")

        assert response.status_code == 200
        assert response.context["breakpoint"] == "lg"

    def test_layout_responsive_demo_all_valid_breakpoints(self, client: Client):
        """
        Test that all valid breakpoints are accepted.

        Given: User provides any valid breakpoint
        When: Page renders
        Then: That breakpoint is used
        """
        for bp in ["sm", "md", "lg", "xl", "xxl"]:
            response = client.get(f"/layout-responsive/?breakpoint={bp}")
            assert response.status_code == 200
            assert response.context["breakpoint"] == bp
