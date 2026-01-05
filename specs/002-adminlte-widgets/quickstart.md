# Quick Start Guide: AdminLTE 4 Widget Components

**Phase**: 1 - Design & Contracts
**Date**: January 5, 2026
**Feature**: [spec.md](./spec.md)

## Prerequisites

Ensure your Django project includes:

- `django-cotton` installed and configured
- `'mvp'` in `INSTALLED_APPS`
- `'django_cotton.apps.SimpleAppConfig'` in `INSTALLED_APPS`
- `django-easy-icons` installed and configured (provides c-icon component)
- AdminLTE 4 CSS in base template (via CDN or local)
- Bootstrap 5.3 CSS in base template

## Installation

Components are included with the `django-mvp` package. No additional installation required.

## Basic Usage

### Info Box

Display metrics and statistics with optional progress indicators.

**Simple metric:**

```html
<c-info-box
    icon="gear-fill"
    text="CPU Traffic"
    number="10%"
/>
```

**With color variant:**

```html
<c-info-box
    icon="bag-check-fill"
    text="Sales"
    number="13,648"
    variant="success"
/>
```

**With progress bar:**

```html
<c-info-box
    icon="download"
    text="Downloads"
    number="114,381"
    variant="info"
    progress="70"
    description="70% Increase in 30 Days"
/>
```

**With box fill mode (entire box colored):**

```html
<c-info-box
    icon="flag-fill"
    text="Bookmarks"
    number="41,410"
    variant="warning"
    fill="box"
/>
```

### Small Box

Dashboard summary widgets with large numbers and optional footer links.

**Basic small box:**

```html
<c-small-box
    heading="150"
    text="New Orders"
    icon="cart-fill"
    variant="primary"
/>
```

**With footer link:**

```html
<c-small-box
    heading="53%"
    text="Bounce Rate"
    icon="graph-up"
    variant="warning"
    link="/analytics/"
/>
```

**Custom link text:**

```html
<c-small-box
    heading="44"
    text="User Registrations"
    icon="person-fill-add"
    variant="success"
    link="/users/"
    link_text="View all users"
/>
```

### Card

Flexible container for grouped content with header, body, footer, and tools.

**Basic card:**

```html
<c-card title="Monthly Revenue">
    <p>Revenue data goes here...</p>
</c-card>
```

**Card with icon:**

```html
<c-card title="Sales Report" icon="graph-up-arrow">
    <p>Sales charts and data...</p>
</c-card>
```

**Card with variant styling:**

```html
<c-card
    title="Important Notice"
    variant="warning"
    fill="outline"
>
    <p>This is an important warning message.</p>
</c-card>
```

**Card with footer:**

```html
<c-card title="User Profile" footer_class="text-end">
    <p>User details and information...</p>
    <c-slot name="footer">
        <button class="btn btn-primary">Save</button>
        <button class="btn btn-secondary">Cancel</button>
    </c-slot>
</c-card>
```

**Card with custom tools:**

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

**Collapsible card:**

```html
<c-card
    title="Expandable Section"
    collapsible
    collapsed
>
    <p>This content is initially hidden.</p>
</c-card>
```

**Card with fill options:**

```html
<!-- Outline (default) - colored border only -->
<c-card title="Outline Card" variant="primary" fill="outline">
    <p>Card with colored border.</p>
</c-card>

<!-- Card - full card background -->
<c-card title="Filled Card" variant="danger" fill="card">
    <p>Card with full background color.</p>
</c-card>

<!-- Compact - zero body padding for tables/maps -->
<c-card title="Sales Data" icon="table" compact>
    <table class="table mb-0">
        <thead><tr><th>Product</th><th>Sales</th></tr></thead>
        <tbody><tr><td>Widget</td><td>$1000</td></tr></tbody>
    </table>
</c-card>
```

## Common Patterns

### Dashboard Layout (from US-001)

```html
<div class="row">
    <div class="col-md-3">
        <c-info-box
            icon="bag-check-fill"
            text="Sales"
            number="13,648"
            variant="success"
        />
    </div>
    <div class="col-md-3">
        <c-info-box
            icon="download"
            text="Downloads"
            number="114,381"
            variant="info"
        />
    </div>
    <div class="col-md-3">
        <c-small-box
            heading="150"
            text="New Orders"
            icon="cart-fill"
            variant="primary"
            link="/orders/"
        />
    </div>
    <div class="col-md-3">
        <c-small-box
            heading="53%"
            text="Bounce Rate"
            icon="graph-up"
            variant="warning"
        />
    </div>
</div>
```

### Card Grid Layout

```html
<div class="row">
    <div class="col-md-6">
        <c-card title="Recent Activity" icon="clock-history">
            <ul class="list-group list-group-flush">
                <li class="list-group-item">Activity 1</li>
                <li class="list-group-item">Activity 2</li>
            </ul>
        </c-card>
    </div>
    <div class="col-md-6">
        <c-card
            title="Sales Chart"
            icon="graph-up-arrow"
            variant="primary"
            fill="header"
        >
            <canvas id="salesChart"></canvas>
        </c-card>
    </div>
</div>
```

### Progress Tracking (from US-004)

```html
<div class="row">
    <div class="col-md-4">
        <c-info-box
            icon="list-check"
            text="Tasks Complete"
            number="8/12"
            variant="success"
            progress="67"
            description="67% Complete"
        />
    </div>
    <div class="col-md-4">
        <c-info-box
            icon="hourglass-split"
            text="In Progress"
            number="3/12"
            variant="warning"
            progress="25"
            description="25% of Total"
        />
    </div>
    <div class="col-md-4">
        <c-info-box
            icon="clipboard-x"
            text="Not Started"
            number="1/12"
            progress="8"
            description="8% Remaining"
        />
    </div>
</div>
```

## Styling Customization

### Adding Custom Classes

All components accept a `class` attribute for additional styling:

```html
<c-info-box
    icon="star-fill"
    text="Featured Item"
    number="99"
    class="mb-3 shadow-sm"
/>

<c-small-box
    heading="42"
    text="The Answer"
    icon="lightbulb"
    variant="info"
    class="rounded-3"
/>

<c-card
    title="Custom Styled Card"
    class="border-3 border-primary"
>
    <p>Card content</p>
</c-card>
```

### Using Bootstrap Utilities

Components work seamlessly with Bootstrap 5 utility classes:

```html
<!-- Spacing -->
<c-info-box ... class="mb-4" />

<!-- Shadows -->
<c-card ... class="shadow-lg" />

<!-- Borders -->
<c-small-box ... class="border border-2" />

<!-- Display -->
<c-card ... class="d-none d-md-block" />
```

## Color Variants

### Available Variants

All components support these color variants:

- `primary` - Blue
- `success` - Green
- `warning` - Yellow/Orange
- `danger` - Red
- `info` - Light Blue
- `secondary` - Gray
- `default` - Default/neutral styling (applied when variant not specified)

### Variant Usage

**Info Box**: Use `variant` attribute for background color

```html
<c-info-box variant="primary" ... />
```

**Small Box**: Use `variant` attribute for background color

```html
<c-small-box variant="success" ... />
```

**Card**: Use `variant` attribute combined with `fill` attribute

```html
<c-card variant="warning" fill="header" ... />
```

## Accessibility

All components include appropriate ARIA attributes:

- Info box progress bars include `role="progressbar"` and `aria-value*` attributes
- Card collapse buttons include `aria-expanded` and `aria-label` attributes
- Decorative icons are marked with `aria-hidden="true"`

Screen readers will properly announce:

- Metric values in info boxes
- Progress percentages and descriptions
- Card expand/collapse state
- Link destinations in small boxes

## Browser Support

Components require:

- Modern browsers with CSS Grid support
- JavaScript enabled (for card collapse functionality)
- AdminLTE 4 CSS loaded
- Bootstrap 5.3+ CSS loaded
- django-easy-icons configured (c-icon component)

## Next Steps

- Review [data-model.md](./data-model.md) for complete attribute reference
- Check [contracts/](./contracts/) for detailed API contracts
- See [spec.md](./spec.md) for full feature requirements
