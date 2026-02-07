# Quickstart: Site Navigation Menu System

**Feature**: 004-site-navigation
**Audience**: Django developers using django-mvp
**Goal**: Define and render custom navigation menus in 5 minutes

## What You'll Build

A sidebar navigation menu with:

- Single menu items (Dashboard, Profile)
- Grouped menu sections (Admin Tools)
- Icons, badges, and active state highlighting

## Prerequisites

- Django project with django-mvp installed
- Basic familiarity with Django URLs and views

## Step 1: Create Your Menu Module

Create `yourapp/menus.py`:

```python
from mvp.menus import AppMenu
from flex_menu import MenuItem

# Add menu items to AppMenu using parent parameter
MenuItem(
    name="dashboard",
    view_name="yourapp:dashboard",
    extra_context={
        "label": "Dashboard",
        "icon": "speedometer"
    },

)

MenuItem(
    name="profile",
    view_name="yourapp:profile",
    extra_context={
        "label": "My Profile",
        "icon": "person-circle"
    },

)

# Group item (appears after singles)
MenuItem(
    name="admin",
    view_name="#",  # Not clickable
    extra_context={
        "label": "Administration",
        "icon": "gear",
        "group_header": "ADMIN TOOLS"  # Section header
    },
    ,
    children=[
        MenuItem(
            name="users",
            view_name="yourapp:admin_users",
            extra_context={
                "label": "User Management",
                "icon": "people"
            }
        ),
        MenuItem(
            name="settings",
            view_name="yourapp:admin_settings",
            extra_context={
                "label": "Settings",
                "icon": "sliders"
            }
        ),
    ]
)
```

## Step 2: Import Menu in AppConfig

Edit `yourapp/apps.py`:

```python
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yourapp'

    def ready(self):
        # Import menus to register items
        from . import menus  # noqa: F401
```

## Step 3: That's It

The menu automatically renders in the sidebar. The `mvp/templates/mvp/base.html` template includes:

```django
{% load flex_menu %}
{% render_menu 'AppMenu' renderer='adminlte' %}
```

(Located in the `app_sidebar` block) - No template modifications needed!

## Result

Your sidebar now shows:

```
┌─────────────────────────┐
│ [🏠] Dashboard          │
│ [👤] My Profile         │
│                         │
│ ADMIN TOOLS             │
│ [⚙️] Administration ▶   │
│   [👥] User Management  │
│   [🎚️] Settings         │
└─────────────────────────┘
```

## Common Patterns

### Adding a Badge

Show notification count:

```python
MenuItem(
    name="messages",
    view_name="yourapp:messages",
    extra_context={
        "label": "Messages",
        "icon": "envelope",
        "badge": "3",
        "badge_classes": "text-bg-danger"
    }
)
```

### Nested Menus (Multi-Level)

Create deeper hierarchies:

```python
MenuItem(
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
                        extra_context={"label": "Revenue Report"}),
                MenuItem(name="expenses", view_name="app:report_expenses",
                        extra_context={"label": "Expenses Report"}),
            ]
        ),
    ]
)
```

### Multiple Apps Contributing Menus

Each app can add items. Order follows `INSTALLED_APPS`:

```python
# app1/menus.py
from mvp.menus import AppMenu
from flex_menu import MenuItem

AppMenu.children.append(
    MenuItem(name="app1_home", view_name="app1:home",
             extra_context={"label": "App 1 Home"})
)

# app2/menus.py
from mvp.menus import AppMenu
from flex_menu import MenuItem

AppMenu.children.append(
    MenuItem(name="app2_home", view_name="app2:home",
             extra_context={"label": "App 2 Home"})
)
```

Result depends on `INSTALLED_APPS` order:

```python
INSTALLED_APPS = [
    'app1',  # app1 items appear first
    'app2',  # app2 items appear second
]
```

### Parameterized URLs

For views requiring parameters:

```python
# Menu definition (no parameters)
MenuItem(
    name="user_detail",
    view_name="yourapp:user_detail",  # Expects 'pk' parameter
    extra_context={"label": "User Profile"}
)

# Template rendering (pass parameter)
{% render_menu 'AppMenu' renderer='adminlte' pk=user.pk %}
```

### Custom CSS Classes

Add styling to specific items:

```python
MenuItem(
    name="important",
    view_name="yourapp:important",
    extra_context={
        "label": "Important Section",
        "icon": "exclamation-triangle",
        "classes": "border-start border-danger",  # Custom li styling
        "link_classes": "text-danger fw-bold"     # Custom link styling
    }
)
```

## Menu Structure Rules

1. **Single items render first**: Items without `children` appear at top
2. **Groups render after**: Items with `children` appear below singles
3. **Group headers**: Use `group_header` in `extra_context` to add section label
4. **Declaration order preserved**: Items appear in the order added (within singles/groups)

## Icon Reference

Django-mvp uses Bootstrap Icons via django-easy-icons. Common icons:

| Icon Name | Visual | Usage |
|-----------|--------|-------|
| `house` | 🏠 | Home |
| `speedometer` | 🚀 | Dashboard |
| `person-circle` | 👤 | Profile |
| `gear` | ⚙️ | Settings |
| `people` | 👥 | Users |
| `file-text` | 📄 | Documents |
| `envelope` | ✉️ | Messages |
| `bell` | 🔔 | Notifications |
| `calendar` | 📅 | Calendar |
| `bar-chart` | 📊 | Reports |

Full icon list: <https://icons.getbootstrap.com/>

## Active State

Current page automatically highlighted:

- **Active detection**: Compares current URL name with `view_name`
- **Visual feedback**: `.active` class adds highlighting
- **Parent expansion**: Parents with active children automatically open

No manual active state management needed!

## Troubleshooting

### Menu Items Don't Appear

**Problem**: Sidebar is empty

**Solutions**:

1. Check `menus.py` is imported in `apps.py` `ready()` method
2. Verify app is in `INSTALLED_APPS`
3. Check for Python errors in `menus.py`

### NoReverseMatch Error

**Problem**: `NoReverseMatch at /: Reverse for 'view_name' not found`

**Solutions**:

1. Verify `view_name` matches URL pattern name
2. Check URL namespace (use `"app_name:view_name"` format)
3. For parameterized URLs, pass parameters in template tag

### Icons Don't Show

**Problem**: Icons missing or show as boxes

**Solutions**:

1. Ensure django-easy-icons is in `INSTALLED_APPS`
2. Check AdminLTE CSS is loaded (should include Bootstrap Icons)
3. Verify icon name is valid Bootstrap Icons name

### Menu Order Wrong

**Problem**: Items appear in unexpected order

**Solutions**:

1. Check `INSTALLED_APPS` order (determines app menu order)
2. Verify singles vs groups (singles always first, groups after)
3. Check declaration order within each `extend()` or `append()`

## Next Steps

- **Customize styling**: Add custom CSS classes via `classes` and `link_classes`
- **Add permissions**: Use `extra_context` to store permission requirements (filter in custom renderer)
- **Dynamic badges**: Calculate badge values in template context
- **Custom templates**: Override default templates for specialized menu items

## Full Example

Complete `yourapp/menus.py` with all features:

```python
from mvp.menus import AppMenu
from flex_menu import MenuItem

AppMenu.children.extend([
    # Single items
    MenuItem(
        name="dashboard",
        view_name="yourapp:dashboard",
        extra_context={
            "label": "Dashboard",
            "icon": "speedometer",
            "badge": "2",
            "badge_classes": "text-bg-warning"
        }
    ),
    MenuItem(
        name="messages",
        view_name="yourapp:messages",
        extra_context={
            "label": "Messages",
            "icon": "envelope",
            "badge": "5",
            "badge_classes": "text-bg-danger"
        }
    ),

    # Admin group
    MenuItem(
        name="admin",
        view_name="#",
        extra_context={
            "label": "Administration",
            "icon": "gear",
            "group_header": "ADMIN"
        },
        children=[
            MenuItem(
                name="users",
                view_name="yourapp:admin_users",
                extra_context={"label": "Users", "icon": "people"}
            ),
            MenuItem(
                name="roles",
                view_name="yourapp:admin_roles",
                extra_context={"label": "Roles", "icon": "shield"}
            ),
            MenuItem(
                name="audit",
                view_name="yourapp:admin_audit",
                extra_context={"label": "Audit Log", "icon": "list"}
            ),
        ]
    ),

    # Reports group
    MenuItem(
        name="reports",
        view_name="#",
        extra_context={
            "label": "Reports",
            "icon": "bar-chart",
            "group_header": "ANALYTICS"
        },
        children=[
            MenuItem(
                name="revenue",
                view_name="yourapp:report_revenue",
                extra_context={"label": "Revenue", "icon": "cash"}
            ),
            MenuItem(
                name="users_report",
                view_name="yourapp:report_users",
                extra_context={"label": "Users", "icon": "people"}
            ),
        ]
    ),

    # Single item at end (still renders before groups!)
    MenuItem(
        name="help",
        view_name="yourapp:help",
        extra_context={
            "label": "Help",
            "icon": "question-circle"
        }
    ),
])
```

**Rendered order**:

1. Dashboard (single)
2. Messages (single)
3. Help (single)
4. ADMIN header + Administration group
5. ANALYTICS header + Reports group

## Summary

**Three steps to custom menus**:

1. Create `yourapp/menus.py` with MenuItem definitions
2. Import in `yourapp/apps.py` `ready()` method
3. Done! Menu renders automatically

**Key concepts**:

- Import `AppMenu` from `mvp.menus`
- Use `MenuItem` from `flex_menu`
- Singles first, groups after (automatic)
- Icons via django-easy-icons (Bootstrap Icons)
- Active state automatic (no manual management)
