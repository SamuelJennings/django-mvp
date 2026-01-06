# App Wrapper Component

**Component**: `<c-app>`
**File**: `mvp/templates/cotton/app/index.html`
**Status**: ✅ Implemented

## Overview

The app wrapper component provides the complete AdminLTE 4 grid-based layout structure with configurable fixed positioning for sidebar, header, and footer elements. This component wraps your entire application layout and controls the overall page behavior.

## Architecture

The `<c-app>` component implements AdminLTE 4's `.app-wrapper` grid container with these major sections:

- `.app-sidebar` - Navigation sidebar
- `.app-header` - Top navigation bar
- `.app-main` - Main content area
  - `.app-content-header` - Page header/breadcrumbs
  - `.app-content` - Page content
- `.app-footer` - Optional footer

## Usage

### Default Layout (All Elements Scroll)

```django
<c-app>
    {% block content %}
        <h1>My Page</h1>
    {% endblock %}
</c-app>
```

All layout elements scroll naturally with the page content.

### Fixed Sidebar

```django
<c-app fixed_sidebar>
    {% block content %}
        <h1>Dashboard</h1>
    {% endblock %}
</c-app>
```

**Effect**: Sidebar remains fixed (sticky) on the left during vertical scrolling.

**CSS Class**: Adds `.layout-fixed` to body element.

**Use Case**: Admin dashboards and data-centric applications where navigation should remain visible while scrolling through content.

**Responsive Behavior**: On mobile devices (below sidebar_expand breakpoint), sidebar collapses to a drawer. Fixed positioning applies when sidebar is expanded.

### Fixed Header

```django
<c-app fixed_header>
    {% block content %}
        <h1>Long Article</h1>
        <p>Content...</p>
    {% endblock %}
</c-app>
```

**Effect**: Top navigation bar remains fixed at the top during vertical scrolling.

**CSS Class**: Adds `.fixed-header` to body element.

**Use Case**: Applications with important navigation or branding that should remain visible, or when using sticky elements in the header.

### Fixed Footer

```django
<c-app fixed_footer>
    {% block content %}
        <h1>Terms of Service</h1>
    {% endblock %}
</c-app>
```

**Effect**: Footer remains fixed at the bottom during scrolling.

**CSS Class**: Adds `.fixed-footer` to body element.

**Use Case**: Copyright notices, status information, or action buttons that should remain accessible.

### Combining Fixed Elements

Multiple fixed attributes can be enabled simultaneously:

```django
<!-- Fixed sidebar + header -->
<c-app fixed_sidebar fixed_header>
    {% block content %}
        <h1>Admin Panel</h1>
    {% endblock %}
</c-app>

<!-- Fixed header + footer -->
<c-app fixed_header fixed_footer>
    {% block content %}
        <h1>Documentation</h1>
    {% endblock %}
</c-app>

<!-- Complete fixed layout -->
<c-app fixed_sidebar fixed_header fixed_footer>
    {% block content %}
        <h1>Full Fixed Layout</h1>
    {% endblock %}
</c-app>
```

**Effect**: All specified elements remain fixed. Only the main content area scrolls.

**CSS Classes**: Adds all corresponding classes (`.layout-fixed`, `.fixed-header`, `.fixed-footer`) to body element.

**Use Case**: Complex applications requiring maximum navigation accessibility.

### Responsive Sidebar Control

```django
<!-- Sidebar expands at medium breakpoint (768px) -->
<c-app sidebar_expand="md">
    {% block content %}
        <h1>My App</h1>
    {% endblock %}
</c-app>

<!-- Sidebar expands at extra-large breakpoint (1200px) -->
<c-app sidebar_expand="xl">
    {% block content %}
        <h1>Wide Layout App</h1>
    {% endblock %}
</c-app>
```

**Effect**: Controls at which Bootstrap breakpoint the sidebar expands from collapsed (drawer) to expanded (visible) state.

**CSS Classes**: Adds `.sidebar-expand-{breakpoint}` to body element.

**Default**: `lg` (992px - sidebar expands on desktops)

**Available Values**:
- `sm` (576px) - Sidebar expands on mobile landscape
- `md` (768px) - Sidebar expands on tablets
- `lg` (992px) - Sidebar expands on desktops *(default)*
- `xl` (1200px) - Sidebar expands on wide screens
- `xxl` (1400px) - Sidebar expands on ultra-wide screens

**Use Case**: Adjust sidebar behavior based on your application's content density and typical screen sizes.

**Interaction with fixed_sidebar**: The `fixed_sidebar` attribute makes the sidebar sticky when it's in expanded state. On smaller screens (below the `sidebar_expand` breakpoint), the sidebar becomes a collapsible drawer regardless of `fixed_sidebar` setting.

## Attributes Reference

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `fixed_sidebar` | boolean | `False` | Makes sidebar fixed (adds `.layout-fixed`) |
| `fixed_header` | boolean | `False` | Makes header fixed (adds `.fixed-header`) |
| `fixed_footer` | boolean | `False` | Makes footer fixed (adds `.fixed-footer`) |
| `sidebar_expand` | string | `"lg"` | Breakpoint where sidebar expands: sm, md, lg, xl, xxl |

## Template Inheritance Patterns

### Global Layout Configuration

Define a base template with your application's default layout:

```django
{# templates/base.html #}
{% load cotton %}
<c-app fixed_sidebar sidebar_expand="lg">
    {% block content %}{% endblock %}
</c-app>
```

All pages extending this template inherit the fixed sidebar layout.

### Per-Page Layout Override

Different pages can use different layouts by calling `<c-app>` with different attributes:

```django
{# templates/dashboard.html - needs navigation visible #}
{% load cotton %}
<c-app fixed_sidebar fixed_header>
    <h1>Dashboard</h1>
</c-app>

{# templates/article.html - immersive reading experience #}
{% load cotton %}
<c-app>
    <h1>Article Title</h1>
    <p>Content...</p>
</c-app>
```

## CSS Classes Generated

The `<c-app>` component applies CSS classes to the `<body>` element based on the attributes:

| Attribute | CSS Class | Effect |
|-----------|-----------|--------|
| `fixed_sidebar` | `.layout-fixed` | Sidebar becomes sticky positioned |
| `fixed_header` | `.fixed-header` | Header becomes sticky positioned |
| `fixed_footer` | `.fixed-footer` | Footer becomes sticky positioned |
| `sidebar_expand="lg"` | `.sidebar-expand-lg` | Sidebar expands at 992px+ |
| *(always applied)* | `.bg-body-tertiary` | Sets body background color |

## Accessibility

- **Keyboard Navigation**: All fixed elements remain keyboard accessible
- **Screen Readers**: Fixed positioning does not affect screen reader navigation order
- **Focus Management**: Focus remains visible when scrolling content
- **Skip Links**: Consider adding skip navigation links for fixed layouts with extensive sidebar navigation

## Browser Compatibility

Fixed positioning is implemented using CSS `position: sticky` and `position: fixed`, which are supported in all modern browsers:

- Chrome 56+
- Firefox 59+
- Safari 13+
- Edge 16+

## Related Components

- **Sidebar Menu**: Use with `<c-flex-menus>` for dynamic menu generation
- **Navbar**: Customize header content via `navbar_left` and `navbar_right` blocks
- **Content Header**: Add page titles and breadcrumbs via `page_title` and `breadcrumbs` blocks

## Examples

### Complete Dashboard Layout

```django
{% load cotton %}
<c-app fixed_sidebar fixed_header sidebar_expand="lg">
    {% block sidebar_menu %}
        <c-flex-menus menu="main" />
    {% endblock %}

    {% block page_title %}
        Dashboard
    {% endblock %}

    {% block content %}
        <div class="row">
            <div class="col-lg-3">
                <c-small-box
                    heading="150"
                    text="New Orders"
                    icon="cart"
                    variant="primary"
                />
            </div>
            <!-- More widgets -->
        </div>
    {% endblock %}
</c-app>
```

### Mobile-Optimized Layout

```django
{% load cotton %}
<c-app sidebar_expand="md">
    {# Sidebar expands on tablet and above #}
    {% block content %}
        <h1>Mobile-First App</h1>
    {% endblock %}
</c-app>
```

## Testing

The component's layout attributes are fully tested in `tests/test_app_component.py`:

- Individual fixed attributes (`fixed_sidebar`, `fixed_header`, `fixed_footer`)
- Combinations of fixed attributes
- Per-page layout configuration patterns
- Responsive sidebar breakpoints
- Default (no fixed elements) layout

## See Also

- [AdminLTE 4 Layout Behavior Analysis](../adminlte-4-layout-behavior-analysis.md) - Deep dive into CSS classes and positioning
- [Feature Specification](../../specs/003-adminlte-layout-config/spec.md) - User stories and requirements
- [Quick Start Guide](../../specs/003-adminlte-layout-config/quickstart.md) - Usage scenarios and examples
