# Creating Custom Navbar Widgets

Django MVP provides a flexible custom widget base template that allows you to quickly create application-specific widgets following AdminLTE and Bootstrap 5 patterns. This guide shows you how to create custom widgets for tasks, alerts, or any other application-specific needs.

## Overview

The custom widget component (`navbar/custom_widget.html`) provides:

- **Icon Support**: Use any Bootstrap Icon
- **Badge Counter**: Optional badge with customizable colors and "99+" overflow
- **Dropdown Slot**: Add custom HTML content via the `children` slot
- **AdminLTE Styling**: Consistent styling with AdminLTE navbar components
- **Accessibility**: Proper ARIA labels and keyboard navigation

## Basic Usage

```django
<c-navbar.custom_widget
    icon="bi-check2-square"
    dropdown_id="tasks-dropdown"
    badge_count="5"
    badge_color="warning">
    <div class="dropdown-item">
        <p>Your custom content here</p>
    </div>
</c-navbar.custom_widget>
```

## Component Props

### Required Props

- **`icon`** (string): Bootstrap Icon class name (e.g., `"bi-check2-square"`, `"bi-bell"`, `"bi-exclamation-triangle"`)
- **`dropdown_id`** (string): Unique ID for the dropdown menu (e.g., `"tasks-dropdown"`)

### Optional Props

- **`badge_count`** (integer, default: `0`): Number to display in badge. Set to `0` to hide badge.
- **`badge_color`** (string, default: `"danger"`): Bootstrap badge color (`"danger"`, `"warning"`, `"info"`, `"success"`, `"primary"`, `"secondary"`)
- **`children`** (HTML): Custom dropdown content passed via slot
- **`class`** (string): Additional CSS classes for the widget container

## Badge Behavior

The badge automatically handles different scenarios:

- **`badge_count = 0`**: Badge is hidden
- **`badge_count = 1-99`**: Shows exact count
- **`badge_count > 99`**: Shows "99+"
- **No `badge_count` provided**: Badge is hidden

## Example 1: Tasks Widget

Create a tasks widget showing incomplete tasks with priority indicators:

```django
{# In your template #}
<c-navbar.custom_widget
    icon="bi-check2-square"
    dropdown_id="tasks-dropdown"
    badge_count="{{ tasks.count }}"
    badge_color="warning">

    {# Dropdown Header #}
    <div class="dropdown-header">
        You have {{ tasks.count }} pending {{ tasks.count|pluralize:"task,tasks" }}
    </div>

    {# Task List #}
    <div class="dropdown-divider"></div>
    {% for task in tasks|slice:":5" %}
        <a href="{% url 'task-detail' task.id %}" class="dropdown-item">
            <div class="d-flex align-items-center">
                {% if task.priority == 'high' %}
                    <span class="badge text-bg-danger me-2">!</span>
                {% elif task.priority == 'medium' %}
                    <span class="badge text-bg-warning me-2">!</span>
                {% endif %}
                <div class="text-truncate">
                    <strong>{{ task.title }}</strong>
                    <div class="small text-muted">Due: {{ task.due_date|date:"M d" }}</div>
                </div>
            </div>
        </a>
        {% if not forloop.last %}
            <div class="dropdown-divider"></div>
        {% endif %}
    {% endfor %}

    {# Footer #}
    <div class="dropdown-divider"></div>
    <a href="{% url 'tasks-list' %}" class="dropdown-item dropdown-footer">
        See All Tasks
    </a>
</c-navbar.custom_widget>
```

**View Context:**

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tasks'] = Task.objects.filter(
        user=self.request.user,
        completed=False
    ).order_by('due_date')[:5]
    return context
```

## Example 2: System Alerts Widget

Create an alerts widget showing system status and warnings:

```django
{# In your template #}
<c-navbar.custom_widget
    icon="bi-exclamation-triangle"
    dropdown_id="alerts-dropdown"
    badge_count="{{ alerts.count }}"
    badge_color="danger">

    {# Dropdown Header #}
    <div class="dropdown-header">
        {% if alerts.count > 0 %}
            {{ alerts.count }} System {{ alerts.count|pluralize:"Alert,Alerts" }}
        {% else %}
            No Alerts
        {% endif %}
    </div>

    {# Alert List #}
    <div class="dropdown-divider"></div>
    {% for alert in alerts|slice:":5" %}
        <div class="dropdown-item">
            <div class="d-flex align-items-start">
                {# Alert Icon #}
                <div class="me-2">
                    {% if alert.severity == 'critical' %}
                        <i class="bi bi-x-circle text-danger"></i>
                    {% elif alert.severity == 'warning' %}
                        <i class="bi bi-exclamation-triangle text-warning"></i>
                    {% else %}
                        <i class="bi bi-info-circle text-info"></i>
                    {% endif %}
                </div>

                {# Alert Content #}
                <div class="flex-grow-1">
                    <strong>{{ alert.title }}</strong>
                    <div class="small text-muted">{{ alert.message|truncatewords:15 }}</div>
                    <div class="small text-muted">
                        <i class="bi bi-clock"></i> {{ alert.created_at|timesince }} ago
                    </div>
                </div>
            </div>
        </div>
        {% if not forloop.last %}
            <div class="dropdown-divider"></div>
        {% endif %}
    {% empty %}
        <div class="dropdown-item text-center text-muted">
            No alerts
        </div>
    {% endfor %}

    {# Footer #}
    <div class="dropdown-divider"></div>
    <a href="{% url 'alerts-list' %}" class="dropdown-item dropdown-footer">
        View All Alerts
    </a>
</c-navbar.custom_widget>
```

**View Context:**

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['alerts'] = SystemAlert.objects.filter(
        acknowledged=False
    ).order_by('-created_at')[:5]
    return context
```

## Example 3: Shopping Cart Widget

Create a shopping cart widget showing item count and cart preview:

```django
{# In your template #}
<c-navbar.custom_widget
    icon="bi-cart"
    dropdown_id="cart-dropdown"
    badge_count="{{ cart.item_count }}"
    badge_color="success">

    {# Cart Header #}
    <div class="dropdown-header">
        {% if cart.item_count > 0 %}
            {{ cart.item_count }} {{ cart.item_count|pluralize:"item,items" }} in cart
        {% else %}
            Your cart is empty
        {% endif %}
    </div>

    {# Cart Items #}
    {% if cart.items %}
        <div class="dropdown-divider"></div>
        {% for item in cart.items|slice:":3" %}
            <div class="dropdown-item">
                <div class="d-flex align-items-center">
                    {% if item.product.thumbnail %}
                        <img src="{{ item.product.thumbnail.url }}"
                             alt="{{ item.product.name }}"
                             class="rounded me-2"
                             style="width: 40px; height: 40px; object-fit: cover;">
                    {% endif %}
                    <div class="flex-grow-1">
                        <strong>{{ item.product.name }}</strong>
                        <div class="small text-muted">
                            Qty: {{ item.quantity }} × ${{ item.product.price }}
                        </div>
                    </div>
                </div>
            </div>
            {% if not forloop.last %}
                <div class="dropdown-divider"></div>
            {% endif %}
        {% endfor %}

        {# Cart Total #}
        <div class="dropdown-divider"></div>
        <div class="dropdown-item">
            <div class="d-flex justify-content-between">
                <strong>Total:</strong>
                <strong>${{ cart.total_price }}</strong>
            </div>
        </div>

        {# Checkout Button #}
        <div class="dropdown-divider"></div>
        <a href="{% url 'checkout' %}" class="dropdown-item dropdown-footer text-center">
            Proceed to Checkout
        </a>
    {% endif %}
</c-navbar.custom_widget>
```

## Styling Tips

### AdminLTE Dropdown Classes

Use AdminLTE's built-in dropdown classes for consistent styling:

- `dropdown-menu-lg`: Larger dropdown (400px width)
- `dropdown-menu-end`: Align dropdown to the right
- `dropdown-header`: Header section styling
- `dropdown-divider`: Visual separator between items
- `dropdown-footer`: Footer link styling

### Scrolling Content

For widgets with many items, add scrolling:

```django
<c-navbar.custom_widget icon="bi-list" dropdown_id="long-list">
    <div style="max-height: 300px; overflow-y: auto;">
        {# Your long list of items #}
    </div>
</c-navbar.custom_widget>
```

### Badge Colors

Choose badge colors based on alert level:

- **`danger`** (red): Errors, critical issues, overdue items
- **`warning`** (yellow): Warnings, moderate priority, approaching deadlines
- **`info`** (blue): Informational, low priority
- **`success`** (green): Completed, positive notifications
- **`primary`** (blue): General notifications
- **`secondary`** (gray): Neutral information

## Best Practices

### 1. Limit Dropdown Items

Show only the most recent or important items (typically 3-5) to keep dropdowns fast and usable:

```django
{% for item in items|slice:":5" %}
    {# ... #}
{% endfor %}
```

### 2. Add "See All" Footer

Always provide a link to view all items:

```django
<a href="{% url 'view-all' %}" class="dropdown-item dropdown-footer">
    See All Items
</a>
```

### 3. Handle Empty States

Show helpful messaging when there are no items:

```django
{% if items %}
    {# Show items #}
{% else %}
    <div class="dropdown-item text-center text-muted">
        No items to display
    </div>
{% endif %}
```

### 4. Use Unique Dropdown IDs

Each widget instance needs a unique `dropdown_id`:

```django
{# Good #}
<c-navbar.custom_widget dropdown_id="tasks-dropdown" ...>
<c-navbar.custom_widget dropdown_id="alerts-dropdown" ...>

{# Bad - Same ID causes conflicts #}
<c-navbar.custom_widget dropdown_id="widget-dropdown" ...>
<c-navbar.custom_widget dropdown_id="widget-dropdown" ...>
```

### 5. Optimize Badge Queries

Use efficient queries to get badge counts:

```python
# Good - count() is optimized
context['task_count'] = Task.objects.filter(user=request.user, completed=False).count()

# Bad - len() loads all objects into memory
context['task_count'] = len(Task.objects.filter(user=request.user, completed=False))
```

### 6. Add Loading States

For widgets with AJAX updates, add loading indicators:

```django
<div id="widget-content">
    {# Content #}
</div>
<div id="widget-loading" class="text-center" style="display: none;">
    <div class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
</div>
```

## JavaScript Enhancements

### Auto-Refresh Widget Content

Add JavaScript to automatically refresh widget content:

```javascript
// Refresh tasks widget every 60 seconds
setInterval(function() {
    fetch('/api/tasks/count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('#tasks-widget .navbar-badge');
            if (data.count > 0) {
                badge.textContent = data.count > 99 ? '99+' : data.count;
                badge.style.display = '';
            } else {
                badge.style.display = 'none';
            }
        });
}, 60000);
```

### Mark Items as Read

Add click handlers to mark items as read/acknowledged:

```javascript
document.querySelectorAll('.alert-item').forEach(item => {
    item.addEventListener('click', function() {
        const alertId = this.dataset.alertId;
        fetch(`/api/alerts/${alertId}/acknowledge/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(() => {
            this.remove();
            updateBadgeCount();
        });
    });
});
```

## Integration with django-flex-menus

To add custom widgets to your navbar via django-flex-menus:

```python
# In your menus.py
from flex_menu import Menu, MenuItem

navbar_menu = Menu("navbar")

# Add to the right side of navbar
navbar_menu.add_item(
    MenuItem(
        text="tasks",
        template="navbar/custom_widget.html",
        context={
            'icon': 'bi-check2-square',
            'dropdown_id': 'tasks-dropdown',
            'badge_count': 5,
            'badge_color': 'warning',
        },
        weight=90
    )
)
```

## Related Documentation

- [Navbar Widgets Overview](navbar-widgets.md)
- [User Profile Widget](navbar-widgets.md#user-profile-widget)
- [Notifications Widget](navbar-widgets.md#notifications-widget)
- [Messages Widget](navbar-widgets.md#messages-widget)
- [Bootstrap Dropdowns](https://getbootstrap.com/docs/5.3/components/dropdowns/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
