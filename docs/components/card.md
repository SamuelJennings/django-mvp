# Card Component

**Component**: `<c-card>`  
**File**: `mvp/templates/cotton/card.html`  
**Status**: ✅ Implemented

## Overview

The card component provides a flexible container for content with optional header, footer, tools, and collapse functionality. Based on AdminLTE 4's card widget with Bootstrap 5.3 styling.

## Usage

### Basic Card with Title and Body

```django
<c-card title="Sample Card">
    <p>This is the card body content.</p>
</c-card>
```

### Card with Icon in Header

```django
<c-card title="Settings" icon="settings">
    <p>Configure your application settings here.</p>
</c-card>
```

### Card with Variant and Fill

```django
<!-- Outline style -->
<c-card title="Primary Card" variant="primary" fill="outline">
    <p>Outlined card with primary color border.</p>
</c-card>

<!-- Header fill style -->
<c-card title="Success Header" variant="success" fill="header">
    <p>Card with colored header background.</p>
</c-card>

<!-- Full card fill style -->
<c-card title="Warning Card" variant="warning" fill="card">
    <p>Entire card has colored background.</p>
</c-card>
```

### Card with Footer

```django
<c-card title="Form Card">
    <p>Enter your information below.</p>
    
    <c-slot name="footer">
        <button class="btn btn-primary">Save</button>
        <button class="btn btn-secondary">Cancel</button>
    </c-slot>
</c-card>
```

### Card with Custom Tools

```django
<c-card title="Dashboard Stats">
    <c-slot name="tools">
        <button type="button" class="btn btn-tool">
            <c-icon name="settings" />
        </button>
        <button type="button" class="btn btn-tool">
            <c-icon name="search" />
        </button>
    </c-slot>
    
    <p>Statistics content here.</p>
</c-card>
```

### Collapsible Card

```django
<c-card title="Collapsible Card" collapsed="true">
    <p>This content is initially hidden and can be toggled.</p>
</c-card>
```

### Simple Card (No Header)

```django
<c-card>
    <p>Simple card with just body content, no header.</p>
</c-card>
```

## Attributes

### Required Attributes

None. All attributes are optional.

### Optional Attributes

| Attribute | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `title` | string | `""` | Card header title | `"Monthly Revenue"` |
| `icon` | string | `""` | Icon name (from easy_icons configuration) in header | `"graph-up-arrow"` |
| `icon_class` | string | `""` | Additional classes for icon | `"fs-5"` |
| `variant` | string | `"default"` | Color variant (primary, success, warning, danger, info, secondary, default) | `"primary"` |
| `fill` | string | `"outline"` | Fill style (outline, header, card) | `"header"` |
| `collapsed` | boolean | `""` | Initial collapsed state (presence = true) | `collapsed="true"` |
| `class_` | string | `""` | Additional CSS classes | `"mb-3 shadow-lg"` |

**Note**: The `class_` attribute uses an underscore to avoid Python/Django reserved keyword conflicts.

## Slots

### Default Slot (unnamed)

The main body content of the card.

```django
<c-card title="Example">
    <p>This goes in the card body.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</c-card>
```

### Named Slot: `tools`

Custom tool buttons in the card header. Only renders if `title` is provided.

```django
<c-card title="Card with Tools">
    <c-slot name="tools">
        <button type="button" class="btn btn-tool">
            <c-icon name="filter" />
        </button>
    </c-slot>
    
    <p>Body content</p>
</c-card>
```

### Named Slot: `footer`

Footer content area. Only renders if content is provided.

```django
<c-card title="Card with Footer">
    <p>Body content</p>
    
    <c-slot name="footer">
        <button class="btn btn-primary">Submit</button>
    </c-slot>
</c-card>
```

## Variant and Fill Combinations

### Outline Fill (default)

Applies a colored border to the card:

```django
<c-card title="Primary Outline" variant="primary" fill="outline">
    <p>Card with primary colored border.</p>
</c-card>
```

**CSS Classes Applied**: `card card-outline card-primary border-primary`

### Header Fill

Colors the card header background:

```django
<c-card title="Success Header" variant="success" fill="header">
    <p>Card with green header.</p>
</c-card>
```

**CSS Classes Applied**:
- Card: `card card-outline card-success`
- Header: `card-header text-bg-success`

### Card Fill

Colors the entire card background:

```django
<c-card title="Warning Card" variant="warning" fill="card">
    <p>Entire card has warning color.</p>
</c-card>
```

**CSS Classes Applied**: `card text-bg-warning`

## Collapse Functionality

Cards can be collapsible using the `collapsed` attribute. When enabled, a collapse button is automatically added to the card tools area.

```django
<c-card title="Collapsible Card" collapsed="true">
    <p>This content starts hidden and can be toggled.</p>
</c-card>
```

The collapse button:
- Automatically added to `.card-tools` when `collapsed` attribute is present
- Uses AdminLTE's `data-lte-toggle="card-collapse"` functionality
- Displays plus/minus icons to indicate collapse state
- Includes proper ARIA attributes (`aria-expanded`, `aria-label`)

**ARIA Attributes**:
- `aria-expanded="false"` - Indicates collapsed state
- `aria-label="Toggle card"` - Describes button action

## Icons

Icons are rendered via the `c-icon` component from django-easy-icons. Use icon names configured in your `EASY_ICONS` settings:

```python
EASY_ICONS = {
    "default": {
        "icons": {
            "settings": "bi bi-gear",
            "search": "bi bi-search",
            "graph-up-arrow": "bi bi-graph-up-arrow",
            "plus": "bi bi-plus-lg",
            "dash": "bi bi-dash-lg",
            # ... more icons
        }
    }
}
```

Common icon names:
- `settings`, `search`, `filter`, `calendar`
- `plus`, `dash` (used for collapse buttons)
- `graph-up-arrow`, `briefcase`, `laptop`

## Accessibility

### Semantic HTML

- `<h3>` for card title (proper heading hierarchy)
- `<button>` for interactive elements (tools, collapse)
- Proper `<div>` structure for card sections

### Screen Readers

- Icon is handled by c-icon component with appropriate ARIA attributes
- Collapse button has `aria-label="Toggle card"`
- Collapsed state indicated with `aria-expanded` attribute
- Card title announced as heading level 3

### Keyboard Navigation

- All tool buttons are keyboard accessible
- Standard tab navigation works correctly
- Collapse functionality accessible via keyboard

## Examples

### Dashboard Card Grid

```django
<div class="row">
    <div class="col-md-6">
        <c-card title="Revenue" icon="briefcase" variant="success" fill="header">
            <h4>$45,823</h4>
            <p class="text-muted">This month</p>
            
            <c-slot name="footer">
                <a href="/reports/revenue/" class="btn btn-sm btn-success">View Report</a>
            </c-slot>
        </c-card>
    </div>
    
    <div class="col-md-6">
        <c-card title="Orders" icon="box-seam" variant="primary" fill="header">
            <h4>1,234</h4>
            <p class="text-muted">This month</p>
            
            <c-slot name="footer">
                <a href="/orders/" class="btn btn-sm btn-primary">View Orders</a>
            </c-slot>
        </c-card>
    </div>
</div>
```

### Collapsible Settings Card

```django
<c-card title="Advanced Settings" icon="settings" collapsed="true" class_="mb-3">
    <div class="form-group">
        <label>API Key</label>
        <input type="text" class="form-control" />
    </div>
    <div class="form-group">
        <label>Webhook URL</label>
        <input type="text" class="form-control" />
    </div>
    
    <c-slot name="footer">
        <button class="btn btn-primary">Save Settings</button>
    </c-slot>
</c-card>
```

### Card with Custom Tools

```django
<c-card title="Data Table" variant="info" fill="outline">
    <c-slot name="tools">
        <button type="button" class="btn btn-tool" title="Filter">
            <c-icon name="filter" />
        </button>
        <button type="button" class="btn btn-tool" title="Export">
            <c-icon name="download" />
        </button>
        <button type="button" class="btn btn-tool" title="Refresh">
            <c-icon name="arrow-clockwise" />
        </button>
    </c-slot>
    
    <table class="table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <!-- Table rows -->
        </tbody>
    </table>
</c-card>
```

### Simple Content Card

```django
<div class="row">
    <div class="col-md-4">
        <c-card class_="text-center">
            <c-icon name="briefcase" class="fs-1 text-primary mb-3" />
            <h5>Business</h5>
            <p>Professional tools for your organization.</p>
        </c-card>
    </div>
    <div class="col-md-4">
        <c-card class_="text-center">
            <c-icon name="person" class="fs-1 text-success mb-3" />
            <h5>Personal</h5>
            <p>Manage your personal projects.</p>
        </c-card>
    </div>
    <div class="col-md-4">
        <c-card class_="text-center">
            <c-icon name="heart" class="fs-1 text-danger mb-3" />
            <h5>Favorites</h5>
            <p>Quick access to starred items.</p>
        </c-card>
    </div>
</div>
```

## Styling Tips

### Custom Spacing

```django
<c-card title="Spaced Card" class_="mb-4 mt-3">
    <p>Card with custom margins.</p>
</c-card>
```

### Shadow Effects

```django
<c-card title="Elevated Card" class_="shadow-lg">
    <p>Card with large shadow for elevation effect.</p>
</c-card>
```

### Full Height Cards

```django
<div class="row">
    <div class="col-md-6">
        <c-card title="Card 1" class_="h-100">
            <p>Content that fills available height.</p>
        </c-card>
    </div>
    <div class="col-md-6">
        <c-card title="Card 2" class_="h-100">
            <p>Both cards have equal height.</p>
        </c-card>
    </div>
</div>
```

## Differences from Other Components

### vs Info Box

- **Card**: Flexible container for any content type with header/footer
- **Info Box**: Specialized for displaying metrics with icons and progress

### vs Small Box

- **Card**: Versatile with slots, tools, collapse functionality
- **Small Box**: Fixed layout for prominent metric display with footer links

Use cards for:
- Forms and data entry
- Tables and data display
- Settings panels
- Content sections with headers and footers
- Any structured content needing a container

## Related Components

- [Info Box](./info-box.md) - Metric display with progress bars
- [Small Box](./small-box.md) - Prominent KPI widgets

## Browser Support

Compatible with all modern browsers supporting Bootstrap 5.3 and AdminLTE 4.

## See Also

- [AdminLTE Card Documentation](https://adminlte.io/themes/v3/pages/widgets.html)
- [Bootstrap 5.3 Card Component](https://getbootstrap.com/docs/5.3/components/card/)
