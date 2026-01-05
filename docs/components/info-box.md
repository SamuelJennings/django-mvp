# Info Box Component

**Component**: `<c-info-box>`
**File**: `mvp/templates/cotton/info_box.html`
**Status**: ✅ Implemented

## Overview

The info box component displays metrics and statistics with optional icons, progress bars, and various color schemes. Based on AdminLTE 4's info box widget.

## Usage

### Basic Usage

```django
<c-info-box
    icon="settings"
    text="CPU Traffic"
    number="10%"
/>
```

### With Color Variant

```django
<c-info-box
    icon="box-seam"
    text="Sales"
    number="13,648"
    variant="success"
/>
```

### With Progress Bar

```django
<c-info-box
    icon="add"
    text="Downloads"
    number="114,381"
    variant="info"
    progress="70"
    description="70% Increase in 30 Days"
/>
```

### With Box Fill Mode

```django
<c-info-box
    icon="book"
    text="Bookmarks"
    number="41,410"
    variant="warning"
    fill="box"
/>
```

### With Custom Classes

```django
<c-info-box
    icon="settings"
    text="CPU Traffic"
    number="10%"
    class="mb-3 shadow-lg"
/>
```

## Attributes

### Required

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `icon` | string | Icon name (from easy_icons configuration) | `"settings"` |
| `text` | string | Primary label text | `"CPU Traffic"` |
| `number` | string | Metric/statistic value | `"10%"` |

### Optional

| Attribute | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `variant` | string | `"default"` | Color variant (primary, success, warning, danger, info, secondary, default) | `"success"` |
| `fill` | string | `"icon"` | Fill mode: "icon" (colors icon only) or "box" (colors entire box) | `"box"` |
| `progress` | integer | `""` | Progress bar percentage (0-100) | `"70"` |
| `description` | string | `""` | Progress bar description text | `"70% Increase"` |
| `icon_class` | string | `""` | Additional classes for icon | `"fs-4"` |
| `class` | string | `""` | Additional CSS classes | `"mb-3 shadow"` |

## Color Variants

The `variant` attribute accepts Bootstrap color variants:

- `primary` - Primary brand color
- `success` - Success/positive state (green)
- `warning` - Warning state (yellow/orange)
- `danger` - Error/danger state (red)
- `info` - Informational state (blue)
- `secondary` - Secondary/muted color (gray)
- `default` - No color applied (inherits parent styles)

## Fill Modes

The `fill` attribute controls where the color variant is applied:

### Icon Fill (Default)

With `fill="icon"` (default), only the icon span receives the colored background:

```django
<c-info-box
    icon="heart"
    text="Likes"
    number="41,410"
    variant="danger"
    fill="icon"
/>
```

### Box Fill

With `fill="box"`, the entire info box receives the colored background:

```django
<c-info-box
    icon="book"
    text="Bookmarks"
    number="500"
    variant="primary"
    fill="box"
/>
```

## Progress Bars

Add a progress indicator with `progress` (0-100) and optional `description`:

```django
<c-info-box
    icon="add"
    text="Downloads"
    number="114,381"
    progress="70"
    description="70% Increase in 30 Days"
/>
```

Progress bars are rendered using the `<c-progress>` component, which automatically includes proper ARIA attributes for accessibility:

- `role="progressbar"`
- `aria-valuenow="{{ progress }}"`
- `aria-valuemin="0"`
- `aria-valuemax="100"`

When using icon fill mode, the progress bar inherits the variant color.

## Icons

Icons are rendered via the `c-icon` component from django-easy-icons. Use icon names configured in your `EASY_ICONS` settings:

```python
EASY_ICONS = {
    "default": {
        "icons": {
            "settings": "bi bi-gear",
            "download": "bi bi-download",
            # ... more icons
        }
    }
}
```

Common icon names:

- `settings`, `add`, `search`, `filter`
- `book`, `heart`, `briefcase`, `laptop`
- `box-seam`, `folder`, `newspaper`

The icon is automatically marked as decorative with `aria-hidden="true"`.

## Accessibility

### ARIA Attributes

- Icon span has `aria-hidden="true"` (decorative)
- Progress bars have complete ARIA attributes:
  - `role="progressbar"`
  - `aria-valuenow` (current value)
  - `aria-valuemin="0"`
  - `aria-valuemax="100"`

### Screen Readers

- Icon is hidden from screen readers (decorative)
- Text and number are announced as-is
- Progress bar announces current value and range
- Description provides additional context

### Keyboard Navigation

No interactive elements - purely informational display.

## Examples

### Dashboard Metrics Grid

```django
<div class="row">
    <div class="col-md-3">
        <c-info-box
            icon="box-seam"
            text="New Orders"
            number="150"
            variant="primary"
        />
    </div>
    <div class="col-md-3">
        <c-info-box
            icon="heart"
            text="Likes"
            number="53"
            variant="danger"
        />
    </div>
    <div class="col-md-3">
        <c-info-box
            icon="briefcase"
            text="Sales"
            number="44"
            variant="success"
        />
    </div>
    <div class="col-md-3">
        <c-info-box
            icon="person"
            text="New Members"
            number="65"
            variant="warning"
        />
    </div>
</div>
```

### Progress Tracking

```django
<div class="row">
    <div class="col-md-6">
        <c-info-box
            icon="add"
            text="Downloads"
            number="114,381"
            variant="info"
            progress="70"
            description="70% Increase in 30 Days"
        />
    </div>
    <div class="col-md-6">
        <c-info-box
            icon="settings"
            text="Processors"
            number="41,410"
            variant="warning"
            fill="box"
            progress="50"
            description="Half capacity"
        />
    </div>
</div>
```

## Related Components

- [Small Box](./small-box.md) - Larger dashboard summary widgets
- [Card](./card.md) - Flexible content containers

## Browser Support

Compatible with all modern browsers supporting Bootstrap 5.3 and AdminLTE 4.

## See Also

- [AdminLTE Info Box Documentation](https://adminlte.io/themes/v3/pages/widgets.html)
- [Bootstrap 5.3 Colors](https://getbootstrap.com/docs/5.3/utilities/colors/)
- [Bootstrap 5.3 Progress](https://getbootstrap.com/docs/5.3/components/progress/)
