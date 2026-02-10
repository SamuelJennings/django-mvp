"""
Tests for AdminLTE body tag layout architecture.

T001-T005: Architecture Fix - Ensure layout classes are on body tag per AdminLTE requirements.

The critical issue: AdminLTE CSS selectors require layout classes on <body> element,
not on div.app-wrapper. Current implementation applies classes to app-wrapper div,
which breaks AdminLTE CSS behavior.

This test file validates the corrected architecture where:
1. Layout classes must be on <body> tag for AdminLTE CSS selectors to work
2. Component should render body tag with appropriate classes
3. JavaScript slot should be available for user scripts
"""

import pytest
from django_cotton import cotton_render


@pytest.mark.django_db
class TestBodyTagArchitecture:
    """
    T001: Test body tag with layout classes for AdminLTE CSS compatibility.

    CRITICAL: This architecture fix is BLOCKING for all user stories.
    AdminLTE CSS requires layout classes on body element, not app-wrapper div.
    """

    def test_component_renders_body_tag_with_layout_classes(self, rf):
        """
        T001: Test that app component renders body tag with layout classes.

        This test validates the CRITICAL architecture requirement:
        - Layout classes must be on <body> tag for AdminLTE CSS selectors
        - Component should include body tag in its output
        - Default classes should be applied when no attributes provided

        Expected: <body class="bg-body-tertiary sidebar-expand-lg">
        Current (BROKEN): <div class="app-wrapper sidebar-expand-lg">
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
        )

        # CRITICAL CHECK: Body tag must exist in component output
        assert "<body" in html, (
            "ARCHITECTURE ERROR: Component must render body tag for AdminLTE CSS compatibility. "
            "Current implementation uses app-wrapper div which breaks AdminLTE selectors."
        )

        # CRITICAL CHECK: Default classes must be on body tag
        assert 'body class="bg-body-tertiary sidebar-expand-lg' in html, (
            f"ARCHITECTURE ERROR: Default layout classes must be on body tag. "
            f"AdminLTE CSS selectors like 'body.layout-fixed' require classes on body element. "
            f"Actual HTML: {html[:200]}..."
        )

        # CRITICAL CHECK: App wrapper must be inside body
        assert (
            "<body" in html and "app-wrapper" in html
        ), "ARCHITECTURE ERROR: App wrapper must be inside body tag structure"

    def test_fixed_sidebar_renders_layout_fixed_on_body(self, rf):
        """
        T001: Test that fixed_sidebar attribute adds layout-fixed class to body tag.

        AdminLTE CSS selector: body.layout-fixed .app-sidebar
        If classes are on div instead of body, sidebar positioning breaks.
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_sidebar=True,
        )

        # CRITICAL CHECK: layout-fixed must be on body tag, not div
        assert 'body class="' in html and "layout-fixed" in html, (
            f"ARCHITECTURE ERROR: fixed_sidebar must add layout-fixed to body tag. "
            f"AdminLTE CSS 'body.layout-fixed .app-sidebar' requires body class. "
            f"Actual HTML: {html[:300]}..."
        )

        # Verify it's not on a div (current broken implementation)
        body_start = html.find("<body")
        body_end = html.find(">", body_start) + 1
        body_tag = html[body_start:body_end]

        assert "layout-fixed" in body_tag, (
            f"layout-fixed class must be on body tag itself, not on child div. " f"Body tag: {body_tag}"
        )

    def test_fixed_header_renders_fixed_header_on_body(self, rf):
        """
        T001: Test that fixed_header attribute adds fixed-header class to body tag.

        AdminLTE CSS selector: body.fixed-header .app-header
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_header=True,
        )

        # CRITICAL CHECK: fixed-header must be on body tag
        assert 'body class="' in html and "fixed-header" in html, (
            f"ARCHITECTURE ERROR: fixed_header must add fixed-header to body tag. " f"Actual HTML: {html[:300]}..."
        )

    def test_fixed_footer_renders_fixed_footer_on_body(self, rf):
        """
        T001: Test that fixed_footer attribute adds fixed-footer class to body tag.

        AdminLTE CSS selector: body.fixed-footer .app-footer
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_footer=True,
        )

        # CRITICAL CHECK: fixed-footer must be on body tag
        assert 'body class="' in html and "fixed-footer" in html, (
            f"ARCHITECTURE ERROR: fixed_footer must add fixed-footer to body tag. " f"Actual HTML: {html[:300]}..."
        )

    def test_sidebar_expand_renders_on_body_tag(self, rf):
        """
        T001: Test that sidebar_expand attribute adds sidebar-expand-{value} to body tag.

        AdminLTE CSS selector: body.sidebar-expand-lg .app-sidebar
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            sidebar_expand="md",
        )

        # CRITICAL CHECK: sidebar-expand-md must be on body tag
        assert 'body class="' in html and "sidebar-expand-md" in html, (
            f"ARCHITECTURE ERROR: sidebar_expand must add sidebar-expand-md to body tag. "
            f"Actual HTML: {html[:300]}..."
        )


@pytest.mark.django_db
class TestLayoutCombinations:
    """
    User Story 2: Test combinations of multiple fixed elements.

    T020-T023: Validate that multiple layout attributes can work together
    without conflicts and render correct combined CSS classes.
    """

    def test_fixed_sidebar_plus_fixed_header(self, rf):
        """
        T020: Test that fixed_sidebar + fixed_header renders both classes on body.

        Should produce: body.layout-fixed.fixed-header for combined positioning.
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
        )

        # Both classes must be present on body tag
        assert 'body class="' in html and "layout-fixed" in html and "fixed-header" in html, (
            f"Both layout-fixed and fixed-header must be on body tag. " f"Actual HTML: {html[:300]}..."
        )

        # Verify both classes are in the body tag specifically
        body_start = html.find("<body")
        body_end = html.find(">", body_start) + 1
        body_tag = html[body_start:body_end]

        assert (
            "layout-fixed" in body_tag and "fixed-header" in body_tag
        ), f"Both classes must be on body tag itself. Body tag: {body_tag}"

    def test_fixed_header_plus_fixed_footer(self, rf):
        """
        T021: Test that fixed_header + fixed_footer renders both classes on body.

        Should produce: body.fixed-header.fixed-footer for top/bottom positioning.
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_header=True,
            fixed_footer=True,
        )

        # Both classes must be present on body tag
        assert 'body class="' in html and "fixed-header" in html and "fixed-footer" in html, (
            f"Both fixed-header and fixed-footer must be on body tag. " f"Actual HTML: {html[:300]}..."
        )

    def test_all_three_fixed_elements(self, rf):
        """
        T022: Test that all fixed attributes together render all classes on body.

        Should produce: body.layout-fixed.fixed-header.fixed-footer for complete fixed layout.
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
            fixed_footer=True,
        )

        # All three classes must be present
        body_classes = ["layout-fixed", "fixed-header", "fixed-footer"]
        for css_class in body_classes:
            assert (
                'body class="' in html and css_class in html
            ), f"Class {css_class} must be on body tag. Actual HTML: {html[:300]}..."

        # Verify all classes are in the body tag specifically
        body_start = html.find("<body")
        body_end = html.find(">", body_start) + 1
        body_tag = html[body_start:body_end]

        for css_class in body_classes:
            assert css_class in body_tag, f"Class {css_class} must be on body tag itself. Body tag: {body_tag}"

    def test_fixed_combinations_with_custom_sidebar_expand(self, rf):
        """
        T023: Test that fixed combinations with custom sidebar_expand work correctly.

        Should preserve sidebar_expand while adding fixed classes.
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
            sidebar_expand="md",
        )

        # All classes must be present: layout-fixed, fixed-header, sidebar-expand-md
        expected_classes = ["layout-fixed", "fixed-header", "sidebar-expand-md"]
        for css_class in expected_classes:
            assert (
                'body class="' in html and css_class in html
            ), f"Class {css_class} must be on body tag. Actual HTML: {html[:300]}..."

        # Ensure default sidebar-expand-lg is NOT present when custom value is used
        assert "sidebar-expand-lg" not in html, (
            f"Default sidebar-expand-lg should not be present when custom value is used. "
            f"Actual HTML: {html[:300]}..."
        )

    def test_sidebar_collapsible_with_fixed_combinations(self, rf):
        """
        T024: Test that sidebar_collapsible works with fixed combinations.

        Should combine sidebar-mini with layout-fixed and other fixed classes.
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
            sidebar_collapsible=True,
        )

        # All classes must be present: layout-fixed, fixed-header, sidebar-mini
        expected_classes = ["layout-fixed", "fixed-header", "sidebar-mini"]
        for css_class in expected_classes:
            assert (
                'body class="' in html and css_class in html
            ), f"Class {css_class} must be on body tag. Actual HTML: {html[:300]}..."

    def test_collapsed_with_fixed_combinations(self, rf):
        """
        T025: Test that collapsed works with fixed combinations.

        Should combine sidebar-mini sidebar-collapse with fixed classes.
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_footer=True,
            sidebar_collapsible=True,
            collapsed=True,
        )

        # All classes must be present: layout-fixed, fixed-footer, sidebar-mini, sidebar-collapse
        expected_classes = ["layout-fixed", "fixed-footer", "sidebar-mini", "sidebar-collapse"]
        for css_class in expected_classes:
            assert (
                'body class="' in html and css_class in html
            ), f"Class {css_class} must be on body tag. Actual HTML: {html[:300]}..."

    def test_extreme_combination_all_attributes(self, rf):
        """
        T026: Test extreme combination with all attributes at once.

        Should handle all layout attributes together without conflicts.
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
            fixed_footer=True,
            sidebar_collapsible=True,
            collapsed=True,
            sidebar_expand="xl",
            **{"class": "custom-test-class"},
        )

        # All classes must be present and properly ordered
        expected_classes = [
            "layout-fixed",
            "fixed-header",
            "fixed-footer",
            "sidebar-mini",
            "sidebar-collapse",
            "sidebar-expand-xl",
            "custom-test-class",
        ]
        for css_class in expected_classes:
            assert (
                'body class="' in html and css_class in html
            ), f"Class {css_class} must be on body tag. Actual HTML: {html[:300]}..."

        # Verify all classes are in the body tag specifically
        body_start = html.find("<body")
        body_end = html.find(">", body_start) + 1
        body_tag = html[body_start:body_end]

        for css_class in expected_classes:
            assert css_class in body_tag, f"Class {css_class} must be on body tag itself. Body tag: {body_tag}"


@pytest.mark.django_db
class TestEdgeCases:
    """
    T053-T055: Edge case testing for layout configuration.

    Tests robustness of the layout system with edge cases and invalid inputs.
    """

    def test_custom_class_attribute_doesnt_conflict(self, rf):
        """
        T053: Test custom class attribute doesn't conflict with layout classes.

        Ensures that adding a custom 'class' attribute to the c-app component
        doesn't interfere with the layout classes that are automatically applied.
        """
        mock_request = rf.get("/")
        html = cotton_render(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
            **{"class": "custom-override-class extra-class"},
        )

        # Verify both custom and layout classes are present
        assert "custom-override-class" in html, "Custom class should be preserved"
        assert "extra-class" in html, "Multiple custom classes should be preserved"
        assert "layout-fixed" in html, "Layout classes should not be removed by custom class"
        assert "fixed-header" in html, "Header layout should not be affected by custom class"

        # Verify classes are in body tag
        body_start = html.find("<body")
        body_end = html.find(">", body_start) + 1
        body_tag = html[body_start:body_end]

        for expected_class in ["custom-override-class", "extra-class", "layout-fixed", "fixed-header"]:
            assert expected_class in body_tag, f"Class {expected_class} must be in body tag. Body: {body_tag}"

    def test_all_valid_breakpoint_values(self, rf):
        """
        T054: Test all valid breakpoint values (sm, md, lg, xl, xxl).

        Ensures that every supported Bootstrap breakpoint works correctly
        and produces the expected sidebar-expand-{breakpoint} class.
        """
        valid_breakpoints = ["sm", "md", "lg", "xl", "xxl"]
        mock_request = rf.get("/")

        for breakpoint in valid_breakpoints:
            html = cotton_render(
                mock_request,
                "app",
                sidebar_expand=breakpoint,
            )

            expected_class = f"sidebar-expand-{breakpoint}"
            assert expected_class in html, f"Expected class {expected_class} for breakpoint {breakpoint}"

            # Verify it's in the body tag specifically
            body_start = html.find("<body")
            body_end = html.find(">", body_start) + 1
            body_tag = html[body_start:body_end]
            assert expected_class in body_tag, f"Class {expected_class} must be in body tag. Body: {body_tag}"

    def test_invalid_attribute_values_gracefully_handled(self, rf):
        """
        T055: Test invalid attribute values are gracefully handled.

        Tests that the component doesn't crash with unexpected values.
        For simplicity, invalid values are passed through as-is, allowing
        developers to see their mistakes rather than silently correcting them.
        """
        mock_request = rf.get("/")

        # Test invalid sidebar_expand values are passed through
        html = cotton_render(
            mock_request,
            "app",
            sidebar_expand="invalid_breakpoint",
        )

        # Invalid breakpoint should be passed through unchanged
        assert "sidebar-expand-invalid_breakpoint" in html, "Invalid breakpoint should be passed through"
        assert "sidebar-expand-lg" not in html, "Should not fallback to default when explicit value provided"

        # Test invalid boolean-like values for fixed attributes
        html = cotton_render(
            mock_request,
            "app",
            fixed_sidebar="invalid_boolean",
            fixed_header="yes",
            fixed_footer="1",
        )

        # Django templates treat non-empty strings as truthy
        assert "layout-fixed" in html, "Non-empty string should be truthy for fixed_sidebar"
        assert "<body" in html, "Component should still render body tag with invalid boolean values"

        # Test empty string values
        html = cotton_render(
            mock_request,
            "app",
            sidebar_expand="",
            fixed_sidebar="",
        )

        # Should render without crashing
        assert "<body" in html, "Component should handle empty string attributes"
        # Empty sidebar_expand should render as empty string in class attribute
        assert "sidebar-expand-" in html, "Empty sidebar_expand should result in 'sidebar-expand-'"
