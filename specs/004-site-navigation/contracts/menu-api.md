# API Contract: Menu and MenuItem Classes

**Feature**: 004-site-navigation
**Date**: January 7, 2026
**Purpose**: Define Python API for menu definition using django-flex-menus

## Overview

Django-mvp provides a pre-configured `AppMenu` instance that users extend by importing and adding `MenuItem` instances. This contract documents the public API provided by django-flex-menus that users will interact with.

## AppMenu Instance

### Location

```python
# Defined in mvp/menus.py
from flex_menu import Menu

# Pre-configured empty menu that users extend
AppMenu = Menu("AppMenu", children=[])
```

### Public Interface

```python
from mvp.menus import AppMenu

# Type: flex_menu.Menu (subclass of anytree.Node)
# Properties (inherited from Menu):
#   - name: str - Identifier ("AppMenu")
#   - children: List[MenuItem] - Top-level menu items (initially empty)
#   - parent: None - Root menu has no parent
```

### Usage Patterns

#### Pattern 1: Add Single Item Using parent Parameter

```python
from mvp.menus import AppMenu
from flex_menu import MenuItem

MenuItem(
    name="home",
    view_name="app:home",
    extra_context={"label": "Home", "icon": "house"},

)
```

#### Pattern 2: Add Multiple Items Sequentially

```python
from mvp.menus import AppMenu
from flex_menu import MenuItem

MenuItem(name="dashboard", view_name="app:dashboard",
         extra_context={"label": "Dashboard", "icon": "speedometer"},
         )
MenuItem(name="profile", view_name="app:profile",
         extra_context={"label": "Profile", "icon": "person-circle"},
         )
```

#### Pattern 3: Modify Existing Item

```python
from mvp.menus import AppMenu

# Access existing menu items
for item in AppMenu.children:
    if item.name == "home":
        item.extra_context["label"] = "Homepage"
```

## MenuItem Class

### Constructor Signature

```python
from flex_menu import MenuItem

def __init__(
    self,
    name: str,                           # Required: Unique identifier
    view_name: str | None = None,        # Optional: Django URL name
    extra_context: dict | None = None,   # Optional: Custom rendering data
    template_name: str | None = None,    # Optional: Custom template override
    children: List['MenuItem'] | None = None,  # Optional: Nested items
    parent: 'BaseMenu' | None = None,    # Optional: Parent node (auto-set by anytree)
    **kwargs                              # Additional anytree.Node parameters
) -> MenuItem
```

### Parameter Specifications

#### `name` (required)

- **Type**: `str`
- **Purpose**: Unique identifier within parent scope
- **Constraints**:
  - Must be unique among siblings
  - Should be valid Python identifier (for introspection/debugging)
  - Recommended: snake_case (e.g., `"admin_users"`, `"reports_dashboard"`)
- **Examples**: `"home"`, `"user_profile"`, `"admin_settings"`

#### `view_name` (optional)

- **Type**: `str | None`
- **Default**: `None`
- **Purpose**: Django URL name for reverse resolution
- **Format**: `"app_name:view_name"` or `"view_name"`
- **Special values**:
  - `"#"` - Non-clickable item (typically parent with children)
  - `None` - No URL (item won't be clickable unless template overrides)
- **Examples**:
  - `"myapp:dashboard"`
  - `"admin:index"`
  - `"#"` (for group headers)

#### `extra_context` (optional)

- **Type**: `dict | None`
- **Default**: `None`
- **Purpose**: Custom data passed to templates as context variables
- **Common keys** (all optional):
  - `label` (str): Display text for menu item
  - `icon` (str): Icon name for django-easy-icons
  - `icon_set` (str): Override default icon set
  - `classes` (str): Additional CSS classes for `<li>` element
  - `link_classes` (str): Additional CSS classes for `<a>` element
  - `badge` (str): Badge text/number
  - `badge_classes` (str): Badge styling classes
  - `group_header` (str): Header text to display before item (for grouping)
  - `url_params` (dict): Static URL parameters
  - Any custom keys needed for specialized templates

#### `template_name` (optional)

- **Type**: `str | None`
- **Default**: `None`
- **Purpose**: Override default renderer template for this item
- **Format**: Django template path (e.g., `"menus/custom-item.html"`)
- **Use case**: Specialized menu items with unique rendering needs

#### `children` (optional)

- **Type**: `List[MenuItem] | None`
- **Default**: `None`
- **Purpose**: Nested menu items (creates hierarchical structure)
- **Behavior**: Items with children are rendered as expandable/collapsible sections

### Return Value

- **Type**: `MenuItem` instance
- **Inheritance**: Inherits from `flex_menu.menu.BaseMenu`, which inherits from `anytree.Node`
- **Tree operations**: Supports all anytree operations (ancestors, descendants, siblings, etc.)

## Usage Examples

### Example 1: Simple Menu Item

```python
from flex_menu import MenuItem

home_item = MenuItem(
    name="home",
    view_name="app:home",
    extra_context={
        "label": "Home",
        "icon": "house"
    }
)
```

**Expected behavior**:

- Renders as clickable link
- URL resolved from `"app:home"` via Django's reverse()
- Displays "Home" text with house icon
- Appears at top of menu (single item, no children)

### Example 2: Parent with Children (Hierarchical)

```python
from flex_menu import MenuItem

admin_section = MenuItem(
    name="admin",
    view_name="#",  # Not clickable itself
    extra_context={
        "label": "Administration",
        "icon": "gear",
        "group_header": "ADMIN TOOLS"  # Section header
    },
    children=[
        MenuItem(
            name="users",
            view_name="app:admin_users",
            extra_context={"label": "User Management", "icon": "people"}
        ),
        MenuItem(
            name="settings",
            view_name="app:admin_settings",
            extra_context={"label": "Settings", "icon": "sliders"}
        ),
    ]
)
```

**Expected behavior**:

- "ADMIN TOOLS" header rendered above section
- Parent "Administration" item rendered with expand/collapse arrow
- Children "User Management" and "Settings" nested underneath
- Section appears after all single items
- Children visible when parent expanded

### Example 3: Item with Badge

```python
from flex_menu import MenuItem

notifications_item = MenuItem(
    name="notifications",
    view_name="app:notifications",
    extra_context={
        "label": "Notifications",
        "icon": "bell",
        "badge": "5",
        "badge_classes": "text-bg-danger"
    }
)
```

**Expected behavior**:

- Displays "Notifications" with bell icon
- Red badge showing "5" appears next to label
- Clicking navigates to notifications page

### Example 4: Parameterized URL

```python
from flex_menu import MenuItem

# Menu definition
profile_item = MenuItem(
    name="profile",
    view_name="app:user_profile",  # Requires 'username' parameter
    extra_context={
        "label": "My Profile",
        "icon": "person-circle"
    }
)

# Template rendering (pass parameter)
{% render_menu 'AppMenu' renderer='adminlte' username=request.user.username %}
```

**Expected behavior**:

- URL resolved as `/profile/john/` (if username="john")
- Parameters automatically extracted from render context
- Item only visible if parameter available

### Example 5: Deep Nesting

```python
from flex_menu import MenuItem

reports = MenuItem(
    name="reports",
    view_name="#",
    extra_context={"label": "Reports", "icon": "file-text"},
    children=[
        MenuItem(
            name="financial",
            view_name="#",
            extra_context={"label": "Financial"},
            children=[
                MenuItem(name="revenue", view_name="app:report_revenue",
                        extra_context={"label": "Revenue"}),
                MenuItem(name="expenses", view_name="app:report_expenses",
                        extra_context={"label": "Expenses"}),
            ]
        ),
        MenuItem(name="operational", view_name="app:report_operational",
                extra_context={"label": "Operational"}),
    ]
)
```

**Expected behavior**:

- Three levels of nesting: Reports → Financial → Revenue/Expenses
- Each level expandable/collapsible independently
- Proper indentation and visual hierarchy
- Renderer uses nested templates for depth 2+

## Integration Points

### Where to Define Menu Items

**Recommended location**: `yourapp/menus.py`

```python
# myapp/menus.py
from mvp.menus import AppMenu
from flex_menu import MenuItem

# Add items during module import
AppMenu.children.extend([
    MenuItem(name="home", view_name="myapp:home",
             extra_context={"label": "Home", "icon": "house"}),
    # ... more items
])
```

**Import in `yourapp/apps.py`** to ensure menus load:

```python
# myapp/apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # Import menus to register items
        from . import menus  # noqa: F401
```

### Rendering in Templates

```django
{# In base template or sidebar component #}
{% load flex_menu %}
{% render_menu 'AppMenu' renderer='adminlte' %}
```

## Validation and Error Handling

### Validation Performed by anytree

- **Circular references**: Prevented automatically
- **Duplicate names**: Not enforced by anytree, but recommended to avoid confusion
- **Parent-child consistency**: Enforced (parent attribute auto-updated)

### Expected Errors

#### NoReverseMatch (Django)

```python
MenuItem(name="broken", view_name="nonexistent:view", ...)
# Raises NoReverseMatch when menu renders
```

**Prevention**: Ensure view_name matches URL patterns

#### KeyError (Template)

```python
MenuItem(name="test", view_name="app:home", extra_context={})
# Template expects c_label but extra_context doesn't have "label"
```

**Prevention**: Always include expected keys in extra_context, or use template defaults

## Type Hints (for Type Checking)

```python
from typing import List, Optional, Dict, Any
from flex_menu import Menu, MenuItem

# Menu definition with type hints
def create_menu() -> Menu:
    return Menu(
        "MyMenu",
        children=[
            MenuItem(
                name=str,
                view_name=Optional[str],
                extra_context=Optional[Dict[str, Any]],
                children=Optional[List[MenuItem]]
            )
        ]
    )

# AppMenu usage
from mvp.menus import AppMenu
AppMenu: Menu  # Type annotation for IDE support
```

## Summary

The Menu/MenuItem API contract defines:

1. **AppMenu**: Pre-configured Menu instance in `mvp.menus`, initially empty
2. **MenuItem**: Django-flex-menus class for defining menu items with:
   - `name` (required): Unique identifier
   - `view_name` (optional): Django URL name
   - `extra_context` (optional): Custom template data
   - `children` (optional): Nested items
3. **Usage**: Import AppMenu, append/extend with MenuItem instances
4. **Rendering**: Via `{% render_menu 'AppMenu' renderer='adminlte' %}` template tag

All items follow django-flex-menus API (inherited from BaseMenu/anytree.Node).
