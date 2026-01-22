"""
Demo views for testing AdminLTE layout configurations.

This view provides an interactive form for testing all layout options:
- Fixed properties (fixed_sidebar, fixed_header, fixed_footer)
- Responsive breakpoints (sidebar_expand)

View uses query parameters for stateless, shareable URL-based configuration.
"""

from django.views.generic import TemplateView

try:
    from django_tables2 import SingleTableView

    from example.models import Product
    from example.tables import ProductTable

    DJANGO_TABLES2_INSTALLED = True
except ImportError:
    DJANGO_TABLES2_INSTALLED = False


class LayoutConfigMixin:
    """
    Mixin that inspects request query parameters for layout configuration.

    Provides standardized layout configuration handling across all demo views.
    Configuration can be controlled via query parameters, allowing shareable URLs
    and dynamic layout switching via the demo sidebar.

    Query Parameters:
        fixed_sidebar (str): 'on' if outer sidebar should be fixed
        fixed_header (str): 'on' if outer header should be fixed
        fixed_footer (str): 'on' if outer footer should be fixed
        sidebar_collapsible (str): 'on' if outer sidebar should be collapsible
        collapsed (str): 'on' if outer sidebar should start collapsed
        fill (str): 'on' if app-wrapper should use fill mode
        sidebar_expand (str): Bootstrap breakpoint for outer sidebar (sm, md, lg, xl, xxl)

        page_fixed_sidebar (str): 'on' if inner sidebar should be sticky
        page_fixed_header (str): 'on' if inner toolbar should be sticky
        page_fixed_footer (str): 'on' if inner footer should be sticky
        page_collapsed (str): 'on' if inner sidebar should start collapsed
        page_sidebar_expand (str): Bootstrap breakpoint for inner sidebar (sm, md, lg, xl, xxl)
        page_layout (str): 6-char layout code (e.g., 'tt-ms-ff')

    Context Variables Added:
        All parsed boolean and string values from query parameters above
    """

    VALID_BREAKPOINTS = ["sm", "md", "lg", "xl", "xxl"]

    def get_context_data(self, **kwargs):
        """Add layout configuration to context from request query parameters."""
        context = super().get_context_data(**kwargs)

        # Outer layout configuration (app-wrapper level)
        context["fixed_sidebar"] = self.request.GET.get("fixed_sidebar") == "on"
        context["fixed_header"] = self.request.GET.get("fixed_header") == "on"
        context["fixed_footer"] = self.request.GET.get("fixed_footer") == "on"
        context["sidebar_collapsible"] = self.request.GET.get("sidebar_collapsible") == "on"
        context["collapsed"] = self.request.GET.get("collapsed") == "on"
        context["fill"] = self.request.GET.get("fill") == "on"

        # Parse outer sidebar breakpoint with fallback to 'lg'
        sidebar_expand = self.request.GET.get("sidebar_expand", self.request.GET.get("breakpoint", "lg"))
        if sidebar_expand not in self.VALID_BREAKPOINTS:
            sidebar_expand = "lg"
        context["sidebar_expand"] = sidebar_expand
        context["breakpoint"] = sidebar_expand  # For compatibility
        context["breakpoints"] = self.VALID_BREAKPOINTS

        # Inner layout configuration (page-layout level)
        context["page_fixed_sidebar"] = self.request.GET.get("page_fixed_sidebar") == "on"
        context["page_fixed_header"] = self.request.GET.get("page_fixed_header") == "on"
        context["page_fixed_footer"] = self.request.GET.get("page_fixed_footer") == "on"
        context["page_collapsed"] = self.request.GET.get("page_collapsed") == "on"

        # Parse inner sidebar breakpoint with fallback to 'lg'
        page_sidebar_expand = self.request.GET.get("page_sidebar_expand", "lg")
        if page_sidebar_expand not in self.VALID_BREAKPOINTS:
            page_sidebar_expand = "lg"
        context["page_sidebar_expand"] = page_sidebar_expand

        # Parse page layout code (e.g., 'tt-ms-ff')
        context["page_layout"] = self.request.GET.get("page_layout", "")

        return context


class LayoutDemoView(LayoutConfigMixin, TemplateView):
    """
    Unified layout demo view for testing all AdminLTE layout configurations.

    User Story 4: Interactive Layout Configuration Demo Page

    Features:
        - Interactive configuration form (right sidebar)
        - Real-time layout updates via query parameters
        - URL-based configuration (shareable links)
        - Bootstrap responsive breakpoint testing

    Template: example/layout_demo.html
    URL Pattern: /layout/
    """

    template_name = "example/layout_demo.html"


class NavbarWidgetsView(LayoutConfigMixin, TemplateView):
    """
    Navbar widgets demonstration page.

    Shows all navbar widget components with usage examples and documentation.
    Widgets are displayed in the navbar header (top right).

    Template: example/navbar_widgets.html
    URL Pattern: /widgets/
    """

    template_name = "example/navbar_widgets.html"

    def get_context_data(self, **kwargs):
        """Add navbar widget sample data to context."""
        context = super().get_context_data(**kwargs)

        # Sample notifications data
        notifications = [
            {"text": "You have 3 new friend requests", "time": "2 mins ago"},
            {"text": "Server maintenance scheduled", "time": "10 mins ago"},
            {"text": "Your password expires soon", "time": "1 hour ago"},
            {"text": "New comment on your post", "time": "3 hours ago"},
            {"text": "Weekly report is ready", "time": "Yesterday"},
            {"text": "Backup completed successfully", "time": "2 days ago"},
            {"text": "System update available", "time": "3 days ago"},
        ]

        context["notifications_count"] = len(notifications)
        context["notifications"] = notifications

        return context


class PageLayoutDemoView(LayoutConfigMixin, TemplateView):
    """
    Inner layout demonstration page.

    Interactive form for testing all inner layout options:
    - Fixed properties (fixed_header, fixed_footer, fixed_sidebar)
    - Responsive breakpoints (sidebar_expand)
    - Initial sidebar state (collapsed)
    - Layout variants (6-char layout codes)

    Template: example/page_layout.html
    URL Pattern: /page-layout/
    """

    template_name = "example/page_layout.html"


# Compatibility functions for URL patterns
layout_demo = LayoutDemoView.as_view()
navbar_widgets_demo = NavbarWidgetsView.as_view()
page_layout_demo = PageLayoutDemoView.as_view()


if DJANGO_TABLES2_INSTALLED:

    class DataTablesView(LayoutConfigMixin, SingleTableView):
        """Django Tables2 demo page showing Product table with sorting and pagination.

        User Story 2: Viewing DataTables Demo Page

        Features:
            - Product data table with 18 columns
            - Bootstrap 5 responsive styling
            - Sortable columns
            - Pagination (25 items per page)
            - Empty state message
            - Layout configuration via query parameters

        Template: example/datatables_demo.html
        URL Pattern: /datatables-demo/
        """

        model = Product
        table_class = ProductTable
        template_name = "example/datatables_demo.html"
        paginate_by = 25
