# Data Model: Inner Layout System

**Feature**: Inner Layout System
**Date**: January 19, 2026
**Status**: Phase 1 - Design

## Overview

This document defines the entities, relationships, and structure for the inner layout system. Since this is a UI-only feature with no data persistence, the "data model" describes the component structure, their attributes, slots, and relationships.

## Component Entities

### 1. Inner Layout Container (`<c-page>`)

**Purpose**: Main container component that establishes the CSS Grid layout structure for nested content areas.

**Component Path**: `mvp/templates/cotton/inner/index.html`

**Attributes**:

| Attribute | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `toolbar_fixed` | boolean | `False` | No | Makes toolbar sticky to top when scrolling |
| `footer_fixed` | boolean | `False` | No | Makes footer sticky to bottom when scrolling |
| `sidebar_fixed` | boolean | `False` | No | Makes sidebar sticky when scrolling |
| `sidebar_breakpoint` | string | `"lg"` | No | Bootstrap breakpoint (`sm`, `md`, `lg`, `xl`, `xxl`) |
| `sidebar_toggleable` | boolean | `False` | No | Enables sidebar toggle functionality |
| `class` | string | `""` | No | Additional CSS classes for the wrapper |

**Note**: Boolean attributes use `:` prefix: `:toolbar_fixed="True"`

**Sub-Components** (using dot notation):

- `<c-page.toolbar>` - Top toolbar area
- `<c-page.footer>` - Bottom footer area
- `<c-page.sidebar>` - Right sidebar area
- `<c-page.toolbar.widget>` - Toolbar action widgets

**Default Slot**: Main content area - fills available space between toolbar and footer

**CSS Classes Generated**:

- `.page-layout` - Grid container
- `.sidebar-breakpoint-{breakpoint}` - Applied based on `sidebar_breakpoint` attribute
- `[data-page-layout]` - Data attribute for JavaScript targeting

**Component State**:

- Toggle state persisted in `sessionStorage` (when `sidebar_toggleable="True"`)
- JavaScript in `mvp/static/mvp/js/page-layout.js` manages toggle interactions

**Grid Structure**:

```
┌─────────────────────────────────┬────────────┐
│    Toolbar (header, optional)   │            │
├─────────────────────────────────┤  Sidebar   │
│                                 │  (aside,   │
│         Main Content            │  optional) │
│         (default slot)          │            │
│                                 │            │
├─────────────────────────────────┤            │
│   Footer (footer, optional)     │            │
└─────────────────────────────────┴────────────┘
```

**CSS Grid Implementation** (mirrors AdminLTE 4 app-wrapper pattern):

```css
.page-layout {
  display: grid;
  grid-template-columns: 1fr auto;           /* Main content expands, sidebar auto-width */
  grid-template-rows: min-content 1fr min-content;  /* Toolbar/footer min, content fills */
  grid-template-areas:
    "toolbar sidebar"   /* Row 1: Toolbar + Sidebar */
    "main sidebar"      /* Row 2: Main content + Sidebar */
    "footer sidebar";   /* Row 3: Footer + Sidebar */
  height: 100%;
  gap: 0;
}
```

**AdminLTE 4 Comparison** (outer app-wrapper for reference):

```scss
.app-wrapper {
  display: grid;
  grid-template-columns: auto 1fr;  // Sidebar first (left), main content second
  grid-template-rows: min-content 1fr min-content;  // Same row structure
  grid-template-areas:
    "app-sidebar app-header"
    "app-sidebar app-main"
    "app-sidebar app-footer";
  min-height: 100vh;
  gap: 0;
}
```

**Similarities:**

- Both use CSS Grid with named grid areas for positioning
- Both use `min-content 1fr min-content` rows (header/footer collapse, main fills)
- Both use auto-width columns for sidebar (collapses naturally to 0)
- Both use `gap: 0` for no spacing

**Differences:**

- Inner: Sidebar right (column 2), content first - better for detail panels
- Outer: Sidebar left (column 1), sidebar first - navigation pattern
- Inner: `height: 100%` fills container
- Outer: `min-height: 100vh` fills viewport

**Grid Areas**:

- `.toolbar` → `grid-area: toolbar`
- `.main` → `grid-area: main`
- `.sidebar` → `grid-area: sidebar` (spans all 3 rows)
- `.footer` → `grid-area: footer`

**Key Features**:

- Auto-width sidebar: When sidebar has `width: 0`, grid column collapses and main content expands automatically
- Min-content rows: Toolbar/footer rows shrink to 0 height when components not in DOM
- Content area: Takes remaining vertical space (1fr)

**Validation Rules**:

- `sidebar_breakpoint` must be Bootstrap breakpoint value (`sm`, `md`, `lg`, `xl`, `xxl`)
- Boolean attributes should use `:` prefix for Python booleans

**State Transitions**:

1. **Initial Load**: Sidebar visibility determined by `sidebar_breakpoint` and viewport width
2. **User Toggle**: If `sidebar_toggleable="True"` and toolbar has `collapsible`, button click toggles sidebar
3. **Viewport Resize**: Below breakpoint, sidebar hidden via CSS responsive classes
4. **Session Restore**: On page load, JavaScript restores toggle state from sessionStorage

---

## CSS Architecture

### Core Layout (page-layout.scss)

**Grid Setup**:

```scss
.page-layout {
  display: grid;
  grid-template-columns: 1fr auto;  // Content expands, sidebar auto
  grid-template-rows: min-content 1fr min-content;  // Dynamic row sizing
  grid-template-areas:
    "toolbar sidebar"
    "main sidebar"
    "footer sidebar";
  height: 100%;
  gap: 0;
}
```

**Sidebar Collapse**:

```scss
.sidebar.sidebar-collapse {
  min-width: 0;
  max-width: 0;
  width: 0;
  padding: 0;
  border: 0;
  opacity: 0;
  overflow: hidden;
  pointer-events: none;
  transition: min-width 0.3s ease, max-width 0.3s ease,
              width 0.3s ease, padding 0.3s ease,
              border-width 0.3s ease, opacity 0.3s ease;
}
```

**Sticky Positioning** (follows AdminLTE 4 pattern):

AdminLTE 4 uses wrapper classes `.fixed-header` and `.fixed-footer` to enable sticky positioning:

```scss
// AdminLTE 4 outer layout pattern
.fixed-header {
  .app-header {
    position: sticky;
    top: 0;
    z-index: $lte-zindex-fixed-header;
  }
}

.fixed-footer {
  .app-footer {
    position: sticky;
    bottom: 0;
    z-index: $lte-zindex-fixed-footer;
  }
}
```

Inner layout follows the same approach with attribute-driven classes:

```scss
// Applied when toolbar_fixed="True"
.page-toolbar-fixed {
  position: sticky;
  top: 0;
  z-index: 100;
}

.page-footer-fixed {
  position: sticky;
  bottom: 0;
  z-index: 100;
}

.page-sidebar-fixed {
  position: sticky;
  top: 0;
  max-height: 100vh;
  overflow-y: auto;
}
```

**Responsive Breakpoints** (example for `sidebar-breakpoint-lg`):

```scss
@media (max-width: 991px) {
  .page-layout.sidebar-breakpoint-lg .sidebar {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 1050;
    transform: translateX(100%);
    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.15);
    transition: transform 0.3s ease;

    &.sidebar-open {
      transform: translateX(0);
    }
  }

  .sidebar-overlay {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 1040;
    background-color: rgba(0, 0, 0, 0.5);

    &.active {
      display: block;
    }
  }
}
```

Breakpoint values:

- `sm`: 576px
- `md`: 768px
- `lg`: 992px (default)
- `xl`: 1200px
- `xxl`: 1400px

---

### 2. Inner Toolbar Sub-Component (`<c-page.toolbar>`)

**Purpose**: Top section for page-specific controls, filters, breadcrumbs, or action buttons.

**Component Path**: `mvp/templates/cotton/inner/toolbar.html`

**Attributes**:

| Attribute | Type | Default | Description |
| --- | --- | --- | --- |
| `collapsible` | boolean | `False` | Adds toggle button for sidebar collapse/expand |
| `class` | string | `""` | Additional CSS classes |

**Slots**:

| Slot | Description |
| --- | --- |
| Default | Main toolbar content |
| `end` | Content positioned at right end of toolbar |

**CSS Classes**:

- `.page-toolbar` - Base toolbar styling
- `.page-toolbar-fixed` - Applied when parent has `:toolbar_fixed="True"`
- `.page-layout-toggle-btn` - Toggle button class (when `collapsible` attribute present)

**Positioning**:

- Grid Row: 1 (first row)
- Grid Column: 1 / -1 (spans all columns)
- CSS Position: sticky (top: 0)
- z-index: 100

**Content Guidelines**:

- Toolbar content should be horizontally-oriented
- Common content: page title, filter dropdowns, action buttons, breadcrumbs
- Should not exceed reasonable height (recommend < 80px)

**Example Content**:

```html
<c-slot name="toolbar">
  <div class="d-flex justify-content-between align-items-center p-3">
    <h2>Data Table View</h2>
    <div>
      <button class="btn btn-primary">Export</button>
      <button class="btn btn-secondary">Filters</button>
    </div>
  </div>
</c-slot>
```

---

### 3. Inner Footer Area (`footer` slot)

**Purpose**: Bottom section for pagination, summary information, or action buttons.

**Slot Type**: Named slot within `page_layout` component

**CSS Classes**:

- `.page-footer` - Base footer styling
- Custom classes via `footer_class` attribute on parent component

**Positioning**:

- Grid Row: 3 (third row)
- Grid Column: 1 (first column only, sidebar spans rows 2-3)
- CSS Position: sticky (bottom: 0)
- z-index: 100

**Content Guidelines**:

- Footer content should be horizontally-oriented
- Common content: pagination controls, record counts, action buttons
- Should not exceed reasonable height (recommend < 60px)

**Example Content**:

```html
<c-slot name="footer">
  <div class="d-flex justify-content-between align-items-center p-3 border-top">
    <span>Showing 1-20 of 150 records</span>
    <nav aria-label="Page navigation">
      <ul class="pagination mb-0">
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
      </ul>
    </nav>
  </div>
</c-slot>
```

---

### 4. Secondary Sidebar Area (`sidebar` slot)

**Purpose**: Right-side panel for supplementary content, properties, filters, or navigation.

**Slot Type**: Named slot within `page_layout` component

**CSS Classes**:

- `.page-sidebar` - Base sidebar styling
- Visibility controlled by `sidebar_visible` attribute and responsive breakpoint

**Positioning**:

- Grid Row: 2 / 4 (spans content + footer rows)
- Grid Column: 2 (second column)
- CSS Position: relative
- Overflow: auto (independent scrolling)

**Responsive Behavior**:

- Hidden below `sidebar_breakpoint` (default: 992px / Bootstrap 'lg')
- Can be toggled by user if `sidebar_toggle="true"`
- Width controlled by `sidebar_width` attribute (default: 280px)

**Content Guidelines**:

- Sidebar content should be vertically-oriented
- Common content: properties panel, filters, navigation tree, legend
- Independent scroll from main content
- Should maintain usable width on various screen sizes

**Example Content**:

```html
<c-slot name="sidebar">
  <div class="p-3">
    <h5>Properties</h5>
    <dl>
      <dt>Status</dt>
      <dd>Active</dd>
      <dt>Last Updated</dt>
      <dd>2026-01-19</dd>
    </dl>
  </div>
</c-slot>
```

---

### 5. Main Content Area (default slot)

**Purpose**: Central content area that fills available space and contains primary page content.

**Slot Type**: Default slot within `page_layout` component

**Positioning**:

- Grid Row: 2 (second row, between toolbar and footer)
- Grid Column: 1 (first column)
- CSS Position: relative
- Overflow: auto (scrollable content)

**Layout Behavior**:

- Automatically fills space after accounting for toolbar, footer, and sidebar
- Independent scrolling from other areas
- Height adjusts based on viewport and toolbar/footer presence

**Content Guidelines**:

- Primary page content lives here
- Can contain any HTML structure: tables, cards, forms, etc.
- Should be the main focus of the page

**Example Content**:

```html
<c-mvp.page_layout>
  <!-- Default slot content -->
  <table class="table">
    <thead>
      <tr><th>Name</th><th>Email</th><th>Status</th></tr>
    </thead>
    <tbody>
      <tr><td>John Doe</td><td>john@example.com</td><td>Active</td></tr>
    </tbody>
  </table>
</c-mvp.page_layout>
```

---

## Component Relationships

```
┌─────────────────────────────────────────────────┐
│  Outer Layout (mvp/base.html)                   │
│  ┌───────────────────────────────────────────┐  │
│  │  app-sidebar (left)                       │  │
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │  app-header (top navbar)                  │  │
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │  app-main (main content area)             │  │
│  │                                           │  │
│  │  ╔═══════════════════════════════════════╗  │
│  │  ║  Inner Layout (page_layout)          ║  │
│  │  ║  ┌────────────────────────┬─────────┐ ║  │
│  │  ║  │  Toolbar (slot)        │         │ ║  │
│  │  ║  ├────────────────────────┤ Sidebar │ ║  │
│  │  ║  │  Main Content (slot)   │ (slot)  │ ║  │
│  │  ║  ├────────────────────────┤         │ ║  │
│  │  ║  │  Footer (slot)         │         │ ║  │
│  │  ║  └────────────────────────┴─────────┘ ║  │
│  │  ╚═══════════════════════════════════════╝  │
│  │                                           │  │
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │  app-footer (optional)                    │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Hierarchy**:

1. **Outer Layout (app-wrapper)** - Provided by MVP base template
2. **Inner Layout** - Optional, used within app-main content area
3. **Toolbar, Content, Footer, Sidebar** - Slots within inner layout

**Integration Points**:

- Inner layout lives inside `{% block content %}` of mvp/base.html
- Does not conflict with outer layout's header, sidebar, or footer
- Independent scrolling: outer layout may or may not scroll, inner layout always manages its own scroll
- No z-index conflicts: inner layout z-indexes (100) are below outer layout (1000+)

**Usage Pattern**:

```html
<!-- Page template extending mvp/base.html -->
{% extends "mvp/base.html" %}

{% block content %}
  <c-mvp.page_layout sidebar_width="320px" sidebar_toggle="true">
    <c-slot name="toolbar">
      <!-- Toolbar content -->
    </c-slot>

    <!-- Main content in default slot -->
    <div>Primary page content</div>

    <c-slot name="sidebar">
      <!-- Sidebar content -->
    </c-slot>

    <c-slot name="footer">
      <!-- Footer content -->
    </c-slot>
  </c-mvp.page_layout>
{% endblock %}
```

---

## CSS Architecture

### SCSS File Structure

**File**: `mvp/static/mvp/css/page-layout.scss`

**Dependencies**:

- Bootstrap 5.3 variables and mixins
- AdminLTE 4 color variables (if applicable)

**Key Selectors**:

```scss
.page-layout-wrapper {
  // Grid container
  display: grid;
  grid-template-rows: auto 1fr auto;
  grid-template-columns: 1fr auto;
  height: 100%;

  &.sidebar-collapsed {
    grid-template-columns: 1fr 0;  // sidebar width = 0
  }
}

.page-toolbar {
  // Sticky toolbar
  position: sticky;
  top: 0;
  z-index: 100;
}

.page-sidebar {
  // Right sidebar
  width: var(--page-sidebar-width, 280px);
  overflow-y: auto;

  @media (max-width: var(--page-sidebar-breakpoint, 992px)) {
    display: none;
  }
}

.page-footer {
  // Sticky footer
  position: sticky;
  bottom: 0;
  z-index: 100;
}
```

---

## JavaScript Module

**File**: `mvp/static/mvp/js/page-layout.js`

**Purpose**: Handle sidebar toggle functionality and state persistence

**Exports**: None (self-initializing module)

**Functions**:

```javascript
function initInnerLayoutToggles() {
  // Attach click handlers to toggle buttons
}

function toggleSidebar(wrapper) {
  // Toggle sidebar-collapsed class
  // Update sessionStorage
}

function restoreSidebarState() {
  // On page load, check sessionStorage
  // Restore collapsed state if needed
}
```

**Events**:

- `DOMContentLoaded` - Initialize toggles and restore state
- Click on `[data-toggle-sidebar]` - Toggle sidebar

**Storage Keys**:

- `innerSidebarCollapsed` (sessionStorage) - Boolean string ("true"/"false")

---

## Accessibility Considerations

### ARIA Attributes

**Sidebar Toggle Button**:

```html
<button
  class="page-sidebar-toggle"
  data-toggle-sidebar
  aria-label="Toggle sidebar"
  aria-expanded="true"
  aria-controls="page-sidebar">
  <i class="icon-toggle"></i>
</button>
```

**Sidebar Element**:

```html
<aside
  id="page-sidebar"
  class="page-sidebar"
  role="complementary"
  aria-label="Secondary sidebar">
  {{ sidebar }}
</aside>
```

**Toolbar**:

```html
<div class="page-toolbar" role="region" aria-label="Page toolbar">
  {{ toolbar }}
</div>
```

**Footer**:

```html
<div class="page-footer" role="contentinfo" aria-label="Page footer">
  {{ footer }}
</div>
```

### Keyboard Navigation

- Sidebar toggle button is keyboard-accessible (standard button element)
- All interactive elements within slots are keyboard-accessible
- Tab order flows naturally: toolbar → content → sidebar → footer

### Screen Reader Support

- Landmark roles identify major sections
- Toggle button announces expanded/collapsed state
- Sidebar visibility changes announced via aria-live (if implemented)

---

## Edge Cases & Validation

### Edge Case: No Sidebar Content

**Scenario**: `sidebar` slot is empty or not provided
**Behavior**: Sidebar area is not rendered, content area spans full width
**Implementation**: Conditional rendering in component template

### Edge Case: Very Tall Toolbar/Footer

**Scenario**: Toolbar or footer content exceeds reasonable height
**Behavior**: Content area shrinks but maintains minimum usable height
**Implementation**: Grid template with minmax() for content area

### Edge Case: Nested Inner Layouts

**Scenario**: Developer attempts to nest inner layouts within inner layouts
**Behavior**: Not recommended, may cause layout issues
**Documentation**: Explicitly document as unsupported pattern

### Edge Case: Narrow Viewport with Sidebar

**Scenario**: Viewport width < sidebar breakpoint, but sidebar is forced visible
**Behavior**: Media query hides sidebar regardless of `sidebar_visible` attribute
**Implementation**: CSS media query takes precedence

### Edge Case: No Content in Default Slot

**Scenario**: Main content area is empty
**Behavior**: Layout renders but content area is empty (valid state)
**Validation**: No validation required, empty content is acceptable

---

## Implementation Checklist

### Component Files

- [ ] `mvp/templates/cotton/mvp/page_layout.html` - Main container component
- [ ] `mvp/static/mvp/css/page-layout.scss` - CSS Grid layout styles
- [ ] `mvp/static/mvp/js/page-layout.js` - Toggle functionality (optional)

### Test Files

- [ ] `tests/components/test_page_layout.py` - Unit tests for component rendering
- [ ] `tests/integration/test_page_layout_integration.py` - Integration tests with outer layout
- [ ] `tests/e2e/test_page_layout_e2e.py` - Playwright E2E tests

### Documentation

- [ ] `docs/page-layout.md` - Component documentation
- [ ] Update quickstart.md with usage examples
- [ ] Update main README.md with inner layout section

### Configuration

- [ ] No MVP settings dictionary changes (template-driven only)
- [ ] Update agent context with new component information
