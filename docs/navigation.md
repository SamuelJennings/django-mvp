# Navigation Menu System

Django MVP provides two approaches for building sidebar navigation menus:

1. **[AppMenu (django-flex-menus)](#appmenu-django-flex-menus)** - Define menus in Python with automatic URL resolution
2. **[Cotton Components](#cotton-components)** - Build menus directly in templates with full control

## AppMenu (django-flex-menus)

Use `AppMenu` to define your navigation structure in Python. Django MVP integrates with [django-flex-menus](https://github.com/christianwgd/django-flex-menu) to provide a declarative menu API with automatic URL resolution and hierarchical organization.

### Quick Start

**Step 1:** Create `yourapp/menus.py`:

```python
from mvp.menus import AppMenu, MenuCollapse, MenuGroup
from flex_menu import MenuItem

# Single menu items
MenuItem(
    name="dashboard",
    view_name="app:dashboard",
    extra_context={"label": "Dashboard", "icon": "house"},

)

# Expandable dropdown menu
MenuCollapse(
    name="products",
    extra_context={"label": "Products", "icon": "box-seam"},
    ,
    children=[
        MenuItem(
            name="product_list",
            view_name="app:products",
            extra_context={"label": "All Products", "icon": "list"}
        ),
        MenuItem(
            name="product_add",
            view_name="app:product_add",
            extra_context={"label": "Add Product", "icon": "plus-circle"}
        ),
    ]
)

# Section header with items
MenuGroup(
    name="admin_section",
    extra_context={"label": "ADMINISTRATION"},
    ,
    children=[
        MenuItem(
            name="users",
            view_name="app:users",
            extra_context={"label": "Users", "icon": "person-badge"}
        ),
        MenuItem(
            name="settings",
            view_name="app:settings",
            extra_context={"label": "Settings", "icon": "gear"}
        ),
    ]
)
```

**Step 2:** Import menus in your `AppConfig`:

```python
# yourapp/apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "yourapp"

    def ready(self):
        import yourapp.menus  # noqa: F401
```

**Step 3:** Render in your template:

```django
{% load flex_menu %}

<c-app.sidebar>
    {% render_menu "AppMenu" renderer="adminlte" %}
</c-app.sidebar>
```

### Menu Item Types

#### MenuItem - Single Items

Leaf nodes without children. Render as clickable links.

```python
MenuItem(
    name="dashboard",
    view_name="app:dashboard",
    extra_context={
        "label": "Dashboard",  # Required: Display text
        "icon": "house",       # Optional: Icon name
    },

)
```

**Features:**

- Automatic URL resolution from `view_name`
- Active state detection (highlights current page)
- Icon support via django-easy-icons
- Optional badge display

#### MenuCollapse - Expandable Dropdowns

Parent items that expand/collapse to show children. AdminLTE treeview behavior with chevron icon.

```python
MenuCollapse(
    name="reports",
    extra_context={
        "label": "Reports",
        "icon": "graph-up"
    },
    ,
    children=[
        MenuItem(name="sales", view_name="app:sales",
                 extra_context={"label": "Sales Report"}),
        MenuItem(name="inventory", view_name="app:inventory",
                 extra_context={"label": "Inventory Report"}),
    ]
)
```

**Features:**

- Click to expand/collapse children
- Automatic chevron rotation (> when closed, ∨ when open)
- Remembers expanded state when child is active
- Supports nested dropdowns (unlimited depth)
- Full AdminLTE treeview integration

#### MenuGroup - Section Headers

Non-clickable section headers that group related items. Renders as uppercase header followed by menu items.

```python
MenuGroup(
    name="admin_tools",
    extra_context={"label": "ADMIN TOOLS"},
    ,
    children=[
        MenuItem(name="users", view_name="app:users",
                 extra_context={"label": "Users", "icon": "people"}),
        MenuItem(name="roles", view_name="app:roles",
                 extra_context={"label": "Roles", "icon": "shield"}),
    ]
)
```

**Features:**

- Uppercase styling for visual separation
- Groups logically related menu items
- Can contain MenuCollapse items for nested groups
- Improves menu organization and scannability

### Extra Context Options

The `extra_context` dictionary provides additional rendering options:

```python
MenuItem(
    name="notifications",
    view_name="app:notifications",
    extra_context={
        "label": "Notifications",           # Required
        "icon": "bell",                     # Icon name
        "badge": "5",                       # Badge text/number
        "badge_classes": "text-bg-danger",  # Badge styling
        "classes": "custom-item",           # Additional <li> classes
        "link_classes": "text-danger",      # Additional <a> classes
    },

)
```

**Available Options:**

| Key | Type | Description | Default |
|-----|------|-------------|---------|
| `label` | str | Display text (required) | - |
| `icon` | str | Icon name from django-easy-icons | `"circle"` |
| `badge` | str/int | Badge text/number | None |
| `badge_classes` | str | Badge CSS classes | `"text-bg-secondary"` |
| `classes` | str | Additional `<li>` classes | `""` |
| `link_classes` | str | Additional `<a>` classes | `""` |

### Nested Menus

Create multi-level hierarchies by nesting MenuCollapse items:

```python
MenuCollapse(
    name="catalog",
    extra_context={"label": "Catalog", "icon": "folder"},
    ,
    children=[
        MenuItem(name="products", view_name="app:products",
                 extra_context={"label": "Products"}),
        MenuCollapse(
            name="categories",
            extra_context={"label": "Categories", "icon": "folder-open"},
            children=[
                MenuItem(name="electronics", view_name="app:cat_electronics",
                         extra_context={"label": "Electronics"}),
                MenuItem(name="clothing", view_name="app:cat_clothing",
                         extra_context={"label": "Clothing"}),
            ]
        ),
    ]
)
```

**Best Practices:**

- Limit nesting to 2-3 levels for usability
- Use icons consistently at each level
- Keep labels concise (1-3 words)

### Auto-Sorting

By default, single items appear before groups:

```python
# These will render in order: Dashboard, Profile, Admin Group
MenuCollapse(name="admin", ..., )  # Renders last
MenuItem(name="dashboard", ..., )   # Renders first
MenuItem(name="profile", ..., )     # Renders second
```

**Rendering Order:**

1. All single MenuItem instances (in declaration order)
2. All MenuCollapse/MenuGroup instances (in declaration order)

To control exact order, declare items in desired sequence.

### Active State Detection

Menu items automatically highlight when their URL matches the current page:

```python
MenuItem(
    name="dashboard",
    view_name="app:dashboard",  # If current URL matches, item is active
    extra_context={"label": "Dashboard"},

)
```

**Features:**

- Adds `.active` class to current page link
- Adds `.menu-open` class to parent dropdowns containing active items
- Parent dropdowns auto-expand when child is active
- Works with Django URL namespaces

### Advanced Usage

#### Dynamic Menu Items

Add menu items conditionally based on user permissions:

```python
# In your AppConfig.ready() method
from django.contrib.auth import get_user_model

def ready(self):
    super().ready()
    import yourapp.menus  # Load base menus

    # Add admin-only items dynamically
    from mvp.menus import AppMenu
    from flex_menu import MenuItem

    # This would typically check in a view/context processor
    # Shown here for illustration
    MenuItem(
        name="admin_panel",
        view_name="admin:index",
        extra_context={"label": "Admin Panel", "icon": "shield-lock"},

    )
```

#### URL Parameters

Use direct URLs for items requiring parameters:

```python
MenuItem(
    name="user_profile",
    url="/users/123/profile",  # Direct URL instead of view_name
    extra_context={"label": "My Profile", "icon": "person"},

)
```

#### External Links

Create menu items linking to external resources:

```python
MenuItem(
    name="docs",
    url="https://docs.example.com",
    extra_context={
        "label": "Documentation",
        "icon": "book",
        "link_classes": "external-link",  # Add custom styling
    },

)
```

## Cotton Components

For full template-level control, build menus directly using Cotton components. This approach is ideal when:

- Menu structure is dynamic per-page
- Items require complex conditionals
- You need custom HTML structure
- You're prototyping layouts

See **[Menu Components Reference](components/menu.md)** for complete documentation.

### Basic Example

```django
<c-app.sidebar>
    <c-app.sidebar.menu>
        <c-app.sidebar.menu-item label="Dashboard" href="/" icon="house" />
        <c-app.sidebar.menu-item label="Profile" href="/profile" icon="person" />

        <c-app.sidebar.menu-collapse label="Settings" icon="gear">
            <c-app.sidebar.menu-item label="Account" href="/settings/account" />
            <c-app.sidebar.menu-item label="Privacy" href="/settings/privacy" />
        </c-app.sidebar.menu-collapse>

        <c-app.sidebar.menu-group label="REPORTS">
            <c-app.sidebar.menu-item label="Sales" href="/reports/sales" icon="graph-up" />
            <c-app.sidebar.menu-item label="Inventory" href="/reports/inventory" icon="boxes" />
        </c-app.sidebar.menu-group>
    </c-app.sidebar.menu>
</c-app.sidebar>
```

### When to Use Each Approach

| Feature | AppMenu | Cotton Components |
|---------|---------|-------------------|
| **Centralized menu definition** | ✅ Yes | ❌ No |
| **Automatic URL resolution** | ✅ Yes | ❌ Manual |
| **Active state detection** | ✅ Automatic | ⚠️ Manual |
| **Reusable across pages** | ✅ Yes | ❌ Template-specific |
| **Dynamic per-page menus** | ⚠️ Complex | ✅ Easy |
| **Custom HTML structure** | ❌ No | ✅ Yes |
| **Learning curve** | ⏱️ Moderate | ⏱️ Low |
| **Best for** | Production apps | Prototypes, custom layouts |

**Recommendation:** Use **AppMenu** for production applications with consistent navigation. Use **Cotton Components** for page-specific menus, prototypes, or when you need full control over HTML output.

## See Also

- **[Menu Components Reference](components/menu.md)** - Complete Cotton component API
- **[App Component](components/app.md)** - App wrapper and sidebar configuration
- **[django-flex-menus Documentation](https://github.com/christianwgd/django-flex-menu)** - Underlying menu library
