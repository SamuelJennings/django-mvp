"""
Tests for interactive layout demo page.

User Story 4: Interactive Layout Demo Page (T036-T052)
Verifies that:
- Demo page at /layout/ renders with form controls for layout options
- Query parameters control layout configuration
- Form checkboxes reflect current URL state
- All layout combinations work through URL parameters
- Invalid values fall back to defaults gracefully
"""

import pytest
from django.test import Client


@pytest.mark.django_db
class TestLayoutDemo:
    """
    User Story 4: Test interactive layout demo page functionality.

    T036-T043: Validate that layout demo page renders correctly and responds
    to query parameters for interactive layout testing.
    """

    def test_layout_demo_view_renders_default_state(self):
        """
        T037: Test that /layout/ view renders with default state (no query params).

        Should show demo page with all layout options unchecked by default.
        """
        client = Client()
        response = client.get("/layout/")

        # Verify successful response
        assert response.status_code == 200, f"Layout demo page should be accessible. Status: {response.status_code}"

        # Verify default layout (no fixed elements)
        html = response.content.decode("utf-8")
        assert (
            "layout-fixed" not in html and "fixed-header" not in html and "fixed-footer" not in html
        ), f"Default layout should have no fixed elements. HTML: {html[:300]}..."

        # Verify default sidebar expansion
        assert "sidebar-expand-lg" in html, f"Default sidebar expansion should be 'lg'. HTML: {html[:300]}..."

    def test_layout_demo_fixed_sidebar_query_param(self):
        """
        T038: Test that /layout/?fixed_sidebar=on applies fixed sidebar layout.

        Should render page with layout-fixed class on body tag.
        """
        client = Client()
        response = client.get("/layout/?fixed_sidebar=on")

        # Verify successful response
        assert response.status_code == 200

        # Verify fixed sidebar is applied
        html = response.content.decode("utf-8")
        assert "layout-fixed" in html, f"Fixed sidebar should be applied via query param. HTML: {html[:300]}..."

        # Verify checkbox is checked in form
        import re

        checkbox_pattern = (
            r'<input[^>]*name="fixed_sidebar"[^>]*checked[^>]*>|<input[^>]*checked[^>]*name="fixed_sidebar"[^>]*>'
        )
        assert re.search(checkbox_pattern, html), f"Fixed sidebar checkbox should be checked. HTML: {html[:300]}..."

    def test_layout_demo_multiple_fixed_elements(self):
        """
        T039: Test that /layout/?fixed_header=on&fixed_footer=on applies both layouts.

        Should render with both fixed-header and fixed-footer classes.
        """
        client = Client()
        response = client.get("/layout/?fixed_header=on&fixed_footer=on")

        # Verify successful response
        assert response.status_code == 200

        # Verify both fixed elements are applied
        html = response.content.decode("utf-8")
        assert (
            "fixed-header" in html and "fixed-footer" in html
        ), f"Both fixed header and footer should be applied. HTML: {html[:300]}..."

    def test_layout_demo_all_fixed_elements(self):
        """
        T040: Test that all fixed attributes together work via query parameters.

        Should handle complete fixed layout configuration from URL.
        """
        client = Client()
        response = client.get("/layout/?fixed_sidebar=on&fixed_header=on&fixed_footer=on")

        # Verify successful response
        assert response.status_code == 200

        # Verify all fixed elements are applied
        html = response.content.decode("utf-8")
        expected_classes = ["layout-fixed", "fixed-header", "fixed-footer"]
        for css_class in expected_classes:
            assert css_class in html, f"Class {css_class} should be applied. HTML: {html[:300]}..."

    def test_layout_demo_custom_sidebar_expand(self):
        """
        T041: Test that /layout/?sidebar_expand=md applies breakpoint correctly.

        Should render with sidebar-expand-md instead of default lg.
        """
        client = Client()
        response = client.get("/layout/?sidebar_expand=md")

        # Verify successful response
        assert response.status_code == 200

        # Verify custom sidebar expand is applied
        html = response.content.decode("utf-8")
        assert "sidebar-expand-md" in html, f"Custom sidebar expand should be applied. HTML: {html[:300]}..."

        # Verify default lg is not present
        assert "sidebar-expand-lg" not in html, f"Default sidebar expand should not be present. HTML: {html[:300]}..."

    def test_layout_demo_invalid_breakpoint_fallback(self):
        """
        T042: Test that invalid breakpoint falls back to default "lg".

        Should gracefully handle invalid sidebar_expand values.
        """
        client = Client()
        response = client.get("/layout/?sidebar_expand=invalid")

        # Verify successful response (doesn't crash)
        assert response.status_code == 200

        # Verify fallback to default
        html = response.content.decode("utf-8")
        assert (
            "sidebar-expand-lg" in html
        ), f"Invalid breakpoint should fall back to default 'lg'. HTML: {html[:300]}..."

        # Verify invalid value is not present
        assert "sidebar-expand-invalid" not in html, f"Invalid breakpoint should not be used. HTML: {html[:300]}..."

    def test_layout_demo_form_reflects_query_params(self):
        """
        T043: Test that form checkboxes reflect current query parameter state.

        Should show checked state for parameters that are active.
        """
        client = Client()
        response = client.get("/layout/?fixed_sidebar=on&sidebar_expand=xl")

        # Verify successful response
        assert response.status_code == 200

        html = response.content.decode("utf-8")

        # Verify fixed_sidebar checkbox is checked
        import re

        checkbox_pattern = (
            r'<input[^>]*name="fixed_sidebar"[^>]*checked[^>]*>|<input[^>]*checked[^>]*name="fixed_sidebar"[^>]*>'
        )
        assert re.search(
            checkbox_pattern, html
        ), f"Fixed sidebar checkbox should reflect query param state. HTML: {html[:300]}..."

        # Verify sidebar_expand dropdown shows correct value
        select_pattern = r'<option[^>]*value="xl"[^>]*selected[^>]*>|<option[^>]*selected[^>]*value="xl"[^>]*>'
        assert re.search(
            select_pattern, html
        ), f"Sidebar expand dropdown should reflect query param state. HTML: {html[:300]}..."


@pytest.mark.django_db
class TestLayoutDemoAdvanced:
    """
    User Story 4: Test advanced demo page features.

    T044-T046: Test collapsible sidebar features and complex combinations
    through the demo interface.
    """

    def test_layout_demo_sidebar_collapsible_query_param(self):
        """
        T044: Test that sidebar_collapsible query param works correctly.

        Should render with sidebar-mini class when enabled.
        """
        client = Client()
        response = client.get("/layout/?sidebar_collapsible=on")

        # Verify successful response
        assert response.status_code == 200

        # Verify sidebar collapsible is applied
        html = response.content.decode("utf-8")
        assert "sidebar-mini" in html, f"Sidebar collapsible should add sidebar-mini class. HTML: {html[:300]}..."

    def test_layout_demo_collapsed_query_param(self):
        """
        T045: Test that collapsed query param works with sidebar_collapsible.

        Should render with both sidebar-mini and sidebar-collapse classes.
        """
        client = Client()
        response = client.get("/layout/?sidebar_collapsible=on&collapsed=on")

        # Verify successful response
        assert response.status_code == 200

        # Verify both classes are applied
        html = response.content.decode("utf-8")
        assert (
            "sidebar-mini" in html and "sidebar-collapse" in html
        ), f"Both sidebar classes should be applied. HTML: {html[:300]}..."

    def test_layout_demo_complete_configuration(self):
        """
        T046: Test complete layout configuration through query parameters.

        Should handle all available options simultaneously.
        """
        client = Client()
        query_params = (
            "?fixed_sidebar=on&fixed_header=on&fixed_footer=on"
            "&sidebar_collapsible=on&collapsed=on&sidebar_expand=xxl"
        )
        response = client.get(f"/layout/{query_params}")

        # Verify successful response
        assert response.status_code == 200

        # Verify all configuration is applied
        html = response.content.decode("utf-8")
        expected_classes = [
            "layout-fixed",
            "fixed-header",
            "fixed-footer",
            "sidebar-mini",
            "sidebar-collapse",
            "sidebar-expand-xxl",
        ]
        for css_class in expected_classes:
            assert css_class in html, f"Class {css_class} should be applied in complete config. HTML: {html[:300]}..."


@pytest.mark.django_db
class TestFillLayoutIntegration:
    """
    User Story 3.5: Test fill layout feature integration (T086-T087).

    Verifies that:
    - Fill checkbox renders in the layout demo form
    - View handles fill query parameter correctly
    - Fill class is applied when fill=on
    """

    def test_fill_checkbox_renders_in_form(self):
        """
        T086: Test that fill checkbox renders in the layout demo form.

        Should show fill checkbox with proper label and help text.
        """
        client = Client()
        response = client.get("/layout/")

        # Verify successful response
        assert response.status_code == 200

        # Verify fill checkbox exists in form
        html = response.content.decode("utf-8")
        assert 'name="fill"' in html, f"Fill checkbox should exist in form. HTML: {html[:500]}..."

        # Verify label text
        assert "Fill Layout" in html, f"Fill checkbox label should exist. HTML: {html[:500]}..."

        # Verify help text mentions viewport-constrained or data tables
        assert (
            "Viewport-constrained" in html or "data tables" in html or "maps" in html
        ), f"Fill help text should mention use cases. HTML: {html[:500]}..."

    def test_view_handles_fill_query_param(self):
        """
        T087: Test that view handles fill query parameter correctly.

        Should parse fill=on from query string and pass to template context.
        """
        client = Client()

        # Test without fill parameter
        response = client.get("/layout/")
        assert response.status_code == 200
        assert response.context["fill"] is False, "Fill should be False without query param"

        # Test with fill=on
        response = client.get("/layout/?fill=on")
        assert response.status_code == 200
        assert response.context["fill"] is True, "Fill should be True with fill=on"

        # Verify .fill class is present in HTML when enabled
        html = response.content.decode("utf-8")
        assert (
            'class="app-wrapper fill"' in html or "app-wrapper fill" in html
        ), f"Fill class should be applied when fill=on. HTML: {html[:500]}..."

        # Verify fill badge shows "Enabled" status
        assert (
            "<code>fill</code>" in html and "Enabled" in html
        ), f"Fill status should show as Enabled. HTML: {html[:1000]}..."

    def test_fill_checkbox_reflects_query_param(self):
        """
        Test that fill checkbox is checked when fill=on in URL.

        Should maintain checkbox state based on URL parameter.
        """
        client = Client()
        response = client.get("/layout/?fill=on")

        assert response.status_code == 200

        # Verify checkbox is checked in the HTML
        html = response.content.decode("utf-8")
        assert (
            'name="fill"' in html and "checked" in html
        ), f"Fill checkbox should be checked when fill=on. HTML: {html[:1000]}..."

    def test_fill_combined_with_other_options(self):
        """
        Test fill works alongside other layout options.

        Should allow fill + fixed_sidebar, fixed_header, etc.
        """
        client = Client()
        response = client.get("/layout/?fill=on&fixed_sidebar=on&fixed_header=on&fixed_footer=on")

        assert response.status_code == 200

        # Verify all options are in context
        assert response.context["fill"] is True
        assert response.context["fixed_sidebar"] is True
        assert response.context["fixed_header"] is True
        assert response.context["fixed_footer"] is True

        # Verify fill class is applied
        html = response.content.decode("utf-8")
        assert "app-wrapper fill" in html, f"Fill class should be present with other options. HTML: {html[:500]}..."
