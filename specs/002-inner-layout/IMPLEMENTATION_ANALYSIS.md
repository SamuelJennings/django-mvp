# Inner Layout Implementation Analysis

**Created**: December 23, 2025  
**Purpose**: Comprehensive analysis of existing inner layout implementation  
**Spec Reference**: [spec.md](spec.md)

---

## Executive Summary

The existing inner layout implementation is **partially complete** with a solid foundation but **significant gaps** for meeting the specification requirements. The current implementation uses a mismatched naming strategy (mixing old `.inner-*` classes with new `.content-*` semantics via backwards-compat aliases), lacks offcanvas mode entirely, has no empty slot detection, and has no data attribute configuration system. The HTML template is minimal (7 lines), the CSS is comprehensive but uses outdated breakpoints, and JavaScript handles only collapse functionality with localStorage persistence.

**Status**: ~40% complete for spec requirements  
**Recommendation**: Refactor HTML template, extend CSS for offcanvas, add JS offcanvas handling, implement data attribute system, add empty slot detection logic.

---

## 1. Current Implementation Analysis

### 1.1 HTML Template: `mvp/templates/cotton/layouts/inner.html`

**File**: [mvp/templates/cotton/layouts/inner.html](../../mvp/templates/cotton/layouts/inner.html)  
**Lines**: 7 total

```django-html
<c-vars gap="0" class />
<div class="content-shell d-flex gap-{{ gap }} {{ class }}"
     {{ attrs }}>
  {{ primary_sidebar }}
  <div class="content-main flex-grow-1 overflow-auto">{{ slot }}</div>
  {{ secondary_sidebar }}
</div>
```

#### What Works ✅

1. **Basic Structure**: Clean flex-based layout with semantic wrapper (`.content-shell`)
2. **Slot System**: Uses Django-Cotton slots correctly:
   - `{{ slot }}` for default/unnamed content (main area)
   - `{{ primary_sidebar }}` for left sidebar (named slot)
   - `{{ secondary_sidebar }}` for right sidebar (named slot)
3. **Pass-through Attributes**: `{{ attrs }}` correctly forwards data attributes
4. **Bootstrap Integration**: Uses Bootstrap flex utilities (`d-flex`, `flex-grow-1`, `overflow-auto`)
5. **Gap Configuration**: Accepts configurable gap via `gap` c-var (default `"0"`)
6. **Class Extension**: Accepts additional classes via `class` c-var

#### What's Incomplete ⚠️

1. **No Empty Slot Detection** (FR-009): Template blindly renders `{{ primary_sidebar }}` and `{{ secondary_sidebar }}` regardless of content. **Empty slots will render empty `<aside>` containers that reserve layout space.**
2. **No Data Attribute Handling** (FR-006): While `{{ attrs }}` passes through attributes, there's **no logic to read and apply them** (e.g., `data-primary-width`, `data-breakpoint`, `data-gap`)
3. **No Offcanvas Structure** (FR-007a): Template only creates in-flow layout. **No Bootstrap offcanvas wrapper, no toggle buttons, no responsive mode switching.**
4. **No Collapse Toggles**: Template has no toggle buttons for collapse functionality (relies on external implementation)
5. **No ARIA Landmarks** (FR-011): Missing `role="complementary"` on sidebars, `role="main"` on content area, `aria-label` descriptors
6. **No Responsive Classes**: No classes to control hide/collapse breakpoint behavior

#### What Needs Replacement/Refactor 🔄

1. **Class Names**: Using old `.content-shell` (aliased to `.inner-layout` via backwards-compat). **Spec mandates semantic naming per STRUCTURE_AND_NAMING.md** - should use `.content-shell` as primary (already correct).
2. **Structure**: Needs conditional rendering for sidebars (empty slot detection)
3. **Offcanvas Wrapper**: Needs dual-mode structure (in-flow vs offcanvas) based on viewport
4. **Toggle Buttons**: Needs collapse and offcanvas toggle buttons with proper ARIA

---

### 1.2 CSS: `mvp/static/scss/_content-layout.scss`

**File**: [mvp/static/scss/_content-layout.scss](../../mvp/static/scss/_content-layout.scss)  
**Lines**: ~180 total (not all reviewed)

#### CSS Architecture: Variables

**Current CSS Variables** (defaults in SCSS):

```scss
// Primary (left) sidebar
--inner-primary-width: 250px           // Default width
--inner-primary-max-width: 300px       // Maximum width
--inner-primary-min-width: 60px        // Minimum width when collapsed

// Secondary (right) sidebar  
--inner-secondary-width: 250px
--inner-secondary-max-width: 300px
--inner-secondary-min-width: 60px
```

**Additional Variables** (found in `example/static/scss/_custom-theme-vars.scss`):

```scss
--inner-primary-bg: #fafafa
--inner-primary-border: #e5e7eb
--inner-secondary-bg: #fafafa
--inner-secondary-border: #e5e7eb
--inner-main-bg: #ffffff
--inner-main-padding: 1.5rem
--inner-toggle-bg: rgba(255, 255, 255, 0.9)
--inner-toggle-border: #d1d5db
```

**Gap vs Spec**: Spec specifies **280px for primary_sidebar, 250px for secondary_sidebar**. Current implementation uses **250px for both**. ⚠️ **Mismatch**

#### CSS Architecture: Class Names

**Current Classes** (from `_content-layout.scss` and `_old_layout.scss`):

| Class | Element | Purpose | Status |
|-------|---------|---------|--------|
| `.inner-layout` | Container | Flex wrapper for inner layout | ✅ In use (aliased from `.content-shell`) |
| `.inner-primary` | Sidebar | Left sidebar structural styles | ✅ In use (aliased from `.content-sidebar-left`) |
| `.inner-secondary` | Sidebar | Right sidebar structural styles | ✅ In use (aliased from `.content-sidebar-right`) |
| `.inner-main` | Content | Main content area | ✅ In use (aliased from `.content-main`) |
| `.collapsed` | Modifier | Collapsed state for sidebars | ✅ Working |
| `.collapsed-only` | Utility | Show only when collapsed | ✅ Working |
| `.expanded-only` | Utility | Show only when expanded | ✅ Working |
| `.inner-primary-toggle` | Button | Toggle button for primary sidebar | ⚠️ Deprecated (but aliased) |
| `.inner-secondary-toggle` | Button | Toggle button for secondary sidebar | ⚠️ Deprecated (but aliased) |
| `.inner-sidebar-content` | Wrapper | Content wrapper inside sidebar | ✅ Working |

**Backwards Compatibility**: File `_backwards-compat.scss` provides SCSS `@extend` aliases:
- `.content-shell` → `.inner-layout`
- `.content-sidebar-left` → `.inner-primary`
- `.content-sidebar-right` → `.inner-secondary`
- `.content-main` → `.inner-main`

**Gap vs Spec**: Spec requires semantic names (`.content-shell`, `.content-sidebar-left`, `.content-sidebar-right`, `.content-main`) as **primary**. Current implementation has this backwards - old `.inner-*` classes are primary, new `.content-*` classes are aliases. ⚠️ **Needs inversion**

#### CSS Architecture: Responsive Behavior

**Current Breakpoint** (from `_content-layout.scss:7-16`):

```scss
.inner-layout {
  min-height: 0;

  /* Mobile: Stack vertically */
  @media (max-width: 991px) {  // ⚠️ 991px = Bootstrap's lg-1, NOT md
    flex-direction: column !important;

    .inner-primary,
    .inner-secondary {
      width: 100% !important;
      max-width: none !important;
      border: none !important;
      border-bottom: 1px solid var(--bs-border-color) !important;
    }
  }
}
```

**Issues**:
1. **Wrong Breakpoint**: Using `max-width: 991px` (just below Bootstrap `lg: 992px`). **Spec requires `md: 768px`**. ⚠️ **Mismatch**
2. **Wrong Responsive Mode**: Stacks vertically (changes to column layout). **Spec requires switch to offcanvas mode (slide-in from off-page), not stacking**. ❌ **Major gap**
3. **No Offcanvas Classes**: No CSS for `.offcanvas` mode, no slide-in transitions, no backdrop

**Found in**: `_old_layout.scss:334` also has same `@media (max-width: 991px)` breakpoint

#### CSS Architecture: Collapse Transitions

**Collapse Implementation** (from `_content-layout.scss:60-80`):

```scss
.inner-primary {
  position: relative;
  transition: all 0.3s ease;  // ✅ Smooth transitions
  width: var(--inner-primary-width, 250px);
  max-width: var(--inner-primary-max-width, 300px);
  min-width: var(--inner-primary-min-width, 60px);
  flex-shrink: 0;
  overflow-y: auto;
  overflow-x: hidden;

  &.collapsed {
    width: var(--inner-primary-min-width, 60px) !important;
    min-width: var(--inner-primary-min-width, 60px) !important;
    overflow-x: visible !important;  // ✅ Allows dropdowns to escape

    .inner-sidebar-content > *:not(.collapsed-only) {
      display: none;  // ✅ Hides expanded content
    }

    .expanded-only {
      display: none !important;
    }

    .collapsed-only {
      display: block !important;  // ✅ Shows collapsed content
    }
  }

  &:not(.collapsed) {
    .collapsed-only {
      display: none !important;
    }
  }
}
```

**What Works** ✅:
1. Smooth 0.3s transitions
2. Proper width reduction to `min-width` when collapsed
3. Content visibility toggling (`.collapsed-only`, `.expanded-only`)
4. `overflow-x: visible` in collapsed state for dropdown menus
5. Prevents accidental layout breaks with `flex-shrink: 0`

**What Works** (Scrollbar styling) ✅:
```scss
/* Scrollbar styling */
scrollbar-width: thin;
scrollbar-color: transparent transparent;

&::-webkit-scrollbar {
  width: 8px;
}

&::-webkit-scrollbar-track {
  background: transparent;
}

&::-webkit-scrollbar-thumb {
  background: transparent;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

&:hover {
  scrollbar-color: rgba(0, 0, 0, 0.3) transparent;

  &::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.3);

    &:hover {
      background: rgba(0, 0, 0, 0.5);
    }
  }
}
```

**Analysis**: Well-implemented scrollbar theming with hover reveal. Cross-browser compatible (Firefox `scrollbar-width`, Webkit `::-webkit-scrollbar-*`).

#### CSS Architecture: Issues & Gaps

1. **No Offcanvas Mode** ❌: Zero CSS for offcanvas behavior (slide-in from off-page, backdrop, toggle)
2. **Wrong Breakpoint** ⚠️: Using `991px` instead of `768px` (md)
3. **Wrong Responsive Behavior** ⚠️: Stacking instead of offcanvas
4. **No Collapse Constraint** ❌: No CSS to enforce "cannot collapse while in offcanvas mode" (FR-007b)
5. **Width Defaults Mismatch** ⚠️: `250px` for primary (spec: `280px`)
6. **Class Naming Inverted** ⚠️: Old `.inner-*` primary, new `.content-*` aliased (should be opposite)
7. **No Empty Slot Handling** ❌: No `.content-sidebar-left:empty` or similar to hide empty sidebars

---

### 1.3 JavaScript: `mvp/static/js/inner_layout.js`

**File**: [mvp/static/js/inner_layout.js](../../mvp/static/js/inner_layout.js)  
**Lines**: 126 total  
**Format**: Vanilla JavaScript (ES5/ES6 compatible, IIFE pattern)

#### JavaScript: What Works ✅

1. **Collapse Functionality**: Fully implemented with proper state management
   ```javascript
   function toggleSidebar(sidebar, storageKey) {
     sidebar.classList.toggle('collapsed')
     const isCollapsed = sidebar.classList.contains('collapsed')
     saveState(storageKey, isCollapsed)
   }
   ```

2. **Independent State Management**: Separate localStorage keys for left/right sidebars
   ```javascript
   const STORAGE_KEY_LEFT = 'contentSidebarLeftCollapsed'
   const STORAGE_KEY_RIGHT = 'contentSidebarRightCollapsed'
   ```

3. **State Persistence**: Survives page reloads via localStorage
   ```javascript
   function saveState(key, isCollapsed) {
     try {
       localStorage.setItem(key, isCollapsed.toString())
     } catch (e) {
       console.warn('Failed to save content layout state:', e)
     }
   }
   ```

4. **No-Flash Restoration**: Disables transitions on page load to prevent flash
   ```javascript
   function restoreSidebarState(sidebar, storageKey) {
     const isCollapsed = getState(storageKey)

     if (isCollapsed) {
       sidebar.style.transition = 'none'  // Disable temporarily
       sidebar.classList.add('collapsed')
       sidebar.offsetHeight  // Force reflow
       requestAnimationFrame(() => {
         sidebar.style.transition = ''  // Re-enable
       })
     }
   }
   ```

5. **Error Handling**: Try-catch for localStorage (handles private browsing, quota exceeded)

6. **Proper Initialization**: Handles both `DOMContentLoaded` and already-loaded states
   ```javascript
   if (document.readyState === 'loading') {
     document.addEventListener('DOMContentLoaded', () => {
       initLeftSidebars()
       initRightSidebars()
     })
   } else {
     initLeftSidebars()
     initRightSidebars()
   }
   ```

7. **Selector Specificity**: Only initializes sidebars marked as collapsible
   ```javascript
   const sidebars = document.querySelectorAll('.content-sidebar-left[data-collapsible="True"]')
   ```

#### JavaScript: What's Missing ❌

1. **No Offcanvas Mode** (FR-007a): Zero implementation for slide-in behavior
   - No viewport size detection (matchMedia for 768px breakpoint)
   - No Bootstrap offcanvas integration
   - No mode switching logic (in-flow → offcanvas)
   - No toggle button handling for offcanvas

2. **No Data Attribute Reading** (FR-006): Doesn't read or apply config from data attributes
   - No reading `data-primary-width`, `data-secondary-width`
   - No reading `data-breakpoint` for custom responsive behavior
   - No reading `data-gap` or other layout config

3. **No Empty Slot Detection** (FR-009): No logic to detect or hide empty sidebars

4. **No Collapse Constraint** (FR-007b): No enforcement of "cannot collapse while in offcanvas mode"

5. **No Responsive Behavior**: No viewport resize listener, no breakpoint detection

6. **Hardcoded Selectors**: Uses old class names (`.content-sidebar-left`, `.content-sidebar-right`, `.content-sidebar-toggle-left`, `.content-sidebar-toggle-right`)
   - **Note**: These ARE the correct new semantic names, so this is actually fine per spec

#### JavaScript: Code Quality Assessment ✅

- **Pattern**: IIFE (Immediately Invoked Function Expression) for namespace isolation ✅
- **Browser Compatibility**: ES5/ES6 compatible, no transpilation needed ✅
- **Performance**: Efficient selectors, minimal DOM manipulation ✅
- **Accessibility**: Proper event handling (preventDefault, stopPropagation) ✅
- **Maintainability**: Clear function names, good separation of concerns ✅

---

## 2. CSS Architecture Deep Dive

### 2.1 CSS Variables Summary

**Width Configuration**:
```scss
// Defaults in _content-layout.scss
--inner-primary-width: 250px           // ⚠️ Spec: 280px
--inner-primary-max-width: 300px       // ✅ Reasonable
--inner-primary-min-width: 60px        // ✅ Icon-width

--inner-secondary-width: 250px         // ✅ Matches spec
--inner-secondary-max-width: 300px     // ✅ Reasonable
--inner-secondary-min-width: 60px      // ✅ Icon-width
```

**Theming Variables** (optional, from example app):
```scss
--inner-primary-bg: #fafafa            // Background color
--inner-primary-border: #e5e7eb        // Border color
--inner-secondary-bg: #fafafa
--inner-secondary-border: #e5e7eb
--inner-main-bg: #ffffff
--inner-main-padding: 1.5rem
--inner-toggle-bg: rgba(255, 255, 255, 0.9)
--inner-toggle-border: #d1d5db
```

**Gap**: No CSS variable for gap - currently hardcoded in template as Bootstrap class `gap-{{ gap }}`

**Recommendation**: 
1. Change `--inner-primary-width` default to `280px` (match spec)
2. Add `--inner-gap` variable (optional, defaults to Bootstrap gap-0/gap-3)
3. Consider adding `--inner-breakpoint` variable (advanced)

### 2.2 Responsive Behavior Breakdown

**Current Implementation** (from `_content-layout.scss`):

```scss
@media (max-width: 991px) {  // ❌ Wrong breakpoint (should be 767px)
  flex-direction: column !important;  // ❌ Wrong mode (should be offcanvas)

  .inner-primary,
  .inner-secondary {
    width: 100% !important;             // For stacking
    max-width: none !important;
    border: none !important;
    border-bottom: 1px solid var(--bs-border-color) !important;
  }
}
```

**What Should Happen** (per spec FR-007a):

1. **Above md (≥768px)**: In-flow layout
   - Sidebars are part of normal document flow
   - Can be collapsed (width reduction)
   - Flex layout: `[sidebar] [main] [sidebar]`

2. **Below md (<768px)**: Offcanvas mode
   - Sidebars slide in from off-page when toggled
   - Main content expands to full width
   - **Cannot collapse** (offcanvas takes precedence - FR-007b)
   - Requires Bootstrap offcanvas component integration

**Required Changes**:
1. Change breakpoint to `@media (max-width: 767px)` (Bootstrap md: 768px)
2. Remove `flex-direction: column` stacking
3. Add offcanvas-specific CSS:
   ```scss
   @media (max-width: 767px) {
     .content-sidebar-left,
     .content-sidebar-right {
       // Hide from flow
       position: fixed;
       transform: translateX(-100%);  // Off-page left
       // Or use Bootstrap .offcanvas classes
     }

     .content-sidebar-right {
       transform: translateX(100%);  // Off-page right
     }

     .content-main {
       width: 100%;  // Full width
     }
   }
   ```

4. Integrate Bootstrap offcanvas classes (`.offcanvas`, `.offcanvas-start`, `.offcanvas-end`)

### 2.3 Collapse Implementation Review

**Collapse Trigger**:
```scss
.inner-primary.collapsed {
  width: var(--inner-primary-min-width, 60px) !important;
  min-width: var(--inner-primary-min-width, 60px) !important;
  overflow-x: visible !important;  // ✅ Critical for dropdowns

  .inner-sidebar-content > *:not(.collapsed-only) {
    display: none;  // ✅ Hides all non-collapsed content
  }

  .expanded-only {
    display: none !important;  // ✅ Explicit hide
  }

  .collapsed-only {
    display: block !important;  // ✅ Show collapsed icons/content
  }
}
```

**Analysis** ✅:
- **Width Reduction**: Smooth transition to `min-width` (typically 60px for icons)
- **Content Visibility**: Proper show/hide logic for `.collapsed-only` and `.expanded-only`
- **Overflow Handling**: `overflow-x: visible` critical for dropdown menus in collapsed state
- **Transitions**: 0.3s ease on width change (not on content visibility to prevent flicker)

**Edge Case**: Direct child selector `.inner-sidebar-content > *:not(.collapsed-only)` means nested elements will still hide correctly. Good specificity.

**Missing**: No constraint to prevent collapse when in offcanvas mode (FR-007b). This requires JS logic.

---

## 3. Gaps vs Specification Requirements

### 3.1 Functional Requirements Coverage

| FR | Requirement | Status | Implementation Gap |
|----|-------------|--------|-------------------|
| FR-001 | Inner layout component in Django templates | ✅ Complete | Component exists and works |
| FR-002 | Default (unnamed) slot for main content | ✅ Complete | `{{ slot }}` implemented |
| FR-003 | Optional primary_sidebar slot (left) | ✅ Complete | `{{ primary_sidebar }}` implemented |
| FR-004 | Optional secondary_sidebar slot (right) | ✅ Complete | `{{ secondary_sidebar }}` implemented |
| FR-005 | Auto-expand content when no sidebars | ⚠️ Partial | Works via flexbox, but doesn't hide empty sidebar containers |
| FR-006 | Customization via data attributes | ❌ Missing | No data attribute reading/application logic |
| FR-007 | Responsive layout based on viewport | ⚠️ Partial | Has responsive breakpoint but wrong mode (stacking vs offcanvas) |
| FR-007a | Support hide (offcanvas) and collapse modes | ❌ Missing | Only collapse implemented, no offcanvas |
| FR-007b | Enforce collapse constraint (not while offcanvas) | ❌ Missing | No constraint logic |
| FR-008 | Integrate with pre-built sidebar components | ✅ Complete | Slot system allows any component |
| FR-009 | No rendering of empty sidebar containers | ❌ Missing | Empty slots render empty containers |
| FR-010 | Consistent spacing/alignment | ✅ Complete | Flexbox + gap handles this |
| FR-011 | Accessible with ARIA best practices | ❌ Missing | No ARIA landmarks, labels, or roles |
| FR-012 | Work within outer layout system | ✅ Complete | Renders correctly in `.app-main` |
| FR-013 | Semantic CSS class names per docs | ⚠️ Partial | Has semantic names but as aliases (inverted priority) |
| FR-014 | Visual boundaries between regions | ✅ Complete | CSS can add borders (theme-level) |
| FR-015 | Handle content overflow gracefully | ✅ Complete | `overflow-y: auto` on sidebars, `overflow-auto` on main |

**Summary**: 8/15 complete, 4/15 partial, 3/15 missing = **~53% coverage**

### 3.2 Critical Gaps for Spec Compliance

#### Gap 1: Offcanvas Mode (FR-007a) ❌ **CRITICAL**

**Current**: Sidebars stack vertically below 991px  
**Required**: Sidebars slide in from off-page below 768px (Bootstrap offcanvas)

**Changes Needed**:
1. **HTML Template**: Add offcanvas wrapper structure
   ```django-html
   {% if primary_sidebar %}
     {# Desktop: in-flow sidebar #}
     <aside class="content-sidebar-left d-none d-md-flex" role="complementary">
       {{ primary_sidebar }}
     </aside>
     
     {# Mobile: offcanvas #}
     <div class="offcanvas offcanvas-start d-md-none" 
          id="primarySidebarOffcanvas" 
          tabindex="-1"
          aria-labelledby="primarySidebarLabel">
       <div class="offcanvas-header">
         <button class="btn-close" data-bs-dismiss="offcanvas"></button>
       </div>
       <div class="offcanvas-body">
         {{ primary_sidebar }}
       </div>
     </div>
     
     {# Mobile: toggle button #}
     <button class="btn d-md-none" 
             data-bs-toggle="offcanvas" 
             data-bs-target="#primarySidebarOffcanvas">
       Toggle Sidebar
     </button>
   {% endif %}
   ```

2. **CSS**: Change breakpoint and remove stacking
   ```scss
   @media (max-width: 767px) {  // md breakpoint
     .content-sidebar-left,
     .content-sidebar-right {
       // Use Bootstrap offcanvas classes
     }
   }
   ```

3. **JavaScript**: Add offcanvas mode detection
   ```javascript
   const mdBreakpoint = window.matchMedia('(max-width: 767px)')
   
   mdBreakpoint.addEventListener('change', (e) => {
     if (e.matches) {
       // Switch to offcanvas mode
       // Remove .collapsed class (cannot collapse in offcanvas)
     } else {
       // Switch to in-flow mode
       // Restore collapse state from localStorage
     }
   })
   ```

**Complexity**: HIGH - requires structural HTML changes, CSS rework, JS logic

---

#### Gap 2: Empty Slot Detection (FR-009) ❌ **CRITICAL**

**Current**: `{{ primary_sidebar }}` and `{{ secondary_sidebar }}` always render (even if empty)  
**Required**: Do not render sidebar containers when slots are empty

**Problem**: Django-Cotton doesn't provide built-in empty slot detection. The `{{ primary_sidebar }}` variable will be an empty string `""` if the slot is not declared, but it still renders in the HTML as an empty text node.

**Potential Solutions**:

**Option A: Template-level conditional** (if Cotton supports it)
```django-html
{% if primary_sidebar %}  {# Check if slot has content #}
  <aside class="content-sidebar-left" role="complementary">
    {{ primary_sidebar }}
  </aside>
{% endif %}
```

**Option B: JavaScript detection** (post-render cleanup)
```javascript
document.querySelectorAll('.content-sidebar-left, .content-sidebar-right').forEach(sidebar => {
  if (sidebar.textContent.trim() === '') {
    sidebar.remove()  // Remove empty sidebar from DOM
  }
})
```

**Option C: CSS-only** (hide but don't remove)
```scss
.content-sidebar-left:empty,
.content-sidebar-right:empty {
  display: none;  // Hide empty sidebars
}
```

**Recommendation**: Use **Option A** if Cotton supports slot truthiness checks, otherwise **Option B** (JS cleanup) for robustness. Option C fails if slots render whitespace.

**Complexity**: MEDIUM - requires testing Cotton slot behavior

---

#### Gap 3: Data Attribute Configuration (FR-006) ❌ **IMPORTANT**

**Current**: No data attribute reading or application  
**Required**: Support `data-primary-width`, `data-secondary-width`, `data-breakpoint`, `data-gap`, etc.

**Implementation**:

1. **JavaScript** (read and apply data attributes on init):
   ```javascript
   function applyDataAttributes(container) {
     const primaryWidth = container.dataset.primaryWidth
     const secondaryWidth = container.dataset.secondaryWidth
     const breakpoint = container.dataset.breakpoint
     const gap = container.dataset.gap
     
     if (primaryWidth) {
       container.style.setProperty('--inner-primary-width', primaryWidth)
     }
     if (secondaryWidth) {
       container.style.setProperty('--inner-secondary-width', secondaryWidth)
     }
     // ... more attributes
   }
   
   document.querySelectorAll('.content-shell').forEach(applyDataAttributes)
   ```

2. **Template** (document supported attributes):
   ```django-html
   <c-layouts.inner
     data-primary-width="320px"
     data-secondary-width="280px"
     data-breakpoint="lg"
     data-gap="4">
     {# ... #}
   </c-layouts.inner>
   ```

**Attributes to Support**:
- `data-primary-width` → `--inner-primary-width`
- `data-primary-max-width` → `--inner-primary-max-width`
- `data-primary-min-width` → `--inner-primary-min-width`
- `data-secondary-width` → `--inner-secondary-width`
- `data-secondary-max-width` → `--inner-secondary-max-width`
- `data-secondary-min-width` → `--inner-secondary-min-width`
- `data-breakpoint` → Control responsive breakpoint (md/lg/xl)
- `data-gap` → Control flex gap between columns

**Complexity**: MEDIUM - straightforward JS implementation

---

#### Gap 4: Collapse Constraint (FR-007b) ❌ **IMPORTANT**

**Current**: No enforcement of "cannot collapse while in offcanvas mode"  
**Required**: When sidebar is in offcanvas mode, it cannot be collapsed

**Implementation**:

```javascript
function toggleSidebar(sidebar, storageKey) {
  // Check if in offcanvas mode
  const isOffcanvasMode = window.innerWidth < 768
  
  if (isOffcanvasMode) {
    console.warn('Cannot collapse sidebar in offcanvas mode')
    return  // Prevent collapse
  }
  
  // Normal collapse logic
  sidebar.classList.toggle('collapsed')
  const isCollapsed = sidebar.classList.contains('collapsed')
  saveState(storageKey, isCollapsed)
}

// On viewport resize, restore collapse state only if not in offcanvas mode
window.addEventListener('resize', debounce(() => {
  const isOffcanvasMode = window.innerWidth < 768
  
  if (!isOffcanvasMode) {
    // Restore collapse state from localStorage
    restoreSidebarState(leftSidebar, STORAGE_KEY_LEFT)
    restoreSidebarState(rightSidebar, STORAGE_KEY_RIGHT)
  } else {
    // Remove .collapsed class (offcanvas mode)
    leftSidebar.classList.remove('collapsed')
    rightSidebar.classList.remove('collapsed')
  }
}, 150))
```

**Complexity**: LOW - simple conditional in toggle function

---

#### Gap 5: ARIA Landmarks & Accessibility (FR-011) ❌ **IMPORTANT**

**Current**: No ARIA attributes on layout regions  
**Required**: Proper ARIA landmarks and labels per WCAG 2.1 Level AA

**Changes Needed** (in HTML template):

```django-html
<div class="content-shell d-flex gap-{{ gap }} {{ class }}" {{ attrs }}>
  
  {% if primary_sidebar %}
    <aside class="content-sidebar-left"
           role="complementary"
           aria-label="Primary sidebar navigation">
      {{ primary_sidebar }}
    </aside>
  {% endif %}
  
  <main class="content-main flex-grow-1 overflow-auto" 
        role="main"
        aria-label="Main content">
    {{ slot }}
  </main>
  
  {% if secondary_sidebar %}
    <aside class="content-sidebar-right"
           role="complementary"
           aria-label="Secondary sidebar">
      {{ secondary_sidebar }}
    </aside>
  {% endif %}
  
</div>
```

**Additional ARIA** (for toggle buttons):
```html
<button class="content-sidebar-toggle-left"
        aria-label="Toggle primary sidebar collapse"
        aria-expanded="true"
        aria-controls="primarySidebarContent">
  <i class="bi bi-chevron-left"></i>
</button>
```

**Complexity**: LOW - template markup additions

---

#### Gap 6: Default Width Mismatch ⚠️ **MINOR**

**Current**: `--inner-primary-width: 250px`  
**Spec**: 280px for primary_sidebar, 250px for secondary_sidebar

**Fix**: Change CSS variable default in `_content-layout.scss`:
```scss
.inner-primary {
  width: var(--inner-primary-width, 280px);  // Changed from 250px
  // ...
}
```

**Complexity**: TRIVIAL

---

#### Gap 7: Responsive Breakpoint ⚠️ **MINOR**

**Current**: `@media (max-width: 991px)` (Bootstrap lg - 1px)  
**Spec**: `@media (max-width: 767px)` (Bootstrap md - 1px)

**Fix**: Change all responsive media queries:
```scss
@media (max-width: 767px) {  // Changed from 991px
  // ...
}
```

**Locations to Fix**:
- `_content-layout.scss:7`
- `_old_layout.scss:334` (if still in use)

**Complexity**: TRIVIAL

---

## 4. Integration Points

### 4.1 Outer Layout Integration

**Status**: ✅ **Works correctly**

The inner layout component is designed to render within the outer layout's `.app-main` container:

```html
<div class="app-shell">
  <aside class="site-sidebar"><!-- Outer sidebar --></aside>
  <div class="app-column">
    <nav class="site-navbar"><!-- Outer navbar --></nav>
    <main class="app-main">
      <!-- Inner layout renders here -->
      <c-layouts.inner>
        <c-slot name="primary_sidebar"><!-- Inner sidebar --></c-slot>
        Main content
        <c-slot name="secondary_sidebar"><!-- Inner sidebar --></c-slot>
      </c-layouts.inner>
    </main>
  </div>
</div>
```

**Key Integration Points**:
1. **Flex Container**: `.app-main` is a flex container, `.content-shell` is a flex child
2. **Height**: `.app-main` has `flex: 1` (fills available height), `.content-shell` inherits
3. **Scrolling**: Both outer `.app-main` and inner `.content-main` have `overflow-auto`
4. **Spacing**: Inner layout respects outer layout padding/margins

**No Conflicts**: Inner layout is entirely independent of outer layout structure. No class name collisions, no layout interference.

---

### 4.2 Bootstrap 5 Dependencies

**Current Dependencies**:

1. **Flexbox Utilities**: `d-flex`, `flex-grow-1`, `flex-shrink-0`, `gap-*`
2. **Spacing Utilities**: `p-3`, `m-2`, etc. (used in examples, not in component itself)
3. **Border Utilities**: `border`, `border-start`, `border-end` (used in examples)
4. **Responsive Utilities**: `d-none`, `d-md-flex`, etc. (needed for offcanvas implementation)
5. **Offcanvas Component**: `.offcanvas`, `.offcanvas-start`, `.offcanvas-end`, `.offcanvas-body` (not yet used, but required for FR-007a)

**Bootstrap JavaScript Dependencies** (for offcanvas):
- Bootstrap's `Offcanvas` JavaScript component
- Requires `data-bs-toggle="offcanvas"` and `data-bs-target` attributes

**Assessment**: Current implementation has **light Bootstrap dependency** (just utility classes). Implementing offcanvas mode will add **moderate Bootstrap JS dependency**.

**Alternative**: Could implement custom offcanvas (slide-in transitions) without Bootstrap JS, but this duplicates effort and diverges from Bootstrap standards. **Recommendation: Use Bootstrap offcanvas**.

---

### 4.3 Django-Cotton Slot Handling

**Current Pattern**:

```django-html
<c-vars gap="0" class />
<div class="content-shell d-flex gap-{{ gap }} {{ class }}" {{ attrs }}>
  {{ primary_sidebar }}  <!-- Named slot -->
  <div class="content-main flex-grow-1 overflow-auto">{{ slot }}</div>  <!-- Default slot -->
  {{ secondary_sidebar }}  <!-- Named slot -->
</div>
```

**How Cotton Slots Work**:
1. **Default Slot**: `{{ slot }}` renders content wrapped directly in component tags
2. **Named Slots**: `{{ primary_sidebar }}` renders content from `<c-slot name="primary_sidebar">`
3. **Empty Slots**: If slot is not declared, variable is empty string `""`

**Usage Pattern**:
```django-html
<c-layouts.inner>
  <c-slot name="primary_sidebar">
    <c-sidebar.default>Sidebar content</c-sidebar.default>
  </c-slot>
  
  Main page content
  
  <c-slot name="secondary_sidebar">
    Additional sidebar content
  </c-slot>
</c-layouts.inner>
```

**Issue with Empty Detection**: Django-Cotton doesn't provide a way to check if a slot has content before rendering. The `{{ primary_sidebar }}` variable will always render (even if empty).

**Solutions**:
1. **Template conditional**: `{% if primary_sidebar %}` (check if Cotton supports this)
2. **JavaScript cleanup**: Remove empty sidebar elements post-render
3. **CSS hide**: `.content-sidebar-left:empty { display: none; }` (fragile, breaks with whitespace)

**Recommendation**: Test Cotton slot truthiness with `{% if primary_sidebar %}`. If not supported, use JavaScript cleanup in `inner_layout.js`.

---

## 5. Recommendations & Next Steps

### 5.1 Priority Ranking

| Priority | Gap | Impact | Effort | Recommendation |
|----------|-----|--------|--------|----------------|
| **P0** | Offcanvas mode (FR-007a) | HIGH | HIGH | Implement in Phase 1 - core functionality |
| **P0** | Empty slot detection (FR-009) | HIGH | MEDIUM | Implement in Phase 1 - prevents layout bugs |
| **P1** | Data attributes (FR-006) | MEDIUM | MEDIUM | Implement in Phase 2 - enables customization |
| **P1** | ARIA landmarks (FR-011) | MEDIUM | LOW | Implement in Phase 1 - quick accessibility win |
| **P1** | Collapse constraint (FR-007b) | MEDIUM | LOW | Implement with offcanvas mode |
| **P2** | Default width fix | LOW | TRIVIAL | Fix immediately - one-line change |
| **P2** | Breakpoint fix | LOW | TRIVIAL | Fix immediately - one-line change |
| **P2** | Class naming inversion | LOW | LOW | Refactor in Phase 3 - backwards-compat concern |

### 5.2 Implementation Phases

#### Phase 1: Core Functionality (P0 + Quick Wins)
**Goal**: Meet critical spec requirements for MVP

1. **Fix default widths** (280px primary, 250px secondary)
2. **Fix responsive breakpoint** (767px instead of 991px)
3. **Add ARIA landmarks** (role, aria-label on regions)
4. **Implement empty slot detection** (test Cotton conditionals or JS cleanup)
5. **Begin offcanvas mode** (HTML structure, Bootstrap integration)

**Estimated Effort**: 8-12 hours

---

#### Phase 2: Offcanvas & Configuration
**Goal**: Complete responsive behavior and customization

1. **Complete offcanvas mode** (HTML, CSS, JS)
2. **Implement collapse constraint** (cannot collapse in offcanvas)
3. **Add data attribute system** (read and apply config)
4. **Add toggle buttons** (collapse and offcanvas)
5. **Test responsive transitions** (in-flow ↔ offcanvas)

**Estimated Effort**: 12-16 hours

---

#### Phase 3: Polish & Refactoring
**Goal**: Production-ready quality

1. **Invert class naming** (make `.content-*` primary, alias `.inner-*`)
2. **Comprehensive testing** (unit tests, integration tests)
3. **Documentation** (usage examples, API reference)
4. **Accessibility audit** (automated tools + manual testing)
5. **Performance optimization** (debounce resize listeners, etc.)

**Estimated Effort**: 8-12 hours

---

### 5.3 Testing Strategy

#### Unit Tests (Component Rendering)
```python
# tests/test_inner_layout_component.py

def test_inner_layout_renders_without_sidebars():
    """FR-001, FR-002: Basic content-only layout"""
    html = render_component('layouts/inner', content='<p>Main content</p>')
    assert 'content-shell' in html
    assert 'content-main' in html
    assert '<p>Main content</p>' in html

def test_inner_layout_renders_with_primary_sidebar():
    """FR-003: Single sidebar layout"""
    html = render_component('layouts/inner', 
                           primary_sidebar='<nav>Sidebar</nav>',
                           content='<p>Main</p>')
    assert 'content-sidebar-left' in html
    assert '<nav>Sidebar</nav>' in html

def test_inner_layout_hides_empty_sidebars():
    """FR-009: Empty slot detection"""
    html = render_component('layouts/inner', 
                           primary_sidebar='',  # Empty slot
                           content='<p>Main</p>')
    # Empty sidebar should not render or be hidden
    assert 'content-sidebar-left' not in html or \
           'style="display: none"' in html

def test_data_attributes_apply_custom_widths():
    """FR-006: Data attribute configuration"""
    html = render_component('layouts/inner',
                           attrs={'data-primary-width': '320px'},
                           primary_sidebar='<nav>Nav</nav>',
                           content='<p>Main</p>')
    assert 'data-primary-width="320px"' in html
```

#### Integration Tests (Responsive Behavior)
```python
def test_offcanvas_mode_below_md_breakpoint():
    """FR-007a: Offcanvas mode at mobile sizes"""
    # Simulate mobile viewport
    html = render_component_with_viewport('layouts/inner', width=767)
    assert 'offcanvas' in html
    assert 'd-md-none' in html  # Offcanvas hidden on desktop

def test_cannot_collapse_in_offcanvas_mode():
    """FR-007b: Collapse constraint"""
    # JS test: trigger collapse toggle at mobile size
    # Should not apply .collapsed class
    pass
```

#### Accessibility Tests
```python
def test_aria_landmarks_present():
    """FR-011: ARIA landmarks"""
    html = render_component('layouts/inner',
                           primary_sidebar='<nav>Nav</nav>',
                           content='<p>Main</p>')
    assert 'role="complementary"' in html
    assert 'role="main"' in html
    assert 'aria-label=' in html
```

---

### 5.4 Decision Points

#### Decision 1: Offcanvas Implementation Approach

**Option A: Bootstrap Offcanvas** ✅ **RECOMMENDED**
- **Pros**: Standard, well-tested, accessible, no custom JS
- **Cons**: Adds Bootstrap JS dependency, less customization
- **Effort**: Low-Medium (integrate existing Bootstrap component)

**Option B: Custom Offcanvas**
- **Pros**: No Bootstrap JS dependency, full control
- **Cons**: Duplicate effort, harder accessibility, more testing
- **Effort**: High (build from scratch)

**Recommendation**: **Option A** - Use Bootstrap offcanvas. It's battle-tested, accessible, and aligns with the Bootstrap ecosystem already in use.

---

#### Decision 2: Empty Slot Detection Method

**Option A: Template Conditional** (if Cotton supports)
```django-html
{% if primary_sidebar %}
  <aside class="content-sidebar-left">{{ primary_sidebar }}</aside>
{% endif %}
```
- **Pros**: Clean, no JS, no empty DOM elements
- **Cons**: Unknown if Cotton supports slot truthiness checks

**Option B: JavaScript Cleanup**
```javascript
document.querySelectorAll('.content-sidebar-left, .content-sidebar-right').forEach(el => {
  if (el.textContent.trim() === '') el.remove()
})
```
- **Pros**: Guaranteed to work, post-render cleanup
- **Cons**: Slight flash of empty element, requires JS

**Option C: CSS Hide**
```scss
.content-sidebar-left:empty,
.content-sidebar-right:empty {
  display: none;
}
```
- **Pros**: No JS, simple
- **Cons**: Fragile (breaks with whitespace), doesn't remove from DOM

**Recommendation**: **Test Option A first** (template conditional). If Cotton doesn't support slot truthiness, fall back to **Option B** (JS cleanup) for robustness.

---

#### Decision 3: Class Naming Strategy

**Current**: Old `.inner-*` classes are primary, new `.content-*` classes are SCSS aliases via `@extend`

**Option A: Invert Now** (make `.content-*` primary)
- **Pros**: Aligns with spec immediately, cleaner architecture
- **Cons**: Breaking change for existing users (even with aliases)

**Option B: Invert Later** (Phase 3)
- **Pros**: Focus on functionality first, less risk
- **Cons**: Technical debt, confusing during development

**Option C: Keep Current** (`.inner-*` primary)
- **Pros**: No breaking changes, backwards-compat
- **Cons**: Doesn't align with spec, confusing naming

**Recommendation**: **Option B** - Keep current naming for Phase 1-2, invert in Phase 3. Document clearly that `.content-*` is the **semantic name** and `.inner-*` is **legacy alias**. This reduces risk while delivering functionality.

---

## 6. Conclusion

The existing inner layout implementation provides a **solid foundation** with working collapse functionality, smooth transitions, and good code quality. However, it has **critical gaps** for spec compliance:

1. **No offcanvas mode** (FR-007a) - sidebars stack instead of sliding in
2. **No empty slot detection** (FR-009) - empty sidebars render empty containers
3. **No data attribute configuration** (FR-006) - cannot customize via data attributes
4. **Missing ARIA landmarks** (FR-011) - accessibility concerns
5. **Wrong breakpoint** (991px vs 767px) - misaligned with spec
6. **Wrong default width** (250px vs 280px for primary sidebar)

**Status**: ~40-53% complete for spec requirements

**Effort to Complete**: 28-40 hours across 3 phases

**Critical Path**: Offcanvas mode implementation is the highest priority and highest effort. Empty slot detection is second priority. Everything else is lower effort and can be done incrementally.

**Risk Areas**:
- Django-Cotton slot behavior (unknown if supports emptiness checks)
- Bootstrap offcanvas integration (adds JS dependency)
- Backwards compatibility (class naming inversion concerns)

**Confidence Level**: HIGH - Implementation is straightforward with clear requirements and existing patterns to follow. Main unknowns are Cotton slot behavior and Bootstrap offcanvas integration, both of which are solvable.

---

**Report Compiled**: December 23, 2025  
**Analyst**: GitHub Copilot  
**Next Step**: Review with team and prioritize Phase 1 implementation
