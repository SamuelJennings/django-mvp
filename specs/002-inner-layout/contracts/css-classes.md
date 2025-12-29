# CSS Classes Contract

**Feature**: 002-inner-layout  
**Version**: 1.0.0  
**Date**: 2025-12-23

## Contract Overview

This document defines the stable CSS class API for the inner layout component. These classes are part of the public API and breaking changes require a MAJOR version bump.

## Semantic Class Names

Per `STRUCTURE_AND_NAMING.md`, inner layout uses `.content-*` namespace to distinguish from outer layout (`.app-*`, `.site-*`, `.page-*`).

### Naming Convention

- **`.content-shell`**: Container for inner layout (analogous to `.app-shell` for outer)
- **`.content-sidebar-left`**: Primary (left) sidebar
- **`.content-sidebar-right`**: Secondary (right) sidebar
- **`.content-main`**: Main content area

## Public CSS Classes

### Layout Container

#### `.content-shell`

**Purpose**: Outer container for inner layout with flex display

**Behavior**:
- Display: `d-flex`
- Gap: Configurable via Bootstrap gap utilities (gap-0 to gap-5)
- CSS Variables: `--content-primary-width`, `--content-secondary-width`

**Structure**:
```html
<div class="content-shell d-flex gap-{0-5}">
  <!-- Sidebars and main content -->
</div>
```

**Customization**:
```css
.content-shell {
  /* Override gap */
  gap: 2rem !important;
  
  /* Override background */
  background: var(--bs-light);
}
```

**Contract**: This class MUST be present on the root element of the component.

---

### Primary Sidebar (Left)

#### `.content-sidebar-left`

**Purpose**: Primary (left) sidebar container

**Behavior**:
- Width: `var(--content-primary-width, 280px)`
- Responsive: Combined with `.offcanvas-{breakpoint} .offcanvas-start`
- Position: Left side of layout
- Flex: `flex-shrink: 0` (does not shrink)

**Responsive Classes** (Bootstrap managed):
- `.offcanvas-md`: Offcanvas below md (768px), normal at md+
- `.offcanvas-start`: Positions offcanvas on left

**State Classes**:
- `.collapsed`: Applied when sidebar collapsed to fit-content
- `.collapsible`: Applied when collapse feature enabled

**Structure**:
```html
<div class="offcanvas-md offcanvas-start content-sidebar-left collapsible"
     id="primarySidebar"
     tabindex="-1"
     role="complementary"
     aria-label="Primary sidebar">
  <div class="offcanvas-header d-md-none">...</div>
  <div class="offcanvas-body">
    <!-- Sidebar content -->
  </div>
</div>
```

**Customization**:
```css
.content-sidebar-left {
  /* Override width */
  --content-primary-width: 320px;
  
  /* Override background */
  background: var(--bs-light);
  
  /* Custom border */
  border-right: 2px solid var(--bs-border-color);
}
```

**Contract**: 
- Class MUST be present when `primary_sidebar` slot has content
- Class MUST NOT be present when `primary_sidebar` slot is empty
- Width MUST respect `--content-primary-width` CSS variable

---

### Secondary Sidebar (Right)

#### `.content-sidebar-right`

**Purpose**: Secondary (right) sidebar container

**Behavior**:
- Width: `var(--content-secondary-width, 250px)`
- Responsive: Combined with `.offcanvas-{breakpoint} .offcanvas-end`
- Position: Right side of layout
- Flex: `flex-shrink: 0` (does not shrink)

**Responsive Classes** (Bootstrap managed):
- `.offcanvas-md`: Offcanvas below md (768px), normal at md+
- `.offcanvas-end`: Positions offcanvas on right

**State Classes**:
- `.collapsed`: Applied when sidebar collapsed to fit-content
- `.collapsible`: Applied when collapse feature enabled

**Structure**:
```html
<div class="offcanvas-md offcanvas-end content-sidebar-right"
     id="secondarySidebar"
     tabindex="-1"
     role="complementary"
     aria-label="Secondary sidebar">
  <div class="offcanvas-header d-md-none">...</div>
  <div class="offcanvas-body">
    <!-- Sidebar content -->
  </div>
</div>
```

**Customization**:
```css
.content-sidebar-right {
  /* Override width */
  --content-secondary-width: 300px;
  
  /* Custom border */
  border-left: 2px solid var(--bs-border-color);
}
```

**Contract**: 
- Class MUST be present when `secondary_sidebar` slot has content
- Class MUST NOT be present when `secondary_sidebar` slot is empty
- Width MUST respect `--content-secondary-width` CSS variable

---

### Main Content

#### `.content-main`

**Purpose**: Main content area that expands to fill available width

**Behavior**:
- Flex: `flex-grow: 1` (expands to fill space)
- Overflow: `overflow-auto` (scrollable if needed)
- ARIA: `role="main"`
- Min-width: `0` (allows flex shrinking without overflow)

**Structure**:
```html
<div class="content-main flex-grow-1 overflow-auto"
     role="main"
     aria-label="Main content">
  <!-- Main page content -->
</div>
```

**Customization**:
```css
.content-main {
  /* Override padding */
  padding: 2rem;
  
  /* Override overflow */
  overflow-y: auto;
  overflow-x: hidden;
  
  /* Custom background */
  background: white;
}
```

**Contract**: This class MUST always be present (main content is required).

---

### Collapse Toggle Button

#### `.collapse-toggle`

**Purpose**: Toggle button for collapsing/expanding sidebars

**Behavior**:
- Visibility: Hidden at <breakpoint (`.d-none .d-{breakpoint}-block`)
- Position: Typically absolute positioned on sidebar edge
- State: Updates icon/direction based on collapsed state
- Disabled: In offcanvas mode

**Structure**:
```html
<button type="button" 
        class="collapse-toggle d-none d-md-block"
        data-target="primarySidebar"
        aria-label="Toggle primary sidebar collapse">
  <i class="bi bi-chevron-left"></i>
</button>
```

**Customization**:
```css
.collapse-toggle {
  /* Position on sidebar edge */
  position: absolute;
  right: -12px;
  top: 50%;
  transform: translateY(-50%);
  
  /* Style */
  background: var(--bs-primary);
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
}
```

**Contract**: 
- Class present only when collapse feature enabled for sidebar
- MUST be hidden at <breakpoint via responsive utilities
- MUST have `data-target` attribute pointing to sidebar ID

---

## State Classes

### `.collapsed`

**Applied To**: `.content-sidebar-left`, `.content-sidebar-right`

**Purpose**: Indicates sidebar is in collapsed state (width reduced to fit-content)

**Behavior**:
- Width: Auto/fit-content (typically ~60px for icons)
- Visibility: `.collapsed-only` content shown, `.expanded-only` hidden
- Transition: 0.3s ease
- Constraint: MUST NOT be applied when viewport <breakpoint

**CSS**:
```scss
.content-sidebar-left.collapsed,
.content-sidebar-right.collapsed {
  width: fit-content !important;
  min-width: 60px;
  overflow-x: visible !important;
  
  .expanded-only {
    display: none !important;
  }
  
  .collapsed-only {
    display: block !important;
  }
}
```

**Contract**:
- Applied/removed only via JavaScript
- MUST NOT coexist with offcanvas active state
- MUST persist in localStorage per sidebar

---

### `.collapsible`

**Applied To**: `.content-sidebar-left`, `.content-sidebar-right`

**Purpose**: Indicates sidebar has collapse feature enabled

**Behavior**:
- Adds collapse toggle button
- Enables collapse state management
- Disables collapse in offcanvas mode

**Contract**: Applied when component parameter `collapse_primary="true"` or `collapse_secondary="true"`

---

## Content Visibility Classes

These classes are used WITHIN sidebars to show/hide content based on collapsed state.

### `.collapsed-only`

**Purpose**: Content visible only when sidebar is collapsed

**Typical Use**: Icons, short labels

**Default State**: `display: none`

**When Sidebar Collapsed**: `display: block` (or appropriate display type)

**Example**:
```html
<div class="sidebar-item">
  <i class="bi bi-house collapsed-only"></i> <!-- Icon always visible -->
  <span class="expanded-only">Home</span>     <!-- Text only when expanded -->
</div>
```

**CSS**:
```scss
.collapsed-only {
  display: none;
}

.collapsed .collapsed-only {
  display: block !important;
}
```

---

### `.expanded-only`

**Purpose**: Content visible only when sidebar is expanded

**Typical Use**: Full text labels, descriptions, expanded navigation

**Default State**: `display: block` (or inherits from parent)

**When Sidebar Collapsed**: `display: none !important`

**CSS**:
```scss
.expanded-only {
  display: block;
}

.collapsed .expanded-only {
  display: none !important;
}
```

---

## Backwards Compatibility

### Deprecated Classes (Aliased)

The following classes are deprecated but aliased in `_backwards-compat.scss`:

| Deprecated | Current | Status |
|------------|---------|--------|
| `.inner-layout` | `.content-shell` | Aliased - DO NOT USE in new code |
| `.inner-primary` | `.content-sidebar-left` | Aliased - DO NOT USE in new code |
| `.inner-secondary` | `.content-sidebar-right` | Aliased - DO NOT USE in new code |
| `.inner-main` | `.content-main` | Aliased - DO NOT USE in new code |

**Migration**: Replace deprecated classes with current equivalents. Deprecated classes will be removed in v2.0.0.

---

## CSS Variables

### Public CSS Variables

These CSS variables are part of the public API and can be customized by consumers.

| Variable | Default | Applied To | Description |
|----------|---------|------------|-------------|
| `--content-primary-width` | `280px` | `.content-sidebar-left` | Width of primary sidebar at ≥breakpoint |
| `--content-secondary-width` | `250px` | `.content-sidebar-right` | Width of secondary sidebar at ≥breakpoint |

**Usage**:
```css
/* Global override */
:root {
  --content-primary-width: 320px;
  --content-secondary-width: 280px;
}

/* Per-layout override */
.my-custom-layout {
  --content-primary-width: 300px;
}
```

**Contract**: These variables MUST be respected by the component CSS.

---

## Responsive Utilities

The component uses Bootstrap 5's responsive utility classes:

| Class Pattern | Description | Example |
|---------------|-------------|---------|
| `.d-{breakpoint}-{display}` | Show/hide at breakpoint | `.d-none .d-md-block` |
| `.offcanvas-{breakpoint}` | Offcanvas below breakpoint | `.offcanvas-md` |
| `.gap-{0-5}` | Flex gap | `.gap-3` |

**Contract**: Component MUST work with standard Bootstrap responsive utilities.

---

## Testing Contract

### CSS Class Presence Tests

```python
def test_content_shell_present():
    """Root element must have .content-shell"""
    html = render_to_string('cotton/layouts/inner.html', {'slot': 'Content'})
    assert 'class="content-shell' in html

def test_sidebar_classes_with_content():
    """Sidebar classes present only when slots have content"""
    html = render_to_string('cotton/layouts/inner.html', {
        'slot': 'Main',
        'primary_sidebar': '<nav>Nav</nav>'
    })
    assert 'content-sidebar-left' in html
    assert 'content-sidebar-right' not in html

def test_sidebar_classes_empty():
    """Sidebar classes absent when slots empty"""
    html = render_to_string('cotton/layouts/inner.html', {
        'slot': 'Main',
        'primary_sidebar': '   '  # Whitespace
    })
    assert 'content-sidebar-left' not in html
```

### CSS Variable Tests

```python
def test_css_variables_applied():
    """CSS variables set from component parameters"""
    html = render_to_string('cotton/layouts/inner.html', {
        'slot': 'Main',
        'primary_width': '320px'
    })
    assert '--content-primary-width: 320px' in html
```

---

## Versioning

Changes to this contract follow Semantic Versioning:

**MAJOR** (Breaking):
- Removing public CSS classes
- Renaming public CSS classes
- Changing CSS variable names
- Removing deprecated classes

**MINOR** (Non-breaking):
- Adding new optional classes
- Adding new CSS variables
- Improving responsive behavior (as long as existing behavior maintained)

**PATCH** (Bug fixes):
- Fixing CSS specificity issues
- Fixing responsive utility application
- Fixing browser compatibility

Current version: **1.0.0** (initial release)
