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

### Fill Layout (Viewport-Constrained)

```django
<c-app fill>
    {% block content %}
        <h1>Data Dashboard</h1>
        <!-- Tables, charts, or maps that need viewport-constrained scrolling -->
    {% endblock %}
</c-app>
```

**Effect**: Creates a viewport-constrained layout where:

- App-wrapper height is restricted to 100vh (full viewport height)
- Scroll container changes from body to app-wrapper
- App-header and app-footer remain visible while app-main scrolls between them
- Scrollbars are hidden for a clean appearance

**CSS Class**: Adds `.fill` to `.app-wrapper` element.

**Use Cases**:

- **Data Tables**: Keep column headers visible while scrolling large datasets
- **Maps**: Full viewport mapping interfaces (e.g., MapLibre, Leaflet) with fixed controls
- **Dashboards**: Constrain charts and widgets to viewport bounds
- **Fixed Toolbars**: Enables page-layout's internal toolbar-fixed/footer-fixed modes (requires inner page-layout component)

**Example - Data Table Dashboard**:

```django
<c-app fill fixed_sidebar>
    {% block content %}
        <div class="table-responsive">
            <table class="table table-striped">
                <!-- Large dataset with 1000+ rows -->
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in dataset %}
                        <tr>
                            <td>{{ item.id }}</td>
                            <td>{{ item.name }}</td>
                            <td>{{ item.status }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% endblock %}
</c-app>
```

**Example - Map Interface**:

```django
<c-app fill>
    {% block content %}
        <div id="map" style="width: 100%; height: 100%;"></div>
        <script>
            // MapLibre or Leaflet map initialization
            // Map will fill viewport height exactly
        </script>
    {% endblock %}
</c-app>
```

**Behavior Details**:

- **Scroll Container**: With fill enabled, scrolling happens within `.app-wrapper` instead of the `body` element
- **Performance**: Scrollbars are hidden using CSS (`scrollbar-width: none` for Firefox, `::-webkit-scrollbar { display: none }` for Chrome/Safari)
- **Combinations**: Fill can be combined with `fixed_sidebar`, `fixed_header`, `fixed_footer`, but fill's viewport-constrained behavior takes precedence
- **Grid Layout**: The CSS grid structure keeps app-header/footer in view while allowing app-main to scroll

**When to Use Fill**:

- ✅ Data-intensive UIs with large tables or datasets
- ✅ Mapping applications requiring full viewport utilization
- ✅ Dashboards with many widgets that need viewport containment
- ✅ Applications using inner page-layout component with fixed toolbars
- ❌ Simple content pages (blog posts, articles, documentation)
- ❌ Pages with naturally short content that doesn't scroll

**Interactive Demo**: Visit `/layout/?fill=on` to test fill layout behavior with other configuration options.

## Attributes Reference

| Attribute        | Type    | Default | Description                                                   |
| ---------------- | ------- | ------- | ------------------------------------------------------------- |
| `fixed_sidebar`  | boolean | `False` | Makes sidebar fixed (adds `.layout-fixed`)                    |
| `fixed_header`   | boolean | `False` | Makes header fixed (adds `.fixed-header`)                     |
| `fixed_footer`   | boolean | `False` | Makes footer fixed (adds `.fixed-footer`)                     |
| `fill`           | boolean | `False` | Viewport-constrained layout (adds `.fill` to app-wrapper)     |
| `sidebar_expand` | string  | `"lg"`  | Breakpoint where sidebar expands: sm, md, lg, xl, xxl         |

## Template Inheritance Patterns

### Global Layout Configuration

Define a base template with your application's default layout:

```django
{# templates/base.html #}
{% load cotton %}
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{% block title %}{% endblock %}</title>
    <!-- AdminLTE CSS from CDN -->
</head>
<c-app fixed_sidebar fixed_header sidebar_expand="lg">
    <div class="app-header">
        <!-- Navigation header -->
    </div>
    <div class="app-sidebar">
        <!-- Navigation menu -->
    </div>
    <div class="app-main">
        <div class="app-content-header">
            <h1>{% block page_title %}{% endblock %}</h1>
        </div>
        <div class="app-content">
            {% block content %}{% endblock %}
        </div>
    </div>
</c-app>
</html>
```

All pages extending this template inherit the fixed sidebar and header layout.

### Per-Page Layout Override

Different pages can use different layouts by calling `<c-app>` with different attributes:

```django
{# templates/dashboard.html - needs navigation visible #}
{% extends "base.html" %}
{% load cotton %}

{% block content %}
    <!-- This inherits fixed_sidebar + fixed_header from base.html -->
    <div class="dashboard-content">
        <h2>Dashboard</h2>
        <!-- Dashboard widgets -->
    </div>
{% endblock %}
```

```django
{# templates/login.html - clean layout without sidebar #}
{% load cotton %}
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Login</title>
    <!-- AdminLTE CSS from CDN -->
</head>
<c-app class="login-page">
    <div class="login-box">
        <form method="post">
            <!-- Login form -->
        </form>
    </div>
</c-app>
</html>
```

### Conditional Layout Configuration

Use Django context variables to conditionally apply layouts:

```django
{# templates/conditional_base.html #}
{% load cotton %}
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
{% if user.is_staff %}
    {# Admin users get full dashboard layout #}
    <c-app fixed_sidebar fixed_header sidebar_collapsible>
        <div class="admin-header">Admin Dashboard</div>
        {% block admin_content %}{% endblock %}
    </c-app>
{% else %}
    {# Regular users get simplified layout #}
    <c-app fixed_header>
        <div class="user-header">User Portal</div>
        {% block user_content %}{% endblock %}
    </c-app>
{% endif %}
</html>
```

### Layout Inheritance Best Practices

**1. Base Template Strategy**: Define your primary layout in a base template:

```django
{# templates/layouts/dashboard.html #}
{% load cotton %}
<c-app fixed_sidebar fixed_header sidebar_expand="lg" sidebar_collapsible>
    {% include "partials/header.html" %}
    {% include "partials/sidebar.html" %}
    <div class="app-main">
        {% block content %}{% endblock %}
    </div>
</c-app>
```

**2. Page-Specific Inheritance**: Extend the appropriate base:

```django
{# templates/reports/index.html #}
{% extends "layouts/dashboard.html" %}

{% block content %}
    <h1>Reports</h1>
    <!-- Reports content inherits dashboard layout -->
{% endblock %}
```

**3. Override When Needed**: Some pages need different layouts:

```django
{# templates/public/landing.html #}
{% load cotton %}
<c-app>
    <!-- Clean layout without sidebar for landing page -->
    {% block content %}{% endblock %}
</c-app>
```

## Combining Layout Attributes

Multiple layout attributes work together seamlessly to create sophisticated interfaces:

### Fixed Element Combinations

All fixed positioning attributes can be used together:

```django
{# Fixed sidebar + header for dashboard-style applications #}
<c-app fixed_sidebar fixed_header>
    {% block content %}{% endblock %}
</c-app>

{# Fixed header + footer for content-focused layouts #}
<c-app fixed_header fixed_footer>
    {% block content %}{% endblock %}
</c-app>

{# Complete fixed layout with all three elements #}
<c-app fixed_sidebar fixed_header fixed_footer>
    {% block content %}{% endblock %}
</c-app>
```

### Sidebar Combinations

The collapsible sidebar attributes work with fixed positioning:

```django
{# Fixed sidebar with collapse capability #}
<c-app fixed_sidebar sidebar_collapsible>
    {% block content %}{% endblock %}
</c-app>

{# Fixed sidebar with mini-mode enabled by default #}
<c-app fixed_sidebar sidebar_collapsible collapsed>
    {% block content %}{% endblock %}
</c-app>
```

### Custom Breakpoints with Fixed Elements

Customize sidebar behavior while maintaining fixed positioning:

```django
{# Fixed layout with wider sidebar breakpoint #}
<c-app fixed_sidebar fixed_header sidebar_expand="xl">
    {% block content %}{% endblock %}
</c-app>
```

### Complete Combination Example

All attributes can be used together for maximum customization:

```django
{# Enterprise dashboard with full fixed layout and collapsible sidebar #}
<c-app
    fixed_sidebar
    fixed_header
    fixed_footer
    sidebar_collapsible
    sidebar_expand="lg"
    class="custom-dashboard">
    {% block content %}{% endblock %}
</c-app>
```

**Combination Rules**:

- All attributes are additive (no conflicts between them)
- Fixed attributes add CSS classes to the `<body>` tag
- Sidebar attributes work together (collapsible + collapsed = mini-mode enabled)
- Custom CSS classes are preserved alongside generated layout classes

## CSS Classes Generated

The `<c-app>` component applies CSS classes to the `<body>` element based on the attributes:

| Attribute | CSS Class | Effect |
| --------- | --------- | ------ |
| `fixed_sidebar` | `.layout-fixed` | Sidebar becomes sticky positioned |
| `fixed_header` | `.fixed-header` | Header becomes sticky positioned |
| `fixed_footer` | `.fixed-footer` | Footer becomes sticky positioned |
| `sidebar_expand="lg"` | `.sidebar-expand-lg` | Sidebar expands at 992px+ |
| *(always applied)* | `.bg-body-tertiary` | Sets body background color |

**Important**: Layout classes are applied directly to the `<body>` tag for proper AdminLTE CSS compatibility. This ensures that AdminLTE selectors like `body.layout-fixed .app-sidebar` work correctly.

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

## Troubleshooting

### Common Layout Issues

#### Fixed Sidebar Not Sticking

**Problem**: Sidebar scrolls with content instead of remaining fixed.

**Causes & Solutions**:

1. **Missing `fixed_sidebar` attribute**

   ```django
   {# ❌ Wrong - sidebar will scroll #}
   <c-app>
       {% block content %}{% endblock %}
   </c-app>

   {# ✅ Correct - sidebar stays fixed #}
   <c-app fixed_sidebar>
       {% block content %}{% endblock %}
   </c-app>
   ```

2. **CSS conflicts from custom styles**
   - Check if custom CSS is overriding `.layout-fixed` styles
   - Use browser developer tools to inspect the `<body>` element
   - Ensure `position: relative` or `position: absolute` on `.app-sidebar` isn't being overridden

3. **Conflicting AdminLTE CSS versions**
   - Verify you're using AdminLTE 4.x (check CDN links)
   - Ensure no AdminLTE 3.x CSS is loaded simultaneously

#### Sidebar Doesn't Expand at Expected Screen Size

**Problem**: Sidebar remains collapsed on screens where it should expand.

**Causes & Solutions**:

1. **Incorrect `sidebar_expand` value**

   ```django
   {# ❌ Wrong - typo in breakpoint name #}
   <c-app sidebar_expand="large">
       {% block content %}{% endblock %}
   </c-app>

   {# ✅ Correct - use valid Bootstrap breakpoint #}
   <c-app sidebar_expand="lg">
       {% block content %}{% endblock %}
   </c-app>
   ```

2. **Valid breakpoint values**: `sm`, `md`, `lg`, `xl`, `xxl`
   - `sm` (576px+): Mobile landscape and above
   - `md` (768px+): Tablets and above
   - `lg` (992px+): Desktops and above *(default)*
   - `xl` (1200px+): Wide screens and above
   - `xxl` (1400px+): Ultra-wide screens

3. **Browser zoom affecting breakpoints**
   - Test at 100% zoom level
   - Check actual pixel width with browser developer tools

#### Header/Footer Not Fixed

**Problem**: Header or footer scrolls with content instead of staying fixed.

**Causes & Solutions**:

1. **Missing fixed attributes**

   ```django
   {# ❌ Wrong - header scrolls #}
   <c-app fixed_sidebar>
       {% block content %}{% endblock %}
   </c-app>

   {# ✅ Correct - header stays fixed #}
   <c-app fixed_sidebar fixed_header>
       {% block content %}{% endblock %}
   </c-app>
   ```

2. **Verify CSS classes on `<body>` element**
   - `fixed_header` should add `.fixed-header` class
   - `fixed_footer` should add `.fixed-footer` class
   - Use browser inspector: right-click → Inspect Element on body tag

#### Content Area Not Scrolling Properly

**Problem**: Fixed layouts cause content to be cut off or scroll issues.

**Causes & Solutions**:

1. **Content height conflicts**
   - Ensure your content doesn't have conflicting `height: 100vh` or `height: 100%` styles
   - Use `min-height` instead of `height` for full-page content

2. **Check AdminLTE CSS loading**

   ```django
   {# Ensure AdminLTE CSS is properly loaded #}
   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/admin-lte@4.0.0-alpha2/dist/css/adminlte.min.css">
   ```

3. **Z-index conflicts**
   - Fixed elements use specific z-index values
   - Avoid setting high z-index values on custom elements that might overlay fixed navigation

#### Layout Classes Not Applied

**Problem**: Inspect element shows CSS classes are missing from `<body>` tag.

**Diagnosis Steps**:

1. **Check component usage**

   ```django
   {# Verify component is properly called #}
   {% load cotton %}
   <c-app fixed_sidebar fixed_header>
       {% block content %}{% endblock %}
   </c-app>
   ```

2. **Verify Cotton is installed and loaded**
   - Ensure `django-cotton` is in `INSTALLED_APPS`
   - Check that `{% load cotton %}` is present in template

3. **Check for template errors**
   - Look in Django debug output for template rendering errors
   - Verify all template blocks are properly closed

#### Mobile Responsiveness Issues

**Problem**: Layout doesn't work properly on mobile devices.

**Solutions**:

1. **Add viewport meta tag**

   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1">
   ```

2. **Test different `sidebar_expand` values**

   ```django
   {# For mobile-first approach #}
   <c-app sidebar_expand="sm">
       {% block content %}{% endblock %}
   </c-app>
   ```

3. **Consider touch interactions**
   - Fixed sidebars become drawer-style on small screens
   - Test touch/swipe interactions for sidebar toggle

### Debugging Steps

1. **Inspect the `<body>` element** in browser developer tools
   - Look for expected CSS classes: `.layout-fixed`, `.fixed-header`, `.fixed-footer`, `.sidebar-expand-{breakpoint}`

2. **Check the Network tab** for CSS loading issues
   - Verify AdminLTE CSS loads successfully (200 status)
   - Look for any 404 errors on CSS files

3. **Test with minimal example**

   ```django
   {% load cotton %}
   <c-app fixed_sidebar>
       <div style="height: 2000px; background: linear-gradient(red, blue);">
           <h1>Test Content</h1>
           <p>Scroll to test fixed behavior</p>
       </div>
   </c-app>
   ```

4. **Enable Django debug mode** to see template rendering errors

5. **Check browser console** for JavaScript errors that might interfere with layout

### Browser Compatibility

**Supported Browsers**:

- Chrome 56+ ✅
- Firefox 59+ ✅
- Safari 13+ ✅
- Edge 16+ ✅

**Unsupported**:

- Internet Explorer (all versions) ❌
- Very old mobile browsers ❌

### Performance Considerations

- Fixed positioning uses `position: sticky` and `position: fixed` which are GPU-accelerated
- Large sidebars with many menu items may affect scroll performance on lower-end devices
- Test with content >1000 lines to verify smooth scrolling

## See Also

- [AdminLTE 4 Layout Behavior Analysis](../adminlte-4-layout-behavior-analysis.md) - Deep dive into CSS classes and positioning
- [Feature Specification](../../specs/002-layout-configuration/spec.md) - User stories and requirements
- [Quick Start Guide](../../specs/002-layout-configuration/quickstart.md) - Usage scenarios and examples
