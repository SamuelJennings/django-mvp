# Data Model: AdminLTE Layout Configuration System

**Feature**: 003-adminlte-layout-config
**Date**: January 5, 2026

## Overview

This feature does not involve persistent data storage. This document describes the conceptual entities that represent layout configuration at template render time.

## Conceptual Entities

### Layout Configuration

**Description**: Represents the set of boolean flags that control fixed vs scrolling behavior for major layout sections.

**Attributes**:

- `fixed_sidebar` (boolean, optional, default=false) - When true, sidebar remains fixed during scroll
- `fixed_header` (boolean, optional, default=false) - When true, header remains fixed at top
- `fixed_footer` (boolean, optional, default=false) - When true, footer remains fixed at bottom
- `sidebar_expand` (string, optional, default="lg") - Bootstrap breakpoint for sidebar visibility

**Relationships**: None (flat structure)

**Validation Rules**:

- All boolean attributes accept truthy/falsy values
- `sidebar_expand` must be one of: `sm`, `md`, `lg`, `xl`, `xxl`
- No conflicts possible - all combinations are valid

**State Transitions**: None (stateless, evaluated at render time only)

**Examples**:

```python
# Fixed sidebar only
{"fixed_sidebar": True}

# Fixed complete (all elements fixed)
{"fixed_sidebar": True, "fixed_header": True, "fixed_footer": True}

# Fixed header with medium breakpoint
{"fixed_header": True, "sidebar_expand": "md"}

# Default (no fixed elements)
{}
```

### Layout Section

**Description**: Represents major areas of the AdminLTE layout structure that can have fixed positioning.

**Sections**:

- `sidebar` - Left navigation panel (`.app-sidebar`)
- `header` - Top navigation bar (`.app-header`)
- `footer` - Bottom information bar (`.app-footer`)
- `wrapper` - Container for entire app (`.app-wrapper`)

**Attributes** (per section):

- `name` (string) - Section identifier
- `css_class` (string) - AdminLTE CSS class for the section
- `is_fixed` (boolean, computed) - Whether section has fixed positioning enabled
- `body_class` (string, computed) - CSS class added to body element when fixed

**Relationships**:

- Each Layout Section is controlled by one Layout Configuration attribute
- Multiple Layout Sections can be fixed simultaneously

**CSS Class Mapping**:

| Section | Attribute | Body Class When Fixed |
|---------|-----------|----------------------|
| sidebar | `fixed_sidebar` | `.layout-fixed` |
| header | `fixed_header` | `.fixed-header` |
| footer | `fixed_footer` | `.fixed-footer` |

## Template Context Structure

Layout configuration is passed to `<c-app>` component via Cotton attributes:

```django-html
<c-app fixed_sidebar fixed_header sidebar_expand="lg">
  <c-app.header />
  <c-app.sidebar />
  <c-app.main>
    {% block content %}{% endblock %}
  </c-app.main>
  <c-app.footer />
</c-app>
```

**Context Variables** (inside `<c-app>` component):

```django
{
    "fixed_sidebar": True,      # Boolean from component attribute
    "fixed_header": True,       # Boolean from component attribute
    "fixed_footer": False,      # Default when not specified
    "sidebar_expand": "lg",     # String from component attribute
    "class": "",                # Additional CSS classes
}
```

## Rendering Logic

**Body Class Generation**:

```django-html
<body class="bg-body-tertiary
    {%- if fixed_sidebar %} layout-fixed{% endif %}
    {%- if fixed_header %} fixed-header{% endif %}
    {%- if fixed_footer %} fixed-footer{% endif %}
    sidebar-expand-{{ sidebar_expand }}
    {{ class }}">
  <div class="app-wrapper">{{ slot }}</div>
</body>
```

**Example Outputs**:

```html
<!-- No fixed elements -->
<body class="bg-body-tertiary sidebar-expand-lg">

<!-- Fixed sidebar only -->
<body class="bg-body-tertiary layout-fixed sidebar-expand-lg">

<!-- Fixed complete -->
<body class="bg-body-tertiary layout-fixed fixed-header fixed-footer sidebar-expand-lg">
```

## No Database Schema

This feature requires no database tables, migrations, or persistent storage. All layout configuration is ephemeral and exists only during template rendering.

## Demo View State (Added 2026-01-06)

**Description**: Query parameter-based state for interactive demo views in `example/` app.

### Fixed Properties Demo State

**URL Pattern**: `/example/layout-fixed/?fixed_sidebar=on&fixed_header=on`

**Query Parameters**:

- `fixed_sidebar` (string, optional) - Checkbox state ("on" if checked, absent if unchecked)
- `fixed_header` (string, optional) - Checkbox state ("on" if checked, absent if unchecked)
- `fixed_footer` (string, optional) - Checkbox state ("on" if checked, absent if unchecked)

**Processing Logic**:

```python
def layout_fixed_demo(request):
    fixed_sidebar = request.GET.get('fixed_sidebar') == 'on'
    fixed_header = request.GET.get('fixed_header') == 'on'
    fixed_footer = request.GET.get('fixed_footer') == 'on'
    return render(request, 'example/layout_fixed.html', {
        'fixed_sidebar': fixed_sidebar,
        'fixed_header': fixed_header,
        'fixed_footer': fixed_footer,
    })
```

### Responsive Breakpoint Demo State

**URL Pattern**: `/example/layout-responsive/?breakpoint=md`

**Query Parameters**:

- `breakpoint` (string, optional, default="lg") - Sidebar expansion breakpoint

**Processing Logic**:

```python
def layout_responsive_demo(request):
    breakpoint = request.GET.get('breakpoint', 'lg')
    if breakpoint not in ['sm', 'md', 'lg', 'xl', 'xxl']:
        breakpoint = 'lg'  # Fallback for invalid values
    return render(request, 'example/layout_responsive.html', {
        'breakpoint': breakpoint,
        'breakpoints': ['sm', 'md', 'lg', 'xl', 'xxl'],
    })
```

**Rationale for Query Parameters**:

- Stateless - no session storage needed
- Shareable URLs - users can bookmark specific configurations
- Simple form handling - GET forms without CSRF complexity
- Natural for testing - easy to programmatically test all combinations

## Key Insights

1. **Stateless Design**: Layout configuration is determined at template render time from component attributes
2. **Additive Classes**: Multiple `fixed_*` attributes result in multiple CSS classes on body element
3. **No Conflicts**: All attribute combinations are valid - AdminLTE CSS handles overlapping fixed elements gracefully
4. **Template Inheritance**: Child templates inherit layout from parent unless explicitly overridden
