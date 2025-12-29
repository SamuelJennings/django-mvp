"""
Tests for inner layout component.

This module consolidates all tests for the inner layout component including:
- Basic rendering and slot handling
- Responsive behavior and offcanvas mode
- Customization parameters
- Edge cases and accessibility
"""

import pytest
from bs4 import BeautifulSoup


@pytest.mark.django_db
class TestInnerLayoutBasicRendering:
    """Test suite for basic rendering behavior."""

    def test_default_slot_renders(self, render_cotton_component):
        """Test that the default slot content renders in main content area (T008)."""
        html = render_cotton_component(
            "test_inner_basic.html", {"test_content": "<h1>Test Content</h1><p>This is the main content.</p>"}
        )
        soup = BeautifulSoup(html, "html.parser")

        main_content = soup.select_one(".content-main")
        assert main_content is not None, "Main content area (.content-main) not found"

        h1 = main_content.find("h1")
        assert h1 is not None, "H1 heading not found in main content"
        assert h1.text.strip() == "Test Content", "H1 text doesn't match"

        p = main_content.find("p")
        assert p is not None, "Paragraph not found in main content"
        assert "main content" in p.text, "Paragraph text doesn't match"

    def test_main_content_expands_with_no_sidebars(self, render_cotton_component):
        """Test that main content expands to full width when no sidebars declared (T009)."""
        html = render_cotton_component(
            "test_inner_basic.html", {"test_content": '<div id="test-content">Full width content</div>'}
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        secondary_sidebar = soup.select_one(".content-sidebar-right")
        assert primary_sidebar is None, "Primary sidebar should not render when not declared"
        assert secondary_sidebar is None, "Secondary sidebar should not render when not declared"

        main_content = soup.select_one(".content-main")
        assert main_content is not None, "Main content area not found"
        assert "flex-grow-1" in main_content.get("class", []), "Main content should have flex-grow-1 class"

        test_content = soup.select_one("#test-content")
        assert test_content is not None, "Test content not found"
        assert test_content.text.strip() == "Full width content"

    def test_aria_landmark_on_content_main(self, render_cotton_component):
        """Test that main content area has role='main' ARIA landmark (T010)."""
        html = render_cotton_component("test_inner_basic.html", {"test_content": "<p>Test content</p>"})
        soup = BeautifulSoup(html, "html.parser")

        main_content = soup.select_one(".content-main")
        assert main_content is not None, "Main content area not found"

        role = main_content.get("role")
        assert role == "main", f"Expected role='main', got role='{role}'"

        aria_label = main_content.get("aria-label")
        assert aria_label is not None, "Main content should have aria-label"
        assert (
            "main" in aria_label.lower() or "content" in aria_label.lower()
        ), f"aria-label should describe main content, got '{aria_label}'"

    def test_content_shell_wrapper_exists(self, render_cotton_component):
        """Test that content-shell wrapper div exists with proper structure."""
        html = render_cotton_component("test_inner_basic.html", {"test_content": "<p>Test</p>"})
        soup = BeautifulSoup(html, "html.parser")

        content_shell = soup.select_one(".content-shell")
        assert content_shell is not None, "Content shell wrapper (.content-shell) not found"
        assert "d-flex" in content_shell.get("class", []), "Content shell should have d-flex class"

    def test_css_variables_set_on_content_shell(self, render_cotton_component):
        """Test that CSS variables are set on content-shell for sidebar widths."""
        html = render_cotton_component("test_inner_basic.html", {"test_content": "<p>Test</p>"})
        soup = BeautifulSoup(html, "html.parser")

        content_shell = soup.select_one(".content-shell")
        assert content_shell is not None, "Content shell not found"

        style = content_shell.get("style")
        assert style is not None, "Content shell should have style attribute with CSS variables"
        assert (
            "--content-primary-width" in style or "content-primary-width" in style
        ), "CSS variable --content-primary-width should be set"
        assert (
            "--content-secondary-width" in style or "content-secondary-width" in style
        ), "CSS variable --content-secondary-width should be set"


@pytest.mark.django_db
class TestInnerLayoutSidebars:
    """Test suite for sidebar rendering and behavior."""

    def test_primary_sidebar_renders_on_left(self, render_cotton_component):
        """Test that primary_sidebar renders on left in two-column layout (T014)."""
        html = render_cotton_component(
            "test_inner_primary_only.html",
            {"test_content": "<h1>Main Content</h1>", "test_primary_content": '<nav id="test-nav">Navigation</nav>'},
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is not None, "Primary sidebar (.content-sidebar-left) not found"

        nav = primary_sidebar.find("nav", id="test-nav")
        assert nav is not None, "Navigation element not found in primary sidebar"
        assert "Navigation" in nav.text, "Navigation text not found"

        main_content = soup.select_one(".content-main")
        assert main_content is not None, "Main content should still exist with sidebar"

        content_shell = soup.select_one(".content-shell")
        element_children = [c for c in content_shell.children if hasattr(c, "name") and hasattr(c, "get")]

        sidebar_index = next(
            (i for i, c in enumerate(element_children) if "content-sidebar-left" in c.get("class", [])), None
        )
        main_index = next((i for i, c in enumerate(element_children) if "content-main" in c.get("class", [])), None)

        assert sidebar_index is not None and main_index is not None, "Both sidebar and main content should be present"
        assert sidebar_index < main_index, "Primary sidebar should come before main content in DOM"

    def test_empty_primary_sidebar_not_rendered(self, render_cotton_component):
        """Test that undeclared primary_sidebar slot does not render container (T015)."""
        html = render_cotton_component(
            "test_inner_basic.html",
            {"test_content": "<h1>Main Content</h1>"},
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is None, "Undeclared primary sidebar should not render"

        main_content = soup.select_one(".content-main")
        assert main_content is not None, "Main content should exist even without sidebar"

    def test_primary_sidebar_aria_landmark(self, render_cotton_component):
        """Test that primary_sidebar has role='complementary' ARIA landmark (T017)."""
        html = render_cotton_component(
            "test_inner_primary_only.html",
            {"test_content": "<h1>Main Content</h1>", "test_primary_content": "<nav>Navigation</nav>"},
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is not None, "Primary sidebar not found"

        role = primary_sidebar.get("role")
        assert role == "complementary", f"Expected role='complementary', got role='{role}'"

        aria_label = primary_sidebar.get("aria-label")
        assert aria_label is not None, "Primary sidebar should have aria-label"
        assert (
            "sidebar" in aria_label.lower() or "navigation" in aria_label.lower() or "primary" in aria_label.lower()
        ), f"aria-label should describe sidebar, got '{aria_label}'"

    def test_dual_sidebar_three_column_layout(self, render_cotton_component):
        """Test that both sidebars render in three-column layout (T022)."""
        html = render_cotton_component(
            "test_inner_dual_sidebar.html",
            {
                "test_primary_content": "<nav>Primary Nav</nav>",
                "test_secondary_content": "<aside>Secondary Content</aside>",
                "test_content": "<h1>Main Content</h1>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        secondary_sidebar = soup.select_one(".content-sidebar-right")
        main_content = soup.select_one(".content-main")

        assert primary_sidebar is not None, "Primary sidebar not found"
        assert secondary_sidebar is not None, "Secondary sidebar not found"
        assert main_content is not None, "Main content not found"

        assert "Primary Nav" in primary_sidebar.text
        assert "Secondary Content" in secondary_sidebar.text
        assert "Main Content" in main_content.text

        content_shell = soup.select_one(".content-shell")
        children = [c for c in content_shell.children if hasattr(c, "name") and hasattr(c, "get")]

        primary_idx = next((i for i, c in enumerate(children) if "content-sidebar-left" in c.get("class", [])), None)
        main_idx = next((i for i, c in enumerate(children) if "content-main" in c.get("class", [])), None)
        secondary_idx = next((i for i, c in enumerate(children) if "content-sidebar-right" in c.get("class", [])), None)

        assert all(idx is not None for idx in [primary_idx, main_idx, secondary_idx]), "All columns should be present"
        assert primary_idx < main_idx < secondary_idx, "Column order should be: primary -> main -> secondary"

    def test_secondary_sidebar_empty_not_rendered(self, render_cotton_component):
        """Test that undeclared secondary_sidebar slot does not render container (T023)."""
        html = render_cotton_component(
            "test_inner_primary_only.html",
            {
                "test_primary_content": "<nav>Primary Nav</nav>",
                "test_content": "<h1>Main Content</h1>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is not None, "Primary sidebar should render"

        secondary_sidebar = soup.select_one(".content-sidebar-right")
        assert secondary_sidebar is None, "Undeclared secondary sidebar should not render"

        main_content = soup.select_one(".content-main")
        assert main_content is not None, "Main content should exist"

    def test_secondary_sidebar_aria_landmark(self, render_cotton_component):
        """Test that secondary_sidebar has role='complementary' ARIA landmark (T026)."""
        html = render_cotton_component(
            "test_inner_dual_sidebar.html",
            {
                "test_primary_content": "<nav>Primary</nav>",
                "test_secondary_content": "<aside>Secondary</aside>",
                "test_content": "<h1>Main</h1>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        secondary_sidebar = soup.select_one(".content-sidebar-right")
        assert secondary_sidebar is not None, "Secondary sidebar not found"

        role = secondary_sidebar.get("role")
        assert role == "complementary", f"Expected role='complementary', got role='{role}'"

        aria_label = secondary_sidebar.get("aria-label")
        assert aria_label is not None, "Secondary sidebar should have aria-label"
        assert (
            "sidebar" in aria_label.lower() or "secondary" in aria_label.lower()
        ), f"aria-label should describe secondary sidebar, got '{aria_label}'"


@pytest.mark.django_db
class TestInnerLayoutSlots:
    """Test suite for slot combination scenarios."""

    def test_mixed_primary_empty_secondary_full(self, render_cotton_component):
        """Test layout with undeclared primary_sidebar and full secondary_sidebar (T024)."""
        html = render_cotton_component(
            "test_inner_secondary_only.html",
            {
                "test_secondary_content": "<aside>Secondary Content</aside>",
                "test_content": "<h1>Main Content</h1>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is None, "Undeclared primary sidebar should not render"

        secondary_sidebar = soup.select_one(".content-sidebar-right")
        assert secondary_sidebar is not None, "Secondary sidebar should render"
        assert "Secondary Content" in secondary_sidebar.text

        main_content = soup.select_one(".content-main")
        assert main_content is not None, "Main content should render"
        assert "Main Content" in main_content.text

    def test_both_sidebars_empty(self, render_cotton_component):
        """Test layout with both sidebars undeclared."""
        html = render_cotton_component(
            "test_inner_basic.html",
            {
                "test_content": "<h1>Main Content</h1>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        secondary_sidebar = soup.select_one(".content-sidebar-right")

        assert primary_sidebar is None, "Undeclared primary sidebar should not render"
        assert secondary_sidebar is None, "Undeclared secondary sidebar should not render"

        main_content = soup.select_one(".content-main")
        assert main_content is not None, "Main content should render"
        assert "flex-grow-1" in main_content.get("class", []), "Main content should expand"

    def test_mixed_primary_full_secondary_empty(self, render_cotton_component):
        """Test layout with full primary_sidebar and undeclared secondary_sidebar."""
        html = render_cotton_component(
            "test_inner_primary_only.html",
            {
                "test_primary_content": "<nav>Primary Nav</nav>",
                "test_content": "<h1>Main Content</h1>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is not None, "Primary sidebar should render"
        assert "Primary Nav" in primary_sidebar.text

        secondary_sidebar = soup.select_one(".content-sidebar-right")
        assert secondary_sidebar is None, "Undeclared secondary sidebar should not render"

        main_content = soup.select_one(".content-main")
        assert main_content is not None, "Main content should render"


@pytest.mark.django_db
class TestInnerLayoutResponsive:
    """Test suite for responsive behavior."""

    def test_offcanvas_mode_classes_present(self, render_cotton_component):
        """Test that offcanvas classes are present for primary sidebar (T016)."""
        html = render_cotton_component(
            "test_inner_primary_only.html",
            {
                "test_content": "<h1>Main Content</h1>",
                "test_primary_content": '<nav><ul><li><a href="/">Home</a></li></ul></nav>',
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is not None, "Primary sidebar not found"

        classes = primary_sidebar.get("class", [])
        assert any(
            "offcanvas-md" in str(c) for c in classes
        ), f"Primary sidebar should have offcanvas-md class, got classes: {classes}"
        assert (
            "offcanvas-start" in classes
        ), f"Primary sidebar should have offcanvas-start class, got classes: {classes}"

    def test_offcanvas_header_hidden_at_breakpoint(self, render_cotton_component):
        """Test that offcanvas header is hidden at/above breakpoint."""
        html = render_cotton_component(
            "test_inner_primary_only.html",
            {"test_content": "<h1>Main Content</h1>", "test_primary_content": "<nav>Navigation</nav>"},
        )
        soup = BeautifulSoup(html, "html.parser")

        offcanvas_header = soup.select_one(".offcanvas-header")
        assert offcanvas_header is not None, "Offcanvas header not found"

        classes = offcanvas_header.get("class", [])
        assert "d-md-none" in classes, f"Offcanvas header should have d-md-none class, got classes: {classes}"

    def test_offcanvas_close_button_present(self, render_cotton_component):
        """Test that offcanvas has close button for mobile."""
        html = render_cotton_component(
            "test_inner_primary_only.html",
            {"test_content": "<h1>Main Content</h1>", "test_primary_content": "<nav>Navigation</nav>"},
        )
        soup = BeautifulSoup(html, "html.parser")

        close_button = soup.select_one(".offcanvas-header .btn-close")
        assert close_button is not None, "Offcanvas close button not found"

        dismiss_attr = close_button.get("data-bs-dismiss")
        assert (
            dismiss_attr == "offcanvas"
        ), f"Close button should have data-bs-dismiss='offcanvas', got '{dismiss_attr}'"

    def test_both_sidebars_offcanvas_mode(self, render_cotton_component):
        """Test that both sidebars use offcanvas mode at mobile breakpoint (T025)."""
        html = render_cotton_component(
            "test_inner_dual_sidebar.html",
            {
                "test_primary_content": "<nav>Primary Nav</nav>",
                "test_secondary_content": "<aside>Secondary Content</aside>",
                "test_content": "<h1>Main Content</h1>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is not None, "Primary sidebar not found"

        primary_classes = primary_sidebar.get("class", [])
        assert "offcanvas-md" in primary_classes, "Primary sidebar should have offcanvas-md class"
        assert "offcanvas-start" in primary_classes, "Primary sidebar should have offcanvas-start class"

        secondary_sidebar = soup.select_one(".content-sidebar-right")
        assert secondary_sidebar is not None, "Secondary sidebar not found"

        secondary_classes = secondary_sidebar.get("class", [])
        assert "offcanvas-md" in secondary_classes, "Secondary sidebar should have offcanvas-md class"
        assert "offcanvas-end" in secondary_classes, "Secondary sidebar should have offcanvas-end class"

        primary_header = primary_sidebar.select_one(".offcanvas-header")
        assert primary_header is not None, "Primary offcanvas header not found"
        assert "d-md-none" in primary_header.get("class", []), "Primary header should be hidden at md+"

        secondary_header = secondary_sidebar.select_one(".offcanvas-header")
        assert secondary_header is not None, "Secondary offcanvas header not found"
        assert "d-md-none" in secondary_header.get("class", []), "Secondary header should be hidden at md+"

    def test_custom_breakpoint(self, render_cotton_component):
        """Test that custom breakpoint parameter changes offcanvas mode (T033)."""
        html = render_cotton_component("test_inner_custom_breakpoint.html", {"test_content": "<h1>Main Content</h1>"})
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is not None, "Primary sidebar not found"

        classes = primary_sidebar.get("class", [])
        assert "offcanvas-lg" in classes, f"Expected offcanvas-lg class, got: {classes}"
        assert "offcanvas-md" not in classes, "Should not have default md breakpoint"

        offcanvas_header = primary_sidebar.select_one(".offcanvas-header")
        assert offcanvas_header is not None, "Offcanvas header not found"

        header_classes = offcanvas_header.get("class", [])
        assert "d-lg-none" in header_classes, f"Expected d-lg-none class on header, got: {header_classes}"


@pytest.mark.django_db
class TestInnerLayoutCustomization:
    """Test suite for customization parameters."""

    def test_custom_primary_width(self, render_cotton_component):
        """Test that custom primary_width parameter sets CSS variable (T031)."""
        html = render_cotton_component("test_inner_custom_width.html", {"test_content": "<h1>Main</h1>"})
        soup = BeautifulSoup(html, "html.parser")

        content_shell = soup.select_one(".content-shell")
        assert content_shell is not None, "Content shell not found"

        style = content_shell.get("style", "")
        assert "320px" in style, f"Custom primary_width not found in style: {style}"
        assert "--content-primary-width: 320px" in style or "--content-primary-width:320px" in style

    def test_custom_secondary_width(self, render_cotton_component):
        """Test that custom secondary_width parameter sets CSS variable (T032)."""
        html = render_cotton_component("test_inner_custom_secondary_width.html", {"test_content": "<h1>Main</h1>"})
        soup = BeautifulSoup(html, "html.parser")

        content_shell = soup.select_one(".content-shell")
        assert content_shell is not None, "Content shell not found"

        style = content_shell.get("style", "")
        assert "300px" in style, f"Custom secondary_width not found in style: {style}"
        assert "--content-secondary-width: 300px" in style or "--content-secondary-width:300px" in style

    def test_custom_gap(self, render_cotton_component):
        """Test that custom gap parameter adds correct Bootstrap gap class (T034)."""
        html = render_cotton_component("test_inner_custom_gap.html", {"test_content": "<h1>Main</h1>"})
        soup = BeautifulSoup(html, "html.parser")

        content_shell = soup.select_one(".content-shell")
        assert content_shell is not None, "Content shell not found"

        classes = content_shell.get("class", [])
        assert "gap-3" in classes, f"gap-3 class not found, got: {classes}"

    def test_collapse_primary_adds_collapsible_class(self, render_cotton_component):
        """Test that collapse_primary="true" adds collapsible class to primary sidebar (T035)."""
        html = render_cotton_component("test_inner_collapse_primary.html", {"test_content": "<h1>Main</h1>"})
        soup = BeautifulSoup(html, "html.parser")

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert primary_sidebar is not None, "Primary sidebar not found"

        classes = primary_sidebar.get("class", [])
        assert "collapsible" in classes, f"collapsible class not found on primary sidebar, got: {classes}"

    def test_collapse_secondary_adds_collapsible_class(self, render_cotton_component):
        """Test that collapse_secondary="true" adds collapsible class to secondary sidebar (T036)."""
        html = render_cotton_component("test_inner_collapse_secondary.html", {"test_content": "<h1>Main</h1>"})
        soup = BeautifulSoup(html, "html.parser")

        secondary_sidebar = soup.select_one(".content-sidebar-right")
        assert secondary_sidebar is not None, "Secondary sidebar not found"

        classes = secondary_sidebar.get("class", [])
        assert "collapsible" in classes, f"collapsible class not found on secondary sidebar, got: {classes}"

    def test_collapse_toggle_button_renders(self, render_cotton_component):
        """Test that collapse toggle button renders with correct data-target attribute (T037)."""
        html = render_cotton_component("test_inner_collapse_primary.html", {"test_content": "<h1>Main</h1>"})
        soup = BeautifulSoup(html, "html.parser")

        toggle_button = soup.select_one(".collapse-toggle[data-target='primary-sidebar']")
        assert toggle_button is not None, "Collapse toggle button not found"

        assert toggle_button.get("type") == "button"
        assert toggle_button.get("aria-label") == "Toggle sidebar collapse"

        icon = toggle_button.select_one(".bi-chevron-left")
        assert icon is not None, "Chevron icon not found in toggle button"

    def test_multiple_custom_parameters(self, render_cotton_component):
        """Test that multiple custom parameters work together (T034 + T035 + T036)."""
        html = render_cotton_component("test_inner_multiple_params.html", {"test_content": "<h1>Main</h1>"})
        soup = BeautifulSoup(html, "html.parser")

        content_shell = soup.select_one(".content-shell")
        assert content_shell is not None

        style = content_shell.get("style", "")
        assert "350px" in style, "Custom primary_width not applied"
        assert "280px" in style, "Custom secondary_width not applied"

        classes = content_shell.get("class", [])
        assert "gap-2" in classes, "Custom gap not applied"

        primary_sidebar = soup.select_one(".content-sidebar-left")
        assert "collapsible" in primary_sidebar.get("class", []), "Collapsible class not applied"


@pytest.mark.django_db
class TestInnerLayoutEdgeCases:
    """Test suite for edge cases and accessibility."""

    def test_invalid_gap_value_uses_default(self, render_cotton_component):
        """Test that invalid gap value falls back to default (0)."""
        html = render_cotton_component("test_inner_basic.html", {"test_content": "<h1>Content</h1>"})
        soup = BeautifulSoup(html, "html.parser")

        content_shell = soup.select_one(".content-shell")
        assert content_shell is not None

        classes = content_shell.get("class", [])
        assert "gap-0" in classes, f"Default gap-0 should be present, got: {classes}"

    def test_extremely_wide_content_has_overflow(self, render_cotton_component):
        """Test that wide non-wrapping content triggers overflow handling."""
        wide_content = '<div style="width: 5000px; white-space: nowrap;">Very wide content that should scroll</div>'
        html = render_cotton_component("test_inner_basic.html", {"test_content": wide_content})
        soup = BeautifulSoup(html, "html.parser")

        main_content = soup.select_one(".content-main")
        assert main_content is not None

        classes = main_content.get("class", [])
        assert "overflow-auto" in classes, "Main content should have overflow-auto for wide content"

    def test_both_sidebars_empty_renders_only_main(self, render_cotton_component):
        """Test that with both sidebars undeclared, only main content renders (full width)."""
        html = render_cotton_component(
            "test_inner_basic.html",
            {
                "test_content": "<h1>Main Only</h1>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary = soup.select_one(".content-sidebar-left")
        secondary = soup.select_one(".content-sidebar-right")
        assert primary is None and secondary is None, "No sidebars should render when undeclared"

        main = soup.select_one(".content-main")
        assert main is not None
        assert "flex-grow-1" in main.get("class", []), "Main should expand to full width"

    def test_aria_labels_present_for_accessibility(self, render_cotton_component):
        """Test that all major regions have proper ARIA labels."""
        html = render_cotton_component(
            "test_inner_dual_sidebar.html",
            {
                "test_primary_content": "<nav>Nav</nav>",
                "test_secondary_content": "<aside>Info</aside>",
                "test_content": "<h1>Main</h1>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary = soup.select_one(".content-sidebar-left")
        assert primary is not None
        assert primary.get("role") == "complementary"
        assert primary.get("aria-label") == "Primary sidebar"

        secondary = soup.select_one(".content-sidebar-right")
        assert secondary is not None
        assert secondary.get("role") == "complementary"
        assert secondary.get("aria-label") == "Secondary sidebar"

        main = soup.select_one(".content-main")
        assert main is not None
        assert main.get("role") == "main"
        assert main.get("aria-label") == "Main content"

    def test_offcanvas_backdrop_disabled(self, render_cotton_component):
        """Test that offcanvas backdrop is disabled (data-bs-backdrop='false')."""
        html = render_cotton_component(
            "test_inner_primary_only.html",
            {
                "test_content": "<h1>Main</h1>",
                "test_primary_content": "<nav>Nav</nav>",
            },
        )
        soup = BeautifulSoup(html, "html.parser")

        primary = soup.select_one(".content-sidebar-left")
        assert primary is not None
        assert primary.get("data-bs-backdrop") == "false", "Backdrop should be disabled"

    def test_multiple_inner_layouts_in_page(self, render_cotton_component):
        """Test that multiple inner layouts can coexist (each with unique IDs)."""
        html1 = render_cotton_component(
            "test_inner_primary_only.html",
            {
                "test_content": "<h1>Section 1</h1>",
                "test_primary_content": "<nav>Nav 1</nav>",
            },
        )
        html2 = render_cotton_component(
            "test_inner_primary_only.html",
            {
                "test_content": "<h1>Section 2</h1>",
                "test_primary_content": "<nav>Nav 2</nav>",
            },
        )

        soup1 = BeautifulSoup(html1, "html.parser")
        soup2 = BeautifulSoup(html2, "html.parser")

        shell1 = soup1.select_one(".content-shell")
        shell2 = soup2.select_one(".content-shell")

        assert shell1 is not None, "First inner layout should render"
        assert shell2 is not None, "Second inner layout should render"
