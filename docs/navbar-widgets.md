# Navbar Widgets

Django MVP provides a collection of interactive navbar widgets for common application features. All widgets are built as Cotton components and follow AdminLTE 4's design patterns.

## Table of Contents

- [Overview](#overview)
- [Installation & Setup](#installation--setup)
- [User Profile Widget](#user-profile-widget)
- [Notifications Widget](#notifications-widget)
- [Messages Widget](#messages-widget)
- [Theme Switcher Widget](#theme-switcher-widget)
- [Fullscreen Widget](#fullscreen-widget)
- [Custom Widgets](#custom-widgets)
- [Accessibility](#accessibility)
- [Troubleshooting](#troubleshooting)

## Overview

Navbar widgets provide interactive UI components in the application's navigation bar:

- **User Profile Widget** - Display user information with dropdown menu for account actions
- **Notifications Widget** - Real-time notification center with badge counter and dropdown list
- **Messages Widget** - Message inbox preview with unread count and recent messages
- **Theme Switcher Widget** - Toggle between light, dark, and auto themes with persistence
- **Fullscreen Widget** - Browser fullscreen mode toggle with cross-browser support
- **Custom Widgets** - Framework for creating application-specific widgets

All widgets are:

- **Responsive** - Adapt to mobile and desktop layouts
- **Accessible** - ARIA-compliant with keyboard navigation
- **Themeable** - Support light/dark themes automatically
- **Configurable** - Props for customization without template overrides

## Installation & Setup

### Prerequisites

```python
# settings.py
INSTALLED_APPS = [
    "django_cotton",
    "cotton_bs5",
    "easy_icons",
    "mvp",
    # ... other apps
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "mvp.context_processors.mvp_config",
                # ... other context processors
            ],
        },
    },
]
```

### Basic Usage

Add widgets to your template by extending `mvp/base.html` and overriding the `navbar_right` block:

```html
{% extends "mvp/base.html" %}

{% block navbar_right %}
  <c-navbar.user-profile-widget user=request.user />
  <c-navbar.notifications-widget unread_count="5" />
  <c-navbar.messages-widget unread_count="3" />
  <c-navbar.theme-switcher-widget />
  <c-navbar.fullscreen-widget />
{% endblock %}
```

## User Profile Widget

Display user information with a dropdown menu for account-related actions.

### Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `user` | User | Yes | - | Django user object |
| `avatar_url` | string | No | `None` | URL to user avatar image |
| `member_since` | string | No | `None` | Membership date/text (e.g., "Jan 2024") |
| `show_email` | boolean | No | `True` | Show user email in dropdown |
| `class` | string | No | `""` | Additional CSS classes |

### Slots

#### `dropdown_menu_items`

Custom menu items between header and footer:

```html
<c-navbar.user-profile-widget user=request.user>
  <c-slot name="dropdown_menu_items">
    <a href="{% url 'settings' %}" class="dropdown-item">
      <i class="bi bi-gear me-2"></i> Settings
    </a>
    <a href="{% url 'billing' %}" class="dropdown-item">
      <i class="bi bi-credit-card me-2"></i> Billing
    </a>
  </c-slot>
</c-navbar.user-profile-widget>
```

#### `dropdown_footer`

Custom footer content:

```html
<c-navbar.user-profile-widget user=request.user>
  <c-slot name="dropdown_footer">
    <a href="{% url 'logout' %}" class="dropdown-item dropdown-footer">
      Sign Out
    </a>
  </c-slot>
</c-navbar.user-profile-widget>
```

### Examples

#### Minimal Usage

```html
<c-navbar.user-profile-widget user=request.user />
```

#### With Avatar and Member Since

```html
<c-navbar.user-profile-widget
  user=request.user
  avatar_url="{{ user.profile.avatar.url }}"
  member_since="Member since Jan 2024" />
```

#### Custom Menu Items

```html
<c-navbar.user-profile-widget user=request.user>
  <c-slot name="dropdown_menu_items">
    <a href="{% url 'profile' %}" class="dropdown-item">
      <i class="bi bi-person me-2"></i> Profile
    </a>
    <div class="dropdown-divider"></div>
    <a href="{% url 'settings' %}" class="dropdown-item">
      <i class="bi bi-gear me-2"></i> Settings
    </a>
    <a href="{% url 'help' %}" class="dropdown-item">
      <i class="bi bi-question-circle me-2"></i> Help
    </a>
  </c-slot>
</c-navbar.user-profile-widget>
```

#### With Context Data

```python
# views.py
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avatar_url"] = self.request.user.profile.avatar.url
        context["member_since"] = f"Member since {self.request.user.date_joined.strftime('%b %Y')}"
        return context
```

```html
<!-- dashboard.html -->
{% extends "mvp/base.html" %}

{% block navbar_right %}
  <c-navbar.user-profile-widget
    user=request.user
    avatar_url=avatar_url
    member_since=member_since />
{% endblock %}
```

## Notifications Widget

Real-time notification center with badge counter and dropdown list.

### Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `unread_count` | int | No | `0` | Number of unread notifications |
| `notifications` | list | No | `[]` | List of notification dictionaries |
| `class` | string | No | `""` | Additional CSS classes |

### Notification Dictionary Structure

```python
{
    "icon": "bell",           # Bootstrap icon name
    "message": "New comment", # Notification text
    "time": "5 mins ago",     # Time display
    "url": "/comments/123",   # Optional link URL
    "read": False,            # Optional read status
}
```

### Examples

#### Basic Usage

```html
<c-navbar.notifications-widget unread_count="5" />
```

#### With Notifications List

```python
# views.py
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["notifications"] = [
        {
            "icon": "bell",
            "message": "New comment on your post",
            "time": "5 mins ago",
            "url": "/comments/123",
        },
        {
            "icon": "person-plus",
            "message": "John followed you",
            "time": "10 mins ago",
            "url": "/users/john",
        },
        {
            "icon": "heart-fill",
            "message": "Sarah liked your photo",
            "time": "1 hour ago",
            "url": "/photos/456",
        },
    ]
    return context
```

```html
<c-navbar.notifications-widget
  unread_count="{{ notifications|length }}"
  notifications=notifications />
```

#### Real-time Updates with HTMX

```html
<c-navbar.notifications-widget
  unread_count="{{ unread_count }}"
  notifications=notifications
  hx-get="{% url 'notifications:list' %}"
  hx-trigger="every 60s"
  hx-swap="outerHTML" />
```

```python
# views.py
from django.views.generic import TemplateView

class NotificationsWidgetView(TemplateView):
    template_name = "widgets/notifications_widget.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = self.request.user.notifications.unread()[:5]
        context["unread_count"] = notifications.count()
        context["notifications"] = [
            {
                "icon": n.icon,
                "message": n.message,
                "time": n.created_at,
                "url": n.get_absolute_url(),
            }
            for n in notifications
        ]
        return context
```

## Messages Widget

Message inbox preview with unread count and recent messages.

### Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `unread_count` | int | No | `0` | Number of unread messages |
| `messages` | list | No | `[]` | List of message dictionaries |
| `class` | string | No | `""` | Additional CSS classes |

### Message Dictionary Structure

```python
{
    "sender_name": "John Doe",           # Sender's name
    "sender_avatar": "/media/john.jpg",  # Optional avatar URL
    "message": "Hey, how are you?",      # Message preview
    "time": "5 mins ago",                # Time display
    "url": "/messages/123",              # Optional link URL
    "read": False,                       # Optional read status
}
```

### Examples

#### Basic Usage

```html
<c-navbar.messages-widget unread_count="3" />
```

#### With Messages List

```python
# views.py
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    recent_messages = self.request.user.messages.all()[:3]
    context["messages"] = [
        {
            "sender_name": msg.sender.get_full_name(),
            "sender_avatar": msg.sender.profile.avatar.url,
            "message": msg.body[:50],
            "time": msg.created_at,
            "url": msg.get_absolute_url(),
            "read": msg.read,
        }
        for msg in recent_messages
    ]
    context["unread_count"] = self.request.user.messages.unread().count()
    return context
```

```html
<c-navbar.messages-widget
  unread_count="{{ unread_count }}"
  messages=messages />
```

#### With Fallback for No Avatar

```python
# views.py
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["messages"] = [
        {
            "sender_name": msg.sender.get_full_name(),
            "sender_avatar": msg.sender.profile.avatar.url if hasattr(msg.sender, 'profile') else None,
            "message": msg.body[:50],
            "time": msg.created_at,
            "url": msg.get_absolute_url(),
        }
        for msg in self.request.user.messages.all()[:3]
    ]
    return context
```

## Theme Switcher Widget

Toggle between light, dark, and auto themes with persistence using localStorage.

### Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `class` | string | No | `""` | Additional CSS classes |

### Features

- **Three Modes**: Light, Dark, Auto (follows system preference)
- **Persistence**: Theme choice saved to `localStorage`
- **Automatic Detection**: Auto mode listens to system theme changes
- **Icons**: Bootstrap Icons (sun, moon, circle-half)
- **Smooth Transitions**: CSS transitions when switching themes

### Examples

#### Basic Usage

```html
<c-navbar.theme-switcher-widget />
```

#### Custom Class

```html
<c-navbar.theme-switcher-widget class="mx-2" />
```

### How It Works

1. **Initial Load**: Checks `localStorage` for saved theme, defaults to "auto"
2. **User Selection**: Click widget to cycle through light → dark → auto
3. **Persistence**: Saves choice to `localStorage` as `theme-mode`
4. **Auto Mode**: When "auto", listens to `prefers-color-scheme` media query changes
5. **Theme Application**: Adds `data-bs-theme="light|dark"` to `<html>` element

### Customization

The widget uses Bootstrap 5's native theme system. To customize theme colors:

```css
/* Custom light theme colors */
[data-bs-theme="light"] {
  --bs-body-bg: #f8f9fa;
  --bs-body-color: #212529;
}

/* Custom dark theme colors */
[data-bs-theme="dark"] {
  --bs-body-bg: #212529;
  --bs-body-color: #f8f9fa;
}
```

## Fullscreen Widget

Browser fullscreen mode toggle using AdminLTE 4's built-in fullscreen functionality.

### Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `class` | string | No | `""` | Additional CSS classes |

### Features

- **AdminLTE Integration**: Uses AdminLTE 4's built-in fullscreen plugin
- **Automatic API Detection**: AdminLTE handles browser compatibility automatically
- **Icon Toggle**: Shows expand icon (arrows-fullscreen) when not fullscreen, collapse icon (arrows-angle-contract) when fullscreen
- **Keyboard Support**: ESC key to exit fullscreen (browser default)
- **Accessibility**: ARIA labels and title attributes
- **No Custom JavaScript**: Leverages AdminLTE's existing functionality

### Examples

#### Basic Usage

```html
<c-navbar/fullscreen_widget />
```

#### Custom Class

```html
<c-navbar/fullscreen_widget class="mx-2" />
```

### How It Works

The widget uses AdminLTE 4's fullscreen plugin via:

- `data-lte-toggle="fullscreen"` - Activates AdminLTE's fullscreen handler
- `data-lte-icon="maximize"` - Maximize icon (visible by default)
- `data-lte-icon="minimize"` - Minimize icon (hidden by default)

AdminLTE automatically:

1. Detects Fullscreen API support
2. Toggles fullscreen mode on click
3. Swaps icon visibility based on state
4. Handles ESC key for exit

### Browser Support

AdminLTE handles browser compatibility automatically using the standard Fullscreen API:

| Browser | Support |
|---------|---------|
| Chrome/Edge 71+ | ✓ |
| Firefox 64+ | ✓ |
| Safari 16.4+ | ✓ |
| IE 11 | ✓ MS-prefixed API |
| Older browsers | ✗ Widget hidden |

### How It Works

1. **API Detection**: Checks for standard or vendor-prefixed Fullscreen API
2. **Auto-hide**: If API not available, widget hidden via JavaScript
3. **Toggle**: Click to enter fullscreen (document.body) or exit
4. **Icon Update**: Listens to `fullscreenchange` events to update icon
5. **ESC Key**: Browser handles ESC key to exit (no custom code needed)

### Troubleshooting

#### Widget Not Showing

The widget hides itself if the Fullscreen API is unavailable. Check browser support or test in a supported browser.

#### Fullscreen Not Working in iframe

For security reasons, iframes require the `allowfullscreen` attribute:

```html
<iframe src="/dashboard" allowfullscreen></iframe>
```

## Custom Widgets

Create application-specific navbar widgets using the `<c-navbar.widget>` component. This base component provides the foundation for building custom widgets with icons, badges, and dropdown content.

### Basic Structure

```html
<c-navbar.widget
  icon="icon-alias"
  badge_count="{{ count }}"
  badge_color="danger"
  aria_label="Descriptive label">

  <!-- Dropdown content goes here -->
  <div class="dropdown-item">Custom content</div>
</c-navbar.widget>
```

### Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `icon` | string | Yes | - | Icon alias from EASY_ICONS configuration |
| `badge_count` | integer | No | `0` | Unread/notification count (0 hides badge) |
| `badge_color` | string | No | `"danger"` | Bootstrap color variant for badge |
| `aria_label` | string | No | `""` | Accessible label for screen readers |

### Quick Example

```html
<c-navbar.widget
  icon="check2-square"
  badge_count="{{ tasks_count }}"
  badge_color="warning"
  aria_label="Tasks">

  {% for task in tasks %}
    <a href="{{ task.get_absolute_url }}" class="dropdown-item">
      {{ task.title }}
    </a>
  {% endfor %}
</c-navbar.widget>
```

### Badge Behavior

- **Count = 0**: Badge hidden
- **Count 1-99**: Shows exact number
- **Count > 99**: Shows "99+"

For more details, see the [Custom Navbar Widgets Tutorial](custom-navbar-widgets.md).

## Accessibility

All navbar widgets follow WCAG 2.1 AA guidelines:

### Keyboard Navigation

- **Tab**: Navigate between widgets
- **Enter/Space**: Open dropdown menus
- **Escape**: Close dropdown menus
- **Arrow Keys**: Navigate dropdown items (managed by Bootstrap)

### Screen Readers

- **ARIA Labels**: All interactive elements have descriptive labels
- **ARIA Live Regions**: Badge counters announce updates
- **Semantic HTML**: Proper `<nav>`, `<button>`, `<a>` elements

### Color Contrast

- **Text**: Meets 4.5:1 contrast ratio
- **Icons**: 3:1 contrast ratio for non-text content
- **Focus Indicators**: Visible focus outlines

### Testing

Test accessibility with:

```bash
# Automated testing
poetry run pytest tests/test_navbar_widgets.py -v

# Manual testing
# 1. Navigate with keyboard only
# 2. Test with screen reader (NVDA, JAWS, VoiceOver)
# 3. Check color contrast with browser DevTools
```

## Troubleshooting

### Widget Not Rendering

**Problem**: Widget doesn't appear in navbar

**Solutions**:

1. Check template extends `mvp/base.html`
2. Verify block name is `navbar_right` (not `navbar-right`)
3. Ensure `django_cotton` in `INSTALLED_APPS`
4. Check for template syntax errors in browser console

### Badge Not Showing

**Problem**: Unread count badge not visible

**Solutions**:

1. Verify `unread_count` prop is passed and > 0
2. Check badge color is valid Bootstrap variant (primary, danger, etc.)
3. Inspect element for `badge` class in rendered HTML

### Dropdown Not Opening

**Problem**: Clicking widget doesn't open dropdown

**Solutions**:

1. Verify Bootstrap 5 JavaScript is loaded in base template
2. Check browser console for JavaScript errors
3. Ensure `data-bs-toggle="dropdown"` attribute present
4. Test with Bootstrap directly: `<button class="btn" data-bs-toggle="dropdown">Test</button>`

### Theme Not Persisting

**Problem**: Theme resets on page reload

**Solutions**:

1. Check browser allows `localStorage` (not disabled by privacy settings)
2. Verify theme-switcher.js is loaded without errors
3. Test `localStorage` in browser console: `localStorage.setItem('test', '1')`
4. Check for Content Security Policy blocking scripts

### Avatar Not Loading

**Problem**: User profile widget shows default avatar instead of custom image

**Solutions**:

1. Verify `avatar_url` prop is valid and accessible
2. Check MEDIA_URL and MEDIA_ROOT settings in Django
3. Test URL directly in browser: `http://localhost:8000{{ avatar_url }}`
4. Ensure image file exists at expected path
5. Check for CORS issues if using external image URLs

### JavaScript Errors

**Problem**: Browser console shows JavaScript errors

**Solutions**:

1. Verify all static files loaded: `poetry run python manage.py collectstatic` (production only)
2. Check for conflicting JavaScript libraries
3. Test with browser DevTools Network tab for 404 errors
4. Ensure jQuery not required (widgets use vanilla JavaScript)

### Mobile Responsiveness

**Problem**: Widgets don't display correctly on mobile

**Solutions**:

1. Verify viewport meta tag in base.html: `<meta name="viewport" content="width=device-width, initial-scale=1">`
2. Check AdminLTE responsive classes in layout configuration
3. Test with browser DevTools responsive mode
4. Verify no custom CSS overrides breaking responsive behavior

## Further Reading

- [Custom Navbar Widgets Tutorial](custom-navbar-widgets.md) - Create application-specific widgets
- [AdminLTE 4 Documentation](https://adminlte.io/docs/4.0/) - Official AdminLTE docs
- [Bootstrap 5 Navbar](https://getbootstrap.com/docs/5.3/components/navbar/) - Bootstrap navbar component
- [django-cotton Documentation](https://django-cotton.com/) - Cotton component system
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/) - Web accessibility standards
