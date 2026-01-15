# Feature Specification: Main Navbar Widgets - Base & Generic Widgets

**Feature Branch**: `005-navbar-widgets`
**Created**: January 14, 2026
**Updated**: January 15, 2026
**Status**: Draft
**Input**: User description: "This feature spec will cover the creation and testing of the base navbar widget component and generic widgets (fullscreen and theme-switcher). The base widget at cotton/navbar/widget/index.html provides the foundation from which all other widgets can be built. User-specific widgets (user profile, messages, notifications) are deferred to future specs."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Base Widget Component (Priority: P1)

Developers can use a reusable base widget component at cotton/navbar/widget/index.html that provides the foundational structure for creating custom navbar widgets with icons, badges, and dropdown content.

**Why this priority**: The base widget is the foundation for all other widgets. Without it, developers cannot create consistent navbar widgets that follow AdminLTE patterns.

**Independent Test**: Create a custom widget using the base component with icon, optional badge, and dropdown content. Verify it renders correctly with AdminLTE styling and Bootstrap dropdown behavior.

**Acceptance Scenarios**:

1. **Given** developer uses base widget component with icon, **When** widget renders, **Then** it displays icon in navbar with proper styling
2. **Given** base widget is provided badge count, **When** widget renders, **Then** badge appears with count and specified color class
3. **Given** base widget is provided dropdown content via slot, **When** widget is clicked, **Then** dropdown opens with provided content
4. **Given** no badge value provided, **When** widget renders, **Then** only icon is displayed without badge element

---

### User Story 2 - Theme Switcher Widget (Priority: P1)

Developers can add a theme switcher widget that allows users to toggle between light, dark, and auto (system preference) themes with persistence across sessions.

**Why this priority**: Modern expectation for web applications. Improves accessibility and user comfort. Requires custom JavaScript implementation and provides immediate user value.

**Independent Test**: Add theme switcher widget, click to change themes, verify theme persists on page reload and respects system preferences in auto mode.

**Acceptance Scenarios**:

1. **Given** user clicks theme switcher, **When** dropdown opens, **Then** it shows Light, Dark, and Auto options with current selection marked
2. **Given** user selects Dark theme, **When** selection is made, **Then** page immediately switches to dark mode and preference is saved to localStorage
3. **Given** user selects Auto mode, **When** system is in dark mode, **Then** page displays in dark theme
4. **Given** user refreshes page, **When** page loads, **Then** previously selected theme is applied

---

### User Story 3 - Fullscreen Toggle Widget (Priority: P2)

Developers can add a fullscreen toggle widget that allows users to expand the application to fullscreen mode.

**Why this priority**: Useful feature for focus modes or presentations. Complements the base widget system well and demonstrates custom widget patterns.

**Independent Test**: Add fullscreen widget, click to toggle fullscreen mode, verify icon changes and fullscreen API is properly invoked.

**Acceptance Scenarios**:

1. **Given** fullscreen widget is clicked, **When** in normal mode, **Then** application enters fullscreen mode and icon changes to "exit fullscreen"
2. **Given** application is in fullscreen, **When** widget is clicked again, **Then** application exits fullscreen and icon returns to normal
3. **Given** user presses ESC key in fullscreen, **When** fullscreen exits, **Then** widget icon updates to reflect normal mode
4. **Given** browser doesn't support fullscreen API, **When** widget renders, **Then** it is hidden or disabled

---

### Edge Cases

- **Badge count validation**: Widget MUST handle negative or non-numeric badge counts by displaying nothing (hide badge)
- **Empty dropdown content**: Widget displays appropriate empty state message or custom content provided by developer
- **localStorage disabled**: Theme switcher functions in session-only mode (no persistence across reloads)
- **Multiple open widgets**: Bootstrap dropdown behavior closes other dropdowns automatically
- **Mobile/narrow screens**: Widgets remain functional and dropdowns are right-aligned
- **JavaScript load failure**: Theme switcher and fullscreen widget non-functional, graceful degradation to default theme
- **Fullscreen API not supported**: Fullscreen widget should be hidden or disabled gracefully

## Clarifications

### Session 2026-01-14

- Q: How should the theme switcher behave when localStorage is unavailable? → A: Session-only theme (works but doesn't persist across page reloads)

### Session 2026-01-15

- Q: Should user-specific widgets (user profile, messages, notifications) be included in this spec? → A: No - defer to future specs. This spec covers only the base widget component and generic widgets (theme-switcher and fullscreen)
- Q: What is the scope of "generic" widgets? → A: Widgets that are application-agnostic and don't require user-specific data (theme switcher, fullscreen toggle)
- Q: Where is the base widget component located? → A: cotton/navbar/widget/index.html - provides foundation for all custom widgets
- Q: How should icons be implemented in widgets? → A: Use `<c-icon name="alias" />` component with aliases from EASY_ICONS settings (never direct `<i class="bi-*">` tags)
- Q: What icon aliases are available? → A: Check tests/settings.py EASY_ICONS dict (notification, theme_light, maximize, minimize, person, settings, etc.)
- Q: What if needed icon alias doesn't exist? → A: Add new alias to EASY_ICONS settings mapping to appropriate Bootstrap Icon class
- Q: Can additional attributes be added to icons? → A: Yes - pass any HTML attributes to `<c-icon />` and they'll be added to rendered element
- Q: How are slots declared in Cotton components? → A: Default slot uses `{{ slot }}` Django variable. Named slots use `{{ slot_name }}` Django variables
- Q: How do you pass content to named slots? → A: From another component, use `<c-slot name="footer">content</c-slot>` to inject into `{{ footer }}` variable
- Q: Can slots be used outside of components? → A: No - `<c-slot name="...">` syntax only works when calling components from within other components

## Requirements *(mandatory)*

### Functional Requirements

#### Base Widget Component (P1)

- **FR-001**: System MUST provide a base widget component at cotton/navbar/widget/index.html
- **FR-002**: Base widget MUST support icon specification via icon alias name (e.g., `icon="notification"` which maps to bootstrap icon via EASY_ICONS settings)
- **FR-003**: Base widget MUST support optional badge with count and color specification
- **FR-004**: Base widget MUST hide badge element when count is zero or not provided
- **FR-005**: Base widget MUST support dropdown content via Cotton default slot ({{ slot }} Django variable)
- **FR-006**: Base widget MUST follow AdminLTE navbar styling conventions (nav-item dropdown pattern)
- **FR-007**: Base widget MUST work with Bootstrap 5 dropdown behavior
- **FR-008**: Badge MUST support Bootstrap color classes (danger, warning, info, success)
- **FR-008a**: Base widget MUST use `<c-icon />` component for all icon rendering (never direct `<i>` tags with Bootstrap Icon classes)

#### Theme Switcher (P1)

- **FR-009**: System MUST provide a theme switcher widget with Light, Dark, and Auto options
- **FR-010**: Theme switcher MUST persist selected theme to localStorage when available
- **FR-011**: Theme switcher MUST function in session-only mode when localStorage is unavailable (theme resets on page reload)
- **FR-012**: Theme switcher MUST apply theme immediately without page reload (< 100ms per SC-003)
- **FR-013**: Theme switcher MUST respect system dark mode preference in Auto mode
- **FR-014**: Theme switcher MUST display theme_light icon alias in navbar button (icon updates handled by dropdown menu active state)
- **FR-015**: Theme switcher MUST work when JavaScript is available (graceful degradation)

#### Fullscreen Widget (P2)

- **FR-016**: System MUST provide a fullscreen toggle widget
- **FR-017**: Fullscreen widget MUST toggle browser fullscreen API
- **FR-018**: Fullscreen widget MUST display appropriate icon using maximize/minimize icon aliases from EASY_ICONS
- **FR-019**: Fullscreen widget MUST be hidden when fullscreen API is not supported

### Non-Functional Requirements

- **NFR-001**: Required icon aliases MUST exist in EASY_ICONS settings: theme_light, maximize, minimize
- **NFR-002**: Icon component MUST accept additional HTML attributes and pass them to rendered element
- **NFR-003**: All widgets MUST be keyboard accessible (Tab navigation, Enter/Space activation)

### Key Entities *(include if feature involves data)*

- **NavbarWidget**: Base component structure - icon, optional badge, optional dropdown, styling classes
- **ThemePreference**: Theme state - current theme (light/dark/auto), stored preference, system preference detection
- **FullscreenState**: Fullscreen state - is fullscreen active, browser API support detection

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can add any widget to the navbar in under 5 lines of Django template code
- **SC-002**: All widgets render correctly on mobile (320px), tablet (768px), and desktop (1200px+) viewports
- **SC-003**: Theme switcher changes theme in under 100ms with no visible flicker
- **SC-004**: Widget dropdowns open/close with smooth animations matching AdminLTE defaults
- **SC-005**: Badge counters display correctly for values from 0 to 999+
- **SC-006**: User can toggle fullscreen mode with single click and widget reflects state accurately
- **SC-007**: All widgets maintain accessibility (ARIA labels, keyboard navigation, screen reader support)
- **SC-008**: Theme preference persists across browser sessions and page reloads
- **SC-009**: Documentation provides complete examples for each widget type
- **SC-010**: Test coverage includes unit tests for all components and integration tests for theme switcher JavaScript

## Assumptions

- Django templates are used for rendering (not a pure JavaScript SPA)
- Bootstrap 5 is available (AdminLTE 4 dependency)
- django-cotton is used for component composition
- django-easy-icons is configured with appropriate icon aliases in settings.py
- Users have browsers with localStorage support for theme persistence
- Fullscreen API support is optional and widget gracefully degrades
- Theme switcher and fullscreen widgets require JavaScript
- Base widget can be used to create custom application-specific widgets
- Icon aliases (notification, theme_light, maximize, minimize, etc.) exist in EASY_ICONS settings

## Out of Scope

- **User profile widget** (deferred to future spec)
- **Messages widget** (deferred to future spec)
- **Notifications widget** (deferred to future spec)
- Real-time updates via WebSocket/SSE
- AJAX-based dropdown content loading
- Search widget implementation (noted as "not working" in AdminLTE 4 docs)
- Custom theme color definitions (beyond light/dark/auto)
- Widget position customization or reordering
- Mobile-specific widget behaviors (swipe gestures, etc.)

## Dependencies

- Bootstrap 5.3+ (AdminLTE 4 requirement)
- django-easy-icons (for icon rendering via `<c-icon />` component)
- django-cotton 2.3+ (for component composition)
- AdminLTE 4 CSS/JS (for navbar styling and behavior)
- Browser support: Modern browsers with ES6+ for theme switcher
- localStorage API for theme persistence

## Notes

### Theme Switcher Implementation

The theme switcher requires custom JavaScript as demonstrated in AdminLTE docs. Key points:

- Uses `data-bs-theme` attribute on `<html>` element
- Detects system preference via `window.matchMedia('(prefers-color-scheme: dark)')`
- Stores user preference in `localStorage.setItem('theme', value)`
- Updates active selection in dropdown menu
- Responds to system preference changes when in Auto mode

### Widget Composition Pattern

All widgets follow the same structural pattern:

```html
<!-- Base widget component definition (cotton/navbar/widgets/index.html) -->
<li class="nav-item dropdown">
  <a class="nav-link" data-bs-toggle="dropdown" href="#">
    <c-icon name="{{ icon }}" />
    <span class="navbar-badge badge text-bg-{{ badge_color }}">{{ badge_count }}</span>
  </a>
  <div class="dropdown-menu dropdown-menu-lg dropdown-menu-end">
    {{ slot }}  <!-- Default slot: content injected here -->
  </div>
</li>
```

**Cotton Slot Syntax:**

- **In component definition**: Use Django variables `{{ slot }}` for default, `{{ footer }}` for named slots
- **When calling component**: Content between tags goes to `{{ slot }}`, use `<c-slot name="footer">` for named slots
- **Example usage**:

  ```html
  <c-navbar.widgets icon="notification" badge_count="5">
    <!-- This content goes into {{ slot }} -->
    <div class="dropdown-header">Notifications</div>

    <!-- Named slots only work from within other components -->
    <c-slot name="footer">
      <a href="#">See all</a>
    </c-slot>
  </c-navbar.widgets>
  ```

**Icon Implementation:**

- Use `<c-icon name="alias" />` component (django-easy-icons)
- Icon aliases defined in settings.py under EASY_ICONS
- Never use direct `<i class="bi bi-icon-name">` tags
- Available aliases: notification, theme_light, maximize, minimize, person, settings, etc.
- Add new aliases to EASY_ICONS settings if needed

This pattern should be abstracted into reusable Cotton components with slots for customization.

### Responsive Behavior

- Dropdown menus: Always dropdown-menu-end (right-aligned)
- Widget icons: Always visible regardless of screen size
- Dropdown width: Use dropdown-menu-lg class for wider dropdowns when needed
- Base widget provides responsive foundation for custom implementations
