# Django Cotton Layouts

Application layouts and UI patterns for Django Cotton - designed for research portals, data-centric applications, and admin-heavy Django projects.

**Note:** This project is currently in alpha development. The API may change as we refine the layout patterns and components.

## Overview

Django Cotton Layouts provides sophisticated, production-ready layout patterns built on top of [django-cotton](https://github.com/wrabit/django-cotton) and [django-cotton-bs5](https://github.com/SamuelJennings/django-cotton-bs5). It's designed for applications that need:

- **Collapsible sidebar navigation** with responsive mobile transforms
- **List/detail view patterns** with integrated filtering, search, and pagination
- **Plugin-based detail views** with categorized sidebar menus
- **Responsive navbar** with desktop and mobile variants
- **Data-centric UI patterns** optimized for research portals and institutional data repositories

## Features

### Layout Components

- **Sidebar Layouts** - Collapsible sidebar with menu sections, mobile-responsive
- **Detail Views** - Complex detail view layouts with plugin support
- **List Views** - Filterable, searchable, paginated list views
- **Navbar System** - Desktop/mobile responsive navigation with dropdown support
- **Page Headers** - Responsive page headers with actions and breadcrumbs
- **Dashboard Layouts** - 2-column responsive dashboard patterns

### View Mixins

Python mixins for common patterns:
- `SearchMixin` - Django admin-style multi-field search
- `OrderMixin` - Dropdown-based result ordering
- `SearchOrderMixin` - Combined search and ordering

### Menu Integration

Custom renderers for [django-flex-menus](https://github.com/SamuelJennings/django-flex-menus):
- `SidebarRenderer` - Sidebar menu rendering
- `NavbarRenderer` - Desktop navbar rendering
- `MobileNavbarRenderer` - Mobile offcanvas navbar
- `DropdownRenderer` - Dropdown menu rendering

## Installation

```bash
pip install django-cotton-layouts
```

Add `cotton_layouts` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_cotton",
    "cotton_bs5",
    "flex_menu",
    "easy_icons",
    "cotton_layouts",
    ...
]
```

### Add Context Processor

Add the `page_config` context processor to make configuration available in all templates:

```python
TEMPLATES = [
    {
        ...
        "OPTIONS": {
            "context_processors": [
                ...
                "cotton_layouts.context_processors.page_config",
            ],
        },
    },
]
```

### Configure Easy Icons

The layouts use Bootstrap Icons via `django-easy-icons`. Add this to your `settings.py`:

```python
EASY_ICONS = {
    "default": {
        "renderer": "easy_icons.renderers.ProviderRenderer",
        "config": {"tag": "i"},
        "icons": {
            # Core Actions
            "add": "bi bi-plus-circle",
            "create": "bi bi-plus-circle",
            "edit": "bi bi-pencil",
            "delete": "bi bi-trash",
            "save": "bi bi-floppy",
            "cancel": "bi bi-x-circle",
            "view": "bi bi-eye",
            # Navigation
            "arrow_right": "bi bi-arrow-right",
            "chevron_down": "bi bi-chevron-down",
            "chevron_up": "bi bi-chevron-up",
            # Search & Filter
            "search": "bi bi-search",
            "filter": "bi bi-funnel",
            # People & Organizations
            "person": "bi bi-person",
            # Metadata
            "calendar": "bi bi-calendar3",
            "documentation": "bi bi-book",
            # Settings
            "settings": "bi bi-gear",
            # Theme
            "theme_light": "bi bi-sun",
            "theme_dark": "bi bi-moon",
            # Social & External
            "github": "bi bi-github",
            # Auth
            "logout": "bi bi-box-arrow-right",
        },
    },
}
```

These are the core icons used by the layouts. You can add more icons as needed for your application.

### Configure Flex Menus

Add custom renderers for `django-flex-menus`:

```python
FLEX_MENUS = {
    "renderers": {
        "sidebar": "cotton_layouts.renderers.SidebarRenderer",
        "navbar": "cotton_layouts.renderers.NavbarRenderer",
        "mobile_navbar": "cotton_layouts.renderers.MobileNavbarRenderer",
        "dropdown": "cotton_layouts.renderers.DropdownRenderer",
    },
}
```

## Configuration System

Django Cotton Layouts uses a **centralized configuration approach** via the `PAGE_CONFIG` dictionary in your Django settings. This configuration is injected into all templates through a context processor, allowing you to control layout behavior, branding, navigation, and UI components from a single location.

### The PAGE_CONFIG Dictionary

Add this to your `settings.py`:

```python
PAGE_CONFIG = {
    # Layout type: 'sidebar' or 'navbar' (default: 'navbar')
    "layout": "sidebar",
    
    # Site branding configuration
    "brand": {
        "text": "My Application",
        "image_light": "img/logo-light.svg",  # Logo for light theme
        "image_dark": "img/logo-dark.svg",    # Logo for dark theme
        "icon_light": "img/icon-light.svg",   # Favicon for light theme
        "icon_dark": "img/icon-dark.svg",     # Favicon for dark theme
    },
    
    # Navigation configuration
    "navigation": {
        "sidebar": {
            "collapsible": True,  # Allow sidebar to collapse to icon-only mode
            "show_at": "lg",      # Bootstrap breakpoint (sm, md, lg, xl, xxl)
            "width": "280px",     # Custom sidebar width (optional)
        },
    },
    
    # Action widgets (e.g., theme toggle, external links)
    "actions": [
        {
            "icon": "github",
            "text": "View on GitHub",
            "href": "https://github.com/user/repo",
            "target": "_blank",
        },
        {
            "icon": "question-circle",
            "text": "Support",
            "href": "/support/",
        },
    ],
}
```

### How Configuration Flows Through Templates

The configuration system follows a hierarchical template structure:

1. **`base.html`** - The foundation template that sets up HTML structure, loads static assets, and configures favicons using `page_config.brand.icon_light/dark`.

2. **`layouts/base.html`** - Minimal base layout that typically just extends `base.html`. Not commonly modified by end users.

3. **`layouts/standard.html`** - The **primary layout template** that:
   - Extends `layouts/base.html`
   - Configures the sidebar layout using `page_config.navigation.sidebar`
   - Passes configuration to navigation components using `:attrs="page_config.navigation.sidebar"`
   - Provides a `content` block for page-specific content

4. **Your templates** - Extend `layouts/standard.html` and override the `content` block:

```html
{% extends "layouts/standard.html" %}

{% block content %}
  <div class="container py-4">
    <h1>Your Page Content</h1>
  </div>
{% endblock %}
```

### Configuration via :attrs

Components receive configuration using Cotton's `:attrs` syntax, which expands dictionaries into component attributes:

```html
<!-- In layouts/standard.html -->
<c-page.navigation.sidebar :attrs="page_config.navigation.sidebar" 
                           :brand="page_config.brand" />
```

If `page_config.navigation.sidebar = {"collapsible": True, "show_at": "lg"}`, this expands to:

```html
<c-page.navigation.sidebar collapsible="True" 
                           show_at="lg" 
                           :brand="page_config.brand" />
```

### Customizing Layouts

Instead of modifying `base.html`, customize layouts by **extending blocks** in `layouts/base.html` or creating a custom base template in your project:

```html
{# templates/layouts/base.html in your project #}
{% extends "cotton_layouts/layouts/base.html" %}

{% block extra_css %}
  <link rel="stylesheet" href="{% static 'css/custom.css' %}">
{% endblock %}
```

### Pre-built Layout Templates

Use these ready-made templates by extending them:

- **`layouts/standard.html`** - Basic sidebar/navbar layout (most common)
- **`layouts/list_view.html`** - List views with search, filters, and pagination
- **`layouts/detail_view.html`** - Detail views with sidebar navigation
- **`layouts/form_view.html`** - Form-based views (coming soon)

Example extending list view:

```html
{% extends "layouts/list_view.html" %}

{% block list_content %}
  {% for item in object_list %}
    <c-card>
      <h3>{{ item.title }}</h3>
    </c-card>
  {% endfor %}
{% endblock %}
```

## Sidebar Layouts

The sidebar layout system provides flexible width control through CSS variables, Bootstrap column classes, or both. Sidebars can be configured globally via `PAGE_CONFIG` or individually at the component level.

### Sidebar Width Configuration

The `c-layouts.sidebar` and `c-sidebar` components support multiple width control methods:

#### Width Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `width` | string | Sets the sidebar width (e.g., `"280px"`, `"20rem"`, `"15%"`) |
| `max_width` | string | Sets maximum width constraint (e.g., `"350px"`) |
| `min_width` | string | Sets minimum width constraint (e.g., `"200px"`) |
| `col_class` | string | Bootstrap column classes for responsive width (e.g., `"col-3 col-lg-2"`) |

#### Other Sidebar Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `reverse` | boolean | `False` | Places sidebar on right side instead of left |
| `border` | boolean | `False` | Adds border to sidebar (border-start or border-end) |
| `collapsible` | boolean | `False` | Enables icon-only collapsed mode with toggle button |
| `sidebar_id` | string | - | Custom ID for the sidebar element |
| `sidebar_class` | string | - | Additional CSS classes for the sidebar |
| `class` | string | - | Additional CSS classes for the layout container |

### Usage Examples

#### Fixed Width Sidebar

```html
<c-layouts.sidebar width="280px">
  <c-slot name="sidebar">
    <nav>Sidebar content</nav>
  </c-slot>
  <div>Main content</div>
</c-layouts.sidebar>
```

#### Width with Constraints

Prevent the sidebar from becoming too wide or too narrow:

```html
<c-layouts.sidebar width="280px" max_width="350px" min_width="200px">
  <c-slot name="sidebar">
    <nav>Sidebar content</nav>
  </c-slot>
  <div>Main content</div>
</c-layouts.sidebar>
```

#### Responsive Width with Bootstrap Columns

Use Bootstrap's responsive column classes for breakpoint-based sizing:

```html
<c-layouts.sidebar col_class="col-12 col-md-4 col-lg-3 col-xl-2">
  <c-slot name="sidebar">
    <nav>Sidebar content</nav>
  </c-slot>
  <div>Main content</div>
</c-layouts.sidebar>
```

This creates a sidebar that:
- Takes full width on mobile (`col-12`)
- 4 columns on medium screens (`col-md-4`)
- 3 columns on large screens (`col-lg-3`)
- 2 columns on extra-large screens (`col-xl-2`)

#### Mixed Approach

Combine fixed width with max-width and responsive classes:

```html
<c-layouts.sidebar width="280px" 
                   max_width="350px" 
                   col_class="col-lg-3">
  <c-slot name="sidebar">
    <nav>Sidebar content</nav>
  </c-slot>
  <div>Main content</div>
</c-layouts.sidebar>
```

#### Reversed Sidebar (Right Side)

```html
<c-layouts.sidebar reverse width="250px">
  <c-slot name="sidebar">
    <aside>Metadata sidebar</aside>
  </c-slot>
  <article>Article content</article>
</c-layouts.sidebar>
```

#### Collapsible Sidebar

```html
<c-layouts.sidebar collapsible width="280px">
  <c-slot name="sidebar">
    <nav>
      <c-sidebar.menu-item icon="home" text="Home" href="/" />
      <c-sidebar.menu-item icon="settings" text="Settings" href="/settings/" />
    </nav>
  </c-slot>
  <div>Main content</div>
</c-layouts.sidebar>
```

When collapsed, the sidebar shrinks to icon-only mode (60px wide).

#### Nested Sidebars (Dual Sidebar Layout)

Create complex layouts with sidebars on both sides:

```html
{# Left sidebar: Navigation #}
<c-layouts.sidebar width="200px" max_width="250px">
  <c-slot name="sidebar">
    <nav>Navigation links</nav>
  </c-slot>
  
  {# Right sidebar: Metadata #}
  <c-layouts.sidebar reverse col_class="col-12 col-lg-3 col-xl-2">
    <c-slot name="sidebar">
      <aside>Article metadata</aside>
    </c-slot>
    
    {# Main content in the center #}
    <article>
      <h1>Article Title</h1>
      <p>Content here...</p>
    </article>
  </c-layouts.sidebar>
</c-layouts.sidebar>
```

### Global Sidebar Configuration

Configure sidebar width globally via `PAGE_CONFIG`:

```python
PAGE_CONFIG = {
    "layout": "sidebar",
    "sidebar": {
        "collapsible": True,
        "show_at": "lg",      # Bootstrap breakpoint for mobile transform
        "width": "280px",     # Sidebar width
        "max_width": "320px", # Maximum width
        "min_width": "200px", # Minimum width
    },
}
```

These settings are passed to the `c-structure.sidebar` component in `layouts/standard.html` via `:attrs="page_config.sidebar"`.

### How Width Control Works

Width control uses CSS custom properties (CSS variables) set inline on the sidebar element:

```html
<aside class="sidebar" style="--sidebar-width: 280px; --sidebar-max-width: 350px;">
  <!-- Sidebar content -->
</aside>
```

The SCSS applies these variables:

```scss
.sidebar {
  width: var(--sidebar-width, auto);
  max-width: var(--sidebar-max-width, var(--sidebar-width, 300px));
  min-width: var(--sidebar-min-width, auto);
}
```

When Bootstrap column classes are used (via `col_class`), the sidebar respects flex-basis sizing while still applying max/min constraints if specified.

### Best Practices

1. **Use fixed widths for desktop navigation sidebars** - Provides consistent layout: `width="280px"`
2. **Add max-width constraints** - Prevents sidebars from becoming too wide on large screens: `max_width="350px"`
3. **Use Bootstrap columns for content sidebars** - Better responsive behavior: `col_class="col-lg-3"`
4. **Combine approaches for complex layouts** - Mix fixed and responsive as needed
5. **Test collapsed state** - If using `collapsible`, ensure icons are visible when collapsed


## Quick Start

### Basic Sidebar Layout

```html
<c-sidebar.layout>
  <c-slot name="sidebar">
    <c-sidebar.index>
      <c-sidebar.menu-section title="Navigation">
        <c-sidebar.menu-item href="/" label="Home" active />
        <c-sidebar.menu-item href="/about" label="About" />
      </c-sidebar.menu-section>
    </c-sidebar.index>
  </c-slot>

  <c-slot name="main">
    <h1>Main Content</h1>
    <p>Your page content here...</p>
  </c-slot>
</c-sidebar.layout>
```

### List View with Filtering

```html
<c-list.index>
  <c-slot name="header">
    <c-list.header title="Projects" />
  </c-slot>

  <c-slot name="search">
    <c-list.search-widget />
  </c-slot>

  <c-slot name="filters">
    <!-- Your filter form here -->
  </c-slot>

  <c-slot name="results">
    <!-- Your results here -->
  </c-slot>

  <c-slot name="pagination">
    <c-list.pagination />
  </c-slot>
</c-list.index>
```

### Detail View with Sidebar

```html
<c-detail.layout>
  <c-slot name="header">
    <c-detail.header 
      title="{{ object.title }}"
      subtitle="{{ object.description }}" />
  </c-slot>

  <c-slot name="sidebar">
    <c-sidebar.index>
      <!-- Sidebar menu items -->
    </c-sidebar.index>
  </c-slot>

  <c-slot name="content">
    <!-- Main detail content -->
  </c-slot>
</c-detail.layout>
```

## Documentation

Full documentation coming soon. For now, see the [example app](./example) for usage patterns.

## Requirements

- Python 3.10+
- Django 4.2+
- django-cotton 2.3.1+
- django-cotton-bs5 0.5.0+
- django-flex-menus 0.3.0+
- django-easy-icons 0.3.0+

## Design Philosophy

Django Cotton Layouts is built around these principles:

1. **Component-based** - Reusable, composable Cotton components
2. **Slot-driven** - Flexible content areas using Cotton's slot system
3. **Responsive-first** - Mobile-friendly layouts that adapt to screen size
4. **Accessible** - ARIA-compliant and keyboard-navigable
5. **Integration-ready** - Works with flex-menus, easy-icons, and Bootstrap 5

## Use Cases

This package is ideal for:

- **Research data portals** managing projects, datasets, and samples
- **Institutional repositories** with hierarchical data structures
- **Admin-heavy applications** requiring sophisticated navigation
- **Data-centric portals** with list/detail/filter patterns
- **Community platforms** with member profiles and content management

## Contributing

Contributions are welcome! This library follows django-cotton conventions and Bootstrap 5 standards. When adding new components:

1. Use `<c-vars />` for default values
2. Include proper accessibility attributes
3. Support responsive behavior
4. Maintain consistent naming conventions
5. Add tests for new components

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built on top of:
- [django-cotton](https://github.com/wrabit/django-cotton) by @wrabit
- [django-cotton-bs5](https://github.com/SamuelJennings/django-cotton-bs5)
- [django-flex-menus](https://github.com/SamuelJennings/django-flex-menus)
- [Bootstrap 5](https://getbootstrap.com/)
