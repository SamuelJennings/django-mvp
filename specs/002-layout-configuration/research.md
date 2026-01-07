# Research: AdminLTE Layout Configuration System

**Feature**: 002-layout-configuration
**Date**: January 5, 2026
**Status**: Complete

## Overview

This document consolidates research findings for implementing AdminLTE 4 layout configuration via Cotton component attributes. Research revealed that core implementation already exists in the `<c-app>` component.

## Key Findings

### 1. Existing Implementation

**Location**: `mvp/templates/cotton/app/index.html`

The `<c-app>` component already implements all required layout attributes:

```django-html
<c-vars class
        fixed_sidebar
        fixed_header
        fixed_footer
        sidebar_collapsible
        collapsed
        sidebar_expand="lg" />
<body class="bg-body-tertiary{% if fixed_sidebar %} layout-fixed{% endif %}{% if fixed_header %} fixed-header{% endif %}{% if fixed_footer %} fixed-footer{% endif %}{% if sidebar_collapsible %} sidebar-mini{% if collapsed %} sidebar-collapse{% endif %}{% endif %} sidebar-expand-{{ sidebar_expand }} {{ class }}">
  <div class="app-wrapper">{{ slot }}</div>
</body>
```

**Status**: ✅ All three layout attributes (`fixed_sidebar`, `fixed_header`, `fixed_footer`) are implemented and functional.

### 2. AdminLTE CSS Class Mapping

Based on [AdminLTE 4 Layout Behavior Analysis](../../../docs/adminlte-4-layout-behavior-analysis.md):

| Boolean Attribute | AdminLTE Body Class | Behavior |
|-------------------|---------------------|----------|
| `fixed_sidebar` | `.layout-fixed` | Sidebar uses `position: sticky`, 100vh height, scrollable content |
| `fixed_header` | `.fixed-header` | Header uses `position: sticky` at top of viewport |
| `fixed_footer` | `.fixed-footer` | Footer uses `position: sticky` at bottom of viewport |

**Combinations**:

- All three together = "Fixed Complete" layout (entire app frame fixed, only content scrolls)
- Any subset = Partial fixed layout

### 3. Cotton Component Patterns

**Boolean Attribute Pattern**:

```django-html
<!-- Declaration in <c-vars> -->
<c-vars fixed_sidebar fixed_header />

<!-- Conditional class application -->
{% if fixed_sidebar %} layout-fixed{% endif %}

<!-- Usage in templates -->
<c-app fixed_sidebar fixed_header>
  ...
</c-app>
```

**String Attribute Pattern** (for sidebar_expand):

```django-html
<!-- Declaration with default -->
<c-vars sidebar_expand="lg" />

<!-- Direct interpolation -->
sidebar-expand-{{ sidebar_expand }}

<!-- Usage -->
<c-app sidebar_expand="md">
  ...
</c-app>
```

### 4. Testing Approach

**Test Framework**: pytest-django with `django_cotton.render_component()`

**Example test structure** (from existing tests):

```python
from django_cotton import render_component
from django.template import RequestContext
from pytest_django.fixtures import rf

def test_fixed_sidebar_renders_layout_fixed_class(rf):
    """Test that fixed_sidebar attribute adds .layout-fixed to body element."""
    html = render_component(
        "app",
        context=RequestContext(rf.get("/"), {"fixed_sidebar": True})
    )
    assert 'class="bg-body-tertiary layout-fixed' in html
    assert '<div class="app-wrapper">' in html
```

### 5. Responsive Behavior

**Key Finding**: Fixed layout and responsive sidebar are independent concerns.

- `fixed_sidebar` → Controls sticky positioning (works at all viewport sizes)
- `sidebar_expand="lg"` → Controls when sidebar is visible vs off-canvas
- These can be combined: `<c-app fixed_sidebar sidebar_expand="md">`

**Breakpoint values**: `sm`, `md`, `lg` (default), `xl`, `xxl`

## Technology Decisions

### Decision 1: Component Attribute Approach (Already Implemented)

**Chosen**: Separate boolean attributes per layout element

**Rationale**:

- Maximum flexibility - can combine any fixed elements
- Clear, explicit syntax: `<c-app fixed_sidebar fixed_header>`
- Follows Bootstrap/AdminLTE conventions (each feature independently toggled)
- Already implemented and working in codebase

**Alternatives Considered**:

- Single `layout` attribute with combined values (e.g., `layout="fixed-sidebar fixed-header"`)
  - Rejected: Less flexible, requires string parsing, conflicts with potential CSS class usage
- Preset layouts (e.g., `layout="complete"`)
  - Rejected: Less flexible, requires maintaining preset definitions

### Decision 2: CSS Class Generation Location

**Chosen**: Generate classes directly in `<c-app>` component's `<body>` tag

**Rationale**:

- AdminLTE requires classes on body element for layout behavior
- Cotton components can render any HTML (including body)
- Keeps layout logic centralized in one component
- Already implemented pattern in codebase

**Alternatives Considered**:

- Context processor + base template
  - Rejected: Would require settings-based config, less flexible than component attributes
- JavaScript-based class injection
  - Rejected: Requires JS, increases complexity, breaks SSR

### Decision 3: Testing Strategy

**Chosen**: pytest-django unit tests with `render_component()`

**Rationale**:

- Fast, deterministic tests
- No browser overhead
- Can test all attribute combinations
- Follows project constitution (Test-First)

**Test Coverage Required**:

- Each individual fixed attribute renders correct class
- Combinations of fixed attributes work together
- Default behavior (no attributes)
- Edge case: contradictory attributes (e.g., `fixed_sidebar fixed_sidebar="false"`)

## Dependencies

### Existing Dependencies (No Changes)

- Django 4.2+
- django-cotton
- Bootstrap 5
- AdminLTE 4 CSS (via CDN in base.html)

### No New Dependencies Required

All functionality uses existing Cotton component patterns.

## Open Questions (Resolved)

1. ~~Component naming?~~ → Resolved: `<c-app>` (no `mvp` prefix)
2. ~~Attribute format?~~ → Resolved: Separate boolean attributes
3. ~~Fixed complete as separate option?~~ → Resolved: No, combine all three attributes
4. ~~Mobile behavior?~~ → Resolved: Fixed layout independent from sidebar_expand breakpoint
5. ~~Custom areas support?~~ → Resolved: Out of scope

## References

- [AdminLTE 4 Layout Behavior Analysis](../../../docs/adminlte-4-layout-behavior-analysis.md)
- [django-cotton Documentation](https://django-cotton.com/)
- [AdminLTE 4 Demo](https://adminlte.io/themes/v4/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)

## Demo View Requirements (Clarified 2026-01-06)

### Decision 4: Demo View Architecture

**Location**: `example/` app within django-mvp package

**Rationale**:

- Keeps demo code separate from production package
- The `example/` app already exists and is designed for this purpose
- Makes it clear these are reference implementations, not required components

### Decision 5: Demo View Content Strategy

**Fixed Properties Demo** (`/example/layout-fixed/`):

- Form with 3 checkboxes (fixed_header, fixed_sidebar, fixed_footer)
- Submits via GET request to same page with query parameters
- Long-form content with multiple sections (2-3 viewport heights)
- Several dummy sidebar menu items (12-15) to demonstrate independent scrolling
- Minimal helper text explaining what to test
- Visual indicators showing current configuration state

**Responsive Breakpoint Demo** (`/example/layout-responsive/`):

- Dropdown selector listing all breakpoints (sm, md, lg, xl, xxl)
- Submits GET request with `breakpoint` query parameter
- Same content structure as fixed properties demo
- Instructions to resize browser window to test breakpoint transitions
- Visual indicator showing currently selected breakpoint

**Content Structure** (both demos):

1. Helper text at top ("Scroll to test fixed elements" / "Resize window to test breakpoint")
2. Configuration form (checkboxes or dropdown)
3. Visual status indicator (current config, applied CSS classes)
4. 2-3 content sections with:
   - Section headings
   - Paragraphs (2-3 per section)
   - Sample data table
5. Sidebar with 12-15 dummy menu items grouped into categories

**Implementation Pattern**:

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

def layout_responsive_demo(request):
    breakpoint = request.GET.get('breakpoint', 'lg')
    if breakpoint not in ['sm', 'md', 'lg', 'xl', 'xxl']:
        breakpoint = 'lg'
    return render(request, 'example/layout_responsive.html', {
        'breakpoint': breakpoint,
        'breakpoints': ['sm', 'md', 'lg', 'xl', 'xxl'],
    })
```

## Next Steps (Phase 1)

1. Create data-model.md (minimal - only layout configuration entities)
2. Create contracts/ (N/A for this feature - no API)
3. Create quickstart.md (usage documentation with examples)
4. Update agent context with new technology decisions
