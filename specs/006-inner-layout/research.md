# Research: Inner Layout System

**Feature**: Inner Layout System
**Date**: January 19, 2026
**Status**: Phase 0 Complete

## Research Tasks

This document consolidates research findings for implementing the inner layout system for Django MVP.

## CSS Grid Layout Pattern (AdminLTE 4 Style)

**Decision**: Use CSS Grid with fixed and flexible areas to replicate AdminLTE 4's outer app-wrapper pattern for the inner layout container.

**Rationale**:

- AdminLTE 4 uses CSS Grid for its main app-wrapper layout with `grid-template-rows` and `grid-template-columns` to create fixed and flexible areas
- CSS Grid provides the most robust way to handle complex layouts with sticky positioning and flexible content areas
- Modern browser support is excellent (95%+ global coverage)
- Grid allows precise control over area sizing with `auto`, `1fr`, and fixed values
- Matches existing outer layout architecture for consistency

**Implementation Pattern**:

```scss
.page-layout-wrapper {
  display: grid;
  grid-template-rows: auto 1fr auto;  // toolbar, content, footer
  grid-template-columns: 1fr auto;    // content, sidebar (when visible)
  height: 100%;
  overflow: hidden;
}

.page-toolbar {
  grid-row: 1;
  grid-column: 1 / -1;
  position: sticky;
  top: 0;
  z-index: 100;
}


.page-sidebar {
  grid-row: 2 / 4;  // spans content + footer rows
  grid-column: 2;
  overflow-y: auto;
}

.page-footer {
  grid-row: 3;
  grid-column: 1;
  position: sticky;
  bottom: 0;
  z-index: 100;
}
```

**Alternatives Considered**:

- Flexbox: Less precise control for complex multi-area layouts
- Absolute positioning: Brittle and difficult to maintain responsively
- Table display: Legacy approach with poor semantic value

## Django Cotton Component Structure

**Decision**: Create 4 separate Cotton components with composition via slots - `page_layout.html` (container), `page_toolbar.html`, `page_footer.html`, `page_sidebar.html`.

**Rationale**:

- Cotton's slot system enables flexible composition with both default and named slots
- Using `<c-vars>` allows defining component attributes with defaults that can be overridden
- Separate components for toolbar/footer/sidebar allows optional usage (only include what you need)
- Follows Cotton best practices: component-specific logic in separate files
- Enables testing each component independently
- Example from Cotton docs shows card component with header/footer named slots - same pattern applies here

**Component Attribute Pattern** (from Cotton documentation):

```html
<!-- cotton/page_layout.html -->
<c-vars
  sidebar_width="280px"
  sidebar_visible="true"
  toolbar_class=""
  footer_class=""
/>

<div class="page-layout-wrapper {{ class }}"
     style="--page-sidebar-width: {{ sidebar_width }}">

  {% if toolbar %}
    <div class="page-toolbar {{ toolbar_class }}">
      {{ toolbar }}
    </div>
  {% endif %}


  {% if sidebar_visible and sidebar %}
    <div class="page-sidebar">
      {{ sidebar }}
    </div>
  {% endif %}

  {% if footer %}
    <div class="page-footer {{ footer_class }}">
      {{ footer }}
    </div>
  {% endif %}
</div>
```

**Usage Example**:

```html
<c-mvp.page_layout sidebar_width="320px" sidebar_visible="true">
  <c-slot name="toolbar">
    <div>Page Title | Filters | Actions</div>
  </c-slot>

  <!-- Main content in default slot -->
  <table>...</table>

  <c-slot name="sidebar">
    <div>Properties Panel</div>
  </c-slot>

  <c-slot name="footer">
    <div>Pagination: 1 2 3...</div>
  </c-slot>
</c-mvp.page_layout>
```

**Alternatives Considered**:

- Single monolithic component: Less flexible, harder to test
- Multiple configuration-driven sections: More complex, harder to understand
- MVP settings dictionary: Violates the clarification that inner layout is template-driven

## Sticky Positioning Within Scroll Container

**Decision**: Use CSS `position: sticky` for toolbar (top) and footer (bottom) within the scrolling content area, not viewport-fixed.

**Rationale**:

- Feature spec clarifies: "sticky within scrolling area (CSS position: sticky)" not fixed to viewport
- Bootstrap 5.3 provides `.sticky-top` and `.sticky-bottom` utilities but these are viewport-relative
- Custom sticky implementation within grid container achieves the desired effect
- Toolbar sticks to top when scrolling down, footer sticks to bottom when scrolling up
- z-index layering ensures sticky elements appear above scrolling content
- Works correctly with nested scroll containers (outer layout scroll + inner layout scroll)

**Implementation**:

```scss
.page-layout-wrapper {
  overflow: hidden;  // container clip

  .page-toolbar {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--bs-body-bg);
  }

  .page-footer {
    position: sticky;
    bottom: 0;
    z-index: 100;
    background: var(--bs-body-bg);
  }
}
```

**Alternatives Considered**:

- Viewport-fixed positioning: Would conflict with outer layout header/footer
- JavaScript scroll handlers: Unnecessary complexity, worse performance
- No sticky behavior: Doesn't meet feature requirements

## Bootstrap 5.3 Breakpoint Integration

**Decision**: Use Bootstrap 5.3's default 'lg' breakpoint (992px) for hiding secondary sidebar on smaller screens, with configurable override via component attribute.

**Rationale**:

- Feature spec clarifies: "Hide below Bootstrap's 'lg' breakpoint (1024px)" but Bootstrap's actual 'lg' is 992px
- Bootstrap breakpoints: xs: 0, sm: 576px, md: 768px, lg: 992px, xl: 1200px, xxl: 1400px
- 'lg' is appropriate for sidebar visibility - typical tablet landscape and desktop sizes
- Using Bootstrap's standard breakpoint ensures consistency with the rest of the framework
- Can be overridden via component attribute for specific use cases

**Implementation**:

```scss
// Using Bootstrap's responsive utilities
.page-sidebar {
  @include media-breakpoint-down(lg) {
    display: none;  // hide below lg (< 992px)
  }

  // Or with custom breakpoint if specified via CSS variable
  @media (max-width: var(--page-sidebar-breakpoint, 992px)) {
    display: none;
  }
}
```

**Usage with Custom Breakpoint**:

```html
<c-mvp.page_layout sidebar_breakpoint="1200px">
  ...
</c-mvp.page_layout>
```

**Alternatives Considered**:

- Fixed 1024px breakpoint: Not aligned with Bootstrap's standard breakpoints
- Always visible: Doesn't meet responsive requirements
- Collapse instead of hide: More complex, requires JavaScript toggle state

## Sidebar Toggle Functionality

**Decision**: Implement optional user toggle functionality with sessionStorage persistence, configurable via component attribute `sidebar_toggle="true"`.

**Rationale**:

- Feature spec clarifies: "configurable default state plus optional user toggle functionality"
- SessionStorage provides persistence during user session without server state
- Toggle button rendered conditionally based on attribute
- JavaScript handles toggle state and updates CSS class on container
- Follows Alpine.js patterns if available, vanilla JS otherwise
- Similar to outer layout sidebar behavior for consistency

**Implementation**:

```html
<!-- cotton/page_layout.html -->
<c-vars sidebar_toggle="false" />

<div class="page-layout-wrapper"
     data-page-layout
     {% if sidebar_toggle %}data-toggle-enabled="true"{% endif %}>

  {% if sidebar_toggle %}
    <button class="page-sidebar-toggle"
            data-toggle-sidebar
            aria-label="Toggle sidebar">
      <i class="icon-toggle"></i>
    </button>
  {% endif %}

  ...
</div>
```

```javascript
// static/mvp/js/page-layout.js
document.querySelectorAll('[data-toggle-sidebar]').forEach(button => {
  button.addEventListener('click', () => {
    const wrapper = button.closest('[data-page-layout]');
    const isCollapsed = wrapper.classList.toggle('sidebar-collapsed');
    sessionStorage.setItem('innerSidebarCollapsed', isCollapsed);
  });
});

// Restore state on page load
document.addEventListener('DOMContentLoaded', () => {
  const collapsed = sessionStorage.getItem('innerSidebarCollapsed') === 'true';
  if (collapsed) {
    document.querySelectorAll('[data-page-layout]').forEach(wrapper => {
      wrapper.classList.add('sidebar-collapsed');
    });
  }
});
```

**Alternatives Considered**:

- Always enabled: Not all use cases need toggle functionality
- LocalStorage: SessionStorage is more appropriate for UI state
- Server-side state: Unnecessary complexity for client-side UI preference

## Testing Strategy

**Decision**: Three-tier testing approach - unit tests for component rendering, integration tests for template inheritance, E2E tests for browser interactions.

**Rationale**:

- Constitution requires pytest, pytest-django, and pytest-playwright coverage
- Cotton components MUST be tested with `django_cotton.render_component()` (not Template() or render_to_string)
- Unit tests verify component rendering with various attribute combinations
- Integration tests verify inner layout works within outer layout structure
- E2E tests verify sticky positioning, responsive behavior, and toggle functionality
- Design-first approach means tests written after visual verification

**Test Structure**:

```python
# tests/components/test_page_layout.py
from django_cotton import render_component
from django.test import RequestFactory
import pytest

@pytest.fixture
def rf():
    return RequestFactory()

def test_page_layout_basic_rendering(rf):
    """Test basic inner layout renders with default slot"""
    result = render_component(
        rf.get('/'),
        'mvp.page_layout',
        slots={'slot': '<div>Main content</div>'}
    )
    assert 'page-layout-wrapper' in result
    assert 'Main content' in result

def test_page_layout_with_toolbar_and_footer(rf):
    """Test inner layout with toolbar and footer slots"""
    result = render_component(
        rf.get('/'),
        'mvp.page_layout',
        slots={
            'toolbar': '<div>Toolbar</div>',
            'slot': '<div>Content</div>',
            'footer': '<div>Footer</div>'
        }
    )
    assert 'page-toolbar' in result
    assert 'page-footer' in result

def test_page_layout_sidebar_visible(rf):
    """Test sidebar visibility with attribute"""
    result = render_component(
        rf.get('/'),
        'mvp.page_layout',
        attrs={'sidebar_visible': 'true'},
        slots={
            'slot': '<div>Content</div>',
            'sidebar': '<div>Sidebar</div>'
        }
    )
    assert 'page-sidebar' in result
```

```python
# tests/e2e/test_page_layout_e2e.py
from playwright.sync_api import Page, expect
import pytest

def test_sticky_toolbar_on_scroll(page: Page):
    """Verify toolbar sticks to top when scrolling down"""
    page.goto('/test-page-layout/')

    toolbar = page.locator('.page-toolbar')
    initial_position = toolbar.bounding_box()['y']

    # Scroll down
    page.evaluate('window.scrollBy(0, 500)')

    # Toolbar should remain at top
    scrolled_position = toolbar.bounding_box()['y']
    assert scrolled_position == initial_position

def test_sidebar_toggle_functionality(page: Page):
    """Verify sidebar toggle button works"""
    page.goto('/test-page-layout-toggle/')

    sidebar = page.locator('.page-sidebar')
    toggle = page.locator('[data-toggle-sidebar]')

    # Initially visible
    expect(sidebar).to_be_visible()

    # Click toggle
    toggle.click()

    # Should be hidden
    expect(sidebar).not_to_be_visible()
```

**Alternatives Considered**:

- Unit tests only: Insufficient coverage for complex layout interactions
- Manual testing only: Not repeatable, violates constitution
- E2E tests only: Slow, doesn't catch component-level issues early

## Component Naming Convention

**Decision**: Use snake_case for all component filenames and kebab-case (with hyphens) for multi-word class names in HTML/CSS.

**Rationale**:

- Cotton components MUST use snake_case (this is a fundamental requirement per instructions)
- ✅ Correct: `page_layout.html`, `page_toolbar.html` → `<c-mvp.page_layout />`, `<c-mvp.page_toolbar />`
- ❌ Wrong: `innerLayout.html`, `InnerLayout.html` → these don't work with Cotton
- CSS classes use kebab-case following BEM conventions: `.page-layout-wrapper`, `.page-toolbar`, `.page-sidebar`
- Consistent with existing MVP component structure

**Files to Create**:

- `mvp/templates/cotton/mvp/page_layout.html`
- `mvp/templates/cotton/mvp/page_toolbar.html` (optional separate component)
- `mvp/templates/cotton/mvp/page_footer.html` (optional separate component)
- `mvp/templates/cotton/mvp/page_sidebar.html` (optional separate component)
- `mvp/static/mvp/css/page-layout.scss`
- `mvp/static/mvp/js/page-layout.js` (for toggle functionality)

## Summary of Key Decisions

| Topic | Decision | Justification |
|-------|----------|---------------|
| Layout Technique | CSS Grid with fixed/flexible areas | Matches AdminLTE 4 pattern, robust for complex layouts |
| Component Structure | 4 separate Cotton components with slots | Flexible composition, independent testing, optional usage |
| Configuration | Template-driven via component attributes | Per spec clarification, not MVP settings dict |
| Sticky Behavior | CSS position: sticky within scroll container | Per spec clarification, not viewport-fixed |
| Responsive Breakpoint | Bootstrap 'lg' (992px) default, configurable | Aligns with Bootstrap standards, allows override |
| Toggle Persistence | SessionStorage for user preference | Appropriate for UI state without server complexity |
| Component Naming | snake_case files, kebab-case CSS classes | Cotton requirement, BEM CSS convention |
| Testing Approach | 3-tier: unit, integration, E2E | Constitution requirement, comprehensive coverage |

## Next Steps (Phase 1)

1. Create data-model.md defining component entities and relationships
2. Generate API contracts in contracts/ directory documenting component attributes and slots
3. Create quickstart.md with developer usage examples
4. Update agent context with new technology decisions
