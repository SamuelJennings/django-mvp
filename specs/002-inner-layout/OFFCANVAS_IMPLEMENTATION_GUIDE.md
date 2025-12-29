# Bootstrap 5.3 Offcanvas Implementation Guide for Inner Layout

**Feature**: Inner Layout Component  
**Created**: December 23, 2025  
**Purpose**: Implementation guidance for integrating Bootstrap 5.3 offcanvas behavior with inner layout sidebars

---

## Table of Contents

1. [Bootstrap 5.3 Offcanvas API](#1-bootstrap-53-offcanvas-api)
2. [Responsive Patterns](#2-responsive-patterns)
3. [Integration with Existing Layout](#3-integration-with-existing-layout)
4. [State Management Constraints](#4-state-management-constraints)
5. [Accessibility Considerations](#5-accessibility-considerations)
6. [Django-Cotton Implementation Pattern](#6-django-cotton-implementation-pattern)
7. [Complete Code Examples](#7-complete-code-examples)

---

## 1. Bootstrap 5.3 Offcanvas API

### 1.1 Required HTML Structure

```html
<!-- Basic offcanvas structure -->
<div class="offcanvas offcanvas-start" 
     tabindex="-1" 
     id="offcanvasExample" 
     aria-labelledby="offcanvasExampleLabel">
  
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasExampleLabel">Title</h5>
    <button type="button" 
            class="btn-close" 
            data-bs-dismiss="offcanvas" 
            aria-label="Close"></button>
  </div>
  
  <div class="offcanvas-body">
    <!-- Your content here -->
  </div>
</div>
```

**Key Elements**:
- `.offcanvas` - Base class (hides content by default)
- `.offcanvas-start` - Placement modifier (left side, use `-end` for right)
- `tabindex="-1"` - Required for keyboard accessibility
- `id` - Unique identifier for targeting
- `aria-labelledby` - References the title element ID

### 1.2 Toggle Button Structure

```html
<!-- Button to trigger offcanvas -->
<button class="btn btn-primary" 
        type="button" 
        data-bs-toggle="offcanvas" 
        data-bs-target="#offcanvasExample" 
        aria-controls="offcanvasExample">
  Toggle Sidebar
</button>
```

**Key Attributes**:
- `data-bs-toggle="offcanvas"` - Activates Bootstrap offcanvas plugin
- `data-bs-target="#id"` - Points to the offcanvas element
- `aria-controls="id"` - Associates button with controlled element

### 1.3 Data Attributes for Configuration

```html
<div class="offcanvas offcanvas-start"
     data-bs-scroll="true"      <!-- Allow body scrolling while open -->
     data-bs-backdrop="true"    <!-- Show backdrop (default) -->
     data-bs-keyboard="true"    <!-- Close on Escape key (default) -->
     tabindex="-1">
  <!-- Content -->
</div>
```

**Configuration Options**:
- `data-bs-scroll="true"` - Enable body scrolling (default: `false`)
- `data-bs-backdrop="false"` - Disable backdrop (default: `true`)
- `data-bs-backdrop="static"` - Static backdrop (won't close on click)
- `data-bs-keyboard="false"` - Disable Escape key to close (default: `true`)

### 1.4 JavaScript API

```javascript
// Get or create offcanvas instance
const offcanvasEl = document.getElementById('myOffcanvas');
const offcanvas = new bootstrap.Offcanvas(offcanvasEl);

// Methods
offcanvas.show();      // Show the offcanvas
offcanvas.hide();      // Hide the offcanvas
offcanvas.toggle();    // Toggle visibility

// Static methods
bootstrap.Offcanvas.getInstance(offcanvasEl);           // Get existing instance
bootstrap.Offcanvas.getOrCreateInstance(offcanvasEl);   // Get or create instance
```

### 1.5 Events

```javascript
const offcanvasEl = document.getElementById('myOffcanvas');

// Event listeners
offcanvasEl.addEventListener('show.bs.offcanvas', function (event) {
  console.log('Offcanvas is about to show');
  // event.preventDefault(); // Can prevent showing
});

offcanvasEl.addEventListener('shown.bs.offcanvas', function (event) {
  console.log('Offcanvas is now visible (transition complete)');
});

offcanvasEl.addEventListener('hide.bs.offcanvas', function (event) {
  console.log('Offcanvas is about to hide');
  // event.preventDefault(); // Can prevent hiding
});

offcanvasEl.addEventListener('hidden.bs.offcanvas', function (event) {
  console.log('Offcanvas is now hidden (transition complete)');
});

offcanvasEl.addEventListener('hidePrevented.bs.offcanvas', function (event) {
  console.log('Hide was prevented (static backdrop or keyboard disabled)');
});
```

**Event Timing**:
- `show.bs.offcanvas` - Fires immediately when `show()` is called
- `shown.bs.offcanvas` - Fires after transition completes (fully visible)
- `hide.bs.offcanvas` - Fires immediately when `hide()` is called
- `hidden.bs.offcanvas` - Fires after transition completes (fully hidden)
- `hidePrevented.bs.offcanvas` - Fires when hide is prevented (static backdrop clicked)

### 1.6 Backdrop and Scroll Locking

**Default Behavior**:
- Backdrop is shown (dark overlay)
- Body scroll is locked
- Click on backdrop closes offcanvas
- Escape key closes offcanvas

**Customization**:
```html
<!-- Allow body scrolling, no backdrop -->
<div class="offcanvas offcanvas-start"
     data-bs-scroll="true"
     data-bs-backdrop="false">
  <!-- Content -->
</div>

<!-- Static backdrop (won't close on click outside) -->
<div class="offcanvas offcanvas-start"
     data-bs-backdrop="static">
  <!-- Content -->
</div>
```

---

## 2. Responsive Patterns

### 2.1 Responsive Offcanvas Classes (Bootstrap 5.2+)

Bootstrap 5.2 introduced responsive offcanvas classes that automatically switch between offcanvas and static sidebar based on breakpoint:

```html
<!-- Offcanvas below lg (992px), static sidebar above -->
<div class="offcanvas-lg offcanvas-start" tabindex="-1" id="responsiveSidebar">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title">Sidebar</h5>
    <button type="button" 
            class="btn-close" 
            data-bs-dismiss="offcanvas" 
            data-bs-target="#responsiveSidebar" 
            aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <!-- Sidebar content -->
  </div>
</div>

<!-- Toggle button (only visible below lg) -->
<button class="btn btn-primary d-lg-none" 
        type="button" 
        data-bs-toggle="offcanvas" 
        data-bs-target="#responsiveSidebar">
  Toggle Sidebar
</button>
```

**Available Classes**:
- `.offcanvas` - Always offcanvas (all breakpoints)
- `.offcanvas-sm` - Offcanvas below 576px
- `.offcanvas-md` - Offcanvas below 768px
- `.offcanvas-lg` - Offcanvas below 992px
- `.offcanvas-xl` - Offcanvas below 1200px
- `.offcanvas-xxl` - Offcanvas below 1400px

### 2.2 CSS Media Query Strategy

When using responsive offcanvas classes, Bootstrap automatically handles the transition:

```scss
// Bootstrap's implementation (for reference)
.offcanvas-lg {
  @media (max-width: 991.98px) {
    // Offcanvas styles (positioned off-screen)
    position: fixed;
    visibility: hidden;
    transition: transform 0.3s ease-in-out;
  }
  
  @media (min-width: 992px) {
    // Static sidebar styles (in-flow)
    position: static;
    visibility: visible;
    transform: none;
    // Reset offcanvas-specific properties
  }
}
```

### 2.3 Toggle Button Visibility Pattern

```html
<!-- Example: Sidebar shows at desktop (≥992px), offcanvas at mobile (<992px) -->

<!-- Toggle button: Only show on mobile -->
<button class="d-lg-none" 
        data-bs-toggle="offcanvas" 
        data-bs-target="#sidebar">
  <i class="bi bi-list"></i>
</button>

<!-- Sidebar with responsive offcanvas -->
<div class="offcanvas-lg offcanvas-start" id="sidebar">
  <div class="offcanvas-header">
    <!-- Close button: Only show on mobile (when offcanvas) -->
    <button type="button" 
            class="btn-close d-lg-none" 
            data-bs-dismiss="offcanvas"></button>
  </div>
  <div class="offcanvas-body">
    <!-- Sidebar content always visible -->
  </div>
</div>
```

**Visibility Classes**:
- `.d-{breakpoint}-none` - Hide at breakpoint and above
- `.d-{breakpoint}-block` - Show at breakpoint and above

### 2.4 Example: Desktop Static, Mobile Offcanvas

```html
<!-- Complete responsive sidebar example -->
<div class="container-fluid">
  <div class="row">
    
    <!-- Toggle button for mobile -->
    <div class="col-12 d-md-none">
      <button class="btn btn-primary" 
              type="button" 
              data-bs-toggle="offcanvas" 
              data-bs-target="#responsiveSidebar">
        <i class="bi bi-list"></i> Menu
      </button>
    </div>
    
    <!-- Sidebar: Offcanvas on mobile, static on desktop -->
    <div class="col-md-3">
      <div class="offcanvas-md offcanvas-start" 
           tabindex="-1" 
           id="responsiveSidebar">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title">Navigation</h5>
          <button type="button" 
                  class="btn-close" 
                  data-bs-dismiss="offcanvas" 
                  data-bs-target="#responsiveSidebar"></button>
        </div>
        <div class="offcanvas-body">
          <nav>
            <ul class="nav flex-column">
              <li class="nav-item"><a class="nav-link" href="#">Link 1</a></li>
              <li class="nav-item"><a class="nav-link" href="#">Link 2</a></li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
    
    <!-- Main content -->
    <div class="col-md-9">
      <h1>Main Content</h1>
    </div>
    
  </div>
</div>
```

---

## 3. Integration with Existing Layout

### 3.1 Wrapping Existing Sidebar in Offcanvas

Based on the existing `.content-sidebar-left` and `.content-sidebar-right` structure:

```html
<!-- Primary (left) sidebar - responsive offcanvas -->
<div class="offcanvas-md offcanvas-start content-sidebar-left" 
     tabindex="-1" 
     id="primarySidebar"
     aria-labelledby="primarySidebarLabel">
  
  <div class="offcanvas-header d-md-none">
    <h5 class="offcanvas-title" id="primarySidebarLabel">Primary Sidebar</h5>
    <button type="button" 
            class="btn-close" 
            data-bs-dismiss="offcanvas" 
            aria-label="Close"></button>
  </div>
  
  <div class="offcanvas-body">
    <!-- Existing sidebar content -->
    <c-sidebar.index>
      {{ primary_sidebar }}
    </c-sidebar.index>
  </div>
</div>

<!-- Secondary (right) sidebar - responsive offcanvas -->
<div class="offcanvas-md offcanvas-end content-sidebar-right" 
     tabindex="-1" 
     id="secondarySidebar"
     aria-labelledby="secondarySidebarLabel">
  
  <div class="offcanvas-header d-md-none">
    <h5 class="offcanvas-title" id="secondarySidebarLabel">Secondary Sidebar</h5>
    <button type="button" 
            class="btn-close" 
            data-bs-dismiss="offcanvas" 
            aria-label="Close"></button>
  </div>
  
  <div class="offcanvas-body">
    <!-- Existing sidebar content -->
    <c-sidebar.index>
      {{ secondary_sidebar }}
    </c-sidebar.index>
  </div>
</div>
```

### 3.2 Toggle Button Placement

```html
<!-- Toggle buttons in page header/toolbar -->
<div class="page-header">
  <div class="d-flex align-items-center gap-2">
    
    <!-- Primary sidebar toggle (mobile only) -->
    <button class="btn btn-outline-secondary d-md-none" 
            type="button"
            data-bs-toggle="offcanvas" 
            data-bs-target="#primarySidebar"
            aria-controls="primarySidebar"
            aria-label="Toggle primary sidebar">
      <i class="bi bi-layout-sidebar"></i>
    </button>
    
    <h1 class="mb-0">Page Title</h1>
    
    <!-- Secondary sidebar toggle (mobile only) -->
    <button class="btn btn-outline-secondary d-md-none ms-auto" 
            type="button"
            data-bs-toggle="offcanvas" 
            data-bs-target="#secondarySidebar"
            aria-controls="secondarySidebar"
            aria-label="Toggle secondary sidebar">
      <i class="bi bi-info-circle"></i>
    </button>
    
  </div>
</div>
```

### 3.3 Preserving Sidebar Content and Scroll State

**Scroll State Preservation**:
```javascript
// Preserve scroll position when transitioning between modes
document.addEventListener('DOMContentLoaded', function() {
  const sidebars = document.querySelectorAll('.offcanvas-body');
  
  sidebars.forEach(sidebar => {
    let savedScrollTop = 0;
    
    sidebar.closest('.offcanvas').addEventListener('hide.bs.offcanvas', function() {
      // Save scroll position before hiding
      savedScrollTop = sidebar.scrollTop;
    });
    
    sidebar.closest('.offcanvas').addEventListener('shown.bs.offcanvas', function() {
      // Restore scroll position after showing
      sidebar.scrollTop = savedScrollTop;
    });
  });
});
```

**Content Preservation**:
- Content is preserved automatically (no unmount/remount)
- CSS transforms only affect positioning, not DOM structure
- Component state (collapsed menus, etc.) remains intact

### 3.4 CSS Integration

```scss
// Enhance existing sidebar styles for offcanvas compatibility
.content-sidebar-left,
.content-sidebar-right {
  // Existing sidebar styles...
  
  // Add offcanvas-specific adjustments
  &.offcanvas {
    // Ensure proper z-index for offcanvas
    z-index: $zindex-offcanvas;
    
    // Match existing sidebar width when shown
    --bs-offcanvas-width: var(--sidebar-width, 280px);
  }
  
  // When acting as static sidebar (above breakpoint)
  &.offcanvas-md {
    @media (min-width: 768px) {
      // Maintain existing sidebar styles
      position: static;
      width: var(--sidebar-width, 280px);
      transform: none;
      
      // Hide offcanvas-specific elements
      .offcanvas-header {
        display: none;
      }
    }
  }
  
  // Offcanvas body should not add padding in static mode
  .offcanvas-body {
    @media (min-width: 768px) {
      padding: 0; // Remove offcanvas padding for static sidebar
    }
  }
}
```

---

## 4. State Management Constraints

### 4.1 Three Distinct States

```
State 1: NORMAL (In-flow, expanded)
├─ Sidebar is visible in page layout
├─ Takes up width in flexbox/grid
├─ Can be collapsed (width reduction)
└─ Above breakpoint threshold

State 2: COLLAPSED (In-flow, minimized)
├─ Sidebar is visible but narrow
├─ Shows only icons, hides text
├─ Still takes up minimal width
├─ Above breakpoint threshold
└─ CONSTRAINT: Not available in offcanvas mode

State 3: OFFCANVAS (Off-canvas, toggled)
├─ Sidebar is hidden off-screen
├─ Does not take up layout width
├─ Slides in when toggled
├─ Below breakpoint threshold
└─ CONSTRAINT: Cannot be collapsed
```

### 4.2 State Transition Rules

```javascript
// State management for inner layout sidebar
class SidebarStateManager {
  constructor(sidebarElement) {
    this.sidebar = sidebarElement;
    this.breakpoint = 768; // md breakpoint
    this.isCollapsed = false;
    
    this.checkMode();
    window.addEventListener('resize', () => this.checkMode());
  }
  
  checkMode() {
    const isOffcanvasMode = window.innerWidth < this.breakpoint;
    
    if (isOffcanvasMode) {
      // Entering offcanvas mode: disable collapse
      this.disableCollapse();
      this.sidebar.classList.remove('collapsed');
    } else {
      // Entering normal mode: enable collapse
      this.enableCollapse();
      this.restoreCollapseState();
    }
  }
  
  disableCollapse() {
    // Hide collapse toggle button
    const toggleBtn = this.sidebar.querySelector('.sidebar-toggle');
    if (toggleBtn) {
      toggleBtn.style.display = 'none';
    }
  }
  
  enableCollapse() {
    // Show collapse toggle button
    const toggleBtn = this.sidebar.querySelector('.sidebar-toggle');
    if (toggleBtn) {
      toggleBtn.style.display = '';
    }
  }
  
  restoreCollapseState() {
    // Restore collapse state from localStorage
    const savedState = localStorage.getItem('sidebar-collapsed');
    if (savedState === 'true') {
      this.sidebar.classList.add('collapsed');
    }
  }
}
```

### 4.3 Toggle Button Visibility Rules

```html
<!-- Toggle button visibility matrix -->

<!-- Offcanvas toggle: Only show below breakpoint -->
<button class="d-md-none offcanvas-toggle" 
        data-bs-toggle="offcanvas" 
        data-bs-target="#sidebar">
  Open Sidebar
</button>

<!-- Collapse toggle: Only show above breakpoint AND when sidebar is collapsible -->
<button class="d-none d-md-inline-flex collapse-toggle" 
        data-action="toggle-collapse">
  <i class="bi bi-chevron-left"></i>
</button>
```

**Visibility Matrix**:
```
Viewport     | Offcanvas Toggle | Collapse Toggle
-------------|------------------|----------------
< md (768px) | Visible          | Hidden
≥ md (768px) | Hidden           | Visible (if collapsible enabled)
```

### 4.4 Constraint Enforcement

```javascript
// Enforce constraints: no collapse in offcanvas mode
document.addEventListener('DOMContentLoaded', function() {
  const sidebars = document.querySelectorAll('.content-sidebar-left, .content-sidebar-right');
  
  sidebars.forEach(sidebar => {
    const offcanvasInstance = bootstrap.Offcanvas.getInstance(sidebar);
    const collapseToggle = sidebar.querySelector('.collapse-toggle');
    
    // Prevent collapse when offcanvas is shown
    sidebar.addEventListener('show.bs.offcanvas', function() {
      sidebar.classList.remove('collapsed');
      if (collapseToggle) {
        collapseToggle.disabled = true;
      }
    });
    
    // Re-enable collapse when offcanvas is hidden (and above breakpoint)
    sidebar.addEventListener('hidden.bs.offcanvas', function() {
      if (window.innerWidth >= 768) {
        if (collapseToggle) {
          collapseToggle.disabled = false;
        }
      }
    });
  });
});
```

---

## 5. Accessibility Considerations

### 5.1 ARIA Roles and Properties

```html
<div class="offcanvas offcanvas-start" 
     tabindex="-1"                                  <!-- Required: Makes offcanvas focusable -->
     id="sidebar"
     role="dialog"                                   <!-- Bootstrap adds automatically -->
     aria-modal="true"                              <!-- Bootstrap adds when shown -->
     aria-labelledby="sidebarTitle"                 <!-- Required: References title -->
     aria-describedby="sidebarDesc">               <!-- Optional: Additional description -->
  
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="sidebarTitle">
      Navigation
    </h5>
    <button type="button" 
            class="btn-close" 
            data-bs-dismiss="offcanvas" 
            aria-label="Close navigation">         <!-- Required: Descriptive label -->
    </button>
  </div>
  
  <div class="offcanvas-body" id="sidebarDesc">
    <nav aria-label="Primary navigation">          <!-- Landmark for screen readers -->
      <!-- Navigation content -->
    </nav>
  </div>
</div>

<!-- Toggle button -->
<button type="button"
        data-bs-toggle="offcanvas" 
        data-bs-target="#sidebar"
        aria-controls="sidebar"                     <!-- Associates with controlled element -->
        aria-expanded="false"                      <!-- Bootstrap updates automatically -->
        aria-label="Open navigation menu">          <!-- Required: Descriptive label -->
  <i class="bi bi-list" aria-hidden="true"></i>   <!-- Hide icon from screen readers -->
</button>
```

**Key ARIA Attributes**:
- `role="dialog"` - Identifies offcanvas as dialog (added by Bootstrap)
- `aria-modal="true"` - Indicates modal behavior (added when shown)
- `aria-labelledby` - Points to element that labels the offcanvas
- `aria-describedby` - Points to element that describes the offcanvas
- `aria-controls` - Associates toggle button with offcanvas
- `aria-expanded` - Indicates toggle state (managed by Bootstrap)

### 5.2 Focus Management

Bootstrap automatically handles focus management:

```javascript
// Bootstrap's built-in focus management (for reference)
const offcanvasEl = document.getElementById('sidebar');

offcanvasEl.addEventListener('shown.bs.offcanvas', function () {
  // Bootstrap automatically:
  // 1. Saves reference to previously focused element
  // 2. Moves focus to offcanvas container
  // 3. Traps focus within offcanvas (Tab cycles within)
});

offcanvasEl.addEventListener('hidden.bs.offcanvas', function () {
  // Bootstrap automatically:
  // 1. Returns focus to previously focused element (usually toggle button)
  // 2. Releases focus trap
});
```

**Custom Focus Enhancement**:
```javascript
// Optional: Move focus to first interactive element
offcanvasEl.addEventListener('shown.bs.offcanvas', function () {
  const firstFocusable = this.querySelector('a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])');
  if (firstFocusable) {
    setTimeout(() => firstFocusable.focus(), 100);
  }
});
```

### 5.3 Keyboard Navigation

Bootstrap handles keyboard events automatically:

- **Escape** - Closes offcanvas (if `data-bs-keyboard="true"`, which is default)
- **Tab** - Cycles through focusable elements within offcanvas
- **Shift+Tab** - Cycles backward through focusable elements

**Testing Keyboard Navigation**:
```javascript
// Ensure all interactive elements are keyboard accessible
const offcanvasBody = document.querySelector('.offcanvas-body');

// Test: Can user reach all links/buttons with Tab key?
// Test: Does Tab wrap to beginning when reaching end?
// Test: Does Escape close the offcanvas?
// Test: Does focus return to toggle button after closing?
```

### 5.4 Screen Reader Considerations

```html
<!-- Announce offcanvas state changes -->
<div class="offcanvas offcanvas-start" 
     tabindex="-1" 
     id="sidebar"
     aria-live="polite"                            <!-- Optional: Announce changes -->
     aria-labelledby="sidebarTitle">
  
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="sidebarTitle">
      Navigation Menu
    </h5>
    <button type="button" 
            class="btn-close" 
            data-bs-dismiss="offcanvas" 
            aria-label="Close navigation menu">
      <span aria-hidden="true">&times;</span>      <!-- Hide visual × from screen readers -->
    </button>
  </div>
  
  <div class="offcanvas-body">
    <!-- Use semantic HTML -->
    <nav aria-label="Primary navigation">
      <ul>
        <li><a href="#">Link with descriptive text</a></li>
      </ul>
    </nav>
  </div>
</div>

<!-- Visually hidden text for context -->
<button data-bs-toggle="offcanvas" data-bs-target="#sidebar">
  <i class="bi bi-list" aria-hidden="true"></i>
  <span class="visually-hidden">Open navigation menu</span>
</button>
```

### 5.5 Accessibility Testing Checklist

- [ ] Toggle button has descriptive `aria-label`
- [ ] Offcanvas has `aria-labelledby` referencing title
- [ ] Close button has descriptive `aria-label`
- [ ] Icons are hidden from screen readers (`aria-hidden="true"`)
- [ ] Focus moves to offcanvas when opened
- [ ] Focus is trapped within offcanvas (Tab doesn't leave)
- [ ] Focus returns to toggle button when closed
- [ ] Escape key closes offcanvas
- [ ] Screen reader announces offcanvas state
- [ ] All interactive elements are keyboard accessible
- [ ] Sufficient color contrast for all text
- [ ] Touch targets are at least 44×44px

---

## 6. Django-Cotton Implementation Pattern

### 6.1 Inner Layout Component Structure

```django-html
<!-- cotton/inner_layout/index.html -->
<c-vars 
  primary_width="280px"
  secondary_width="250px" 
  breakpoint="md"
  primary_collapsible="true"
  secondary_collapsible="false"
  class
/>

<div class="inner-layout d-flex" {{ attrs }}>
  
  {% if primary_sidebar %}
  <!-- Primary Sidebar (Left) with Offcanvas -->
  <div class="offcanvas-{{ breakpoint }} offcanvas-start content-sidebar-left" 
       tabindex="-1" 
       id="primarySidebar"
       aria-labelledby="primarySidebarLabel"
       style="--sidebar-width: {{ primary_width }};">
    
    <div class="offcanvas-header d-{{ breakpoint }}-none">
      <h5 class="offcanvas-title" id="primarySidebarLabel">Primary Sidebar</h5>
      <button type="button" 
              class="btn-close" 
              data-bs-dismiss="offcanvas" 
              aria-label="Close"></button>
    </div>
    
    <div class="offcanvas-body p-0">
      <div class="inner-sidebar-content h-100" data-collapsible="{{ primary_collapsible }}">
        {{ primary_sidebar }}
      </div>
    </div>
  </div>
  {% endif %}
  
  <!-- Main Content Area -->
  <div class="inner-main flex-grow-1 overflow-auto">
    {{ slot }}
  </div>
  
  {% if secondary_sidebar %}
  <!-- Secondary Sidebar (Right) with Offcanvas -->
  <div class="offcanvas-{{ breakpoint }} offcanvas-end content-sidebar-right" 
       tabindex="-1" 
       id="secondarySidebar"
       aria-labelledby="secondarySidebarLabel"
       style="--sidebar-width: {{ secondary_width }};">
    
    <div class="offcanvas-header d-{{ breakpoint }}-none">
      <h5 class="offcanvas-title" id="secondarySidebarLabel">Secondary Sidebar</h5>
      <button type="button" 
              class="btn-close" 
              data-bs-dismiss="offcanvas" 
              aria-label="Close"></button>
    </div>
    
    <div class="offcanvas-body p-0">
      <div class="inner-sidebar-content h-100" data-collapsible="{{ secondary_collapsible }}">
        {{ secondary_sidebar }}
      </div>
    </div>
  </div>
  {% endif %}
  
</div>
```

### 6.2 Toggle Buttons Component

```django-html
<!-- cotton/inner_layout_toggles/index.html -->
<c-vars breakpoint="md" />

<div class="inner-layout-toggles d-flex gap-2">
  
  {% if has_primary_sidebar %}
  <!-- Primary Sidebar Toggle (Mobile Only) -->
  <button class="btn btn-outline-secondary d-{{ breakpoint }}-none" 
          type="button"
          data-bs-toggle="offcanvas" 
          data-bs-target="#primarySidebar"
          aria-controls="primarySidebar"
          aria-label="Toggle primary sidebar">
    <i class="bi bi-layout-sidebar"></i>
  </button>
  {% endif %}
  
  {{ slot }}
  
  {% if has_secondary_sidebar %}
  <!-- Secondary Sidebar Toggle (Mobile Only) -->
  <button class="btn btn-outline-secondary d-{{ breakpoint }}-none" 
          type="button"
          data-bs-toggle="offcanvas" 
          data-bs-target="#secondarySidebar"
          aria-controls="secondarySidebar"
          aria-label="Toggle secondary sidebar">
    <i class="bi bi-info-circle"></i>
  </button>
  {% endif %}
  
</div>
```

### 6.3 Usage Example

```django-html
<!-- example/templates/dashboard.html -->
{% extends "base.html" %}

{% block content %}
<div class="page-wrapper">
  
  <!-- Page Header with Toggle Buttons -->
  <div class="page-header d-flex align-items-center p-3">
    <c-inner_layout_toggles breakpoint="md" />
    <h1 class="mb-0 ms-2">Dashboard</h1>
  </div>
  
  <!-- Inner Layout with Sidebars -->
  <c-inner_layout 
    primary_width="280px" 
    secondary_width="300px" 
    breakpoint="md"
    primary_collapsible="true">
    
    <c-slot name="primary_sidebar">
      <c-sidebar.index collapsible="true">
        <c-sidebar.menu_section title="Navigation">
          <c-sidebar.menu_item href="/dashboard" icon="bi-house">Dashboard</c-sidebar.menu_item>
          <c-sidebar.menu_item href="/reports" icon="bi-graph-up">Reports</c-sidebar.menu_item>
        </c-sidebar.menu_section>
      </c-sidebar.index>
    </c-slot>
    
    <c-slot name="secondary_sidebar">
      <div class="info-panel p-3">
        <h5>Quick Info</h5>
        <p>Additional context here</p>
      </div>
    </c-slot>
    
    <!-- Main content in default slot -->
    <div class="content-area p-4">
      <h2>Dashboard Content</h2>
      <p>Your main content here</p>
    </div>
    
  </c-inner_layout>
  
</div>
{% endblock %}
```

### 6.4 SCSS Integration

```scss
// _inner-layout.scss

.inner-layout {
  min-height: 0;
  height: 100%;
  
  // Sidebars
  .content-sidebar-left,
  .content-sidebar-right {
    flex-shrink: 0;
    overflow-y: auto;
    
    // When acting as offcanvas
    &.offcanvas {
      --bs-offcanvas-width: var(--sidebar-width, 280px);
    }
    
    // Responsive breakpoint handling
    @each $breakpoint, $min-width in $grid-breakpoints {
      &.offcanvas-#{$breakpoint} {
        @media (min-width: $min-width) {
          // Static sidebar styles (above breakpoint)
          position: static;
          width: var(--sidebar-width, 280px);
          transform: none;
          visibility: visible;
          
          // Hide offcanvas-specific elements
          .offcanvas-header {
            display: none;
          }
          
          // Remove offcanvas body padding
          .offcanvas-body {
            padding: 0;
          }
        }
        
        @media (max-width: ($min-width - 0.02px)) {
          // Offcanvas styles (below breakpoint)
          // (Bootstrap handles this automatically)
          
          // Ensure collapse is disabled
          .inner-sidebar-content.collapsed {
            width: auto;
            min-width: auto;
          }
        }
      }
    }
  }
  
  // Main content area
  .inner-main {
    min-width: 0;
    flex: 1 1 auto;
  }
}

// Collapse toggle visibility
.inner-sidebar-content[data-collapsible="true"] {
  .collapse-toggle {
    @media (max-width: 767.98px) {
      display: none !important;
    }
  }
}
```

### 6.5 JavaScript Integration

```javascript
// inner_layout.js

(function () {
  'use strict';
  
  class InnerLayoutManager {
    constructor() {
      this.init();
    }
    
    init() {
      this.setupOffcanvasHandlers();
      this.setupCollapseHandlers();
      this.handleBreakpointChanges();
      
      window.addEventListener('resize', () => this.handleBreakpointChanges());
    }
    
    setupOffcanvasHandlers() {
      const offcanvasElements = document.querySelectorAll('.content-sidebar-left, .content-sidebar-right');
      
      offcanvasElements.forEach(sidebar => {
        // Preserve scroll position
        let savedScrollTop = 0;
        
        sidebar.addEventListener('hide.bs.offcanvas', function() {
          const body = this.querySelector('.offcanvas-body');
          if (body) savedScrollTop = body.scrollTop;
        });
        
        sidebar.addEventListener('shown.bs.offcanvas', function() {
          const body = this.querySelector('.offcanvas-body');
          if (body) body.scrollTop = savedScrollTop;
        });
        
        // Disable collapse when offcanvas is active
        sidebar.addEventListener('show.bs.offcanvas', function() {
          this.classList.remove('collapsed');
          const collapseToggle = this.querySelector('.collapse-toggle');
          if (collapseToggle) collapseToggle.disabled = true;
        });
      });
    }
    
    setupCollapseHandlers() {
      const collapseToggles = document.querySelectorAll('.collapse-toggle');
      
      collapseToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
          e.preventDefault();
          
          const sidebar = toggle.closest('.content-sidebar-left, .content-sidebar-right');
          if (!sidebar) return;
          
          // Only allow collapse if not in offcanvas mode
          if (!this.isOffcanvasMode(sidebar)) {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('inner-sidebar-collapsed', sidebar.classList.contains('collapsed'));
          }
        });
      });
    }
    
    handleBreakpointChanges() {
      const sidebars = document.querySelectorAll('.content-sidebar-left, .content-sidebar-right');
      
      sidebars.forEach(sidebar => {
        const isOffcanvas = this.isOffcanvasMode(sidebar);
        const collapseToggle = sidebar.querySelector('.collapse-toggle');
        
        if (isOffcanvas) {
          // Disable collapse in offcanvas mode
          sidebar.classList.remove('collapsed');
          if (collapseToggle) {
            collapseToggle.style.display = 'none';
          }
        } else {
          // Enable collapse in static mode
          if (collapseToggle) {
            collapseToggle.style.display = '';
          }
          // Restore collapse state
          const wasCollapsed = localStorage.getItem('inner-sidebar-collapsed') === 'true';
          if (wasCollapsed) {
            sidebar.classList.add('collapsed');
          }
        }
      });
    }
    
    isOffcanvasMode(sidebar) {
      // Check if sidebar is in offcanvas mode
      const style = window.getComputedStyle(sidebar);
      return style.position === 'fixed';
    }
  }
  
  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new InnerLayoutManager());
  } else {
    new InnerLayoutManager();
  }
})();
```

---

## 7. Complete Code Examples

### 7.1 Basic Implementation: Single Sidebar with Offcanvas

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Inner Layout - Single Sidebar</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    .inner-layout {
      height: calc(100vh - 56px); /* Adjust for navbar */
    }
    .content-sidebar-left {
      --bs-offcanvas-width: 280px;
    }
    .content-sidebar-left.offcanvas-md {
      @media (min-width: 768px) {
        position: static;
        width: 280px;
        transform: none;
        visibility: visible;
      }
    }
    .offcanvas-body {
      @media (min-width: 768px) {
        padding: 0 !important;
      }
    }
    .inner-main {
      overflow-y: auto;
    }
  </style>
</head>
<body>

  <!-- Page Header -->
  <nav class="navbar navbar-dark bg-dark">
    <div class="container-fluid">
      <!-- Sidebar toggle (mobile only) -->
      <button class="btn btn-dark d-md-none" 
              type="button" 
              data-bs-toggle="offcanvas" 
              data-bs-target="#primarySidebar">
        <i class="bi bi-list"></i>
      </button>
      <span class="navbar-brand mb-0 h1">My App</span>
    </div>
  </nav>

  <!-- Inner Layout -->
  <div class="inner-layout d-flex">
    
    <!-- Primary Sidebar with Responsive Offcanvas -->
    <div class="offcanvas-md offcanvas-start content-sidebar-left" 
         tabindex="-1" 
         id="primarySidebar"
         aria-labelledby="primarySidebarLabel">
      
      <div class="offcanvas-header d-md-none">
        <h5 class="offcanvas-title" id="primarySidebarLabel">Navigation</h5>
        <button type="button" 
                class="btn-close" 
                data-bs-dismiss="offcanvas" 
                aria-label="Close"></button>
      </div>
      
      <div class="offcanvas-body p-3">
        <nav aria-label="Primary navigation">
          <ul class="nav flex-column">
            <li class="nav-item">
              <a class="nav-link active" href="#"><i class="bi bi-house me-2"></i>Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#"><i class="bi bi-graph-up me-2"></i>Dashboard</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#"><i class="bi bi-gear me-2"></i>Settings</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="inner-main flex-grow-1 p-4">
      <h1>Main Content</h1>
      <p>This is the main content area. On mobile (below 768px), the sidebar becomes an offcanvas that can be toggled.</p>
      <p>On desktop (768px and above), the sidebar is always visible.</p>
    </div>
    
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 7.2 Advanced Implementation: Dual Sidebars with Collapse

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Inner Layout - Dual Sidebars</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
  <style>
    .inner-layout {
      height: calc(100vh - 56px);
    }
    
    /* Sidebar base styles */
    .content-sidebar-left,
    .content-sidebar-right {
      transition: width 0.3s ease;
    }
    
    .content-sidebar-left {
      --bs-offcanvas-width: 280px;
      width: 280px;
    }
    
    .content-sidebar-right {
      --bs-offcanvas-width: 250px;
      width: 250px;
    }
    
    /* Collapsed state (desktop only) */
    @media (min-width: 768px) {
      .content-sidebar-left.collapsed {
        width: 64px;
      }
      
      .content-sidebar-left.collapsed .menu-text,
      .content-sidebar-right.collapsed .menu-text {
        display: none;
      }
    }
    
    /* Static sidebar above breakpoint */
    .offcanvas-md {
      @media (min-width: 768px) {
        position: static !important;
        transform: none !important;
        visibility: visible !important;
      }
      
      .offcanvas-header {
        @media (min-width: 768px) {
          display: none;
        }
      }
      
      .offcanvas-body {
        @media (min-width: 768px) {
          padding: 0 !important;
        }
      }
    }
    
    .inner-main {
      overflow-y: auto;
      min-width: 0;
    }
    
    .collapse-toggle {
      @media (max-width: 767.98px) {
        display: none !important;
      }
    }
  </style>
</head>
<body>

  <!-- Page Header -->
  <nav class="navbar navbar-dark bg-dark">
    <div class="container-fluid">
      <div class="d-flex align-items-center gap-2 w-100">
        <!-- Primary sidebar toggle (mobile) -->
        <button class="btn btn-dark d-md-none" 
                type="button" 
                data-bs-toggle="offcanvas" 
                data-bs-target="#primarySidebar">
          <i class="bi bi-layout-sidebar"></i>
        </button>
        
        <span class="navbar-brand mb-0 h1">Dashboard</span>
        
        <!-- Secondary sidebar toggle (mobile) -->
        <button class="btn btn-dark d-md-none ms-auto" 
                type="button" 
                data-bs-toggle="offcanvas" 
                data-bs-target="#secondarySidebar">
          <i class="bi bi-info-circle"></i>
        </button>
      </div>
    </div>
  </nav>

  <!-- Inner Layout -->
  <div class="inner-layout d-flex">
    
    <!-- Primary Sidebar (Left) -->
    <div class="offcanvas-md offcanvas-start content-sidebar-left" 
         tabindex="-1" 
         id="primarySidebar"
         aria-labelledby="primarySidebarLabel">
      
      <div class="offcanvas-header d-md-none">
        <h5 class="offcanvas-title" id="primarySidebarLabel">Navigation</h5>
        <button type="button" 
                class="btn-close" 
                data-bs-dismiss="offcanvas" 
                aria-label="Close"></button>
      </div>
      
      <div class="offcanvas-body">
        <div class="sidebar-inner h-100 d-flex flex-column">
          
          <!-- Collapse toggle (desktop only) -->
          <div class="d-none d-md-flex justify-content-end p-2">
            <button class="btn btn-sm btn-outline-secondary collapse-toggle" 
                    id="primaryCollapseToggle"
                    aria-label="Toggle sidebar collapse">
              <i class="bi bi-chevron-left"></i>
            </button>
          </div>
          
          <nav class="flex-grow-1 p-3" aria-label="Primary navigation">
            <ul class="nav flex-column">
              <li class="nav-item mb-2">
                <a class="nav-link active d-flex align-items-center" href="#">
                  <i class="bi bi-house fs-5"></i>
                  <span class="menu-text ms-2">Home</span>
                </a>
              </li>
              <li class="nav-item mb-2">
                <a class="nav-link d-flex align-items-center" href="#">
                  <i class="bi bi-graph-up fs-5"></i>
                  <span class="menu-text ms-2">Dashboard</span>
                </a>
              </li>
              <li class="nav-item mb-2">
                <a class="nav-link d-flex align-items-center" href="#">
                  <i class="bi bi-people fs-5"></i>
                  <span class="menu-text ms-2">Users</span>
                </a>
              </li>
              <li class="nav-item mb-2">
                <a class="nav-link d-flex align-items-center" href="#">
                  <i class="bi bi-gear fs-5"></i>
                  <span class="menu-text ms-2">Settings</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="inner-main flex-grow-1 p-4">
      <h1>Dashboard</h1>
      <p>This is the main content area with dual sidebars.</p>
      
      <h2>Features:</h2>
      <ul>
        <li><strong>Mobile (&lt;768px)</strong>: Both sidebars are offcanvas (can be toggled)</li>
        <li><strong>Desktop (≥768px)</strong>: Both sidebars are visible, primary sidebar can collapse</li>
        <li><strong>Collapse</strong>: Only works in desktop mode (static sidebar)</li>
        <li><strong>State Preservation</strong>: Scroll positions and collapse state are preserved</li>
      </ul>
      
      <div class="card mt-4">
        <div class="card-body">
          <h5 class="card-title">Sample Content</h5>
          <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        </div>
      </div>
    </div>
    
    <!-- Secondary Sidebar (Right) -->
    <div class="offcanvas-md offcanvas-end content-sidebar-right" 
         tabindex="-1" 
         id="secondarySidebar"
         aria-labelledby="secondarySidebarLabel">
      
      <div class="offcanvas-header d-md-none">
        <h5 class="offcanvas-title" id="secondarySidebarLabel">Info Panel</h5>
        <button type="button" 
                class="btn-close" 
                data-bs-dismiss="offcanvas" 
                aria-label="Close"></button>
      </div>
      
      <div class="offcanvas-body p-3">
        <h5>Quick Info</h5>
        <div class="card mb-3">
          <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">Statistics</h6>
            <p class="card-text">Total Users: 1,234</p>
            <p class="card-text">Active: 456</p>
          </div>
        </div>
        
        <h5>Recent Activity</h5>
        <ul class="list-unstyled">
          <li class="mb-2">
            <small class="text-muted">2 mins ago</small>
            <div>User signed up</div>
          </li>
          <li class="mb-2">
            <small class="text-muted">5 mins ago</small>
            <div>Report generated</div>
          </li>
        </ul>
      </div>
    </div>
    
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    // Collapse toggle functionality
    document.addEventListener('DOMContentLoaded', function() {
      const primarySidebar = document.getElementById('primarySidebar');
      const collapseToggle = document.getElementById('primaryCollapseToggle');
      
      // Restore collapse state
      const wasCollapsed = localStorage.getItem('primary-sidebar-collapsed') === 'true';
      if (wasCollapsed && window.innerWidth >= 768) {
        primarySidebar.classList.add('collapsed');
      }
      
      // Toggle collapse
      collapseToggle.addEventListener('click', function() {
        // Only allow collapse if not in offcanvas mode
        const isOffcanvas = window.getComputedStyle(primarySidebar).position === 'fixed';
        
        if (!isOffcanvas) {
          primarySidebar.classList.toggle('collapsed');
          const isCollapsed = primarySidebar.classList.contains('collapsed');
          localStorage.setItem('primary-sidebar-collapsed', isCollapsed);
          
          // Update toggle icon
          const icon = this.querySelector('i');
          icon.classList.toggle('bi-chevron-left');
          icon.classList.toggle('bi-chevron-right');
        }
      });
      
      // Disable collapse when entering offcanvas mode
      primarySidebar.addEventListener('show.bs.offcanvas', function() {
        this.classList.remove('collapsed');
      });
      
      // Handle window resize
      window.addEventListener('resize', function() {
        const isOffcanvas = window.getComputedStyle(primarySidebar).position === 'fixed';
        
        if (isOffcanvas) {
          primarySidebar.classList.remove('collapsed');
        } else {
          // Restore collapse state when back to static
          const wasCollapsed = localStorage.getItem('primary-sidebar-collapsed') === 'true';
          if (wasCollapsed) {
            primarySidebar.classList.add('collapsed');
          }
        }
      });
    });
  </script>
</body>
</html>
```

---

## Summary

This guide provides comprehensive implementation patterns for integrating Bootstrap 5.3 offcanvas behavior into the inner layout component. Key takeaways:

1. **Use Responsive Offcanvas Classes** (`.offcanvas-md`, etc.) for automatic breakpoint handling
2. **Enforce State Constraints**: Collapse is disabled when sidebar is in offcanvas mode
3. **Toggle Button Visibility**: Show offcanvas toggle below breakpoint, collapse toggle above
4. **Preserve Content State**: Scroll positions and sidebar state persist across mode transitions
5. **Follow Accessibility Best Practices**: Proper ARIA labels, focus management, keyboard navigation
6. **Django-Cotton Pattern**: Component-based structure with slot composition for flexible layouts

The implementation should seamlessly switch between static sidebar (desktop) and offcanvas (mobile) while maintaining user state and providing excellent accessibility.
