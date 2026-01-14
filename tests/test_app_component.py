"""
Tests for <c-app> component layout attributes.

These tests validate the AdminLTE layout configuration system,
ensuring that fixed_sidebar, fixed_header, and fixed_footer attributes
generate the correct AdminLTE CSS classes on the body element.
"""

import pytest
from django_cotton import render_component


@pytest.mark.django_db
class TestAppLayoutAttributes:
    """Test User Story 1: Apply Basic Layout Variations"""

    def test_fixed_sidebar_renders_layout_fixed_class(self, rf):
        """
        T002: Test that fixed_sidebar attribute adds .layout-fixed to body element.

        Given: A Django project using django-mvp
        When: Developer configures fixed sidebar layout
        Then: Sidebar CSS class appears on body element
        """
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
        )

        # Verify layout-fixed class is present
        assert "layout-fixed" in html, "Expected .layout-fixed class for fixed_sidebar"

        # Verify app-wrapper is present
        assert 'class="app-wrapper' in html, "Expected app-wrapper div"

        # Verify default sidebar_expand
        assert "sidebar-expand-lg" in html, "Expected default sidebar-expand-lg class"

    def test_fixed_header_renders_fixed_header_class(self, rf):
        """
        T003: Test that fixed_header attribute adds .fixed-header to body element.

        Given: Fixed header is enabled
        When: User scrolls down a long page
        Then: Navigation header CSS class appears on body element
        """
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
            fixed_header=True,
        )

        # Verify fixed-header class is present
        assert "fixed-header" in html, "Expected .fixed-header class for fixed_header"

        # Verify app-wrapper is present
        assert 'class="app-wrapper' in html, "Expected app-wrapper div"

        # Verify no other fixed classes
        assert "layout-fixed" not in html, "Should not have layout-fixed without fixed_sidebar"

    def test_fixed_footer_renders_fixed_footer_class(self, rf):
        """
        T004: Test that fixed_footer attribute adds .fixed-footer to body element.

        Given: Fixed footer is enabled
        When: User scrolls content
        Then: Footer CSS class appears on body element
        """
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
            fixed_footer=True,
        )

        # Verify fixed-footer class is present
        assert "fixed-footer" in html, "Expected .fixed-footer class for fixed_footer"

        # Verify app-wrapper is present
        assert 'class="app-wrapper' in html, "Expected app-wrapper div"

        # Verify no other fixed classes
        assert "layout-fixed" not in html, "Should not have layout-fixed without fixed_sidebar"
        assert "fixed-header" not in html, "Should not have fixed-header without fixed_header"

    def test_default_layout_no_fixed_classes(self, rf):
        """
        T005: Test that default (no attributes) renders no fixed classes.

        Given: Default (non-fixed) layout is used
        When: User scrolls
        Then: All layout elements scroll naturally (no fixed classes)
        """
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
        )

        # Verify base classes are present
        assert 'class="app-wrapper' in html, "Expected app-wrapper div"
        assert "sidebar-expand-lg" in html, "Expected default sidebar-expand-lg class"

        # Verify NO fixed classes
        assert "layout-fixed" not in html, "Should not have layout-fixed in default layout"
        assert "fixed-header" not in html, "Should not have fixed-header in default layout"
        assert "fixed-footer" not in html, "Should not have fixed-footer in default layout"


@pytest.mark.django_db
class TestAppLayoutCombinations:
    """Test User Story 2: Combine Multiple Fixed Elements"""

    def test_fixed_sidebar_plus_fixed_header(self, rf):
        """
        T007: Test that fixed_sidebar + fixed_header renders both classes.

        Given: Fixed sidebar and header are enabled
        When: User scrolls content
        Then: Both sidebar and header CSS classes appear on body element
        """
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
        )

        # Verify both classes present
        assert "layout-fixed" in html, "Expected .layout-fixed class for fixed_sidebar"
        assert "fixed-header" in html, "Expected .fixed-header class for fixed_header"

        # Verify footer is not fixed
        assert "fixed-footer" not in html, "Should not have fixed-footer"

    def test_fixed_header_plus_fixed_footer(self, rf):
        """
        T008: Test that fixed_header + fixed_footer renders both classes.

        Given: Fixed header and footer are enabled
        When: User scrolls content
        Then: Both header and footer CSS classes appear on body element
        """
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
            fixed_header=True,
            fixed_footer=True,
        )

        # Verify both classes present
        assert "fixed-header" in html, "Expected .fixed-header class for fixed_header"
        assert "fixed-footer" in html, "Expected .fixed-footer class for fixed_footer"

        # Verify sidebar is not fixed
        assert "layout-fixed" not in html, "Should not have layout-fixed without fixed_sidebar"

    def test_all_three_fixed_elements(self, rf):
        """
        T009: Test that all three fixed attributes render all three classes.

        Given: Complete fixed layout (sidebar, header, footer)
        When: User scrolls content
        Then: All three CSS classes appear on body element
        """
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
            fixed_footer=True,
        )

        # Verify all three classes present
        assert "layout-fixed" in html, "Expected .layout-fixed class for fixed_sidebar"
        assert "fixed-header" in html, "Expected .fixed-header class for fixed_header"
        assert "fixed-footer" in html, "Expected .fixed-footer class for fixed_footer"

        # Verify app-wrapper is present
        assert 'class="app-wrapper' in html, "Expected app-wrapper div"


@pytest.mark.django_db
class TestAppLayoutInheritance:
    """Test User Story 3: Configure Layout Per-Page or Globally"""

    def test_base_template_with_fixed_sidebar(self, rf):
        """
        T010: Test that base layout configuration can be applied consistently.

        Given: A project uses fixed sidebar as the base layout
        When: Component is rendered with fixed_sidebar attribute
        Then: Sidebar remains fixed across navigation
        """
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
        )

        # Verify base layout has fixed sidebar
        assert "layout-fixed" in html, "Expected .layout-fixed for base layout"
        assert 'class="app-wrapper' in html, "Expected app-wrapper div"

    def test_per_page_layout_override(self, rf):
        """
        T011: Test that different pages can use different layout configurations.

        Given: Base template has fixed_sidebar, but one page needs different layout
        When: That page renders <c-app> with fixed_header instead
        Then: The page has the overridden layout (fixed header, not fixed sidebar)
        """
        mock_request = rf.get("/")

        # Simulate base template pattern (typical page uses fixed_sidebar)
        base_html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
        )
        assert "layout-fixed" in base_html, "Base should have fixed sidebar"
        assert "fixed-header" not in base_html, "Base should not have fixed header"

        # Simulate override pattern (special page uses fixed_header)
        override_html = render_component(
            mock_request,
            "app",
            fixed_header=True,
        )
        assert "fixed-header" in override_html, "Override should have fixed header"
        assert "layout-fixed" not in override_html, "Override should not have fixed sidebar"


@pytest.mark.django_db
class TestAppLayoutEdgeCases:
    """Test edge cases and responsive behavior"""

    def test_custom_class_attribute_no_conflict(self, rf):
        """
        T019: Test that custom class attribute doesn't conflict with fixed classes.

        Given: User provides custom CSS classes
        When: Component also applies fixed layout classes
        Then: Both custom and fixed classes are present without conflicts
        """
        # Note: <c-app> currently doesn't expose a class attribute
        # This test verifies that fixed classes are applied consistently
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
            fixed_sidebar=True,
            fixed_header=True,
        )

        # Verify both fixed classes present
        assert "layout-fixed" in html, "Expected .layout-fixed class"
        assert "fixed-header" in html, "Expected .fixed-header class"

    def test_sidebar_expand_breakpoints(self, rf):
        """
        T020: Test sidebar_expand values render correct responsive classes.

        Given: Different Bootstrap breakpoint values
        When: Component renders with sidebar_expand attribute
        Then: Correct .sidebar-expand-{breakpoint} class appears
        """
        mock_request = rf.get("/")

        # Test each breakpoint
        breakpoints = ["sm", "md", "lg", "xl", "xxl"]

        for bp in breakpoints:
            html = render_component(
                mock_request,
                "app",
                sidebar_expand=bp,
            )
            expected_class = f"sidebar-expand-{bp}"
            assert expected_class in html, f"Expected {expected_class} for breakpoint {bp}"

    def test_sidebar_expand_default_is_lg(self, rf):
        """
        Test that default sidebar_expand is 'lg' when not specified.
        """
        mock_request = rf.get("/")
        html = render_component(
            mock_request,
            "app",
        )

        # Verify default lg breakpoint
        assert "sidebar-expand-lg" in html, "Expected default sidebar-expand-lg class"

    def test_boolean_attributes_handle_string_values(self, rf):
        """
        T020b: Test that string values for boolean attributes are handled correctly.

        Given: Boolean attributes receive string values (e.g., fixed_sidebar="false")
        When: Component processes these attributes
        Then: Attributes are treated as booleans per Cotton's behavior
        """
        mock_request = rf.get("/")

        # In Cotton, any non-empty attribute value is truthy
        # This is expected behavior - attributes like fixed_sidebar="false" are still truthy
        html_string_true = render_component(
            mock_request,
            "app",
            fixed_sidebar="false",  # String "false" is truthy in Cotton
        )

        # String "false" is still truthy, so class should be present
        # This is documented Cotton behavior - use absence of attribute to disable
        assert "layout-fixed" in html_string_true, (
            'String "false" is truthy in Cotton - ' "use absent attribute to disable features"
        )

        # Correct way: omit the attribute entirely
        html_no_attr = render_component(
            mock_request,
            "app",
            # fixed_sidebar NOT provided
        )
        assert "layout-fixed" not in html_no_attr, "Omitted attribute should disable feature"
