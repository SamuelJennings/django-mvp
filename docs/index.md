# Django MVP Documentation

**AdminLTE 4 for Django** - Modern, responsive admin dashboard components built with Django Cotton.

## Component Library

Django MVP provides AdminLTE 4-specific components as reusable Cotton templates. For standard Bootstrap 5 components (buttons, modals, forms, etc.), use the separate [django-cotton-bs5](https://github.com/SamuelJennings/django-cotton-bs5) package.

### Navigation Components

Build sophisticated sidebar navigation menus with AdminLTE 4 styling:

- **[Navigation Menu System](navigation.md)** - Complete navigation solution
  - **AppMenu**: Centralized Python-based menu definition with django-flex-menus
  - **Cotton Components**: Template-level menu building with full control
  - Automatic URL resolution and active state detection
  - Expandable dropdowns with AdminLTE treeview behavior
  - Section headers for grouping related items
  - Multi-level nesting support

- **[Menu Components Reference](components/menu.md)** - Cotton component API
  - `<c-app.sidebar.menu>` - Menu container
  - `<c-app.sidebar.menu-item>` - Single items and parent items
  - `<c-app.sidebar.menu-collapse>` - Expandable dropdowns
  - `<c-app.sidebar.menu-group>` - Section headers

### Widget Components

Dashboard widgets for displaying metrics, statistics, and key performance indicators:

- **[Info Box](components/info-box.md)** - Display metrics with icons and optional progress bars
  - Compact metric display with icon
  - Two fill modes: icon-only or full-box coloring
  - Optional progress indicators
  - ARIA-compliant and accessible

- **[Small Box](components/small-box.md)** - Prominent dashboard summary widgets
  - Large metric display with background color
  - Decorative background icons
  - Optional action links in footer
  - Perfect for dashboard KPIs

- **[Card](components/card.md)** - Flexible content containers
  - Header with optional icon and tools
  - Collapsible/expandable sections
  - Three fill modes: outline, header, card
  - Footer support with named slots
  - AdminLTE card tools integration

## Getting Started

### Installation

```bash
pip install django-mvp
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "django_cotton",      # Cotton template components
    "cotton_bs5",         # Bootstrap 5 components
    "easy_icons",         # Icon system
    "mvp",                # Django MVP
    ...
]
```

### Basic Usage

All components are available as Cotton components with the `<c-{name}>` syntax:

```html
{% extends "mvp/base.html" %}

{% block content %}
  <div class="row">
    <div class="col-md-3">
      <c-info-box
        icon="box-seam"
        text="New Orders"
        number="150"
        variant="primary" />
    </div>

    <div class="col-md-3">
      <c-small-box
        heading="53%"
        text="Bounce Rate"
        icon="chart"
        variant="warning"
        link="/stats/" />
    </div>

    <div class="col-md-6">
      <c-card title="Revenue" variant="success" fill="header">
        Revenue chart and details...
      </c-card>
    </div>
  </div>
{% endblock %}
```

## Component Naming Convention

**Important:** Cotton components use **snake_case (kebab-case)** naming, never camelCase:

- ✅ Correct: `<c-info-box />`, `<c-small-box />`
- ❌ Wrong: `<c-infoBox />`, `<c-smallBox />`

## Architecture

### Template Hierarchy

1. **`base.html`** - Foundation HTML with AdminLTE CSS/JS
2. **`mvp/base.html`** - AdminLTE app-wrapper layout
3. **Your templates** - Extend and customize

### Configuration-Driven Design

All layout behavior is controlled via the `MVP` configuration in Django settings:

```python
MVP = {
    "brand": {
        "text": "My Application",
        "logo": "img/logo.png",
    },
    "layout": {
        "fixed_sidebar": True,
        "sidebar_expand": "lg",
    },
    "sidebar": {
        "visible": True,
    },
    "footer": {
        "visible": True,
        "text": "© 2026 My Application",
    },
}
```

## Component Guidelines

### Color Variants

All components support Bootstrap 5 color variants:

- `primary` - Primary brand color
- `success` - Success/positive (green)
- `warning` - Warning (yellow/orange)
- `danger` - Error/danger (red)
- `info` - Informational (blue)
- `secondary` - Secondary/muted (gray)
- `default` - No color applied

### Icons

Components use `django-easy-icons` for icon rendering. Configure icon mappings in settings:

```python
EASY_ICONS = {
    "default": {
        "icons": {
            "box-seam": "bi bi-box-seam",
            "cart": "bi bi-cart",
            "chart": "bi bi-bar-chart",
            # ... more icons
        }
    }
}
```

### Accessibility

All components follow WCAG 2.1 AA guidelines:

- Proper ARIA attributes
- Keyboard navigation support
- Screen reader compatibility
- Semantic HTML structure

## View Mixins

Python helpers for common patterns:

- `SearchMixin` - Django admin-style multi-field search
- `OrderMixin` - Dropdown-based result ordering
- See main [README.md](../README.md) for detailed examples

## Resources

- [Main README](../README.md) - Installation and configuration
- [CHANGELOG](../CHANGELOG.md) - Version history and updates
- [AdminLTE 4 Documentation](https://adminlte.io/) - Upstream reference
- [django-cotton](https://django-cotton.com/) - Component system docs
- [Bootstrap 5.3](https://getbootstrap.com/docs/5.3/) - CSS framework

## Contributing

When adding new components:

1. Focus on AdminLTE-specific components only
2. Use `<c-vars />` for default values
3. Include proper ARIA attributes
4. Support AdminLTE data attributes and JS interactions
5. Add comprehensive tests
6. Document with examples and accessibility guidelines

## License

MIT License - See [LICENSE](../LICENSE) for details.
