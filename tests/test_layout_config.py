"""Tests for layout configuration options."""

import pytest
from django.template.loader import render_to_string
from django.test import RequestFactory, override_settings


@pytest.mark.django_db
class TestLayoutConfiguration:
    """Test layout configuration rendering."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup request factory for all tests."""
        self.factory = RequestFactory()
        self.request = self.factory.get("/")

    def test_sidebar_layout_only(self):
        """Test sidebar layout: navbar hidden above show_at, sidebar always visible."""
        context = {
            "request": self.request,
            "page_config": {
                "layout": "sidebar",
                "brand": {"text": "Test Brand"},
                "sidebar": {
                    "collapsible": True,
                    "width": "250px",
                    "show_at": "lg",
                },
                "navbar": {
                    "fixed": True,
                    "border": True,
                    "variant": "dark",
                },
            },
        }
        html = render_to_string("layouts/standard.html", context)

        # Both components should be rendered
        assert 'id="page-sidebar"' in html
        assert 'id="page-navbar"' in html
        # Navbar should have d-lg-none class (hidden at lg and above)
        assert "d-lg-none" in html
        # Sidebar should NOT have d-none class
        assert "page-sidebar" in html and "d-none" not in html.split('id="page-sidebar"')[1].split(">")[0]

    def test_navbar_layout_only(self):
        """Test navbar layout: sidebar hidden (d-none), navbar always visible."""
        context = {
            "request": self.request,
            "page_config": {
                "layout": "navbar",
                "brand": {"text": "Test Brand"},
                "sidebar": {
                    "collapsible": True,
                    "width": "250px",
                    "show_at": "lg",
                },
                "navbar": {
                    "fixed": True,
                    "border": True,
                    "variant": "dark",
                    "start": {"navbar.brand": {}},
                    "end": {"navbar.menu": {"menu": "navbar"}},
                },
            },
        }
        html = render_to_string("layouts/standard.html", context)

        # Both components should be rendered
        assert 'id="page-sidebar"' in html
        assert 'id="page-navbar"' in html
        # Sidebar should have d-none class
        sidebar_section = html.split('id="page-sidebar"')[1].split(">")[0]
        assert "d-none" in sidebar_section
        # Navbar should NOT have d-lg-none class
        navbar_section = html.split('id="page-navbar"')[1].split(">")[0]
        assert "d-lg-none" not in navbar_section and "d-md-none" not in navbar_section

    def test_both_layouts_visible(self):
        """Test both layout: both sidebar and navbar visible, navbar components hidden."""
        context = {
            "request": self.request,
            "page_config": {
                "layout": "both",
                "brand": {"text": "Test Brand"},
                "sidebar": {
                    "collapsible": True,
                    "width": "250px",
                    "show_at": "lg",
                },
                "navbar": {
                    "fixed": True,
                    "border": True,
                    "variant": "dark",
                    "start": {"navbar.brand": {}},
                    "end": {"navbar.menu": {"menu": "navbar"}},
                },
            },
        }
        html = render_to_string("layouts/standard.html", context)

        # Both should be rendered
        assert 'id="page-sidebar"' in html
        assert 'id="page-navbar"' in html
        # Neither should have d-none or d-*-none classes for hiding
        sidebar_section = html.split('id="page-sidebar"')[1].split(">")[0]
        navbar_section = html.split('id="page-navbar"')[1].split(">")[0]
        assert "d-none" not in sidebar_section
        assert "d-lg-none" not in navbar_section and "d-md-none" not in navbar_section
        # Navbar brand, menu, and actions should be hidden when layout='both'
        # The navbar.brand component should not be rendered
        assert "navbar.brand" not in html or html.count("navbar.brand") == 0

    def test_default_layout_is_sidebar(self):
        """Test that default layout is 'sidebar' when not specified."""
        from unittest.mock import Mock

        from mvp.context_processors import page_config

        # Mock request
        request = Mock()

        # Mock settings without layout key
        with override_settings(PAGE_CONFIG={"brand": {"text": "Test"}}):
            result = page_config(request)
            assert result["page_config"]["layout"] == "sidebar"

    def test_context_processor_preserves_layout_setting(self):
        """Test that context processor preserves explicit layout setting."""
        from unittest.mock import Mock

        from mvp.context_processors import page_config

        request = Mock()

        # Test with 'both' layout
        with override_settings(PAGE_CONFIG={"layout": "both"}):
            result = page_config(request)
            assert result["page_config"]["layout"] == "both"

        # Test with 'navbar' layout
        with override_settings(PAGE_CONFIG={"layout": "navbar"}):
            result = page_config(request)
            assert result["page_config"]["layout"] == "navbar"

        # Test with 'sidebar' layout
        with override_settings(PAGE_CONFIG={"layout": "sidebar"}):
            result = page_config(request)
            assert result["page_config"]["layout"] == "sidebar"

    def test_main_content_area_always_present(self):
        """Test that main content area is always present regardless of layout."""
        for layout in ["sidebar", "navbar", "both"]:
            context = {
                "request": self.request,
                "page_config": {
                    "layout": layout,
                    "brand": {"text": "Test Brand"},
                    "sidebar": {"collapsible": True, "width": "250px", "show_at": "lg"},
                    "navbar": {
                        "fixed": True,
                        "border": True,
                        "variant": "dark",
                    },
                },
            }
            html = render_to_string("layouts/standard.html", context)

            # Main content structure should always be present
            assert '<div class="col">' in html
            assert "structure.main" in html or "<main" in html


@pytest.mark.django_db
class TestSidebarWidthConfiguration:
    """Test sidebar width configuration features."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup request factory for all tests."""
        self.factory = RequestFactory()
        self.request = self.factory.get("/")

    def test_sidebar_width_css_variable(self):
        """Test that width attribute generates --sidebar-width CSS variable."""
        context = {
            "request": self.request,
            "page_config": {
                "layout": "sidebar",
                "brand": {"text": "Test"},
                "sidebar": {"width": "280px", "show_at": "lg"},
            },
        }
        html = render_to_string("layouts/standard.html", context)
        assert "--sidebar-width: 280px" in html

    def test_sidebar_max_width_css_variable(self):
        """Test that max_width attribute generates --sidebar-max-width CSS variable."""
        context = {
            "request": self.request,
            "page_config": {
                "layout": "sidebar",
                "brand": {"text": "Test"},
                "sidebar": {"max_width": "320px", "show_at": "lg"},
            },
        }
        html = render_to_string("layouts/standard.html", context)
        assert "--sidebar-max-width: 320px" in html

    def test_sidebar_min_width_css_variable(self):
        """Test that min_width attribute generates --sidebar-min-width CSS variable."""
        context = {
            "request": self.request,
            "page_config": {
                "layout": "sidebar",
                "brand": {"text": "Test"},
                "sidebar": {"min_width": "200px", "show_at": "lg"},
            },
        }
        html = render_to_string("layouts/standard.html", context)
        assert "--sidebar-min-width: 200px" in html

    def test_sidebar_multiple_width_variables(self):
        """Test that all width variables can be set together."""
        context = {
            "request": self.request,
            "page_config": {
                "layout": "sidebar",
                "brand": {"text": "Test"},
                "sidebar": {
                    "width": "280px",
                    "max_width": "320px",
                    "min_width": "200px",
                    "show_at": "lg",
                },
            },
        }
        html = render_to_string("layouts/standard.html", context)
        assert "--sidebar-width: 280px" in html
        assert "--sidebar-max-width: 320px" in html
        assert "--sidebar-min-width: 200px" in html
