"""Example menu configuration showing all django-mvp menu features.

This file demonstrates how to use the AppMenu system to create comprehensive
navigation menus with all available features:

- Single menu items with icons
- Hierarchical menu groups and sections
- Badge support for notifications
- Active state detection
- URL resolution (view names and direct URLs)
- Multi-level nesting
- Menu sections with headers
"""

from flex_menu import MenuItem

from mvp.menus import AppMenu, MenuCollapse, MenuGroup

# =============================================================================
# SINGLE MENU ITEMS
# =============================================================================
# Single items appear at the top of the menu before any groups

AppMenu.extend(
    [
        # Dashboard - main entry point
        MenuItem(
            name="dashboard",
            view_name="dashboard",
            extra_context={
                "label": "Dashboard",
                "icon": "house",
            },
        ),
        # Layout Demo with badge showing "New" feature
        MenuItem(
            name="layout_demo",
            view_name="layout_demo",
            extra_context={
                "label": "Layout Demo",
                "icon": "box-seam",
                "badge": "New",
                "badge_classes": "text-bg-success",
            },
        ),
        # Navbar Widgets Demo
        MenuItem(
            name="navbar_widgets_demo",
            view_name="navbar_widgets_demo",
            extra_context={
                "label": "Navbar Widgets",
                "icon": "grid",
                "badge": "MVP",
                "badge_classes": "text-bg-primary",
            },
        ),
        MenuItem(
            name="page_layout_demo",
            view_name="page_layout_demo",
            extra_context={
                "label": "Inner Layout",
                "icon": "sidebar",
            },
        ),
        MenuItem(
            name="list_view_demo",
            view_name="list_view_demo",
            extra_context={
                "label": "MVP List View",
                "icon": "list",
            },
        ),
        MenuItem(
            name="form_view_demo",
            view_name="form_view_demo",
            extra_context={
                "label": "MVP Form View",
                "icon": "form",
            },
        ),
        MenuItem(
            name="profile",
            url="/profile/",
            extra_context={
                "label": "My Profile",
                "icon": "add",
                "badge": "2",
                "badge_classes": "text-bg-info",
            },
        ),
    ]
)

# =============================================================================
# HIERARCHICAL MENU GROUPS
# =============================================================================
# Groups appear after single items and contain related functionality

# Administration section with nested items
admin_group = MenuCollapse(
    name="administration",
    extra_context={"label": "Administration", "icon": "briefcase", "component_type": "menu.collapse"},
    parent=AppMenu,
)

# Add admin sub-items
admin_group.extend(
    [
        MenuItem(
            name="users",
            url="/admin/users/",
            extra_context={
                "label": "User Management",
                "icon": "people",
            },
        ),
        MenuItem(
            name="permissions",
            url="/admin/permissions/",
            extra_context={
                "label": "Permissions",
                "icon": "briefcase",
            },
        ),
        MenuItem(
            name="settings",
            url="/admin/settings/",
            extra_context={
                "label": "System Settings",
                "icon": "box-seam",
            },
        ),
    ]
)

# Content management with notification badges
content_group = MenuCollapse(
    name="content",
    extra_context={"label": "Content Management", "icon": "book", "component_type": "menu.collapse"},
    parent=AppMenu,
)

content_group.extend(
    [
        MenuItem(
            name="articles",
            url="/content/articles/",
            extra_context={"label": "Articles", "icon": "book", "badge": "12", "badge_classes": "text-bg-primary"},
        ),
        MenuItem(
            name="pages",
            url="/content/pages/",
            extra_context={
                "label": "Pages",
                "icon": "book",
            },
        ),
        MenuItem(
            name="media",
            url="/content/media/",
            extra_context={
                "label": "Media Library",
                "icon": "book",
                "badge": "5",
                "badge_classes": "text-bg-warning",
            },
        ),
    ]
)

# =============================================================================
# LIST VIEW DEMOS SECTION
# =============================================================================
# Dashboard list view demos showcasing different configurations

list_views_group = MenuCollapse(
    name="list_views",
    extra_context={"label": "List Views", "icon": "list", "component_type": "menu.collapse"},
    parent=AppMenu,
)

list_views_group.extend(
    [
        MenuItem(
            name="list_view_full_demo",
            view_name="list_view_demo",
            extra_context={
                "label": "Full Demo",
                "icon": "list",
                "badge": "All Features",
                "badge_classes": "text-bg-primary",
            },
        ),
        MenuItem(
            name="basic_list_demo",
            view_name="basic_list_demo",
            extra_context={
                "label": "Basic ListView",
                "icon": "list",
            },
        ),
        MenuItem(
            name="minimal_list_demo",
            view_name="minimal_list_demo",
            extra_context={
                "label": "Minimal",
                "icon": "list",
            },
        ),
    ]
)

# Grid layout demos
grid_layouts_group = MenuCollapse(
    name="grid_layouts",
    extra_context={"label": "Grid Layouts", "icon": "grid", "component_type": "menu.collapse"},
    parent=AppMenu,
)

grid_layouts_group.extend(
    [
        MenuItem(
            name="grid_1col_demo",
            view_name="grid_demo_1col",
            extra_context={
                "label": "1 Column",
                "icon": "grid",
            },
        ),
        MenuItem(
            name="grid_2col_demo",
            view_name="grid_demo_2col",
            extra_context={
                "label": "2 Columns",
                "icon": "grid",
            },
        ),
        MenuItem(
            name="grid_3col_demo",
            view_name="grid_demo_3col",
            extra_context={
                "label": "3 Columns",
                "icon": "grid",
            },
        ),
        MenuItem(
            name="grid_responsive_demo",
            view_name="grid_demo_responsive",
            extra_context={
                "label": "Responsive",
                "icon": "grid",
                "badge": "Adaptive",
                "badge_classes": "text-bg-success",
            },
        ),
    ]
)

# =============================================================================
# MENU SECTIONS WITH HEADERS
# =============================================================================
# MenuGroup creates visual section separators

# Integrations section - Third-party library integrations
integrations_section = MenuGroup(
    name="integrations_section",
    extra_context={"label": "INTEGRATIONS", "component_type": "menu.group"},
    parent=AppMenu,
)

# Django Tables2 integration (conditional - only shows if django-tables2 is installed)
try:
    from django_tables2 import Table  # noqa: F401

    integrations_section.append(
        MenuItem(
            name="datatables_demo",
            view_name="datatables_demo",
            extra_context={
                "label": "DataTables Demo",
                "icon": "table",
                "badge": "New",
                "badge_classes": "text-bg-primary",
            },
        )
    )
except ImportError:
    pass

# Tools section
MenuGroup(
    name="tools_section",
    extra_context={"label": "TOOLS & UTILITIES", "component_type": "menu.group"},
    parent=AppMenu,
    children=[
        MenuItem(
            name="import_export",
            url="/tools/import-export/",
            extra_context={
                "label": "Import/Export",
                "icon": "add",
            },
        ),
        MenuItem(
            name="backup",
            url="/tools/backup/",
            extra_context={
                "label": "Backup & Restore",
                "icon": "add",
            },
        ),
        MenuItem(
            name="logs",
            url="/tools/logs/",
            extra_context={
                "label": "System Logs",
                "icon": "book",
            },
        ),
    ],
)

# Reports section with nested structure
reports_group = MenuCollapse(
    name="reports",
    extra_context={"label": "Reports & Analytics", "icon": "briefcase", "component_type": "menu.collapse"},
    parent=AppMenu,
)

# Add nested report categories
reports_group.extend(
    [
        # User Reports sub-section
        MenuCollapse(
            name="user_reports",
            extra_context={"label": "User Reports", "icon": "people", "component_type": "menu.collapse"},
            parent=reports_group,
            children=[
                MenuItem(
                    name="active_users",
                    url="/reports/users/active/",
                    extra_context={
                        "label": "Active Users",
                        "icon": "add",
                    },
                ),
                MenuItem(
                    name="user_activity",
                    url="/reports/users/activity/",
                    extra_context={
                        "label": "User Activity",
                        "icon": "add",
                        "badge": "Live",
                        "badge_classes": "text-bg-success",
                    },
                ),
            ],
        ),
        # Content Reports
        MenuItem(
            name="content_stats",
            url="/reports/content/",
            extra_context={
                "label": "Content Statistics",
                "icon": "add",
            },
        ),
        # System Reports
        MenuItem(
            name="system_health",
            url="/reports/system/",
            extra_context={
                "label": "System Health",
                "icon": "add",
                "badge": "OK",
                "badge_classes": "text-bg-success",
            },
        ),
    ]
)

# =============================================================================
# EXAMPLES SECTION
# =============================================================================
# Demonstration of various menu patterns

MenuGroup(
    name="examples_section",
    extra_context={"label": "EXAMPLES", "component_type": "menu.group"},
    parent=AppMenu,
    children=[
        MenuItem(
            name="external_link",
            url="https://github.com/example/django-mvp",
            extra_context={
                "label": "GitHub Repository",
                "icon": "add",
            },
        ),
        MenuItem(
            name="documentation",
            url="https://django-mvp.readthedocs.io/",
            extra_context={
                "label": "Documentation",
                "icon": "book",
            },
        ),
        MenuItem(
            name="api_docs",
            url="/api/docs/",
            extra_context={
                "label": "API Documentation",
                "icon": "code-slash",
                "badge": "v1.0",
                "badge_classes": "text-bg-secondary",
            },
        ),
    ],
)

# =============================================================================
# BEST PRACTICES DEMONSTRATED
# =============================================================================
"""
This example demonstrates:

1. **Organization**: Single items first, then groups
2. **Icons**: Consistent icon usage with Bootstrap Icons
3. **Badges**: Various badge styles and use cases
4. **Nesting**: Multi-level menu hierarchies
5. **URLs**: Mix of view_name and direct URL approaches
6. **Sections**: Visual grouping with MenuGroup headers
7. **Labels**: Clear, descriptive menu labels
8. **Structure**: Logical organization of related features

Usage in your own app:
1. Import AppMenu: `from mvp.menus import AppMenu`
2. Add items: `AppMenu.extend([MenuItem(...)])`
3. Or create groups: `MenuCollapse(..., parent=AppMenu)`
4. Configure in apps.py ready() method for auto-loading
"""
