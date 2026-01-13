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
                "icon": "house-door",
            },
        ),
        # Layout Demo with badge showing "New" feature
        MenuItem(
            name="layout_demo",
            view_name="layout_demo",
            extra_context={
                "label": "Layout Demo",
                "icon": "sliders",
                "badge": "New",
                "badge_classes": "text-bg-success",
            },
        ),
        # Profile with notification count
        MenuItem(
            name="profile",
            url="/profile/",
            extra_context={
                "label": "My Profile",
                "icon": "person-circle",
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
    extra_context={"label": "Administration", "icon": "gear-wide-connected", "component_type": "menu.collapse"},
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
                "icon": "shield-lock",
            },
        ),
        MenuItem(
            name="settings",
            url="/admin/settings/",
            extra_context={
                "label": "System Settings",
                "icon": "sliders",
            },
        ),
    ]
)

# Content management with notification badges
content_group = MenuCollapse(
    name="content",
    extra_context={"label": "Content Management", "icon": "file-earmark-text", "component_type": "menu.collapse"},
    parent=AppMenu,
)

content_group.extend(
    [
        MenuItem(
            name="articles",
            url="/content/articles/",
            extra_context={"label": "Articles", "icon": "newspaper", "badge": "12", "badge_classes": "text-bg-primary"},
        ),
        MenuItem(
            name="pages",
            url="/content/pages/",
            extra_context={
                "label": "Pages",
                "icon": "file-text",
            },
        ),
        MenuItem(
            name="media",
            url="/content/media/",
            extra_context={
                "label": "Media Library",
                "icon": "images",
                "badge": "5",
                "badge_classes": "text-bg-warning",
            },
        ),
    ]
)

# =============================================================================
# MENU SECTIONS WITH HEADERS
# =============================================================================
# MenuGroup creates visual section separators

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
                "icon": "arrow-left-right",
            },
        ),
        MenuItem(
            name="backup",
            url="/tools/backup/",
            extra_context={
                "label": "Backup & Restore",
                "icon": "cloud-download",
            },
        ),
        MenuItem(
            name="logs",
            url="/tools/logs/",
            extra_context={
                "label": "System Logs",
                "icon": "file-text",
            },
        ),
    ],
)

# Reports section with nested structure
reports_group = MenuCollapse(
    name="reports",
    extra_context={"label": "Reports & Analytics", "icon": "bar-chart-line", "component_type": "menu.collapse"},
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
                        "icon": "person-check",
                    },
                ),
                MenuItem(
                    name="user_activity",
                    url="/reports/users/activity/",
                    extra_context={
                        "label": "User Activity",
                        "icon": "activity",
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
                "icon": "graph-up",
            },
        ),
        # System Reports
        MenuItem(
            name="system_health",
            url="/reports/system/",
            extra_context={
                "label": "System Health",
                "icon": "heart-pulse",
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
                "icon": "github",
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
