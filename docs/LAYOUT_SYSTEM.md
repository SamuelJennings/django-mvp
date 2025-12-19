# Layout System Documentation

## Page Structure

### HTML Structure
```html
<body class="layout-{mode} toggle-at-{breakpoint}">
  <div class="sidebar-layout">
    <aside class="demo-sidebar offcanvas offcanvas-start" id="mainSidebar">
      <div class="offcanvas-header">
        <div id="mainSidebarLabel"><!-- Sidebar title --></div>
        <button class="btn-close hide-if-sidebar-visible" data-bs-dismiss="offcanvas"></button>
      </div>
      <div class="offcanvas-body">
        <!-- Sidebar navigation content -->
      </div>
    </aside>
    
    <div class="main-column">
      <nav class="navbar">
        <button class="show-if-sidebar-hidden" data-bs-toggle="offcanvas" data-bs-target="#mainSidebar">
          <!-- Hamburger button -->
        </button>
        <nav class="hide-if-sidebar-hidden">
          <!-- Navbar menu items -->
        </nav>
        <!-- Action buttons (always visible) -->
      </nav>
      
      <main class="main-content">
        <!-- Page content -->
      </main>
    </div>
  </div>
</body>
```

### Key Structural Elements

#### Container Elements
- `.sidebar-layout` - Root flex container for the layout
- `.main-column` - Right column containing navbar and content

#### Sidebar
- `.demo-sidebar` - The main sidebar element
- `#mainSidebar` - Sidebar ID (required for offcanvas targeting)
- `.offcanvas.offcanvas-start` - Bootstrap offcanvas classes
- `.collapsible` - Makes sidebar collapsible (optional)
- `.collapsed` - Applied when sidebar is in collapsed state

#### Navbar
- `.navbar` - Top navigation bar
- `.show-if-sidebar-hidden` - Hamburger button container
- `.hide-if-sidebar-hidden` - Navbar menu items container

#### Content
- `.main-content` - Main scrollable content area

## Layout Modes

Layout modes are controlled by two body classes:
1. `layout-{mode}` - Determines which elements are visible
2. `toggle-at-{breakpoint}` - Sets responsive breakpoint behavior

### Mode: `layout-navbar`

**Navbar Only Layout**

```html
<body class="layout-navbar toggle-at-lg">
```

**Desktop (≥992px):**
- Sidebar: Always offcanvas (never in-flow)
- Navbar: Visible
- Navbar menu: Visible
- Hamburger: Hidden

**Mobile (<992px):**
- Sidebar: Offcanvas
- Navbar: Visible
- Navbar menu: Hidden
- Hamburger: Visible

**Use Case:** Simple applications, marketing sites

---

### Mode: `layout-sidebar`

**Sidebar Only Layout**

```html
<body class="layout-sidebar toggle-at-lg">
```

**Desktop (≥992px):**
- Sidebar: In-flow (260px width)
- Navbar: Completely hidden
- Navbar menu: N/A (navbar hidden)
- Hamburger: N/A (navbar hidden)

**Mobile (<992px):**
- Sidebar: Offcanvas
- Navbar: Visible
- Navbar menu: Hidden
- Hamburger: Visible

**Use Case:** Admin panels, file managers, data-centric interfaces

---

### Mode: `layout-both`

**Both Sidebar + Navbar Layout**

```html
<body class="layout-both toggle-at-lg">
```

**Desktop (≥992px):**
- Sidebar: In-flow (260px width)
- Navbar: Visible
- Navbar menu: Always hidden
- Hamburger: Hidden

**Mobile (<992px):**
- Sidebar: Offcanvas
- Navbar: Visible
- Navbar menu: Always hidden
- Hamburger: Visible

**Use Case:** Enterprise applications, SaaS platforms, complex admin panels

## Breakpoint Classes

Control when the sidebar switches between in-flow and offcanvas:

- `toggle-at-sm` - 576px
- `toggle-at-md` - 768px (tablets)
- `toggle-at-lg` - 992px (recommended default)
- `toggle-at-xl` - 1200px
- `toggle-at-xxl` - 1400px

## Utility Classes

### `.hide-if-sidebar-hidden`

Hides elements below the specified breakpoint.

**Applied to:** Navbar menu items

**Behavior:**
```scss
body.toggle-at-lg .hide-if-sidebar-hidden {
  @media (max-width: 991px) {
    display: none !important;
  }
}
```

**Layout-specific overrides:**
- `layout-sidebar`: Always hidden
- `layout-both`: Always hidden

---

### `.show-if-sidebar-hidden`

Shows elements only below the specified breakpoint.

**Applied to:** Hamburger button

**Behavior:**
```scss
body.toggle-at-lg .show-if-sidebar-hidden {
  display: none !important;
  
  @media (max-width: 991px) {
    display: block !important;
  }
}
```

**Shows when:**
- Below breakpoint (all modes)

**Hidden when:**
- Above breakpoint (all modes)

---

### `.hide-if-sidebar-visible`

Hides elements when sidebar is in the document flow (in-flow), shows when offcanvas.

**Applied to:** Offcanvas dismiss button (X)

**Behavior:**
```scss
body.toggle-at-lg .hide-if-sidebar-visible {
  // Hide above breakpoint (when sidebar is in-flow)
  @media (min-width: 992px) {
    display: none !important;
  }
  
  // Show below breakpoint (when sidebar is offcanvas)
  @media (max-width: 991px) {
    display: block !important;
  }
}
```

**Layout-specific overrides:**
- `layout-navbar`: Always shown (sidebar always offcanvas)

**Shows when:**
- Sidebar is offcanvas (below breakpoint in sidebar/both modes)
- Always in navbar-only mode

**Hidden when:**
- Sidebar is in-flow (above breakpoint in sidebar/both modes)

---

### `.show-on-collapse`

Shows element only when sidebar is collapsed.

**Applied to:** Icon-only indicators, tooltips

**Behavior:**
```scss
.show-on-collapse {
  display: none; // Hidden by default
}

.demo-sidebar.collapsed .show-on-collapse {
  display: block !important;
}
```

---

### `.hide-on-collapse`

Hides element when sidebar is collapsed.

**Applied to:** Text labels, headings, full-width elements

**Behavior:**
```scss
.demo-sidebar.collapsed .hide-on-collapse {
  display: none !important;
}
```

---

### `.show-on-expanded`

Shows element only when sidebar is expanded (not collapsed).

**Behavior:**
```scss
.demo-sidebar.collapsed .show-on-expanded {
  display: none !important;
}
```

---

### `.hide-on-expanded`

Hides element when sidebar is expanded.

**Applied to:** Collapsed-state indicators

**Behavior:**
```scss
.hide-on-expanded {
  display: none;
}

.demo-sidebar:not(.collapsed) .hide-on-expanded {
  display: none !important;
}
```

## Sidebar Collapse Feature

### Overview

When the sidebar has the `.collapsible` class, it can be collapsed to show only icons (60px width) when in-flow.

### Collapse Behavior

**Collapsed State:**
- Sidebar width: 60px
- Only icons visible
- Text labels hidden
- Smooth transition (0.3s)

**When Collapse is Available:**
- `layout-sidebar` mode: Above breakpoint (when in-flow)
- `layout-both` mode: Above breakpoint (when in-flow)
- `layout-navbar` mode: Never (sidebar always offcanvas)

### Collapse Toggle Button

The collapse toggle appears in the same position as the offcanvas dismiss button:

```html
<button type="button" 
        class="sidebar-collapse-toggle"
        onclick="document.getElementById('mainSidebar').classList.toggle('collapsed')">
  <i class="bi bi-chevron-left"></i>
</button>
```

**Button Behavior:**
- Hidden by default
- Only visible when sidebar is in-flow AND has `.collapsible` class
- Rotates 180° when collapsed
- Positioned absolutely at top-right of sidebar

### Example Implementation

```html
<aside class="demo-sidebar offcanvas offcanvas-start collapsible" id="mainSidebar">
  <div class="offcanvas-header">
    <div id="mainSidebarLabel">
      <i class="bi bi-grid hide-on-collapse"></i>
      <h6 class="hide-on-collapse">My App</h6>
    </div>
    <button class="btn-close hide-if-sidebar-visible" 
            data-bs-dismiss="offcanvas"></button>
    <button class="sidebar-collapse-toggle"
            onclick="this.closest('.demo-sidebar').classList.toggle('collapsed')">
      <i class="bi bi-chevron-left"></i>
    </button>
  </div>
  <div class="offcanvas-body">
    <nav>
      <a href="#" title="Dashboard">
        <i class="bi bi-house"></i>
        <span class="hide-on-collapse">Dashboard</span>
      </a>
    </nav>
  </div>
</aside>
```

## Layout Mode Comparison

| Mode | Desktop Sidebar | Desktop Navbar | Desktop Menu | Mobile Sidebar | Mobile Navbar | Mobile Menu | Mobile Hamburger |
|------|----------------|----------------|--------------|----------------|---------------|-------------|------------------|
| **navbar** | Offcanvas | Visible | Visible | Offcanvas | Visible | Hidden | Visible |
| **sidebar** | In-flow (260px) | Hidden | N/A | Offcanvas | Visible | Hidden | Visible |
| **both** | In-flow (260px) | Visible | Hidden | Offcanvas | Visible | Hidden | Visible |

## CSS Variables

The sidebar width when in-flow can be customized:

```scss
body.layout-sidebar.toggle-at-lg,
body.layout-both.toggle-at-lg {
  @media (min-width: 992px) {
    .sidebar-layout > .demo-sidebar {
      width: 260px; // Customize this value
    }
  }
}
```

## Implementation Example

```html
<!-- Navbar-only layout with lg breakpoint -->
<body class="layout-navbar toggle-at-lg">
  <div class="sidebar-layout">
    <aside class="demo-sidebar offcanvas offcanvas-start" id="mainSidebar">
      <div class="offcanvas-header">
        <div id="mainSidebarLabel">My App</div>
        <button class="btn-close hide-if-sidebar-visible" 
                data-bs-dismiss="offcanvas"></button>
      </div>
      <div class="offcanvas-body">
        <!-- Navigation links -->
      </div>
    </aside>
    
    <div class="main-column">
      <nav class="navbar">
        <button class="show-if-sidebar-hidden" 
                data-bs-toggle="offcanvas" 
                data-bs-target="#mainSidebar">☰</button>
        <nav class="hide-if-sidebar-hidden">
          <a href="#">Home</a>
          <a href="#">Products</a>
        </nav>
      </nav>
      
      <main class="main-content">
        <!-- Your content here -->
      </main>
    </div>
  </div>
</body>
```
