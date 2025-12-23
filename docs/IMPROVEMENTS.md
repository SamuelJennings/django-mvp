# Recommended Improvements for Django Cotton Layouts

This document outlines suggested improvements for code clarity, maintainability, and usability based on the structural analysis and naming scheme standardization.

## Priority 1: Critical Structural Updates

### 1.1 Rename SCSS Files to Match New Naming Scheme

**Current:**
- `_layout.scss` (ambiguous)
- `_inner-layout.scss` (unclear hierarchy)
- `_sidebar.scss` (applies to multiple sidebar types)

**Recommended:**
- `_outer-layout.scss` - Application shell (`.app-shell`, `.app-column`)
- `_content-layout.scss` - Inner content layout (`.content-shell`, `.content-sidebar-left/right`, `.content-main`)
- `_sidebar.scss` - Keep, but document it applies to ALL sidebar types (site + content)
- `_navbar.scss` - Keep
- `_page.scss` - NEW: Page-level elements (`.page-toolbar`, `.page-header`, `.page-title`, `.page-content`)
- `_footer.scss` - NEW: Footer component

**Action Items:**
```bash
# Rename files
mv _layout.scss _outer-layout.scss
mv _inner-layout.scss _content-layout.scss

# Create new files
touch _page.scss
touch _footer.scss
```

### 1.2 Update JavaScript Files to Match Naming

**Current:**
- `sidebar.js` (handles site sidebar)
- `inner_layout.js` (handles content sidebars)

**Recommended:**
- `site-sidebar.js` - Site navigation sidebar collapse/toggle
- `content-sidebars.js` - Content area left/right sidebar management

**Rationale:** Clear distinction between site-level and content-level sidebars.

### 1.3 Migrate Class Names in Templates

Create migration aliases in SCSS:

```scss
// _backwards-compat.scss - For gradual migration
.sidebar-layout {
  @extend .app-shell;
}

.main-column {
  @extend .app-column;
}

.main-content {
  @extend .app-main;
}

.inner-layout {
  @extend .content-shell;
}

.inner-primary {
  @extend .content-sidebar-left;
}

.inner-secondary {
  @extend .content-sidebar-right;
}

.inner-main {
  @extend .content-main;
}
```

**Deprecation Plan:**
1. Add aliases (done in v0.2)
2. Update all package templates to use new names (v0.3)
3. Mark old names as deprecated in docs (v0.3)
4. Remove aliases (v1.0 - breaking change)

---

## Priority 2: Component Organization

### 2.1 Reorganize Template Directory Structure

**Current:**
```
templates/cotton/
├── structure/
│   ├── sidebar/
│   ├── navbar/
│   └── main/
├── sidebar/  # Duplicate? Unclear purpose
├── layouts/
└── page/
```

**Recommended:**
```
templates/cotton/
├── app/           # Application shell components
│   ├── shell.html          # .app-shell container
│   ├── sidebar.html        # .site-sidebar
│   ├── navbar.html         # .site-navbar
│   ├── main.html           # .app-main
│   └── footer.html         # .app-footer
├── page/          # Page-level components
│   ├── toolbar.html        # .page-toolbar
│   ├── breadcrumbs.html    # .page-breadcrumbs
│   ├── header.html         # .page-header
│   ├── title.html          # .page-title
│   └── content.html        # .page-content wrapper
├── content/       # Content layout components
│   ├── shell.html          # .content-shell
│   ├── sidebar-left.html   # .content-sidebar-left
│   ├── sidebar-right.html  # .content-sidebar-right
│   └── main.html           # .content-main
├── sidebar/       # Shared sidebar components
│   ├── base.html           # Base .sidebar component
│   ├── menu-item.html
│   ├── menu-section.html
│   └── brand.html
└── layouts/       # Pre-built layout templates
    ├── standard.html
    ├── list_view.html
    └── detail_view.html
```

**Benefits:**
- Clear separation of concerns (app, page, content levels)
- Easy to find components based on hierarchy
- Consistent naming with class names

### 2.2 Create Component Index/Registry

Create `components.py` to document all available components:

```python
"""Component registry for django-cotton-layouts."""

COMPONENTS = {
    "app": {
        "shell": "app/shell.html",
        "sidebar": "app/sidebar.html",
        "navbar": "app/navbar.html",
        "main": "app/main.html",
        "footer": "app/footer.html",
    },
    "page": {
        "toolbar": "page/toolbar.html",
        "breadcrumbs": "page/breadcrumbs.html",
        "header": "page/header.html",
        "title": "page/title.html",
        "content": "page/content.html",
    },
    "content": {
        "shell": "content/shell.html",
        "sidebar_left": "content/sidebar-left.html",
        "sidebar_right": "content/sidebar-right.html",
        "main": "content/main.html",
    },
    "sidebar": {
        "base": "sidebar/base.html",
        "menu_item": "sidebar/menu-item.html",
        "menu_section": "sidebar/menu-section.html",
        "brand": "sidebar/brand.html",
    },
}
```

Use in views or context processors to validate components exist.

---

## Priority 3: Configuration Improvements

### 3.1 Enhance PAGE_CONFIG Schema

Add validation and defaults:

```python
# cotton_layouts/conf.py

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DEFAULT_PAGE_CONFIG = {
    "layout": "sidebar",
    "brand": {
        "text": "",
        "image_light": None,
        "image_dark": None,
        "icon_light": None,
        "icon_dark": None,
    },
    "navigation": {
        "toggle_at": "lg",
        "collapsible": True,
        "sidebar": {
            "width": "280px",
            "max_width": "320px",
            "min_width": "200px",
        },
    },
    "footer": {
        "visible": True,
        "sticky": False,  # False, True, or breakpoint ('sm', 'md', 'lg', 'xl', 'xxl')
    },
    "actions": [],
}

def get_page_config():
    """Get validated PAGE_CONFIG with defaults."""
    config = {**DEFAULT_PAGE_CONFIG}
    user_config = getattr(settings, "PAGE_CONFIG", {})
    
    # Deep merge user config
    for key, value in user_config.items():
        if isinstance(value, dict) and key in config:
            config[key] = {**config[key], **value}
        else:
            config[key] = value
    
    # Validate
    if config["layout"] not in ("sidebar", "navbar", "both"):
        raise ImproperlyConfigured(
            f"PAGE_CONFIG['layout'] must be 'sidebar', 'navbar', or 'both', got {config['layout']}"
        )
    
    return config
```

Update context processor:

```python
# cotton_layouts/context_processors.py

from .conf import get_page_config

def page_config(request):
    """Provide validated PAGE_CONFIG to all templates."""
    return {"page_config": get_page_config()}
```

### 3.2 Add TypeScript Type Definitions

Create `types/page_config.d.ts`:

```typescript
interface BrandConfig {
  text?: string;
  image_light?: string;
  image_dark?: string;
  icon_light?: string;
  icon_dark?: string;
}

interface SidebarConfig {
  width?: string;
  max_width?: string;
  min_width?: string;
}

interface NavigationConfig {
  toggle_at?: 'sm' | 'md' | 'lg' | 'xl' | 'xxl';
  collapsible?: boolean;
  sidebar?: SidebarConfig;
}

interface FooterConfig {
  visible?: boolean;
  sticky?: boolean | 'sm' | 'md' | 'lg' | 'xl' | 'xxl';
}

interface ActionWidget {
  icon: string;
  text: string;
  href: string;
  target?: string;
}

interface PageConfig {
  layout: 'sidebar' | 'navbar' | 'both';
  brand?: BrandConfig;
  navigation?: NavigationConfig;
  footer?: FooterConfig;
  actions?: ActionWidget[];
}

declare global {
  interface Window {
    PAGE_CONFIG: PageConfig;
  }
}
```

---

## Priority 4: Documentation Enhancements

### 4.1 Create Comprehensive Component Documentation

For each component, document:

```markdown
## Component: app/sidebar.html

### Purpose
The site-level navigation sidebar that contains the main application menu.

### Class Name
`.site-sidebar`

### Template Path
`cotton/app/sidebar.html`

### Usage
```html
<c-app.sidebar :brand="page_config.brand" collapsible="True">
  <c-sidebar.menu-item href="/" icon="home" text="Dashboard" />
</c-app.sidebar>
```

### Attributes
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `brand` | dict | - | Brand configuration (text, logo, icons) |
| `collapsible` | bool | False | Enable icon-only collapse mode |
| `width` | str | 280px | Sidebar width |

### CSS Variables
```css
--site-sidebar-width: 280px;
--site-sidebar-collapsed-width: 64px;
--site-sidebar-bg: #ffffff;
```

### JavaScript
Handled by `site-sidebar.js` for collapse/expand functionality.

### Accessibility
- Uses `<nav>` with `aria-label="Site navigation"`
- Keyboard navigable menu items
- Focus management on collapse/expand
```

### 4.2 Create Visual Hierarchy Diagram

Add SVG diagram to README showing the three levels:

```
┌─────────────────────────────────────────────────────────────┐
│ .app-shell (Level 1: Application Shell)                    │
│ ┌──────────────┐ ┌────────────────────────────────────────┐│
│ │.site-sidebar │ │ .app-column                            ││
│ │              │ │ ┌────────────────────────────────────┐ ││
│ │  Site Nav    │ │ │ .site-navbar                       │ ││
│ │              │ │ └────────────────────────────────────┘ ││
│ │              │ │ ┌────────────────────────────────────┐ ││
│ │              │ │ │ .app-main (Level 2: Page Content)  │ ││
│ │              │ │ │ ┌────────────────────────────────┐ │ ││
│ │              │ │ │ │ .page-toolbar                  │ │ ││
│ │              │ │ │ ├────────────────────────────────┤ │ ││
│ │              │ │ │ │ .page-breadcrumbs              │ │ ││
│ │              │ │ │ ├────────────────────────────────┤ │ ││
│ │              │ │ │ │ .page-header                   │ │ ││
│ │              │ │ │ ├────────────────────────────────┤ │ ││
│ │              │ │ │ │ .page-content                  │ │ ││
│ │              │ │ │ │ ┌──────────────────────────┐   │ │ ││
│ │              │ │ │ │ │ Level 3: Content Layout  │   │ │ ││
│ │              │ │ │ │ │ .content-shell           │   │ │ ││
│ │              │ │ │ │ ├──────┬────────┬─────────┤   │ │ ││
│ │              │ │ │ │ │.left │.content│ .right  │   │ │ ││
│ │              │ │ │ │ │side  │ -main  │ sidebar │   │ │ ││
│ │              │ │ │ │ │bar   │        │         │   │ │ ││
│ │              │ │ │ │ └──────┴────────┴─────────┘   │ │ ││
│ │              │ │ │ └────────────────────────────────┘ │ ││
│ │              │ │ └────────────────────────────────────┘ ││
│ │              │ │ ┌────────────────────────────────────┐ ││
│ │              │ │ │ .app-footer                        │ ││
│ │              │ │ └────────────────────────────────────┘ ││
│ └──────────────┘ └────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Add Interactive Examples

Create a demo page showing all three levels with live collapse/expand:

- `/demo/structure/` - Interactive structure visualization
- `/demo/app-shell/` - Outer layout examples
- `/demo/page-elements/` - Page component examples  
- `/demo/content-layout/` - Inner layout examples

---

## Priority 5: Testing & Quality Assurance

### 5.1 Add Component Tests

```python
# tests/test_components.py

import pytest
from django.template import Context, Template

@pytest.mark.parametrize("component,expected_class", [
    ("app/shell.html", "app-shell"),
    ("app/sidebar.html", "site-sidebar"),
    ("app/navbar.html", "site-navbar"),
    ("app/main.html", "app-main"),
    ("app/footer.html", "app-footer"),
    ("page/toolbar.html", "page-toolbar"),
    ("content/shell.html", "content-shell"),
    ("content/sidebar-left.html", "content-sidebar-left"),
])
def test_component_uses_correct_class(component, expected_class):
    """Verify components use semantic class names."""
    template = Template(f"{{% load cotton %}}{{% c-{component.replace('/', '.')} %}}")
    html = template.render(Context({}))
    assert expected_class in html
```

### 5.2 Add SCSS Linting

Configure stylelint with naming conventions:

```json
// .stylelintrc.json
{
  "extends": "stylelint-config-standard-scss",
  "rules": {
    "selector-class-pattern": [
      "^(app|site|page|content|sidebar|menu|navbar)(-[a-z]+)*$",
      {
        "message": "Class names must follow hierarchy: app-, site-, page-, content-, sidebar-, menu-, navbar-"
      }
    ],
    "custom-property-pattern": [
      "^(app|site|page|content|sidebar|navbar)(-[a-z]+)*$",
      {
        "message": "CSS variables must follow hierarchy: --app-, --site-, --page-, --content-"
      }
    ]
  }
}
```

### 5.3 Add Accessibility Tests

```python
# tests/test_accessibility.py

import pytest
from django.template import Context, Template

def test_site_sidebar_has_nav_role():
    """Site sidebar should use <nav> with aria-label."""
    template = Template("{% load cotton %}{% c-app.sidebar %}")
    html = template.render(Context({}))
    assert '<nav' in html
    assert 'aria-label' in html

def test_menu_items_keyboard_accessible():
    """Menu items should be keyboard navigable."""
    template = Template("{% load cotton %}{% c-sidebar.menu-item href='/' text='Home' %}")
    html = template.render(Context({}))
    assert '<a' in html
    assert 'href' in html
```

---

## Priority 6: Developer Experience

### 6.1 Add Debug Mode

```python
# cotton_layouts/conf.py

DEBUG_MODE = getattr(settings, "COTTON_LAYOUTS_DEBUG", settings.DEBUG)

if DEBUG_MODE:
    # Add data attributes showing component source
    # Log configuration warnings
    # Highlight layout boundaries in browser
```

Add to templates:

```html
{% if debug %}
  data-component="app.sidebar"
  data-file="cotton/app/sidebar.html"
{% endif %}
```

### 6.2 Create CLI Tool

```python
# cotton_layouts/management/commands/layout_check.py

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Check layout configuration and component usage"
    
    def handle(self, *args, **options):
        # Validate PAGE_CONFIG
        # Check for deprecated class names in templates
        # Report unused components
        # Suggest optimizations
```

Usage:
```bash
python manage.py layout_check
python manage.py layout_check --strict  # Fail on deprecation warnings
```

### 6.3 Add Hot Reload for Development

Integrate with django-browser-reload for instant updates:

```python
# settings.py (dev only)
if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]
```

---

## Priority 7: Performance Optimizations

### 7.1 Lazy Load Components

Only load JavaScript for components actually used on the page:

```html
<!-- base.html -->
<script>
  // Detect which components are present
  const hasContentSidebars = document.querySelector('.content-sidebar-left, .content-sidebar-right');
  const hasSiteSidebar = document.querySelector('.site-sidebar');
  
  // Conditionally load JS
  if (hasContentSidebars) {
    import('{% static "js/content-sidebars.js" %}');
  }
  if (hasSiteSidebar) {
    import('{% static "js/site-sidebar.js" %}');
  }
</script>
```

### 7.2 Optimize SCSS Compilation

Split into smaller, cacheable files:

```scss
// main.scss
@import "critical";  // Above-the-fold styles

// lazy.scss (loaded async)
@import "content-layout";
@import "advanced-components";
```

### 7.3 Add CSS Purging

Configure django-compressor to remove unused CSS in production:

```python
# settings.py
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
        "compressor.filters.template.TemplateFilter",  # Remove unused classes
    ],
}
```

---

## Summary: Implementation Roadmap

### Phase 1: Foundation (v0.2 - Next Release)
- ✅ Create STRUCTURE_AND_NAMING.md
- ✅ Update README with architecture section
- ✅ Update instructions with naming conventions
- ☐ Add backwards-compatible class aliases
- ☐ Create _page.scss and _footer.scss
- ☐ Rename _layout.scss → _outer-layout.scss
- ☐ Rename _inner-layout.scss → _content-layout.scss

### Phase 2: Migration (v0.3 - 2 weeks)
- ☐ Update all package templates to new names
- ☐ Rename JavaScript files
- ☐ Add component tests
- ☐ Add configuration validation
- ☐ Mark old class names as deprecated

### Phase 3: Enhancement (v0.4 - 1 month)
- ☐ Reorganize template directory structure
- ☐ Create component documentation
- ☐ Add interactive examples
- ☐ Implement footer component
- ☐ Add layout_check management command

### Phase 4: Optimization (v0.5 - 2 months)
- ☐ Add lazy loading
- ☐ Optimize SCSS compilation
- ☐ Add accessibility tests
- ☐ Performance profiling

### Phase 5: Stabilization (v1.0 - 3 months)
- ☐ Remove deprecated aliases (breaking change)
- ☐ Finalize API
- ☐ Complete documentation
- ☐ Production-ready release

---

## Immediate Next Steps

1. **Rename SCSS files** (15 min)
2. **Add class aliases** for backwards compatibility (30 min)
3. **Update standard.html** to use new class names (15 min)
4. **Test theme customization** still works (30 min)
5. **Create _footer.scss** with sticky/flow logic (1 hour)
6. **Document footer configuration** in README (30 min)

**Total Time: ~3.5 hours** for immediate structural improvements.

---

## Long-term Vision

By v1.0, django-cotton-layouts should be:

1. **Semantically clear** - Class names describe purpose and hierarchy
2. **Easy to theme** - CSS variables for all customization points
3. **Accessible** - WCAG AA compliant out of the box
4. **Performant** - Lazy loading, optimized bundles
5. **Well-documented** - Examples, API docs, guides
6. **Developer-friendly** - Debug tools, validation, helpful errors
7. **Production-ready** - Used in real projects, battle-tested

The naming standardization is the foundation for all these improvements.
