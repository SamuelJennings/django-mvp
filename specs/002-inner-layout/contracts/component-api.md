# Component API Contract

**Feature**: 002-inner-layout  
**Version**: 1.0.0  
**Date**: 2025-12-23

## Contract Overview

This document defines the stable API contract for the `inner` layout component. Breaking changes to this contract require a MAJOR version bump per semantic versioning.

## Component Signature

**File**: `mvp/templates/cotton/layouts/inner.html`  
**Namespace**: `c-layouts.inner`

### Required Parameters

None - component works with zero configuration.

### Optional Parameters

| Parameter | Type | Default | Constraints | Description |
|-----------|------|---------|-------------|-------------|
| `primary_width` | CSS length | `280px` | Must be valid CSS length (px, rem, %, etc.) | Width of primary_sidebar at ≥breakpoint |
| `secondary_width` | CSS length | `250px` | Must be valid CSS length | Width of secondary_sidebar at ≥breakpoint |
| `breakpoint` | String | `md` | Must be valid Bootstrap breakpoint: `sm`, `md`, `lg`, `xl`, `xxl` | Viewport size below which sidebars become offcanvas |
| `gap` | String/Number | `0` | Bootstrap gap value: `0-5` or CSS length | Spacing between columns (Bootstrap gap utility) |
| `collapse_primary` | String boolean | `false` | `"true"` or `"false"` (string values) | Enable collapse toggle for primary_sidebar |
| `collapse_secondary` | String boolean | `false` | `"true"` or `"false"` (string values) | Enable collapse toggle for secondary_sidebar |
| `class` | String | `` | Any valid CSS class names | Additional classes applied to `.content-shell` container |

### Slots

| Slot Name | Required | Type | Description |
|-----------|----------|------|-------------|
| `(default)` | Yes | HTML content | Main page content. Uses default unnamed slot `{{ slot }}`. Always rendered. Expands to fill available width. |
| `primary_sidebar` | No | HTML content | Left sidebar content. Not rendered if empty . Becomes offcanvas at <breakpoint. |
| `secondary_sidebar` | No | HTML content | Right sidebar content. Not rendered if empty. Becomes offcanvas at <breakpoint. |

## Usage Examples

### Minimal Usage (Zero Configuration)

```django-html
{% load cotton %}

<c-layouts.inner>
  <h1>Main Content</h1>
  <p>This uses all default settings.</p>
</c-layouts.inner>
```

**Behavior**: Renders single-column layout (no sidebars) with main content filling width.

### Single Sidebar

```django-html
<c-layouts.inner>
  <c-slot name="primary_sidebar">
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  </c-slot>
  
  <h1>Main Content</h1>
  <p>With navigation sidebar on the left.</p>
</c-layouts.inner>
```

**Behavior**: Two-column layout with 280px primary sidebar (left) and expanding main content. Sidebar becomes offcanvas below md (768px).

### Dual Sidebar

```django-html
<c-layouts.inner>
  <c-slot name="primary_sidebar">
    <nav>Navigation</nav>
  </c-slot>
  
  <c-slot name="secondary_sidebar">
    <aside>Related Content</aside>
  </c-slot>
  
  <h1>Main Content</h1>
</c-layouts.inner>
```

**Behavior**: Three-column layout with both sidebars. Both become offcanvas below md.

### Custom Configuration

```django-html
<c-layouts.inner 
  primary_width="320px"
  secondary_width="280px"
  breakpoint="lg"
  gap="3"
  collapse_primary="true"
  class="my-custom-layout">
  
  <c-slot name="primary_sidebar">
    <nav>Wide Navigation</nav>
  </c-slot>
  
  <h1>Custom Layout</h1>
</c-layouts.inner>
```

**Behavior**: 
- Primary sidebar 320px wide (custom)
- Offcanvas mode below lg (992px) instead of md
- 1rem gap between columns (Bootstrap gap-3)
- Collapse toggle enabled for primary sidebar
- Custom class applied to container

### Collapse-Enabled Sidebar

```django-html
<c-layouts.inner collapse_primary="true">
  <c-slot name="primary_sidebar">
    <div class="sidebar-content">
      <div class="sidebar-item">
        <i class="bi bi-house collapsed-only"></i>
        <span class="expanded-only">Home</span>
      </div>
      <div class="sidebar-item">
        <i class="bi bi-info-circle collapsed-only"></i>
        <span class="expanded-only">About</span>
      </div>
    </div>
  </c-slot>
  
  <h1>Main Content</h1>
</c-layouts.inner>
```

**Behavior**: 
- Collapse toggle button appears on primary sidebar
- When collapsed: Only icons (`.collapsed-only`) visible, width reduces to fit-content
- When expanded: Full text (`.expanded-only`) visible, width is 280px
- Collapse disabled in offcanvas mode (<md)

## Contract Guarantees

### Empty Slot Handling

**Contract**: Empty slots MUST NOT render containers.

**Definition of Empty**: 
- Slot not declared, OR
- Slot declared with empty string, OR
- Slot declared with whitespace only, OR
- Slot declared with HTML comments only

**Test**:
```python
def test_empty_slot_contract():
    """Empty sidebar slots must not render containers"""
    html = render_to_string('cotton/layouts/inner.html', {
        'slot': '<h1>Main</h1>',
        'primary_sidebar': '   \n  ',  # Whitespace
    })
    assert 'content-sidebar-left' not in html
    assert 'primarySidebar' not in html
```

### Responsive Behavior

**Contract**: At viewport < breakpoint, sidebars MUST switch to offcanvas mode.

**Offcanvas Mode Requirements**:
1. Sidebars hidden by default
2. Offcanvas toggle buttons visible
3. Clicking toggle shows sidebar as overlay
4. Backdrop dims background
5. Close button, Escape key, and backdrop click close offcanvas
6. Collapse mode disabled (constraint)

### Collapse Constraint

**Contract**: Sidebars MUST NOT collapse when in offcanvas mode.

**Enforcement**:
- Collapse toggle buttons hidden at <breakpoint
- JavaScript prevents collapse when viewport <breakpoint
- Entering offcanvas mode clears collapsed state

### Accessibility

**Contract**: Component MUST provide accessible landmarks and navigation.

**Requirements**:
1. Main content has `role="main"`
2. Sidebars have `role="complementary"`
3. All regions have `aria-label`
4. Offcanvas has `role="dialog"` and `aria-modal="true"` (Bootstrap managed)
5. Toggle buttons have `aria-controls` and `aria-label`
6. Keyboard navigable (Tab, Escape)

### CSS Variable Support

**Contract**: Component MUST apply configuration as CSS variables for runtime theming.

**Variables**:
- `--content-primary-width`: Set to `primary_width` parameter
- `--content-secondary-width`: Set to `secondary_width` parameter

**Usage**: Consumers can override these variables via custom CSS without modifying component.

## Breaking Changes

The following changes would require a MAJOR version bump:

1. **Removing or renaming slots** (e.g., renaming `primary_sidebar` to `left_sidebar`)
2. **Changing parameter names** (e.g., `primary_width` → `sidebar_width`)
3. **Changing default behavior** (e.g., changing default breakpoint from `md` to `lg`)
4. **Removing CSS classes** from the public API (e.g., removing `.content-shell`)
5. **Changing slot semantics** (e.g., making `primary_sidebar` use named slot instead of default)
6. **Removing data attribute support**

## Non-Breaking Changes

The following changes are allowed in MINOR or PATCH versions:

1. **Adding new optional parameters** with defaults
2. **Adding new slots** (as long as they're optional)
3. **Adding new CSS classes** (as long as existing classes still work)
4. **Improving accessibility** (adding ARIA attributes, improving focus management)
5. **Performance optimizations** (as long as behavior unchanged)
6. **Bug fixes** (e.g., fixing empty slot detection edge case)

## Deprecation Policy

When deprecating part of the API:

1. **Announce** in CHANGELOG with version where deprecation starts
2. **Maintain backwards compatibility** for at least one MAJOR version
3. **Provide migration path** in documentation
4. **Use console warnings** (if applicable) to alert developers
5. **Remove** in next MAJOR version

Example:
- v1.5.0: Add new `sidebar_primary` parameter, deprecate `primary_sidebar`
- v1.x.x: Both parameters work, `primary_sidebar` logs deprecation warning
- v2.0.0: Remove `primary_sidebar`, only `sidebar_primary` works

## Versioning

This component follows [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** version: Incompatible API changes
- **MINOR** version: Backwards-compatible functionality additions
- **PATCH** version: Backwards-compatible bug fixes

Current version: **1.0.0** (initial release)
