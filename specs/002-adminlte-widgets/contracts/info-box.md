# API Contract: Info Box Component

**Component Name**: `info-box`
**File**: `mvp/templates/cotton/info-box.html`
**Status**: Phase 1 Design

## Component Signature

```django
<c-info-box
    icon="string"
    icon_class="string"
    text="string"
    number="string"
    variant="string"
    fill="string"
    progress="integer"
    description="string"
    class="string"
/>
```

## Attributes

### Required Attributes

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `icon` | string | Icon name for c-icon component | `"gear-fill"` |
| `text` | string | Primary label text | `"CPU Traffic"` |
| `number` | string | Metric/statistic value | `"10%"` |

### Optional Attributes

| Attribute | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `variant` | string | `"default"` | Color variant (primary, success, warning, danger, info, secondary, default) | `"success"` |
| `fill` | string | `"icon"` | Where to apply color: "icon" (colored icon span) or "box" (entire info-box) | `"box"` |
| `progress` | integer | `""` | Progress bar percentage (0-100) | `"70"` |
| `description` | string | `""` | Progress bar description text | `"70% Increase"` |
| `icon_class` | string | `""` | Additional classes for c-icon component | `"fs-4"` |
| `class` | string | `""` | Additional CSS classes | `"mb-3 shadow"` |

## Slots

This component does not use slots.

## Output Contract

### HTML Structure

```html
<div class="info-box [fill-box-classes] [custom-classes]">
    <span class="info-box-icon [fill-icon-classes]" aria-hidden="true">
        <c-icon name="{{ icon }}" class="{{ icon_class }}" />
    </span>
    <div class="info-box-content">
        <span class="info-box-text">[text]</span>
        <span class="info-box-number">[number]</span>
        [progress-section]
    </div>
</div>
```

### Progress Section (when `progress` provided)

```html
<c-progress :value="[progress]"
            variant="[variant if fill==icon]"
            only />
<span class="progress-description">[description]</span>
```

## CSS Class Generation

### Fill Modes

The `fill` attribute controls where the `variant` color is applied:

| fill Value | Effect |
|------------|--------|
| `icon` (default) | Applies `text-bg-{variant}` to icon span only |
| `box` | Applies `text-bg-{variant}` to entire info-box div |

### Variant Classes

When `variant` != "default", applies Bootstrap's `text-bg-*` class to the element determined by `fill`:

| Variant | Class Applied |
|---------|---------------|
| primary | `text-bg-primary` |
| success | `text-bg-success` |
| warning | `text-bg-warning` |
| danger | `text-bg-danger` |
| info | `text-bg-info` |
| secondary | `text-bg-secondary` |
| default | *(no classes)* |

## Validation Rules

1. **Required Validation**:
   - `icon` must be provided
   - `text` must be provided
   - `number` must be provided

2. **Type Validation**:
   - `progress` must be numeric if provided
   - `progress` should be between 0-100 (no strict enforcement, relies on CSS)

3. **Dependency Validation**:
   - If `description` is provided, `progress` should also be provided (description shown but may look odd without progress bar)

4. **Attribute Validation** (recommended but not enforced):
   - `variant` should be one of: primary, success, warning, danger, info, secondary, default
   - `fill` should be one of: icon, box

## Accessibility

### ARIA Attributes

- `aria-hidden="true"` on `.info-box-icon` (decorative)
- `role="progressbar"` on `.progress` div (when progress present)
- `aria-valuenow="[progress]"` on `.progress` div
- `aria-valuemin="0"` on `.progress` div
- `aria-valuemax="100"` on `.progress` div

### Screen Reader Announcements

- Icon is hidden from screen readers (decorative)
- Text and number are read as-is
- Progress bar announces current value and range
- Description provides additional context for progress

## Examples

### Example 1: Basic Usage (Default Fill)

**Input**:

```django
<c-info-box
    icon="gear-fill"
    text="CPU Traffic"
    number="10%"
/>
```

**Output**:

```html
<div class="info-box">
    <span class="info-box-icon" aria-hidden="true">
        <c-icon name="gear-fill" />
    </span>
    <div class="info-box-content">
        <span class="info-box-text">CPU Traffic</span>
        <span class="info-box-number">10%</span>
    </div>
</div>
```

### Example 2: With Variant and Fill="icon" (Default)

**Input**:

```django
<c-info-box
    icon="bag-check-fill"
    text="Sales"
    number="13,648"
    variant="success"
/>
```

**Output**:

```html
<div class="info-box">
    <span class="info-box-icon text-bg-success" aria-hidden="true">
        <c-icon name="bag-check-fill" />
    </span>
    <div class="info-box-content">
        <span class="info-box-text">Sales</span>
        <span class="info-box-number">13,648</span>
    </div>
</div>
```

### Example 3: With Progress

**Input**:

```django
<c-info-box
    icon="download"
    text="Downloads"
    number="114,381"
    variant="info"
    progress="70"
    variant="info"
    progress="70"
    description="70% Increase in 30 Days"
/>
```

**Output**:

```html
<div class="info-box">
    <span class="info-box-icon text-bg-info" aria-hidden="true">
        <c-icon name="download" />
    </span>
    <div class="info-box-content">
        <span class="info-box-text">Downloads</span>
        <span class="info-box-number">114,381</span>
        <c-progress :value="70" variant="info" only />
        <span class="progress-description">70% Increase in 30 Days</span>
    </div>
</div>
```

### Example 4: With Fill="box" (Entire Box Colored)

**Input**:

```django
<c-info-box
    icon="flag-fill"
    text="Bookmarks"
    number="41,410"
    variant="warning"
    fill="box"
/>
```

**Output**:

```html
<div class="info-box text-bg-warning">
    <span class="info-box-icon" aria-hidden="true">
        <c-icon name="flag-fill" />
    </span>
    <div class="info-box-content">
        <span class="info-box-text">Bookmarks</span>
        <span class="info-box-number">41,410</span>
    </div>
</div>
```

## Error Handling

### Missing Required Attributes

Component renders with degraded experience:

- Missing `icon`: Icon span renders empty
- Missing `text`: Text span renders empty
- Missing `number`: Number span renders empty

### Invalid Attribute Values

- Invalid `progress` values (e.g., non-numeric): Template may error or render as-is depending on template engine
- Invalid `variant`: No classes applied (falls back to default styling)
- Invalid `bg`: Applied as `bg-{value}` (may not have CSS defined)

## CSS Dependencies

### Required AdminLTE 4 Classes

- `.info-box`
- `.info-box-icon`
- `.info-box-content`
- `.info-box-text`
- `.info-box-number`

### Required Bootstrap 5 Classes

- `.progress`
- `.progress-bar`
- `.text-bg-{variant}`
- `.bg-{color}`
- `.bg-gradient`

### Required Icon Component

- c-icon component for icon rendering

## Testing Requirements

### Unit Tests Required

1. ✅ Renders with all required attributes
2. ✅ Renders with variant classes correctly
3. ✅ Renders with custom background and gradient
4. ✅ Renders progress bar when progress provided
5. ✅ Omits progress bar when progress not provided
6. ✅ Applies custom classes via class attribute
7. ✅ Includes proper ARIA attributes on progress bar
8. ✅ Hides icon from screen readers with aria-hidden

### Integration Tests Required

1. ✅ Works within Bootstrap grid layouts
2. ✅ Multiple info boxes render independently
3. ✅ CSS classes resolve correctly with AdminLTE 4 CSS

## Version History

- **v1.0** (Phase 1): Initial contract definition
- **v2.0** (2026-01-05): Replaced `bg` and `gradient` attributes with unified `fill` attribute ("icon"|"box"). Progress bar now uses `<c-progress>` component. Simplified color application logic to match card component pattern.
