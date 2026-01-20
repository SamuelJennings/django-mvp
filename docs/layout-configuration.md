# Layout Configuration System

**Feature**: AdminLTE 4 Layout Configuration via `<c-app>` Component
**Status**: ✅ Implemented
**Version**: Added in v0.1.0

## Overview

Django MVP provides a comprehensive layout configuration system through the `<c-app>` component, allowing you to control the positioning and behavior of major layout elements (sidebar, header, footer) and enable specialized viewport-constrained layouts for data-intensive applications.

All layout configurations are controlled via simple boolean attributes on the `<c-app>` component, with no JavaScript required for basic functionality.

## Quick Reference

| Attribute        | Type    | Default | Purpose                                    | Use Case                           |
| ---------------- | ------- | ------- | ------------------------------------------ | ---------------------------------- |
| `fixed_sidebar`  | boolean | `False` | Makes sidebar sticky during scroll         | Admin dashboards                   |
| `fixed_header`   | boolean | `False` | Keeps navbar fixed at top                  | Important navigation               |
| `fixed_footer`   | boolean | `False` | Keeps footer fixed at bottom               | Status/action bars                 |
| `fill`           | boolean | `False` | Viewport-constrained scrolling (100vh)     | Data tables, maps, dashboards      |
| `sidebar_expand` | string  | `"lg"`  | Breakpoint for sidebar expansion           | Responsive sidebar behavior        |

## Layout Options

### Fixed Sidebar

**Attribute**: `fixed_sidebar`

Makes the sidebar remain visible (sticky) during vertical scrolling. The sidebar scrolls independently when it contains more content than fits in the viewport.

**Example**:

```django
<c-app fixed_sidebar>
    <c-app.sidebar>
        <!-- Sidebar navigation -->
    </c-app.sidebar>
</c-app>
```

**CSS Class**: Adds `.layout-fixed` to `<body>` element

**Use Cases**:

- Admin dashboards where navigation should always be accessible
- Applications with extensive menu structures
- Data-centric interfaces requiring constant navigation access
- Sites that require widgets in the navbar

**Responsive Behavior**: On screens below the `sidebar_expand` breakpoint, the sidebar becomes a collapsible drawer. Fixed positioning applies when expanded.

---

### Fixed Header

**Attribute**: `fixed_header`

Keeps the top navigation bar fixed at the top of the viewport during scrolling.

**Example**:

```django
<c-app fixed_header>
    <c-app.header>
        <!-- Top navigation bar -->
    </c-app.header>
</c-app>
```

**CSS Class**: Adds `.fixed-header` to `<body>` element

**Use Cases**:

- Applications with important branding in header
- Sites requiring constant access to search or user menu
- Long-form content where navigation should remain accessible

---

### Fixed Footer

**Attribute**: `fixed_footer`

Keeps the footer visible at the bottom of the viewport during scrolling.

**Example**:

```django
<c-app fixed_footer>
    <c-app.footer>
        <!-- Footer content -->
    </c-app.footer>
</c-app>
```

**CSS Class**: Adds `.fixed-footer` to `<body>` element

**Use Cases**:

- Copyright notices or legal disclaimers
- Status bars showing connection status
- Action buttons that should remain accessible

---

### Fill Layout (Viewport-Constrained)

**Attribute**: `fill`

**NEW in v0.1.0** - Creates a viewport-constrained layout perfect for data-intensive applications. The app-wrapper is restricted to 100vh height, scroll container changes from body to app-wrapper, and scrollbars are hidden for a clean appearance.

**Example**:

```django
<c-app fill>
    {% block content %}
        <h1>Data Dashboard</h1>
        <div class="table-responsive">
            <table class="table">
                <!-- Large dataset with 1000+ rows -->
            </table>
        </div>
    {% endblock %}
</c-app>
```

**CSS Class**: Adds `.fill` to `.app-wrapper` element

**Behavior**:

- App-wrapper height restricted to 100vh (full viewport height)
- Scroll container changes from body to app-wrapper
- App-header and app-footer remain visible (if declared)
- App-main scrolls between them
- Scrollbars hidden for clean appearance

**Use Cases**:

- Data tables with large datasets requiring scrollable content
- Map interfaces needing full viewport utilization
- Dashboards with fixed toolbars

**When to Use Fill**:

- ✅ Data-intensive UIs with large tables or datasets
- ✅ Mapping applications requiring full viewport utilization
- ✅ Dashboards with many widgets needing viewport containment
- ✅ Applications using inner page-layout component with fixed toolbars
- ❌ Simple content pages (blog posts, articles, documentation)
- ❌ Pages with naturally short content that doesn't scroll

**Interactive Demo**: Visit `/layout/?fill=on` to test fill layout behavior.

---

### Sidebar Expansion Breakpoint

**Attribute**: `sidebar_expand`

Controls at which Bootstrap breakpoint the sidebar transitions from collapsed (drawer) to expanded (visible) state.

**Example**:

```django
<c-app sidebar_expand="md">
    <c-app.sidebar>
        <!-- Sidebar expands on tablets and above (≥768px) -->
    </c-app.sidebar>
</c-app>
```

**CSS Class**: Adds `.sidebar-expand-{breakpoint}` to `<body>` element

**Available Values**:

- `sm` (576px) - Sidebar expands on mobile landscape
- `md` (768px) - Sidebar expands on tablets
- `lg` (992px) - Sidebar expands on desktops *(default)*
- `xl` (1200px) - Sidebar expands on wide screens
- `xxl` (1400px) - Sidebar expands on ultra-wide screens

**Use Cases**:

- Adjust for content density and typical user screen sizes
- Mobile-first apps can use `sm` or `md`
- Desktop-focused apps can use `xl` or `xxl`

## Combining Layout Options

Multiple layout attributes work together seamlessly:

### Complete Fixed Layout

All elements remain fixed while only the main content scrolls:

```django
<c-app fixed_sidebar fixed_header fixed_footer>
    <c-app.header>
        <!-- Top navigation -->
    </c-app.header>

    <c-app.sidebar>
        <!-- Side navigation -->
    </c-app.sidebar>

    <c-app.footer>
        <!-- Footer content -->
    </c-app.footer>
</c-app>
```

### Fill Layout with Sidebar

Perfect for data dashboards requiring sidebar navigation:

```django
<c-app fill sidebar_expand="lg">
    <c-app.sidebar>
        <!-- Sidebar navigation -->
    </c-app.sidebar>
</c-app>
```

### Responsive Layout with Fixed Header

Header stays visible while sidebar adapts to screen size:

```django
<c-app fixed_header sidebar_expand="md">
    <c-app.header>
        <!-- Fixed branding/navigation -->
    </c-app.header>

    <c-app.sidebar>
        <!-- Responsive sidebar -->
    </c-app.sidebar>
</c-app>
```

## Configuration Patterns

### Global Default Layout

Define your application's default layout in a base template:

```django
{# templates/base.html #}
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{% block title %}My App{% endblock %}</title>
</head>
<c-app fixed_header sidebar_expand="lg">
    <c-app.header>
        <!-- Your header/navbar content -->
    </c-app.header>

    <c-app.sidebar>
        <!-- Your sidebar/menu content -->
    </c-app.sidebar>

    <c-app.footer>
        <!-- Your footer content -->
    </c-app.footer>

    {% block content %}{% endblock %}
</c-app>
</html>
```

All pages extending this template inherit the fixed header and responsive sidebar.
