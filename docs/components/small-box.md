# Small Box Component

**Component**: `<c-small-box>`
**File**: `mvp/templates/cotton/small_box.html`
**Status**: ✅ Implemented

## Overview

The small box component displays prominent dashboard metrics with large numbers, descriptive text, icons, and optional footer links. Based on AdminLTE 4's small box widget.

## Usage

### Basic Usage

```django
<c-small-box
    heading="150"
    text="New Orders"
    icon="box-seam"
    variant="primary"
/>
```

### With Footer Link (Default Text)

```django
<c-small-box
    heading="53%"
    text="Bounce Rate"
    icon="settings"
    variant="warning"
    link="/analytics/"
/>
```

### With Custom Link Text

```django
<c-small-box
    heading="44"
    text="User Registrations"
    icon="person"
    variant="success"
    link="/users/"
    link_text="View all users"
/>
```

### With Custom Classes

```django
<c-small-box
    heading="65"
    text="Unique Visitors"
    icon="eye"
    variant="info"
    class="mb-3 shadow-lg"
/>
```

## Attributes

### Required

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `heading` | string | Main metric/number display | `"150"` |
| `text` | string | Description label | `"New Orders"` |
| `icon` | string | Icon name (from easy_icons configuration) | `"box-seam"` |

### Optional

| Attribute | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `variant` | string | `"default"` | Background color variant (primary, success, warning, danger, info, secondary, default) | `"primary"` |
| `link` | string | `""` | Footer link URL | `"/orders/"` |
| `link_text` | string | `"More info"` | Footer link text | `"View all orders"` |
| `link_icon` | string | `"link"` | Footer link icon name | `"arrow-right"` |
| `icon_class` | string | `""` | Additional classes for icon | `"fs-4"` |
| `class` | string | `""` | Additional CSS classes | `"mb-3 shadow"` |

## Color Backgrounds

### Standard Background Colors (via `variant` attribute)

Applies Bootstrap's `text-bg-*` classes:

- `primary` - Primary brand color (blue)
- `success` - Success state (green)
- `warning` - Warning state (yellow/orange)
- `danger` - Danger state (red)
- `info` - Informational state (cyan/blue)
- `secondary` - Secondary color (gray)
- `default` - No background color applied

### Examples

```django
<!-- Primary blue background -->
<c-small-box
    heading="150"
    text="New Orders"
    icon="box-seam"
    variant="primary"
/>

<!-- Success green background -->
<c-small-box
    heading="53"
    text="Bounce Rate"
    icon="settings"
    variant="success"
/>

<!-- Warning orange background -->
<c-small-box
    heading="44"
    text="User Registrations"
    icon="person"
    variant="warning"
/>
```

## Footer Links

Add a footer link with the `link` attribute. By default, it displays "More info" with an arrow icon:

```django
<c-small-box
    heading="150"
    text="New Orders"
    icon="box-seam"
    variant="primary"
    link="/orders/"
/>
```

Customize the link text with `link_text`:

```django
<c-small-box
    heading="44"
    text="User Registrations"
    icon="person"
    variant="success"
    link="/users/"
    link_text="View all users"
/>
```

The footer link includes:

- Light colored text (`link-light`)
- No underline by default
- Underline on hover (50% opacity)
- Arrow right icon

## Icons

Icons are rendered via the `c-icon` component from django-easy-icons. Use icon names configured in your `EASY_ICONS` settings:

```python
EASY_ICONS = {
    "default": {
        "icons": {
            "box-seam": "bi bi-box-seam",
            "settings": "bi bi-gear",
            "person": "bi bi-person",
            # ... more icons
        }
    }
}
```

Common icon names:

- `box-seam`, `settings`, `person`, `eye`
- `heart`, `briefcase`, `laptop`, `folder`
- `add`, `search`, `filter`, `calendar`

The icon is automatically positioned and styled with the `small-box-icon` class.

## Accessibility

### Semantic HTML

- `<h3>` for heading (proper heading hierarchy)
- `<p>` for descriptive text
- `<a>` for footer link (keyboard navigable)

### Screen Readers

- Icon is handled by c-icon component with appropriate ARIA attributes
- Heading is announced as heading level 3
- Text is read as paragraph content
- Link announces destination and link text

### Keyboard Navigation

- Footer link is fully keyboard accessible
- Standard tab navigation works correctly

## Examples

### Dashboard Summary Row

```django
<div class="row">
    <div class="col-lg-3 col-6">
        <c-small-box
            heading="150"
            text="New Orders"
            icon="box-seam"
            variant="primary"
            link="/orders/"
        />
    </div>
    <div class="col-lg-3 col-6">
        <c-small-box
            heading="53%"
            text="Bounce Rate"
            icon="settings"
            variant="success"
        />
    </div>
    <div class="col-lg-3 col-6">
        <c-small-box
            heading="44"
            text="User Registrations"
            icon="person"
            variant="warning"
            link="/users/"
            link_text="View all users"
        />
    </div>
    <div class="col-lg-3 col-6">
        <c-small-box
            heading="65"
            text="Unique Visitors"
            icon="eye"
            variant="danger"
        />
    </div>
</div>
```

### With Custom Styling

```django
<div class="row">
    <div class="col-md-4">
        <c-small-box
            heading="$9,842"
            text="Total Revenue"
            icon="briefcase"
            variant="success"
            link="/revenue/"
            link_text="Revenue report"
            class="shadow-lg mb-3"
        />
    </div>
</div>
```

### Without Footer Links

```django
<div class="row">
    <div class="col-md-3">
        <c-small-box
            heading="93.5%"
            text="Server Uptime"
            icon="settings"
            variant="info"
        />
    </div>
</div>
```

## Differences from Info Box

Small boxes are designed for prominent display of key metrics:

- **Larger appearance**: More visual weight with bigger numbers
- **Solid backgrounds**: Always uses colored backgrounds (not optional)
- **Footer links**: Built-in support for "more info" links
- **No progress bars**: Focused on single metric display
- **Simpler layout**: Less information density

Use small boxes for:

- Dashboard summary metrics
- Key performance indicators (KPIs)
- High-level statistics

Use info boxes for:

- Detailed metrics with progress tracking
- Statistics requiring additional context
- Multiple related data points

## Related Components

- [Info Box](./info-box.md) - Metric display with progress bars
- [Card](./card.md) - Flexible content containers

## Browser Support

Compatible with all modern browsers supporting Bootstrap 5.3 and AdminLTE 4.

## See Also

- [AdminLTE Small Box Documentation](https://adminlte.io/themes/v3/pages/widgets.html)
- [Bootstrap 5.3 Colors](https://getbootstrap.com/docs/5.3/utilities/colors/)

