"""
Demo views for testing AdminLTE layout configurations.

This view provides an interactive form for testing all layout options:
- Fixed properties (fixed_sidebar, fixed_header, fixed_footer)
- Responsive breakpoints (sidebar_expand)

View uses query parameters for stateless, shareable URL-based configuration.
"""

from django.shortcuts import render


def layout_demo(request):
    """
    Unified layout demo view for testing all AdminLTE layout configurations.

    User Story 4: Interactive Layout Configuration Demo Page

    Query Parameters:
        fixed_sidebar (str): 'on' if checkbox is checked
        fixed_header (str): 'on' if checkbox is checked
        fixed_footer (str): 'on' if checkbox is checked
        breakpoint (str): Bootstrap breakpoint (sm, md, lg, xl, xxl)
                         Defaults to 'lg' if not provided or invalid

    Returns:
        Rendered template with configuration form (right sidebar) and
        layout demonstration (main content area)

    Template Structure:
        - Left column (col-lg-8): Main content with demo information
        - Right column (col-lg-4): Configuration form with checkboxes and dropdown

    Context Variables:
        - fixed_sidebar (bool): Whether sidebar should be fixed
        - fixed_header (bool): Whether header should be fixed
        - fixed_footer (bool): Whether footer should be fixed
        - breakpoint (str): Current sidebar expansion breakpoint
        - breakpoints (list): Available breakpoint options
    """
    # Valid Bootstrap breakpoint values
    VALID_BREAKPOINTS = ["sm", "md", "lg", "xl", "xxl"]

    # Parse query parameters (checkboxes send 'on' when checked, absent when unchecked)
    fixed_sidebar = request.GET.get("fixed_sidebar") == "on"
    fixed_header = request.GET.get("fixed_header") == "on"
    fixed_footer = request.GET.get("fixed_footer") == "on"
    sidebar_collapsible = request.GET.get("sidebar_collapsible") == "on"
    collapsed = request.GET.get("collapsed") == "on"

    # Parse breakpoint with fallback to default 'lg' (support both parameter names)
    sidebar_breakpoint = request.GET.get("sidebar_expand", request.GET.get("breakpoint", "lg"))
    if sidebar_breakpoint not in VALID_BREAKPOINTS:
        sidebar_breakpoint = "lg"  # Fallback to default

    context = {
        "fixed_sidebar": fixed_sidebar,
        "fixed_header": fixed_header,
        "fixed_footer": fixed_footer,
        "sidebar_collapsible": sidebar_collapsible,
        "collapsed": collapsed,
        "breakpoint": sidebar_breakpoint,
        "sidebar_expand": sidebar_breakpoint,  # For compatibility with tests
        "breakpoints": VALID_BREAKPOINTS,
    }

    return render(request, "example/layout_demo.html", context)
