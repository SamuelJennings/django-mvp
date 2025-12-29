# Research: Inner Layout Component

**Feature**: 002-inner-layout  
**Date**: 2025-12-23  
**Phase**: 0 (Research & Discovery)

## Overview

This document consolidates research findings to resolve unknowns from the Technical Context and inform Phase 1 design decisions for the inner layout component.

## Research Areas

### 1. Existing Implementation Analysis

**Status**: ~40-53% complete for specification requirements

#### What Exists and Works

**HTML Component** (`mvp/templates/cotton/layouts/inner.html`):
```django-html
<c-vars gap="0" class />
<div class="content-shell d-flex gap-{{ gap }} {{ class }}"
     {{ attrs }}>
  {{ primary_sidebar }}
  <div class="content-main flex-grow-1 overflow-auto">{{ slot }}</div>
  {{ secondary_sidebar }}
</div>
```

**Strengths**:
- Uses Django-Cotton component with named slots (primary_sidebar, secondary_sidebar)
- Default slot for main content (✅ aligns with spec clarification)
- Flexbox-based layout with configurable gap
- Pass-through attributes via `{{ attrs }}`

**Gaps for Spec**:
- No empty slot detection (FR-009) - empty slots render as empty containers
- No data attribute processing (FR-006) - gap is component parameter, not data attribute
- No responsive offcanvas wrapping at md breakpoint
- No ARIA landmarks (FR-011)

**CSS** (`mvp/static/scss/_content-layout.scss`):

**Strengths**:
- CSS variables for sidebar widths (--inner-primary-width, --inner-secondary-width)
- Smooth collapse transitions (0.3s ease)
- Cross-browser scrollbar styling
- Collapsed state with .collapsed-only/.expanded-only content switching
- Mobile stacking at 991px

**Gaps for Spec**:
- Wrong default width: 250px (spec requires 280px primary, 250px secondary)
- Wrong breakpoint: 991px/lg (spec requires 768px/md)
- Mobile behavior: stacks vertically (spec requires offcanvas mode)
- No offcanvas integration
- Class naming uses deprecated .inner-* instead of .content-* (backwards-compat aliases exist)

**JavaScript** (`mvp/static/js/inner_layout.js`):

**Strengths**:
- Toggle collapse state for primary/secondary sidebars independently
- LocalStorage persistence of collapse state
- Event-based toggle buttons
- Responsive initialization

**Gaps for Spec**:
- No offcanvas mode implementation
- No constraint enforcement (collapse allowed in offcanvas mode - spec prohibits this)
- No TypeScript source (spec requires compiled JS from TS)
- No data attribute configuration processing

#### Critical Implementation Gaps

1. **Offcanvas Mode** (HIGH PRIORITY):
   - Currently: Sidebars stack vertically at <991px
   - Required: Sidebars become toggleable offcanvas at <768px
   - Needs: Bootstrap 5.3 offcanvas component integration

2. **Empty Slot Detection** (HIGH PRIORITY):
   - Currently: Empty sidebar slots render empty `<div>` containers
   - Required: Empty slots should not render containers (FR-009)
   - Needs: Django-Cotton template logic to check slot content

3. **Data Attribute Configuration** (MEDIUM PRIORITY):
   - Currently: Only `gap` parameter via `<c-vars>`
   - Required: data-primary-width, data-secondary-width, data-breakpoint, data-gap
   - Needs: Attribute extraction and CSS variable application

4. **Responsive Breakpoint** (HIGH PRIORITY):
   - Currently: 991px (Bootstrap lg)
   - Required: 768px (Bootstrap md)
   - Needs: SCSS media query update

5. **Default Dimensions** (LOW PRIORITY - easy fix):
   - Currently: 250px for both sidebars
   - Required: 280px primary_sidebar, 250px secondary_sidebar
   - Needs: CSS variable update

6. **ARIA Landmarks** (MEDIUM PRIORITY):
   - Currently: No accessibility markup
   - Required: role="main" for content-main, role="complementary" for sidebars
   - Needs: HTML attribute additions

### 2. Bootstrap 5.3 Offcanvas Integration

#### Offcanvas API

**Required HTML Structure**:
```html
<div class="offcanvas offcanvas-start" tabindex="-1" id="sidebarOffcanvas"
     aria-labelledby="sidebarOffcanvasLabel">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="sidebarOffcanvasLabel">Navigation</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <!-- Sidebar content -->
  </div>
</div>
```

**Bootstrap Responsive Offcanvas** (Bootstrap 5.3+):
```html
<!-- Shows as offcanvas below md, normal sidebar at md+ -->
<div class="offcanvas-md offcanvas-start">...</div>
```

**Key Classes**:
- `.offcanvas-{breakpoint}`: Responsive offcanvas (e.g., `.offcanvas-md`)
- `.offcanvas-start`: Left sidebar
- `.offcanvas-end`: Right sidebar
- `.offcanvas-backdrop`: Background overlay (auto-managed by Bootstrap)

**JavaScript API**:
```javascript
const offcanvas = new bootstrap.Offcanvas(element);
offcanvas.show();   // Open offcanvas
offcanvas.hide();   // Close offcanvas
offcanvas.toggle(); // Toggle state
```

**Events**:
- `show.bs.offcanvas`: Before opening
- `shown.bs.offcanvas`: After opening (with transition)
- `hide.bs.offcanvas`: Before closing
- `hidden.bs.offcanvas`: After closing (with transition)

#### Responsive Pattern Decision

**Recommendation**: Use Bootstrap's `.offcanvas-md` class

**Rationale**:
- Native Bootstrap feature (v5.3+) - no custom media queries needed
- Automatically handles breakpoint transitions
- Maintains Bootstrap accessibility patterns
- Simplifies state management

**Implementation**:
```html
<div class="offcanvas-md offcanvas-start content-sidebar-left" 
     id="primarySidebar"
     tabindex="-1">
  <div class="offcanvas-header d-md-none">
    <h5 class="offcanvas-title">Primary Sidebar</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
  </div>
  <div class="offcanvas-body">
    <!-- Sidebar content from primary_sidebar slot -->
  </div>
</div>
```

**Toggle Button** (visible only <md):
```html
<button class="btn btn-primary d-md-none" 
        type="button" 
        data-bs-toggle="offcanvas" 
        data-bs-target="#primarySidebar"
        aria-controls="primarySidebar">
  <i class="bi bi-list"></i> Toggle Sidebar
</button>
```

#### State Management Constraints

**Three Distinct States**:
1. **NORMAL**: Sidebar visible in layout (≥768px)
2. **COLLAPSED**: Sidebar width reduced to fit-content/icons (≥768px only)
3. **OFFCANVAS**: Sidebar hidden, toggleable overlay (<768px)

**Constraint Enforcement** (from spec clarification):
- A sidebar **MAY NOT** be collapsed while in offcanvas mode
- Offcanvas mode takes precedence at <md breakpoint
- Collapse toggle button should be hidden/disabled at <md

**Implementation Pattern**:
```javascript
class InnerLayoutState {
  constructor(sidebar) {
    this.sidebar = sidebar;
    this.breakpoint = 768; // md breakpoint
  }
  
  isOffcanvasMode() {
    return window.innerWidth < this.breakpoint;
  }
  
  toggleCollapse() {
    if (this.isOffcanvasMode()) {
      console.warn('Cannot collapse sidebar in offcanvas mode');
      return false;
    }
    this.sidebar.classList.toggle('collapsed');
    return true;
  }
  
  updateCollapseButtonVisibility() {
    const collapseBtn = this.sidebar.querySelector('.collapse-toggle');
    if (this.isOffcanvasMode()) {
      collapseBtn?.setAttribute('disabled', 'true');
      collapseBtn?.classList.add('d-none');
    } else {
      collapseBtn?.removeAttribute('disabled');
      collapseBtn?.classList.remove('d-none');
    }
  }
}
```

### 3. Django-Cotton Slot Patterns

#### Empty Slot Detection

**Problem**: Need to detect if a named slot has content to avoid rendering empty containers.

**Django-Cotton Pattern**:
```django-html
{% if primary_sidebar %}
  <div class="content-sidebar-left">
    {{ primary_sidebar }}
  </div>
{% endif %}
```

**Limitation**: Django-Cotton slots are always defined (even if empty), so simple `{% if %}` won't work.

**Solution**: Use `{% if primary_sidebar|striptags|trim %}`
```django-html
{% if primary_sidebar|striptags|trim %}
  <div class="offcanvas-md offcanvas-start content-sidebar-left"
       id="primarySidebar">
    <div class="offcanvas-body">
      {{ primary_sidebar }}
    </div>
  </div>
{% endif %}
```

This strips HTML tags and whitespace to check for actual content.

#### Default vs Named Slots

**Spec Clarification**: Main content uses default (unnamed) slot.

**Current Implementation**: ✅ Already correct
```django-html
<div class="content-main">{{ slot }}</div>
```

**Usage**:
```django-html
<c-layouts.inner>
  <!-- This goes to default slot / {{ slot }} -->
  <h1>Main Content</h1>
  
  <c-slot name="primary_sidebar">
    <!-- This goes to {{ primary_sidebar }} -->
    <nav>...</nav>
  </c-slot>
</c-layouts.inner>
```

### 4. Data Attribute Configuration

#### Pattern Decision

**Approach**: Extract data attributes from `{{ attrs }}` and apply as CSS variables.

**Implementation**:
```django-html
<c-vars 
  gap="0" 
  class
  primary_width="280px"
  secondary_width="250px"
  breakpoint="md"
/>

<div class="content-shell d-flex gap-{{ gap }} {{ class }}"
     style="
       --content-primary-width: {{ primary_width }};
       --content-secondary-width: {{ secondary_width }};
     "
     data-breakpoint="{{ breakpoint }}"
     {{ attrs }}>
  <!-- ... -->
</div>
```

**CSS Consumption**:
```scss
.content-sidebar-left {
  width: var(--content-primary-width, 280px);
}

.content-sidebar-right {
  width: var(--content-secondary-width, 250px);
}
```

#### Supported Data Attributes

From spec requirements and clarifications:

| Attribute | Default | Description |
|-----------|---------|-------------|
| `primary-width` | 280px | Width of primary_sidebar |
| `secondary-width` | 250px | Width of secondary_sidebar |
| `breakpoint` | md | When to switch to offcanvas mode |
| `gap` | 0 | Spacing between columns |
| `collapse-primary` | false | Enable collapse for primary_sidebar |
| `collapse-secondary` | false | Enable collapse for secondary_sidebar |

### 5. Accessibility Requirements

#### ARIA Landmarks

**From Spec**: FR-011 requires accessible layout regions.

**Implementation**:
```django-html
<!-- Main content -->
<div class="content-main" role="main" aria-label="Main content">
  {{ slot }}
</div>

<!-- Primary sidebar -->
<div class="content-sidebar-left" role="complementary" aria-label="Primary sidebar">
  {{ primary_sidebar }}
</div>

<!-- Secondary sidebar -->
<div class="content-sidebar-right" role="complementary" aria-label="Secondary sidebar">
  {{ secondary_sidebar }}
</div>
```

#### Offcanvas Accessibility

**Bootstrap Handles**:
- `role="dialog"` on offcanvas container
- `aria-modal="true"` for modal behavior
- `tabindex="-1"` for focus management
- Escape key to close
- Focus trap when open

**We Must Add**:
- `aria-label` or `aria-labelledby` for offcanvas title
- Proper heading hierarchy in offcanvas-header
- Toggle button `aria-controls` and `aria-expanded` states

#### Keyboard Navigation

**Requirements**:
- Tab through sidebar content
- Escape to close offcanvas
- Toggle buttons keyboard accessible (native button elements)
- Focus visible indicators

### 6. Testing Strategy

#### Unit Tests (pytest + pytest-django)

**Test Slot Handling** (`test_inner_layout_slots.py`):
```python
def test_renders_without_sidebars():
    """Test basic content layout without sidebars (User Story 1)"""
    html = render_to_string('cotton/layouts/inner.html', {
        'slot': '<h1>Main Content</h1>'
    })
    assert 'Main Content' in html
    assert 'content-sidebar-left' not in html
    assert 'content-sidebar-right' not in html

def test_renders_with_primary_sidebar():
    """Test single sidebar layout (User Story 2)"""
    html = render_to_string('cotton/layouts/inner.html', {
        'slot': '<h1>Main Content</h1>',
        'primary_sidebar': '<nav>Navigation</nav>'
    })
    assert 'Navigation' in html
    assert 'content-sidebar-left' in html
    assert 'content-sidebar-right' not in html

def test_empty_sidebar_not_rendered():
    """Test FR-009: Empty slots don't render containers"""
    html = render_to_string('cotton/layouts/inner.html', {
        'slot': '<h1>Main Content</h1>',
        'primary_sidebar': '   \n  ',  # Whitespace only
    })
    assert 'content-sidebar-left' not in html
```

**Test Responsive Behavior** (`test_inner_layout_responsive.py`):
- Verify `.offcanvas-md` class applied
- Verify toggle buttons present
- Verify ARIA attributes
- Verify collapse constraint enforcement

**Test Component Rendering** (`test_inner_layout_component.py`):
- Verify default dimensions (280px/250px)
- Verify data attribute configuration
- Verify CSS variables set correctly
- Verify accessibility landmarks

## Key Design Decisions

### Decision 1: Use Bootstrap's `.offcanvas-md` Class

**Chosen**: Bootstrap 5.3's responsive offcanvas feature  
**Alternative Considered**: Custom media queries + JavaScript state management  
**Rationale**: Native Bootstrap feature eliminates custom breakpoint logic, maintains accessibility patterns, simplifies implementation

### Decision 2: Empty Slot Detection via `|striptags|trim` Filter

**Chosen**: `{% if slot_name|striptags|trim %}`  
**Alternative Considered**: Custom Cotton template tag to check slot content  
**Rationale**: Standard Django template filters, no custom tag needed, works with any whitespace or HTML

### Decision 3: Data Attributes as CSS Variables

**Chosen**: Extract data attributes → Apply as inline CSS variables → Consume in SCSS  
**Alternative Considered**: JavaScript-driven style application  
**Rationale**: CSS variables support runtime theming (Constitution Principle VI), no JS required for static configuration, plays well with django-compressor

### Decision 4: Collapse Constraint via JavaScript State Management

**Chosen**: JavaScript class tracks viewport width, disables collapse at <md  
**Alternative Considered**: CSS-only media queries (can't enforce constraint)  
**Rationale**: Spec explicitly requires collapse cannot happen in offcanvas mode; needs programmatic enforcement

### Decision 5: TypeScript for All Behavior

**Chosen**: Author in TypeScript → Compile to ES5/ES6 bundle → Ship compiled JS  
**Alternative Considered**: Plain JavaScript  
**Rationale**: Constitution Principle IX requires TypeScript; provides type safety for state management; aligns with modern tooling

## Implementation Priorities

### Phase 1 (High Priority - 8-12 hours):
1. Fix default dimensions (280px/250px)
2. Update breakpoint (991px → 768px)
3. Add empty slot detection with `|striptags|trim`
4. Add ARIA landmarks (role="main", role="complementary")
5. Integrate `.offcanvas-md` class
6. Add toggle buttons with proper ARIA

### Phase 2 (Medium Priority - 12-16 hours):
1. Implement data attribute configuration
2. Create TypeScript source for state management
3. Implement collapse constraint enforcement
4. Add offcanvas event handling
5. Comprehensive testing (3 test files)

### Phase 3 (Low Priority - 8-12 hours):
1. Update class naming (.inner-* → .content-*)
2. Documentation (INNER_LAYOUT.md)
3. Update quickstart.md
4. Example templates
5. Performance testing

## Next Steps

With research complete, proceed to **Phase 1: Design** to generate:
1. `data-model.md` - Component structure, state model, data attributes
2. `contracts/` - Component API, CSS classes, JavaScript API
3. `quickstart.md` - Developer quick-start examples
4. Update agent context with inner layout patterns
