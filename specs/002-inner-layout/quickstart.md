# Quick Start: Inner Layout Component

**Feature**: 002-inner-layout  
**Version**: 1.0.0  
**Date**: 2025-12-23

## What is the Inner Layout?

The inner layout component provides a flexible multi-column layout for content pages with optional sidebars. It's designed for use **inside** the outer layout system (after `.page-content`) to create sophisticated content layouts without writing custom CSS.

**Key Features**:
- Zero-configuration default (works out of the box)
- Optional primary sidebar (left) and secondary sidebar (right)
- Responsive: Sidebars become offcanvas overlays on mobile
- Collapsible sidebars for icon-only navigation
- Fully accessible (ARIA landmarks, keyboard navigation)
- Customizable via data attributes

## Basic Usage

### 1. Simple Content Layout (No Sidebars)

The simplest usage - just main content with no sidebars.

```django-html
{% load cotton %}

{% block content %}
<c-layouts.inner>
  <h1>Welcome to My Page</h1>
  <p>This is the main content area.</p>
  <p>It automatically expands to fill the available width.</p>
</c-layouts.inner>
{% endblock %}
```

**Result**: Single-column layout with main content filling the width.

---

### 2. Layout with Primary Sidebar (Left)

Add a navigation sidebar on the left.

```django-html
{% load cotton %}

{% block content %}
<c-layouts.inner>
  {# Primary Sidebar (Left) #}
  <c-slot name="primary_sidebar">
    <nav>
      <h3>Navigation</h3>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  </c-slot>
  
  {# Main Content #}
  <h1>Page Title</h1>
  <p>Main content goes here.</p>
</c-layouts.inner>
{% endblock %}
```

**Result**: 
- Desktop (≥768px): Two-column layout with 280px sidebar on left
- Mobile (<768px): Sidebar becomes toggleable offcanvas overlay

---

### 3. Layout with Secondary Sidebar (Right)

Add metadata or related content on the right.

```django-html
{% load cotton %}

{% block content %}
<c-layouts.inner>
  {# Secondary Sidebar (Right) #}
  <c-slot name="secondary_sidebar">
    <aside>
      <h4>Related Links</h4>
      <ul>
        <li><a href="/related1">Related Article 1</a></li>
        <li><a href="/related2">Related Article 2</a></li>
      </ul>
      
      <h4>Tags</h4>
      <div class="tags">
        <span class="badge bg-secondary">Django</span>
        <span class="badge bg-secondary">Python</span>
      </div>
    </aside>
  </c-slot>
  
  {# Main Content #}
  <article>
    <h1>Article Title</h1>
    <p>Article content here.</p>
  </article>
</c-layouts.inner>
{% endblock %}
```

**Result**: 
- Desktop: Two-column layout with 250px sidebar on right
- Mobile: Sidebar becomes offcanvas overlay

---

### 4. Full Layout with Both Sidebars

The most complex layout with navigation left and metadata right.

```django-html
{% load cotton %}

{% block content %}
<c-layouts.inner>
  {# Primary Sidebar (Left) - Navigation #}
  <c-slot name="primary_sidebar">
    <nav>
      <h3>Documentation</h3>
      <ul>
        <li><a href="/docs/intro">Introduction</a></li>
        <li><a href="/docs/setup">Setup</a></li>
        <li><a href="/docs/usage">Usage</a></li>
      </ul>
    </nav>
  </c-slot>
  
  {# Secondary Sidebar (Right) - Table of Contents #}
  <c-slot name="secondary_sidebar">
    <aside>
      <h4>On This Page</h4>
      <ul>
        <li><a href="#section1">Section 1</a></li>
        <li><a href="#section2">Section 2</a></li>
        <li><a href="#section3">Section 3</a></li>
      </ul>
    </aside>
  </c-slot>
  
  {# Main Content #}
  <article>
    <h1>Documentation Page</h1>
    <section id="section1">
      <h2>Section 1</h2>
      <p>Content for section 1.</p>
    </section>
    <section id="section2">
      <h2>Section 2</h2>
      <p>Content for section 2.</p>
    </section>
  </article>
</c-layouts.inner>
{% endblock %}
```

**Result**: 
- Desktop: Three-column layout (280px left, content, 250px right)
- Mobile: Both sidebars become offcanvas overlays

---

## Customization

### Custom Sidebar Widths

Change sidebar widths from defaults (280px primary, 250px secondary).

```django-html
<c-layouts.inner 
  primary_width="320px"
  secondary_width="300px">
  
  <c-slot name="primary_sidebar">
    <nav>Wide navigation sidebar</nav>
  </c-slot>
  
  <h1>Main Content</h1>
</c-layouts.inner>
```

---

### Custom Responsive Breakpoint

Change when sidebars switch to offcanvas (default is `md`/768px).

```django-html
<c-layouts.inner breakpoint="lg">
  <c-slot name="primary_sidebar">
    <nav>This sidebar stays visible up to 992px</nav>
  </c-slot>
  
  <h1>Main Content</h1>
</c-layouts.inner>
```

**Breakpoint Options**:
- `sm`: 576px
- `md`: 768px (default)
- `lg`: 992px
- `xl`: 1200px
- `xxl`: 1400px

---

### Add Spacing Between Columns

Use Bootstrap's gap utilities (0-5).

```django-html
<c-layouts.inner gap="3">
  <c-slot name="primary_sidebar">
    <nav>Navigation</nav>
  </c-slot>
  
  <h1>Main Content with 1rem gap</h1>
</c-layouts.inner>
```

**Gap Values**:
- `0`: No gap (default)
- `1`: 0.25rem
- `2`: 0.5rem
- `3`: 1rem
- `4`: 1.5rem
- `5`: 3rem

---

### Enable Collapsible Sidebar

Allow users to collapse sidebar to icon-only mode.

```django-html
<c-layouts.inner collapse_primary="true">
  <c-slot name="primary_sidebar">
    <nav class="sidebar-nav">
      <a href="/" class="nav-item">
        <i class="bi bi-house collapsed-only"></i>
        <span class="expanded-only">Home</span>
      </a>
      <a href="/about" class="nav-item">
        <i class="bi bi-info-circle collapsed-only"></i>
        <span class="expanded-only">About</span>
      </a>
      <a href="/contact" class="nav-item">
        <i class="bi bi-envelope collapsed-only"></i>
        <span class="expanded-only">Contact</span>
      </a>
    </nav>
  </c-slot>
  
  <h1>Main Content</h1>
</c-layouts.inner>
```

**How Collapse Works**:
- Toggle button appears on sidebar
- When collapsed: Only `.collapsed-only` elements visible (icons)
- When expanded: Only `.expanded-only` elements visible (text)
- **Note**: Collapse disabled on mobile (<768px) when sidebar is offcanvas

---

### Combine All Options

```django-html
<c-layouts.inner 
  primary_width="300px"
  secondary_width="280px"
  breakpoint="lg"
  gap="2"
  collapse_primary="true"
  collapse_secondary="true"
  class="my-custom-layout">
  
  <c-slot name="primary_sidebar">
    <nav>Fully customized sidebar</nav>
  </c-slot>
  
  <c-slot name="secondary_sidebar">
    <aside>Customized metadata</aside>
  </c-slot>
  
  <h1>Fully Customized Layout</h1>
</c-layouts.inner>
```

---

## Common Patterns

### Documentation Layout

```django-html
<c-layouts.inner collapse_primary="true">
  <c-slot name="primary_sidebar">
    {% include "docs/_navigation.html" %}
  </c-slot>
  
  <c-slot name="secondary_sidebar">
    {# Table of contents generated from headings #}
    <div id="toc"></div>
  </c-slot>
  
  <article class="prose">
    {{ content|safe }}
  </article>
</c-layouts.inner>
```

---

### Blog Post Layout

```django-html
<c-layouts.inner>
  <c-slot name="secondary_sidebar">
    <aside>
      <h4>About the Author</h4>
      <img src="{{ post.author.avatar }}" alt="{{ post.author.name }}">
      <p>{{ post.author.bio }}</p>
      
      <h4>Share This Post</h4>
      <div class="share-buttons">
        {# Share buttons #}
      </div>
      
      <h4>Related Posts</h4>
      {% for related in post.related_posts %}
        <a href="{{ related.url }}">{{ related.title }}</a>
      {% endfor %}
    </aside>
  </c-slot>
  
  <article class="blog-post">
    <h1>{{ post.title }}</h1>
    <div class="post-meta">
      <span>{{ post.date }}</span>
      <span>{{ post.author.name }}</span>
    </div>
    <div class="post-content">
      {{ post.content|safe }}
    </div>
  </article>
</c-layouts.inner>
```

---

### Dashboard Layout

```django-html
<c-layouts.inner 
  collapse_primary="true"
  gap="3">
  
  <c-slot name="primary_sidebar">
    <nav class="dashboard-nav">
      {% for item in dashboard_menu %}
        <a href="{{ item.url }}" class="nav-item">
          <i class="{{ item.icon }} collapsed-only"></i>
          <span class="expanded-only">{{ item.label }}</span>
        </a>
      {% endfor %}
    </nav>
  </c-slot>
  
  <div class="dashboard-content">
    <h1>{{ dashboard_title }}</h1>
    <div class="dashboard-widgets">
      {% for widget in widgets %}
        {% include widget.template %}
      {% endfor %}
    </div>
  </div>
</c-layouts.inner>
```

---

### List/Detail View

```django-html
<c-layouts.inner primary_width="300px">
  <c-slot name="primary_sidebar">
    <div class="item-list">
      <h3>{{ list_title }}</h3>
      <div class="list-group">
        {% for item in items %}
          <a href="{{ item.url }}" 
             class="list-group-item {% if item.id == current_item.id %}active{% endif %}">
            {{ item.title }}
          </a>
        {% endfor %}
      </div>
    </div>
  </c-slot>
  
  <div class="item-detail">
    <h1>{{ current_item.title }}</h1>
    <p>{{ current_item.description }}</p>
    {# Detail content #}
  </div>
</c-layouts.inner>
```

---

## Responsive Behavior

### Desktop (≥768px by default)

- Sidebars visible in layout
- Primary sidebar: 280px (left)
- Secondary sidebar: 250px (right)
- Main content: Expands to fill remaining width
- Collapse toggles visible (if enabled)

### Mobile (<768px by default)

- Sidebars hidden by default (offcanvas)
- Toggle buttons visible for each sidebar
- Main content uses full width
- Clicking toggle shows sidebar as overlay
- Backdrop dims main content
- Close button, Escape key, or backdrop click closes sidebar
- **Collapse disabled** in offcanvas mode

---

## Accessibility

### ARIA Landmarks

The component automatically adds proper ARIA landmarks:

- Main content: `role="main"`
- Sidebars: `role="complementary"`
- Offcanvas: `role="dialog"`, `aria-modal="true"`

### Keyboard Navigation

- **Tab**: Navigate through content and controls
- **Escape**: Close offcanvas
- **Enter/Space**: Activate toggle buttons

### Screen Readers

- All regions labeled via `aria-label`
- Toggle buttons have descriptive labels
- Offcanvas headers identify sidebar purpose

---

## JavaScript API (Optional)

For advanced use cases, you can control layout programmatically.

### Initialize

```javascript
const layout = new InnerLayoutManager();
layout.init();
```

### Toggle Collapse

```javascript
// Toggle primary sidebar collapse
layout.toggleCollapse('primary');

// Toggle secondary sidebar collapse
layout.toggleCollapse('secondary');
```

### Check State

```javascript
// Check if collapsed
if (layout.isCollapsed('primary')) {
  console.log('Primary sidebar is collapsed');
}

// Check if in offcanvas mode
if (layout.isOffcanvasMode()) {
  console.log('Mobile view active');
}
```

### Listen to Events

```javascript
// Listen for collapse events
document.addEventListener('innerlayout:collapsed', (event) => {
  console.log(`${event.detail.sidebar} collapsed`);
});

document.addEventListener('innerlayout:expanded', (event) => {
  console.log(`${event.detail.sidebar} expanded`);
});

// Listen for offcanvas mode changes
document.addEventListener('innerlayout:offcanvasmode', (event) => {
  if (event.detail.active) {
    console.log('Entered mobile view');
  }
});
```

---

## Styling Tips

### Custom Sidebar Background

```css
.content-sidebar-left {
  background: var(--bs-light);
  border-right: 1px solid var(--bs-border-color);
}

.content-sidebar-right {
  background: var(--bs-light);
  border-left: 1px solid var(--bs-border-color);
}
```

### Custom Main Content Padding

```css
.content-main {
  padding: 2rem;
}
```

### Override Sidebar Width Globally

```css
:root {
  --content-primary-width: 320px;
  --content-secondary-width: 280px;
}
```

### Sticky Sidebar Content

```css
.content-sidebar-left {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
```

---

## Troubleshooting

### Sidebar not showing

**Problem**: Sidebar declared but not visible.

**Solution**: Check if slot has content. Empty slots (whitespace only) don't render.

```django-html
{# This renders #}
<c-slot name="primary_sidebar">
  <nav>Content here</nav>
</c-slot>

{# This doesn't render (empty) #}
<c-slot name="primary_sidebar">
  
</c-slot>
```

---

### Collapse not working on mobile

**Expected**: Collapse is **disabled** when viewport < breakpoint (offcanvas mode).

**Reason**: Spec constraint - sidebars cannot collapse while in offcanvas mode.

**Solution**: This is intentional. Collapse works only at ≥breakpoint.

---

### Custom width not applying

**Problem**: Setting `primary_width="320px"` but sidebar still 280px.

**Solution**: Check for CSS specificity issues. Use `!important` if needed or increase specificity.

```css
.my-layout .content-sidebar-left {
  width: 320px !important;
}
```

---

### Icons not showing in collapsed mode

**Problem**: Icons missing when sidebar collapsed.

**Solution**: Add `.collapsed-only` class to icons:

```html
<a href="/" class="nav-item">
  <i class="bi bi-house collapsed-only"></i>
  <span class="expanded-only">Home</span>
</a>
```

---

## Next Steps

- **Full API Reference**: See [contracts/component-api.md](contracts/component-api.md)
- **CSS Classes**: See [contracts/css-classes.md](contracts/css-classes.md)
- **JavaScript API**: See [contracts/javascript-api.md](contracts/javascript-api.md)
- **Data Model**: See [data-model.md](data-model.md)
- **Examples**: Check the example app templates

---

## Support

For issues or questions:
- GitHub Issues: [github.com/your-repo/issues](https://github.com/your-repo/issues)
- Documentation: [docs/INNER_LAYOUT.md](../../../docs/INNER_LAYOUT.md)
