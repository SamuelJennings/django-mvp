# Data Model: Inner Layout Component

**Feature**: 002-inner-layout  
**Date**: 2025-12-23  
**Phase**: 1 (Design)

## Overview

The inner layout component provides a flexible multi-column content layout system using Django-Cotton's slot-based architecture. This document defines the component structure, slot model, data attributes, CSS class contracts, and state machine.

## Component Structure

### HTML Template Structure

**File**: `mvp/templates/cotton/layouts/inner.html`

```django-html
<c-vars 
  primary_width="280px"
  secondary_width="250px"
  breakpoint="md"
  gap="0"
  collapse_primary="false"
  collapse_secondary="false"
  class
/>

{% load cotton %}

<div class="content-shell d-flex gap-{{ gap }} {{ class }}"
     style="
       --content-primary-width: {{ primary_width }};
       --content-secondary-width: {{ secondary_width }};
     "
     data-breakpoint="{{ breakpoint }}"
     {{ attrs }}>
  
  {# Primary Sidebar (Left) #}
  {% if primary_sidebar %}
  <div class="offcanvas-{{ breakpoint }} offcanvas-start content-sidebar-left {% if collapse_primary == 'true' %}collapsible{% endif %}"
       id="primarySidebar"
       tabindex="-1"
       role="complementary"
       aria-label="Primary sidebar">
    <div class="offcanvas-header d-{{ breakpoint }}-none">
      <h5 class="offcanvas-title" id="primarySidebarLabel">Primary Sidebar</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      {{ primary_sidebar }}
    </div>
    {% if collapse_primary == 'true' %}
    <button type="button" 
            class="collapse-toggle d-none d-{{ breakpoint }}-block"
            data-target="primarySidebar"
            aria-label="Toggle primary sidebar collapse">
      <i class="bi bi-chevron-left"></i>
    </button>
    {% endif %}
  </div>
  {% endif %}
  
  {# Main Content #}
  <div class="content-main flex-grow-1 overflow-auto"
       role="main"
       aria-label="Main content">
    {{ slot }}
  </div>
  
  {# Secondary Sidebar (Right) #}
  {% if secondary_sidebar %}
  <div class="offcanvas-{{ breakpoint }} offcanvas-end content-sidebar-right {% if collapse_secondary == 'true' %}collapsible{% endif %}"
       id="secondarySidebar"
       tabindex="-1"
       role="complementary"
       aria-label="Secondary sidebar">
    <div class="offcanvas-header d-{{ breakpoint }}-none">
      <h5 class="offcanvas-title" id="secondarySidebarLabel">Secondary Sidebar</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      {{ secondary_sidebar }}
    </div>
    {% if collapse_secondary == 'true' %}
    <button type="button" 
            class="collapse-toggle d-none d-{{ breakpoint }}-block"
            data-target="secondarySidebar"
            aria-label="Toggle secondary sidebar collapse">
      <i class="bi bi-chevron-right"></i>
    </button>
    {% endif %}
  </div>
  {% endif %}
  
</div>
```

### Slot Definitions

#### 1. Default Slot (Main Content)

- **Name**: `{{ slot }}` (unnamed/default)
- **Required**: Yes (always rendered)
- **Purpose**: Primary page content
- **Behavior**: Expands to fill available width when sidebars absent
- **ARIA**: `role="main"`

**Usage**:
```django-html
<c-layouts.inner>
  <h1>My Page Content</h1>
  <p>This goes into the default slot.</p>
</c-layouts.inner>
```

#### 2. Primary Sidebar Slot

- **Name**: `{{ primary_sidebar }}`
- **Required**: No (optional)
- **Purpose**: Left sidebar content (navigation, filters, etc.)
- **Behavior**: 
  - Not rendered if slot not declared in template
  - Positioned on left at ≥breakpoint
  - Becomes offcanvas (toggleable overlay) at <breakpoint
  - Can collapse to fit-content if `collapse_primary="true"` (only at ≥breakpoint)
- **ARIA**: `role="complementary"`
- **Default Width**: 280px

**Usage**:
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
  
  <!-- Main content -->
  <h1>Page Title</h1>
</c-layouts.inner>
```

#### 3. Secondary Sidebar Slot

- **Name**: `{{ secondary_sidebar }}`
- **Required**: No (optional)
- **Purpose**: Right sidebar content (metadata, related content, etc.)
- **Behavior**:
  - Not rendered if slot not declared in template
  - Positioned on right at ≥breakpoint
  - Becomes offcanvas (toggleable overlay) at <breakpoint
  - Can collapse to fit-content if `collapse_secondary="true"` (only at ≥breakpoint)
- **ARIA**: `role="complementary"`
- **Default Width**: 250px

**Usage**:
```django-html
<c-layouts.inner>
  <c-slot name="secondary_sidebar">
    <aside>
      <h3>Related Links</h3>
      <ul>...</ul>
    </aside>
  </c-slot>
  
  <!-- Main content -->
  <h1>Page Title</h1>
</c-layouts.inner>
```

## Data Attributes

### Component Configuration

Data attributes are specified via `<c-vars>` in the component definition. End users can override these when using the component.

| Attribute | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `primary_width` | CSS length | `280px` | Width of primary_sidebar at ≥breakpoint | `primary_width="320px"` |
| `secondary_width` | CSS length | `250px` | Width of secondary_sidebar at ≥breakpoint | `secondary_width="300px"` |
| `breakpoint` | Bootstrap breakpoint | `md` | When to switch to offcanvas mode | `breakpoint="lg"` |
| `gap` | CSS length/unitless | `0` | Spacing between layout columns (Bootstrap gap utility) | `gap="3"` |
| `collapse_primary` | Boolean string | `false` | Enable collapse toggle for primary_sidebar | `collapse_primary="true"` |
| `collapse_secondary` | Boolean string | `false` | Enable collapse toggle for secondary_sidebar | `collapse_secondary="true"` |
| `class` | CSS classes | `` | Additional classes for .content-shell | `class="my-layout"` |

### User Override Example

```django-html
<c-layouts.inner 
  primary_width="300px"
  breakpoint="lg"
  collapse_primary="true"
  gap="2">
  <!-- Content -->
</c-layouts.inner>
```

## CSS Variables

CSS variables are applied as inline styles on `.content-shell` to enable runtime configuration without rebuilding assets.

| Variable | Default | Applied To | Description |
|----------|---------|------------|-------------|
| `--content-primary-width` | `280px` | `.content-sidebar-left` | Width of primary sidebar |
| `--content-secondary-width` | `250px` | `.content-sidebar-right` | Width of secondary sidebar |

**SCSS Consumption**:
```scss
.content-sidebar-left {
  width: var(--content-primary-width, 280px);
}

.content-sidebar-right {
  width: var(--content-secondary-width, 250px);
}
```

## CSS Class Hierarchy

### Layout Container

- **`.content-shell`**: Outer flexbox container
  - Purpose: Contains all layout regions
  - Display: `d-flex`
  - Gap: Configurable via Bootstrap gap utilities (gap-0 to gap-5)
  - Allows custom classes via `class` attribute

### Sidebar Classes

#### Primary Sidebar (Left)

- **`.content-sidebar-left`**: Primary sidebar container
  - Width: `var(--content-primary-width, 280px)`
  - Responsive: `.offcanvas-{breakpoint} .offcanvas-start`
  - Optional: `.collapsible` (if collapse enabled)
  - State: `.collapsed` (when collapsed to fit-content)

#### Secondary Sidebar (Right)

- **`.content-sidebar-right`**: Secondary sidebar container
  - Width: `var(--content-secondary-width, 250px)`
  - Responsive: `.offcanvas-{breakpoint} .offcanvas-end`
  - Optional: `.collapsible` (if collapse enabled)
  - State: `.collapsed` (when collapsed to fit-content)

### Main Content

- **`.content-main`**: Main content container
  - Flex: `flex-grow-1` (expands to fill space)
  - Overflow: `overflow-auto` (scrollable if needed)
  - ARIA: `role="main"`

### Collapse Toggle

- **`.collapse-toggle`**: Toggle button for collapse state
  - Visibility: `d-none d-{breakpoint}-block` (hidden in offcanvas mode)
  - State: Disabled when viewport < breakpoint

### Content Visibility Classes

Used within sidebars to show/hide content based on collapsed state:

- **`.collapsed-only`**: Visible only when sidebar is collapsed (e.g., icons)
- **`.expanded-only`**: Visible only when sidebar is expanded (e.g., text labels)

## State Machine

### Sidebar States

Each sidebar can be in one of three mutually exclusive states:

```
┌─────────────────────────────────────────────────┐
│                 SIDEBAR STATE                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────┐    Viewport >= breakpoint         │
│  │  NORMAL  │ ◄──────────────────────────────┐  │
│  └──────────┘                                 │  │
│       │                                       │  │
│       │ collapse_* = true                     │  │
│       │ + collapse toggle clicked             │  │
│       ▼                                       │  │
│  ┌───────────┐                                │  │
│  │ COLLAPSED │                                │  │
│  └───────────┘                                │  │
│       │                                       │  │
│       │ Viewport < breakpoint                 │  │
│       ▼                                       │  │
│  ┌────────────┐                               │  │
│  │ OFFCANVAS  │───────────────────────────────┘  │
│  └────────────┘   Viewport >= breakpoint         │
│       │                                          │
│       │ (Offcanvas hidden by default)            │
│       │ User clicks toggle button                │
│       ▼                                          │
│  ┌────────────────┐                              │
│  │ OFFCANVAS OPEN │                              │
│  └────────────────┘                              │
│                                                  │
└─────────────────────────────────────────────────┘
```

### State Definitions

#### NORMAL State

- **When**: Viewport ≥ breakpoint AND sidebar not collapsed
- **Behavior**: 
  - Sidebar visible in layout with full width
  - Collapse toggle visible (if collapse enabled)
  - Offcanvas classes inactive (Bootstrap auto-handles)
- **CSS**: `.content-sidebar-left` or `.content-sidebar-right`
- **Width**: Full configured width (280px or 250px)

#### COLLAPSED State

- **When**: Viewport ≥ breakpoint AND collapse toggle clicked AND collapse enabled
- **Behavior**:
  - Sidebar visible but width reduced to fit-content
  - `.collapsed` class applied
  - `.collapsed-only` content visible
  - `.expanded-only` content hidden
- **CSS**: `.content-sidebar-left.collapsed` or `.content-sidebar-right.collapsed`
- **Width**: Auto/fit-content (typically ~60px for icons)
- **Transition**: 0.3s ease

#### OFFCANVAS State

- **When**: Viewport < breakpoint
- **Behavior**:
  - Sidebar hidden by default (off-screen)
  - Offcanvas toggle button visible
  - User can toggle to show overlay
  - Backdrop dims main content when open
  - **CONSTRAINT**: Collapse mode disabled (cannot be collapsed in offcanvas)
- **CSS**: `.content-sidebar-left.offcanvas-{breakpoint}.offcanvas-start`
- **Width**: Default offcanvas width (typically 320px)

#### OFFCANVAS OPEN State

- **When**: Viewport < breakpoint AND user clicks offcanvas toggle
- **Behavior**:
  - Sidebar slides in from left/right
  - Backdrop overlay visible
  - Close button in offcanvas header
  - Escape key closes
  - Focus trapped in offcanvas
- **Duration**: ~0.3s transition

### State Transitions

| From | To | Trigger | Constraint |
|------|----| --------|-----------|
| NORMAL | COLLAPSED | User clicks collapse toggle | `collapse_*="true"` required |
| COLLAPSED | NORMAL | User clicks collapse toggle again | None |
| NORMAL | OFFCANVAS | Viewport shrinks < breakpoint | Collapse state cleared |
| COLLAPSED | OFFCANVAS | Viewport shrinks < breakpoint | Collapse state cleared |
| OFFCANVAS | NORMAL | Viewport expands ≥ breakpoint | Returns to NORMAL (not COLLAPSED) |
| OFFCANVAS | OFFCANVAS OPEN | User clicks offcanvas toggle | None |
| OFFCANVAS OPEN | OFFCANVAS | User closes (button/escape/backdrop) | None |

### State Persistence

**Collapse State**:
- Stored in localStorage per sidebar (e.g., `innerLayout.primarySidebar.collapsed`)
- Restored on page load
- Cleared when entering offcanvas mode

**Offcanvas State**:
- NOT persisted (Bootstrap default behavior)
- Always starts closed

## Validation Rules

### Slot Declaration Handling

**Rule**: FR-010 - Do not render sidebar containers when slots are undeclared

**Implementation**:
```django-html
{% if sidebar_name %}
  <!-- Render sidebar -->
{% endif %}
```

**Django-Cotton Slot Behavior**: Slots are truthy when DECLARED in the template, regardless of content. To hide a sidebar, simply do not declare the slot.

**Test Cases**:
- Slot not declared → Not rendered ✅
- Slot declared with content → Rendered ✅

### Collapse Constraint

**Rule**: Sidebars MAY NOT collapse when in offcanvas mode

**Implementation**:
```javascript
toggleCollapse(sidebar) {
  if (this.isOffcanvasMode()) {
    console.warn('Cannot collapse sidebar in offcanvas mode');
    return false;
  }
  // Proceed with collapse
}
```

**Enforcement**:
- Collapse toggle button hidden at <breakpoint (`.d-none .d-{breakpoint}-block`)
- JavaScript prevents collapse in offcanvas mode
- Entering offcanvas mode clears collapsed state

### Responsive Breakpoint

**Rule**: Default breakpoint is `md` (768px)

**Bootstrap Breakpoints**:
- `sm`: 576px
- `md`: 768px ← Default
- `lg`: 992px
- `xl`: 1200px
- `xxl`: 1400px

**Usage**: `.offcanvas-md` means offcanvas below md, normal at md+

## Next Steps

With data model complete, proceed to:
1. **contracts/** - Define formal API contracts for component, CSS, and JavaScript
2. **quickstart.md** - Create developer quick-start guide with examples
3. **Update agent context** - Add inner layout patterns to Copilot instructions
