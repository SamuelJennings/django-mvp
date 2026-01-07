# API Contract: Small Box Component

**Component Name**: `small-box`
**File**: `mvp/templates/cotton/small-box.html`
**Status**: Phase 1 Design

## Component Signature

```django
<c-small-box
    heading="string"
    text="string"
    icon="string"
    icon_class="string"
    variant="string"
    link="string"
    link_text="string"
    link_icon="string"
    class="string"
/>
```

## Attributes

### Required Attributes

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `heading` | string | Main metric/number display | `"150"` |
| `text` | string | Description label | `"New Orders"` |
| `icon` | string | Icon name for c-icon component | `"cart-fill"` |

### Optional Attributes

| Attribute | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `variant` | string | `"default"` | Background color variant (primary, success, warning, danger, info, secondary, default) | `"primary"` |
| `link` | string | `""` | Footer link URL | `"/orders/"` |
| `link_text` | string | `"More info"` | Footer link text | `"View all orders"` |
| `link_icon` | string | `"link"` | Footer link icon name | `"arrow-right"` |
| `icon_class` | string | `""` | Additional classes for c-icon component | `"fs-4"` |
| `class` | string | `""` | Additional CSS classes | `"mb-3 shadow"` |

## Slots

This component does not use slots.

## Output Contract

### HTML Structure

```html
<div class="small-box text-bg-[variant] [custom-classes]">
    <div class="inner">
        <h3>[heading]</h3>
        <p>[text]</p>
    </div>
    <c-icon name="{{ icon }}" class="small-box-icon {{ icon_class }}" />
    [footer-section]
</div>
```

### Footer Section (when `link` provided)

```html
<a href="[link]" class="small-box-footer link-light link-underline-opacity-0 link-underline-opacity-50-hover">
    [link_text] <c-icon name="[link_icon]" />
</a>
```

## CSS Class Generation

### Background Classes

| variant Value | Classes Applied |
|---------------|----------------|
| primary | `text-bg-primary` |
| success | `text-bg-success` |
| warning | `text-bg-warning` |
| danger | `text-bg-danger` |
| info | `text-bg-info` |
| secondary | `text-bg-secondary` |
| default | `text-bg-default` |

## Validation Rules

1. **Required Validation**:
   - `heading` must be provided
   - `text` must be provided
   - `icon` must be provided

2. **Type Validation**:
   - `link` should be a valid URL or path if provided

3. **Dependency Validation**:
   - `link_text` only renders if `link` is provided
   - Default `link_text="More info"` is used if `link` present but `link_text` not specified

4. **Background Validation** (recommended but not enforced):
   - `variant` should be one of: primary, success, warning, danger, info, secondary, default

## Accessibility

### ARIA Attributes

- `aria-hidden="true"` on c-icon component (decorative, handled by component)

### Screen Reader Announcements

- Icon is hidden from screen readers (decorative)
- Heading is announced as heading level 3
- Text is read as paragraph
- Link announces destination and link text

### Semantic HTML

- `<h3>` for heading (proper heading hierarchy)
- `<p>` for descriptive text
- `<a>` for footer link (keyboard navigable)

## Examples

### Example 1: Basic Usage

**Input**:

```django
<c-small-box
    heading="150"
    text="New Orders"
    icon="cart-fill"
    variant="primary"
/>
```

**Output**:

```html
<div class="small-box text-bg-primary">
    <div class="inner">
        <h3>150</h3>
        <p>New Orders</p>
    </div>
    <c-icon name="cart-fill" class="small-box-icon" />
</div>
```

### Example 2: With Footer Link (Default Text)

**Input**:

```django
<c-small-box
    heading="53%"
    text="Bounce Rate"
    icon="graph-up"
    variant="warning"
    link="/analytics/"
/>
```

**Output**:

```html
<div class="small-box text-bg-warning">
    <div class="inner">
        <h3>53%</h3>
        <p>Bounce Rate</p>
    </div>
    <c-icon name="graph-up" class="small-box-icon" />
    <a href="/analytics/" class="small-box-footer link-light link-underline-opacity-0 link-underline-opacity-50-hover">
        More info <c-icon name="link-45deg" />
    </a>
</div>
```

### Example 3: With Custom Link Text

**Input**:

```django
<c-small-box
    heading="44"
    text="User Registrations"
    icon="person-fill-add"
    variant="success"
    link="/users/"
    link_text="View all users"
/>
```

**Output**:

```html
<div class="small-box text-bg-success">
    <div class="inner">
        <h3>44</h3>
        <p>User Registrations</p>
    </div>
    <c-icon name="person-fill-add" class="small-box-icon" />
    <a href="/users/" class="small-box-footer link-light link-underline-opacity-0 link-underline-opacity-50-hover">
        View all users <c-icon name="link-45deg" />
    </a>
</div>
```

### Example 4: With Custom Classes

**Input**:

```django
<c-small-box
    heading="99"
    text="Important Alerts"
    icon="exclamation-triangle-fill"
    variant="danger"
    class="shadow-lg mb-4"
/>
```

**Output**:

```html
<div class="small-box text-bg-danger shadow-lg mb-4">
    <div class="inner">
        <h3>99</h3>
        <p>Important Alerts</p>
    </div>
    <c-icon name="exclamation-triangle-fill" class="small-box-icon" />
</div>
```

### Example 5: Default Background

**Input**:

```django
<c-small-box
    heading="0"
    text="Pending Items"
    icon="hourglass"
/>
```

**Output**:

```html
<div class="small-box">
    <div class="inner">
        <h3>0</h3>
        <p>Pending Items</p>
    </div>
    <c-icon name="hourglass" class="small-box-icon" />
</div>
```

## Error Handling

### Missing Required Attributes

Component renders with degraded experience:

- Missing `heading`: `<h3>` renders empty
- Missing `text`: `<p>` renders empty
- Missing `icon`: c-icon component renders without icon

### Invalid Attribute Values

- Invalid `variant`: Renders with `text-bg-{invalid-value}` class (may not have styling)
- Invalid `link`: May cause 404 or broken link
- Empty `link_text`: Link renders with default "More info"

## CSS Dependencies

### Required AdminLTE 4 Classes

- `.small-box`
- `.inner`
- `.small-box-icon`
- `.small-box-footer`

### Required Bootstrap 5 Classes

- `.text-bg-{variant}`
- `.link-light`
- `.link-underline-opacity-0`
- `.link-underline-opacity-50-hover`

### Required Icon Component

- c-icon component for icon rendering

## Icon Implementation Note

Small boxes use **SVG symbol references** instead of icon fonts:

```html
<svg class="small-box-icon">
    <use xlink:href="#icon-name" />
</svg>
```

This requires an SVG sprite to be included in the page with corresponding symbol definitions. AdminLTE 4 typically provides this sprite, or it can be generated from Bootstrap Icons.

## Testing Requirements

### Unit Tests Required

1. ✅ Renders with all required attributes
2. ✅ Renders with background variant classes correctly
3. ✅ Renders footer link when link provided
4. ✅ Uses default "More info" when link provided but link_text omitted
5. ✅ Uses custom link_text when provided
6. ✅ Omits footer when link not provided
7. ✅ Applies custom classes via class attribute
8. ✅ Hides icon from screen readers with aria-hidden
9. ✅ Uses proper semantic HTML (h3, p, a tags)

### Integration Tests Required

1. ✅ Works within Bootstrap grid layouts
2. ✅ Multiple small boxes render independently
3. ✅ CSS classes resolve correctly with AdminLTE 4 CSS
4. ✅ Links are keyboard navigable

## Known Limitations

1. **Icon Format**: Uses SVG symbol references, not icon fonts. Requires SVG sprite to be present in page.
2. **Heading Level**: Always uses `<h3>`. If different heading level needed, requires wrapper adjustment.

## Version History

- **v1.0** (Phase 1): Initial contract definition
- **v1.1** (2026-01-05): Changed `bg` attribute to `variant` for consistency; added `link_icon` attribute for customizable footer icon
