# Research: AdminLTE 4 Widget Components

**Phase**: 0 - Outline & Research
**Date**: January 5, 2026
**Feature**: [spec.md](./spec.md)

## Research Tasks Completed

### 1. Django-Cotton Component Best Practices

**Decision**: Use `<c-vars>` for all configurable attributes with defaults
**Rationale**:

- Prevents attribute leakage to HTML output
- Provides clean default values
- Enables type documentation
- Follows django-cotton recommended patterns

**Implementation Pattern**:

```html
<c-vars
    variant="default"
    bg=""
    icon=""
    text=""
    number=""
    class=""
/>
```

**Alternatives Considered**:

- Direct attribute passthrough → Rejected: causes HTML attribute pollution
- Django template variables → Rejected: less explicit, harder to document

### 2. Bootstrap Icons Integration

**Decision**: Use c-icon component from django-easy-icons
**Rationale**:

- Provides unified icon interface across multiple icon libraries (Bootstrap Icons, FontAwesome, etc.)
- Handles icon rendering, sizing, and accessibility automatically
- Better separation of concerns - components receive icon names, c-icon handles implementation
- Supports future migration to different icon libraries without changing component APIs
- Includes built-in ARIA attributes for accessibility

**Example Implementation**:

```html
{% if icon %}
<c-icon name="bi:{{ icon }}" />
{% endif %}
```

**Alternatives Considered**:

- Direct Bootstrap Icons CSS (`<i class="bi bi-{icon}"></i>`) → Rejected: tightly couples components to specific icon library
- SVG slots → Rejected: more complex, inconsistent sizing, accessibility concerns
- Custom icon component → Rejected: django-easy-icons already provides this functionality

### 3. AdminLTE 4 Class Naming Conventions

**Decision**: Follow AdminLTE 4 BEM-style class structure
**Rationale**:

- Ensures visual parity with reference implementation
- Leverages existing AdminLTE CSS
- Maintains upgrade path to future AdminLTE versions

**Key Patterns Discovered**:

- **Info Box**: `.info-box`, `.info-box-icon`, `.info-box-content`, `.info-box-text`, `.info-box-number`
- **Small Box**: `.small-box`, `.small-box-icon`, `.inner`, `.small-box-footer`
- **Card**: `.card`, `.card-header`, `.card-title`, `.card-tools`, `.card-body`, `.card-footer`
- **Variants**: `.card-primary`, `.card-outline`, `.card-outline-primary`, `.text-bg-primary`

### 4. Color Variant Handling

**Decision**: Use `variant` attribute with "default" fallback, apply via class conditionals
**Rationale**:

- Separates semantic intent (variant) from presentation (classes)
- Enables validation and documentation
- Supports AdminLTE's color scheme system

**Implementation Pattern**:

```html
<div class="info-box{% if variant != 'default' %} text-bg-{{ variant }}{% endif %}">
```

**Alternatives Considered**:

- Direct class passthrough → Rejected: less validation, inconsistent API
- Separate boolean flags → Rejected: doesn't scale to 6+ variants

### 5. Gradient Effect Implementation

**Decision**: Apply `.bg-gradient` class when `gradient` attribute present and `bg` is set
**Rationale**:

- Leverages Bootstrap 5 gradient utilities
- Simple conditional logic
- Consistent with AdminLTE 4 patterns

**Implementation Pattern**:

```html
{% if bg and gradient %}bg-gradient{% endif %}
```

### 6. Cotton Named Slots Usage

**Decision**: Use named slots for optional complex content (footer, tools); default slot for body
**Rationale**:

- Provides flexibility for custom content
- Maintains simple API for common cases
- Follows Cotton best practices for composition

**Slot Patterns**:

- **Card footer**: `<c-slot name="footer">`
- **Card tools**: `<c-slot name="tools">` (can include buttons with c-icon components)
- **Card body**: Default unnamed slot

**Example with c-icon in tools slot**:

```html
<c-card title="System Status">
    <c-slot name="tools">
        <button type="button" class="btn btn-tool">
            <c-icon name="bi:gear" />
        </button>
    </c-slot>
    <p>System metrics and status...</p>
</c-card>
```

### 7. Component Testing Strategy

**Decision**: Use `django_cotton.render_component()` with pytest-django fixtures
**Rationale**:

- Tests actual Cotton component resolution
- Validates attribute handling
- Faster than full template rendering
- Aligns with constitution test-first principle

**Test Structure**:

```python
def test_info_box_basic(rf):
    result = render_component(
        rf.get("/"),
        "info-box",
        icon="gear-fill",
        text="CPU Traffic",
        number="10%"
    )
    assert 'class="info-box"' in result
    # Verify c-icon component is rendered with correct icon name
    assert 'bi:gear-fill' in result or 'c-icon' in result
```

### 8. AdminLTE JavaScript Integration

**Decision**: Render data attributes for AdminLTE JS; no custom JavaScript
**Rationale**:

- AdminLTE 4 handles collapse/remove/maximize via data attributes
- Keeps components stateless
- Maintains separation of concerns

**Data Attributes Required**:

- `data-lte-toggle="card-collapse"` - Collapse/expand functionality
- `data-lte-toggle="card-remove"` - Remove card functionality
- `data-lte-toggle="card-maximize"` - Maximize/minimize functionality
- `data-lte-icon="expand"` / `data-lte-icon="collapse"` - Icon state management

### 9. Accessibility Requirements

**Decision**: Include ARIA attributes for all interactive and semantic elements
**Rationale**:

- WCAG 2.1 AA compliance requirement (SC-006)
- Improves screen reader experience
- Matches AdminLTE 4 accessibility standards

**ARIA Patterns**:

- Progress bars: `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`
- Buttons: `aria-label` for icon-only buttons
- Collapsed state: `aria-expanded="false"` on card tools
- Decorative icons: c-icon component automatically includes `aria-hidden="true"` for decorative usage

### 10. Default Value Strategy

**Decision**: All color-related attributes default to "default" string in `<c-vars>`
**Rationale**:

- Provides explicit fallback for conditionals
- Distinguishes "not set" from "set to empty"
- Enables consistent template logic patterns
- Aligns with clarification decision

**Default Values by Component**:

- **info-box**: `variant="default"`, `bg=""`, `gradient=""`
- **small-box**: `variant="default"`, `link_text="More info"`
- **card**: `variant="default"`, `fill="outline"`, `collapsed=""`

## Dependencies Confirmed

### Required (Already in Project)

- Django 4.2+
- django-cotton (latest)
- django-easy-icons (provides c-icon component)
- Bootstrap 5.3 (via CDN in base template)
- AdminLTE 4 CSS (via CDN in base template)

### Testing

- pytest
- pytest-django
- djlint (template linting)

### No New Dependencies Required

All dependencies are already part of django-mvp project. No additional packages needed.

## Risk Assessment

### Low Risk

- ✅ Template-only changes (no Python code)
- ✅ No database migrations
- ✅ No breaking changes to existing API
- ✅ Incremental testing possible

### Medium Risk

- ⚠️ Visual regression if AdminLTE CSS changes
- ⚠️ JavaScript integration depends on AdminLTE version

### Mitigation Strategies

- Pin AdminLTE 4 version in documentation
- Include visual comparison tests against reference implementation
- Document AdminLTE JavaScript dependencies explicitly
