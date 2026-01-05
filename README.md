# Django MVP

**AdminLTE 4 for Django** - A modern, responsive admin dashboard template system built with Django Cotton, providing AdminLTE 4 layouts and components for building production-ready data-centric applications.

**Note:** This project is currently in active development. Version 1.0 will introduce AdminLTE 4 integration with breaking changes from previous versions.

## Overview

Django MVP brings the powerful [AdminLTE 4](https://github.com/colorlibhq/AdminLTE) admin dashboard template to Django as a collection of reusable [django-cotton](https://github.com/wrabit/django-cotton) components. It provides:

- **AdminLTE 4 Layout System** - Full implementation of AdminLTE's grid-based layout structure
- **Configuration-Driven Design** - Control layout and appearance via Django settings
- **Cotton Component Library** - AdminLTE-specific components (cards, boxes, widgets, etc.)
- **Bootstrap 5 Foundation** - Built on Bootstrap 5 with [django-cotton-bs5](https://github.com/SamuelJennings/django-cotton-bs5) for base components
- **Production-Ready** - Designed for data-centric applications, admin interfaces, and dashboards

### What's Included

Django MVP provides **AdminLTE-specific components only**. Standard Bootstrap 5 components (buttons, modals, forms, etc.) are provided by the separate `django-cotton-bs5` package. This includes:

- **AdminLTE Layouts** - App wrapper, sidebar, header, main content area, footer
- **AdminLTE Widgets** - Info boxes, small boxes, cards, direct chat
- **AdminLTE Components** - Specialized components unique to AdminLTE
- **View Mixins** - Python helpers for common patterns (search, ordering, pagination)
- **Menu Integration** - Renderers for [django-flex-menus](https://github.com/SamuelJennings/django-flex-menus)

## Architecture

Django MVP mirrors AdminLTE 4's grid-based layout structure:

```
.app-wrapper (grid container)
├── .app-sidebar (navigation)
├── .app-header (top navbar)
├── .app-main (content area)
│   ├── .app-content-header (page header/breadcrumbs)
│   └── .app-content (main content)
└── .app-footer (optional footer)
```

All layout behavior is controlled via the `MVP` configuration object in Django settings, requiring minimal template customization.

## Installation

```bash
pip install django-mvp
```

Add required apps to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_cotton",      # Cotton template components
    "cotton_bs5",         # Bootstrap 5 components
    "easy_icons",         # Icon system
    "flex_menu",          # Optional: menu system
    "mvp",                # Django MVP
    ...
]
```

### Add Context Processor

Add the MVP context processor to make configuration available in all templates:

```python
TEMPLATES = [
    {
        ...
        "OPTIONS": {
            "context_processors": [
                ...
                "mvp.context_processors.mvp_config",
            ],
        },
    },
]
```

### Configure Icons

Django MVP uses Bootstrap Icons via `django-easy-icons`:

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
            "search": "bi bi-search",
            "filter": "bi bi-funnel",
            "person": "bi bi-person",
            "calendar": "bi bi-calendar3",
            "settings": "bi bi-gear",
            "theme_light": "bi bi-sun",
            "theme_dark": "bi bi-moon",
            "github": "bi bi-github",
        },
    },
}
```

## Configuration

Django MVP uses a centralized `MVP` configuration dictionary in Django settings to control all layout behavior, branding, and navigation.

### The MVP Configuration Object

Add this to your `settings.py`:

```python
MVP = {
    # Site branding
    "brand": {
        "text": "My Application",
        "logo": "img/logo.png",  # Optional logo image
    },

    # AdminLTE layout options
    "layout": {
        "fixed_sidebar": True,     # Fixed sidebar position
        "sidebar_expand": "lg",    # When sidebar expands: 'sm', 'md', 'lg', 'xl', 'xxl'
        "body_class": "layout-fixed sidebar-expand-lg",  # Additional body classes
    },

    # Sidebar configuration
    "sidebar": {
        "visible": True,
        "width": "280px",  # Optional custom width
    },

    # Footer configuration
    "footer": {
        "visible": True,
        "text": "© 2026 My Application",
    },

    # Action buttons/links in navbar
    "actions": [
        {
            "icon": "github",
            "text": "View on GitHub",
            "href": "https://github.com/user/repo",
            "target": "_blank",
        },
    ],
}
```

### Configuration Flow

The MVP configuration is made available in all templates via the `mvp_config` context processor:

```html
<!-- Access in templates as {{ mvp }} -->
{{ mvp.brand.text }}
{{ mvp.layout.body_class }}
```

### Template Hierarchy

Django MVP follows a simple template hierarchy:

1. **`base.html`** - Foundation HTML structure with AdminLTE CSS/JS
2. **`mvp/base.html`** - AdminLTE app-wrapper layout structure
3. **Your templates** - Extend `mvp/base.html` and override blocks

Example page template:

```html
{% extends "mvp/base.html" %}

{% block content %}
  <div class="container-fluid">
    <h1>Your Page Content</h1>
  </div>
{% endblock %}
```

### Customizing Layouts

Create a custom base layout in your project to override blocks:

```html
{# templates/layouts/base.html in your project #}
{% extends "mvp/mvp/base.html" %}

{% block extra_css %}
  <link rel="stylesheet" href="{% static 'css/custom.css' %}">
{% endblock %}
```

## Quick Start

### Basic Page Template

```html
{% extends "mvp/base.html" %}

{% block content %}
  <div class="app-content">
    <div class="container-fluid">
      <h1>Welcome to My Application</h1>
      <p>Your content here...</p>
    </div>
  </div>
{% endblock %}
```

### With Page Header and Breadcrumbs

```html
{% extends "mvp/base.html" %}

{% block page_header %}
  <div class="app-content-header">
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-6">
          <h3 class="mb-0">Dashboard</h3>
        </div>
        <div class="col-sm-6">
          <ol class="breadcrumb float-sm-end">
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item active">Dashboard</li>
          </ol>
        </div>
      </div>
    </div>
  </div>
{% endblock %}

{% block content %}
  <div class="app-content">
    <div class="container-fluid">
      <!-- Your dashboard content -->
    </div>
  </div>
{% endblock %}
```

## AdminLTE Components

Django MVP provides Cotton components for AdminLTE-specific widgets. Standard Bootstrap components (cards, buttons, modals, etc.) should use `django-cotton-bs5`.

### Info Boxes

```html
<c-adminlte.info-box
  icon="shopping-cart"
  bg_class="text-bg-primary"
  number="150"
  text="New Orders" />
```

### Small Boxes

```html
<c-adminlte.small-box
  bg_class="text-bg-success"
  number="53%"
  text="Bounce Rate"
  icon="chart-area"
  href="/stats/" />
```

### Cards with Tools

```html
<c-adminlte.card>
  <c-slot name="header">
    <h3 class="card-title">Monthly Report</h3>
    <div class="card-tools">
      <button type="button" class="btn btn-tool" data-lte-toggle="card-collapse">
        <i class="bi bi-dash"></i>
      </button>
    </div>
  </c-slot>

  <c-slot name="body">
    Card content here
  </c-slot>
</c-adminlte.card>
```

## View Mixins

Python mixins for common patterns:

### SearchMixin

Django admin-style multi-field search:

```python
from mvp.views import SearchMixin
from django.views.generic import ListView

class ProjectListView(SearchMixin, ListView):
    model = Project
    search_fields = ["title", "description", "owner__username"]
```

### OrderMixin

Dropdown-based result ordering:

```python
from mvp.views import OrderMixin
from django.views.generic import ListView

class ProjectListView(OrderMixin, ListView):
    model = Project
    order_fields = {
        "title": "Title A-Z",
        "-title": "Title Z-A",
        "-created": "Newest First",
        "created": "Oldest First",
    }
```

## Requirements

- Python 3.10+
- Django 4.2+
- django-cotton 2.3.1+
- django-cotton-bs5 0.5.0+
- django-easy-icons 0.3.0+
- AdminLTE 4.x (CSS/JS included)

## Design Philosophy

Django MVP provides:

1. **AdminLTE Layout System** - Grid-based app-wrapper structure
2. **Configuration-Driven** - Control via Django settings, not templates
3. **AdminLTE Components Only** - Standard BS5 components in django-cotton-bs5
4. **Production-Ready** - Built for data-centric dashboards and admin interfaces

## Use Cases

Ideal for:

- **Admin dashboards** with metrics and data visualization
- **Data management applications** requiring sophisticated layouts
- **Internal tools** with complex navigation structures
- **Research portals** managing datasets and projects
- **SaaS admin interfaces** with multi-tenant support

## Contributing

Contributions welcome! When adding components:

1. Focus on AdminLTE-specific components only
2. Use `<c-vars />` for default values
3. Include proper ARIA attributes
4. Support AdminLTE's data attributes and JS interactions
5. Add tests for new components

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:

- [AdminLTE](https://github.com/colorlibhq/AdminLTE) - The admin dashboard template
- [django-cotton](https://github.com/wrabit/django-cotton) - Component system by @wrabit
- [django-cotton-bs5](https://github.com/SamuelJennings/django-cotton-bs5) - Bootstrap 5 components
- [Bootstrap 5](https://getbootstrap.com/) - CSS framework
